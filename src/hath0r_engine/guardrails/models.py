"""Data models for deterministic tool pre-execution guardrails."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class GuardrailAction(str, Enum):
    """Enforcement action determined by pre-execution guardrail evaluation."""

    ALLOW = "allow"
    REPAIR = "repair"
    BLOCK = "block"
    ESCALATE_HUMAN = "escalate_human"


@dataclass
class ToolCallDescriptor:
    """Descriptor capturing pending tool invocation parameters."""

    tool_name: str
    arguments: Dict[str, Any] = field(default_factory=dict)
    caller_role: Optional[str] = None
    context_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GuardrailEvaluation:
    """Outcome of pre-execution guardrail evaluation."""

    action: GuardrailAction
    reason: str = ""
    repaired_arguments: Optional[Dict[str, Any]] = None
    violations: List[str] = field(default_factory=list)
    escalation_gate: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["action"] = self.action.value
        return data
