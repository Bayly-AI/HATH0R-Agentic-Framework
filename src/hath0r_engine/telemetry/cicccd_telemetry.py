"""Continuous Integration, Calibration, Deployment & Training (CICCCDCT) Telemetry Substrate for Hath0r Framework."""

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
    """AgentGraph continuous calibration and training telemetry recorder and drift monitor."""

    workspace_root: Path = field(default_factory=Path.cwd)
    state_file: Optional[Path] = None

    def __post_init__(self) -> None:
        self.workspace_root = self.workspace_root.resolve()
        file_name = Path(self.state_file).name if self.state_file else CCCD_STATE_FILE
        self.state_file = (self.workspace_root / HATH0R_DIR / file_name).resolve()

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

        self._save_state(state)
        return state

    def record_training_telemetry(
        self,
        model_name: str,
        model_version: Any,
        train_loss: float,
        eval_reward: float,
        mlflow_run_id: Optional[str] = None,
        candidate_improvement: float = 0.0,
        dataset_samples: int = 0,
        stage: str = "Staging",
    ) -> Dict[str, Any]:
        """Record Continuous Training (CT) model training run metadata into state."""
        state = self.get_calibration_metrics()
        now_ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        training_block = state.get("training", {})
        training_block["active_training"] = True
        training_block["total_training_runs"] = training_block.get("total_training_runs", 0) + 1
        training_block["last_trained_timestamp"] = now_ts
        training_block["active_model_name"] = model_name
        training_block["active_model_version"] = model_version
        training_block["active_model_stage"] = stage
        training_block["mlflow_run_id"] = mlflow_run_id
        training_block["train_loss"] = round(train_loss, 4)
        training_block["eval_benchmark_reward"] = round(eval_reward, 4)
        training_block["candidate_model_improvement"] = round(candidate_improvement, 4)
        training_block["dataset_samples_count"] = dataset_samples

        state["training"] = training_block

        # Append to history
        history = state.get("history", [])
        history.append({
            "type": "training",
            "timestamp": now_ts,
            "model_name": model_name,
            "model_version": model_version,
            "train_loss": train_loss,
            "eval_reward": eval_reward,
            "stage": stage,
        })
        state["history"] = history[-20:]  # Keep last 20 events

        self._save_state(state)
        return state

    def get_calibration_metrics(self) -> Dict[str, Any]:
        """Read active CICCCDCT calibration and training state."""
        default_state: Dict[str, Any] = {
            "schema_version": "hath0r.cicccdct.state/1",
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
            "training": {
                "active_training": True,
                "total_training_runs": 0,
                "last_trained_timestamp": None,
                "active_model_name": "default",
                "active_model_version": 1,
                "active_model_stage": "Production",
                "mlflow_run_id": None,
                "train_loss": 0.0,
                "eval_benchmark_reward": 0.85,
                "candidate_model_improvement": 0.0,
                "dataset_samples_count": 0,
            },
            "history": [],
        }

        if not self.state_file or not self.state_file.is_file():
            return default_state

        try:
            val = json.loads(self.state_file.read_text(encoding="utf-8"))
            if isinstance(val, dict):
                # Ensure training block exists even in legacy cccd_state.json files
                if "training" not in val:
                    val["training"] = default_state["training"]
                return val
            return default_state
        except Exception:
            return default_state

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

    def is_training_fresh(self, max_age_hours: float = 168.0) -> bool:
        """Verify model training freshness SLA is <= max_age_hours (default 168.0h / 7 days)."""
        metrics = self.get_calibration_metrics()
        training = metrics.get("training", {})
        ts_str = training.get("last_trained_timestamp")
        if not ts_str:
            return False
        try:
            last_ts = time.mktime(time.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ"))
            age_hours = (time.time() - last_ts) / 3600.0
            return age_hours <= max_age_hours
        except Exception:
            return False

    def _save_state(self, state: Dict[str, Any]) -> None:
        """Persist state safely within workspace."""
        if self.state_file is not None:
            base_dir = os.path.realpath(str(self.workspace_root))
            target_path = os.path.realpath(str(self.state_file))
            if not (target_path.startswith(base_dir + os.sep) or target_path == base_dir):
                raise ValueError("State file path escapes workspace root")
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(json.dumps(state, indent=2))


# Alias for explicit CICCCDCT usage
CICCCDCTTelemetryHook = CICCCDTelemetryHook
