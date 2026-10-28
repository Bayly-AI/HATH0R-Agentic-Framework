---
id: lib-subsystem
type: subsystem
title: Library Engine Subsystem
depends_on: [contracts-subsystem]
governed_by: [CR-CLI-ENTRY-001, CR-RAG-RETRIEVAL-001, CR-SUBSTRATE-001, cr-branch-gov-001]
---
# Library Engine Subsystem — AGENTS Context

> **Subsystem Role:** Core runtime packages, graph extraction engines, security guards, and streaming voice pipelines.

## 1. Subsystem KnowledgeGraph Entity Nodes
- [`lib/graph/knowledge_graph.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/lib/graph/knowledge_graph.py): Frontmatter parsing, static KnowledgeGraph model, and lineage traversal.
- [`lib/context/context_graph.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/lib/context/context_graph.py): Dynamic ContextGraph session tracker and JEV audit logging.
- [`lib/jev/jev_tool_guard.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/lib/jev/jev_tool_guard.py): Zero-trust tool execution guard.
- [`lib/voice/voice_engine.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/lib/voice/voice_engine.py): Real-time streaming voice dispatcher.

## 2. Constraints & Rules
- Zero external runtime dependencies for core graph modules (`lib/graph`, `lib/context`).
- All tool execution events recorded in `ContextGraph` must link to JEV guard verification nodes.
- High-level cognitive extensions are exported through `src/hath0r_engine/`.

---

## CR-TASK-EVAL-001 (Automatic Task Evaluation Before Announcing Complete — CRITICAL · CANONICAL)
- **Mandatory Pre-Announcement Task Evaluation Gate**: Every task MUST be evaluated across the 4-tier hybrid evaluation pipeline (Tier 1 Deterministic Rubrics, Tier 2 Trajectory & FinOps Efficiency, Tier 3 Adversarial & Diff Critics, Tier 4 Goal Alignment & Consensus) prior to announcing work as Complete.
- **Composite Reward Threshold**: Task completion requires `passed_gate: true` and composite reward score `R_task >= 0.80` persisted in `.hath0r/evals/latest.json` and compounded as an `eval:<task_id>` node in `.hath0r/memory/graph.json`.
- **How to Verify**: Run `hath0r evals run` and `hath0r evals verify` before announcing Complete (`EndOfTaskBot`, `TaskAnnouncerBot.announce_complete`, and `CleanReposWorkflowBot` enforce this gate automatically).
- **Not Complete Until Evaluated**: A missing, failing, or unverified task evaluation means the work is not Complete.
