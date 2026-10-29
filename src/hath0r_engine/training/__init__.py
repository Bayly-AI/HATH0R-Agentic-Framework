"""Hath0r Cognitive Substrate Continuous Training (CT), SFT, LoRA & PEFT Module."""

from __future__ import annotations

from hath0r_engine.training.dataset_curator import DatasetCurator
from hath0r_engine.training.gameshow_judge import GameshowJudge
from hath0r_engine.training.gameshow_models import (
    CardAttempt,
    EvaluationCard,
    GameshowCard,
    GameshowDeckState,
    GameshowRoundStats,
    TournamentDeckState,
    TournamentRoundStats,
)
from hath0r_engine.training.model_evaluator import CandidateModelEvaluator
from hath0r_engine.training.peft_lora_sft import (
    DEFAULT_TARGET_MODULES,
    NF4_CODEBOOK,
    LoRAConfig,
    LoRALinearAdapter,
    NF4Quantizer,
    PEFTConfig,
    PEFTMethod,
    SFTDatasetFormatter,
    SFTLoRATrainer,
    SFTTrainingResult,
)
from hath0r_engine.training.training_pipeline import (
    SUPPORTED_TRAINING_METHODS,
    ContinuousTrainingPipeline,
)

__all__ = [
    "DatasetCurator",
    "CandidateModelEvaluator",
    "ContinuousTrainingPipeline",
    "SUPPORTED_TRAINING_METHODS",
    "DEFAULT_TARGET_MODULES",
    "NF4_CODEBOOK",
    "PEFTMethod",
    "LoRAConfig",
    "PEFTConfig",
    "NF4Quantizer",
    "LoRALinearAdapter",
    "SFTDatasetFormatter",
    "SFTTrainingResult",
    "SFTLoRATrainer",
    "CardAttempt",
    "EvaluationCard",
    "GameshowCard",
    "GameshowJudge",
    "GameshowDeckState",
    "GameshowRoundStats",
    "TournamentDeckState",
    "TournamentRoundStats",
]
