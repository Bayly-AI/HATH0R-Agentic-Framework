"""Human Approval Escalation and Audit Hooks for Tool Guardrails."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from hath0r_engine.guardrails.models import ToolCallDescriptor


@dataclass
class EscalationEvent:
    """Escalation payload sent to human authorization queue."""

    escalation_id: str = field(default_factory=lambda: f"esc-{uuid.uuid4().hex[:10]}")
    tool_name: str = ""
    violations: List[str] = field(default_factory=list)
    descriptor: Optional[Dict[str, Any]] = None
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class HumanEscalationAuditHook:
    """Dispatches high-risk tool violations to the human authorization queue."""

    def __init__(self) -> None:
        self.escalations: List[EscalationEvent] = []

    def escalate(self, descriptor: ToolCallDescriptor, violations: List[str]) -> EscalationEvent:
        """Record escalation event and return descriptor."""
        event = EscalationEvent(
            tool_name=descriptor.tool_name,
            violations=violations,
            descriptor=descriptor.to_dict(),
        )
        self.escalations.append(event)
        return event

    def get_pending_escalations(self) -> List[EscalationEvent]:
        return list(self.escalations)
