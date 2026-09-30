# Declarative Agent Pipelines Playbook

> **Status:** Active  
> **Parent Issue:** Bayly-AI/HATH0R-Agentic-Framework#131  
> **Target Subsystem:** `src/hath0r_engine/pipeline`

---

## 1. Overview

This playbook provides patterns for building declarative agent pipelines using typed signatures, schema assertions, and teleprompter few-shot compilation.

---

## 2. Usage Examples

### 2.1 Defining a Typed Signature & ChainOfThought Module

```python
from hath0r_engine.pipeline import (
    Signature,
    InputField,
    OutputField,
    ChainOfThought,
    Assert,
)

class CodeRefactorSignature(Signature):
    """Refactor code while preserving interface contracts."""
    source_code = InputField(desc="Original source code snippet")
    contract_schema = InputField(desc="Required JSON schema contracts")
    
    rationale = OutputField(desc="Step-by-step reasoning for the refactor")
    refactored_code = OutputField(desc="Updated source code matching contracts")

module = ChainOfThought(CodeRefactorSignature)

# Add schema validation assertion
module.add_assertion(lambda out: len(out.refactored_code) > 0, "Refactored code cannot be empty.")

prediction = module(
    source_code="def calc(a, b): return a + b",
    contract_schema="{}",
)
print(f"Rationale: {prediction.rationale}")
print(f"Code: {prediction.refactored_code}")
```

### 2.2 Compiling with Teleprompter

```python
from hath0r_engine.pipeline import BootstrapFewShotCompiler

compiler = BootstrapFewShotCompiler(metric=lambda example, pred: len(pred.refactored_code) > 0)
compiled_module = compiler.compile(
    student_module=module,
    trainset=[
        {"source_code": "def foo(): pass", "contract_schema": "{}"}
    ],
)
```
