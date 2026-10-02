"""Immutable Event Journal and Checkpointing Store for Durable Execution."""

from __future__ import annotations

import json
import sqlite3
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class EventType(str, Enum):
    """Event types recorded in the immutable execution journal."""

    WORKFLOW_STARTED = "workflow_started"
    STEP_STARTED = "step_started"
    STEP_COMPLETED = "step_completed"
    STEP_FAILED = "step_failed"
    HUMAN_PAUSED = "human_paused"
    HUMAN_RESUMED = "human_resumed"
    STATE_MUTATED = "state_mutated"
    WORKFLOW_COMPLETED = "workflow_completed"
    WORKFLOW_FAILED = "workflow_failed"


@dataclass
class EventRecord:
    """Individual immutable journal event record."""

    workflow_id: str
    seq_num: int
    event_type: EventType
    event_id: str = field(default_factory=lambda: f"evt-{uuid.uuid4().hex[:12]}")
    step_name: Optional[str] = None
    idempotency_key: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["event_type"] = self.event_type.value
        return data


class EventJournal:
    """SQLite-backed append-only event journal ensuring deterministic replay and step memoization."""

    def __init__(self, db_path: str | Path = ":memory:") -> None:
        self.db_path = str(db_path)
        if self.db_path != ":memory:":
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS workflow_events (
                    event_id TEXT PRIMARY KEY,
                    workflow_id TEXT NOT NULL,
                    seq_num INTEGER NOT NULL,
                    event_type TEXT NOT NULL,
                    step_name TEXT,
                    idempotency_key TEXT,
                    payload_json TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                );
                """
            )
            self.conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_workflow_seq
                ON workflow_events (workflow_id, seq_num);
                """
            )
            self.conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_workflow_idempotency
                ON workflow_events (workflow_id, idempotency_key);
                """
            )

    def append_event(
        self,
        workflow_id: str,
        event_type: EventType,
        step_name: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> EventRecord:
        """Append an event record to the journal with incremented sequence number."""
        with self.conn:
            cur = self.conn.execute(
                "SELECT COALESCE(MAX(seq_num), 0) + 1 FROM workflow_events WHERE workflow_id = ?",
                (workflow_id,),
            )
            seq_num = cur.fetchone()[0]

            event = EventRecord(
                workflow_id=workflow_id,
                seq_num=seq_num,
                event_type=event_type,
                step_name=step_name,
                idempotency_key=idempotency_key,
                payload=payload or {},
            )

            self.conn.execute(
                """
                INSERT INTO workflow_events (
                    event_id, workflow_id, seq_num, event_type, step_name, idempotency_key, payload_json, timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.event_id,
                    event.workflow_id,
                    event.seq_num,
                    event.event_type.value,
                    event.step_name,
                    event.idempotency_key,
                    json.dumps(event.payload),
                    event.timestamp,
                ),
            )
            return event

    def get_events(self, workflow_id: str) -> List[EventRecord]:
        """Retrieve all events for a workflow in strict sequence order."""
        cur = self.conn.execute(
            """
            SELECT event_id, workflow_id, seq_num, event_type, step_name, idempotency_key, payload_json, timestamp
            FROM workflow_events
            WHERE workflow_id = ?
            ORDER BY seq_num ASC
            """,
            (workflow_id,),
        )
        records = []
        for row in cur.fetchall():
            records.append(
                EventRecord(
                    event_id=row["event_id"],
                    workflow_id=row["workflow_id"],
                    seq_num=row["seq_num"],
                    event_type=EventType(row["event_type"]),
                    step_name=row["step_name"],
                    idempotency_key=row["idempotency_key"],
                    payload=json.loads(row["payload_json"]),
                    timestamp=row["timestamp"],
                )
            )
        return records

    def find_step_result(self, workflow_id: str, idempotency_key: str) -> Optional[Dict[str, Any]]:
        """Look up memoized output of a previously completed step."""
        cur = self.conn.execute(
            """
            SELECT payload_json FROM workflow_events
            WHERE workflow_id = ? AND idempotency_key = ? AND event_type = ?
            ORDER BY seq_num DESC LIMIT 1
            """,
            (workflow_id, idempotency_key, EventType.STEP_COMPLETED.value),
        )
        row = cur.fetchone()
        if row:
            payload = json.loads(row["payload_json"])
            return payload.get("result")
        return None

    def close(self) -> None:
        """Close database connection."""
        self.conn.close()
