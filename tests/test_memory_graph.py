"""Tests for Hath0r MemoryGraph engine and schema conformance."""

from pathlib import Path

from lib.memory.memory_graph import MemoryEdge, MemoryGraph, MemoryNode


def test_memory_graph_lifecycle(tmp_path: Path) -> None:
    graph = MemoryGraph(graph_id="test-workspace-memory")

    # Add core rules node
    node_rules = MemoryNode(
        id="rule:cr-cli-entry-001",
        type="rule",
        label="Start with CLI Rule",
        content="Agents must start with the CLI operator hath0r for all workflows.",
        importance=1.0,
        tags=["governance", "cli", "mandatory"],
    )
    graph.add_node(node_rules)

    # Add architecture node
    node_arch = MemoryNode(
        id="concept:tri-graph-substrate",
        type="concept",
        label="Tri-Graph Substrate Architecture",
        content="Three interconnected graphs: KnowledgeGraph, ContextGraph, MemoryGraph.",
        importance=0.9,
        tags=["architecture", "graph"],
    )
    graph.add_node(node_arch)

    # Add relational edge
    edge = MemoryEdge(
        source="rule:cr-cli-entry-001",
        target="concept:tri-graph-substrate",
        relation="ENFORCES",
        weight=1.0,
    )
    graph.add_edge(edge)

    # Verify query
    assert len(graph.nodes) == 2
    assert len(graph.edges) == 1
    assert graph.get_node("rule:cr-cli-entry-001") is not None

    rules_found = graph.find_nodes(node_type="rule")
    assert len(rules_found) == 1
    assert rules_found[0].id == "rule:cr-cli-entry-001"

    # Test neighborhood retrieval
    neighborhood = graph.get_neighborhood("rule:cr-cli-entry-001", depth=1)
    assert len(neighborhood["nodes"]) == 2
    assert len(neighborhood["edges"]) == 1

    # Test serialization and deserialization
    save_file = tmp_path / "memory_graph.json"
    graph.save_to_file(save_file)
    assert save_file.exists()

    loaded_graph = MemoryGraph.load_from_file(save_file)
    assert loaded_graph.graph_id == "test-workspace-memory"
    assert len(loaded_graph.nodes) == 2
    assert len(loaded_graph.edges) == 1
    assert loaded_graph.get_node("concept:tri-graph-substrate") is not None
