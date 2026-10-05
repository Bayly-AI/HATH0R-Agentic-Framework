"""Continuous Integration, Continuous Calibration & Continuous Deployment (CICCCD) Telemetry Substrate for Hath0r Framework."""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional

HATH0R_DIR = ".hath0r"
CCCD_STATE_FILE = "cccd_state.json"


@dataclass
class CICCCDTelemetryHook:
    """AgentGraph continuous calibration telemetry recorder and parameter drift monitor."""

    workspace_root: Path = field(default_factory=Path.cwd)
    state_file: Optional[Path] = None

    def __post_init__(self) -> None:
        self.workspace_root = self.workspace_root.resolve()
        file_name = Path(self.state_file).name if self.state_file else CCCD_STATE_FILE
        self.state_file = (self.workspace_root / HATH0R_DIR / file_name).resolve()
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

    def record_calibration_telemetry(
        self,
        signature_name: str,
        drift_metrics: Dict[str, float],
        calibrated_params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Record calibration telemetry event into .hath0r/cccd_state.json."""
        state = self.get_calibration_metrics()
        state["last_run_timestamp"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        state["total_calibration_runs"] = state.get("total_calibration_runs", 0) + 1
        state["current_parameters"] = calibrated_params
        state["drift_metrics"] = drift_metrics
        state["last_signature"] = signature_name

        if self.state_file is not None:
            base_dir = os.path.realpath(str(self.workspace_root))
            target_path = os.path.realpath(str(self.state_file))
            if not (target_path.startswith(base_dir + os.sep) or target_path == base_dir):
                raise ValueError("State file path escapes workspace root")
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(state, indent=2))
        return state

    def get_calibration_metrics(self) -> Dict[str, Any]:
        """Read active CICCCD calibration metrics and freshness state."""
        if not self.state_file or not self.state_file.is_file():
            return {
                "active_calibration": True,
                "last_run_timestamp": None,
                "total_calibration_runs": 0,
                "current_parameters": {
                    "temperature": 0.2,
                    "max_tokens": 2048,
                    "top_p": 0.95,
                    "retry_count": 3,
                    "guardrail_threshold": 0.85,
                },
                "drift_metrics": {
                    "accuracy_drift": 0.0,
                    "latency_drift_ms": 0.0,
                    "token_tax_drift": 0.0,
                },
            }
        try:
            val = json.loads(self.state_file.read_text(encoding="utf-8"))
            return val if isinstance(val, dict) else {}
        except Exception:
            return {}

    def is_calibration_fresh(self, max_age_hours: float = 24.0) -> bool:
        """Verify calibration telemetry is <= 24 hours old."""
        metrics = self.get_calibration_metrics()
        ts_str = metrics.get("last_run_timestamp")
        if not ts_str:
            return False
        try:
            last_ts = time.mktime(time.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ"))
            age_hours = (time.time() - last_ts) / 3600.0
            return age_hours <= max_age_hours
        except Exception:
            return False
