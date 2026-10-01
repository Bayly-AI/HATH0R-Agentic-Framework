"""Master Test Case Catalog Manager for Playwright UI testing."""

from __future__ import annotations

import ast
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from hath0r_engine.testing.models import (
    PlaywrightActionType,
    PlaywrightBrowserType,
    PlaywrightMasterCatalog,
    PlaywrightStep,
    PlaywrightTestCase,
    PlaywrightTestStatus,
    PlaywrightTestSuite,
)

logger = logging.getLogger(__name__)


class PlaywrightMasterCatalogManager:
    """Manages reading, validation, component scanning, and synchronization of the master Playwright test case specification."""

    def __init__(self, catalog_path: Optional[Path] = None):
        self.catalog_path = catalog_path or Path("tests/e2e/master-playwright-tests.json")
        self.catalog: Optional[PlaywrightMasterCatalog] = None
        if self.catalog_path.exists():
            self.load_catalog()

    def load_catalog(self, path: Optional[Path] = None) -> PlaywrightMasterCatalog:
        """Load catalog from JSON file."""
        target_path = path or self.catalog_path
        if not target_path.exists():
            raise FileNotFoundError(f"Playwright master catalog not found at {target_path}")

        with open(target_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.catalog = PlaywrightMasterCatalog.from_dict(data)
        self.catalog_path = target_path
        return self.catalog

    def save_catalog(self, path: Optional[Path] = None) -> Path:
        """Save catalog to JSON file."""
        target_path = path or self.catalog_path
        if self.catalog is None:
            raise ValueError("No catalog loaded or initialized to save.")

        self.catalog.last_synced_at = datetime.now(timezone.utc).isoformat()
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(self.catalog.to_dict(), f, indent=2)

        return target_path

    def scan_ui_components(self, root_dir: Path) -> List[Dict[str, str]]:
        """Scan workspace for UI components, Generative UI builders, and web interfaces."""
        discovered_components: List[Dict[str, str]] = []

        # 1. Scan Generative UI builder methods in src/hath0r_engine/ui/
        ui_dir = root_dir / "src" / "hath0r_engine" / "ui"
        if ui_dir.exists():
            for py_file in ui_dir.glob("*.py"):
                try:
                    tree = ast.parse(py_file.read_text(encoding="utf-8"))
                    for node in ast.walk(tree):
                        if isinstance(node, ast.ClassDef) and "UIComponentBuilder" in node.name:
                            for item in node.body:
                                if isinstance(item, ast.FunctionDef) and item.name.startswith("build_"):
                                    comp_raw = item.name.replace("build_", "")
                                    # Convert snake_case to PascalCase
                                    comp_name = "".join(part.capitalize() for part in comp_raw.split("_"))
                                    discovered_components.append({
                                        "name": comp_name,
                                        "type": "generative_ui",
                                        "path": str(py_file.relative_to(root_dir)),
                                        "identifier": f"gen-ui-{comp_raw}",
                                    })
                except Exception as e:
                    logger.warning(f"Error parsing {py_file}: {e}")

        # 2. Scan frontend/web UI component directories if present
        for pattern in ["src/**/*.tsx", "src/**/*.jsx", "src/**/*.vue", "web/src/**/*.tsx", "components/**/*.tsx"]:
            for ui_file in root_dir.glob(pattern):
                comp_name = ui_file.stem
                if not comp_name.startswith("_") and not comp_name.endswith(".test") and not comp_name.endswith(".spec"):
                    discovered_components.append({
                        "name": comp_name,
                        "type": "web_component",
                        "path": str(ui_file.relative_to(root_dir)),
                        "identifier": f"web-ui-{comp_name.lower()}",
                    })

        return discovered_components

    def audit_and_sync_test_cases(
        self,
        workspace_root: Path,
        catalog_path: Optional[Path] = None,
        auto_save: bool = True,
    ) -> Dict[str, Any]:
        """Audit workspace for UI changes and synchronize master Playwright test cases.

        Ensures all discovered UI components have a test suite in the master document.
        Creates template pending test cases for any new or untracked UI components.
        """
        target_path = catalog_path or self.catalog_path
        if not target_path.exists():
            # Initialize new master catalog
            self.catalog = PlaywrightMasterCatalog(
                project="Bayly-AI/HATH0R-Agentic-Framework",
                suites=[],
            )
            self.catalog_path = target_path
        else:
            self.load_catalog(target_path)

        assert self.catalog is not None

        discovered = self.scan_ui_components(workspace_root)
        existing_targets: Set[str] = {s.target_component.lower() for s in self.catalog.suites}

        new_suites_added: List[str] = []
        new_tests_added: List[str] = []

        for comp in discovered:
            comp_name = comp["name"]
            if comp_name.lower() not in existing_targets:
                # Create a new suite for this component
                suite_id = f"suite-{comp['identifier']}"
                test_id = f"TC-{comp['name'].upper()[:8]}-001"

                template_steps = [
                    PlaywrightStep(
                        step_number=1,
                        action=PlaywrightActionType.GOTO,
                        value=f"http://localhost:3000/components/{comp['identifier']}",
                    ),
                    PlaywrightStep(
                        step_number=2,
                        action=PlaywrightActionType.WAIT_FOR_SELECTOR,
                        selector=f"[data-testid='{comp['identifier']}-container']",
                        timeout_ms=5000,
                    ),
                    PlaywrightStep(
                        step_number=3,
                        action=PlaywrightActionType.EXPECT_VISIBLE,
                        selector=f"[data-testid='{comp['identifier']}-container']",
                    ),
                    PlaywrightStep(
                        step_number=4,
                        action=PlaywrightActionType.EXPECT_VISUAL_MATCH,
                        snapshot_name=f"{comp['identifier']}-baseline.png",
                    ),
                ]

                new_test_case = PlaywrightTestCase(
                    test_id=test_id,
                    title=f"Verify {comp_name} renders and matches visual baseline",
                    description=f"Auto-generated Playwright verification suite for {comp_name} ({comp['path']})",
                    status=PlaywrightTestStatus.PENDING_GENERATION,
                    browser=PlaywrightBrowserType.CHROMIUM,
                    tags=["ui", "auto-generated", comp["type"]],
                    steps=template_steps,
                    expected_outcome=f"{comp_name} component renders correctly without visual regression",
                )

                new_suite = PlaywrightTestSuite(
                    suite_id=suite_id,
                    title=f"{comp_name} UI Test Suite",
                    description=f"Playwright test suite for component {comp_name}",
                    target_component=comp_name,
                    target_path=comp["path"],
                    tags=["ui", comp["type"]],
                    test_cases=[new_test_case],
                )

                self.catalog.suites.append(new_suite)
                existing_targets.add(comp_name.lower())
                new_suites_added.append(suite_id)
                new_tests_added.append(test_id)

        if auto_save:
            self.save_catalog(target_path)

        total_tests = sum(len(s.test_cases) for s in self.catalog.suites)
        pending_tests = sum(
            1 for s in self.catalog.suites for tc in s.test_cases if tc.status == PlaywrightTestStatus.PENDING_GENERATION
        )
        automated_tests = sum(
            1 for s in self.catalog.suites for tc in s.test_cases if tc.status == PlaywrightTestStatus.AUTOMATED
        )

        return {
            "success": True,
            "catalog_path": str(target_path),
            "last_synced_at": self.catalog.last_synced_at,
            "discovered_components_count": len(discovered),
            "new_suites_added": new_suites_added,
            "new_tests_added": new_tests_added,
            "total_suites": len(self.catalog.suites),
            "total_tests": total_tests,
            "automated_tests": automated_tests,
            "pending_tests": pending_tests,
        }

    def export_playwright_spec(self, suite_id: str, language: str = "typescript") -> str:
        """Export Playwright test cases in executable TypeScript or Python test code."""
        if self.catalog is None:
            raise ValueError("No catalog loaded.")

        target_suite = next((s for s in self.catalog.suites if s.suite_id == suite_id), None)
        if not target_suite:
            raise ValueError(f"Suite with ID '{suite_id}' not found in catalog.")

        if language.lower() in ["ts", "typescript"]:
            lines = [
                'import { test, expect } from "@playwright/test";',
                "",
                f'test.describe("{target_suite.title}", () => {{',
            ]
            for tc in target_suite.test_cases:
                lines.append(f'  test("{tc.title}", async ({{ page }}) => {{')
                for step in tc.steps:
                    action = step.action.value if isinstance(step.action, PlaywrightActionType) else step.action
                    if action == "goto":
                        lines.append(f'    await page.goto("{step.value}");')
                    elif action == "click":
                        lines.append(f'    await page.locator("{step.selector}").click();')
                    elif action == "fill":
                        lines.append(f'    await page.locator("{step.selector}").fill("{step.value}");')
                    elif action == "waitForSelector":
                        timeout = f", {{ timeout: {step.timeout_ms} }}" if step.timeout_ms else ""
                        lines.append(f'    await page.waitForSelector("{step.selector}"{timeout});')
                    elif action == "expectVisible":
                        lines.append(f'    await expect(page.locator("{step.selector}")).toBeVisible();')
                    elif action == "expectText":
                        lines.append(f'    await expect(page.locator("{step.selector}")).toHaveText("{step.expected}");')
                    elif action == "expectValue":
                        lines.append(f'    await expect(page.locator("{step.selector}")).toHaveValue("{step.expected}");')
                    elif action == "expectVisualMatch":
                        lines.append(f'    await expect(page).toHaveScreenshot("{step.snapshot_name}");')
                lines.append("  });")
                lines.append("")
            lines.append("});")
            return "\n".join(lines)

        elif language.lower() in ["py", "python"]:
            lines = [
                "import pytest",
                "from playwright.sync_api import Page, expect",
                "",
                f"# Suite: {target_suite.title}",
            ]
            for tc in target_suite.test_cases:
                func_name = f"test_{tc.test_id.lower().replace('-', '_')}"
                lines.append(f"def {func_name}(page: Page) -> None:")
                lines.append(f'    """{tc.description}"""')
                for step in tc.steps:
                    action = step.action.value if isinstance(step.action, PlaywrightActionType) else step.action
                    if action == "goto":
                        lines.append(f'    page.goto("{step.value}")')
                    elif action == "click":
                        lines.append(f'    page.locator("{step.selector}").click()')
                    elif action == "fill":
                        lines.append(f'    page.locator("{step.selector}").fill("{step.value}")')
                    elif action == "waitForSelector":
                        timeout = f", timeout={step.timeout_ms}" if step.timeout_ms else ""
                        lines.append(f'    page.wait_for_selector("{step.selector}"{timeout})')
                    elif action == "expectVisible":
                        lines.append(f'    expect(page.locator("{step.selector}")).to_be_visible()')
                    elif action == "expectText":
                        lines.append(f'    expect(page.locator("{step.selector}")).to_have_text("{step.expected}")')
                    elif action == "expectValue":
                        lines.append(f'    expect(page.locator("{step.selector}")).to_have_value("{step.expected}")')
                    elif action == "expectVisualMatch":
                        lines.append(f'    expect(page).to_have_screenshot("{step.snapshot_name}")')
                lines.append("")
            return "\n".join(lines)

        else:
            raise ValueError(f"Unsupported language format: {language}")
