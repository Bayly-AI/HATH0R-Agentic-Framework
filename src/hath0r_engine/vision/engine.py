"""Unified VisionEngine Cognitive Substrate Facade for Hath0r Framework."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional

from hath0r_engine.vision.design_to_code import DesignToCodeSynthesizer
from hath0r_engine.vision.document_parser import DocumentLayoutParser
from hath0r_engine.vision.grounding import VisualGroundingEngine
from hath0r_engine.vision.perception import MultimodalPerceptionManager


class VisionEngine:
    """Unified cognitive substrate interface for visual perception, layout parsing, and UI grounding."""

    def __init__(
        self,
        default_provider: str = "auto",
        config_path: Optional[Path | str] = None,
    ) -> None:
        self.perception = MultimodalPerceptionManager(default_provider=default_provider)
        self.grounding = VisualGroundingEngine(perception_manager=self.perception)
        self.document_parser = DocumentLayoutParser(perception_manager=self.perception)
        self.design_synthesizer = DesignToCodeSynthesizer(perception_manager=self.perception)

    def inspect(
        self,
        image_path: Path | str,
        prompt: Optional[str] = None,
        provider: Optional[str] = None,
        device: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Perform visual inspection and object recognition."""
        res = self.perception.inspect(image_path=image_path, prompt=prompt, provider=provider, device=device)
        return res.to_dict()

    def ground(
        self,
        image_path: Path | str,
        target: str,
        device: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Ground natural language UI target description to pixel coordinates and bounding box."""
        res = self.grounding.ground(image_path=image_path, target=target, device=device)
        return res.to_dict()

    def parse_document(
        self,
        image_path: Path | str,
        prompt: Optional[str] = None,
        device: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Parse technical diagrams, architecture flowcharts, and structured document layouts."""
        res = self.document_parser.parse(image_path=image_path, prompt=prompt, device=device)
        return res.to_dict()

    def embed(
        self,
        image_path: Path | str,
        dim: int = 512,
        device: Optional[str] = None,
    ) -> List[float]:
        """Generate normalized cross-modal embedding vector for Tri-Graph RAG indexing."""
        return self.perception.compute_embedding(image_path=image_path, dim=dim, device=device)

    def synthesize_code(
        self,
        image_path: Path | str,
        framework: str = "react_tailwind",
        prompt: Optional[str] = None,
        device: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Synthesize interactive UI component code from a visual design mockup."""
        res = self.design_synthesizer.synthesize(
            image_path=image_path,
            framework=framework,
            prompt=prompt,
            device=device,
        )
        return res.to_dict()
