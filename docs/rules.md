---
id: rule:subsystem-docs
type: rule_policy
title: "Documentation Subsystem - Local Rules"
priority: 2
priority_name: SUBSYSTEM_RULE
target_scope: docs
restricted_actions: [bypass_hexad_standard]
governs_roles: [developer, architect, researcher]
---
# Documentation Subsystem — Local Rules

> **Rule ID:** `rule:subsystem-docs`  
> **Subsystem Scope:** `docs/`  
> **Precedence Priority:** `2` (`SUBSYSTEM_RULE`)  

---

## Operational Constraints

1. **Hexad Artifact Standard:**
   - Feature packages must conform to the governance artifact hexad (`Strategy`, `Procedure`, `Playbook`, `Runbook`, `Workflow`, `Bot Spec`) as defined in `docs/governance/workflow-documentation-standard.md`.
2. **Canonical OpenSource Corpus:**
   - `docs/` in `hath0r-framework` is the authoritative documentation corpus for the OpenSource project.
3. **MCP Publishing:**
   - Governance docs must be published to group MCP via `hath0r docs share`.
