"""Deterministic Pre-Execution Guardrails Orchestrator."""

from __future__ import annotations

from typing import Any, List, Optional

from hath0r_engine.guardrails.ast_validator import SyntaxGuardrail
from hath0r_engine.guardrails.escalation import HumanEscalationAuditHook
from hath0r_engine.guardrails.models import (
    GuardrailAction,
    GuardrailEvaluation,
    ToolCallDescriptor,
)
from hath0r_engine.guardrails.schema_repair import SchemaRepairEngine


class GuardrailsManager:
    """Pre-execution guardrails engine evaluating tool payloads before sandbox dispatch."""

    def __init__(
        self,
        syntax_validator: Optional[SyntaxGuardrail] = None,
        schema_repair: Optional[SchemaRepairEngine] = None,
        escalation_hook: Optional[HumanEscalationAuditHook] = None,
        agent_graph: Optional[Any] = None,
        auto_repair: bool = True,
    ) -> None:
        self.syntax_validator = syntax_validator or SyntaxGuardrail()
        self.schema_repair = schema_repair or SchemaRepairEngine()
        self.escalation_hook = escalation_hook or HumanEscalationAuditHook()
        self.agent_graph = agent_graph
        self.auto_repair = auto_repair

    def evaluate(
        self,
        descriptor: ToolCallDescriptor,
        agent_graph: Optional[Any] = None,
        role_id: Optional[str] = None,
    ) -> GuardrailEvaluation:
        """Evaluate tool call descriptor against syntax security, schema, and AgentGraph constraints."""
        args = descriptor.arguments
        repaired_args = None
        violations: List[str] = []

        # 1. Schema Repair
        if self.auto_repair:
            rep, modified = self.schema_repair.repair_arguments(args)
            if modified:
                repaired_args = rep
                args = rep

        # 2. AgentGraph RBAC & Rule Constraint Validation
        graph = agent_graph or self.agent_graph
        effective_role = role_id or descriptor.caller_role

        if graph and effective_role:
            # Check authorized tools (RBAC)
            if hasattr(graph, "get_authorized_tools"):
                auth_tools = graph.get_authorized_tools(effective_role)
                if (
                    descriptor.tool_name not in auth_tools
                    and f"tool:{descriptor.tool_name}" not in auth_tools
                ):
                    violations.append(
                        f"Tool '{descriptor.tool_name}' is not authorized for role '{effective_role}' under active AgentGraph policies."
                    )

            # Check active rule constraints
            resolve_fn = getattr(graph, "resolve_rules", None) or getattr(graph, "resolve_agent_rules", None)
            if resolve_fn:
                resolved = resolve_fn(effective_role)
                restricted_actions = getattr(resolved, "restricted_actions", [])
                if restricted_actions:
                    if descriptor.tool_name in restricted_actions:
                        violations.append(
                            f"Tool '{descriptor.tool_name}' violates active rule policy restriction."
                        )
                    for param_key in ("command", "code", "query", "target", "path"):
                        val = args.get(param_key)
                        if isinstance(val, str):
                            r_viols = self.syntax_validator.validate_action_against_rules(
                                val, restricted_actions
                            )
                            violations.extend(r_viols)

        # 3. Syntax & AST Validation based on tool type / parameters
        if "command" in args and isinstance(args["command"], str):
            cmd_violations = self.syntax_validator.validate_bash_command(args["command"])
            violations.extend(cmd_violations)

        if "code" in args and isinstance(args["code"], str):
            code_violations = self.syntax_validator.validate_python_code(args["code"])
            violations.extend(code_violations)

        if "query" in args and isinstance(args["query"], str):
            sql_violations = self.syntax_validator.validate_sql_query(args["query"])
            violations.extend(sql_violations)

        # 4. Decision
        if violations:
            is_policy_violation = any(
                "AgentGraph" in v or "rule policy" in v or "not authorized for role" in v
                for v in violations
            )
            if is_policy_violation:
                return GuardrailEvaluation(
                    action=GuardrailAction.BLOCK,
                    reason="Execution blocked: AgentGraph role or rule policy constraint violated.",
                    violations=violations,
                    repaired_arguments=repaired_args,
                )

            # Escalate destructive syntax to human gate
            esc_event = self.escalation_hook.escalate(descriptor, violations)
            return GuardrailEvaluation(
                action=GuardrailAction.ESCALATE_HUMAN,
                reason="Security guardrail violation detected in tool parameters.",
                violations=violations,
                escalation_gate=esc_event.escalation_id,
                repaired_arguments=repaired_args,
            )

        if repaired_args is not None:
            return GuardrailEvaluation(
                action=GuardrailAction.REPAIR,
                reason="Arguments automatically coerced and repaired.",
                repaired_arguments=repaired_args,
            )

        return GuardrailEvaluation(
            action=GuardrailAction.ALLOW,
            reason="Tool arguments verified safe.",
            repaired_arguments=args,
        )

