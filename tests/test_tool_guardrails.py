"""Unit tests for Deterministic Pre-Execution Tool Guardrails and Schema Repair."""


from hath0r_engine.guardrails import (
    GuardrailAction,
    GuardrailsManager,
    SchemaRepairEngine,
    SyntaxGuardrail,
    ToolCallDescriptor,
)


def test_syntax_guardrail_python_ast():
    validator = SyntaxGuardrail()

    # Safe code
    safe_code = "def add(a, b):\n    return a + b\nresult = add(1, 2)"
    assert validator.validate_python_code(safe_code) == []

    # Forbidden OS call
    bad_code_os = "import os\nos.system('echo hacked')"
    violations_os = validator.validate_python_code(bad_code_os)
    assert len(violations_os) > 0
    assert any("os.system" in v for v in violations_os)

    # Forbidden eval
    bad_code_eval = "x = eval('2 + 2')"
    violations_eval = validator.validate_python_code(bad_code_eval)
    assert len(violations_eval) > 0
    assert any("eval" in v for v in violations_eval)


def test_syntax_guardrail_bash_and_sql():
    validator = SyntaxGuardrail()

    # Safe bash
    assert validator.validate_bash_command("pytest tests/ -v") == []

    # Destructive bash
    bad_bash = "rm -rf /"
    violations_bash = validator.validate_bash_command(bad_bash)
    assert len(violations_bash) > 0

    # Safe SQL
    assert validator.validate_sql_query("SELECT id, name FROM users WHERE active = 1") == []

    # Destructive SQL: DROP TABLE
    drop_sql = "DROP TABLE users;"
    violations_sql = validator.validate_sql_query(drop_sql)
    assert len(violations_sql) > 0

    # Destructive SQL: Unconstrained DELETE
    delete_sql = "DELETE FROM users"
    violations_del = validator.validate_sql_query(delete_sql)
    assert len(violations_del) > 0


def test_schema_repair_engine_coercion():
    repairer = SchemaRepairEngine()

    args = {
        "is_active": "true",
        "dry_run": "false",
        "limit": "100",
        "threshold": "0.95",
        "config": '{"timeout": 30, "retries": 3}',
        "name": "project_alpha",
    }

    repaired, modified = repairer.repair_arguments(args)
    assert modified is True
    assert repaired["is_active"] is True
    assert repaired["dry_run"] is False
    assert repaired["limit"] == 100
    assert repaired["threshold"] == 0.95
    assert repaired["config"] == {"timeout": 30, "retries": 3}
    assert repaired["name"] == "project_alpha"


def test_guardrails_manager_evaluation_pipeline():
    manager = GuardrailsManager()

    # 1. Clean tool call -> ALLOW
    safe_call = ToolCallDescriptor(
        tool_name="git_status",
        arguments={"path": "."},
    )
    eval_safe = manager.evaluate(safe_call)
    assert eval_safe.action == GuardrailAction.ALLOW

    # 2. Malformed types -> REPAIR
    repair_call = ToolCallDescriptor(
        tool_name="fetch_records",
        arguments={"limit": "50"},
    )
    eval_repair = manager.evaluate(repair_call)
    assert eval_repair.action == GuardrailAction.REPAIR
    assert eval_repair.repaired_arguments["limit"] == 50

    # 3. Dangerous command -> ESCALATE_HUMAN
    dangerous_call = ToolCallDescriptor(
        tool_name="shell_execute",
        arguments={"command": "rm -rf / --no-preserve-root"},
    )
    eval_danger = manager.evaluate(dangerous_call)
    assert eval_danger.action == GuardrailAction.ESCALATE_HUMAN
    assert eval_danger.escalation_gate is not None
    assert len(eval_danger.violations) > 0
