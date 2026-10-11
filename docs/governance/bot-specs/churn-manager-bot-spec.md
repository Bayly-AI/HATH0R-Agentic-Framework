# Bot Spec: ChurnManagerBot & HotspotRefactorBot

> Canonical Autonomous Bot Specification · Hath0r Agentic Framework  
> Updated: 2026-10-05

## 1. ChurnManagerBot Specification

### Purpose
Monitors repository git histories, calculates time-windowed code churn metrics, injects volatility scores into `AgentGraph`, and enforces PR review gating.

### RBAC Tool Authorizations
- `churn:analyze`: Execute commit volatility extraction.
- `churn:hotspots`: Query ranked architectural hotspots.
- `churn:pr-risk`: Inspect diff risk between work branch and base.
- `agentgraph:update`: Write hotspot nodes and co-changing relation edges.

---

## 2. HotspotRefactorBot Specification

### Purpose
Proactively inspects files flagged with `CRITICAL` or `HIGH` risk tiers, using DSPy declarative reasoning pipelines to propose clean decoupled abstractions.

### Core Signature
```python
class HotspotRefactoringSignature(dspy.Signature):
    """Proposes decoupling refactorings for high-churn complex modules."""
    file_path: str = dspy.InputField()
    complexity_score: float = dspy.InputField()
    co_changing_files: List[str] = dspy.InputField()
    refactoring_plan: str = dspy.OutputField()
    decoupled_interface_code: str = dspy.OutputField()
```
