"""Deterministic Pre-Execution Guardrails Orchestrator."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

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
        auto_repair: bool = True,
    ) -> None:
        self.syntax_validator = syntax_validator or SyntaxGuardrail()
        self.schema_repair = schema_repair or SchemaRepairEngine()
        self.escalation_hook = escalation_hook or HumanEscalationAuditHook()
        self.auto_repair = auto_repair

    def evaluate(self, descriptor: ToolCallDescriptor) -> GuardrailEvaluation:
        """Evaluate tool call descriptor against syntax security and schema constraints."""
        args = descriptor.arguments
        repaired_args = None
        violations: List[str] = []

        # 1. Schema Repair
        if self.auto_repair:
            rep, modified = self.schema_repair.repair_arguments(args)
            if modified:
                repaired_args = rep
                args = rep

        # 2. Syntax & AST Validation based on tool type / parameters
        if "command" in args and isinstance(args["command"], str):
            cmd_violations = self.syntax_validator.validate_bash_command(args["command"])
            violations.extend(cmd_violations)

        if "code" in args and isinstance(args["code"], str):
            code_violations = self.syntax_validator.validate_python_code(args["code"])
            violations.extend(code_violations)

        if "query" in args and isinstance(args["query"], str):
            sql_violations = self.syntax_validator.validate_sql_query(args["query"])
            violations.extend(sql_violations)

        # 3. Decision
        if violations:
            # Escalate to human gate
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
