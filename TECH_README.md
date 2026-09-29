# HATHOR Framework — Technical Architecture & Engine Reference

> Language-agnostic agentic application framework and cognitive substrate for the Enterprise Agentic Platform.

---

## 🛠️ Developers Working on HATH0R-CLI & Core Framework

This document contains deep technical specifications, Tri-Graph substrate data structures, repository layouts, binary build pipelines, and governance systems for developers building or extending `hath0r`, `hath0r-framework`, and the underlying engine.

> **Looking to install and use Hath0r in your own projects?**  
> You only need the **HATH0R CLI** (`hath0r`). Download pre-compiled standalone binaries in [`release/`](release/) or see the [CLI Quick Start](#-quick-start-operators--users) below.

---

## 🚀 Quick Start: Operators & Users

The Hath0r CLI is distributed as a zero-dependency standalone binary for macOS, Linux, and Windows:

```sh
# Option 1: Direct Standalone Binary (Zero Setup Required)
chmod +x release/hath0r-darwin-arm64
./release/hath0r-darwin-arm64 doctor
./release/hath0r-darwin-arm64 init

# Option 2: Python / pipx package
pipx install hath0r-cli
hath0r doctor
hath0r init
```

---

## 🏗️ Architecture at a Glance

```text
Operator / Human Developer / Autonomous Agent
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│                   HATH0R Operator CLI                  │
├────────────────────────────────────────────────────────┤
│ • Execution Engine (`step_runner`, `factories`)        │
│ • Elevation of Authority (`guest` → `sovereign`)       │
│ • Credential Mediation (`AWS Secrets` → `~/.env`)      │
│ • Voice Streaming Interface (Ambient Daemon)           │
└────────────────────┬───────────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│              Tri-Graph Cognitive Substrate             │
├────────────────────┬───────────────────┬───────────────┤
│   KnowledgeGraph   │   ContextGraph    │  MemoryGraph  │
│   (Static Truth)   │ (Dynamic Runtime) │(Working State)│
└────────────────────┴───────────────────┴───────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│               Universal Project Layout                 │
├────────────────────────────────────────────────────────┤
│ `CFG/`  `BIN/`  `LIB/`  `SRC/`  `DIST/`  `tests/`      │
│ `.hath0r/` (State, Caches, Working Memory, Lineage)   │
└────────────────────────────────────────────────────────┘
```

---

## 📦 Standalone CLI Binary Pipeline & Distribution

The CLI operator is packaged with PyInstaller into single-file drop-in executables for all major operating systems:

```text
hathor-cli/ (Source)
     │
     ├── packaging/binary/hath0r-entry.py
     └── scripts/build_binary.py
              │
              ▼ (PyInstaller --onefile)
hath0r-framework/release/
     ├── hath0r-darwin-arm64       (macOS Apple Silicon)
     ├── hath0r-darwin-x86_64      (macOS Intel)
     ├── hath0r-linux-x86_64       (Linux x86_64)
     ├── hath0r-linux-arm64        (Linux ARM64)
     ├── hath0r-windows-x64.cmd    (Windows x64)
     ├── CHECKSUMS.sha256          (Cryptographic Signatures)
     └── README.md                 (Execution Guide)
```

To build and package standalone binaries from source:
```bash
python3 scripts/build_binary.py --out dist/binary
```

---

## 🧠 Tri-Graph Cognitive Substrate Deep Dive

HATHOR replaces flat prompt buffers with an interconnected, three-tier cognitive graph model:

```text
                                Tri-Graph Substrate
                                         │
        ┌────────────────────────────────┼────────────────────────────────┐
        ▼                                ▼                                ▼
1. KnowledgeGraph (KG)           2. ContextGraph (CG)             3. MemoryGraph (MG)
   • Static Codebase Lineage        • Dynamic Agent Topologies       • Semantic Working Memory
   • Markdown & Contract Parsing    • JEV Guard Action Audit         • Rules, Decisions & Playbooks
   • .hath0r/state/cache/           • .hath0r/state/context/         • .hath0r/memory/graph.json
```

### 1. KnowledgeGraph (KG — Static Layer)
- **Engine Module:** [`lib/graph/knowledge_graph.py`](lib/graph/knowledge_graph.py)
- **Role:** Maps static AST code structures, markdown governance docs with YAML frontmatter, and schema contracts into relational tables.
- **Relational Edges:** `depends_on`, `implements`, `governed_by`, `references`.
- **Contract Schema:** [`contracts/schemas/knowledge-graph-schema.json`](contracts/schemas/knowledge-graph-schema.json).

### 2. ContextGraph (CG — Dynamic Runtime Layer)
- **Engine Module:** [`lib/context/context_graph.py`](lib/context/context_graph.py)
- **Role:** Tracks real-time multi-agent execution hierarchies, subagent delegations, and task lifecycles during active turns.
- **JEV Guard Audit:** Attaches `guarded_by` relationships to all mutating tool executions, ensuring zero-trust verification.
- **Dynamic Pruning:** Subagents receive tailored context subgraphs instead of full transcript dumps.
- **Contract Schema:** [`contracts/schemas/context-graph-schema.json`](contracts/schemas/context-graph-schema.json).

### 3. MemoryGraph (MG — Semantic Working Memory Layer)
- **Engine Module:** [`lib/memory/memory_graph.py`](lib/memory/memory_graph.py)
- **Role:** Persists episodic memory, architectural decisions, and operational rules in `.hath0r/memory/graph.json`.
- **Relational Edge Semantics:**
  - `ENFORCES` (e.g. *Branch Policy* $\rightarrow$ *Issue First Enforcement*)
  - `REQUIRES` (e.g. *Onboarding Factory* $\rightarrow$ *Layout Validation*)
  - `DERIVES_FROM` / `SUPERSEDES` (capturing evolving architectural decisions)
  - `RESOLVES` / `RELATES_TO`
- **Contract Schema:** [`contracts/schemas/memory-graph-schema.json`](contracts/schemas/memory-graph-schema.json).

---

## 📂 Universal Project Layout & Subsystem Governance

The HATHOR layout is strictly language-agnostic and organized for autonomous agent navigation:

| Directory | Subsystem Role | Governance Pointer |
| :--- | :--- | :--- |
| **`cfg/`** | Configuration files, factory workflows, docker setups | `cfg/AGENTS.md` |
| **`bin/`** | Executables, hooks, and member bootstrap scripts | `bin/hath0r-bootstrap.sh` |
| **`lib/`** | Graph engines, cognitive substrate, shared libraries | `lib/AGENTS.md` |
| **`contracts/`** | Formal JSON schemas and protocol specifications | `contracts/AGENTS.md` |
| **`release/`** | Standalone pre-compiled CLI executables and checksums | `release/README.md` |
| **`tests/`** | Unit, integration, and contract verification test harnesses | `tests/AGENTS.md` |
| **`docs/`** | Canonical OpenSource documentation corpus | `docs/AGENTS.md` |
| **`.hath0r/`** | Hidden agent state, caches, working memory, and lineage | Local `.hath0r/` |

---

## 🔒 Security & Zero-Trust Credential Resolution

The CLI resolves credentials through a fixed four-tier elevation order:
1. **AWS Secrets Manager** (Primary enterprise source when configured).
2. **User Root Credentials File** (`~/.credentials/<service>/.env`).
3. **Project Scoped Environment File** (`.env`).
4. **Sibling / Workspace Environment Files** (if explicitly permitted).

**Zero Leakage Guarantee:** Credentials are never printed in transcripts, passed into AST graphs, or committed to Git.

---

## 🧪 Testing & Verification

Run the framework test harness across all graph engines and schema validators:

```bash
pytest tests/ -v
```

All 35+ test cases validate `MemoryGraph` serialization, `KnowledgeGraph` relational indexing, `ContextGraph` delegation trees, and contract schema compliance.

---

## ⚖️ License

Licensed under the [Apache License, Version 2.0](LICENSE).
