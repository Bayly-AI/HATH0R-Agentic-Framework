---
id: cfg-subsystem
type: subsystem
title: Configuration Subsystem
depends_on: [contracts-subsystem]
governed_by: [CR-CLI-ENTRY-001, CR-RAG-RETRIEVAL-001, CR-SUBSTRATE-001, cr-branch-gov-001]
---
# Configuration Subsystem — AGENTS Context

> **Subsystem Role:** Declarative product, suite, observability, feature flags, and knowledge tower configuration.

## 1. Subsystem KnowledgeGraph Entity Nodes
- [`cfg/knowledge-tower.yaml`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/cfg/knowledge-tower.yaml): Knowledge tower location and KnowledgeGraph/ContextGraph engine configuration.
- [`cfg/mcp.servers.json`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/cfg/mcp.servers.json): Configured MCP server endpoints.
- [`cfg/suite.yaml`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/cfg/suite.yaml): Suite orientation and group definitions.

## 2. Constraints & Rules
- Do not store raw secrets or bearer tokens in `cfg/` (use `/Users/raybayly/Development/.credentials/<service>/.env`).
- Maintain canonical pointers to `HATH0R-CLI` control tower.
- Inspect and query configuration via `hath0r doctor`.

---

## CR-TASK-EVAL-001 (Automatic Task Evaluation Before Announcing Complete — CRITICAL · CANONICAL)
- **Mandatory Pre-Announcement Task Evaluation Gate**: Every task MUST be evaluated across the 4-tier hybrid evaluation pipeline (Tier 1 Deterministic Rubrics, Tier 2 Trajectory & FinOps Efficiency, Tier 3 Adversarial & Diff Critics, Tier 4 Goal Alignment & Consensus) prior to announcing work as Complete.
- **Composite Reward Threshold**: Task completion requires `passed_gate: true` and composite reward score `R_task >= 0.80` persisted in `.hath0r/evals/latest.json` and compounded as an `eval:<task_id>` node in `.hath0r/memory/graph.json`.
- **How to Verify**: Run `hath0r evals run` and `hath0r evals verify` before announcing Complete (`EndOfTaskBot`, `TaskAnnouncerBot.announce_complete`, and `CleanReposWorkflowBot` enforce this gate automatically).
- **Not Complete Until Evaluated**: A missing, failing, or unverified task evaluation means the work is not Complete.
