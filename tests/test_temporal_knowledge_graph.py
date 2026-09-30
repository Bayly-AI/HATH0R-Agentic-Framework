"""Unit tests for Temporal KnowledgeGraph edges, interval validity, and point-in-time queries."""

import tempfile
from pathlib import Path

from hath0r_engine.graph.knowledge_graph import KnowledgeEdge, KnowledgeGraph, KnowledgeNode
from hath0r_engine.graph.sqlite_graph import SQLiteGraphStore


def test_temporal_knowledge_edge_validity():
    edge = KnowledgeEdge(
        source="user:alice",
        target="project:tri-graph",
        relation="leads",
        valid_from="2026-01-01T00:00:00Z",
        valid_to="2026-06-30T23:59:59Z",
        is_current=False,
    )

    # Valid during Q1 2026
    assert edge.is_valid_at(as_of="2026-03-15T00:00:00Z") is True
    # Invalid in Q3 2026
    assert edge.is_valid_at(as_of="2026-08-01T00:00:00Z") is False
    # Invalid when checking current state
    assert edge.is_valid_at(only_current=True) is False


def test_temporal_graph_queries_q1_vs_q3():
    kg = KnowledgeGraph()

    alice = KnowledgeNode(id="user:alice", type="bot", title="Alice Lead", path="bots/alice.md")
    bob = KnowledgeNode(id="user:bob", type="bot", title="Bob Lead", path="bots/bob.md")
    tri_graph = KnowledgeNode(id="project:tri-graph", type="subsystem", title="Tri-Graph Engine", path="subsystems/tri-graph.md")

    kg.add_node(alice)
    kg.add_node(bob)
    kg.add_node(tri_graph)

    # Alice was lead in Q1/Q2 (ended 2026-06-30)
    kg.add_edge(
        KnowledgeEdge(
            source="user:alice",
            target="project:tri-graph",
            relation="leads",
            valid_from="2026-01-01T00:00:00Z",
            valid_to="2026-06-30T23:59:59Z",
            is_current=False,
        )
    )

    # Bob became lead in Q3 (started 2026-07-01, current)
    kg.add_edge(
        KnowledgeEdge(
            source="user:bob",
            target="project:tri-graph",
            relation="leads",
            valid_from="2026-07-01T00:00:00Z",
            valid_to=None,
            is_current=True,
        )
    )

    # Q1 query: Alice leads tri-graph, Bob does not
    alice_q1 = kg.get_neighbors("user:alice", relation="leads", as_of="2026-03-01T00:00:00Z")
    bob_q1 = kg.get_neighbors("user:bob", relation="leads", as_of="2026-03-01T00:00:00Z")
    assert len(alice_q1) == 1
    assert alice_q1[0].id == "project:tri-graph"
    assert len(bob_q1) == 0

    # Q3 query: Bob leads tri-graph, Alice does not
    alice_q3 = kg.get_neighbors("user:alice", relation="leads", as_of="2026-08-15T00:00:00Z")
    bob_q3 = kg.get_neighbors("user:bob", relation="leads", as_of="2026-08-15T00:00:00Z")
    assert len(alice_q3) == 0
    assert len(bob_q3) == 1
    assert bob_q3[0].id == "project:tri-graph"

    # Current query: only Bob is current
    current_edges = kg.get_edges(relation="leads", only_current=True)
    assert len(current_edges) == 1
    assert current_edges[0].source == "user:bob"


def test_sqlite_temporal_graph_persistence():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = Path(tmpdir) / "temporal_test.db"
        store = SQLiteGraphStore(db_file)

        store.upsert_node("doc:v1", "document", "Spec v1", content="Old spec")
        store.upsert_node("doc:v2", "document", "Spec v2", content="New spec")
        store.upsert_node("tool:mcp", "tool", "MCP Tool", content="MCP implementation")

        # Edge valid only historically
        store.add_edge(
            "doc:v1",
            "tool:mcp",
            "implements",
            valid_from="2026-01-01T00:00:00Z",
            valid_to="2026-05-01T00:00:00Z",
            is_current=False,
        )

        # Edge currently active
        store.add_edge(
            "doc:v2",
            "tool:mcp",
            "implements",
            valid_from="2026-05-01T00:00:00Z",
            valid_to=None,
            is_current=True,
        )

        # Query active in February 2026
        feb_edges = store.get_edges(as_of="2026-02-01T00:00:00Z")
        assert len(feb_edges) == 1
        assert feb_edges[0]["source"] == "doc:v1"

        # Query active in June 2026
        june_edges = store.get_edges(as_of="2026-06-01T00:00:00Z")
        assert len(june_edges) == 1
        assert june_edges[0]["source"] == "doc:v2"

        # Query only current
        current_edges = store.get_edges(only_current=True)
        assert len(current_edges) == 1
        assert current_edges[0]["source"] == "doc:v2"

        store.close()
