# Runbook — Playwright UI Testing Operations & Troubleshooting

> Reference: `CR-PLAYWRIGHT-UI-001` · Playbook: `docs/governance/playbooks/playwright-ui-testing-playbook.md`

## Common Operational Tasks

### 1. Synchronizing Master Test Catalog on Clean Repo
If untracked UI changes are flagged during preflight or clean-repo:
```bash
python3 -c "
from hath0r_engine.testing import PlaywrightMasterCatalogManager
from pathlib import Path
mgr = PlaywrightMasterCatalogManager()
result = mgr.audit_and_sync_test_cases(Path('.'))
print('Sync Result:', result)
"
```

### 2. Exporting Executable Playwright Spec Code
Export TypeScript specs:
```python
from hath0r_engine.testing import PlaywrightMasterCatalogManager
mgr = PlaywrightMasterCatalogManager()
ts_code = mgr.export_playwright_spec("suite-diff-viewer", language="typescript")
print(ts_code)
```

Export Python specs:
```python
py_code = mgr.export_playwright_spec("suite-diff-viewer", language="python")
print(py_code)
```

### 3. Diagnosing Test Failures
- **Selector Timeout**: Ensure `data-testid` attributes are properly applied on target elements.
- **Visual Regression Mismatch**: Check `tests/e2e/snapshots/` and verify resolution/viewport consistency (default: 1280x720).
- **Schema Validation Errors**: Validate `tests/e2e/master-playwright-tests.json` against `contracts/hath0r-playwright-test-spec-v1.schema.json`.
