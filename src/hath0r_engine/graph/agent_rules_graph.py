"""AgentRulesGraph: First-class Rule and Role Governance Substrate.

Provides deterministic inheritance DAG traversal, cycle detection,
role-based tool authorization (RBAC/ABAC), and conflict resolution across
governance policies.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from hath0r_engine.graph.agent_graph import (
    AgentGraphEngine,
    AgentGraphNode,
    AgentGraphPlane,
    AgentGraphValidationReport,
    ResolvedRuleSet,
    RulePriority,
)


class AgentRulesGraph:
    """Dedicated Rules & Governance cognitive substrate plane.

    Enforces deterministic rule evaluation, hierarchical inheritance (Org -> Repo -> Subsystem -> Role),
    zero-prompt-tax tool authorization, and constraint checking.
    """

    def __init__(self, engine: Optional[AgentGraphEngine] = None, graph_id: str = "agent-rules-graph") -> None:
        self.engine = engine or AgentGraphEngine(graph_id=graph_id)

    @property
    def nodes(self) -> Dict[str, AgentGraphNode]:
        """Return all nodes belonging to the rules plane."""
        return {
            nid: n for nid, n in self.engine.nodes.items()
            if n.plane == AgentGraphPlane.RULES.value
        }

    def register_agent_role(
        self,
        role_id: str,
        role_name: str,
        scope: str = "root",
        permitted_tools: Optional[List[str]] = None,
        forbidden_tools: Optional[List[str]] = None,
        parent_role_id: Optional[str] = None,
        max_subagents: int = 4,
        allowed_child_roles: Optional[List[str]] = None,
        properties: Optional[Dict[str, Any]] = None,
    ) -> AgentGraphNode:
        """Register a strongly-typed AgentRoleNode in the graph."""
        props = properties or {}
        props.update({
            "role_name": role_name,
            "scope": scope,
            "permitted_tools": permitted_tools or [],
            "forbidden_tools": forbidden_tools or [],
            "max_subagents": max_subagents,
            "allowed_child_roles": allowed_child_roles or [],
        })
        node = self.engine.register_agent_role(
            role_id=role_id,
            role_name=role_name,
            scope=scope,
            permitted_tools=permitted_tools,
            forbidden_tools=forbidden_tools,
            parent_role_id=parent_role_id,
        )
        node.properties.update(props)
        return node

    def register_rule_policy(
        self,
        rule_id: str,
        title: str,
        content: str,
        priority: RulePriority = RulePriority.REPO_STANDARD,
        target_scope: str = "root",
        governs_roles: Optional[List[str]] = None,
        restricted_actions: Optional[List[str]] = None,
        allowed_actions: Optional[List[str]] = None,
        supersedes_rule_id: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
    ) -> AgentGraphNode:
        """Register a strongly-typed RuleNode / rule_policy in the graph."""
        node = self.engine.register_rule_policy(
            rule_id=rule_id,
            title=title,
            content=content,
            priority=priority,
            target_scope=target_scope,
            governs_roles=governs_roles,
            restricted_actions=restricted_actions,
            allowed_actions=allowed_actions,
            supersedes_rule_id=supersedes_rule_id,
        )
        if properties:
            node.properties.update(properties)
        return node

    def resolve_rules(
        self,
        role_id: str,
        scope: Optional[str] = None,
        as_of: Optional[str] = None,
        only_current: bool = True,
    ) -> ResolvedRuleSet:
        """Deterministically compute active rule policies, constraints, and tool authorizations for a role."""
        return self.engine.resolve_agent_rules(
            role_id=role_id,
            scope=scope,
            as_of=as_of,
            only_current=only_current,
        )

    def get_authorized_tools(
        self,
        role_id: str,
        scope: Optional[str] = None,
    ) -> Set[str]:
        """Return the exact set of authorized tool names for an agent role after inheritance and pruning."""
        resolved = self.resolve_rules(role_id=role_id, scope=scope)
        return set(resolved.authorized_tools)

    def is_action_allowed(
        self,
        role_id: str,
        action: str,
        scope: Optional[str] = None,
    ) -> bool:
        """Verify whether an action is permitted under the active rule constraints for a role."""
        resolved = self.resolve_rules(role_id=role_id, scope=scope)
        # If explicitly restricted by precedence, deny
        if action in resolved.restricted_actions:
            return False
        # If explicitly allowed or no restrictions apply
        return True

    def validate_rules(self) -> AgentGraphValidationReport:
        """Audit the rules graph for dangling relations, cycles, and precedence conflicts."""
        return self.engine.validate_integrity()

    def export_rules(self, path: Path) -> None:
        """Serialize rules plane to JSON."""
        self.engine.export_snapshot(path)

    def import_rules(self, path: Path) -> None:
        """Load rules plane from JSON snapshot."""
        self.engine.import_snapshot(path)
