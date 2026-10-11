"""Unit and integration tests for Playwright UI testing integration and master test case catalog management."""

from pathlib import Path

from hath0r_engine.testing import (
    PlaywrightActionType,
    PlaywrightBrowserType,
    PlaywrightExecutionResult,
    PlaywrightMasterCatalog,
    PlaywrightMasterCatalogManager,
    PlaywrightStep,
    PlaywrightTestCase,
    PlaywrightTestRunner,
    PlaywrightTestStatus,
    PlaywrightTestSuite,
)


def test_playwright_models_serialization():
    step = PlaywrightStep(
        step_number=1,
        action=PlaywrightActionType.GOTO,
        value="http://localhost:3000/dashboard",
    )
    assert step.to_dict()["action"] == "goto"
    assert step.to_dict()["value"] == "http://localhost:3000/dashboard"

    step_restored = PlaywrightStep.from_dict(step.to_dict())
    assert step_restored.step_number == 1
    assert step_restored.action == PlaywrightActionType.GOTO
    assert step_restored.value == "http://localhost:3000/dashboard"

    tc = PlaywrightTestCase(
        test_id="TC-SAMPLE-001",
        title="Sample verification test",
        description="Verify sample element",
        status=PlaywrightTestStatus.AUTOMATED,
        browser=PlaywrightBrowserType.CHROMIUM,
        steps=[step],
        expected_outcome="Sample element loaded",
    )
    tc_dict = tc.to_dict()
    assert tc_dict["test_id"] == "TC-SAMPLE-001"
    assert len(tc_dict["steps"]) == 1

    tc_restored = PlaywrightTestCase.from_dict(tc_dict)
    assert tc_restored.test_id == "TC-SAMPLE-001"
    assert tc_restored.status == PlaywrightTestStatus.AUTOMATED
    assert len(tc_restored.steps) == 1

    suite = PlaywrightTestSuite(
        suite_id="suite-sample",
        title="Sample Suite",
        description="Sample suite description",
        target_component="SampleComponent",
        test_cases=[tc],
    )
    suite_dict = suite.to_dict()
    assert suite_dict["suite_id"] == "suite-sample"
    assert len(suite_dict["test_cases"]) == 1

    suite_restored = PlaywrightTestSuite.from_dict(suite_dict)
    assert suite_restored.suite_id == "suite-sample"
    assert suite_restored.target_component == "SampleComponent"


def test_master_catalog_loading_and_saving(tmp_path: Path):
    catalog_file = tmp_path / "master-tests.json"
    mgr = PlaywrightMasterCatalogManager(catalog_path=catalog_file)

    # Initialize and populate catalog
    mgr.catalog = PlaywrightMasterCatalog(
        project="Test-Project",
        suites=[
            PlaywrightTestSuite(
                suite_id="suite-1",
                title="Suite 1",
                description="First suite",
                target_component="WidgetA",
                test_cases=[
                    PlaywrightTestCase(
                        test_id="TC-WIDGET-001",
                        title="Widget A Renders",
                        description="Test widget A rendering",
                        status=PlaywrightTestStatus.AUTOMATED,
                        steps=[
                            PlaywrightStep(step_number=1, action=PlaywrightActionType.GOTO, value="/widget-a"),
                            PlaywrightStep(step_number=2, action=PlaywrightActionType.EXPECT_VISIBLE, selector="#widget-a"),
                        ],
                    )
                ],
            )
        ],
    )

    saved_path = mgr.save_catalog()
    assert saved_path.exists()

    # Load into a new manager
    mgr2 = PlaywrightMasterCatalogManager(catalog_path=catalog_file)
    assert mgr2.catalog is not None
    assert mgr2.catalog.project == "Test-Project"
    assert len(mgr2.catalog.suites) == 1
    assert mgr2.catalog.suites[0].test_cases[0].test_id == "TC-WIDGET-001"


def test_master_catalog_canonical_file():
    canonical_path = Path("tests/e2e/master-playwright-tests.json")
    assert canonical_path.exists(), "Canonical master Playwright test catalog must exist at tests/e2e/master-playwright-tests.json"

    mgr = PlaywrightMasterCatalogManager(catalog_path=canonical_path)
    assert mgr.catalog is not None
    assert mgr.catalog.schema_version == "hath0r.playwright.testspec/1"
    assert len(mgr.catalog.suites) >= 4

    suite_ids = {s.suite_id for s in mgr.catalog.suites}
    assert "suite-diff-viewer" in suite_ids
    assert "suite-param-slider" in suite_ids
    assert "suite-crypto-signoff" in suite_ids
    assert "suite-test-badge" in suite_ids


def test_scan_ui_components():
    mgr = PlaywrightMasterCatalogManager()
    root_dir = Path(".")
    components = mgr.scan_ui_components(root_dir)
    assert len(components) > 0

    comp_names = {c["name"] for c in components}
    assert "DiffViewer" in comp_names
    assert "ParameterSlider" in comp_names
    assert "CryptoSignoffCard" in comp_names
    assert "TestBadge" in comp_names


