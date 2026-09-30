"""Tests for KnowledgeGraph hybrid BM25 and vector embedding search."""

from __future__ import annotations

from pathlib import Path

from hath0r_engine.graph.knowledge_graph import (
    BM25Index,
    KnowledgeGraph,
    KnowledgeGraphExtractor,
    KnowledgeNode,
    LightweightVectorIndex,
)


def test_bm25_index_basic() -> None:
    docs = {
        "doc1": "Hath0r CLI is the OpenSource Control Tower and operator interface.",
        "doc2": "KnowledgeGraph engine compiles repository documentation and rules.",
        "doc3": "Promotion path requires local to development to testing to staging to master.",
    }
    index = BM25Index()
    index.index_documents(docs)

    scores = index.score("Control Tower CLI")
    assert scores["doc1"] > scores["doc2"]
    assert scores["doc1"] > scores["doc3"]

    scores_promo = index.score("promotion path development master")
    assert scores_promo["doc3"] > scores_promo["doc1"]


def test_lightweight_vector_index_basic() -> None:
    docs = {
        "doc1": "autonomous agent working memory and rule enforcement",
        "doc2": "voice engine with speech recognition and synthesis",
    }
    vindex = LightweightVectorIndex(dim=64)
    vindex.index_documents(docs)

    scores = vindex.score("agent memory rules")
    assert scores["doc1"] > scores["doc2"]


def test_knowledge_graph_hybrid_search() -> None:
    kg = KnowledgeGraph()
    kg.add_node(
        KnowledgeNode(
            id="rule:cli-first",
            type="rule",
            title="Start with the CLI",
            path="docs/governance/cr-cli-entry-001.md",
            subsystem="governance",
            content="When receiving any request, agents must always start with hath0r operator CLI.",
        )
    )
    kg.add_node(
        KnowledgeNode(
            id="playbook:repo-init",
            type="playbook",
            title="Repository Initialization Playbook",
            path="docs/playbooks/init.md",
            subsystem="playbooks",
            content="Follow standard procedures to initialize a new repository with full governance.",
        )
    )
    kg.add_node(
        KnowledgeNode(
            id="concept:promotion-path",
            type="policy",
            title="Promotion Path Standard",
            path="docs/governance/promotion.md",
            subsystem="governance",
            content="Environment promotion: local -> development -> testing -> staging -> master.",
        )
    )

    # Search with hybrid balanced alpha=0.5
    results = kg.search("hath0r operator CLI", top_k=2, alpha=0.5)
    assert len(results) > 0
    assert results[0]["id"] == "rule:cli-first"
    assert "CLI" in results[0]["snippet"] or "hath0r" in results[0]["snippet"]
    assert results[0]["hybrid_score"] > 0.0

    # Search with subsystem filter
    playbook_results = kg.search("initialization", subsystem="playbooks")
    assert len(playbook_results) == 1
    assert playbook_results[0]["id"] == "playbook:repo-init"

    # Search with pure BM25 (alpha=1.0)
    bm25_results = kg.search("promotion path testing staging", alpha=1.0)
    assert len(bm25_results) > 0
    assert bm25_results[0]["id"] == "concept:promotion-path"


def test_knowledge_graph_extractor_with_content(tmp_path: Path) -> None:
    doc1 = tmp_path / "playbook.md"
    doc1.write_text(
        "---\nid: playbook:test\ntype: playbook\ntitle: Testing Playbook\n---\n# Testing Playbook\nInstructions for test harness.",
        encoding="utf-8",
    )

    kg = KnowledgeGraphExtractor.scan_directory(tmp_path)
    assert "playbook:test" in kg.nodes
    assert kg.nodes["playbook:test"].content != ""

    res = kg.search("test harness")
    assert len(res) == 1
    assert res[0]["id"] == "playbook:test"
