"""Data contracts and models for Hath0r Vision & Multimodal Subsystem."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ImageMetadata:
    """Zero-dependency visual asset metadata."""

    format: str
    width: int
    height: int
    channels: int
    size_bytes: int
    sha256: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "format": self.format,
            "width": self.width,
            "height": self.height,
            "channels": self.channels,
            "size_bytes": self.size_bytes,
            "sha256": self.sha256,
        }


@dataclass
class GroundedTarget:
    """Localized UI element coordinate descriptor."""

    target: str
    found: bool
    bounding_box: List[float] = field(default_factory=list)  # [ymin, xmin, ymax, xmax]
    center_coordinates: Dict[str, float] = field(default_factory=dict)  # {"x": ..., "y": ...}
    device: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target": self.target,
            "found": self.found,
            "bounding_box": self.bounding_box,
            "center_coordinates": self.center_coordinates,
            "device": self.device,
        }


@dataclass
class DocumentStructure:
    """Structured AST representation of parsed document or architecture diagram."""

    doc_type: str
    sections: List[str] = field(default_factory=list)
    entities: Dict[str, Any] = field(default_factory=dict)
    tables: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_type": self.doc_type,
            "sections": self.sections,
            "entities": self.entities,
            "tables": self.tables,
        }


@dataclass
class VisionResult:
    """Unified result envelope for Hath0r Vision operations."""

    success: bool
    operation: str
    provider: str
    model: str = "vit-base-patch16"
    device: Optional[str] = None
    image_path: Optional[str] = None
    image_metadata: Optional[ImageMetadata] = None
    description: Optional[str] = None
    detected_objects: List[Dict[str, Any]] = field(default_factory=list)
    extracted_text: Optional[str] = None
    document_structure: Optional[DocumentStructure] = None
    grounded_target: Optional[GroundedTarget] = None
    embedding: Optional[List[float]] = None
    ranked_candidates: Optional[List[Dict[str, Any]]] = None
    generated_code: Optional[str] = None
    code_framework: Optional[str] = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        out: Dict[str, Any] = {
            "success": self.success,
            "operation": self.operation,
            "provider": self.provider,
            "model": self.model,
        }
        if self.device:
            out["device"] = self.device
        if self.image_path:
            out["image_path"] = self.image_path
        if self.image_metadata:
            out["image_metadata"] = self.image_metadata.to_dict()
        if self.description:
            out["description"] = self.description
        if self.detected_objects:
            out["detected_objects"] = self.detected_objects
        if self.extracted_text:
            out["extracted_text"] = self.extracted_text
        if self.document_structure:
            out["document_structure"] = self.document_structure.to_dict()
        if self.grounded_target:
            out["grounded_target"] = self.grounded_target.to_dict()
        if self.embedding:
            out["embedding"] = self.embedding
        if self.ranked_candidates:
            out["ranked_candidates"] = self.ranked_candidates
        if self.generated_code:
            out["generated_code"] = self.generated_code
        if self.code_framework:
            out["code_framework"] = self.code_framework
        if self.error:
            out["error"] = self.error
        return out
