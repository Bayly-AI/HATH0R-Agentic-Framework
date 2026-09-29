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
> `pipx install hath0r-cli` (or `pip install hath0r-cli`)

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

### 3. Run Autonomous Agent Workflows
```sh
hath0r run --workflow repo-onboarding
hath0r status
```

---

## 🌟 Why Enterprises Choose HATHOR

Traditional AI coding assistants rely on ephemeral chat windows, flat-file dumps, and unverified prompt injections. HATHOR establishes a **resilient, cryptographically governed runtime** for autonomous engineering teams:

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
│ • Cryptographic JEV Policy Enforcement                                 │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      Tri-Graph Cognitive Substrate                     │
├───────────────────┬────────────────────────────┬───────────────────────┤
│  KnowledgeGraph   │        ContextGraph        │      MemoryGraph      │
│  (Static Lineage) │     (Dynamic Session)      │   (Working Memory)    │
└───────────────────┴────────────────────────────┴───────────────────────┘
```

### 💎 Key Business & Architectural Advantages

1. 🧠 **Tri-Graph Cognitive Substrate (Zero Tribal Memory Loss):**
   - **KnowledgeGraph (KG):** Compiles code ASTs, API contracts, and governance policies into relational graph lineage (`depends_on`, `implements`, `governed_by`).
   - **ContextGraph (CG):** Dynamically prunes context windows and visualizes live subagent delegation trees with zero context window bloat.
   - **MemoryGraph (MG):** Persists semantic rules, decisions, and failure learnings across developer turns with causal `ENFORCES` / `RESOLVES` relations.

2. 🛡️ **Zero-Trust Security & JEV Guard:**
   - Every mutating action (file write, git commit, shell execution) is evaluated against Justified Execution Verification (JEV) policies before touching your filesystem.

3. 🚀 **Universal & Language Agnostic:**
   - Works immediately out of the box with any stack: React/Vite, Next.js, Python FastAPI/Django, Go, Rust, Java, or C#.

4. 🎙️ **Streaming Voice & Ambient CLI:**
   - Low-latency conversational audio interface allows engineers to interact verbally with their agentic workspace in real time.

5. ⚡ **Declarative Multi-Bot Factories:**
   - Pre-configured micro-bot pipelines automate repository onboarding, PR generation, CI testing, and release artifact packaging.

---

## 🛠️ For Framework & Engine Developers

If you are developing core cognitive algorithms, contract schemas, or CLI extensions:

- 📖 **Deep Technical Architecture:** See [TECH_README.md](TECH_README.md) for data schemas, graph engines, and subsystem specifications.
- 📐 **Contract Schemas:** Located in [`contracts/schemas/`](contracts/schemas/).
- 🧪 **Unit Tests:** Run `pytest tests/ -v` (35+ unit tests covering graph compilation and persistence).
- 🏛️ **Control Tower:** Located in [Bayly-AI/HATH0R-CLI](https://github.com/Bayly-AI/HATH0R-CLI).

---

## 📜 Documentation Index

- [Standalone Releases & Binaries (release/README.md)](release/README.md)
- [Technical Developer Reference (TECH_README.md)](TECH_README.md)
- [Control Tower Repository (HATH0R-CLI)](https://github.com/Bayly-AI/HATH0R-CLI)
- [Governance Rules & Promotion Standards](docs/governance/)
- [Canonical Documentation Corpus](docs/README.md)

---

## ⚖️ License

Licensed under the [Apache License, Version 2.0](LICENSE).
