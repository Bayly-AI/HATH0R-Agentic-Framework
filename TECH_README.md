# HATH0R Framework — Technical Reference & Architecture Guide

> **Core agentic architecture, contract specifications, and graph substrate for the HATH0R ecosystem.**

| Field | Value |
|---|---|
| Product | `HATH0R-Agentic-Framework` |
| Group | `hath0r-opensource` |
| Local Path | `/Users/raybayly/Development/OpenSource/hath0r` |
| Control Tower | `/Users/raybayly/Development/OpenSource/HATH0R-CLI` (`Bayly-AI/HATH0R-CLI`) |
| Canonical Knowledgebase | `/Users/raybayly/Development/OpenSource/.hath0r/knowledgebase` |
| Canonical Docs Corpus | `docs/` |
| GitHub | [Bayly-AI/HATH0R-Agentic-Framework](https://github.com/Bayly-AI/HATH0R-Agentic-Framework) |

---

## 1. Technical Overview

The HATH0R Framework provides the foundational protocols, contracts, schemas, security guards, and graph execution layers that govern how AI agents operate deterministically across codebases.

### Key Capabilities
- **Static KnowledgeGraph (`lib/graph/`):** Frontmatter and Markdown cross-reference extractor that compiles repository truth into an indexed entity-relationship graph (`hath0r-knowledgegraph-v1`).
- **Dynamic ContextGraph (`lib/context/`):** Runtime multi-agent session tracker for subagent delegation topologies, ephemeral state, and JEV guard execution trails (`hath0r-contextgraph-v1`).
- **Justified Execution Verification (`lib/jev/`):** Zero-trust execution boundary intercepting and verifying mutating agent tool invocations against signed policies.
- **Voice Interface Subsystem (`lib/voice/`):** Low-latency streaming voice engine with speculative routing, VAD endpointing, and System 1 / System 2 escalation.

---

## 2. Architecture & Subsystems

```text
                        ┌──────────────────────────────────────┐
                        │          Active LLM Agent            │
                        └──────────────────┬───────────────────┘
                                           │
                        ┌──────────────────▼───────────────────┐
                        │      Operator CLI (`hath0r`)         │
                        └─────────┬──────────────────┬─────────┘
                                  │                  │
                ┌─────────────────▼────────┐  ┌──────▼──────────────────┐
                │   Static KnowledgeGraph  │  │   Dynamic ContextGraph  │
                │   (Files-as-Truth / KG)  │  │   (Session Topologies)  │
                └─────────────────┬────────┘  └──────┬──────────────────┘
                                  │                  │
                ┌─────────────────▼──────────────────▼─────────┐
                │      JEV Guard & Security Mediation          │
                └──────────────────────────┬───────────────────┘
                                           │
                        ┌──────────────────▼───────────────────┐
                        │      Universal Project Layout        │
                        │    (cfg / bin / lib / contracts)     │
                        └──────────────────────────────────────┘
```

### Subsystem Directory Map
- **`cfg/`**: Declarative configuration for observability (OpenTelemetry), feature flags (OpenFeature), Docker stacks, MCP servers (`cfg/mcp.servers.json`), and tower pointers (`cfg/knowledge-tower.yaml`).
- **`contracts/`**: Authoritative JSON Schema definitions (`hath0r-*.schema.json`) and exit codes (`contracts/exit-codes.yaml`).
- **`docs/`**: Canonical documentation corpus (Governance, Procedures, Strategies, Playbooks, Runbooks, Checklists).
- **`lib/`**: Core runtime engines:
  - `lib/graph/`: KnowledgeGraph extractor and lineage traversal.
  - `lib/context/`: ContextGraph session and subagent hierarchy management.
  - `lib/jev/`: JEV client and tool execution guard.
  - `lib/voice/`: Voice engine, speculative pipeline, and audio adapters.
- **`bin/`**: Member initialization and bootstrap scripts (`bin/hath0r-bootstrap.sh`).
- **`tests/`**: Pytest regression and contract verification suite.

---

## 3. Contracts & Schemas

| Contract Schema | Version | Purpose |
|---|---|---|
| [`contracts/hath0r-knowledgegraph-v1.schema.json`](contracts/hath0r-knowledgegraph-v1.schema.json) | `1.0.0` | Entity nodes and relational edges for static codebase knowledge. |
| [`contracts/hath0r-contextgraph-v1.schema.json`](contracts/hath0r-contextgraph-v1.schema.json) | `1.0.0` | Dynamic session snapshot, subagent delegation, and tool guard tracking. |
| [`contracts/hath0r-cli-response-v1.schema.json`](contracts/hath0r-cli-response-v1.schema.json) | `1.0.0` | Standardized JSON payload envelope for all CLI command responses. |
| [`contracts/hath0r-voice-action-v1.schema.json`](contracts/hath0r-voice-action-v1.schema.json) | `1.0.0` | Typed voice intent and platform action execution contract. |
| [`contracts/hath0r-factory-v1.schema.json`](contracts/hath0r-factory-v1.schema.json) | `1.0.0` | Declarative automation factory and orchestrated bot manifest. |

---

## 4. Developer Quickstart & Testing

### Environment Setup
```sh
cd /path/to/OpenSource/hath0r-framework
./bin/hath0r-bootstrap.sh
```

### Running Test Suite
```sh
PYTHONPATH=. pytest -v
```

---

## 5. Governance & Policy Rules

1. **`CR-CLI-ENTRY-001` (Start with the CLI):** Agents must begin every task via the `hath0r` CLI rather than ad-hoc scripts (`docs/governance/rules/cr-cli-entry-001.md`).
2. **`cr-hath0r-root-001` (Hidden Root):** Only `.hath0r/` is permitted for framework metadata. Legacy roots (`.ai/`, `.customerSystem/`, `.infraOS/`) are strictly forbidden.
3. **`cr-branch-gov-001` (Branching & Promotion):** Feature branches follow `feature/<issue-number>-slug` branching from and targeting `development`.

---

## 6. License

Apache License 2.0 — see [LICENSE](LICENSE).
