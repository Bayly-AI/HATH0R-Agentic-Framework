# Procedure: JEV Tool-Guard Runtime Enforcement

> Document Type: **Procedure** (`cr-workflow-doc-001`)  
> Product: **HATH0R-Agentic-Framework** · Issue: #65 · SemVer: `minor`

## 1. Scope

Normative procedure for enabling, configuring, and verifying JEV tool-guard pre-execution interception.

## 2. Steps

### Step 1: Pre-Execution Interception Call
Before executing any tool or operation that modifies state, the execution engine invokes:
```python
result = await evaluate_tool_guard(tool_name, args, client=client)
if result and result.blocked:
    return format_block_message(tool_name, result)
```

### Step 2: OpenFeature Flag Toggle
Enable the guard using environment variables or OpenFeature catalog configuration:
```bash
export JEV_TOOL_GUARD_ENABLED=true
export JEV_MODE=stub   # or live with JEV_API_KEY
```

### Step 3: Argument Redaction
All argument payloads are parsed by `_summarize_args()`. Any keys containing `password`, `secret`, `token`, `api_key`, or `authorization` are masked with `[REDACTED]`.

### Step 4: Verification
Execute pytest suite:
```bash
PYTHONPATH=. pytest tests/test_jev_tool_guard.py -v
```
