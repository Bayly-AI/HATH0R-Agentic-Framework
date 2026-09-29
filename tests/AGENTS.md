---
id: tests-subsystem
type: subsystem
title: Testing Subsystem
depends_on: [contracts-subsystem, lib-subsystem]
governed_by: [cr-branch-gov-001, CR-CLI-ENTRY-001]
---
# Testing Subsystem — AGENTS Context

> **Subsystem Role:** Unit, regression, contract verification, and latency benchmark test harness.

## 1. Subsystem KnowledgeGraph Entity Nodes
- [`tests/test_graph_contracts.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/tests/test_graph_contracts.py): Contract validation for `hath0r.knowledgegraph/1` and `hath0r.contextgraph/1`.
- [`tests/test_jev_tool_guard.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/tests/test_jev_tool_guard.py): JEV tool guard security tests.
- [`tests/test_streaming_voice.py`](file:///Users/raybayly/Development/OpenSource/hath0r-framework/tests/test_streaming_voice.py): Speculative pipeline and audio VAD tests.

## 2. Test Execution
- Always run with `PYTHONPATH=. pytest -v`.
