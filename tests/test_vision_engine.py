"""Unit tests for Hath0r VisionEngine & Multimodal Cognitive Substrate."""

import struct
import tempfile
from pathlib import Path

import pytest
from hath0r_engine.vision import (
    DesignToCodeSynthesizer,
    DocumentLayoutParser,
    DocumentStructure,
    GroundedTarget,
    ImageMetadata,
    MultimodalPerceptionManager,
    VisionEngine,
    VisionResult,
)


def _create_sample_png(file_path: Path, width: int = 400, height: int = 300) -> Path:
    """Create a minimal valid PNG binary file for test execution."""
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    ihdr_crc = struct.pack(">I", 0)
    ihdr_chunk = struct.pack(">I", len(ihdr_data)) + b"IHDR" + ihdr_data + ihdr_crc
    file_path.write_bytes(signature + ihdr_chunk)
    return file_path


def test_image_metadata_extraction():
    """Verify zero-dependency image header extraction."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        img_path = _create_sample_png(Path(tmp_dir) / "test_diagram.png", width=640, height=480)
        mgr = MultimodalPerceptionManager()
        meta = mgr.extract_metadata(img_path)

        assert meta.format == "png"
        assert meta.width == 640
        assert meta.height == 480
        assert meta.channels == 3
        assert len(meta.sha256) == 64


def test_multimodal_inspection():
    """Verify visual inspection result envelope."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        img_path = _create_sample_png(Path(tmp_dir) / "system_architecture.png")
        engine = VisionEngine()
        res = engine.inspect(img_path)

        assert res["success"] is True
        assert res["operation"] == "inspect"
        assert "image_metadata" in res
        assert res["image_metadata"]["width"] == 400
        assert len(res["detected_objects"]) >= 1


def test_visual_grounding():
    """Verify natural language UI target coordinate grounding."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        img_path = _create_sample_png(Path(tmp_dir) / "dashboard_view.png", width=1920, height=1080)
        engine = VisionEngine()
        res = engine.ground(img_path, target="Deploy Cluster")

        assert res["success"] is True
        assert res["operation"] == "ground"
        grounded = res["grounded_target"]
        assert grounded["found"] is True
        assert grounded["target"] == "Deploy Cluster"
        assert len(grounded["bounding_box"]) == 4
        assert 0 <= grounded["center_coordinates"]["x"] <= 1920
        assert 0 <= grounded["center_coordinates"]["y"] <= 1080


def test_document_layout_parsing():
    """Verify architecture diagram and document layout AST generation."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        img_path = _create_sample_png(Path(tmp_dir) / "cloud_topology_diag.png")
        engine = VisionEngine()
        res = engine.parse_document(img_path)

        assert res["success"] is True
        assert res["operation"] == "parse_doc"
        doc = res["document_structure"]
        assert doc["doc_type"] == "architecture_diagram"
        assert len(doc["sections"]) >= 3
        assert "extracted_text" in res


def test_design_to_code_synthesis():
    """Verify component code synthesis from visual mockups."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        img_path = _create_sample_png(Path(tmp_dir) / "analytics_card.png")
        engine = VisionEngine()
        res = engine.synthesize_code(img_path, framework="react_tailwind")

        assert res["success"] is True
        assert res["operation"] == "design_to_code"
        assert "AnalyticsCard" in res["generated_code"]
        assert "React.FC" in res["generated_code"]
        assert "className=" in res["generated_code"]


def test_cross_modal_embeddings():
    """Verify 512-d normalized embedding computation."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        img_path = _create_sample_png(Path(tmp_dir) / "neural_flow.png")
        engine = VisionEngine()
        vec = engine.embed(img_path, dim=512)

        assert len(vec) == 512
        assert isinstance(vec[0], float)


def test_error_handling_for_missing_files():
    """Verify graceful error reporting when image path does not exist."""
    engine = VisionEngine()
    res = engine.inspect("/nonexistent/file/path/image.png")

    assert res["success"] is False
    assert "error" in res
