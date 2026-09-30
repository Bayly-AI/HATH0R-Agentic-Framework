# Agent Rules & CLI-First Operational Playbook

> **Status:** Active  
> **Parent Issue:** Bayly-AI/HATH0R-Agentic-Framework#142  
> **Target Audience:** All AI Agents, Autonomous Bots, and System Operators

---

## 1. Lifecycle Operator Workflow

When assigned an objective, agents must execute the following canonical CLI sequence:

### Step 1: Branch & Task Initialization
```bash
# Validate branch naming rules before creation
hath0r branch validate feature/<issue-number>-<slug>

# Check environment health and control tower connectivity
hath0r doctor
```

### Step 2: Knowledge Retrieval & Tri-Graph RAG
Do not invent requirements or assume file layouts. Retrieve facts via the operator CLI:
```bash
# Retrieve canonical knowledgebase paths
hath0r kb path

# Semantic and temporal memory graph search
hath0r memory search "tri-graph temporal edge indexing"

# Runtime session and context graph query
hath0r context query
```

### Step 3: Schema Contract Verification
```bash
# Verify schema contracts before modifications
hath0r contracts validate
```

### Step 4: Documentation Before Code
Author or update the relevant Strategy and Playbook in `docs/governance/` following `docs/governance/workflow-documentation-standard.md`.

### Step 5: Implementation & Pre-Execution Safety
Utilize `hath0r_engine` modules:
- Enforce `GuardrailsManager` before tool executions.
- Use `TieredRouter` to match prompt complexity to model tier (`LIGHT`, `STANDARD`, `REASONING`).
- Structure multi-step reasoning with `ChainOfThought` and programmatic `Assert` checks.

### Step 6: Test Verification & Preflight Gates
```bash
# Run unit test suite
pytest -v

# Run Hath0r PR quality and preflight checks
hath0r preflight
hath0r quality
```

### Step 7: Post-Merge Knowledge Sharing
```bash
# Publish PR knowledge to MCP and group KB
hath0r docs share --pr <pr-number>

# Clean up merged branches
hath0r janitor
```
