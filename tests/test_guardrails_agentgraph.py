"""Integration tests for AgentGraph with DynamicToolRouter and Pre-Execution Guardrails.

Verifies:
1. Zero-prompt-tax dynamic tool routing filtering by active agent role in AgentRulesGraph.
2. Pre-execution guardrails blocking invocations when:
   - Tool is unauthorized for the caller role.
   - Command / payload violates active governing rule policy constraints.
3. Successful execution when commands and tools conform to AgentGraph policies.
"""

from __future__ import annotations

import pytest

from hath0r_engine.graph import AgentRulesGraph, RulePriority
from hath0r_engine.guardrails import (
    GuardrailAction,
    GuardrailsManager,
    ToolCallDescriptor,
)
from hath0r_engine.mcp.identity import CallerIdentity
from hath0r_engine.mcp.tool_router import DynamicToolRouter


@pytest.fixture
def rules_graph() -> AgentRulesGraph:
    graph = AgentRulesGraph()
    # 1. Register reader role
    graph.register_agent_role(
        role_id="role:reader",
        role_name="Read-Only Agent",
        permitted_tools=["read_file", "search_code"],
        forbidden_tools=["run_command", "write_file"],
    )
    # 2. Register developer role inheriting standard dev tools
    graph.register_agent_role(
        role_id="role:developer",
        role_name="Developer Agent",
        permitted_tools=["read_file", "write_file", "run_command"],
    )
    # 3. Register branch policy invariant
    graph.register_rule_policy(
        rule_id="rule:branch_governance",
        title="Branch Governance Invariant",
        content="Direct pushes to master and force pushes are strictly forbidden.",
        priority=RulePriority.ORG_INVARIANT,
        governs_roles=["role:developer", "role:reader"],
        restricted_actions=["push origin master", "git push --force", "rm -rf /"],
    )
    return graph


@pytest.fixture
def tool_router() -> DynamicToolRouter:
    router = DynamicToolRouter()
    router.register_tool(
        server_id="fs",
        name="read_file",
        description="Read file contents from filesystem",
        parameters={"path": {"type": "string"}},
    )
    router.register_tool(
        server_id="fs",
        name="write_file",
        description="Write text contents to a file",
        parameters={"path": {"type": "string"}, "content": {"type": "string"}},
    )
    router.register_tool(
        server_id="fs",
        name="search_code",
        description="Search code keywords across the repository",
        parameters={"query": {"type": "string"}},
    )
    router.register_tool(
        server_id="shell",
        name="run_command",
        description="Execute a shell command",
        parameters={"command": {"type": "string"}},
    )
    return router


def test_dynamic_tool_router_agentgraph_filtering(
    rules_graph: AgentRulesGraph,
    tool_router: DynamicToolRouter,
):
    """Ensure tools not authorized for the role are pruned dynamically."""
    caller_reader = CallerIdentity(roles=["role:reader"])

    # Query for 'read file or execute command'
    routed = tool_router.route_tools(
        query="read file execute command",
        top_k=10,
        caller=caller_reader,
        agent_graph=rules_graph,
    )
    routed_names = [tool.name for tool, _ in routed]
    assert "read_file" in routed_names
    # run_command is not permitted for reader
    assert "run_command" not in routed_names
    assert "write_file" not in routed_names

    # Test LLM prompt pruning
    pruned = tool_router.get_pruned_tools_for_llm(
        query="command and write",
        top_k=5,
        caller=caller_reader,
        agent_graph=rules_graph,
    )
    pruned_names = [t["name"] for t in pruned]
    assert "run_command" not in pruned_names
    assert "write_file" not in pruned_names


def test_guardrails_blocks_unauthorized_tool(rules_graph: AgentRulesGraph):
    """Ensure GuardrailsManager blocks tool calls not permitted for role."""
    manager = GuardrailsManager(agent_graph=rules_graph)

    descriptor = ToolCallDescriptor(
        tool_name="run_command",
        arguments={"command": "ls -la"},
        caller_role="role:reader",
    )

    evaluation = manager.evaluate(descriptor)
    assert evaluation.action == GuardrailAction.BLOCK
    assert any("not authorized for role 'role:reader'" in v for v in evaluation.violations)


def test_guardrails_blocks_rule_policy_violations(rules_graph: AgentRulesGraph):
    """Ensure GuardrailsManager blocks commands violating active AgentGraph rules."""
    manager = GuardrailsManager(agent_graph=rules_graph)

    descriptor = ToolCallDescriptor(
        tool_name="run_command",
        arguments={"command": "git push origin master"},
        caller_role="role:developer",
    )

    evaluation = manager.evaluate(descriptor)
    assert evaluation.action == GuardrailAction.BLOCK
    assert any("push origin master" in v for v in evaluation.violations)


def test_guardrails_allows_safe_authorized_tool(rules_graph: AgentRulesGraph):
    """Ensure GuardrailsManager allows authorized and compliant tool calls."""
    manager = GuardrailsManager(agent_graph=rules_graph)

    descriptor = ToolCallDescriptor(
        tool_name="read_file",
        arguments={"path": "src/main.py"},
        caller_role="role:reader",
    )

    evaluation = manager.evaluate(descriptor)
    assert evaluation.action == GuardrailAction.ALLOW
    assert len(evaluation.violations) == 0
