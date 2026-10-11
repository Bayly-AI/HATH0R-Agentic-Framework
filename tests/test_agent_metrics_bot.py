"""Unit tests for AgentMetricsBot substrate."""

from pathlib import Path
import pytest

from hath0r_engine.bots.agent_metrics_bot import AgentMetricsBot, agent_metrics_bot
from hath0r_engine.graph.agent_graph import AgentGraphEngine
from hath0r_engine.pipeline.assertions import validate_json_contract


def test_bot_trigger_intents():
    bot = AgentMetricsBot()
    assert bot.is_triggered_by("show agent metrics")
    assert bot.is_triggered_by("get agent metrics")
    assert bot.is_triggered_by("agent metrics report")
    assert bot.is_triggered_by("show metrics")
    assert bot.is_triggered_by("  Agent Metrics  ")
    assert not bot.is_triggered_by("run code refactor")
    assert not bot.is_triggered_by("")


def test_generate_metrics_report_contract(tmp_path: Path):
    bot = AgentMetricsBot(workspace_root=tmp_path)
    report = bot.generate_metrics_report(intent="show agent metrics", repo_path=Path("."))

    assert report["schema_version"] == "hath0r.agent.metrics/1"
    assert report["bot_id"] == "agent-metrics-bot"
    assert report["intent"] == "show agent metrics"
    assert "summary" in report
    assert "observability" in report
    assert "histogram" in report
    assert "pmat" in report
    assert "tui_metadata" in report

    # Contract schema validation
    contract_file = Path("contracts/hath0r-agent-metrics-report-v1.schema.json")
    if contract_file.is_file():
        validate_json_contract(report, str(contract_file))


def test_render_tui_and_markdown():
    bot = AgentMetricsBot()
    report = bot.generate_metrics_report(intent="show agent metrics", repo_path=Path("."))

    tui_output = bot.render_tui(report)
    assert "HATH0R AGENT METRICS MONITOR" in tui_output or "Agent Metrics Report" in tui_output

    md_output = bot.render_markdown(report)
    assert "# Agent Metrics Report" in md_output
    assert "## Executive Operational Summary" in md_output
    assert "## 1. Observability Tracing" in md_output
    assert "## 2. Token Telemetry Histogram Distribution" in md_output
    assert "## 3. PMAT Multi-Dimensional Code Churn" in md_output


def test_ingest_into_agentgraph():
    bot = AgentMetricsBot()
    report = bot.generate_metrics_report(intent="show agent metrics", repo_path=Path("."))
    ag_engine = AgentGraphEngine()

    node_id = bot.ingest_into_agentgraph(report, agent_graph=ag_engine)
    assert node_id.startswith("bot_execution:agent-metrics-bot:")
    node = ag_engine.get_node(node_id)
    assert node is not None
    assert node.properties["bot_id"] == "agent-metrics-bot"


def test_bot_run_end_to_end():
    bot = AgentMetricsBot()
    res = bot.run(intent="show agent metrics", render_mode="auto")

    assert res["bot_id"] == "agent-metrics-bot"
    assert "report" in res
    assert "output" in res
    assert "markdown_fallback" in res
    assert res["agentgraph_node_id"].startswith("bot_execution:agent-metrics-bot:")
