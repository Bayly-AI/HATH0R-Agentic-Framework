"""Human Hibernation Gate for Zero-Compute Workflow Pauses."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional


class GateStatus(str, Enum):
    """Lifecycle status of a human authorization gate."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    TIMED_OUT = "timed_out"


@dataclass
class HumanGateRequest:
    """Human gate authorization request descriptor."""

    gate_name: str
    prompt: str
    required_role: Optional[str] = None
    status: GateStatus = GateStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    resolved_at: Optional[str] = None
    approved: Optional[bool] = None
    decision_payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        return data


class WorkflowSuspendedException(Exception):
    """Raised when workflow hits an unresolved human gate to pause compute."""

    def __init__(self, gate_request: HumanGateRequest) -> None:
        super().__init__(f"Workflow suspended waiting for human approval gate: {gate_request.gate_name}")
        self.gate_request = gate_request
