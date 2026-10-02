"""HATH0R Optimization Subsystem — Robust Design, Orthogonal Arrays, and Taguchi Methods."""

from hath0r_engine.optimization.taguchi import (
    ArrayType,
    ExperimentMatrix,
    ExperimentRun,
    Factor,
    FactorAnalysis,
    FactorLevelEffect,
    SNRType,
    TaguchiAnalysisResult,
    TaguchiEngine,
    TaguchiLossFunction,
    calculate_snr,
)

__all__ = [
    "ArrayType",
    "ExperimentMatrix",
    "ExperimentRun",
    "Factor",
    "FactorAnalysis",
    "FactorLevelEffect",
    "SNRType",
    "TaguchiAnalysisResult",
    "TaguchiEngine",
    "TaguchiLossFunction",
    "calculate_snr",
]
