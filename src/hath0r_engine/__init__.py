"""HATH0R Engine — Core Cognitive Substrate & Runtime Safety Engine."""

from __future__ import annotations

__version__ = "1.0.0"

from hath0r_engine.context.context_graph import ContextEdge, ContextGraph, ContextNode
from hath0r_engine.graph.knowledge_graph import KnowledgeEdge, KnowledgeGraph, KnowledgeGraphExtractor, KnowledgeNode
from hath0r_engine.graph.sqlite_graph import SQLiteGraphStore
from hath0r_engine.jev.jev_client import JevClient, JevSettings, ToolGuardRequest, ToolGuardResult
from hath0r_engine.jev.jev_tool_guard import (
    build_tool_guard_request,
    evaluate_tool_guard,
    format_block_message,
    is_guarded_tool,
)
from hath0r_engine.memory.memory_graph import MemoryEdge, MemoryGraph, MemoryNode
from hath0r_engine.memory.reflection import ReflectionEngine
from hath0r_engine.telemetry.otel_tracer import OTELTracerBot, TelemetrySpan
from hath0r_engine.voice.voice_config import VoiceConfig
from hath0r_engine.voice.voice_engine import VoiceEngine

__all__ = [
    "__version__",
    "KnowledgeGraph",
    "KnowledgeNode",
    "KnowledgeEdge",
    "KnowledgeGraphExtractor",
    "SQLiteGraphStore",
    "ContextGraph",
    "ContextNode",
    "ContextEdge",
    "MemoryGraph",
    "MemoryNode",
    "MemoryEdge",
    "ReflectionEngine",
    "OTELTracerBot",
    "TelemetrySpan",
    "JevClient",
    "JevSettings",
    "ToolGuardRequest",
    "ToolGuardResult",
    "is_guarded_tool",
    "evaluate_tool_guard",
    "build_tool_guard_request",
    "format_block_message",
    "VoiceEngine",
    "VoiceConfig",
]
