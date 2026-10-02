"""Event-Sourced Durable Workflow Engine and State Machine."""

from __future__ import annotations

from enum import Enum
from typing import Any, Callable, Dict, Optional, TypeVar

from hath0r_engine.orchestration.hibernation import (
    HumanGateRequest,
    WorkflowSuspendedException,
)
from hath0r_engine.orchestration.journal import EventJournal, EventType

T = TypeVar("T")


class WorkflowStatus(str, Enum):
    """Execution status of a durable workflow."""

    INITIALIZED = "initialized"
    RUNNING = "running"
    SUSPENDED = "suspended"
    COMPLETED = "completed"
    FAILED = "failed"


class DurableWorkflowEngine:
    """Deterministic event-sourced workflow state machine."""

    def __init__(
        self,
        workflow_id: str,
        journal: Optional[EventJournal] = None,
        auto_start: bool = True,
    ) -> None:
        self.workflow_id = workflow_id
        self.journal = journal or EventJournal(":memory:")
        self.status = WorkflowStatus.INITIALIZED
        self.state: Dict[str, Any] = {}
        self.output: Optional[Any] = None
        self.error: Optional[str] = None

        # Reconstruct in-flight state from journal history
        self.replay()

        if auto_start and self.status == WorkflowStatus.INITIALIZED:
            self._start()

    def _start(self) -> None:
        """Record workflow start event."""
        self.journal.append_event(
            workflow_id=self.workflow_id,
            event_type=EventType.WORKFLOW_STARTED,
            payload={"workflow_id": self.workflow_id},
        )
        self.status = WorkflowStatus.RUNNING

    def replay(self) -> None:
        """Replay all historic journal events to reconstruct exact workflow state."""
        events = self.journal.get_events(self.workflow_id)
        if not events:
            return

        for evt in events:
            if evt.event_type == EventType.WORKFLOW_STARTED:
                self.status = WorkflowStatus.RUNNING
            elif evt.event_type == EventType.HUMAN_PAUSED:
                self.status = WorkflowStatus.SUSPENDED
            elif evt.event_type == EventType.HUMAN_RESUMED:
                self.status = WorkflowStatus.RUNNING
            elif evt.event_type == EventType.STATE_MUTATED:
                key = evt.payload.get("key")
                val = evt.payload.get("value")
                if key:
                    self.state[key] = val
            elif evt.event_type == EventType.WORKFLOW_COMPLETED:
                self.status = WorkflowStatus.COMPLETED
                self.output = evt.payload.get("output")
            elif evt.event_type == EventType.WORKFLOW_FAILED:
                self.status = WorkflowStatus.FAILED
                self.error = evt.payload.get("error")

    def run_step(
        self,
        step_name: str,
        fn: Callable[[], T],
        idempotency_key: Optional[str] = None,
    ) -> T:
        """Execute a deterministic step with automatic memoization / replay recovery."""
        if self.status in (WorkflowStatus.COMPLETED, WorkflowStatus.FAILED):
            raise RuntimeError(f"Cannot run step '{step_name}'; workflow is {self.status.value}.")

        key = idempotency_key or f"step:{step_name}"

        # 1. Check for previously memoized completion in journal
        cached_result = self.journal.find_step_result(self.workflow_id, key)
        if cached_result is not None:
            return cached_result  # type: ignore[return-value]

        # 2. Record step start
        self.journal.append_event(
            workflow_id=self.workflow_id,
            event_type=EventType.STEP_STARTED,
            step_name=step_name,
            idempotency_key=key,
        )

        try:
            # 3. Execute function
            result = fn()

            # 4. Record step completion with result
            self.journal.append_event(
                workflow_id=self.workflow_id,
                event_type=EventType.STEP_COMPLETED,
                step_name=step_name,
                idempotency_key=key,
                payload={"result": result},
            )
            return result
        except Exception as err:
            self.journal.append_event(
                workflow_id=self.workflow_id,
                event_type=EventType.STEP_FAILED,
                step_name=step_name,
                idempotency_key=key,
                payload={"error": str(err)},
            )
            raise

    def pause_for_human(
        self,
        gate_name: str,
        prompt: str,
        required_role: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Suspend workflow execution until an external human approval signal is recorded."""
        # Check if approval already recorded in event log
        events = self.journal.get_events(self.workflow_id)
        for evt in events:
            if evt.event_type == EventType.HUMAN_RESUMED and evt.payload.get("gate_name") == gate_name:
                self.status = WorkflowStatus.RUNNING
                return evt.payload

        # No approval signal found -> record pause event and suspend
        gate_req = HumanGateRequest(
            gate_name=gate_name,
            prompt=prompt,
            required_role=required_role,
        )

        self.journal.append_event(
            workflow_id=self.workflow_id,
            event_type=EventType.HUMAN_PAUSED,
            step_name=gate_name,
            payload=gate_req.to_dict(),
        )
        self.status = WorkflowStatus.SUSPENDED
        raise WorkflowSuspendedException(gate_req)

    def signal_human_approval(
        self,
        gate_name: str,
        approved: bool,
        payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Signal approval or rejection to resume a suspended human gate."""
        data = {
            "gate_name": gate_name,
            "approved": approved,
            "decision_payload": payload or {},
        }
        self.journal.append_event(
            workflow_id=self.workflow_id,
            event_type=EventType.HUMAN_RESUMED,
            step_name=gate_name,
            payload=data,
        )
        self.status = WorkflowStatus.RUNNING

    def mutate_state(self, key: str, value: Any) -> None:
        """Persist a state mutation into the event journal."""
        self.state[key] = value
        self.journal.append_event(
            workflow_id=self.workflow_id,
            event_type=EventType.STATE_MUTATED,
            payload={"key": key, "value": value},
        )

    def get_state(self, key: str, default: Any = None) -> Any:
        """Read a value from the reconstructed working state."""
        return self.state.get(key, default)

    def complete(self, output: Optional[Any] = None) -> None:
        """Mark workflow as successfully completed."""
        self.status = WorkflowStatus.COMPLETED
        self.output = output
        self.journal.append_event(
            workflow_id=self.workflow_id,
            event_type=EventType.WORKFLOW_COMPLETED,
            payload={"output": output},
        )

    def fail(self, error: str) -> None:
        """Mark workflow as failed."""
        self.status = WorkflowStatus.FAILED
        self.error = error
        self.journal.append_event(
            workflow_id=self.workflow_id,
            event_type=EventType.WORKFLOW_FAILED,
            payload={"error": error},
        )
