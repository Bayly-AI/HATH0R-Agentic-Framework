---
id: docs-subsystem
type: subsystem
title: Documentation Corpus Subsystem
depends_on: [hath0r-framework]
governed_by: [CR-CLI-ENTRY-001, CR-RAG-RETRIEVAL-001, CR-SUBSTRATE-001, cr-branch-gov-001]
---
# Documentation Corpus Subsystem — AGENTS Context

> **Subsystem Role:** Canonical documentation corpus for the HATH0R OpenSource ecosystem. Authoritative source for strategies, playbooks, procedures, runbooks, and architectural RFCs.

## 1. Subsystem KnowledgeGraph Entity Nodes
- [`docs/governance/strategies/agent-rules-rag-cli-first-strategy.md`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/docs/governance/strategies/agent-rules-rag-cli-first-strategy.md): Unified Agent Rules, RAG Strategy & CLI-First doctrine.
- [`docs/governance/playbooks/agent-rules-rag-cli-first-playbook.md`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/docs/governance/playbooks/agent-rules-rag-cli-first-playbook.md): Operator workflow for CLI execution and RAG retrieval.
- [`docs/governance/rules/cr-cli-entry-001.md`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/docs/governance/rules/cr-cli-entry-001.md): Mandatory "Start with the CLI" rule.
- [`docs/governance/rules/cr-playwright-ui-001.md`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/docs/governance/rules/cr-playwright-ui-001.md): Mandatory Playwright UI testing & master test case registration rule.
- [`docs/governance/strategies/playwright-ui-testing-strategy.md`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/docs/governance/strategies/playwright-ui-testing-strategy.md): Playwright UI testing and test governance strategy.
- [`docs/architect/hathor-adr-007-taguchi-techniques-robust-design-20261002.md`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/docs/architect/hathor-adr-007-taguchi-techniques-robust-design-20261002.md): Taguchi Techniques for Robust Design, OATS, and Quality Loss Optimization.
- [`docs/architect/hathor-adr-008-pixel-native-vision-tokenizer-tax-20261002.md`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/docs/architect/hathor-adr-008-pixel-native-vision-tokenizer-tax-20261002.md): Pixel-Native Vision Ingestion and Tokenizer Tax Auditing.
- [`docs/runbook.md`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/docs/runbook.md): Framework operational runbook.

## 2. Frontmatter Standards for KG Ingestion
All canonical markdown documents in `docs/` MUST define:
- `id`: Unique identifier (e.g., `strategy-rag-cli-001`, `cr-cli-entry-001`).
- `type`: `procedure | strategy | playbook | runbook | checklist | policy | standard`.
- `depends_on`: List of upstream node IDs.
- `implements`: List of contract schema IDs or RFCs.
- `governed_by`: List of governing rules.

## 3. RAG Retrieval & Publishing Discipline
- Agents must query knowledge via `hath0r kb path` and `hath0r memory search`.
- Completed PR documentation must be published via `hath0r docs share --pr <number>`.

---

## CR-TASK-EVAL-001 (Automatic Task Evaluation Before Announcing Complete — CRITICAL · CANONICAL)
- **Mandatory Pre-Announcement Task Evaluation Gate**: Every task MUST be evaluated across the 4-tier hybrid evaluation pipeline (Tier 1 Deterministic Rubrics, Tier 2 Trajectory & FinOps Efficiency, Tier 3 Adversarial & Diff Critics, Tier 4 Goal Alignment & Consensus) prior to announcing work as Complete.
- **Composite Reward Threshold**: Task completion requires `passed_gate: true` and composite reward score `R_task >= 0.80` persisted in `.hath0r/evals/latest.json` and compounded as an `eval:<task_id>` node in `.hath0r/memory/graph.json`.
- **How to Verify**: Run `hath0r evals run` and `hath0r evals verify` before announcing Complete (`EndOfTaskBot`, `TaskAnnouncerBot.announce_complete`, and `CleanReposWorkflowBot` enforce this gate automatically).
- **Not Complete Until Evaluated**: A missing, failing, or unverified task evaluation means the work is not Complete.
