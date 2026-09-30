"""Unit tests for Generative UI & Evidence Handshake Protocol."""

import json
import pytest

from hath0r_engine.ui import (
    BiDirectionalStateSync,
    EvidenceComponent,
    EvidenceType,
    HandshakeSession,
    HandshakeState,
    SignOffRecord,
    UIComponentBuilder,
    generate_cryptographic_signature,
)


def test_ui_component_builder():
    diff_comp = UIComponentBuilder.build_diff_viewer(
        file_path="src/main.py",
        old_code="def run(): pass",
        new_code="def run(): return 42",
    )
    assert diff_comp.type == EvidenceType.DIFF_VIEWER
    assert diff_comp.props["file_path"] == "src/main.py"

    badge_comp = UIComponentBuilder.build_test_badge(
        suite_name="Unit Suite",
        passed=85,
        failed=0,
        coverage_pct=99.2,
    )
    assert badge_comp.type == EvidenceType.TEST_BADGE
    assert badge_comp.props["status"] == "PASS"

    slider_comp = UIComponentBuilder.build_parameter_slider(
        param_key="temperature",
        min_val=0.0,
        max_val=1.0,
        current_val=0.7,
        step=0.05,
    )
    assert slider_comp.type == EvidenceType.PARAMETER_SLIDER
    assert slider_comp.props["current"] == 0.7

    signoff_comp = UIComponentBuilder.build_crypto_signoff_card(
        gate_name="prod_gate",
        required_role="release_lead",
    )
    assert signoff_comp.type == EvidenceType.CRYPTO_SIGNOFF_CARD


def test_handshake_session_lifecycle_and_signoff():
    session = HandshakeSession(task_name="deploy_auth_v2")
    assert session.state == HandshakeState.INITIATED

    diff = UIComponentBuilder.build_diff_viewer("auth.py", "v1", "v2")
    session.add_component(diff)
    assert session.state == HandshakeState.INTERACTING

    # Sign off
    record = session.sign_off(
        reviewer="somesayray",
        role="lead_architect",
        decision=True,
        notes="All 90 unit tests green",
    )
    assert session.state == HandshakeState.SIGNED
    assert len(record.signature) == 64  # SHA-256 hex string
    assert record.decision is True

    # Export payload
    payload = session.export_payload()
    assert payload["task_name"] == "deploy_auth_v2"
    assert payload["state"] == "signed"
    assert len(payload["components"]) == 1
    assert payload["sign_off"]["signature"] == record.signature

    # Verify JSON serializability
    json_str = json.dumps(payload)
    assert json_str is not None


def test_bidirectional_state_synchronization():
    sync = BiDirectionalStateSync()
    agent_state = {"threshold": 0.5, "max_tokens": 1000}

    events = []

    def on_change(key, val):
        events.append((key, val))

    sync.register_listener(on_change)

    sync.apply_update(agent_state, "threshold", 0.85)
    assert agent_state["threshold"] == 0.85
    assert events == [("threshold", 0.85)]


def test_cryptographic_signature_determinism():
    sig1 = generate_cryptographic_signature(
        session_id="sess-001",
        task_name="task-1",
        reviewer="alice",
        decision=True,
        timestamp="2026-09-30T08:00:00Z",
    )
    sig2 = generate_cryptographic_signature(
        session_id="sess-001",
        task_name="task-1",
        reviewer="alice",
        decision=True,
        timestamp="2026-09-30T08:00:00Z",
    )
    assert sig1 == sig2

    # Modified timestamp -> different signature
    sig_tampered = generate_cryptographic_signature(
        session_id="sess-001",
        task_name="task-1",
        reviewer="alice",
        decision=True,
        timestamp="2026-09-30T08:00:01Z",
    )
    assert sig1 != sig_tampered
