"""Unit and integration tests for Pixel-Native 2D Document Parsing and DOM-Independent Playwright Grounding."""

import pytest
from pathlib import Path

Image = pytest.importorskip("PIL.Image")

from hath0r_engine.testing.models import (
    PlaywrightActionType,
    PlaywrightBrowserType,
    PlaywrightStep,
    PlaywrightTestCase,
    PlaywrightTestStatus,
)
from hath0r_engine.testing.runner import PlaywrightTestRunner
from hath0r_engine.vision.document_parser import DocumentLayoutParser
from hath0r_engine.vision.engine import VisionEngine
from hath0r_engine.vision.grounding import VisualGroundingEngine


@pytest.fixture
def sample_image(tmp_path: Path) -> Path:
    """Create a temporary 256x256 test image."""
    img_path = tmp_path / "system_architecture_diagram.png"
    img = Image.new("RGB", (256, 256), color=(240, 240, 240))
    img.save(img_path)
    return img_path


@pytest.fixture
def table_image(tmp_path: Path) -> Path:
    """Create a temporary 512x512 tabular balance sheet test image."""
    img_path = tmp_path / "balance_sheet_table.png"
    img = Image.new("RGB", (512, 512), color=(255, 255, 255))
    img.save(img_path)
    return img_path


class TestPixelNativeDocumentParsing:
    """Test continuous visual patch document and 2D spatial layout parsing."""

    def test_parse_architecture_diagram_patches(self, sample_image: Path):
        parser = DocumentLayoutParser()
        res = parser.parse_pixel_native(sample_image, patch_size=16)

        assert res.success is True
        assert res.operation == "parse_doc_pixel_native"
        assert res.provider == "pixel_native_patch_parser"
        assert res.document_structure is not None

        entities = res.document_structure.entities
        assert entities["preserves_2d_spatial_layout"] is True
        assert entities["ocr_bypassed"] is True
        assert entities["patch_size"] == 16

        # 256 / 16 = 16 patches per axis -> 256 patches total
        patch_grid = entities["patch_grid"]
        assert patch_grid["x"] == 16
        assert patch_grid["y"] == 16
        assert patch_grid["total_patches"] == 256

    def test_parse_tabular_document_spatial_cells(self, table_image: Path):
        parser = DocumentLayoutParser()
        res = parser.parse_pixel_native(table_image, patch_size=32)

        assert res.success is True
        assert res.document_structure.doc_type == "2d_tabular_document"
        assert len(res.document_structure.tables) > 0

        table = res.document_structure.tables[0]
        assert table["table_id"] == "tbl_01"
        assert table["dimensions"]["rows"] == 4
        assert table["dimensions"]["columns"] == 3
        assert len(table["cells"]) >= 7

        # Verify 2D cell coordinate preservation
        first_cell = table["cells"][0]
        assert first_cell["row"] == 0
        assert first_cell["col"] == 0
        assert "bbox" in first_cell

    def test_nonexistent_file_returns_error(self):
        parser = DocumentLayoutParser()
        res = parser.parse_pixel_native("missing_document_404.png")
        assert res.success is False
        assert "not found" in res.error.lower()


class TestVisualGroundingToPlaywright:
    """Test visual grounding translation into DOM-independent Playwright steps."""

    def test_ground_to_playwright_step_click(self, sample_image: Path):
        grounding = VisualGroundingEngine()
        step = grounding.ground_to_playwright_step(
            image_path=sample_image,
            target="Submit and Approve Button",
            action="click",
            step_number=1,
        )

        assert step["step_number"] == 1
        assert step["action"] == "click"
        assert step.get("selector") is None  # DOM-independent!
        assert "coordinates" in step
        assert "x" in step["coordinates"]
        assert "y" in step["coordinates"]
        assert "bounding_box" in step
        assert len(step["bounding_box"]) == 4

    def test_ground_to_playwright_step_hover(self, sample_image: Path):
        grounding = VisualGroundingEngine()
        step = grounding.ground_to_playwright_step(
            image_path=sample_image,
            target="User Profile Avatar",
            action="hover",
            step_number=2,
        )

        assert step["step_number"] == 2
        assert step["action"] == "hover"
        assert step["coordinates"]["x"] > 0

    def test_execute_coordinate_step_in_playwright_runner(self, sample_image: Path):
        grounding = VisualGroundingEngine()
        step_dict = grounding.ground_to_playwright_step(
            image_path=sample_image,
            target="Checkout CTA Button",
            action="click",
            step_number=1,
        )

        step = PlaywrightStep.from_dict(step_dict)
        test_case = PlaywrightTestCase(
            test_id="TC-VISUAL-001",
            title="Visual Grounded Click Test",
            description="Verify DOM-independent click via visual patch coordinates",
            status=PlaywrightTestStatus.AUTOMATED,
            browser=PlaywrightBrowserType.CHROMIUM,
            steps=[step],
        )

        runner = PlaywrightTestRunner()
        result = runner.execute_test_case(test_case=test_case, suite_id="SUITE-VISUAL")

        assert result.status == "PASS"
        assert result.steps_passed == 1
        assert result.steps_total == 1


class TestVisionEngineUnifiedFacade:
    """Test unified VisionEngine interface for pixel-native parsing and Playwright grounding."""

    def test_facade_pixel_native_parse(self, sample_image: Path):
        engine = VisionEngine()
        data = engine.parse_document_pixel_native(sample_image, patch_size=16)

        assert data["success"] is True
        assert data["operation"] == "parse_doc_pixel_native"
        assert "document_structure" in data

    def test_facade_ground_to_playwright(self, sample_image: Path):
        engine = VisionEngine()
        step = engine.ground_to_playwright_step(
            image_path=sample_image,
            target="Navigation Hamburger Menu",
            action="click",
            step_number=3,
        )

        assert step["step_number"] == 3
        assert step["action"] == "click"
        assert step.get("selector") is None
        assert step["coordinates"] is not None