def test_audit_and_sync_test_cases(tmp_path: Path):
    temp_catalog_file = tmp_path / "sync-tests.json"
    mgr = PlaywrightMasterCatalogManager(catalog_path=temp_catalog_file)

    # Perform audit and sync against current workspace
    report = mgr.audit_and_sync_test_cases(
        workspace_root=Path("."),
        catalog_path=temp_catalog_file,
        auto_save=True,
    )

    assert report["success"] is True
    assert report["total_suites"] >= 4
    assert report["total_tests"] >= 4
    assert temp_catalog_file.exists()

    # Re-running sync on already up-to-date catalog should add 0 new suites
    report_retest = mgr.audit_and_sync_test_cases(
        workspace_root=Path("."),
        catalog_path=temp_catalog_file,
        auto_save=True,
    )
    assert len(report_retest["new_suites_added"]) == 0
    assert len(report_retest["new_tests_added"]) == 0


def test_export_playwright_spec_typescript_and_python():
    mgr = PlaywrightMasterCatalogManager(catalog_path=Path("tests/e2e/master-playwright-tests.json"))

    # Export TypeScript
    ts_spec = mgr.export_playwright_spec("suite-diff-viewer", language="typescript")
    assert 'import { test, expect } from "@playwright/test";' in ts_spec
    assert 'test.describe("Interactive DiffViewer UI Component Suite"' in ts_spec
    assert 'await page.goto(' in ts_spec
    assert 'await expect(page).toHaveScreenshot(' in ts_spec

    # Export Python
    py_spec = mgr.export_playwright_spec("suite-diff-viewer", language="python")
    assert "import pytest" in py_spec
    assert "from playwright.sync_api import Page, expect" in py_spec
    assert "def test_tc_diff_001(page: Page)" in py_spec
    assert "page.goto(" in py_spec


def test_playwright_test_runner_execution():
    runner = PlaywrightTestRunner()
    tc = PlaywrightTestCase(
        test_id="TC-RUNNER-001",
        title="Test Runner Smoke Test",
        description="Verify runner execution",
        status=PlaywrightTestStatus.AUTOMATED,
        steps=[
            PlaywrightStep(step_number=1, action=PlaywrightActionType.GOTO, value="http://localhost:3000"),
            PlaywrightStep(step_number=2, action=PlaywrightActionType.WAIT_FOR_SELECTOR, selector="[data-testid='root']"),
            PlaywrightStep(step_number=3, action=PlaywrightActionType.EXPECT_VISIBLE, selector="[data-testid='root']"),
        ],
    )

    result = runner.execute_test_case(tc, suite_id="suite-smoke")
    assert isinstance(result, PlaywrightExecutionResult)
    assert result.status == "PASS"
    assert result.steps_passed == 3
    assert result.steps_total == 3
    assert result.error is None
    assert result.visual_diff_percentage == 0.0

    # Test skipped case
    tc_skipped = PlaywrightTestCase(
        test_id="TC-RUNNER-002",
        title="Skipped Test",
        description="Verify skip behavior",
        status=PlaywrightTestStatus.SKIPPED,
        steps=[PlaywrightStep(step_number=1, action=PlaywrightActionType.GOTO, value="/skip")],
    )
    result_skipped = runner.execute_test_case(tc_skipped, suite_id="suite-smoke")
    assert result_skipped.status == "SKIPPED"

    # Test suite execution
    suite = PlaywrightTestSuite(
        suite_id="suite-batch",
        title="Batch Suite",
        description="Batch suite execution",
        target_component="BatchComponent",
        test_cases=[tc, tc_skipped],
    )
    suite_result = runner.execute_suite(suite)
    assert suite_result["status"] == "PASS"
    assert suite_result["total_tests"] == 2
    assert suite_result["passed"] == 1
    assert suite_result["skipped"] == 1


def test_churn_heatmap_playwright_catalog_and_runner():
    mgr = PlaywrightMasterCatalogManager(catalog_path=Path("tests/e2e/master-playwright-tests.json"))
    assert mgr.catalog is not None
    suite = next((s for s in mgr.catalog.suites if s.suite_id == "suite-churn-heatmap"), None)
    assert suite is not None
    assert suite.target_component == "ChurnHeatmapComponent"
    assert len(suite.test_cases) == 1

    tc = suite.test_cases[0]
    assert tc.test_id == "TC-CHURN-001"
    assert len(tc.steps) == 5

    # Export TypeScript spec
    ts_code = mgr.export_playwright_spec("suite-churn-heatmap", language="typescript")
    assert "PMAT Churn & Hotspot Heatmap UI Component Suite" in ts_code
    assert "data-testid='churn-heatmap-widget'" in ts_code

    # Run with PlaywrightTestRunner
    runner = PlaywrightTestRunner()
    result = runner.execute_test_case(tc, suite_id=suite.suite_id)
    assert result.status == "PASS"
    assert result.steps_passed == 5
    assert result.error is None

