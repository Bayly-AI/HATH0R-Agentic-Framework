---
id: rule:cr-hath0r-root-001
type: rule_policy
title: "CR-HATH0R-ROOT-001: Framework Hidden Root Scoping"
priority: 4
priority_name: ORG_INVARIANT
target_scope: root
restricted_actions: []
governs_roles: [developer, architect, qa-engineer]
---
# CR-HATH0R-ROOT-001: Framework Hidden Root Scoping (CRITICAL — Org-Wide)

> **Rule ID:** `CR-HATH0R-ROOT-001`  
> **Status:** RATIFIED & MANDATORY INVARIANT  
> **Applies to:** All Repositories, Tooling, Bots, and Workflows in the HATH0R OpenSource & Enterprise Ecosystem.  
> **Effective Date:** 2026-09-30  

---

## 1. Main Entry Statement (CRITICAL INVARIANT)

> **All framework-created, modified, or saved project metadata MUST reside EXCLUSIVELY under `.hath0r/`.**
>
> The creation or usage of legacy, unapproved metadata directories (such as `.ai/`, `.customerSystem/`, `.infraOS/`, or root scattered metadata) is **STRICTLY FORBIDDEN**.

---

## 2. Standard Metadata Layout

All HATH0R metadata paths must conform to the canonical `.hath0r/` directory structure:

- `.hath0r/agentgraph/` — AgentGraph snapshot, topology, and SQLite graph database.
- `.hath0r/context/` — Hyper context state, session spans, and active subagent tracking.
- `.hath0r/knowledgebase` — Group knowledgebase pointer or local stub.
- `.hath0r/finops/` — Token telemetry ledger (`token_telemetry.jsonl`) and cost tracking.
- `.hath0r/cache/` — SQLite FTS5 index caches and local vector embeddings.

---

## 3. Enforcement & Verification

- **Repository Hygiene Audit:** `hath0r repo audit` scans workspace roots for unapproved hidden directories.
- **Bootstrap Verification:** `./bin/hath0r-bootstrap.sh` verifies that `.hath0r/` exists and is properly configured in `.gitignore`.
