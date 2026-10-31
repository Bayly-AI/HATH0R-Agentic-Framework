"""Embedded ELT Engine Adapter for Cognitive Substrate and AgentGraph."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from hath0r_engine.graph.knowledge_graph import KnowledgeGraph, KnowledgeNode
from hath0r_engine.orchestration.journal import EventRecord


class ELTEngineAdapter:
    """Bridges the Hath0r Cognitive Substrate to the Embedded ELT Raw Staging Store."""

    def __init__(self, db_path: Optional[Path | str] = None) -> None:
        if db_path is None:
            # Fallback path under root .hath0r/cache/ingest/raw_staging.sqlite
            self.db_path = Path.cwd() / ".hath0r" / "cache" / "ingest" / "raw_staging.sqlite"
        else:
            self.db_path = Path(db_path)

        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=30.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        return conn

    def _init_db(self) -> None:
        """Ensure schema compatibility with CLI raw_records."""
        with self._get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS raw_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_uri TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    content_sha256 TEXT NOT NULL UNIQUE,
                    raw_payload TEXT NOT NULL,
                    content_length INTEGER NOT NULL,
                    metadata_json TEXT NOT NULL,
                    ingested_at REAL NOT NULL,
                    status TEXT NOT NULL DEFAULT 'staged'
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS projection_states (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    record_id INTEGER NOT NULL REFERENCES raw_records(id) ON DELETE CASCADE,
                    projection_name TEXT NOT NULL,
                    projected_at REAL NOT NULL,
                    status TEXT NOT NULL DEFAULT 'synced',
                    error_message TEXT,
                    UNIQUE(record_id, projection_name)
                )
                """
            )
            conn.commit()

    @staticmethod
    def _compute_sha256(content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def stage_event(
        self,
        event: EventRecord | Dict[str, Any],
        source_uri: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Stage an immutable execution event into raw staging for non-destructive history."""
        if isinstance(event, EventRecord):
            payload_str = json.dumps(event.to_dict())
            uri = source_uri or f"orchestration/{event.workflow_id}/{event.seq_num}"
            meta = {"workflow_id": event.workflow_id, "step_name": event.step_name}
        else:
            payload_str = json.dumps(event)
            w_id = event.get("workflow_id", "default")
            seq = event.get("seq_num", int(time.time() * 1000))
            uri = source_uri or f"orchestration/{w_id}/{seq}"
            meta = {"workflow_id": w_id}

        sha = self._compute_sha256(payload_str)
        now = time.time()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM raw_records WHERE content_sha256 = ?", (sha,))
            row = cursor.fetchone()
            if row:
                return {"record_id": row[0], "status": "existing", "is_duplicate": True}

            cursor.execute(
                """
                INSERT INTO raw_records (
                    source_uri, source_type, content_sha256, raw_payload,
                    content_length, metadata_json, ingested_at, status
                ) VALUES (?, 'event', ?, ?, ?, ?, ?, 'staged')
                """,
                (uri, sha, payload_str, len(payload_str), json.dumps(meta), now),
            )
            rec_id = cursor.lastrowid
            conn.commit()
            return {"record_id": rec_id, "status": "staged", "is_duplicate": False}

    def stage_document(
        self,
        path: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Stage a raw document or schema contract into raw staging."""
        meta = metadata or {}
        sha = self._compute_sha256(content)
        now = time.time()

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM raw_records WHERE content_sha256 = ?", (sha,))
            row = cursor.fetchone()
            if row:
                return {"record_id": row[0], "status": "existing", "is_duplicate": True}

            cursor.execute(
                """
                INSERT INTO raw_records (
                    source_uri, source_type, content_sha256, raw_payload,
                    content_length, metadata_json, ingested_at, status
                ) VALUES (?, 'docs', ?, ?, ?, ?, ?, 'staged')
                """,
                (path, sha, content, len(content), json.dumps(meta), now),
            )
            rec_id = cursor.lastrowid
            conn.commit()
            return {"record_id": rec_id, "status": "staged", "is_duplicate": False}

    def project_to_agentgraph(self, knowledge_graph: KnowledgeGraph) -> int:
        """Project unprojected raw documentation records into the AgentGraph KnowledgeGraph."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT r.id, r.source_uri, r.raw_payload, r.metadata_json
                FROM raw_records r
                LEFT JOIN projection_states p ON r.id = p.record_id AND p.projection_name = 'agentgraph'
                WHERE r.source_type = 'docs' AND (p.id IS NULL OR p.status = 'dirty')
                """
            )
            rows = cursor.fetchall()
            projected_count = 0

            for row in rows:
                rec_id = row[0]
                source_uri = row[1]
                payload = row[2]
                try:
                    meta = json.loads(row[3])
                except Exception:
                    meta = {}

                # Create entity node in KnowledgeGraph
                node_id = f"doc:{source_uri.replace('/', '_').replace('.', '_')}"
                title = Path(source_uri).stem
                for line in payload.splitlines()[:10]:
                    if line.strip().startswith("# "):
                        title = line.strip()[2:].strip()
                        break

                knode = KnowledgeNode(
                    id=node_id,
                    type="document",
                    title=title,
                    path=source_uri,
                    content=payload,
                    properties=meta,
                )
                knowledge_graph.add_node(knode)

                # Mark projection synced
                cursor.execute(
                    """
                    INSERT INTO projection_states (record_id, projection_name, projected_at, status)
                    VALUES (?, 'agentgraph', ?, 'synced')
                    ON CONFLICT(record_id, projection_name) DO UPDATE SET
                        projected_at = excluded.projected_at,
                        status = 'synced'
                    """,
                    (rec_id, time.time()),
                )
                projected_count += 1

            conn.commit()
            return projected_count

    def get_events_for_reflection(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch raw event history to feed MemoryGraph reflection consolidation."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, source_uri, raw_payload, ingested_at
                FROM raw_records
                WHERE source_type = 'event'
                ORDER BY id ASC
                LIMIT ?
                """,
                (limit,),
            )
            events: List[Dict[str, Any]] = []
            for row in cursor.fetchall():
                try:
                    data = json.loads(row["raw_payload"])
                except Exception:
                    data = {"raw": row["raw_payload"]}
                events.append({
                    "record_id": row["id"],
                    "source_uri": row["source_uri"],
                    "ingested_at": row["ingested_at"],
                    "payload": data,
                })
            return events

    def stage_records_batch(
        self,
        records: List[Dict[str, Any]],
        source_type: str = "batch_airflow",
        default_uri_prefix: str = "airflow/batch",
    ) -> Dict[str, Any]:
        """Stage a collection of raw records in a single database transaction.

        Returns summary of ingested, duplicates, and total records.
        """
        now = time.time()
        staged_count = 0
        duplicate_count = 0
        staged_ids: List[int] = []

        with self._get_connection() as conn:
            cursor = conn.cursor()
            for idx, item in enumerate(records):
                if isinstance(item, dict):
                    payload_val = item.get("payload", item)
                    payload_str = json.dumps(payload_val) if isinstance(payload_val, (dict, list)) else str(payload_val)
                    uri = item.get("source_uri", f"{default_uri_prefix}/{int(now * 1000)}_{idx}")
                    meta = item.get("metadata", {})
                    s_type = item.get("source_type", source_type)
                else:
                    payload_str = str(item)
                    uri = f"{default_uri_prefix}/{int(now * 1000)}_{idx}"
                    meta = {}
                    s_type = source_type

                sha = self._compute_sha256(payload_str)
                cursor.execute("SELECT id FROM raw_records WHERE content_sha256 = ?", (sha,))
                row = cursor.fetchone()
                if row:
                    duplicate_count += 1
                else:
                    cursor.execute(
                        """
                        INSERT INTO raw_records (
                            source_uri, source_type, content_sha256, raw_payload,
                            content_length, metadata_json, ingested_at, status
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, 'staged')
                        """,
                        (uri, s_type, sha, payload_str, len(payload_str), json.dumps(meta), now),
                    )
                    staged_count += 1
                    if cursor.lastrowid is not None:
                        staged_ids.append(cursor.lastrowid)

            conn.commit()

        return {
            "total_processed": len(records),
            "staged_count": staged_count,
            "duplicate_count": duplicate_count,
            "staged_ids": staged_ids,
        }

    def stage_batch_archive(
        self,
        archive_path: Path | str,
        source_type: str = "batch_airflow",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Ingest an external batch archive file (JSON lines, JSON array, or plain text).

        Commonly emitted by enterprise Airflow ELT extraction tasks.
        """
        path = Path(archive_path)
        if not path.exists():
            raise FileNotFoundError(f"Batch archive not found at: {path}")

        records: List[Dict[str, Any]] = []
        raw_text = path.read_text(encoding="utf-8")

        # Try parsing as JSON array
        try:
            parsed = json.loads(raw_text)
            if isinstance(parsed, list):
                for idx, entry in enumerate(parsed):
                    records.append({
                        "source_uri": f"{path.name}#{idx}",
                        "source_type": source_type,
                        "payload": entry,
                        "metadata": metadata or {"archive_path": str(path)},
                    })
            elif isinstance(parsed, dict):
                records.append({
                    "source_uri": f"{path.name}#0",
                    "source_type": source_type,
                    "payload": parsed,
                    "metadata": metadata or {"archive_path": str(path)},
                })
        except json.JSONDecodeError:
            # Fallback to JSONL line-by-line
            for idx, line in enumerate(raw_text.splitlines()):
                line = line.strip()
                if not line:
                    continue
                try:
                    line_data = json.loads(line)
                except Exception:
                    line_data = line
                records.append({
                    "source_uri": f"{path.name}#line_{idx + 1}",
                    "source_type": source_type,
                    "payload": line_data,
                    "metadata": metadata or {"archive_path": str(path), "line_num": idx + 1},
                })

        return self.stage_records_batch(records, source_type=source_type)

