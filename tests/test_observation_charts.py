"""Unit and integration tests for Agent Observability & Observation Charts."""

from __future__ import annotations

from pathlib import Path
import pytest

from hath0r_engine.telemetry.otel_tracer import AgentObservabilityBot
from hath0r_engine.telemetry.observation_charts import ObservationChartsEngine
from hath0r_engine.telemetry.token_telemetry import TokenTelemetryRecord


def test_agent_observability_bot_spans():
    bot = AgentObservabilityBot(service_name="test-observability-agent")
    bot.new_trace()

    # Record LLM call
    span_llm = bot.record_llm_call(
        model_name="claude-3-5-sonnet",
        prompt_tokens=500,
        completion_tokens=150,
        latency_ms=210.0,
    )
    assert span_llm.span_kind == "LLM"
    assert span_llm.attributes["llm.model_name"] == "claude-3-5-sonnet"

    # Record Tool call
    span_tool = bot.record_tool_call(
        tool_name="view_file",
        input_args={"AbsolutePath": "/tmp/test.txt"},
        output_data="File content preview...",
        success=True,
    )
    assert span_tool.span_kind == "TOOL"
    assert span_tool.attributes["tool.name"] == "view_file"

    # Record Guardrail check
    span_guard = bot.record_guardrail_check(
        guardrail_name="SyntaxGuardrail",
        input_content="def test(): pass",
        passed=True,
    )
    assert span_guard.span_kind == "GUARDRAIL"
    assert span_guard.attributes["guardrail.passed"] is True

    # Record Retriever query
    span_ret = bot.record_retriever_query(
        retriever_name="AgentGraphRetriever",
        query="CR-AGENTGRAPH-001",
        result_count=5,
        latency_ms=12.5,
    )
    assert span_ret.span_kind == "RETRIEVER"
    assert span_ret.attributes["retriever.result_count"] == 5

    # Check total spans
    assert len(bot.spans) == 4

    # Test OTLP payload export
    otlp = bot.export_otlp_payload()
    assert "resourceSpans" in otlp
    assert len(otlp["resourceSpans"][0]["scopeSpans"][0]["spans"]) == 4


def test_observation_charts_engine_computation(tmp_path: Path):
    ledger_path = tmp_path / "telemetry.jsonl"
    engine = ObservationChartsEngine(ledger_path=ledger_path)

    # Append test records
    records = [
        TokenTelemetryRecord(prompt_tokens=200, completion_tokens=50, total_tokens=250, latency_ms=120.0, cost_usd=0.0005),
        TokenTelemetryRecord(prompt_tokens=800, completion_tokens=200, total_tokens=1000, latency_ms=350.0, cost_usd=0.0025),
        TokenTelemetryRecord(prompt_tokens=1500, completion_tokens=400, total_tokens=1900, latency_ms=750.0, cost_usd=0.0055),
    ]
    for r in records:
        engine.ledger.append(r)

    metrics = engine.compute_performance_metrics()
    assert metrics["total_requests"] == 3
    assert metrics["total_tokens"] == 3150
    assert metrics["stats"]["mean"] > 0

    # Test ASCII rendering
    ascii_out = engine.render_ascii_charts(metrics)
    assert "HATH0R AGENT PERFORMANCE OBSERVATION CHARTS" in ascii_out
    assert "Total Interactions : 3" in ascii_out

    # Test Generative UI HTML dashboard
    html_out = engine.render_generative_ui_dashboard(metrics)
    assert "<h2" in html_out
    assert "Hath0r Agent Observation Charts" in html_out
    assert "P90 Latency" in html_out
