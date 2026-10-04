---
id: rule:cr-kb-tower-001
type: rule_policy
title: "CR-KB-TOWER-001: Canonical Knowledgebase & Control Tower Routing"
priority: 3
priority_name: REPO_STANDARD
target_scope: root
restricted_actions: []
governs_roles: [developer, architect, researcher]
---
# CR-KB-TOWER-001: Canonical Knowledgebase & Control Tower Routing (CRITICAL)

> **Rule ID:** `CR-KB-TOWER-001`  
> **Status:** RATIFIED & MANDATORY REPO STANDARD  
> **Applies to:** All Knowledgebase, Search, and RAG operations across the OpenSource Suite.  
> **Effective Date:** 2026-09-30  

---

## 1. Main Entry Statement

> **Local knowledgebase operations MUST point to the OpenSource group hub (`hath0r kb path`), with HATH0R-CLI as the suite control tower.**
>
> Member repository `.hath0r/knowledgebase` directories are stubs/pointers to the group hub. Treating private product trees as canonical OpenSource sources is forbidden.

---

## 2. Core Directives

1. **Group Hub Pointer:**
   - Resolve knowledgebase path dynamically via `hath0r kb path` (`/Users/raybayly/Development/OpenSource/.hath0r/knowledgebase`).
2. **Control Tower Orientation:**
   - Control tower features and suite-wide CLI commands live in `HATH0R-CLI` (`Bayly-AI/HATH0R-CLI`).
3. **Canonical Documentation Corpus:**
   - `docs/` in `hath0r` (`HATH0R-Agentic-Framework`) represents the canonical OpenSource documentation corpus.

---

## 3. Enforcement & Verification

- **Doctor Verification:** `hath0r doctor` checks knowledgebase hub availability and path resolution.
- **KB Sync:** `hath0r kb index` synchronizes member docs into the group SQLite FTS5 index.
