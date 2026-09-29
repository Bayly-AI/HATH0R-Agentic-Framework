"""Tests verifying Tri-Graph persistence (KnowledgeGraph, ContextGraph, MemoryGraph)
and governance document ingestion (playbooks, runbooks, policies, procedures, strategies).
"""

from pathlib import Path
from lib.graph.knowledge_graph import KnowledgeGraph, KnowledgeNode, KnowledgeEdge
from lib.context.context_graph import ContextGraph, ContextNode, ContextEdge
from lib.memory.memory_graph import MemoryGraph, MemoryNode, MemoryEdge


def test_tri_graph_persistence_and_roundtrip(tmp_path: Path) -> None:
    # 1. Test KnowledgeGraph Persistence
    kg = KnowledgeGraph()
    kg.add_node(KnowledgeNode(id="doc:playbook-coding", type="playbook", title="Coding Playbook", path="docs/governance/playbooks/playbook-coding.md"))
    kg.add_node(KnowledgeNode(id="rule:cr-cli-entry-001", type="policy", title="CLI Entry Gate", path="docs/governance/rules/cr-cli-entry-001.md"))
    kg.add_edge(KnowledgeEdge(source="doc:playbook-coding", target="rule:cr-cli-entry-001", relation="governed_by"))

    kg_file = tmp_path / "knowledge_graph.json"
    kg.save_to_file(kg_file)
    assert kg_file.exists()

    loaded_kg = KnowledgeGraph.load_from_file(kg_file)
    assert len(loaded_kg.nodes) == 2
    assert len(loaded_kg.edges) == 1
    assert loaded_kg.nodes["doc:playbook-coding"].title == "Coding Playbook"

    # 2. Test ContextGraph Persistence
    cg = ContextGraph(session_id="test-session-123")
    subagent_node = cg.register_subagent(subagent_id="subagent-42", label="Code Reviewer")
    tool_id = cg.record_tool_execution(tool_name="view_file", caller_id=subagent_node.id, jev_status="approved")

    cg_file = tmp_path / "context_graph.json"
    cg.save_to_file(cg_file)
    assert cg_file.exists()

    loaded_cg = ContextGraph.load_from_file(cg_file)
    assert loaded_cg.session_id == "test-session-123"
    assert len(loaded_cg.nodes) >= 2
    assert any(n.label == "Code Reviewer" for n in loaded_cg.nodes.values())

    # 3. Test MemoryGraph Persistence
    mg = MemoryGraph(graph_id="workspace-memory")
    mg.add_node(MemoryNode(id="rule:cli-first", type="rule", label="Start With CLI", content="Always use CLI first."))
    mg.add_node(MemoryNode(id="concept:tri-graph", type="concept", label="Tri-Graph Substrate", content="KG, CG, MG."))
    mg.add_edge(MemoryEdge(source="rule:cli-first", target="concept:tri-graph", relation="ENFORCES"))

    mg_file = tmp_path / "memory_graph.json"
    mg.save_to_file(mg_file)
    assert mg_file.exists()

    loaded_mg = MemoryGraph.load_from_file(mg_file)
    assert loaded_mg.graph_id == "workspace-memory"
    assert len(loaded_mg.nodes) == 2
    assert len(loaded_mg.edges) == 1


def test_memory_graph_governance_docs_ingestion(tmp_path: Path) -> None:
    # Point at the live framework docs directory relative to repo root
    framework_docs = Path(__file__).resolve().parents[1] / "docs"
    mg = MemoryGraph(graph_id="hathor-framework-governance-memory")

    count = mg.ingest_markdown_documents(framework_docs)
    assert count > 0, "Should ingest markdown documents from docs/"

    # Verify playbooks, rules, and procedures are ingested
    rules = mg.find_nodes(node_type="rule")
    concepts = mg.find_nodes(node_type="concept")
    assert len(rules) > 0, "Should have extracted rule nodes"
    assert len(concepts) > 0, "Should have extracted concept / playbook nodes"

    # Verify specific key documents exist in memory
    coding_playbook_nodes = [n for n in mg.nodes.values() if "coding" in n.id.lower() or "coding" in n.label.lower()]
    assert len(coding_playbook_nodes) > 0

    # Test persistence of ingested memory graph
    memory_save_path = tmp_path / ".hath0r" / "memory" / "graph.json"
    mg.save_to_file(memory_save_path)
    assert memory_save_path.exists()

    reloaded = MemoryGraph.load_from_file(memory_save_path)
    assert len(reloaded.nodes) == count
