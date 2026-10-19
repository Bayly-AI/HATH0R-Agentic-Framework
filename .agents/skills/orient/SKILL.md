---
name: orient
description: Standard operating procedure for repository orientation. Activates whenever the operator runs "orient", "run orient", "orient repo", "orient repository", or requests full repository orientation.
---

# Repository Orientation Standard Operating Procedure

This workflow executes full cognitive and operational orientation when an operator triggers **"orient"**. It establishes complete context across governance rules, application architecture, AST symbol trees, agent performance telemetry, and runtime parameter calibration.

Whenever an operator or prompt triggers **"orient"**, execute the following 6 steps in exact sequence:

---

## 6-Step Orientation Procedure

### Step 1: Read the Agents, Rules, and MemoryGraph from AgentGraph
- Ensure `.hath0r/memory/graph.json` is initialized (`hath0r memory init`) and query the AgentGraph snapshot at `.hath0r/agentgraph/snapshot.json` (or via `hath0r agentgraph status`, `hath0r agentgraph query "rules"`, and `hath0r memory search`).
- Extract:
  - **Agent Roles**: Identify all declared roles (e.g. `role:developer`, `role:reader`), their permitted tools, forbidden tools, and inheritance hierarchy.
  - **Rules & Governance Policies**: Identify all active rule policies (`CR-CLI-ENTRY-001`, `CR-AGENTGRAPH-001`, `CR-MEMORY-COMPOUND-001`, `CR-CICCCDCT-001`, `CR-IAC-001`, `CR-BRANCH-GOV-001`, etc.), their priorities, and restricted actions.
  - **MemoryGraph, Micro Memory Session & Graph Topology**: Ensure `.hath0r/memory/graph.json` and `.hath0r/memory/sessions/current.json` are initialized, read the active Micro Memory Session (`hath0r memory session read`), write orientation observations (`hath0r memory session write`), tally node distributions across Knowledge, Memory, Rules, and Context planes, and verify compounded memory nodes.

### Step 2: Read the Project Readme
- Read the repository root `README.md` (and `TECH_README.md` if present).
- Extract:
  - Repository identity, name, mission, and OpenSource group membership.
  - Technology stack, build targets, and primary runtime environment.
  - Key architectural components and directory structure highlights.

### Step 3: Scan Code to Understand the Application
- Discover and scan the codebase (e.g. `src/`, `lib/`, `contracts/`, `tests/`):
  - Identify primary programming languages and file distributions.
  - Inspect core entry points, modules, and factories.
  - Extract top-level AST symbols (classes, methods, functions) using structural code intelligence (`CodeParser` / `hath0r code outline`).
  - Synthesize a concise technical overview of the application's functionality.

### Step 4: Run Agent Metrics
- Execute the Agent Metrics inspection via `AgentMetricsBot` / `hath0r observe charts` / `hath0r pmat stats`:
  - **Observability Tracing**: Latency quantiles (P50 median, P90 SLA, P95, P99 tail latency, mean ± std dev), total requests, token volume, and spend (USD).
  - **Token Telemetry Histogram**: Binned distribution of token consumption.
  - **PMAT Multi-Dimensional Code Churn & Hotspots**: Provability score, cyclomatic complexity, hotspot count, and highest-risk files ranked by Composite Hotspot Risk Index ($R$).

### Step 5: Run Agent Calibration
- Execute Continuous Calibration via `hath0r cicccd calibrate` (or `CCCDCalibrationLoop`):
  - Check calibration freshness SLA ($\le 24.0\text{ hours}$).
  - Trigger parameter calibration loop.
  - Record updated calibrated runtime hyperparameters:
    - `temperature`
    - `max_tokens`
    - `top_p`
    - `retry_count`
    - `guardrail_threshold`

### Step 6: Show a Report Detailing the Findings, the Metrics, and the Calibration
- Present a comprehensive, beautifully structured orientation report to the operator detailing:
  1. **AgentGraph Findings**: Active roles, permitted/forbidden tools, governing rules.
  2. **Project Findings**: Readme overview, technology stack, and architectural role.
  3. **Application Code Findings**: Subsystem layout, language breakdown, and key entry points.
  4. **Agent Metrics Report**: Latencies, token usage, spend, and PMAT hotspot risk indices.
  5. **Agent Calibration Report**: Calibration ID, timestamp, freshness status, and tuned parameters.
  6. **Executive Orientation Verdict & Recommendations**: Summary of repository readiness and immediate next steps.
