# CR-PLAYWRIGHT-UI-001: Mandatory Playwright UI Testing & Master Test Case Registration (CRITICAL — Org-Wide)

> **Rule ID:** `CR-PLAYWRIGHT-UI-001` (also tracked as `cr-playwright-ui-001`)  
> **Status:** RATIFIED & MANDATORY ENTRY GATE  
> **Applies to:** All Agents, Workflows, Bots, Subagents, and Clean Repo Lifecycles across HATH0R OpenSource & Enterprise Products.  
> **Effective Date:** 2026-10-01  

---

## 1. Main Entry Statement (CRITICAL ENTRY GATE)

> **All UI components, Generative UI widgets, dashboard views, web applications, and interactive interfaces MUST be integrated with Playwright for headless, end-to-end, and visual regression verification.**
>
> In addition, every repository containing UI code **MUST maintain a canonical Master Test Case Document (`tests/e2e/master-playwright-tests.json`) in Playwright-compliant format**. During the Clean Repo / Clean Repos lifecycle, agents and bots must audit all UI components and ensure newly added or modified UI components have corresponding test cases registered in the master test case document.

---

## 2. Core Directives

1. **Playwright as Canonical UI Testing Standard:**
   - Playwright is the authoritative framework for cross-browser (Chromium, Firefox, WebKit), headless, component, and visual regression testing across Hath0r.
   - Bots and test runners must execute Playwright test suites using `PlaywrightTestRunner` or `pytest -k playwright` / `npx playwright test`.

2. **Playwright-Compliant Master Test Case Document:**
   - The master test case document lives at `tests/e2e/master-playwright-tests.json` and conforms to `contracts/hath0r-playwright-test-spec-v1.schema.json`.
   - Each test suite must define target components, steps (`goto`, `waitForSelector`, `expectVisible`, `expectText`, `expectValue`, `expectVisualMatch`), selectors, timeouts, and expected outcomes.

3. **Clean Repo Synchronization Doctrine:**
   - During Step 7 of the 13-step Clean Repo Lifecycle, agents and bots must run `PlaywrightMasterCatalogManager.audit_and_sync_test_cases()` or equivalent.
   - Any new or modified UI components without existing tests must be automatically appended as `pending_generation` or `automated` test cases before committing changes and raising PRs.

4. **Visual Regression Baselines:**
   - Visual assertions (`expectVisualMatch`) require baseline snapshots stored in `tests/e2e/snapshots/`.
   - UI changes that alter layout or styling must include verified snapshot updates approved through the evidence handshake protocol.

---

## 3. Enforcement & Verification

- **Preflight & Quality Gates:** Quality Gate bot (`hath0r quality`) verifies that all UI test suites pass and that the master test case catalog is up to date with zero unregistered UI components.
- **CI Enforcement:** PR validation workflows enforce contract validation on `tests/e2e/master-playwright-tests.json` and execute automated Playwright test suites.
