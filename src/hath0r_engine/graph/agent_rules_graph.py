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


ROLE_READER = "role:reader"
ROLE_RESEARCHER = "role:researcher"
ROLE_DEVELOPER = "role:developer"
ROLE_QA = "role:qa-engineer"
ROLE_ARCHITECT = "role:architect"
ROLE_RELEASE = "role:release-manager"


class AgentRulesGraph:
    """Dedicated Rules & Governance cognitive substrate plane.

    Enforces deterministic rule evaluation, hierarchical inheritance (Org -> Repo -> Subsystem -> Role),
    zero-prompt-tax tool authorization, and constraint checking.
    """

    def __init__(self, engine: Optional[AgentGraphEngine] = None, graph_id: str = "agent-rules-graph") -> None:
        self.engine = engine or AgentGraphEngine(graph_id=graph_id)

    def initialize_standard_roles(self) -> List[AgentGraphNode]:
        """Register canonical Hath0r agent role hierarchy and tool RBAC manifests."""
        reader = self.register_agent_role(
            role_id=ROLE_READER,
            role_name="Read-Only Agent",
            scope="root",
            permitted_tools=["view_file", "search_code", "search_web", "read_url_content"],
            forbidden_tools=["direct_push_master"],
        )
        researcher = self.register_agent_role(
            role_id=ROLE_RESEARCHER,
            role_name="Codebase & KB Researcher",
            scope="root",
            permitted_tools=["hath0r_kb_search", "hath0r_memory_search", "view_file", "search_code", "search_web"],
            forbidden_tools=["write_to_file", "replace_file_content", "run_command"],
            parent_role_id=ROLE_READER,
        )
        developer = self.register_agent_role(
            role_id=ROLE_DEVELOPER,
            role_name="Developer Agent",
            scope="root",
            permitted_tools=["view_file", "search_code", "write_to_file", "replace_file_content", "run_command", "hath0r_branch_validate"],
            forbidden_tools=["direct_push_master", "direct_push_staging"],
            parent_role_id=ROLE_READER,
        )
        qa = self.register_agent_role(
            role_id=ROLE_QA,
            role_name="QA & UI Test Engineer",
            scope="root",
            permitted_tools=["run_playwright_test", "audit_master_catalog", "view_file", "run_command", "write_to_file"],
            forbidden_tools=["direct_push_master"],
            parent_role_id=ROLE_DEVELOPER,
        )
        architect = self.register_agent_role(
            role_id=ROLE_ARCHITECT,
            role_name="System & Contract Architect",
            scope="root",
            permitted_tools=["validate_contracts", "generate_image", "hath0r_agentgraph_validate", "write_to_file", "view_file", "run_command"],
            forbidden_tools=["direct_push_master"],
            parent_role_id=ROLE_DEVELOPER,
        )
        release = self.register_agent_role(
            role_id=ROLE_RELEASE,
            role_name="Release & Governance Manager",
            scope="root",
            permitted_tools=["validate_promotion_path", "update_version", "compile_changelog", "run_command", "view_file"],
            forbidden_tools=["non_linear_promotion"],
            parent_role_id=ROLE_DEVELOPER,
        )
        return [reader, researcher, developer, qa, architect, release]

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
