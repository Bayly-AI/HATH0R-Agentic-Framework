# Hath0r Infrastructure Release Prompts & Self-Contained Knowledge Pack

This directory is a **completely self-contained distribution package** designed for autonomous AI agents and DevOps operators to build and deploy the complete **Hath0r Infrastructure Release** (CLI, MCP, ATC) from scratch.

> **Zero External File Dependency**: An Operator can take **only this `release/prompts` folder** to any environment, provide either 1 or 3 repository links, and fully stand up Hath0r, Hath0r MCP, and Hath0r ATC, complete with the basic set of canonical knowledge and tool definitions.

---

## 🏛️ Tripartite Infrastructure Architecture

The Hath0r Infrastructure consists of three core components:

| Component | Role | Default Port / Target | Technology |
| :--- | :--- | :--- | :--- |
| **Hath0r CLI** | Operator CLI, cognitive engine orchestrator, and entry gate | System PATH (`hath0r`) | Standalone native binary / Python Wheel / Node CLI |
| **Hath0r MCP** | Model Context Protocol server (Knowledgebase, tools, docs, runbooks) | `http://127.0.0.1:38083` | FastAPI / Python MCP container on `hath0r-net` |
| **Hath0r ATC** | Air Traffic Control (Control Tower, session state, edge proxy, observation) | `http://127.0.0.1:38000` | Nginx 1.27 (`Hath0r-Edge`) + Redis 7 (`Hath0r-Sessions`) |

All containerized services communicate over an isolated Docker bridge network: **`hath0r-net`**.

---

## 📚 Bundled Knowledge & Tool Pack (`knowledge/`)

Embedded directly inside this folder is the foundational knowledge pack required for agents and operators to understand and wield all Hath0r tools:

- **[`knowledge/tools/`](knowledge/tools/)**:
  - [`HATHOR-CLI-TOOLS-CATALOG.md`](knowledge/tools/HATHOR-CLI-TOOLS-CATALOG.md): Commands for workspace init, memory sessions, AgentGraph, and IaC salting.
  - [`HATHOR-MCP-TOOLS-CATALOG.md`](knowledge/tools/HATHOR-MCP-TOOLS-CATALOG.md): Complete catalog of **all 42 MCP tools** across semantic search, docs retrieval, and runbook prompt synthesis.
  - [`HATHOR-ATC-TOOLS-CATALOG.md`](knowledge/tools/HATHOR-ATC-TOOLS-CATALOG.md): Control Tower ingress routing, Redis session coordination, and OpenTelemetry spans.
- **[`knowledge/contracts/`](knowledge/contracts/)**: JSON schemas defining CLI responses, MCP servers, and AgentGraph structures.
- **[`knowledge/canonical/`](knowledge/canonical/)**:
  - `architecture/`: Ecosystem overview, quad-graph substrate, and ATC design.
  - `rules/`: Core invariants (`CR-CLI-ENTRY-001`, `CR-AGENTGRAPH-001`, `CR-MEMORY-COMPOUND-001`, `CR-IAC-001`).
  - `runbooks/`: Operational runbooks for bootstrap, MCP operations, and ATC edge proxy.
  - `strategies/`: $CIC^3DCT$ Continuous Calibration and Zero-Prompt-Tax Retrieval.

- **[`artifacts/`](artifacts/)**:
  - `python/cli/`: Pre-compiled standalone native binaries (`hath0r-darwin-arm64`, `hath0r-darwin-x86_64`, `hath0r-linux-x86_64`, Windows cmd), pip wheel (`hath0r_cli-*.whl`), and fileset template archive (`hath0r-fileset-*.tar.gz`).
  - `javascript/node/`: Node package tarball (`hath0r-node-*.tgz`) and TypeScript CLI source distributions.
  - `previous/`: Archived historical release bundles and migration notes.

---

## 🔀 Repository Topology Options

The agent installer and prompt sequence support two deployment topologies. The operator can supply either 1 or 3 repository links:

