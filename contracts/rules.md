---
id: rule:subsystem-contracts
type: rule_policy
title: "Contracts Subsystem - Local Rules"
priority: 2
priority_name: SUBSYSTEM_RULE
target_scope: contracts
restricted_actions: [modify_contract_schema_without_semver]
governs_roles: [developer, architect, qa-engineer]
---
# Contracts Subsystem — Local Rules

> **Rule ID:** `rule:subsystem-contracts`  
> **Subsystem Scope:** `contracts/`  
> **Precedence Priority:** `2` (`SUBSYSTEM_RULE`)  

---

## Operational Constraints

1. **Schema Authority:**
   - All machine-consumed JSON schemas, exit code specs, and API payloads MUST be defined under `contracts/`.
2. **Schema Contract Validation:**
   - Run `hath0r contracts validate` to verify schema validity against Draft 2020-12 / Draft 07 specifications.
3. **Immutable Versioning:**
   - Modifying pre-existing schema files requires a formal SemVer major/minor version increment or new schema file creation (e.g., `hath0r-*-v2.schema.json`).
4. **Cross-Repo Sync:**
   - Shared contracts must be kept synchronized across `HATH0R-CLI` and `hath0r-framework` using `hath0r contracts sync`.
