---
id: contracts-subsystem
type: subsystem
title: Contracts & Schemas Subsystem
depends_on: [hath0r-framework]
governed_by: [CR-CLI-ENTRY-001, CR-RAG-RETRIEVAL-001, CR-SUBSTRATE-001, cr-branch-gov-001]
---
# Contracts Subsystem — AGENTS Context

> **Subsystem Role:** Authoritative source for JSON Schemas, exit code specifications, API payloads, and graph contracts across the HATH0R ecosystem.

## 1. Subsystem KnowledgeGraph Entity Nodes
- [`contracts/hath0r-knowledgegraph-v1.schema.json`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/contracts/hath0r-knowledgegraph-v1.schema.json): Static KnowledgeGraph entity nodes & edge schema.
- [`contracts/hath0r-contextgraph-v1.schema.json`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/contracts/hath0r-contextgraph-v1.schema.json): Runtime ContextGraph session & JEV guard schema.
- [`contracts/hath0r-cli-response-v1.schema.json`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/contracts/hath0r-cli-response-v1.schema.json): Standardized CLI envelope contract.
- [`contracts/exit-codes.yaml`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/contracts/exit-codes.yaml): CLI and engine process exit codes.

## 2. CLI Validation & Invariants
- Validate schema integrity via `hath0r contracts validate`.
- Maintain strict backward compatibility for all schema contracts (`hath0r.*`).
- Mirror active schemas into `lib/schemas/` for in-tree validation without network dependencies.
- Changes to schemas require validation test additions in `tests/test_graph_contracts.py`.
