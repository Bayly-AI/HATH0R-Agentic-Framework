"""Unit tests for Letta-compatible memory paging tools, archival search, and sleep cycle consolidation."""

import pytest

from hath0r_engine.memory.memory_graph import MemoryGraph, MemoryNode
from hath0r_engine.memory.memory_tools import MemoryPagingManager
from hath0r_engine.memory.reflection import ReflectionEngine


def test_core_memory_append_and_replace():
    manager = MemoryPagingManager()

    # Initial state check
    persona = manager.core_memory_get("persona")
    assert "Hath0r Autonomous Agent" in persona

    # Append
    manager.core_memory_append("persona", "Specialized in distributed edge inference.")
    updated_persona = manager.core_memory_get("persona")
    assert "Specialized in distributed edge inference." in updated_persona

    # Replace
    manager.core_memory_replace(
        "persona",
        "distributed edge inference",
        "tri-graph memory systems",
    )
    final_persona = manager.core_memory_get("persona")
    assert "tri-graph memory systems" in final_persona
    assert "distributed edge inference" not in final_persona

    # Replace error handling
    with pytest.raises(ValueError, match="Target text not found"):
        manager.core_memory_replace("persona", "non-existent text", "replacement")


def test_archival_memory_insert_and_temporal_search():
    manager = MemoryPagingManager()

    # Insert historical fact
    manager.archival_memory_insert(
        content="Migrated database tables from PostgreSQL to SQLite in Q1.",
        tags=["database", "migration", "sqlite"],
        importance=0.8,
        valid_from="2026-01-01T00:00:00Z",
        valid_to="2026-03-31T23:59:59Z",
        is_current=False,
    )

    # Insert current fact
    manager.archival_memory_insert(
        content="Active database cluster operates on Turso LibSQL with WAL mode in Q3.",
        tags=["database", "turso", "libsql"],
        importance=0.9,
        valid_from="2026-07-01T00:00:00Z",
        valid_to=None,
        is_current=True,
    )

    # Search with Q1 filter
    q1_results = manager.archival_memory_search(
        query="database migration",
        as_of="2026-02-15T00:00:00Z",
    )
    assert len(q1_results) >= 1
    assert "PostgreSQL" in q1_results[0]["content"]

    # Search with current filter
    current_results = manager.archival_memory_search(
        query="database",
        only_current=True,
    )
    assert len(current_results) >= 1
    assert "Turso LibSQL" in current_results[0]["content"]


def test_memory_prune():
    manager = MemoryPagingManager()

    # High importance item (should survive)
    manager.archival_memory_insert("Critical architectural decision", importance=0.9)

    # Low importance ephemeral item (should be pruned)
    low_id = manager.archival_memory_insert("Transient debug trace", importance=0.1)
    assert low_id in manager.memory_graph.nodes

    pruned_count = manager.memory_prune(min_importance=0.3)
    assert pruned_count >= 1
    assert low_id not in manager.memory_graph.nodes


def test_sleep_cycle_consolidation():
    reflection = ReflectionEngine()
    mem_graph = MemoryGraph(graph_id="sleep-cycle-test")

    # Add related episodic memories
    for i in range(4):
        node = MemoryNode(
            id=f"ep-{i}",
            type="episode",
            label=f"Session {i}: Tool Execution",
            content=f"Agent executed tool bash and git status during debugging session {i}",
            importance=0.4,
            tags=["debugging", "git", "bash"],
        )
        mem_graph.add_node(node)

    # Add low importance transient node
    mem_graph.add_node(
        MemoryNode(
            id="ep-trash",
            type="episode",
            label="Transient noise",
            content="temporary log output",
            importance=0.05,
            tags=["noise"],
        )
    )

    result = reflection.consolidate_sleep_cycle(
        mem_graph, cluster_threshold=2, max_insights=2, prune_below_importance=0.1
    )

    assert result["insights_generated"] > 0
    assert result["pruned_nodes_count"] >= 1
    assert "ep-trash" not in mem_graph.nodes
