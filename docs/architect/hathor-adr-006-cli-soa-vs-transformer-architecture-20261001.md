---
id: HATHOR-ADR-006
title: HATHOR-ADR-006 — CLI Architectural Evaluation: Service-Oriented Architecture (SOA) vs. Transformer Architecture
summary: Evaluates the architectural proposal to replace Hath0r CLI's Service-Oriented Architecture (SOA) with a pure Transformer/Neural architecture. Decision is to retain SOA as the deterministic control plane and leverage Transformers as modular cognitive services (Hybrid Cognitive Substrate).
doc_type: ADR
diataxis: decision
audience: [architect, agent, developer]
tags: [architecture, cli, soa, transformers, cognition, substrate]
version: 1.0.0
status: accepted
created: '2026-10-01'
updated: '2026-10-01'
owner: Raymond Bayly (BaylyAI)
review: {trust: verified, reviewed_by: 'Raymond Bayly', reviewed_at: '2026-10-01', interval: null, next_review: null}
stale: false
supersedes: []
superseded_by: null
amended_by: []
parent: null
sources: []
---
# HATHOR-ADR-006 — CLI Architectural Evaluation: SOA vs. Transformer Architecture

## Status
**ACCEPTED** (2026-10-01)

## Decision Class
Architecture Decision Record (Control Plane & Substrate Architecture)

---

## 1. Context & Problem Statement

The question was posed whether the **HATH0R-CLI** control plane should be refactored from its current **Service-Oriented Architecture (SOA)** / Modular Substrate to an end-to-end **Transformer Architecture**.

The HATH0R-CLI serves as the primary control tower and deterministic execution harness across the HATH0R ecosystem (`hath0r init`, `doctor`, `branch validate`, `preflight`, `contracts`, `factory`, `memory`, `mcp`, `jev`).

---

## 2. Decision

**REJECT** a pure/end-to-end Transformer architecture replacement for the CLI control plane.  
**MAINTAIN & ADVANCE** the **Hybrid Cognitive Substrate Doctrine**:
1. **Deterministic Control Plane (SOA / Event-Driven Modular Substrate)**: Core CLI operations, schema contracts, AST parsing, sandboxed execution, and governance enforcement remain strictly deterministic and service-oriented.
2. **Pluggable Cognitive Micro-Services (Transformers & DSPy)**: Neural attention models, dense embedding encoders, and transformer LLMs are consumed on-demand through dedicated interface boundaries (`AIGatewayClient`, `DynamicToolRouter`, `ReflectionEngine`, `MemoryPagingManager`).

```
                    HATH0R-CLI Operator / Control Plane
                                    │
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
Deterministic Services      Tri-Graph Engine             Zero-Trust Execution
• git-branch-manager        • KnowledgeGraph (AST)       • JEV System One Guards
• schema-contracts-validator• ContextGraph (Lineage)     • Syntax AST Guardrails
• preflight-evaluator       • MemoryGraph (Working)      • Sandbox Providers
       │                            │                            │
       └────────────────────────────┼────────────────────────────┘
                                    ▼
                      Cognitive Substrate Interface
                  (AI Gateway, Tiered Routing, DSPy)
```

---

## 3. Analysis & Evaluation

### 3.1 Determinism and Governance Compliance
* **SOA Substrate**: CLI operations like branch naming validation (`CR-BRANCH-GOV-001`), promotion order checks (`CR-BAI-001`), and JSON schema validations (`contracts/`) require 100% reproducible execution and standard POSIX exit codes.
* **Pure Transformer**: Autoregressive neural token generation is non-deterministic, probabilistic, and prone to hallucinations or subtle semantic drift when evaluating boolean constraints.

### 3.2 Latency and Cold-Start Overhead
* **SOA Substrate**: Boots in `< 50ms` using standard Python virtual environments or `pipx`.
* **Pure Transformer**: Local inference requires loading multi-gigabyte weight tensors into VRAM/RAM (multi-second cold start). Remote API calls introduce 200ms–2000ms network round-trip latency for local filesystem checks.

### 3.3 Security & Zero-Trust Sandboxing
* **SOA Substrate**: Enforces compile-time schema contracts (`pydantic`, `jsonschema`), AST validation (`SyntaxGuardrail`), and sandboxed execution (`LocalSandboxProvider`, `E2BSandboxProvider`).
* **Pure Transformer**: Direct model-to-OS execution without service boundaries creates vulnerability to prompt injection, uncontrolled tool calling, and arbitrary parameter generation.

### 3.4 Summary Trade-Off Matrix

| Dimension | Service-Oriented Architecture (SOA) | Pure Transformer Architecture | Hybrid Substrate (Hath0r Adopted) |
| :--- | :--- | :--- | :--- |
| **Cold-Start Time** | ⚡ < 100ms | 🐢 Multi-second / GPU required | ⚡ < 100ms for deterministic core |
| **Determinism** | 🛡️ 100% reproducible | ⚠️ Stochastic / Probabilistic | 🛡️ Deterministic gates & contracts |
| **Zero-Trust Safety**| 🔒 Rigid AST/Schema checks | ⚠️ Susceptible to prompt injection | 🔒 Guardrail & Sandbox mediation |
| **Cognitive Depth** | ❌ Static logic | 🧠 Broad semantic reasoning | 🧠 DSPy & AI Gateway on-demand |
| **Offline Reliability**| 💻 Complete offline operability | ⚠️ Heavy local footprint | 💻 Core functions work offline |

---

## 4. Consequences & Implementation Guidance

1. **CLI Commands remain contract-backed**: All CLI commands continue to inherit from deterministic command handlers and declarative factories.
2. **Cognitive features use the Cognitive Substrate**: Semantic memory summarization (`hath0r memory read/update`), neural KB search (`hath0r kb search`), and agentic code repair (`DynamicToolRouter`) route through `src/hath0r_engine/` cognitive modules.
3. **No direct LLM coupling in core utilities**: CLI utilities (`hath0r branch`, `hath0r doctor`, `hath0r preflight`) must never block on or require neural model availability for core operations.
