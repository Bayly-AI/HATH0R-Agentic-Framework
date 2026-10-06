---
id: rule:cr-hath0r-init-001
type: rule_policy
title: "CR-HATH0R-INIT-001: Repository Initialization Entry Gate"
priority: 4
priority_name: ORG_INVARIANT
target_scope: root
restricted_actions: []
governs_roles: [developer, architect]
---
# CR-HATH0R-INIT-001: Repository Initialization Entry Gate (CRITICAL — Org-Wide)

> **Rule ID:** `CR-HATH0R-INIT-001`  
> **Status:** RATIFIED & MANDATORY ENTRY GATE  
> **Applies to:** All Repositories being initialized or re-initialized with HATH0R.  
> **Effective Date:** 2026-09-19  

---

## 1. Main Entry Statement (CRITICAL ENTRY GATE)

> **Before initializing (or re-initializing) ANY repository with Hath0r, agents MUST locate and satisfy both the canonical Hath0r setup playbook AND a same-technology runbook.**
>
> Layout scaffolding or applying file structures without an established setup playbook and technology-matched runbook is **STRICTLY FORBIDDEN**.

---

## 2. Core Directives

1. **Setup Playbook Gate:**
   - Locate and follow the canonical setup playbook:  
     `docs/developers/hathor-playbook-001-repo-init-setup-20260919.md`
   - If missing or incomplete, create or update the playbook first before proceeding.
2. **Same-Technology Runbook Gate:**
   - Locate a runbook for an individual repo with the same technology stack (e.g. React+Vite UXP, Python CLI, FastMCP server).
   - Prefer sibling product `docs/runbook.md` in that tech family. If none exists, create a tech-appropriate runbook in the target repository.
3. **Execution Gate:**
   - Only after (1) and (2) are satisfied: apply layout, `.hath0r/`, `cfg/`, contract pins, `AGENTS.md` identity, and `./bin/hath0r-bootstrap.sh`.

---

## 3. Enforcement & Verification

- **Init Bot:** `hath0r init` verifies playbook and runbook prerequisites before executing scaffolding routines.
