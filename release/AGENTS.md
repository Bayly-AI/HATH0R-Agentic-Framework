---
id: release-subsystem
type: subsystem
title: Release Distribution & Agent Provisioning Subsystem
depends_on: [contracts-subsystem, cfg-subsystem]
governed_by: [CR-CLI-ENTRY-001, CR-AGENTGRAPH-001, CR-MEMORY-COMPOUND-001, CR-IAC-001, cr-branch-gov-001]
---
# Release Subsystem — AGENTS Context

> **Subsystem Role:** Authoritative home for production release distributions, standalone executable binaries, hardened container manifests, and the self-contained prompt ticket sequence (`release/prompts/`) required for an agent or operator to build out the complete Hath0r Infrastructure (CLI, MCP, ATC) and hydrate canonical seed knowledge from scratch.

---

## 🏛️ 1. Subsystem Architecture & Invariants

1. **Target is Release, Not Code**:
   This subsystem publishes and stages **production release artifacts** (standalone compiled binaries, Python wheels, npm distributions, container manifests, and edge proxy gateways) — **not raw uncompiled source checkouts**.

2. **Tripartite Infrastructure Scope**:
   The release coordinates all three primary nodes of the Hath0r ecosystem:
   - **Hath0r CLI**: Operator CLI, cognitive router, and AST guardrails (`hath0r`).
   - **Hath0r MCP**: Model Context Protocol server exposing knowledge, docs, and 42 tools on `http://127.0.0.1:38083`.
   - **Hath0r ATC**: Air Traffic Control (Control Tower, Redis session state, and Nginx ingress edge on `http://127.0.0.1:38000`).

3. **Topology Flexibility**:
   Supports both:
   - **3 Separate Repositories (RECOMMENDED)**: Decoupled release management across CLI, MCP, and ATC.
   - **1 Unified Repository (Monorepo)**: Consolidated repository housing `cli/`, `mcp/`, and `atc/` as subdirectories.

4. **Self-Contained Knowledge Portability**:
   The [`release/prompts/`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/release/prompts/) directory is completely self-contained. It houses the basic set of canonical knowledge, contracts, schemas, operational runbooks, and tool catalogs in [`release/prompts/knowledge/`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/release/prompts/knowledge/). An operator possessing **only** this folder can stand up the entire infrastructure.

---

## 🛠️ 2. Subsystem Layout & Tooling

The `release/` directory is strictly curated to hold **only** the following three entities:

```text
release/
├── AGENTS.md    # Subsystem agent rules, invariants, and governance context
├── install.sh   # Prompt-guided walkthrough installer with Dependency Approval Gate
└── prompts/     # Fully self-contained prompts, knowledge pack, and pre-compiled artifacts
```

- [`release/install.sh`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/release/install.sh): Interactive, ticket-by-ticket guided walkthrough installer using the prompt tickets in `release/prompts/`.
- [`release/prompts/`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/release/prompts/):
  - [`00-ORCHESTRATION-MASTER-TICKET.md`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/release/prompts/00-ORCHESTRATION-MASTER-TICKET.md): Master lead agent conductor prompt.
  - [`install.sh`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/release/prompts/install.sh): Self-contained prompts installer runnable directly from the prompts folder.
  - [`knowledge/`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/release/prompts/knowledge/): Complete basic set of knowledge, contracts, runbooks, and catalogs of all Hath0r CLI, MCP (42 tools), and ATC tools.
  - [`artifacts/`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/release/prompts/artifacts/): Pre-compiled native binaries, Python wheels, fileset tarballs, and Node packages.

---

## 📋 3. Agent Operating Rules & Constraints

1. **Start with the CLI (`CR-CLI-ENTRY-001`)**:
   Always verify the installed CLI binary (`hath0r --version`, `hath0r doctor`) and use it for operational validation.
2. **Zero-Prompt-Tax Retrieval (`CR-AGENTGRAPH-001`)**:
   Never dump full files or entire rulebooks into prompt context. Query targeted AgentGraph and MemoryGraph nodes.
3. **Container Security Standards (`CR-IAC-001`)**:
   Container images for MCP and ATC must run non-root (`UID 10001:GID 10001`), declare read-only root filesystems, drop capabilities, and communicate across `hath0r-net`.
4. **Mandatory Memory Compounding (`CR-MEMORY-COMPOUND-001`)**:
   Every build or installation run MUST record micro-entries (`hath0r memory session write`) and compound knowledge into `.hath0r/memory/graph.json` before announcing task completion.
5. **Release Checksum Integrity**:
   Verify cryptographic digests against `release/python/cli/CHECKSUMS.sha256` and produce an immutable `RELEASE_RECEIPT.json`.

---

## CR-TASK-EVAL-001 (Automatic Task Evaluation Before Announcing Complete — CRITICAL · CANONICAL)
- **Mandatory Pre-Announcement Task Evaluation Gate**: Every task MUST be evaluated across the 4-tier hybrid evaluation pipeline (Tier 1 Deterministic Rubrics, Tier 2 Trajectory & FinOps Efficiency, Tier 3 Adversarial & Diff Critics, Tier 4 Goal Alignment & Consensus) prior to announcing work as Complete.
- **Composite Reward Threshold**: Task completion requires `passed_gate: true` and composite reward score `R_task >= 0.80` persisted in `.hath0r/evals/latest.json` and compounded as an `eval:<task_id>` node in `.hath0r/memory/graph.json`.
- **How to Verify**: Run `hath0r evals run` and `hath0r evals verify` before announcing Complete (`EndOfTaskBot`, `TaskAnnouncerBot.announce_complete`, and `CleanReposWorkflowBot` enforce this gate automatically).
- **Not Complete Until Evaluated**: A missing, failing, or unverified task evaluation means the work is not Complete.
