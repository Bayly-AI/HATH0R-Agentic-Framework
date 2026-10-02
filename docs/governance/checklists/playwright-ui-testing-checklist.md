# Checklist — Playwright UI Testing Compliance Gate

> Rule: `CR-PLAYWRIGHT-UI-001` · PR Gate: `SonarCloud & Quality Gates`

Before opening or merging a PR that contains or modifies UI components:

- [ ] All new/modified UI components are scanned and cataloged.
- [ ] Master test case document (`tests/e2e/master-playwright-tests.json`) is updated.
- [ ] JSON Schema validation passes against `contracts/hath0r-playwright-test-spec-v1.schema.json`.
- [ ] All automated Playwright UI test cases pass with zero failures.
- [ ] Visual regression snapshots exist and are verified.
- [ ] Clean Repo Step 7 has executed Playwright test catalog sync.
- [ ] Evidence handshake / cryptographic signoff completed for UI changes.
