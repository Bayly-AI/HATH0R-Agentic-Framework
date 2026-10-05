"""Unit tests for Framework CICCCD Methodology and CICCCDTelemetryHook."""

from __future__ import annotations

from pathlib import Path

from hath0r_engine.telemetry import CICCCDTelemetryHook


def test_cicccd_telemetry_hook(tmp_path):
    hook = CICCCDTelemetryHook(workspace_root=tmp_path, state_file=tmp_path / ".hath0r" / "cccd_state.json")

    metrics = hook.get_calibration_metrics()
    assert "current_parameters" in metrics

    # Record calibration event
    updated = hook.record_calibration_telemetry(
        signature_name="test_framework_sig",
        drift_metrics={"accuracy_drift": 0.005, "latency_drift_ms": 1.2},
        calibrated_params={"temperature": 0.3, "max_tokens": 4096},
    )

    assert updated["last_signature"] == "test_framework_sig"
    assert updated["current_parameters"]["temperature"] == 0.3
    assert hook.is_calibration_fresh() is True


def test_agents_md_references_cicccd():
    agents_md = Path("AGENTS.md").read_text(encoding="utf-8")
    assert "CR-CICCCD-001" in agents_md
    assert "Continuous Integration, Calibration & Deployment" in agents_md
