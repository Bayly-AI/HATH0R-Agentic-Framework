"""Tests for AgentGraph JSON schema contracts (v1).

Validates schema definitions and payloads for:
- contracts/hath0r-agentgraph-v1.schema.json
- contracts/hath0r-rule-node-v1.schema.json
- contracts/hath0r-agent-role-v1.schema.json
"""

import json
from pathlib import Path

import jsonschema
import pytest


@pytest.fixture
def contracts_dir() -> Path:
    return Path(__file__).parent.parent / "contracts"


@pytest.fixture
def agentgraph_schema(contracts_dir: Path) -> dict:
    schema_path = contracts_dir / "hath0r-agentgraph-v1.schema.json"
    assert schema_path.exists(), "hath0r-agentgraph-v1.schema.json not found"
    return json.loads(schema_path.read_text(encoding="utf-8"))


@pytest.fixture
def rule_node_schema(contracts_dir: Path) -> dict:
    schema_path = contracts_dir / "hath0r-rule-node-v1.schema.json"
    assert schema_path.exists(), "hath0r-rule-node-v1.schema.json not found"
    return json.loads(schema_path.read_text(encoding="utf-8"))


@pytest.fixture
def agent_role_schema(contracts_dir: Path) -> dict:
    schema_path = contracts_dir / "hath0r-agent-role-v1.schema.json"
    assert schema_path.exists(), "hath0r-agent-role-v1.schema.json not found"
    return json.loads(schema_path.read_text(encoding="utf-8"))


def test_agentgraph_schema_validity(agentgraph_schema: dict):
    """Ensure the AgentGraph schema itself is valid JSON Schema Draft 2020-12."""
    validator_cls = jsonschema.validators.validator_for(agentgraph_schema)
    validator_cls.check_schema(agentgraph_schema)


def test_rule_node_schema_validity(rule_node_schema: dict):
    """Ensure the RuleNode schema is valid JSON Schema."""
    validator_cls = jsonschema.validators.validator_for(rule_node_schema)
    validator_cls.check_schema(rule_node_schema)


def test_agent_role_schema_validity(agent_role_schema: dict):
    """Ensure the AgentRoleNode schema is valid JSON Schema."""
    validator_cls = jsonschema.validators.validator_for(agent_role_schema)
    validator_cls.check_schema(agent_role_schema)


def test_agentgraph_snapshot_payload_validation(agentgraph_schema: dict):
    """Test validating an AgentGraph snapshot covering all required node and edge types."""
    payload = {
        "schema_version": "hath0r.agentgraph/1",
        "graph_id": "test-cluster",
        "timestamp": "2026-10-02T12:00:00Z",
        "nodes": [
            {
                "id": "role:curator",
                "plane": "rules",
                "type": "agent_role",
                "label": "Codebase Curator",
                "content": "Manages repo structure.",
                "properties": {"role_name": "Codebase Curator", "scope": "root"},
                "is_current": True,
            },
            {
                "id": "rule:cr-cli-entry-001",
                "plane": "rules",
                "type": "rule_policy",
                "label": "CLI Entry Rule",
                "content": "Always prefer hath0r CLI entrypoint.",
                "properties": {"priority": 4, "target_scope": "root"},
                "is_current": True,
            },
            {
                "id": "doc:architecture",
                "plane": "knowledge",
                "type": "knowledge_doc",
                "label": "Architecture Doc",
                "content": "ADR notes",
                "is_current": True,
            },
            {
                "id": "span:step-1",
                "plane": "context",
                "type": "context_span",
                "label": "Execution Span",
                "is_current": True,
            },
            {
                "id": "mem:reflection-1",
                "plane": "memory",
                "type": "memory_entity",
                "label": "Session Reflection",
                "is_current": True,
            },
            {
                "id": "asset:diagram.png",
                "plane": "extensible",
                "type": "file_asset",
                "label": "Architecture Diagram",
                "is_current": True,
            },
        ],
        "edges": [
            {
                "source": "rule:cr-cli-entry-001",
                "target": "role:curator",
                "relation": "GOVERNS",
            },
            {
                "source": "role:curator",
                "target": "role:base",
                "relation": "INHERITS_FROM",
            },
            {
                "source": "role:curator",
                "target": "tool:read_file",
                "relation": "AUTHORIZES_TOOL",
            },
            {
                "source": "role:curator",
                "target": "rule:no-direct-push",
                "relation": "RESTRICTED_BY",
            },
            {
                "source": "role:curator",
                "target": "role:sub-worker",
                "relation": "CAN_SPAWN",
            },
            {
                "source": "rule:cr-cli-entry-002",
                "target": "rule:cr-cli-entry-001",
                "relation": "SUPERSEDES",
            },
        ],
    }

    # Should validate without error
    jsonschema.validate(instance=payload, schema=agentgraph_schema)


def test_agentgraph_snapshot_invalid_payload(agentgraph_schema: dict):
    """Test that invalid node plane or missing id raises ValidationError."""
    invalid_payload = {
        "schema_version": "hath0r.agentgraph/1",
        "graph_id": "test-cluster",
        "nodes": [
            {
                "id": "role:curator",
                "plane": "invalid_plane_name",  # Invalid plane
                "type": "agent_role",
                "label": "Codebase Curator",
            }
        ],
        "edges": [],
    }

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_payload, schema=agentgraph_schema)


def test_rule_node_payload_validation(rule_node_schema: dict):
    """Test validating a single RuleNode entity payload."""
    valid_rule = {
        "schema_version": "hath0r.rule-node/1",
        "id": "rule:cr-docker-001",
        "plane": "rules",
        "type": "rule_policy",
        "label": "Docker Group Policy",
        "content": "All services must join hath0r Docker group.",
        "properties": {
            "priority": 4,
            "priority_name": "ORG_INVARIANT",
            "target_scope": "root",
            "restricted_actions": ["docker run --rm"],
            "allowed_actions": ["make docker-up"],
            "supersedes_rule_id": None,
        },
        "is_current": True,
    }

    jsonschema.validate(instance=valid_rule, schema=rule_node_schema)


def test_rule_node_invalid_priority(rule_node_schema: dict):
    """Test that an invalid priority tier fails schema validation."""
    invalid_rule = {
        "id": "rule:invalid",
        "plane": "rules",
        "type": "rule_policy",
        "label": "Invalid Rule",
        "properties": {
            "priority": 99,  # Only 1..4 allowed
        },
    }

    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(instance=invalid_rule, schema=rule_node_schema)


def test_agent_role_payload_validation(agent_role_schema: dict):
    """Test validating an AgentRoleNode entity payload."""
    valid_role = {
        "schema_version": "hath0r.agent-role/1",
        "id": "role:quality_auditor",
        "plane": "rules",
        "type": "agent_role",
        "label": "Quality Gate Auditor",
        "content": "Audits quality gate compliance.",
        "properties": {
            "role_name": "Quality Auditor",
            "scope": "tests",
            "permitted_tools": ["pytest", "ruff"],
            "forbidden_tools": ["git_push_master"],
            "parent_role_id": "role:base_auditor",
            "max_subagents": 2,
            "allowed_child_roles": ["role:test_runner"],
        },
        "is_current": True,
    }

    jsonschema.validate(instance=valid_role, schema=agent_role_schema)
