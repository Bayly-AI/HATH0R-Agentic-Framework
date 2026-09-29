---
id: docs-subsystem
type: subsystem
title: Documentation Corpus Subsystem
depends_on: [hath0r-framework]
governed_by: [cr-branch-gov-001, CR-CLI-ENTRY-001]
---
# Documentation Corpus Subsystem — AGENTS Context

> **Subsystem Role:** Canonical documentation corpus for the HATH0R OpenSource ecosystem.

## 1. Subsystem KnowledgeGraph Entity Nodes
- [`docs/governance/strategies/knowledgegraph-contextgraph-strategy.md`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/docs/governance/strategies/knowledgegraph-contextgraph-strategy.md): Strategic RFC for hybrid KG/CG.
- [`docs/governance/rules/cr-cli-entry-001.md`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/docs/governance/rules/cr-cli-entry-001.md): Mandatory "Start with the CLI" rule.
- [`docs/runbook.md`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/docs/runbook.md): Framework operational runbook.

## 2. Frontmatter Standards for KG Ingestion
All canonical markdown documents in `docs/` MUST define:
- `id`: Unique identifier (e.g., `strategy-kg-cg-001`, `cr-cli-entry-001`).
- `type`: `procedure | strategy | playbook | runbook | checklist | policy | standard`.
- `depends_on`: List of upstream node IDs.
- `implements`: List of contract schema IDs or RFCs.
- `governed_by`: List of governing rules.
