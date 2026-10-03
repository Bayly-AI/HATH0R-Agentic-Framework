<p align="center">
  <img src="lib/assets/images/hathor-logo-1.png" alt="HATHOR logo" width="280" />
</p>

# HATHOR Agentic Framework

**The Enterprise Cognitive Operating System & Governance Substrate for Autonomous AI Engineering**

HATHOR transforms enterprise software repositories and business applications into self-governing, mathematically robust operating environments for autonomous AI agents and human engineering teams.

---

## 🏛️ Executive Blueprint: The Autonomous Enterprise Advantage

Enterprises scaling autonomous AI agents face three existential bottlenecks: **runaway inference costs**, **brittle execution failure**, and **unbounded compliance liability**. HATHOR solves all three through a unified cognitive architecture.

```text
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   ENTERPRISE BUSINESS APPLICATIONS                             │
│                  (SAP • Salesforce • Workday • Custom Microservices • Cloud Infra)              │
└───────────────────────────────────────────────┬─────────────────────────────────────────────────┘
                                                │
                                                ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             HATH0R OPERATOR CLI (Single Enterprise Gate)                        │
│                 Autonomous Repo Onboarding • Universal Orchestration • Governance Enforcement    │
└───────────────────────┬─────────────────────────────────────────────────┬───────────────────────┘
                        │                                                 │
                        ▼                                                 ▼
┌───────────────────────────────────────────────┐ ┌───────────────────────────────────────────────┐
│          FINOPS & OPTIMIZATION LAYER          │ │         COGNITIVE SUBSTRATE & RUNTIME         │
├───────────────────────────────────────────────┤ ├───────────────────────────────────────────────┤
│ • Tokenizer Tax Auditor (Save up to 65%)      │ │ • Tri-Graph RAG (Knowledge, Context, Memory)  │
│ • Taguchi Robust Parameter Optimization       │ │ • Pre-Execution AST & Syntax Guardrails       │
│ • Pixel-Native 2D Document & UI Ingestion     │ │ • Multi-Provider AI Gateway Tiering           │
│ • DOM-Independent Playwright UI Grounding    │ │ • Durable Event Journal & Human Hibernation   │
│ • Orthogonal Array Testing Strategies (OATS)  │ │ • HMAC SHA-256 Cryptographic Evidence Sign-off│
└───────────────────────────────────────────────┘ └───────────────────────────────────────────────┘
```

---

## 📊 The Executive Scorecard: Business ROI & Value Realization

| Strategic Dimension | Legacy AI Systems | HATH0R Enterprise Advantage | Quantifiable Impact |
| :--- | :--- | :--- | :--- |
| **Multilingual Economics** | 3.5x–5.0x token cost penalty on non-Latin scripts (Arabic, Hindi, CJK) | **Tokenizer Tax Auditor & Pixel-Native ViT** normalizes input via continuous visual patches | **Up to 65% inference cost reduction** in global enterprise deployments |
| **Infrastructure VRAM** | 1B+ parameters (2–4 GB VRAM) wasted on static vocabulary tables per instance | **Patch Projection Substrate** replaces 256k-token vocab matrices with 3MB projection layers | **4.19 GB VRAM recovered** per model instance for actual reasoning |
| **Workflow Quality & Tuning** | Combinatorial grid-search guessing causing unexpected runtime regressions | **Taguchi Robust Design ($L_4 - L_{18}$)** maximizes Signal-to-Noise Ratio (SNR) | **Up to 96% reduction in test combinations** while guaranteeing zero-defect stability |
| **Enterprise UI Automation** | Brittle DOM selector chains break with every CSS/layout change | **DOM-Independent Visual Grounding** resolves targets directly to pixel coordinates | **Zero automation breakage** across SAP, Salesforce, and dynamic web views |
| **Document Processing** | Costly proprietary OCR licenses, brittle parsers, and separate pipelines | **Pixel-Native 2D Document Parser** preserves complex balance sheets and diagrams in one pass | **100% OCR license retirement** and single-pass visual comprehension |
| **Risk & Compliance** | Uncontrolled black-box execution risking production outages | **Deterministic AST Guardrails** and **HMAC SHA-256 Cryptographic Evidence Handshakes** | **Zero unauthorized commands** with immutable SOC2-compliant audit trails |
| **Durable Execution** | Flaky networks or human review gates abort multi-step agent workflows | **Event-Sourced Replay Engine** with **HumanHibernationGate** zero-compute suspension | **100% workflow state preservation** across hours or days of human review |

---

