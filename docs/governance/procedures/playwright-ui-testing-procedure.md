# Procedure — Playwright UI Testing & Master Test Case Catalog

> Governance ID: `PROC-PLAYWRIGHT-001` · Rule: `CR-PLAYWRIGHT-UI-001`

1. **Verify Playwright Environment**:
   - Ensure Playwright dependencies and browsers are available (`playwright install chromium` or Python `playwright` package).
2. **Scan UI Components**:
   - Run `PlaywrightMasterCatalogManager.scan_ui_components()` to discover all Generative UI builders and frontend components.
3. **Audit & Sync Master Test Catalog**:
   - Execute `PlaywrightMasterCatalogManager.audit_and_sync_test_cases()` against `tests/e2e/master-playwright-tests.json`.
   - Ensure all UI components have registered test suites.
4. **Execute UI Test Suites**:
   - Run `PlaywrightTestRunner.execute_suite()` or `pytest tests/test_playwright_testing.py`.
5. **Verify Visual Baselines & Evidence Handshake**:
   - Confirm visual regression checks match approved snapshots.
6. **Commit Test Catalog during Clean Repo**:
   - Stage and commit `tests/e2e/master-playwright-tests.json` alongside updated docs before opening PRs.
