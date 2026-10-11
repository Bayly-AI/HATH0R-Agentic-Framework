"""Unit and integration tests for Hath0r Continuous Training (CT) and CICCCDCT telemetry."""

import pytest
from pathlib import Path
from hath0r_engine.training import (
    DatasetCurator,
    CandidateModelEvaluator,
    ContinuousTrainingPipeline,
)
from hath0r_engine.telemetry.cicccd_telemetry import CICCCDCTTelemetryHook, CICCCDTelemetryHook


def test_dataset_curator_filtration(tmp_path: Path) -> None:
    curator = DatasetCurator(output_dir=tmp_path)
    traces = [
        {"input": "Test 1", "output": "Output 1", "reward": 0.85, "assertions_passed": True},
        {"input": "Test 2", "output": "Output 2", "reward": 0.40, "assertions_passed": True},  # filtered by reward
        {"input": "Test 3", "output": "Output 3", "reward": 0.90, "assertions_passed": False}, # filtered by assertion
        {"input": "Test 4", "output": "Output 4", "reward": 0.95, "assertions_passed": True},
    ]

    curated = curator.curate_from_traces(traces, min_reward=0.70)
    assert len(curated) == 2
    assert curated[0]["input"] == "Test 1"
    assert curated[1]["input"] == "Test 4"

    stats = curator.compute_statistics(curated)
    assert stats["samples_count"] == 2
    assert stats["mean_reward"] == 0.90

    saved_path = curator.save_dataset(curated, "test_set")
    assert saved_path.is_file()

    loaded = curator.load_dataset(saved_path)
    assert len(loaded) == 2


def test_candidate_model_evaluator() -> None:
    evaluator = CandidateModelEvaluator(epsilon_improvement=0.02)
    single_reward = evaluator.calculate_reward(accuracy=0.90, tokens_used=1000, latency_ms=80.0)
    assert "total_reward" in single_reward
    assert single_reward["total_reward"] > 0.0

    candidates = [
        {"accuracy": 0.92, "tokens_used": 800, "latency_ms": 70.0},
        {"accuracy": 0.94, "tokens_used": 750, "latency_ms": 65.0},
    ]
    baselines = [
        {"accuracy": 0.75, "tokens_used": 1400, "latency_ms": 120.0},
        {"accuracy": 0.72, "tokens_used": 1350, "latency_ms": 125.0},
    ]

    benchmark = evaluator.evaluate_benchmark(candidates, baselines)
    assert benchmark["promotable"] is True
    assert benchmark["improvement"] > 0.02
    assert "PASS" in benchmark["promotion_verdict"]


def test_continuous_training_pipeline(tmp_path: Path) -> None:
    curator = DatasetCurator(output_dir=tmp_path / "data")
    pipeline = ContinuousTrainingPipeline(curator=curator, artifacts_dir=tmp_path / "artifacts")

    result = pipeline.execute_training_job(
        target="reasoning_slm",
        method="lora",
        epochs=2,
    )
    assert result["status"] == "completed"
    assert result["target"] == "reasoning_slm"
    assert result["metrics"]["train_loss"] < 2.0
    assert result["metrics"]["promotable"] is True
    assert Path(result["model_artifact_uri"]).name.startswith("reasoning_slm_lora")


def test_cicccdct_telemetry_hook(tmp_path: Path) -> None:
    hook = CICCCDCTTelemetryHook(workspace_root=tmp_path)
    metrics = hook.get_calibration_metrics()
    assert "training" in metrics
    assert hook.is_training_fresh() is False  # Never trained yet

    # Record training event
    hook.record_training_telemetry(
        model_name="qwen-2.5-coder-7b-lora",
        model_version=2,
        train_loss=0.32,
        eval_reward=0.88,
        mlflow_run_id="run-12345",
        candidate_improvement=0.06,
        dataset_samples=400,
        stage="Production",
    )

    updated = hook.get_calibration_metrics()
    assert updated["training"]["active_model_name"] == "qwen-2.5-coder-7b-lora"
    assert updated["training"]["total_training_runs"] == 1
    assert updated["training"]["train_loss"] == 0.32
    assert hook.is_training_fresh(max_age_hours=1.0) is True
