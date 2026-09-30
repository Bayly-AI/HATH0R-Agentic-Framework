"""Telemetry and Observability for MCP Semantic Routing and Schema Pruning."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclass
class RoutingMetric:
    """Telemetry data point for a single tool routing resolution."""

    query: str
    total_fleet_tools: int
    routed_tools_count: int
    unpruned_tokens: int
    pruned_tokens: int
    tokens_saved: int
    reduction_pct: float
    latency_ms: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MCPRoutingTelemetry:
    """Aggregates routing metrics, token savings, and fleet performance statistics."""

    def __init__(self, max_history: int = 1000) -> None:
        self.max_history = max_history
        self._history: List[RoutingMetric] = []

    def record(self, metric: RoutingMetric) -> None:
        """Record a routing metric event."""
        self._history.append(metric)
        if len(self._history) > self.max_history:
            self._history.pop(0)

    def get_summary(self) -> Dict[str, Any]:
        """Calculate aggregated summary of token savings and latency."""
        if not self._history:
            return {
                "total_queries": 0,
                "total_unpruned_tokens": 0,
                "total_pruned_tokens": 0,
                "total_tokens_saved": 0,
                "avg_reduction_pct": 0.0,
                "avg_latency_ms": 0.0,
            }

        total_queries = len(self._history)
        tot_unpruned = sum(m.unpruned_tokens for m in self._history)
        tot_pruned = sum(m.pruned_tokens for m in self._history)
        tot_saved = sum(m.tokens_saved for m in self._history)
        avg_red = sum(m.reduction_pct for m in self._history) / total_queries
        avg_lat = sum(m.latency_ms for m in self._history) / total_queries

        return {
            "total_queries": total_queries,
            "total_unpruned_tokens": tot_unpruned,
            "total_pruned_tokens": tot_pruned,
            "total_tokens_saved": tot_saved,
            "avg_reduction_pct": round(avg_red, 2),
            "avg_latency_ms": round(avg_lat, 2),
        }

    def reset(self) -> None:
        """Clear recorded history."""
        self._history.clear()