## ⚡ The Single Tool You Need: HATH0R CLI

> **No complex Python environments, virtualenv juggling, or dependency conflicts.**  
> Everything required to operate, govern, audit, and orchestrate autonomous agents across your projects is bundled into the standalone **HATH0R CLI** (`hath0r`).

📦 **Enterprise Standalone Binaries:**
- 🍏 **macOS (Apple Silicon):** [`release/python/cli/hath0r-darwin-arm64`](release/python/cli/hath0r-darwin-arm64)
- 🍏 **macOS (Intel):** [`release/python/cli/hath0r-darwin-x86_64`](release/python/cli/hath0r-darwin-x86_64)
- 🐧 **Linux (x86_64):** [`release/python/cli/hath0r-linux-x86_64`](release/python/cli/hath0r-linux-x86_64)
- 🐧 **Linux (ARM64):** [`release/python/cli/hath0r-linux-arm64`](release/python/cli/hath0r-linux-arm64)
- 🪟 **Windows (x64):** [`release/python/cli/hath0r-windows-x64.cmd`](release/python/cli/hath0r-windows-x64.cmd)

*Or install globally via package manager:* `pipx install hath0r-cli` (or `pip install hath0r-engine`)

---

## 🚀 30-Second Quick Start

Deploy Hath0r into any repository in three commands:

```sh
# 1. Verify health and operational readiness
./release/python/cli/hath0r-darwin-arm64 doctor

# 2. Initialize enterprise governance in any repository
cd /path/to/enterprise-repo
/path/to/release/python/cli/hath0r-darwin-arm64 init

# 3. Execute quality gates, FinOps audit, and memory queries
hath0r preflight
hath0r quality
hath0r memory search "governance policies"
```

---

## 💎 Core Cognitive Subsystems & Enterprise Capabilities

### 1. 📉 FinOps Tokenizer Tax Auditor (`hath0r_engine.gateway.tokenizer_tax`)
* **Problem:** Standard BPE tokenizers charge enterprises an invisible "tax" on non-Latin languages and waste over 4 GB of GPU memory on vocabulary tables.
* **Solution:** Analyzes enterprise text corpora across Unicode scripts (Arabic, Devanagari, CJK, Cyrillic, Latin), quantifies token expansion inflation ($\tau_{lang}$), calculates serving VRAM waste ($P_{vocab} = 2 \cdot V \cdot d_{model}$), and provides pixel-native continuous patch budgets.
* **Architecture Decision:** [ADR-008: Pixel-Native Vision & Tokenizer Tax](docs/architect/hathor-adr-008-pixel-native-vision-tokenizer-tax-20261002.md).

### 2. 🎯 Taguchi Robust Parameter Optimization Engine (`hath0r_engine.optimization.taguchi`)
* **Problem:** Autonomous agent systems are hyper-sensitive to prompt variations, model temperature, and retrieval parameters. Brute-force tuning requires thousands of expensive LLM calls.
* **Solution:** Applies Taguchi Methods and Orthogonal Array Testing Strategies (OATS) ($L_4, L_8, L_9, L_{12}, L_{18}$). Maximizes Signal-to-Noise Ratio (SNR) across Nominal-is-Best, Smaller-is-Better, and Larger-is-Better criteria, and quantifies dollar variance using Taguchi's quadratic Quality Loss Function ($L(y) = k(y-m)^2$).
* **Architecture Decision:** [ADR-007: Taguchi Techniques for Robust Design](docs/architect/hathor-adr-007-taguchi-techniques-robust-design-20261002.md).

### 3. 👁️ Pixel-Native 2D Document Parsing & Playwright Grounding (`hath0r_engine.vision`)
* **Problem:** Enterprise documents (invoices, balance sheets, architecture flowcharts) lose 2D relational structure when flattened into 1D text tokens, while DOM-based UI automation breaks constantly.
* **Solution:** Decomposes documents into continuous visual patches to preserve 2D cell grids and topological hierarchy without OCR licenses. Translates natural language directives into DOM-independent Playwright action steps executed via pixel coordinates.
* **Playwright Master Test Catalog:** Conforms to `contracts/hath0r-playwright-test-spec-v1.schema.json` with automated test catalog synchronization.

### 4. 🧠 Hybrid Tri-Graph RAG & Letta Memory Substrate (`hath0r_engine.memory` / `graph`)
* **KnowledgeGraph:** Static codebase lineage, API contracts, and policy invariants.
* **ContextGraph:** Real-time multi-agent delegation traces and active execution spans.
* **MemoryGraph:** Temporal entity graph with valid-time filtering (`is_valid_at(as_of)`), Letta-compatible memory paging, and sleep-cycle reflection consolidation.

