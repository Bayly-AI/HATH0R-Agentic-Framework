"""Unit and integration tests for AgentGraph Unified Quad-Graph Substrate.

Verifies:
  1. Quad-plane node/edge population.
  2. Deterministic rule inheritance and precedence resolution.
  3. Tool authorization (RBAC) and forbidden tool pruning.
  4. Cycle detection and conflict errors.
  5. Bitemporal edge and node validity intervals.
  6. Pluggable file/modality adapters (Markdown & AST).
  7. Cross-plane hybrid BM25 retrieval.
  8. Graph integrity auditing.
  9. Snapshot serialization roundtrip.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from hath0r_engine.graph.agent_graph import (
    AgentGraphEngine,
    AgentGraphNode,
    AgentGraphPlane,
    RuleConflictError,
    RuleCycleError,
    RulePriority,
)


def test_agent_graph_initialization():
    engine = AgentGraphEngine(graph_id="test-agentgraph")
    assert engine.graph_id == "test-agentgraph"
    assert engine.schema_version == "hath0r.agentgraph/1"
    assert len(engine.nodes) == 0
    assert len(engine.edges) == 0


def test_agent_graph_quad_plane_nodes():
    engine = AgentGraphEngine()

    # 1. Knowledge plane
    n_k = AgentGraphNode(
        id="doc:architecture",
        plane=AgentGraphPlane.KNOWLEDGE.value,
        type="document",
        label="Architecture Spec",
        content="Overview of AgentGraph substrate.",
    )
    # 2. Context plane
    n_c = AgentGraphNode(
        id="agent:subagent-1",
        plane=AgentGraphPlane.CONTEXT.value,
        type="subagent",
        label="Research Subagent",
    )
    # 3. Memory plane
    n_m = AgentGraphNode(
        id="concept:taguchi",
        plane=AgentGraphPlane.MEMORY.value,
        type="concept",
        label="Taguchi Methods",
        content="Robust parameter optimization.",
    )
    # 4. Rules plane
    n_r = AgentGraphNode(
        id="rule:cli-entry",
        plane=AgentGraphPlane.RULES.value,
        type="rule_policy",
        label="CR-CLI-ENTRY-001",
        content="Always start with the CLI.",
        properties={"priority": int(RulePriority.ORG_INVARIANT)},
    )

    engine.add_node(n_k)
    engine.add_node(n_c)
    engine.add_node(n_m)
    engine.add_node(n_r)

    assert len(engine.nodes) == 4
    report = engine.validate_integrity()
    assert report.total_nodes == 4
    assert report.plane_counts["knowledge"] == 1
    assert report.plane_counts["context"] == 1
    assert report.plane_counts["memory"] == 1
    assert report.plane_counts["rules"] == 1


def test_deterministic_rule_inheritance_and_rbac():
    engine = AgentGraphEngine()

    # Register parent role: base_developer
    engine.register_agent_role(
        role_id="role:base_developer",
        role_name="Base Developer",
        permitted_tools=["view_file", "search_web"],
        forbidden_tools=["force_push"],
    )

    # Register child role: framework_architect inheriting from base_developer
    engine.register_agent_role(
        role_id="role:framework_architect",
        role_name="Framework Architect",
        permitted_tools=["write_to_file", "generate_diagram"],
        parent_role_id="role:base_developer",
    )

    # Register org invariant rule
    engine.register_rule_policy(
        rule_id="rule:org_cli_first",
        title="CR-CLI-ENTRY-001",
        content="Always start with hath0r operator CLI.",
        priority=RulePriority.ORG_INVARIANT,
        restricted_actions=["direct_ad_hoc_script"],
        governs_roles=["role:base_developer"],
    )

    # Register subsystem rule overriding an allowance
    engine.register_rule_policy(
        rule_id="rule:engine_strict_ast",
        title="Engine Syntax Gate",
        content="Require AST parsing before code execution.",
        priority=RulePriority.SUBSYSTEM_RULE,
        allowed_actions=["ast_inspection"],
        governs_roles=["role:framework_architect"],
    )

    # Resolve rules for framework_architect
    resolved = engine.resolve_agent_rules("role:framework_architect")

    assert resolved.role_id == "role:framework_architect"
    assert "role:framework_architect" in resolved.lineage_path
    assert "role:base_developer" in resolved.lineage_path

    # Permitted tools inherited from parent + child
    assert "view_file" in resolved.authorized_tools
    assert "search_web" in resolved.authorized_tools
    assert "write_to_file" in resolved.authorized_tools
    assert "generate_diagram" in resolved.authorized_tools
    assert "force_push" not in resolved.authorized_tools  # was forbidden

    # Actions resolved
    assert "direct_ad_hoc_script" in resolved.restricted_actions
    assert "ast_inspection" in resolved.allowed_actions
    assert "CR-CLI-ENTRY-001" in resolved.governing_invariants


def test_rule_inheritance_cycle_detection():
    engine = AgentGraphEngine()

    engine.register_agent_role(role_id="role:A", role_name="Role A", parent_role_id="role:B")
    engine.register_agent_role(role_id="role:B", role_name="Role B", parent_role_id="role:C")
    engine.register_agent_role(role_id="role:C", role_name="Role C", parent_role_id="role:A")

    with pytest.raises(RuleCycleError) as exc_info:
        engine.resolve_agent_rules("role:A")

    assert "Cycle detected" in str(exc_info.value)


def test_rule_conflict_error_at_equal_priority():
    engine = AgentGraphEngine()

    engine.register_agent_role(role_id="role:coder", role_name="Coder")

    # Rule 1 allows action at REPO_STANDARD
    engine.register_rule_policy(
        rule_id="rule:allow_eval",
        title="Allow Eval",
        content="Permit eval execution.",
        priority=RulePriority.REPO_STANDARD,
        allowed_actions=["dynamic_eval"],
        governs_roles=["role:coder"],
    )

    # Rule 2 restricts action at SAME priority REPO_STANDARD
    engine.register_rule_policy(
        rule_id="rule:block_eval",
        title="Block Eval",
        content="Forbid eval execution.",
        priority=RulePriority.REPO_STANDARD,
        restricted_actions=["dynamic_eval"],
        governs_roles=["role:coder"],
    )

    with pytest.raises(RuleConflictError) as exc_info:
        engine.resolve_agent_rules("role:coder")

    assert "Rule conflict detected" in str(exc_info.value)
    assert "dynamic_eval" in str(exc_info.value)


def test_bitemporal_validity_intervals():
    engine = AgentGraphEngine()

    # Register rule valid only in past
    engine.add_node(
        AgentGraphNode(
            id="rule:legacy-001",
            plane=AgentGraphPlane.RULES.value,
            type="rule_policy",
            label="Legacy Rule",
            valid_from="2025-01-01T00:00:00Z",
            valid_to="2025-12-31T23:59:59Z",
            is_current=False,
        )
    )

    # Register current rule
    engine.add_node(
        AgentGraphNode(
            id="rule:current-002",
            plane=AgentGraphPlane.RULES.value,
            type="rule_policy",
            label="Current Rule",
            valid_from="2026-01-01T00:00:00Z",
            valid_to=None,
            is_current=True,
        )
    )

    # Query with only_current=True
    current_node = engine.get_node("rule:current-002")
    legacy_node = engine.get_node("rule:legacy-001")
    assert current_node.is_valid_at(only_current=True) is True
    assert legacy_node.is_valid_at(only_current=True) is False

    # Historical query at 2025-06-01
    assert legacy_node.is_valid_at(as_of="2025-06-01T00:00:00Z", only_current=False) is True
    assert current_node.is_valid_at(as_of="2025-06-01T00:00:00Z", only_current=False) is False


def test_pluggable_adapters(tmp_path: Path):
    engine = AgentGraphEngine()

    # Create dummy markdown document
    md_file = tmp_path / "spec.md"
    md_file.write_text("# Agent Design Guide\nDetails on subagents and [link](other.md).", encoding="utf-8")

    # Create dummy python file
    py_file = tmp_path / "models.py"
    py_file.write_text('class UserModel:\n    """User entity."""\n    pass\n\ndef get_user():\n    pass\n', encoding="utf-8")

    count = engine.ingest_path(tmp_path)
    assert count >= 3  # 1 doc, 1 module, 1 class, 1 func

    # Check ingested nodes
    assert engine.get_node("doc:spec.md") is not None
    assert engine.get_node("class:models.UserModel") is not None
    assert engine.get_node("func:models.get_user") is not None


def test_hybrid_bm25_retrieval():
    engine = AgentGraphEngine()

    engine.add_node(
        AgentGraphNode(
            id="doc:opt",
            plane=AgentGraphPlane.KNOWLEDGE.value,
            type="strategy",
            label="Taguchi Robust Design",
            content="Orthogonal Array Testing and Signal-to-Noise Ratio tuning.",
        )
    )
    engine.add_node(
        AgentGraphNode(
            id="doc:gov",
            plane=AgentGraphPlane.RULES.value,
            type="rule_policy",
            label="Branch Promotion Policy",
            content="Strict lifecycle from development to testing to staging to master.",
        )
    )

    results = engine.query_hybrid("Taguchi Signal-to-Noise")
    assert len(results) > 0
    assert results[0].node.id == "doc:opt"
    assert "taguchi" in [h.lower() for h in results[0].highlights]

    gov_results = engine.query_hybrid("Promotion staging master", planes=[AgentGraphPlane.RULES.value])
    assert len(gov_results) > 0
    assert gov_results[0].node.id == "doc:gov"


def test_snapshot_roundtrip_persistence(tmp_path: Path):
    engine = AgentGraphEngine(graph_id="persistence-space")
    engine.register_agent_role(
        role_id="role:tester",
        role_name="QA Bot",
        permitted_tools=["pytest_runner"],
    )
    engine.register_rule_policy(
        rule_id="rule:test_pass",
        title="100% Pass Invariant",
        content="All unit tests must pass before opening PR.",
        priority=RulePriority.ORG_INVARIANT,
        governs_roles=["role:tester"],
    )

    snapshot_file = tmp_path / "agentgraph_snapshot.json"
    engine.export_snapshot(snapshot_file)
    assert snapshot_file.exists()

    # Re-import into a clean engine
    new_engine = AgentGraphEngine(graph_id="persistence-space")
    new_engine.import_snapshot(snapshot_file)

    resolved = new_engine.resolve_agent_rules("role:tester")
    assert "pytest_runner" in resolved.authorized_tools
    assert "100% Pass Invariant" in resolved.governing_invariants


def test_agent_rules_graph_substrate():
    from hath0r_engine.graph import AgentRulesGraph

    arg = AgentRulesGraph()
    arg.register_agent_role(
        role_id="role:curator",
        role_name="Curator Bot",
        scope="contracts",
        permitted_tools=["view_file", "write_to_file"],
        forbidden_tools=["git_push"],
    )
    arg.register_rule_policy(
        rule_id="rule:branch_rules",
        title="Branch Governance Rule",
        content="Must branch from development only.",
        priority=RulePriority.REPO_STANDARD,
        governs_roles=["role:curator"],
        restricted_actions=["git_push_master"],
        allowed_actions=["git_push_feature"],
    )

    resolved = arg.resolve_rules("role:curator")
    assert "view_file" in resolved.authorized_tools
    assert "write_to_file" in resolved.authorized_tools
    assert "git_push" not in resolved.authorized_tools
    assert "git_push_master" in resolved.restricted_actions

    tools = arg.get_authorized_tools("role:curator")
    assert tools == {"view_file", "write_to_file"}
    assert arg.is_action_allowed("role:curator", "git_push_feature") is True
    assert arg.is_action_allowed("role:curator", "git_push_master") is False

    report = arg.validate_rules()
    assert report.is_valid is True


def test_sqlite_roundtrip_persistence(tmp_path: Path):
    db_file = tmp_path / "agentgraph_test.db"

    engine = AgentGraphEngine(graph_id="sqlite-space")
    engine.register_agent_role(
        role_id="role:architect",
        role_name="System Architect",
        permitted_tools=["adr_author", "graph_query"],
    )
    engine.register_rule_policy(
        rule_id="rule:adr_standard",
        title="ADR Standard Invariant",
        content="All architecture shifts require ratified ADRs.",
        priority=RulePriority.ORG_INVARIANT,
        governs_roles=["role:architect"],
    )

    engine.persist_sqlite(db_file)
    assert db_file.exists()

    new_engine = AgentGraphEngine(graph_id="sqlite-space")
    new_engine.load_sqlite(db_file)

    assert len(new_engine.nodes) == 2  # role + rule
    assert len(new_engine.edges) == 3  # 2 AUTHORIZES_TOOL edges + 1 GOVERNS edge
    resolved = new_engine.resolve_agent_rules("role:architect")
    assert "adr_author" in resolved.authorized_tools
    assert "ADR Standard Invariant" in resolved.governing_invariants


def test_standard_roles_and_frontmatter_rule_policies():
    from hath0r_engine.graph.agent_rules_graph import AgentRulesGraph

    arg = AgentRulesGraph()
    roles = arg.initialize_standard_roles()
    assert len(roles) == 6

    # Verify developer inherits from reader
    dev_tools = arg.get_authorized_tools("role:developer")
    assert "view_file" in dev_tools
    assert "write_to_file" in dev_tools
    assert "direct_push_master" not in dev_tools

    # Test ingesting frontmatter governance rules
    engine = arg.engine
    engine.ingest_path(Path("docs/governance/rules"))
    engine.ingest_path(Path("contracts/rules.md"))
    engine.ingest_path(Path("archive/rules.md"))

    rule_nodes = [n for n in engine.nodes.values() if n.plane == "rules" and n.type == "rule_policy"]
    rule_ids = {r.id for r in rule_nodes}

    assert "rule:cr-substrate-001" in rule_ids
    assert "rule:cr-branch-gov-001" in rule_ids
    assert "rule:cr-hath0r-root-001" in rule_ids
    assert "rule:cr-hath0r-init-001" in rule_ids
    assert "rule:cr-kb-tower-001" in rule_ids
    assert "rule:subsystem-contracts" in rule_ids
    assert "rule:subsystem-archive" in rule_ids


