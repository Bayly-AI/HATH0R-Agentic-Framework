"""Hath0r KnowledgeGraph Engine (Backward-compatibility shim for hath0r_engine.graph.knowledge_graph)."""

from __future__ import annotations

from hath0r_engine.graph.knowledge_graph import (
    BM25Index,
    KnowledgeEdge,
    KnowledgeGraph,
    KnowledgeGraphExtractor,
    KnowledgeNode,
    LightweightVectorIndex,
)

__all__ = [
    "BM25Index",
    "KnowledgeEdge",
    "KnowledgeGraph",
    "KnowledgeGraphExtractor",
    "KnowledgeNode",
    "LightweightVectorIndex",
]
