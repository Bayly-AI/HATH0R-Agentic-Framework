"""OpenTelemetry (OTEL) Tracing & OpenInference Telemetry Engine for Hath0r.

Provides zero-overhead distributed trace span collection, OpenInference semantic
conventions for LLM, Tool, Retriever, and Agent steps, and OTLP-compatible exporter.
"""

from __future__ import annotations

import contextlib
import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional


@dataclass
class TelemetrySpan:
    """An individual trace span conforming to OpenInference semantic conventions."""

    name: str
    span_id: str = field(default_factory=lambda: uuid.uuid4().hex[:16])
    trace_id: str = field(default_factory=lambda: uuid.uuid4().hex[:32])
    parent_span_id: Optional[str] = None
    span_kind: str = "AGENT"  # AGENT | LLM | TOOL | RETRIEVER | CHAIN
    start_time_ns: int = field(default_factory=time.time_ns)
    end_time_ns: Optional[int] = None
    status: str = "OK"  # OK | ERROR | UNSET
    error_message: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def duration_ms(self) -> float:
        """Return span duration in milliseconds."""
        if self.end_time_ns is None:
            return 0.0
        return (self.end_time_ns - self.start_time_ns) / 1_000_000.0

    def finish(self, status: str = "OK", error: Optional[str] = None) -> None:
        """Close span timestamp and record terminal status."""
        self.end_time_ns = time.time_ns()
        self.status = status
        if error:
            self.error_message = error
            self.status = "ERROR"

    def add_event(self, name: str, attributes: Optional[Dict[str, Any]] = None) -> None:
        """Record an in-span lifecycle event."""
        self.events.append(
            {
                "name": name,
                "timestamp_ns": time.time_ns(),
                "attributes": attributes or {},
            }
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize span to dictionary representation."""
        data = asdict(self)
        data["duration_ms"] = round(self.duration_ms, 3)
        return data

    def to_otlp_span(self) -> Dict[str, Any]:
        """Format span as standard OpenTelemetry Protocol (OTLP) JSON object."""
        return {
            "traceId": self.trace_id,
            "spanId": self.span_id,
            "parentSpanId": self.parent_span_id or "",
            "name": self.name,
            "kind": 1,  # SPAN_KIND_INTERNAL
            "startTimeUnixNano": str(self.start_time_ns),
            "endTimeUnixNano": str(self.end_time_ns or time.time_ns()),
            "status": {"code": 1 if self.status == "OK" else 2, "message": self.error_message or ""},
            "attributes": [{"key": k, "value": {"stringValue": str(v)}} for k, v in self.attributes.items()],
            "events": [
                {
                    "name": evt["name"],
                    "timeUnixNano": str(evt["timestamp_ns"]),
                    "attributes": [
                        {"key": k, "value": {"stringValue": str(v)}} for k, v in evt.get("attributes", {}).items()
                    ],
                }
                for evt in self.events
            ],
        }


class OTELTracerBot:
    """Manages trace context hierarchies, OpenInference instrumentation, and OTLP export."""

    def __init__(self, service_name: str = "hath0r-engine") -> None:
        self.service_name = service_name
        self.spans: List[TelemetrySpan] = []
        self._active_span_stack: List[TelemetrySpan] = []
        self._current_trace_id: str = uuid.uuid4().hex[:32]

    def new_trace(self) -> str:
        """Reset current active trace identifier."""
        self._current_trace_id = uuid.uuid4().hex[:32]
        self._active_span_stack.clear()
        return self._current_trace_id

    @contextlib.contextmanager
    def start_span(
        self,
        name: str,
        span_kind: str = "AGENT",
        attributes: Optional[Dict[str, Any]] = None,
    ) -> Generator[TelemetrySpan, None, None]:
        """Context manager creating a nested execution trace span."""
        parent_id = self._active_span_stack[-1].span_id if self._active_span_stack else None
        attrs = dict(attributes or {})
        attrs["service.name"] = self.service_name
        attrs["openinference.span.kind"] = span_kind

        span = TelemetrySpan(
            name=name,
            trace_id=self._current_trace_id,
            parent_span_id=parent_id,
            span_kind=span_kind,
            attributes=attrs,
        )

        self._active_span_stack.append(span)
        try:
            yield span
            if span.end_time_ns is None:
                span.finish(status="OK")
        except Exception as e:
            if span.end_time_ns is None:
                span.finish(status="ERROR", error=str(e))
            raise
        finally:
            if self._active_span_stack and self._active_span_stack[-1] is span:
                self._active_span_stack.pop()
            self.spans.append(span)

    def record_llm_call(
        self,
        model_name: str,
        prompt_tokens: int,
        completion_tokens: int,
        latency_ms: float,
        temperature: float = 0.7,
    ) -> TelemetrySpan:
        """Record standard OpenInference LLM telemetry span."""
        attrs = {
            "llm.model_name": model_name,
            "llm.token_count.prompt": prompt_tokens,
            "llm.token_count.completion": completion_tokens,
            "llm.token_count.total": prompt_tokens + completion_tokens,
            "llm.invocation_parameters.temperature": temperature,
        }
        with self.start_span(f"llm:{model_name}", span_kind="LLM", attributes=attrs) as span:
            span.add_event("token_generation_complete", {"latency_ms": latency_ms})
            return span

    def record_tool_call(
        self,
        tool_name: str,
        input_args: Dict[str, Any],
        output_data: Any,
        success: bool = True,
    ) -> TelemetrySpan:
        """Record OpenInference tool execution span."""
        attrs = {
            "tool.name": tool_name,
            "tool.parameters": json.dumps(input_args),
            "tool.output": str(output_data)[:500],
        }
        with self.start_span(f"tool:{tool_name}", span_kind="TOOL", attributes=attrs) as span:
            if not success:
                span.finish(status="ERROR", error=str(output_data))
            return span

    def record_guardrail_check(
        self,
        guardrail_name: str,
        input_content: str,
        passed: bool,
        repaired: bool = False,
        error_message: Optional[str] = None,
    ) -> TelemetrySpan:
        """Record OpenInference guardrail evaluation span."""
        attrs = {
            "guardrail.name": guardrail_name,
            "guardrail.passed": passed,
            "guardrail.repaired": repaired,
            "guardrail.input_length": len(input_content),
        }
        with self.start_span(f"guardrail:{guardrail_name}", span_kind="GUARDRAIL", attributes=attrs) as span:
            if not passed:
                span.finish(status="ERROR", error=error_message or "Guardrail validation failed")
            return span

    def record_retriever_query(
        self,
        retriever_name: str,
        query: str,
        result_count: int,
        latency_ms: float,
    ) -> TelemetrySpan:
        """Record OpenInference retriever/KB search span."""
        attrs = {
            "retriever.name": retriever_name,
            "retriever.query": query[:200],
            "retriever.result_count": result_count,
            "retriever.latency_ms": latency_ms,
        }
        with self.start_span(f"retriever:{retriever_name}", span_kind="RETRIEVER", attributes=attrs) as span:
            return span

    def export_otlp_payload(self) -> Dict[str, Any]:
        """Package collected spans into an OpenTelemetry Protocol (OTLP) resource span bundle."""
        return {
            "resourceSpans": [
                {
                    "resource": {
                        "attributes": [
                            {"key": "service.name", "value": {"stringValue": self.service_name}},
                            {"key": "telemetry.sdk.language", "value": {"stringValue": "python"}},
                            {"key": "telemetry.sdk.name", "value": {"stringValue": "hath0r-otel"}},
                        ]
                    },
                    "scopeSpans": [
                        {
                            "scope": {"name": "hath0r.engine", "version": "1.0.0"},
                            "spans": [s.to_otlp_span() for s in self.spans],
                        }
                    ],
                }
            ]
        }

    def save_traces(self, output_path: str | Path) -> None:
        """Persist collected spans as JSON lines file."""
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            for s in self.spans:
                f.write(json.dumps(s.to_dict()) + "\n")


AgentObservabilityBot = OTELTracerBot
agent_observability_bot = AgentObservabilityBot()

