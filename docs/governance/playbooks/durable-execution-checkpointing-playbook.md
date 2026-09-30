# Durable Execution & Event-Sourced Checkpointing Playbook

> **Status:** Active  
> **Parent Issue:** Bayly-AI/HATH0R-Agentic-Framework#129  
> **Target Subsystem:** `src/hath0r_engine/orchestration`

---

## 1. Overview

This playbook demonstrates how to structure durable, long-horizon agent workflows that survive process crashes, rate limits, and asynchronous human approval gates.

---

## 2. Usage Examples

### 2.1 Defining a Durable Workflow

```python
from hath0r_engine.orchestration import DurableWorkflowEngine, WorkflowStatus

engine = DurableWorkflowEngine(workflow_id="wf-refactor-001")

# Step 1: Ingest source code (deterministic / idempotent)
files = engine.run_step("ingest_source", lambda: ["src/app.py", "src/auth.py"])

# Step 2: Run static analysis
lint_results = engine.run_step("run_linter", lambda: {"errors": 0, "warnings": 2})

# Step 3: Human Hibernation Gate
approval = engine.pause_for_human(
    gate_name="approve_production_deploy",
    prompt="Confirm deployment of v2 auth refactor to staging environment.",
)

if approval and approval.get("approved"):
    deploy_result = engine.run_step("deploy_staging", lambda: {"status": "deployed"})
    engine.complete(output={"status": "success", "deployed": True})
```

### 2.2 Resuming After Crash or Human Approval

```python
# 1. External signal arrives
engine.signal_human_approval(
    gate_name="approve_production_deploy",
    approved=True,
    payload={"reviewer": "alice@bayly.ai", "notes": "Approved for staging"},
)

# 2. Re-run workflow function: Step 1 and Step 2 will NOT re-execute;
# execution resumes from the approval gate forward!
```
