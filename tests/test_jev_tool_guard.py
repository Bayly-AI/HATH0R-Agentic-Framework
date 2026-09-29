"""Unit and policy evaluation tests for JEV tool guard in hath0r-framework."""

from __future__ import annotations

import asyncio
from typing import Any, Mapping

import pytest

from lib.jev.jev_client import (
    JevClient,
    JevSettings,
    ToolGuardRequest,
    ToolGuardResult,
    stub_tool_guard,
)
from lib.jev.jev_tool_guard import (
    GUARDED_TOOL_PROFILES,
    build_tool_guard_request,
    evaluate_tool_guard,
    format_block_message,
    is_guarded_tool,
)


def test_guarded_tools_catalog() -> None:
    # Mutating tools must be guarded
    assert is_guarded_tool("kb_index_delete") is True
    assert is_guarded_tool("kb_add_document") is True
    assert is_guarded_tool("fs_write") is True
    assert is_guarded_tool("fs_delete") is True
    assert is_guarded_tool("shell_execute") is True
    assert is_guarded_tool("network_request") is True

    # Read-only tools must NOT be in the guarded set
    assert is_guarded_tool("kb_search") is False
    assert is_guarded_tool("kb_get_document") is False
    assert is_guarded_tool("health_check") is False


def test_build_tool_guard_request_redacts_secrets() -> None:
    args: Mapping[str, Any] = {
        "path": "/workspace/config.yaml",
        "api_key": "secret_key_12345",
        "password": "super_secret_password",
        "token": "ghp_abcdef1234567890",
    }
    req = build_tool_guard_request("fs_write", args)
    assert req is not None
    assert req.tool == "fs_write"
    summary_text = " ".join(req.arguments_summary)
    assert "secret_key_12345" not in summary_text
    assert "super_secret_password" not in summary_text
    assert "ghp_abcdef" not in summary_text
    assert "api_key=[REDACTED]" in summary_text
    assert "password=[REDACTED]" in summary_text
    assert "token=[REDACTED]" in summary_text


def test_stub_tool_guard_destructive_denied() -> None:
    req = build_tool_guard_request("fs_delete", {"path": "/workspace/data"})
    assert req is not None
    result = stub_tool_guard(req)
    assert result.decision == "deny"
    assert result.confidence >= 0.9


def test_stub_tool_guard_mutating_confirmed() -> None:
    req = build_tool_guard_request("fs_write", {"path": "/workspace/file.txt"})
    assert req is not None
    result = stub_tool_guard(req)
    assert result.decision == "confirm"
    assert result.confidence >= 0.8


def test_evaluate_tool_guard_disabled_returns_none() -> None:
    client = JevClient(settings=JevSettings(enabled=False, mode="off"))
    res = asyncio.run(evaluate_tool_guard("fs_write", {"path": "test.txt"}, client=client))
    assert res is None


def test_evaluate_tool_guard_stub_blocks_mutating() -> None:
    client = JevClient(settings=JevSettings(enabled=True, mode="stub"))
    res = asyncio.run(evaluate_tool_guard("fs_delete", {"path": "important.txt"}, client=client))
    assert res is not None
    assert res.blocked is True
    assert res.decision == "deny"

    block_json = format_block_message("fs_delete", res)
    assert "jev_tool_guard_blocked" in block_json
    assert "fs_delete" in block_json


def test_jev_settings_from_openfeature_env() -> None:
    settings = JevSettings.from_env({
        "HATH0R_FLAG_JEV_TOOL_GUARD_ENABLED": "true",
        "JEV_MODE": "stub",
    })
    assert settings.enabled is True
    assert settings.mode == "stub"


def test_jev_fails_closed_on_error_when_configured() -> None:
    # on_error="deny" fails closed
    settings = JevSettings(enabled=True, mode="live", api_key="", on_error="deny")
    client = JevClient(settings=settings)
    req = build_tool_guard_request("fs_write", {"path": "foo"})
    assert req is not None
    res = asyncio.run(client.guard_tool_call(req))
    assert res.blocked is True
    assert res.decision == "deny"
