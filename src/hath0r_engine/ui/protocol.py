"""Evidence Handshake Protocol Models and Session Management."""

from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from hath0r_engine.ui.crypto_signoff import generate_cryptographic_signature


class EvidenceType(str, Enum):
    """Supported interactive Generative UI component types."""

    DIFF_VIEWER = "diff_viewer"
    TEST_BADGE = "test_badge"
    PARAMETER_SLIDER = "parameter_slider"
    CRYPTO_SIGNOFF_CARD = "crypto_signoff_card"
    PROMOTION_GATE = "promotion_gate"
    CHURN_HEATMAP = "churn_heatmap"



class HandshakeState(str, Enum):
    """Lifecycle status of the evidence handshake session."""

    INITIATED = "initiated"
    INTERACTING = "interacting"
    SIGNED = "signed"
    REJECTED = "rejected"


@dataclass
class EvidenceComponent:
    """Standardized descriptor for an interactive Generative UI card."""

    component_id: str
    type: EvidenceType
    title: str
    props: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["type"] = self.type.value
        return data


@dataclass
class SignOffRecord:
    """Cryptographic audit sign-off record."""

    reviewer: str
    role: str
    decision: bool
    signature: str
    timestamp: str
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class HandshakeSession:
    """Manages active evidence handshake review session with the web dashboard."""

    def __init__(self, session_id: Optional[str] = None, task_name: str = "agent_task") -> None:
        self.session_id = session_id or f"sess-{uuid.uuid4().hex[:12]}"
        self.task_name = task_name
        self.state = HandshakeState.INITIATED
        self.components: List[EvidenceComponent] = []
        self.sign_off_record: Optional[SignOffRecord] = None
        self.created_at = datetime.now(timezone.utc).isoformat()

    def add_component(self, component: EvidenceComponent) -> None:
        """Add UI component to session."""
        self.components.append(component)
        if self.state == HandshakeState.INITIATED:
            self.state = HandshakeState.INTERACTING

    def add_components(self, components: List[EvidenceComponent]) -> None:
        for c in components:
            self.add_component(c)

    def sign_off(
        self,
        reviewer: str,
        role: str,
        decision: bool,
        notes: str = "",
        secret_key: str = "hath0r-handshake-secret",
    ) -> SignOffRecord:
        """Complete sign-off with cryptographic signature generation."""
        now = datetime.now(timezone.utc).isoformat()
        signature = generate_cryptographic_signature(
            session_id=self.session_id,
            task_name=self.task_name,
            reviewer=reviewer,
            decision=decision,
            timestamp=now,
            secret_key=secret_key,
        )
        self.sign_off_record = SignOffRecord(
            reviewer=reviewer,
            role=role,
            decision=decision,
            signature=signature,
            timestamp=now,
            notes=notes,
        )
        self.state = HandshakeState.SIGNED if decision else HandshakeState.REJECTED
        return self.sign_off_record

    def export_payload(self) -> Dict[str, Any]:
        """Export serialized handshake payload for dashboard streaming."""
        return {
            "session_id": self.session_id,
            "task_name": self.task_name,
            "state": self.state.value,
            "created_at": self.created_at,
            "components": [c.to_dict() for c in self.components],
            "sign_off": self.sign_off_record.to_dict() if self.sign_off_record else None,
        }