### Option 1: 3 Separate Repositories (RECOMMENDED)
Maximizes modularity, decoupled release trains, and strict separation of concerns:
1. **CLI Repo**: `https://github.com/Bayly-AI/HATH0R-CLI.git` (or local path)
2. **MCP Repo**: `https://github.com/Bayly-AI/HATH0R-MCP.git` (or local path)
3. **ATC Repo**: `https://github.com/Bayly-AI/HATH0R-ATC.git` (or local path)

### Option 2: 1 Unified Repository (Monorepo)
Consolidates infrastructure within a single repository containing designated subdirectories:
- **Unified Repo**: `https://github.com/Bayly-AI/hath0r.git` (or local path)
  - `cli/` (CLI engine & packaging)
  - `mcp/` (MCP knowledge server & tools)
  - `atc/` (Control Tower compose, edge proxy, observation)

---

## 🎫 Ticket Series Index

Execute the tickets in sequence. For automated end-to-end execution, dispatch the **[Master Orchestrator Prompt](00-ORCHESTRATION-MASTER-TICKET.md)**.

| Ticket | Title | Focus Area | Artifacts Produced |
| :--- | :--- | :--- | :--- |
| **[00](00-ORCHESTRATION-MASTER-TICKET.md)** | **Master Orchestrator Ticket** | End-to-end agent workflow conductor | Full pipeline execution & status reporting |
| **[01](TICKET-01-TOPOLOGY-AND-ENVIRONMENT-PREFLIGHT.md)** | **Topology & Preflight** | Operator intake & prerequisite validation | `preflight-report.json`, `hath0r-net` bridge |
| **[02](TICKET-02-CLI-RELEASE-PACKAGING-AND-INSTALL.md)** | **CLI Release Packaging** | Native binary / wheel packaging & PATH install | `hath0r` executable, CLI response verification |
| **[03](TICKET-03-MCP-SERVER-CONTAINERIZATION-AND-DEPLOYMENT.md)** | **MCP Server Deployment** | Hardened container build & tool registration | `Hath0r-MCP` container, `cfg/mcp.servers.json` |
| **[04](TICKET-04-ATC-CONTROL-TOWER-AND-OBSERVATION-FABRIC.md)** | **ATC Control Tower** | Edge gateway, Redis sessions & OTel observability | `Hath0r-Edge`, `Hath0r-Sessions`, reverse proxy routes |
| **[05](TICKET-05-AGENTGRAPH-AND-MEMORY-SUBSTRATE-INTEGRATION.md)** | **AgentGraph & Memory Substrate** | Letta memory paging, SHA-256 CAS & rules DAG | `.hath0r/memory/graph.json`, `.hath0r/agentgraph/` |
| **[06](TICKET-06-SEED-KNOWLEDGE-AND-TOOL-CATALOG-TRANSFER.md)** | **Seed Knowledge & Tool Transfer** | Hydrates basic set of knowledge & tools | MCP knowledgebase sync, memory seed concepts |
| **[07](TICKET-07-END-TO-END-ACCEPTANCE-AND-RELEASE-ATTESTATION.md)** | **Acceptance & Attestation** | Smoke test suite & cryptographic receipt | `RELEASE_RECEIPT.json`, `CHECKSUMS.sha256` |

---

## ⚡ Self-Contained Quick Start

Run directly from within this directory:

```bash
# Interactive mode:
./install.sh

# Headless agent execution with 3 repos (Recommended):
./install.sh --non-interactive --topology 3-repos \
  --cli-repo https://github.com/Bayly-AI/HATH0R-CLI.git \
  --mcp-repo https://github.com/Bayly-AI/HATH0R-MCP.git \
  --atc-repo https://github.com/Bayly-AI/HATH0R-ATC.git

# Headless agent execution with 1 monorepo:
./install.sh --non-interactive --topology 1-repo \
  --unified-repo https://github.com/Bayly-AI/hath0r.git
```
