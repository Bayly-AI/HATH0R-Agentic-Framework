"""Unit tests for ReflectionEngine in hath0r_engine.memory.reflection."""

from datetime import datetime, timedelta, timezone

from hath0r_engine.graph.knowledge_graph import KnowledgeGraph
from hath0r_engine.memory.memory_graph import MemoryGraph, MemoryNode
from hath0r_engine.memory.reflection import ReflectionEngine


def test_recency_scoring():
    engine = ReflectionEngine(decay_rate_per_hour=0.1)
    now = datetime.now(timezone.utc)

    # 0 hours elapsed
    s0 = engine.score_recency(now.isoformat(), reference_time=now)
    assert abs(s0 - 1.0) < 1e-4

    # 10 hours elapsed: e^(-0.1 * 10) = e^(-1) ≈ 0.3678
    t10 = (now - timedelta(hours=10)).isoformat()
    s10 = engine.score_recency(t10, reference_time=now)
    assert 0.35 < s10 < 0.38

    # 50 hours elapsed: e^(-5) ≈ 0.0067
    t50 = (now - timedelta(hours=50)).isoformat()
    s50 = engine.score_recency(t50, reference_time=now)
    assert s50 < 0.02


def test_relevance_scoring_and_ranking():
    engine = ReflectionEngine()
    graph = MemoryGraph()

    now = datetime.now(timezone.utc)
    n1 = MemoryNode(
        id="mem:1",
        type="rule",
        label="CLI Operator Rule",
        content="Always start with the hath0r CLI entrypoint.",
        importance=0.9,
        tags=["cli", "governance"],
        created_at=now.isoformat(),
    )
    n2 = MemoryNode(
        id="mem:2",
        type="episode",
        label="Old Bugfix Episode",
        content="Fixed memory leak in old socket connection.",
        importance=0.2,
        tags=["bugfix"],
        created_at=(now - timedelta(days=10)).isoformat(),
    )
    graph.add_node(n1)
    graph.add_node(n2)

    ranked = engine.rank_memories(graph, query="hath0r CLI", top_k=2)
    assert len(ranked) == 2
    assert ranked[0][0].id == "mem:1"
    assert ranked[0][1]["composite"] > ranked[1][1]["composite"]


def test_synthesize_reflections_and_promotion():
    engine = ReflectionEngine()
    mem_graph = MemoryGraph()

    now = datetime.now(timezone.utc)
    # Add multiple episodes sharing the 'deployment' tag
    for i in range(3):
        mem_graph.add_node(
            MemoryNode(
                id=f"ep:deploy-{i}",
                type="episode",
                label=f"Deployment Phase {i}",
                content=f"Executed stage {i} promotion through staging and master pipelines.",
                importance=0.6,
                tags=["deployment", "ci"],
                created_at=(now - timedelta(hours=i)).isoformat(),
            )
        )

    insights = engine.synthesize_reflections(mem_graph, cluster_threshold=2)
    assert len(insights) >= 1
    insight = insights[0]
    assert insight.type == "insight"
    assert "deployment" in insight.tags
    assert insight.importance > 0.6
    assert insight.id in mem_graph.nodes

    # Check DERIVES_FROM edges
    derives_edges = [e for e in mem_graph.edges if e.source == insight.id and e.relation == "DERIVES_FROM"]
    assert len(derives_edges) >= 2

    # Promote to KnowledgeGraph
    kg = KnowledgeGraph()
    promoted = engine.promote_to_knowledge(mem_graph, kg, min_importance=0.5)
    assert len(promoted) >= 1
    assert any(p.id == f"promoted:{insight.id}" for p in promoted)
    assert f"promoted:{insight.id}" in kg.nodes
