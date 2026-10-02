# Strategy — Playwright UI Testing & Test Case Governance

> Issue #151 · Rule: `CR-PLAYWRIGHT-UI-001`

Standardize all UI, Generative UI, and dashboard testing on **Playwright**.
Maintain a single source of truth in `tests/e2e/master-playwright-tests.json` conforming to `contracts/hath0r-playwright-test-spec-v1.schema.json`.
Leverage Clean Repo synchronization to guarantee zero untested UI drift across framework evolutions. Export specs to TypeScript and Python runners while capturing OpenTelemetry traces and visual regression snapshots.
