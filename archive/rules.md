---
id: rule:subsystem-archive
type: rule_policy
title: "Archive Subsystem - Local Rules"
priority: 2
priority_name: SUBSYSTEM_RULE
target_scope: archive
restricted_actions: [import_archive_code, mutate_archive_file]
governs_roles: [developer, qa-engineer, architect]
---
# Archive Subsystem — Local Rules

> **Rule ID:** `rule:subsystem-archive`  
> **Subsystem Scope:** `archive/`  
> **Precedence Priority:** `2` (`SUBSYSTEM_RULE`)  

---

## Operational Constraints

1. **Read-Only Preservation:**
   - All files within `archive/` are preserved solely for historical provenance and auditing.
   - Modifying, mutating, or overwriting files in `archive/` is strictly forbidden.
2. **Zero Runtime Imports:**
   - Active runtime modules in `src/hath0r_engine/` and `lib/` MUST NOT import code or assets directly from `archive/`.
3. **Query Channel:**
   - Retrieve historical context through `hath0r kb search` or `hath0r memory search` rather than active imports.
