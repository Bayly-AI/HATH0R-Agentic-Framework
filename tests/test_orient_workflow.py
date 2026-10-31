"""Test suite for repository orientation workflow, OrientBot, and schema contracts."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import pytest

from hath0r_engine.bots.orient_bot import OrientBot


@pytest.fixture
def workspace_root() -> Path:
    return Path(__file__).parent.parent.resolve()


@pytest.fixture
def orient_bot(workspace_root: Path) -> OrientBot:
    return OrientBot(workspace_root=workspace_root)


def test_orient_bot_trigger_intents(orient_bot: OrientBot) -> None:
    assert orient_bot.is_triggered_by("orient")
    assert orient_bot.is_triggered_by("hath0r orient")
    assert orient_bot.is_triggered_by("run orient")
    assert orient_bot.is_triggered_by("orient repository")
    assert not orient_bot.is_triggered_by("unrelated query")


def test_read_agentgraph(orient_bot: OrientBot, workspace_root: Path) -> None:
    res = orient_bot.read_agentgraph(repo_path=workspace_root)
    assert "agents" in res
    assert "rules" in res
    assert "topology" in res
    assert isinstance(res["agents"], list)
    assert isinstance(res["rules"], list)
    assert res["topology"]["total_nodes"] > 0


def test_read_readme(orient_bot: OrientBot, workspace_root: Path) -> None:
    res = orient_bot.read_readme(repo_path=workspace_root)
    assert res["found"] is True
    assert "HATHOR" in res["title"].upper()
    assert len(res["summary"]) > 0
    assert isinstance(res["components"], list)


def test_scan_code(orient_bot: OrientBot, workspace_root: Path) -> None:
    res = orient_bot.scan_code(repo_path=workspace_root)
    assert "primary_languages" in res
    assert "subsystems" in res
    assert "src" in res["subsystems"]
    assert res["total_files"] > 0
    assert len(res["summary"]) > 0


def test_run_agent_metrics(orient_bot: OrientBot, workspace_root: Path) -> None:
    res = orient_bot.run_agent_metrics(repo_path=workspace_root)
    assert "summary" in res
    assert "observability" in res
    assert "pmat" in res
    assert "latency_quantiles" in res["observability"]


def test_run_agent_calibration(orient_bot: OrientBot, workspace_root: Path) -> None:
    res = orient_bot.run_agent_calibration(repo_path=workspace_root)
    assert "fresh" in res
    assert res["fresh"] is True
    assert "parameters" in res
    params = res["parameters"]
    assert "temperature" in params
    assert "max_tokens" in params
    assert "top_p" in params
    assert "retry_count" in params
    assert "guardrail_threshold" in params


def test_orientation_report_schema_contract(orient_bot: OrientBot, workspace_root: Path) -> None:
    report = orient_bot.generate_orientation_report(repo_path=workspace_root)
    schema_path = workspace_root / "contracts" / "hath0r-orient-report-v1.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    jsonschema.validate(instance=report, schema=schema)
    assert report["verdict"]["status"] in ("ORIENTED", "NEEDS_ATTENTION")
    assert len(report["verdict"]["findings_summary"]) > 0


def test_dual_mode_rendering(orient_bot: OrientBot, workspace_root: Path) -> None:
    res = orient_bot.run(repo_path=workspace_root, render_mode="markdown")
    assert "output" in res
    assert "# Repository Orientation Report" in res["output"]
    assert "Executive Operational Scorecard" in res["output"]

    tui_res = orient_bot.run(repo_path=workspace_root, render_mode="auto")
    assert "HATH0R REPOSITORY ORIENTATION" in tui_res["output"] or "# Repository Orientation Report" in tui_res["output"]
