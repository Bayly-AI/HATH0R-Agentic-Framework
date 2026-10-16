"""Tests for Hath0r MemoryGraph engine, compounding, verification gate, and schema conformance."""

from pathlib import Path

from hath0r_engine.memory.memory_graph import MemoryEdge, MemoryGraph, MemoryNode


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


def test_memory_graph_compounding_and_verification_gate(tmp_path: Path) -> None:
    graph = MemoryGraph(graph_id="test-compounding")
    graph.add_node(
        MemoryNode(
            id="concept:tri-graph",
            type="concept",
            label="Quad-Graph Substrate",
            content="Unified quad-graph architecture.",
            importance=0.9,
            tags=["architecture"],
        )
    )

    # Only seed node exists -> verify_compounded is False
    gate_before = graph.verify_compounded()
    assert gate_before["compounded"] is False
    assert gate_before["compounded_nodes_count"] == 0

    # Compound first task episode
    res1 = graph.compound_knowledge(
        label="Implement MemoryGraph Pre-Announcement Gate",
        content="Enforced CR-MEMORY-COMPOUND-001 in TaskAnnouncerBot and EndOfTaskBot.",
        node_type="episode",
        importance=0.85,
        tags=["memorygraph", "governance"],
        relates_to=["concept:tri-graph"],
        relation="DERIVES_FROM",
    )
    assert res1["node"]["type"] == "episode"
    assert len(res1["edges_added"]) == 1

    # Gate now passes
    gate_after = graph.verify_compounded()
    assert gate_after["compounded"] is True
    assert gate_after["compounded_nodes_count"] >= 1
    assert gate_after["latest_node"] is not None

    # Compound second decision with shared tag -> triggers ReflectionEngine insight synthesis
    res2 = graph.compound_knowledge(
        label="Suite-Wide .hath0r/memory Provisioning Decision",
        content="All active repositories in Development must maintain .hath0r/memory/graph.json.",
        node_type="decision",
        importance=0.9,
        tags=["memorygraph", "governance"],
        supersedes=res1["node"]["id"],
    )
    assert res2["reflection"]["insights_generated"] >= 1
    assert graph.get_node(res1["node"]["id"]).is_current is False


def test_ensure_repo_memory(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("# Sample Project\nA test repository for MemoryGraph.", encoding="utf-8")
    graph = MemoryGraph.ensure_repo_memory(tmp_path)
    assert (tmp_path / ".hath0r" / "memory" / "graph.json").is_file()
    assert (tmp_path / ".hath0r" / "memory" / "core_rules.md").is_file()
    assert (tmp_path / ".hath0r" / "memory" / "architecture.md").is_file()
    assert "rule:cr-memory-compound-001" in graph.nodes
    assert graph.verify_compounded()["compounded"] is True
