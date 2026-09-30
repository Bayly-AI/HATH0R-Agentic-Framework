<p align="center">
  <img src="lib/assets/images/hathor-logo-1.png" alt="HATHOR logo" width="280" />
</p>

# HATHOR Agentic Framework

**The Cognitive Architecture & Governance Framework for Autonomous AI Software Engineering**

HATHOR transforms any software repository into a self-governing, durable operating environment for autonomous AI coding agents and human engineers.

> ### ⚡ The Single Tool You Need: HATH0R CLI
> **You do NOT need complex installations, Python environments, or multi-step dependency setups.**  
> Everything required to operate, govern, audit, and orchestrate autonomous agents across your projects is bundled in the standalone **HATH0R CLI** (`hath0r`).
>
> 📦 **Download Standalone Binaries directly from the repository:**
> - 🍏 **macOS (Apple Silicon):** [`release/hath0r-darwin-arm64`](release/hath0r-darwin-arm64)
> - 🍏 **macOS (Intel):** [`release/hath0r-darwin-x86_64`](release/hath0r-darwin-x86_64)
> - 🐧 **Linux (x86_64):** [`release/hath0r-linux-x86_64`](release/hath0r-linux-x86_64)
> - 🐧 **Linux (ARM64):** [`release/hath0r-linux-arm64`](release/hath0r-linux-arm64)
> - 🪟 **Windows (x64):** [`release/hath0r-windows-x64.cmd`](release/hath0r-windows-x64.cmd)
>
> Or install globally via Python package managers:  
> `pipx install hath0r-cli` (or `pip install hath0r-cli` / `pip install hath0r-engine`)

---

## 🚀 30-Second Quick Start

Get your autonomous agent operating environment running in three steps:

### 1. Download & Verify Binary
```sh
# Make the downloaded standalone binary executable (macOS / Linux)
chmod +x release/hath0r-darwin-arm64

# Verify system health and operational readiness
./release/hath0r-darwin-arm64 doctor
```

