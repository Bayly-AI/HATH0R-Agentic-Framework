---
id: rule:subsystem-lib
type: rule_policy
title: "Library Subsystem - Local Rules"
priority: 2
priority_name: SUBSYSTEM_RULE
target_scope: lib
restricted_actions: [introduce_engine_circular_dependencies]
governs_roles: [developer, architect]
---
# Library Subsystem — Local Rules

> **Rule ID:** `rule:subsystem-lib`  
> **Subsystem Scope:** `lib/`  
> **Precedence Priority:** `2` (`SUBSYSTEM_RULE`)  

---

## Operational Constraints

1. **Engine Boundary Isolation:**
   - Package helpers and utilities in `lib/` must remain decoupled from specific runtime UI frameworks.
2. **Zero Circular Dependencies:**
   - Modules in `lib/` MUST NOT introduce circular imports with `src/hath0r_engine/`.
3. **Type Annotation Coverage:**
   - Public classes and functions in `lib/` must include complete Python type hints (`__future__.annotations`).