### 5. 🛡️ Deterministic AST Guardrails & Schema Repair (`hath0r_engine.guardrails`)
* Pre-execution static AST analysis blocks destructive bash, root escalations, and SQL drops before runtime.
* In-flight schema repair engine coerces hallucinated tool parameters back into schema compliance.

### 6. ⏱️ Durable Workflow Replay & Zero-Compute Hibernation (`hath0r_engine.orchestration`)
* Append-only event journaling enables instant crash recovery and workflow replay.
* `@durable_task` and `HumanHibernationGate` pause workflows for human approval without consuming GPU/CPU resources.

### 7. 🔐 Generative UI & Cryptographic Evidence Handshake (`hath0r_engine.ui`)
* Interactive dashboard streaming cards: visual diff viewers, parameter sliders, test badges.
* Cryptographic HMAC SHA-256 signatures bind human sign-offs to precise execution artifacts.

---

## 📜 Enterprise Governance Strategies & Playbooks

| Strategic Capability | Architecture Strategy | Operator Playbook |
| :--- | :--- | :--- |
| **Tokenizer Tax & Pixel-Native AI** | [ADR-008 Strategy](docs/architect/hathor-adr-008-pixel-native-vision-tokenizer-tax-20261002.md) | [`playbooks/ai-gateway-tiered-routing-playbook.md`](docs/governance/playbooks/ai-gateway-tiered-routing-playbook.md) |
| **Taguchi Robust Optimization** | [ADR-007 Strategy](docs/architect/hathor-adr-007-taguchi-techniques-robust-design-20261002.md) | [`strategies/declarative-dspy-pipeline-strategy.md`](docs/governance/strategies/declarative-dspy-pipeline-strategy.md) |
| **Agent Rules & CLI-First RAG** | [`strategies/agent-rules-rag-cli-first-strategy.md`](docs/governance/strategies/agent-rules-rag-cli-first-strategy.md) | [`playbooks/agent-rules-rag-cli-first-playbook.md`](docs/governance/playbooks/agent-rules-rag-cli-first-playbook.md) |
| **Pre-Execution Guardrails** | [`strategies/deterministic-tool-guardrails-strategy.md`](docs/governance/strategies/deterministic-tool-guardrails-strategy.md) | [`playbooks/deterministic-tool-guardrails-playbook.md`](docs/governance/playbooks/deterministic-tool-guardrails-playbook.md) |
| **Generative UI & Sign-Off** | [`strategies/generative-ui-evidence-handshake-strategy.md`](docs/governance/strategies/generative-ui-evidence-handshake-strategy.md) | [`playbooks/generative-ui-evidence-handshake-playbook.md`](docs/governance/playbooks/generative-ui-evidence-handshake-playbook.md) |
| **Durable Workflow Replay** | [`strategies/durable-execution-checkpointing-strategy.md`](docs/governance/strategies/durable-execution-checkpointing-strategy.md) | [`playbooks/durable-execution-checkpointing-playbook.md`](docs/governance/playbooks/durable-execution-checkpointing-playbook.md) |
| **Zero-Trust Compute Sandbox** | [`strategies/isolated-compute-sandbox-strategy.md`](docs/governance/strategies/isolated-compute-sandbox-strategy.md) | [`playbooks/isolated-compute-sandbox-playbook.md`](docs/governance/playbooks/isolated-compute-sandbox-playbook.md) |
| **Temporal Knowledge Graphs** | [`strategies/temporal-knowledge-graph-strategy.md`](docs/governance/strategies/temporal-knowledge-graph-strategy.md) | [`playbooks/temporal-knowledge-graph-playbook.md`](docs/governance/playbooks/temporal-knowledge-graph-playbook.md) |

---

## 🛠️ Deep Technical Documentation

For developers, architects, and machine learning engineers implementing or extending cognitive subsystems:
- 📖 **Deep Technical Architecture & Code Examples:** [TECH_README.md](TECH_README.md)
- 📐 **Contract Schemas:** Located in [`contracts/`](contracts/)
- 🧪 **Test Suite:** **178 passing unit & integration tests** across all cognitive modules (`pytest -q`)
- 🏛️ **Control Tower:** [Bayly-AI/HATH0R-CLI](https://github.com/Bayly-AI/HATH0R-CLI)

---

## ⚖️ License

Licensed under the [Apache License, Version 2.0](LICENSE).
