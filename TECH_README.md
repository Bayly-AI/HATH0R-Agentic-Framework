# HATHOR Framework — Technical Architecture & Developer Reference

> Language-agnostic agentic application framework and cognitive substrate for the Enterprise Agentic Platform.

---

## 🛠️ Developers Working on HATH0R-CLI & Core Framework

This document contains deep technical specifications, Tri-Graph substrate data structures, repository layouts, and governance systems for developers building or contributing to `hath0r`, `hath0r-framework`, and the underlying engine.

> **Looking to install and use Hath0r in your own projects?**  
> You only need the **HATH0R CLI** (`hath0r-cli`). See the [CLI Quick Start](#-quick-start-operators--users) below or visit [Bayly-AI/HATH0R-CLI](https://github.com/Bayly-AI/HATH0R-CLI).

---

## 🚀 Quick Start: Operators & Users

To use the HATHOR platform on your machine and align any repository with the framework, install the CLI:

### 1. Install `hath0r`
```sh
pipx install hath0r-cli
# or: python3 -m pip install hath0r-cli
```

### 2. Verify Installation
```sh
hath0r --version
hath0r doctor
```

### 3. Initialize & Align Any Repository
Navigate to any repository (Python, Node/TS, Go, Rust, polyglot) and run:
```sh
cd /path/to/my-repo
hath0r init
```
This automatically scaffolds governance (`AGENTS.md`), refactors documentation, provisions test harnesses, and compiles the **Tri-Graph Cognitive Substrate**.

---

## Why HATHOR

Most agent tooling assumes a chat session and a pile of files. HATHOR assumes a **durable operating environment**:

- A standard project shape every agent can navigate.
- A single CLI as the agent’s first interface.
- Layered knowledge (project → machine → organization → public).
- Provenance, freshness, and governance on what agents read and write.
- Credential mediation that never dumps secrets into source control.

---

## Architecture at a Glance

```text
Agent ──► CLI ──► Universal Project Layout
              │
              ├─ Knowledge Infrastructure (MCP / CLI / Project)
              ├─ Governance & Rules
              └─ Security & Credentials
```

### Agent
The agent is the worker. It does not own the project layout or secret store. It discovers authority, knowledge, and tools through HATHOR’s interfaces.

### CLI
The CLI is a **globally installed** application on every machine that uses the Enterprise Agentic Platform. It is the first thing agents consent to interface with.

It provides:
- Commands, models, research, and context access.
- Elevation of authority across trust tiers: **guest → elevated → sovereign**.
- Mediation of credentials and knowledge lookups.
- A stable boundary between agent intent and host capabilities.

### Universal Project Layout
The project layout is code- and framework-agnostic. It lets file agents (and humans) orient quickly **before** building out any application.

| Path | Role |
| --- | --- |
| **CFG** | All project configuration files that aren’t required at the root |
| **BIN** | Executables and scripts, organized by folder, allowing script organization at the project level. Standard wrapper scripts live here. |
| **LIB** | Static assets, files, images, etc. Reports, artifacts, and documents that are not docs live here. |
| **docker** | Docker files kept alongside to keep deployment files out of the main repo root noise. |
| **SRC** | Application source. All code writes happen here prior to building and testing. |
| **DIST** | Build output. Transpiled/compiled code placed here for testing and packaging. |
| **Test** | Unit, pre- and post-deploy tests, test cases, and testing scripts. |
| **docs** | Canonical human- and agent-facing documentation. |

#### Hidden Agent Configuration (`.hath0r/`)
All agent state, caches, working memory, and lineage graphs consolidate strictly under `.hath0r/`.
- Every significant folder contains a localized `AGENTS.md` covering that folder and its constraints.
- Avoids source clutter while remaining instantly discoverable for agents.

---

## Tri-Graph Cognitive Substrate

HATHOR features a unified **Tri-Graph Cognitive Substrate** providing AST lineage, dynamic agent topology, and semantic working memory:

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
- **Files-as-truth**: Markdown records with YAML frontmatter (`.hath0r/knowledgebase/**`, `docs/**`, `contracts/**`) remain canonical.
- **Compiled Engine**: Relational lineage connecting `depends_on`, `implements`, `governed_by`, and `references` relationships across policies, tools, and procedures.
- **Contract Schema**: `contracts/schemas/knowledge-graph-schema.json`.

### 2. ContextGraph (CG — Dynamic Runtime Layer)
- **Dynamic Session Topologies**: In-memory and session-cached graph capturing parent-child subagent delegations, task trees, and active context slices.
- **JEV Guard Audit Trails**: Every mutating tool execution automatically logs a `guarded_by` validation edge connecting the action to its Justified Execution Verification (JEV) policy check.
- **Context Pruning**: Provides targeted subgraphs for subagents instead of token-heavy flat context dumps.
- **Contract Schema**: `contracts/schemas/context-graph-schema.json`.

### 3. MemoryGraph (MG — Semantic Working Memory Layer)
- **Semantic Topic Network**: Structured memory space (`.hath0r/memory/graph.json`) organizing rules, architectural concepts, episodic learnings, and decision records.
- **Relational Memory Retrieval**: Enables context-aware memory recall and neighborhood extraction across `ENFORCES`, `REQUIRES`, `DERIVES_FROM`, and `RELATES_TO` edge topologies.
- **Contract Schema**: `contracts/schemas/memory-graph-schema.json`.

---

## Knowledge Hierarchy & Search Order

```text
Project  →  Machine  →  Organization (MCP)  →  Public
```

If a higher-priority tier answers the query, lower tiers are not required. Missing tiers **degrade gracefully**.

| Level | Surface | Purpose |
| --- | --- | --- |
| **Project** | Project knowledge / Tri-Graph | Authoritative project truth |
| **Machine** | CLI knowledge | Local library standard to the host machine |
| **Organization** | MCP server | Shared organization knowledge accessible via MCP |
| **Public** | Web / Search | Lowest trust, requires explicit citation and scrutiny |

---

## Security and Credentials

The CLI mediates credential resolution in a fixed priority order:
1. **AWS Secrets Manager** — first priority when available.
2. **User root credentials file** — if Secrets Manager is not available (`~/.credentials/<service>/.env`).
3. **Project repo `.env` file** — if the secret is scoped locally.
4. **Sibling repos’ `.env` files** — nearby project envs if configured/allowed.

Principles:
- Secrets never touch `SRC` or chat transcripts.
- Agents request capabilities through the CLI; they do not scrape raw disk files for API keys.
- Missing credentials trigger guided onboarding rather than silent crashes.

---

## Design Principles

1. **Language agnostic** — layout and contracts are not tied to one runtime.
2. **Agent-first navigation** — every important folder explains itself (`AGENTS.md`).
3. **CLI as control plane** — one elevation and mediation path.
4. **Local context wins** — project truth beats generic model memory.
5. **Provenance over vibes** — cite, timestamp, and mark staleness.
6. **Degrade, don’t die** — missing MCP/org/machine services still allow useful work.
7. **Secure by mediation** — credentials flow through policy, not copy-paste.

---

## License

Licensed under the [Apache License, Version 2.0](LICENSE).
