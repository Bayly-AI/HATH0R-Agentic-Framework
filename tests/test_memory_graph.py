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
    assert (tmp_path / ".hath0r" / "memory" / "sessions" / "current.json").is_file()
    assert (tmp_path / ".hath0r" / "memory" / "sessions" / "latest.json").is_file()
    assert "rule:cr-memory-compound-001" in graph.nodes
    gate = graph.verify_compounded(repo_root=tmp_path, require_session=True)
    assert gate["compounded"] is True
    assert gate["session"]["read_verified"] is True
    assert gate["session"]["write_verified"] is True


def test_micro_memory_session_lifecycle_and_budget(tmp_path: Path) -> None:
    MemoryGraph.ensure_repo_memory(tmp_path)

    # Start session 1
    s1 = MemoryGraph.start_micro_session(tmp_path, session_id="sess-test-001", focus="Initial session")
    assert s1.read_count >= 1
    assert s1.write_count >= 1
    assert s1.byte_size() <= 2048

    # Read session 1
    s1_read = MemoryGraph.read_micro_session(tmp_path)
    assert s1_read.read_count >= 2

    # Write multiple entries to verify <2KB budget enforcement
    for idx in range(12):
        s1_write = MemoryGraph.write_micro_session(
            tmp_path,
            summary=f"Observation {idx}: verifying micro memory session capsule stays compact and bounded",
            kind="observation",
            tags=["test", "budget"],
        )
    assert s1_write.byte_size() <= 2048
    assert len(s1_write.micro_entries) <= 8

    # End session 1
    s1_end = MemoryGraph.end_micro_session(tmp_path, summary="Finished session 1", next_steps=["Start session 2"])
    assert s1_end.status == "flushed"

    # Start session 2 -> links via PRECEDES to sess-test-001
    s2 = MemoryGraph.start_micro_session(tmp_path, session_id="sess-test-002", focus="Follow-up session")
    assert s2.prior_session_id == "sess-test-001"
    graph = MemoryGraph.load_from_file(tmp_path / ".hath0r" / "memory" / "graph.json")
    assert "session:sess-test-001" in graph.nodes
    assert "session:sess-test-002" in graph.nodes
    assert any(
        e.source == "session:sess-test-001" and e.target == "session:sess-test-002" and e.relation == "PRECEDES"
        for e in graph.edges
    )


def test_file_hashing_and_cas_conflict_resolution(tmp_path: Path) -> None:
    import pytest

    from hath0r_engine.memory.memory_graph import MemoryHashConflictError

    src_file = tmp_path / "src" / "module.py"
    src_file.parent.mkdir(parents=True, exist_ok=True)
    src_file.write_text("def hello() -> str:\n    return 'v1'\n", encoding="utf-8")

    graph = MemoryGraph.ensure_repo_memory(tmp_path)
    graph_file = tmp_path / ".hath0r" / "memory" / "graph.json"
    hashes_file = tmp_path / ".hath0r" / "memory" / "hashes.json"
    assert hashes_file.is_file()

    # Compound node with tracked source_files
    graph.compound_knowledge(
        node_id="fact:module-v1",
        node_type="fact",
        label="Module V1 Implementation",
        content="Tracks src/module.py SHA-256 digest.",
        source_files=["src/module.py"],
        repo_root=tmp_path,
        run_reflection=False,
    )
    graph.save_to_file(graph_file)

    ver_ok = MemoryGraph.verify_repo_hashes(tmp_path)
    assert ver_ok["verified"] is True
    assert "src/module.py" in (graph.get_node("fact:module-v1").metadata or {}).get("source_files", {})

    # Modify tracked source file on disk -> verify_repo_hashes detects staleness
    src_file.write_text("def hello() -> str:\n    return 'v2'\n", encoding="utf-8")
    ver_stale = MemoryGraph.verify_repo_hashes(tmp_path)
    assert ver_stale["verified"] is False
    assert "src/module.py" in ver_stale["stale_source_files"]

    # Sync hashes refreshes the manifest and node source_files digest
    MemoryGraph.sync_repo_hashes(tmp_path)
    ver_synced = MemoryGraph.verify_repo_hashes(tmp_path)
    assert ver_synced["verified"] is True

    # Test deterministic CAS auto-merge across two concurrent writers adding distinct nodes
    writer_a = MemoryGraph.load_from_file(graph_file)
    writer_b = MemoryGraph.load_from_file(graph_file)

    writer_a.add_node(
        MemoryNode(
            id="episode:agent-a",
            type="episode",
            label="Agent A Work",
            content="Concurrent node A",
        )
    )
    writer_a.save_to_file(graph_file)

    writer_b.add_node(
        MemoryNode(
            id="episode:agent-b",
            type="episode",
            label="Agent B Work",
            content="Concurrent node B",
        )
    )
    writer_b.save_to_file(graph_file)

    merged = MemoryGraph.load_from_file(graph_file)
    assert "episode:agent-a" in merged.nodes
    assert "episode:agent-b" in merged.nodes

    # Test explicit expected_hash mismatch raises MemoryHashConflictError
    with pytest.raises(MemoryHashConflictError):
        merged.save_to_file(graph_file, expected_hash="sha256:0000000000000000000000000000000000000000000000000000000000000000")


def test_gitignore_unignores_graph_folders(tmp_path: Path) -> None:
    import subprocess

    subprocess.run(["git", "init", str(tmp_path)], check=True, capture_output=True)
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text(
        "# Bad rules that ignore graph folders\n"
        ".hath0r/state/\n"
        ".hath0r/memory/\n"
        ".hath0r/*.json\n",
        encoding="utf-8",
    )

    bad_check = MemoryGraph.verify_graphs_not_gitignored(tmp_path)
    assert bad_check["graphs_not_ignored"] is False
    assert len(bad_check["ignored_paths"]) > 0

    sanitize_res = MemoryGraph.ensure_gitignore_unignores_graphs(tmp_path)
    assert sanitize_res["updated"] is True
    assert ".hath0r/state/ -> .hath0r/state/*" in sanitize_res["rewritten_rules"]
    assert ".hath0r/memory/" in sanitize_res["removed_rules"]

    good_check = MemoryGraph.verify_graphs_not_gitignored(tmp_path)
    assert good_check["graphs_not_ignored"] is True
    assert good_check["ignored_paths"] == []
