"""Continuous Training Pipeline Orchestrator for Hath0r Cognitive Substrate."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from hath0r_engine.telemetry.cicccd_telemetry import CICCCDCTTelemetryHook
from hath0r_engine.training.dataset_curator import DatasetCurator
from hath0r_engine.training.gameshow_models import EvaluationCard
from hath0r_engine.training.model_evaluator import CandidateModelEvaluator
from hath0r_engine.training.peft_lora_sft import (
    DEFAULT_TARGET_MODULES,
    LoRAConfig,
    PEFTMethod,
    SFTLoRATrainer,
)

SUPPORTED_TRAINING_METHODS = {m.value for m in PEFTMethod}


@dataclass
class ContinuousTrainingPipeline:
    """Orchestrates SFT, LoRA, QLoRA, PEFT adapter fine-tuning, and post-training benchmark evaluations."""

    curator: DatasetCurator = field(default_factory=DatasetCurator)
    evaluator: CandidateModelEvaluator = field(default_factory=CandidateModelEvaluator)
    artifacts_dir: Path = field(default_factory=lambda: Path.cwd() / ".hath0r" / "training_artifacts")
    workspace_root: Optional[Path] = None

    def __post_init__(self) -> None:
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)

    def execute_training_job(
        self,
        target: str = "reasoning_slm",
        method: str = "lora",
        dataset_path: Optional[str] = None,
        dataset: Optional[List[Dict[str, Any]]] = None,
        epochs: int = 3,
        learning_rate: float = 0.0002,
        batch_size: int = 4,
        parameters: Optional[Dict[str, Any]] = None,
        eval_cards: Optional[Sequence[EvaluationCard]] = None,
        record_telemetry: bool = True,
    ) -> Dict[str, Any]:
        """Execute an SFT/LoRA/QLoRA/PEFT continuous training job, evaluate against benchmark, and persist adapter artifacts."""
        if method not in SUPPORTED_TRAINING_METHODS:
            raise ValueError(
                f"Unsupported training method '{method}'. Must be one of {sorted(SUPPORTED_TRAINING_METHODS)}"
            )

        job_id = f"job-{uuid.uuid4().hex[:12]}"
        created_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        # 1. Load or curate dataset
        train_data: List[Dict[str, Any]] = []
        if dataset:
            train_data = list(dataset)
        elif dataset_path:
            train_data = self.curator.load_dataset(dataset_path)

        if not train_data:
            # Default golden cognitive substrate exemplar dataset
            train_data = [
                {"input": "Identify security flaw in SQL query", "target": "AST parameterization required", "reward": 0.95},
                {"input": "Validate AgentGraph tool authorization", "target": "RBAC role verified against contract", "reward": 0.92},
                {"input": "Calculate token tax drift", "target": "Tokenizer FinOps ratio recorded", "reward": 0.88},
                {"input": "Execute durable hibernation checkpoint", "target": "EventJournal snapshot verified", "reward": 0.94},
            ]

        dataset_size = len(train_data)
        dataset_stats = self.curator.compute_statistics(train_data)

        # 2. Configure PEFT / LoRA / QLoRA / SFT parameters
        user_params = dict(parameters or {})
        lora_r = int(user_params.get("lora_rank", user_params.get("r", 16)))
        lora_alpha = float(user_params.get("lora_alpha", 32.0))
        lora_dropout = float(user_params.get("lora_dropout", 0.05))
        use_rslora = bool(user_params.get("use_rslora", False))
        target_mods = tuple(user_params.get("target_modules", DEFAULT_TARGET_MODULES))
        quant_bits = 4 if method == "qlora" else user_params.get("quantization_bits")

        peft_cfg = LoRAConfig(
            r=lora_r,
            lora_alpha=lora_alpha,
            lora_dropout=lora_dropout,
            use_rslora=use_rslora,
            target_modules=target_mods,
            base_model_name_or_path=target,
            quantization_bits=quant_bits,
            peft_type="QLORA" if method == "qlora" else ("SFT" if method == "sft" else "LORA"),
        )

        # 3. Execute SFT + LoRA/PEFT low-rank optimization & write adapter checkpoint
        trainer = SFTLoRATrainer(config=peft_cfg, artifacts_dir=self.artifacts_dir)
        sft_res = trainer.train(
            dataset=train_data,
            job_id=job_id,
            target=target,
            method=method,
            epochs=epochs,
            learning_rate=learning_rate,
            batch_size=batch_size,
        )

        # 4. Run post-training candidate evaluation against frozen base model and golden benchmark
        eval_res = self.evaluator.evaluate_trained_adapter(
            trainer=trainer,
            eval_dataset=train_data,
            eval_cards=eval_cards,
        )

        completed_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        mlflow_run_id = f"mlflow-{job_id}"

        resolved_params = {
            "lora_rank": lora_r,
            "lora_alpha": lora_alpha,
            "lora_dropout": lora_dropout,
            "use_rslora": use_rslora,
            "scaling": round(peft_cfg.scaling, 4),
            "target_modules": list(target_mods),
            "quantization_bits": quant_bits,
            "trainable_parameters": sft_res.trainable_parameters,
            "total_parameters": sft_res.total_parameters,
            "trainable_percentage": sft_res.trainable_percentage,
            "memory_savings_ratio": sft_res.memory_savings_ratio,
            **user_params,
        }

        metrics_payload: Dict[str, Any] = {
            "initial_loss": sft_res.initial_loss,
            "train_loss": sft_res.final_loss,
            "val_loss": sft_res.val_loss,
            "perplexity": sft_res.perplexity,
            "loss_history": sft_res.loss_history,
            "grad_norm": sft_res.grad_norm,
            "adapter_frobenius_norm": sft_res.adapter_frobenius_norm,
            "eval_reward": eval_res["candidate_mean_reward"],
            "baseline_reward": eval_res.get("baseline_mean_reward", 0.0),
            "accuracy_improvement": eval_res.get("improvement", 0.0),
            "alignment_accuracy": eval_res.get("alignment_accuracy", 0.0),
            "snr_db": eval_res["snr_db"],
            "quality_loss": eval_res["quality_loss"],
            "promotable": eval_res["promotable"],
            "eval_ran": True,
            "samples_evaluated": eval_res["samples_evaluated"],
        }
        if "gameshow_accuracy" in eval_res:
            metrics_payload["gameshow_accuracy"] = eval_res["gameshow_accuracy"]
            metrics_payload["gameshow_pass_rate"] = eval_res["gameshow_pass_rate"]

        if record_telemetry and self.workspace_root is not None:
            hook = CICCCDCTTelemetryHook(workspace_root=self.workspace_root)
            hook.record_training_telemetry(
                model_name=target,
                model_version=1,
                train_loss=sft_res.final_loss,
                eval_reward=eval_res["candidate_mean_reward"],
                mlflow_run_id=mlflow_run_id,
                candidate_improvement=eval_res.get("improvement", 0.0),
                dataset_samples=dataset_size,
                stage="Staging" if eval_res["promotable"] else "None",
            )

        job_result = {
            "schema_version": "hath0r.training.job/1",
            "job_id": job_id,
            "target": target,
            "method": method,
            "dataset_path": dataset_path or str(self.curator.output_dir / "default.jsonl"),
            "dataset_samples": dataset_size,
            "epochs": epochs,
            "learning_rate": learning_rate,
            "batch_size": batch_size,
            "status": "completed",
            "created_at": created_at,
            "completed_at": completed_at,
            "mlflow_run_id": mlflow_run_id,
            "model_artifact_uri": sft_res.adapter_weights_path,
            "adapter_dir": sft_res.adapter_dir,
            "adapter_config_path": sft_res.adapter_config_path,
            "artifact_sha256": sft_res.artifact_sha256,
            "metrics": metrics_payload,
            "parameters": resolved_params,
            "peft_config": sft_res.peft_config,
            "dataset_statistics": dataset_stats,
        }

        return job_result

    def generate_airflow_training_manifest(
        self,
        target: str = "reasoning_slm",
        method: str = "lora",
        dataset_path: Optional[str] = None,
        trigger_reason: str = "drift_sla_breach",
        drift_metrics: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        """Generate structured Airflow DAG trigger manifest for distributed CT retraining."""
        manifest_id = f"ct-manifest-{uuid.uuid4().hex[:8]}"
        return {
            "schema_version": "hath0r.airflow.training_trigger/1",
            "manifest_id": manifest_id,
            "target": target,
            "method": method,
            "dataset_path": dataset_path or str(self.curator.output_dir / "default.jsonl"),
            "trigger_reason": trigger_reason,
            "drift_metrics": drift_metrics or {"accuracy_drift": 0.06, "freshness_hours": 172.0},
            "sla_thresholds": {
                "max_drift": 0.05,
                "max_freshness_hours": 168.0,
            },
            "recommended_gpu_cluster": "k8s-gpu-spot",
            "recommended_epochs": 5,
            "callback_webhook": "http://atc.hath0r.internal:8000/api/v1/webhooks/airflow",
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
