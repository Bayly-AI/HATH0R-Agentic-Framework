---
id: tests-subsystem
type: subsystem
title: Testing Subsystem
depends_on: [contracts-subsystem, lib-subsystem, engine-core-subsystem]
governed_by: [CR-CLI-ENTRY-001, CR-RAG-RETRIEVAL-001, CR-SUBSTRATE-001, CR-PLAYWRIGHT-UI-001, cr-branch-gov-001]
---
# Testing Subsystem — AGENTS Context

> **Subsystem Role:** Unit, regression, contract verification, cognitive substrate validation, Playwright UI testing, and latency benchmark test harness.

## 1. Subsystem KnowledgeGraph Entity Nodes
- [`tests/test_dspy_pipeline.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/tests/test_dspy_pipeline.py): Declarative DSPy pipeline and teleprompter tests.
- [`tests/test_tool_guardrails.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/tests/test_tool_guardrails.py): Pre-execution AST security and schema repair tests.
- [`tests/test_generative_ui.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/tests/test_generative_ui.py): Generative UI evidence handshake and crypto sign-off tests.
- [`tests/test_playwright_testing.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/tests/test_playwright_testing.py): Playwright UI test runner, catalog manager, and schema validation tests.
- [`tests/test_taguchi.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/tests/test_taguchi.py): Taguchi Methods, Orthogonal Arrays, and Robust Parameter Design tests.
- [`tests/e2e/master-playwright-tests.json`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/tests/e2e/master-playwright-tests.json): Master test case document in Playwright-compliant format.
- [`tests/test_ai_gateway.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/tests/test_ai_gateway.py): Tiered routing, semantic cache, and FinOps tests.
- [`tests/test_tokenizer_tax.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/tests/test_tokenizer_tax.py): FinOps Tokenizer Tax Auditor, multilingual inflation, and VRAM overhead tests.
- [`tests/test_vision_pixel_native.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/tests/test_vision_pixel_native.py): Pixel-native 2D document parsing and DOM-independent Playwright grounding tests.
- [`tests/test_durable_orchestration.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/tests/test_durable_orchestration.py): Event journaling, replay, and human hibernation tests.
- [`tests/test_sandbox_providers.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/tests/test_sandbox_providers.py): Zero-trust sandbox execution tests.
- [`tests/test_mcp_tool_router.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/tests/test_mcp_tool_router.py): Dynamic MCP tool routing and schema pruner tests.
- [`tests/test_temporal_knowledge_graph.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/tests/test_temporal_knowledge_graph.py): Temporal graph edge validity tests.

## 2. CLI Execution & Quality Gates
- Execute test suite: `pytest -v`.
- Playwright UI test suite execution: `pytest tests/test_playwright_testing.py`.
- Sync Playwright master test catalog on clean-repo: `PlaywrightMasterCatalogManager.audit_and_sync_test_cases()`.
- Enforce preflight & quality gate bot: `hath0r preflight` and `hath0r quality`.

---

## CR-TASK-EVAL-001 (Automatic Task Evaluation Before Announcing Complete — CRITICAL · CANONICAL)
- **Mandatory Pre-Announcement Task Evaluation Gate**: Every task MUST be evaluated across the 4-tier hybrid evaluation pipeline (Tier 1 Deterministic Rubrics, Tier 2 Trajectory & FinOps Efficiency, Tier 3 Adversarial & Diff Critics, Tier 4 Goal Alignment & Consensus) prior to announcing work as Complete.
- **Composite Reward Threshold**: Task completion requires `passed_gate: true` and composite reward score `R_task >= 0.80` persisted in `.hath0r/evals/latest.json` and compounded as an `eval:<task_id>` node in `.hath0r/memory/graph.json`.
- **How to Verify**: Run `hath0r evals run` and `hath0r evals verify` before announcing Complete (`EndOfTaskBot`, `TaskAnnouncerBot.announce_complete`, and `CleanReposWorkflowBot` enforce this gate automatically).
- **Not Complete Until Evaluated**: A missing, failing, or unverified task evaluation means the work is not Complete.
