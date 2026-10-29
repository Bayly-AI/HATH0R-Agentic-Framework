"""Unit and integration tests for Hath0r Continuous Training (CT), SFT, LoRA, QLoRA, PEFT, and CICCCDCT telemetry."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from hath0r_engine.telemetry.cicccd_telemetry import CICCCDCTTelemetryHook
from hath0r_engine.training import (
    CandidateModelEvaluator,
    ContinuousTrainingPipeline,
    DatasetCurator,
    EvaluationCard,
    LoRAConfig,
    LoRALinearAdapter,
    NF4Quantizer,
    PEFTConfig,
    PEFTMethod,
    SFTDatasetFormatter,
    SFTLoRATrainer,
)


def test_dataset_curator_filtration(tmp_path: Path) -> None:
    curator = DatasetCurator(output_dir=tmp_path)
    traces = [
        {"input": "Test 1", "output": "Output 1", "reward": 0.85, "assertions_passed": True},
        {"input": "Test 2", "output": "Output 2", "reward": 0.40, "assertions_passed": True},  # filtered by reward
        {"input": "Test 3", "output": "Output 3", "reward": 0.90, "assertions_passed": False},  # filtered by assertion
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
    assert curator.load_dataset(tmp_path / "missing.jsonl") == []
    assert curator.compute_statistics([])["samples_count"] == 0


def test_lora_and_peft_config() -> None:
    cfg = LoRAConfig(r=16, lora_alpha=32.0, lora_dropout=0.05, use_rslora=False)
    assert cfg.scaling == 2.0
    peft_dict = cfg.to_peft_dict()
    assert peft_dict["peft_type"] == "LORA"
    assert peft_dict["r"] == 16
    assert peft_dict["quantization_config"] is None

    rs_cfg = PEFTConfig(r=16, lora_alpha=32.0, use_rslora=True, quantization_bits=4)
    assert rs_cfg.scaling == 8.0
    rs_dict = rs_cfg.to_peft_dict()
    assert rs_dict["quantization_config"]["load_in_4bit"] is True
    assert rs_dict["quantization_config"]["bnb_4bit_quant_type"] == "nf4"

    with pytest.raises(ValueError):
        LoRAConfig(r=0)
    with pytest.raises(ValueError):
        LoRAConfig(lora_alpha=0.0)
    with pytest.raises(ValueError):
        LoRAConfig(lora_dropout=1.0)


def test_nf4_quantizer_roundtrip() -> None:
    quantizer = NF4Quantizer(block_size=8, double_quant=True)
    weights = [[0.1 * ((i + j) % 5 - 2) for j in range(8)] for i in range(4)]
    q_state = quantizer.quantize_matrix(weights)
    assert q_state["rows"] == 4
    assert q_state["cols"] == 8
    assert q_state["compression_ratio"] > 1.5

    recon = quantizer.dequantize_matrix(q_state)
    assert len(recon) == 4
    assert len(recon[0]) == 8
    # Verify bounded quantization error
    max_err = max(abs(weights[i][j] - recon[i][j]) for i in range(4) for j in range(8))
    assert max_err < 0.08


def test_lora_linear_adapter_identity_and_update() -> None:
    cfg = LoRAConfig(r=4, lora_alpha=8.0, d_model=16)
    adapter = LoRALinearAdapter("q_proj", in_features=16, out_features=16, config=cfg)

    # At t=0, B is initialized to 0 so Delta W == 0 and forward(use_adapter=True) == forward_base
    assert adapter.frobenius_norm() == 0.0
    x = [0.25] * 16
    y_base = adapter.forward_base(x)
    y_lora, ax = adapter.forward(x, use_adapter=True)
    assert y_base == y_lora

    # After a backward step, B becomes non-zero and loss toward target decreases
    target = [0.5] * 16
    grad_out = [2.0 * (y_lora[i] - target[i]) / 16.0 for i in range(16)]
    grad_norm = adapter.backward_step(x=x, ax=ax, grad_out=grad_out, learning_rate=0.1)
    assert grad_norm > 0.0
    assert adapter.frobenius_norm() > 0.0

    merged = adapter.merged_weights()
    assert len(merged) == 16
    assert len(merged[0]) == 16


def test_sft_dataset_formatter_and_trainer(tmp_path: Path) -> None:
    formatter = SFTDatasetFormatter(d_model=16)
    formatted = formatter.format_chatml("Verify AST guardrail", "SyntaxGuardrail validated AST")
    assert "<|im_start|>user" in formatted["chatml_text"]
    assert "<|im_start|>assistant" in formatted["chatml_text"]
    assert formatted["labels_mask"].count(-100) == formatted["prompt_token_count"]
    assert formatted["labels_mask"].count(1) == formatted["completion_token_count"]

    cfg = LoRAConfig(r=4, lora_alpha=8.0, d_model=16, quantization_bits=4)
    trainer = SFTLoRATrainer(config=cfg, artifacts_dir=tmp_path / "artifacts")
    dataset = [
        {"input": "Identify SQL injection risk", "target": "Parameterize query via AST validator"},
        {"input": "Check AgentGraph RBAC", "target": "Verify role permission in policy DAG"},
    ]
    sft_res = trainer.train(dataset=dataset, job_id="job-test1", target="reasoning_slm", method="qlora", epochs=4)

    # Verify real optimization convergence: final loss strictly lower than initial loss
    assert sft_res.final_loss < sft_res.initial_loss
    assert sft_res.adapter_frobenius_norm > 0.0
    assert 0.0 < sft_res.trainable_percentage < 100.0
    assert sft_res.memory_savings_ratio > 1.5
    assert Path(sft_res.adapter_config_path).is_file()
    assert Path(sft_res.adapter_weights_path).is_file()


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


def test_continuous_training_pipeline_and_evals(tmp_path: Path) -> None:
    curator = DatasetCurator(output_dir=tmp_path / "data")
    pipeline = ContinuousTrainingPipeline(
        curator=curator,
        artifacts_dir=tmp_path / "artifacts",
        workspace_root=tmp_path,
    )
    cards = [
        EvaluationCard(
            card_id="CARD-01",
            domain="security",
            question="How are SQL queries validated?",
            expected_answer="AST parameterization required via SyntaxGuardrail",
            key_facts=["AST parameterization", "SyntaxGuardrail"],
        )
    ]

    for method in (PEFTMethod.LORA.value, PEFTMethod.QLORA.value, PEFTMethod.SFT.value, PEFTMethod.PEFT.value):
        result = pipeline.execute_training_job(
            target="reasoning_slm",
            method=method,
            epochs=3,
            eval_cards=cards,
        )
        assert result["status"] == "completed"
        assert result["target"] == "reasoning_slm"
        assert result["method"] == method
        assert result["metrics"]["train_loss"] < result["metrics"]["initial_loss"]
        assert result["metrics"]["eval_ran"] is True
        assert result["metrics"]["promotable"] is True
        assert result["metrics"]["gameshow_pass_rate"] == 1.0
        assert Path(result["model_artifact_uri"]).is_file()
        assert Path(result["adapter_config_path"]).is_file()

        # Validate against formal JSON schema contract
        schema_path = Path("contracts/hath0r-training-job-v1.schema.json")
        if schema_path.is_file():
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            jsonschema.validate(instance=result, schema=schema)

    with pytest.raises(ValueError):
        pipeline.execute_training_job(method="invalid_method")


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
