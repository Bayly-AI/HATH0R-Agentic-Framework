"""Programmatic Assertions and Schema Invariant Checkers for Agent Pipelines."""

from __future__ import annotations

import json
import warnings
from typing import Any, Dict


class SchemaAssertionError(Exception):
    """Hard failure when an agent output violates a mandatory contract assertion."""

    pass


class SchemaSuggestionWarning(UserWarning):
    """Soft warning when an agent output fails an advisory suggestion."""

    pass


def assert_contract(condition: bool, msg: str = "Assertion failed.") -> None:
    """Enforce a mandatory contract invariant on prediction output."""
    if not condition:
        raise SchemaAssertionError(msg)


def suggest_constraint(condition: bool, msg: str = "Suggestion violated.") -> bool:
    """Evaluate an advisory constraint, returning False if not met."""
    if not condition:
        warnings.warn(msg, SchemaSuggestionWarning, stacklevel=2)
        return False
    return True


Assert = assert_contract
Suggest = suggest_constraint


def validate_json_contract(data_str: str, schema: Dict[str, Any]) -> bool:
    """Validate a JSON string or dict against a basic schema contract."""
    try:
        data = json.loads(data_str) if isinstance(data_str, str) else data_str
        if not isinstance(data, dict):
            return False

        required_fields = schema.get("required", [])
        for req in required_fields:
            if req not in data:
                return False

        return True
    except Exception:
        return False