### 2. Initialize Any Existing or New Repository
Navigate to any codebase (Python, TypeScript, Go, Rust, C#, polyglot) and initialize Hath0r:
```sh
cd /path/to/your-project
/path/to/release/hath0r-darwin-arm64 init
```

### 3. Run Autonomous Agent Workflows & RAG Queries
```sh
# Query knowledge base and memory graph via CLI
hath0r kb path
hath0r memory search "architectural rules"
hath0r context query

# Execute preflight quality gates
hath0r preflight
hath0r quality
```

---

## 🌟 Cognitive Substrate & Engine Capabilities (`hath0r_engine`)

Hath0r provides an enterprise-grade cognitive substrate exported via `src/hath0r_engine/`:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Enterprise AI Engineering                       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                    HATH0R CLI (Single Operator Tool)                   │
├────────────────────────────────────────────────────────────────────────┤
│ • Automated Repo Onboarding (`hath0r init`)                            │
│ • Universal Bot & Factory Orchestrator                                 │
│ • Streaming Voice Interface & Ambient Daemon                           │
│ • Preflight & Quality Hard Gates (`hath0r preflight / quality`)        │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      Tri-Graph Cognitive Substrate                     │
├───────────────────┬────────────────────────────┬───────────────────────┤
│  KnowledgeGraph   │        ContextGraph        │      MemoryGraph      │
│  (Static Lineage) │     (Dynamic Session)      │ (Temporal & Reflection)│
└───────────────────┴────────────────────────────┴───────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                 Modern Cognitive Subsystems (v1.0.1)                   │
├──────────────────────┬─────────────────────────┬───────────────────────┤
│ • AST Guardrails     │ • Dynamic Tool Router   │ • Durable Replay      │
│ • AI Gateway Tiering │ • Declarative DSPy      │ • Generative UI Sign  │
│ • Zero-Trust Sandbox │ • OpenTelemetry Tracing │ • Voice Speculation   │
└──────────────────────┴─────────────────────────┴───────────────────────┘
```

### 💎 Key Architectural Modules

1. 🧠 **Temporal Tri-Graph Substrate (`hath0r_engine.memory` / `graph`):**
   - **KnowledgeGraph (KG):** Compiles code ASTs, API contracts, and governance policies into relational graph lineage.
   - **ContextGraph (CG):** Dynamically tracks live session spans and subagent delegations.
   - **MemoryGraph (MG):** Stores entities with temporal validity windows (`valid_from`, `valid_to`, `is_valid_at(as_of)`), Letta-compatible paging (`MemoryPagingManager`), and sleep-cycle reflection consolidation (`ReflectionEngine`).

2. 🛡️ **Deterministic Pre-Execution Guardrails (`hath0r_engine.guardrails`):**
   - Static Python AST, destructive shell script, and SQL drop blocking via `SyntaxGuardrail`.
   - In-flight parameter type coercion and JSON schema recovery via `SchemaRepairEngine`.
   - Security incident escalation to human authorization gates via `HumanEscalationAuditHook`.

3. 🔀 **Dynamic MCP Tool Router & Schema Pruning (`hath0r_engine.mcp`):**
   - Hybrid BM25 + dense vector tool ranking (`DynamicToolRouter`) across massive MCP server swarms.
   - Context compression via `SchemaPruner` (`AGGRESSIVE`, `STANDARD`, `MINIMAL`, `NONE`).

4. 🌐 **Multi-Provider AI Gateway & Tiered Routing (`hath0r_engine.gateway`):**
   - Universal LLM routing across `LIGHT`, `STANDARD`, and `REASONING` model tiers.
   - Cosine-similarity `SemanticCache` with FinOps token and cost savings tracking.

5. ⏱️ **Durable Orchestration & Event Replay (`hath0r_engine.orchestration`):**
   - SQLite append-only `EventJournal` with deterministic step memoization and replay recovery in `DurableWorkflowEngine`.
   - Zero-compute human suspension with `HumanHibernationGate` and `@durable_task`.

6. 🧩 **Declarative DSPy Pipelines (`hath0r_engine.pipeline`):**
   - Typed declarative `Signature`, `InputField`, `OutputField`, and step-by-step `ChainOfThought`.
   - Programmatic assertion validation and automated self-correction (`Assert`, `Suggest`).
   - Automated few-shot demonstration synthesis via `BootstrapFewShotCompiler`.

7. 🎨 **Generative UI & Evidence Handshake Protocol (`hath0r_engine.ui`):**
   - Structured visual dashboard components: diff viewers, test status badges, parameter tuning sliders, and cryptographic sign-off cards.
   - Bi-directional state synchronization (`BiDirectionalStateSync`) and deterministic HMAC SHA-256 signature verification (`generate_cryptographic_signature`).

8. 📦 **Zero-Trust Isolated Sandboxes (`hath0r_engine.sandbox`):**
   - Ephemeral micro-VM execution environments (`E2BSandboxProvider`, `DaytonaSandboxProvider`, `LocalSandboxProvider`) with zero-trust network policies managed via `SandboxManager`.

---

## 🛠️ For Framework & Engine Developers

- 📖 **Deep Technical Architecture:** See [TECH_README.md](TECH_README.md).
- 📐 **Contract Schemas:** Located in [`contracts/`](contracts/).
- 🧪 **Unit Tests:** Run `pytest -v` (**97 unit tests passing** across all cognitive subsystems).
- 🏛️ **Control Tower:** Located in [Bayly-AI/HATH0R-CLI](https://github.com/Bayly-AI/HATH0R-CLI).

---

## 📜 Governance Strategies & Playbooks Index

| Capability | Architecture Strategy | Operator Playbook |
| :--- | :--- | :--- |
| **Agent Rules & CLI-First RAG** | [`strategies/agent-rules-rag-cli-first-strategy.md`](docs/governance/strategies/agent-rules-rag-cli-first-strategy.md) | [`playbooks/agent-rules-rag-cli-first-playbook.md`](docs/governance/playbooks/agent-rules-rag-cli-first-playbook.md) |
| **Generative UI & Sign-Off** | [`strategies/generative-ui-evidence-handshake-strategy.md`](docs/governance/strategies/generative-ui-evidence-handshake-strategy.md) | [`playbooks/generative-ui-evidence-handshake-playbook.md`](docs/governance/playbooks/generative-ui-evidence-handshake-playbook.md) |
| **Pre-Execution Guardrails** | [`strategies/deterministic-tool-guardrails-strategy.md`](docs/governance/strategies/deterministic-tool-guardrails-strategy.md) | [`playbooks/deterministic-tool-guardrails-playbook.md`](docs/governance/playbooks/deterministic-tool-guardrails-playbook.md) |
| **Declarative DSPy Pipelines** | [`strategies/declarative-dspy-pipeline-strategy.md`](docs/governance/strategies/declarative-dspy-pipeline-strategy.md) | [`playbooks/declarative-dspy-pipeline-playbook.md`](docs/governance/playbooks/declarative-dspy-pipeline-playbook.md) |
| **AI Gateway & Tiered Routing** | [`strategies/ai-gateway-tiered-routing-strategy.md`](docs/governance/strategies/ai-gateway-tiered-routing-strategy.md) | [`playbooks/ai-gateway-tiered-routing-playbook.md`](docs/governance/playbooks/ai-gateway-tiered-routing-playbook.md) |
| **Durable Workflow Replay** | [`strategies/durable-execution-checkpointing-strategy.md`](docs/governance/strategies/durable-execution-checkpointing-strategy.md) | [`playbooks/durable-execution-checkpointing-playbook.md`](docs/governance/playbooks/durable-execution-checkpointing-playbook.md) |
| **Zero-Trust Compute Sandbox** | [`strategies/isolated-compute-sandbox-strategy.md`](docs/governance/strategies/isolated-compute-sandbox-strategy.md) | [`playbooks/isolated-compute-sandbox-playbook.md`](docs/governance/playbooks/isolated-compute-sandbox-playbook.md) |
| **Dynamic MCP Tool Routing** | [`strategies/dynamic-mcp-tool-router-strategy.md`](docs/governance/strategies/dynamic-mcp-tool-router-strategy.md) | [`playbooks/dynamic-mcp-tool-router-playbook.md`](docs/governance/playbooks/dynamic-mcp-tool-router-playbook.md) |
| **Temporal Knowledge Graphs** | [`strategies/temporal-knowledge-graph-strategy.md`](docs/governance/strategies/temporal-knowledge-graph-strategy.md) | [`playbooks/temporal-knowledge-graph-playbook.md`](docs/governance/playbooks/temporal-knowledge-graph-playbook.md) |

---

## ⚖️ License

Licensed under the [Apache License, Version 2.0](LICENSE).
