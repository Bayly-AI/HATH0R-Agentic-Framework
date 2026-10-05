"""Unit tests for OTELTracerBot and OpenInference distributed tracing."""

import json
import tempfile
from pathlib import Path

from hath0r_engine.telemetry.otel_tracer import OTELTracerBot, TelemetrySpan


def test_telemetry_span_lifecycle():
    span = TelemetrySpan(name="test_span", span_kind="AGENT")
    span.add_event("start_work", {"user": "ray"})
    assert span.duration_ms == 0.0
    assert span.status == "OK"

    span.finish(status="OK")
    assert span.end_time_ns is not None
    assert span.duration_ms >= 0.0

    d = span.to_dict()
    assert d["name"] == "test_span"
    assert len(d["events"]) == 1
    assert d["events"][0]["name"] == "start_work"


def test_otel_tracer_nested_spans():
    tracer = OTELTracerBot(service_name="hath0r-test")
    trace_id = tracer.new_trace()

    with tracer.start_span("agent_step", span_kind="AGENT") as root_span:
        assert root_span.trace_id == trace_id
        assert root_span.parent_span_id is None

        with tracer.start_span("retrieve_context", span_kind="RETRIEVER") as child_span:
            assert child_span.trace_id == trace_id
            assert child_span.parent_span_id == root_span.span_id

    assert len(tracer.spans) == 2
    # Spans finish in reverse order (child first, then root)
    assert tracer.spans[0].name == "retrieve_context"
    assert tracer.spans[1].name == "agent_step"


def test_openinference_helpers_and_otlp_export():
    tracer = OTELTracerBot(service_name="hath0r-test")

    # LLM Call
    llm_span = tracer.record_llm_call(
        model_name="claude-3-7-sonnet",
        prompt_tokens=150,
        completion_tokens=45,
        latency_ms=320.5,
        cost_usd=0.0025,
        input_value="Explain quantum teleportation in 2 sentences",
        output_value="Quantum teleportation transfers quantum information using entanglement.",
        project_name="hath0r-telemetry-eval",
    )
    assert llm_span.attributes["llm.model_name"] == "claude-3-7-sonnet"
    assert llm_span.attributes["llm.token_count.total"] == 195
    assert llm_span.attributes["llm.cost.total"] == 0.0025
    assert llm_span.attributes["input.value"] == "Explain quantum teleportation in 2 sentences"
    assert "entanglement" in llm_span.attributes["output.value"]
    assert llm_span.attributes["openinference.project.name"] == "hath0r-telemetry-eval"

    # Tool Call
    tool_span = tracer.record_tool_call(
        tool_name="git_status",
        input_args={"cwd": "."},
        output_data="clean working tree",
        success=True,
    )
    assert tool_span.attributes["tool.name"] == "git_status"
    assert tool_span.status == "OK"

    # Export OTLP payload
    payload = tracer.export_otlp_payload()
    assert "resourceSpans" in payload
    res_spans = payload["resourceSpans"][0]["scopeSpans"][0]["spans"]
    assert len(res_spans) == 2

    # Save to JSON lines
    with tempfile.TemporaryDirectory() as tmpdir:
        trace_file = Path(tmpdir) / "traces.jsonl"
        tracer.save_traces(trace_file)
        assert trace_file.exists()
        lines = trace_file.read_text(encoding="utf-8").strip().splitlines()
        assert len(lines) == 2
        first_span = json.loads(lines[0])
        assert "trace_id" in first_span
