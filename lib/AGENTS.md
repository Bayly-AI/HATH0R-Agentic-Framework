---
id: lib-subsystem
type: subsystem
title: Library Engine Subsystem
depends_on: [contracts-subsystem]
governed_by: [cr-branch-gov-001, CR-CLI-ENTRY-001]
---
# Library Engine Subsystem — AGENTS Context

> **Subsystem Role:** Core runtime packages, graph extraction engines, security guards, and streaming voice pipelines.

## 1. Subsystem KnowledgeGraph Entity Nodes
- [`lib/graph/knowledge_graph.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/lib/graph/knowledge_graph.py): Frontmatter parsing, static KnowledgeGraph model, and lineage traversal.
- [`lib/context/context_graph.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/lib/context/context_graph.py): Dynamic ContextGraph session tracker and JEV audit logging.
- [`lib/jev/jev_tool_guard.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/lib/jev/jev_tool_guard.py): Zero-trust tool execution guard.
- [`lib/voice/voice_engine.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/lib/voice/voice_engine.py): Real-time streaming voice dispatcher.

## 2. Constraints & Rules
- Zero external runtime dependencies for core graph modules (`lib/graph`, `lib/context`).
- All tool execution events recorded in `ContextGraph` must link to JEV guard verification nodes.
