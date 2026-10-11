"""Tests for ELTEngineAdapter batch ingestion and Airflow CT training manifest generation."""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from hath0r_engine.orchestration.elt_adapter import ELTEngineAdapter
from hath0r_engine.training.training_pipeline import ContinuousTrainingPipeline


class TestELTAirflowAdapter:
    """Test suite for batch ingestion and Airflow CT retraining triggers."""

    def test_stage_records_batch(self, tmp_path: Path):
        db_path = tmp_path / "raw_staging.sqlite"
        adapter = ELTEngineAdapter(db_path=db_path)

        records = [
            {"source_uri": "airflow/batch/001", "payload": {"user": "alice", "action": "login"}, "metadata": {"run_id": "dag_run_1"}},
            {"source_uri": "airflow/batch/002", "payload": {"user": "bob", "action": "logout"}, "metadata": {"run_id": "dag_run_1"}},
            {"source_uri": "airflow/batch/001", "payload": {"user": "alice", "action": "login"}, "metadata": {"run_id": "dag_run_1"}},  # Duplicate payload
        ]

        res = adapter.stage_records_batch(records, source_type="batch_airflow")
        assert res["total_processed"] == 3
        assert res["staged_count"] == 2
        assert res["duplicate_count"] == 1
        assert len(res["staged_ids"]) == 2

    def test_stage_batch_archive_json_array(self, tmp_path: Path):
        db_path = tmp_path / "raw_staging.sqlite"
        adapter = ELTEngineAdapter(db_path=db_path)

        archive_file = tmp_path / "batch_export.json"
        data = [
            {"id": 101, "record": "Enterprise entity A"},
            {"id": 102, "record": "Enterprise entity B"},
        ]
        archive_file.write_text(json.dumps(data), encoding="utf-8")

        res = adapter.stage_batch_archive(archive_file)
        assert res["total_processed"] == 2
        assert res["staged_count"] == 2
        assert res["duplicate_count"] == 0

        # Ingest again, should all be recognized as duplicates via SHA256
        res2 = adapter.stage_batch_archive(archive_file)
        assert res2["total_processed"] == 2
        assert res2["staged_count"] == 0
        assert res2["duplicate_count"] == 2

    def test_stage_batch_archive_jsonl(self, tmp_path: Path):
        db_path = tmp_path / "raw_staging.sqlite"
        adapter = ELTEngineAdapter(db_path=db_path)

        archive_file = tmp_path / "events.jsonl"
        lines = [
            json.dumps({"event": "page_view", "url": "/dashboard"}),
            json.dumps({"event": "click", "target": "run_workflow"}),
        ]
        archive_file.write_text("\n".join(lines), encoding="utf-8")

        res = adapter.stage_batch_archive(archive_file)
        assert res["total_processed"] == 2
        assert res["staged_count"] == 2

    def test_stage_batch_archive_missing_file_raises(self, tmp_path: Path):
        adapter = ELTEngineAdapter(db_path=tmp_path / "raw_staging.sqlite")
        with pytest.raises(FileNotFoundError):
            adapter.stage_batch_archive(tmp_path / "non_existent.jsonl")

    def test_generate_airflow_training_manifest(self, tmp_path: Path):
        pipeline = ContinuousTrainingPipeline(artifacts_dir=tmp_path)
        manifest = pipeline.generate_airflow_training_manifest(
            target="reasoning_slm",
            method="lora",
            trigger_reason="accuracy_drift_detected",
            drift_metrics={"accuracy_drift": 0.07, "freshness_hours": 170.0},
        )

        assert manifest["schema_version"] == "hath0r.airflow.training_trigger/1"
        assert manifest["target"] == "reasoning_slm"
        assert manifest["method"] == "lora"
        assert manifest["trigger_reason"] == "accuracy_drift_detected"
        assert manifest["drift_metrics"]["accuracy_drift"] == 0.07
        assert "callback_webhook" in manifest
