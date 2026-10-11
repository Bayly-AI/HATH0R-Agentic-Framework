---
id: rule:subsystem-tests
type: rule_policy
title: "Testing Subsystem - Local Rules"
priority: 2
priority_name: SUBSYSTEM_RULE
target_scope: tests
restricted_actions: [skip_playwright_catalog_sync]
governs_roles: [developer, qa-engineer]
---
# Testing Subsystem — Local Rules

> **Rule ID:** `rule:subsystem-tests`  
> **Subsystem Scope:** `tests/`  
> **Precedence Priority:** `2` (`SUBSYSTEM_RULE`)  

---

## Operational Constraints

1. **Mandatory Playwright Coverage:**
   - All UI component changes and frontend features MUST include Playwright test coverage.
2. **Master Test Catalog Sync:**
   - The master Playwright test case document (`tests/e2e/master-playwright-tests.json`) MUST be kept in sync with all UI components.
3. **Clean Repo Audit Gate:**
   - Clean Repo lifecycle (Step 7) MUST run `PlaywrightMasterCatalogManager.audit_and_sync_test_cases()` to prevent untested UI drift.
4. **Visual Regression Baselines:**
   - Visual regressions MUST be validated against baseline snapshots with 0% unintended visual difference.
