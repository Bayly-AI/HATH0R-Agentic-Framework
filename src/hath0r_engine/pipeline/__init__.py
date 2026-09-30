"""Declarative Agent Pipelines and DSPy-compatible Module Optimization package."""

from hath0r_engine.pipeline.assertions import (
    Assert,
    SchemaAssertionError,
    SchemaSuggestionWarning,
    Suggest,
    validate_json_contract,
)
from hath0r_engine.pipeline.module import (
    ChainOfThought,
    PipelineModule,
    Predictor,
)
from hath0r_engine.pipeline.signature import (
    Field,
    InputField,
    OutputField,
    Prediction,
    Signature,
)
from hath0r_engine.pipeline.teleprompter import BootstrapFewShotCompiler

__all__ = [
    "Field",
    "InputField",
    "OutputField",
    "Prediction",
    "Signature",
    "SchemaAssertionError",
    "SchemaSuggestionWarning",
    "Assert",
    "Suggest",
    "validate_json_contract",
    "PipelineModule",
    "Predictor",
    "ChainOfThought",
    "BootstrapFewShotCompiler",
]
