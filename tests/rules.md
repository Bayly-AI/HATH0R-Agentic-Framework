# Tests Subsystem - Local Rules

> Specific rules and constraints for the Tests Subsystem module.

## Constraints
- All UI component changes and new frontend features MUST include Playwright test coverage.
- The master Playwright test case document (`tests/e2e/master-playwright-tests.json`) MUST be kept in sync with all UI components in the codebase.
- Clean Repo lifecycle (Step 7) MUST run `PlaywrightMasterCatalogManager.audit_and_sync_test_cases()` to prevent untested UI drift.
- Visual regressions MUST be validated against baseline snapshots with 0% unintended visual difference.
