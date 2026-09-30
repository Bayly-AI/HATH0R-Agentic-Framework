"""Unit and integration tests for SQLiteGraphStore vector and property graph engine."""

import tempfile
from pathlib import Path

from hath0r_engine.graph.knowledge_graph import KnowledgeEdge, KnowledgeGraph, KnowledgeNode
from hath0r_engine.graph.sqlite_graph import (
    SQLiteGraphStore,
    _cosine_similarity,
    _deserialize_vector,
    _serialize_vector,
)
from hath0r_engine.memory.memory_graph import MemoryEdge, MemoryGraph, MemoryNode


def test_vector_serialization():
    vec = [0.1, 0.2, 0.3, -0.4, 0.5]
    blob = _serialize_vector(vec)
    assert isinstance(blob, bytes)
    deserialized = _deserialize_vector(blob)
    assert len(deserialized) == len(vec)
    for v1, v2 in zip(vec, deserialized):
        assert abs(v1 - v2) < 1e-6


def test_cosine_similarity():
    v1 = [1.0, 0.0, 0.0]
    v2 = [1.0, 0.0, 0.0]
    assert abs(_cosine_similarity(v1, v2) - 1.0) < 1e-6

    v3 = [0.0, 1.0, 0.0]
    assert abs(_cosine_similarity(v1, v3) - 0.0) < 1e-6

    v4 = [0.5, 0.5, 0.0]
    sim = _cosine_similarity(v1, v4)
    assert 0.70 < sim < 0.72


def test_sqlite_graph_store_crud():
    store = SQLiteGraphStore(":memory:")

    store.upsert_node(
        node_id="doc:adr-001",
        node_type="document",
        title="ADR 001 Architecture",
        content="This document describes the Hath0r tri-graph cognitive substrate.",
        subsystem="engine",
        tags=["architecture", "graph"],
        properties={"author": "ray"},
        embedding=[0.8, 0.2, 0.1],
    )

    store.upsert_node(
        node_id="doc:adr-002",
        node_type="document",
        title="ADR 002 JEV System",
        content="Describes JEV System One fast tool guard decisions and policies.",
        subsystem="jev",
        tags=["safety", "jev"],
        properties={"author": "ray"},
        embedding=[0.1, 0.9, 0.2],
    )

    assert store.count_nodes() == 2

    node = store.get_node("doc:adr-001")
    assert node is not None
    assert node["title"] == "ADR 001 Architecture"
    assert node["tags"] == ["architecture", "graph"]
    assert node["properties"]["author"] == "ray"
    assert len(node["embedding"]) == 3

    store.add_edge("doc:adr-001", "doc:adr-002", "references", weight=1.5)
    assert store.count_edges() == 1

    edges = store.get_edges(source="doc:adr-001")
    assert len(edges) == 1
    assert edges[0]["target"] == "doc:adr-002"
    assert edges[0]["weight"] == 1.5

    # Delete
    deleted = store.delete_node("doc:adr-002")
    assert deleted is True
    assert store.count_nodes() == 1
    assert store.count_edges() == 0

    store.close()


def test_sqlite_graph_vector_and_fts_search():
    store = SQLiteGraphStore(":memory:")

    store.upsert_node(
        node_id="n1",
        node_type="rule",
        title="CLI First Entry Gate",
        content="Always start with the Hath0r operator CLI before executing ad-hoc actions.",
        embedding=[1.0, 0.0, 0.0],
    )

    store.upsert_node(
        node_id="n2",
        node_type="rule",
        title="Branch Promotion Policy",
        content="Promote branches sequentially across local development testing staging and master.",
        embedding=[0.0, 1.0, 0.0],
    )

    store.upsert_node(
        node_id="n3",
        node_type="rule",
        title="Knowledgebase Hub",
        content="Store all shared architectural knowledge in canonical group hub.",
        embedding=[0.0, 0.0, 1.0],
    )

    # FTS search
    fts_res = store.search_fts("operator CLI")
    assert len(fts_res) >= 1
    assert fts_res[0]["id"] == "n1"

    # Vector similarity search
    vec_res = store.search_vector([0.9, 0.1, 0.0], top_k=2)
    assert len(vec_res) == 2
    assert vec_res[0][0]["id"] == "n1"
    assert vec_res[0][1] > 0.9

    # Hybrid search
    hybrid_res = store.search_hybrid("promotion policy", query_embedding=[0.1, 0.9, 0.0], alpha=0.5)
    assert len(hybrid_res) >= 1
    assert hybrid_res[0]["id"] == "n2"
    assert "hybrid_score" in hybrid_res[0]

    store.close()


def test_knowledge_graph_sqlite_sync():
    kg = KnowledgeGraph()
    kg.add_node(
        KnowledgeNode(
            id="doc:1", type="procedure", title="Setup Guide", path="docs/setup.md", content="Install dependencies."
        )
    )
    kg.add_node(
        KnowledgeNode(
            id="doc:2",
            type="playbook",
            title="Deploy Runbook",
            path="docs/deploy.md",
            content="Execute deploy pipeline.",
        )
    )
    kg.add_edge(KnowledgeEdge(source="doc:1", target="doc:2", relation="depends_on"))

    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = Path(tmpdir) / "test_knowledge.db"
        store = kg.to_sqlite(db_file)
        assert store.count_nodes(graph_type="knowledge") == 2
        assert store.count_edges(graph_type="knowledge") == 1
        store.close()

        loaded_kg = KnowledgeGraph.load_from_sqlite(db_file)
        assert len(loaded_kg.nodes) == 2
        assert "doc:1" in loaded_kg.nodes
        assert loaded_kg.nodes["doc:1"].title == "Setup Guide"
        assert len(loaded_kg.edges) == 1
        assert loaded_kg.edges[0].relation == "depends_on"


def test_memory_graph_sqlite_sync():
    mem = MemoryGraph(graph_id="agent-workspace-memory")
    mem.add_node(
        MemoryNode(
            id="mem:1",
            type="decision",
            label="Adopt SQLite Store",
            content="Use embedded SQLite for ACID property graph.",
        )
    )
    mem.add_node(
        MemoryNode(
            id="mem:2", type="episode", label="Task Execution 1", content="Executed migration of KnowledgeGraph."
        )
    )
    mem.add_edge(MemoryEdge(source="mem:1", target="mem:2", relation="RELATES_TO"))

    with tempfile.TemporaryDirectory() as tmpdir:
        db_file = Path(tmpdir) / "test_memory.db"
        store = mem.to_sqlite(db_file)
        assert store.count_nodes(graph_type="memory") == 2
        assert store.count_edges(graph_type="memory") == 1
        store.close()

        loaded_mem = MemoryGraph.load_from_sqlite(db_file, graph_id="agent-workspace-memory")
        assert len(loaded_mem.nodes) == 2
        assert "mem:1" in loaded_mem.nodes
        assert loaded_mem.nodes["mem:1"].label == "Adopt SQLite Store"
        assert len(loaded_mem.edges) == 1
        assert loaded_mem.edges[0].relation == "RELATES_TO"
