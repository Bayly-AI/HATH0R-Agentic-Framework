"""Tests for KnowledgeGraph and ContextGraph contracts, extraction, and runtime topologies."""

import json
from pathlib import Path

from lib.context.context_graph import ContextEdge, ContextGraph, ContextNode
from lib.graph.knowledge_graph import KnowledgeEdge, KnowledgeGraph, KnowledgeGraphExtractor, KnowledgeNode


def test_knowledge_graph_basic_operations():
    kg = KnowledgeGraph()
    n1 = KnowledgeNode(id="doc-1", type="procedure", title="Deploy Guide", path="docs/deploy.md")
    n2 = KnowledgeNode(id="contract-1", type="contract", title="Deploy Schema", path="contracts/deploy.json")
    kg.add_node(n1)
    kg.add_node(n2)

    kg.add_edge(KnowledgeEdge(source="doc-1", target="contract-1", relation="implements"))

    neighbors = kg.get_neighbors("doc-1", relation="implements")
    assert len(neighbors) == 1
    assert neighbors[0].id == "contract-1"

    lineage = kg.get_lineage("doc-1")
    assert lineage["id"] == "doc-1"
    assert len(lineage["children"]) == 1
    assert lineage["children"][0]["id"] == "contract-1"

    data = kg.to_dict()
    assert data["schema_version"] == "hath0r.knowledgegraph/1"
    assert len(data["nodes"]) == 2
    assert len(data["edges"]) == 1


def test_knowledge_graph_frontmatter_extraction(tmp_path: Path):
    doc1 = tmp_path / "guide.md"
    doc1.write_text(
        """---
id: guide-001
type: procedure
title: Setup Guide
depends_on: [spec-001, policy-001]
implements: contract-001
governed_by: cr-gov-001
---
# Setup Guide Body
Content here.
""",
        encoding="utf-8",
    )

    kg = KnowledgeGraphExtractor.scan_directory(tmp_path)
    assert "guide-001" in kg.nodes
    assert kg.nodes["guide-001"].title == "Setup Guide"
    assert kg.nodes["guide-001"].type == "procedure"

    # Verify extracted edges
    edges = kg.edges
    assert len(edges) == 4
    relations = {e.relation for e in edges}
    assert relations == {"depends_on", "implements", "governed_by"}


def test_context_graph_runtime_tracking():
    cg = ContextGraph(session_id="test-session-123")
    parent = ContextNode(id="agent-root", type="agent", label="Root Agent", state="running")
    cg.add_node(parent)

    subagent = cg.register_subagent(subagent_id="sub-1", label="Research Bot", parent_id="agent-root")
    assert subagent.id == "sub-1"
    assert cg.active_subagent_id == "sub-1"

    tool_id = cg.record_tool_execution(
        tool_name="read_file",
        caller_id="sub-1",
        jev_status="ALLOW",
        properties={"target": "docs/deploy.md"},
    )
    assert tool_id.startswith("tool-")

    data = cg.to_dict()
    assert data["schema_version"] == "hath0r.contextgraph/1"
    assert data["session_id"] == "test-session-123"
    # Should have root agent, subagent, tool execution, and jev guard
    assert len(data["nodes"]) == 4
    assert len(data["edges"]) == 3
