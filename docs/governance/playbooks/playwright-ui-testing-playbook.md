# Playbook — Playwright UI Testing and Test Catalog Management

> Rule: `CR-PLAYWRIGHT-UI-001` · Standard: `docs/governance/SUITE_STANDARDS.md`

## 1. Scope & Purpose
This playbook defines the operating procedures for integrating, executing, and synchronizing Playwright UI tests and master test case specifications across the Hath0r ecosystem.

## 2. Master Test Case Specification
The canonical document resides at `tests/e2e/master-playwright-tests.json`.
- Each suite corresponds to a UI component or page.
- Test cases specify deterministic actions (`goto`, `waitForSelector`, `click`, `fill`, `expectVisible`, `expectText`, `expectVisualMatch`).
- Status taxonomy: `automated`, `pending_generation`, `manual`, `skipped`, `deprecated`.

## 3. Clean Repo Sync Flow
1. Execute Step 7 of Clean Repo SOP:
   ```python
   from hath0r_engine.testing import PlaywrightMasterCatalogManager
   from pathlib import Path

   mgr = PlaywrightMasterCatalogManager()
   report = mgr.audit_and_sync_test_cases(Path("."))
   print(report)
   ```
2. Verify all newly added components have been assigned a `pending_generation` or `automated` test suite.
3. Stage `tests/e2e/master-playwright-tests.json` in Step 8 commit.

## 4. Test Execution & Visual Baselines
- Run tests via `PlaywrightTestRunner` or `pytest tests/test_playwright_testing.py`.
- If visual regressions occur, inspect diffs, update snapshot baselines if intentional, and obtain cryptographic sign-off via `HandshakeSession`.
