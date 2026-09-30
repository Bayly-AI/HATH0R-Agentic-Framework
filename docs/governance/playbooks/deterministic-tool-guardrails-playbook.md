# Deterministic Pre-Execution Tool Guardrails Playbook

> **Status:** Active  
> **Parent Issue:** Bayly-AI/HATH0R-Agentic-Framework#132  
> **Target Subsystem:** `src/hath0r_engine/guardrails`

---

## 1. Overview

This playbook shows how to configure and enforce deterministic pre-execution tool guardrails, AST code safety validators, and automatic schema repair in Hath0r agent swarms.

---

## 2. Usage Examples

### 2.1 Guardrail Interception and AST Safety Validation

```python
from hath0r_engine.guardrails import (
    GuardrailsManager,
    ToolCallDescriptor,
    GuardrailAction,
)

manager = GuardrailsManager()

# Safe invocation
safe_call = ToolCallDescriptor(
    tool_name="bash_execute",
    arguments={"command": "pytest tests/"},
)
res = manager.evaluate(safe_call)
assert res.action == GuardrailAction.ALLOW

# Dangerous invocation with destructive AST
dangerous_call = ToolCallDescriptor(
    tool_name="bash_execute",
    arguments={"command": "rm -rf / --no-preserve-root"},
)
res_blocked = manager.evaluate(dangerous_call)
assert res_blocked.action in (GuardrailAction.BLOCK, GuardrailAction.ESCALATE_HUMAN)
```

### 2.2 In-Flight Schema Repair

```python
# Malformed argument typing (string where integer expected)
malformed_call = ToolCallDescriptor(
    tool_name="query_database",
    arguments={"limit": "50", "timeout_ms": "5000"},
)
repaired = manager.evaluate(malformed_call)
assert repaired.repaired_arguments["limit"] == 50
assert repaired.repaired_arguments["timeout_ms"] == 5000
```
