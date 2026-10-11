---
id: rule:subsystem-cfg
type: rule_policy
title: "Configuration Subsystem - Local Rules"
priority: 2
priority_name: SUBSYSTEM_RULE
target_scope: cfg
restricted_actions: [store_plain_text_secrets]
governs_roles: [developer, architect, qa-engineer]
---
# Configuration Subsystem — Local Rules

> **Rule ID:** `rule:subsystem-cfg`  
> **Subsystem Scope:** `cfg/`  
> **Precedence Priority:** `2` (`SUBSYSTEM_RULE`)  

---

## Operational Constraints

1. **Zero Secret Ingestion:**
   - Plaintext API keys, bearer tokens, or database credentials MUST NEVER be committed to `cfg/`.
   - Credentials must be sourced from `/Users/raybayly/Development/.credentials/<service>/.env` or environment variables.
2. **Declarative Configuration:**
   - Product feature flags, observability endpoints, and factory definitions must be stored as structured YAML or JSON in `cfg/`.
3. **Environment Bindings:**
   - Configuration changes must specify environment targets (`development`, `testing`, `staging`, `production`).
