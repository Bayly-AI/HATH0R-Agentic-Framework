"""Unit tests for Declarative Agent Pipelines, Typed Signatures, and Few-Shot Compilation."""

import pytest

from hath0r_engine.pipeline import (
    Assert,
    BootstrapFewShotCompiler,
    ChainOfThought,
    InputField,
    OutputField,
    PipelineModule,
    Prediction,
    Predictor,
    SchemaAssertionError,
    Signature,
    Suggest,
    validate_json_contract,
)


class CodeAnalysisSignature(Signature):
    """Analyze code snippet for safety vulnerabilities and compliance."""

    code_snippet = InputField(desc="Source code to analyze")
    language = InputField(desc="Programming language", default="python")

    rationale = OutputField(desc="Reasoning breakdown")
    vulnerabilities = OutputField(desc="List of detected vulnerabilities")
    safety_score = OutputField(desc="Calculated safety score (0-100)", default=95)


def test_signature_introspection():
    inputs = CodeAnalysisSignature.get_inputs()
    outputs = CodeAnalysisSignature.get_outputs()

    assert "code_snippet" in inputs
    assert "language" in inputs
    assert inputs["language"].default == "python"

    assert "rationale" in outputs
    assert "vulnerabilities" in outputs
    assert outputs["safety_score"].default == 95


def test_chain_of_thought_prediction():
    cot = ChainOfThought(CodeAnalysisSignature)

    pred = cot(code_snippet="import os; os.system('ls')")
    assert isinstance(pred, Prediction)
    assert hasattr(pred, "rationale")
    assert "code_snippet" in pred.rationale
    assert hasattr(pred, "vulnerabilities")
    assert pred.safety_score == 95


def test_schema_assertions_and_retries():
    cot = ChainOfThought(CodeAnalysisSignature)

    # Add assertion: safety_score must be >= 50
    cot.add_assertion(lambda p: p.safety_score >= 50, "Safety score must be at least 50")

    pred = cot(code_snippet="x = 1 + 2")
    assert pred.safety_score == 95

    # Add failing assertion
    cot.add_assertion(lambda p: False, "Always fail assertion")
    with pytest.raises(SchemaAssertionError) as exc_info:
        cot(code_snippet="x = 1 + 2", max_retries=1)
    assert "Always fail assertion" in str(exc_info.value)


def test_json_contract_validation():
    schema = {"required": ["status", "version"]}
    assert validate_json_contract('{"status": "ok", "version": "1.0.0"}', schema) is True
    assert validate_json_contract('{"status": "ok"}', schema) is False
    assert validate_json_contract("invalid json", schema) is False


def test_bootstrap_few_shot_compiler():
    cot = ChainOfThought(CodeAnalysisSignature)

    def custom_metric(example, pred):
        return len(pred.rationale) > 0

    compiler = BootstrapFewShotCompiler(metric=custom_metric, max_bootstrapped_demos=2)
    trainset = [
        {"code_snippet": "print('hello')", "language": "python"},
        {"code_snippet": "SELECT * FROM users", "language": "sql"},
        {"code_snippet": "cat /etc/passwd", "language": "bash"},
    ]

    compiled_module = compiler.compile(student_module=cot, trainset=trainset)
    assert len(compiled_module.demonstrations) == 2
    assert "prediction" in compiled_module.demonstrations[0]
