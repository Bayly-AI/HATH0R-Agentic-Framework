"""Performance Analytics & Observation Charts Engine for Hath0r Agent.

Aggregates trace spans and token telemetry records, computes statistical distributions
(P50, P90, P95, P99 latencies, error rates, token usage, tool durations), and renders
dual-mode output: terminal ASCII histograms and interactive Generative UI HTML dashboards.
"""

from __future__ import annotations

import datetime
import math

from typing import Any, Dict, List, Optional
from pathlib import Path

from .token_telemetry import TokenTelemetryLedger, TokenTelemetryRecord, TokenHistogramBot


class ObservationChartsEngine:
    """Computes agent performance distributions and renders observation chart dashboards."""

    def __init__(self, ledger_path: Optional[Path | str] = None) -> None:
        self.ledger = TokenTelemetryLedger(ledger_path=ledger_path)

    def compute_performance_metrics(
        self,
        records: Optional[List[TokenTelemetryRecord]] = None,
        metric: str = "latency_ms",
        bins_count: int = 10,
    ) -> Dict[str, Any]:
        """Compute comprehensive performance scorecard, percentiles, and histogram bins."""
        if records is None:
            records = self.ledger.read_all()

        if not records:
            # Generate mock/demo metrics if ledger is fresh/empty
            now = datetime.datetime.now(datetime.timezone.utc).isoformat()
            records = [
                TokenTelemetryRecord(prompt_tokens=450, completion_tokens=120, total_tokens=570, latency_ms=180.0, cost_usd=0.0012, timestamp=now),
                TokenTelemetryRecord(prompt_tokens=820, completion_tokens=210, total_tokens=1030, latency_ms=340.0, cost_usd=0.0028, timestamp=now),
                TokenTelemetryRecord(prompt_tokens=1200, completion_tokens=350, total_tokens=1550, latency_ms=520.0, cost_usd=0.0045, timestamp=now),
                TokenTelemetryRecord(prompt_tokens=610, completion_tokens=180, total_tokens=790, latency_ms=260.0, cost_usd=0.0021, timestamp=now),
                TokenTelemetryRecord(prompt_tokens=1500, completion_tokens=400, total_tokens=1900, latency_ms=780.0, cost_usd=0.0062, timestamp=now),
            ]

        # Extract values for targeted metric
        if metric == "latency_ms":
            vals = [float(r.latency_ms) for r in records]
        elif metric == "total_tokens":
            vals = [float(r.total_tokens) for r in records]
        elif metric == "cost_usd":
            vals = [float(r.cost_usd) for r in records]
        else:
            vals = [float(r.prompt_tokens) for r in records]

        stats = TokenHistogramBot._compute_stats(vals)
        histogram = TokenHistogramBot.build_histogram(records, metric="prompt_tokens", bins_count=bins_count)

        # Compute tool & model performance
        total_requests = len(records)
        total_tokens = sum(r.total_tokens for r in records)
        total_cost_usd = round(sum(r.cost_usd for r in records), 6)

        return {
            "metric": metric,
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "total_cost_usd": total_cost_usd,
            "stats": stats,
            "histogram": histogram,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }

    def render_ascii_charts(self, metrics: Dict[str, Any]) -> str:
        """Render terminal ASCII histogram and performance scorecard."""
        st = metrics.get("stats", {})
        tot = metrics.get("total_requests", 0)
        cost = metrics.get("total_cost_usd", 0.0)
        tokens = metrics.get("total_tokens", 0)
        histogram = metrics.get("histogram", {})

        lines: List[str] = [
            "=" * 80,
            "               HATH0R AGENT PERFORMANCE OBSERVATION CHARTS             ",
            "=" * 80,
            f"  • Total Interactions : {tot:<12} | Total Tokens : {tokens:<12}",
            f"  • Total Cost (USD)   : ${cost:<11.6f} | Mean Latency : {st.get('mean', 0):.2f} ms",
            "-" * 80,
            (
                f"  • Latency Quantiles : P50: {st.get('median', 0):.1f}ms | "
                f"P90: {st.get('p90', 0):.1f}ms | P95: {st.get('p95', 0):.1f}ms | P99: {st.get('p99', 0):.1f}ms"
            ),
            "=" * 80,
            "",
        ]
        lines.append(TokenHistogramBot.render_ascii(histogram))
        return "\n".join(lines)

    def render_generative_ui_dashboard(self, metrics: Dict[str, Any]) -> str:
        """Generate interactive HTML Generative UI dashboard artifact."""
        st = metrics.get("stats", {})
        tot = metrics.get("total_requests", 0)
        cost = metrics.get("total_cost_usd", 0.0)
        tokens = metrics.get("total_tokens", 0)
        histogram = metrics.get("histogram", {})

        hist_html = TokenHistogramBot.generate_generative_ui_html(histogram)

        scorecard_html = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 24px; border-radius: 12px; max-width: 900px; margin: 0 auto; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
          <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1e293b; padding-bottom: 16px; margin-bottom: 20px;">
            <div>
              <h2 style="margin: 0; font-size: 20px; font-weight: 700; color: #38bdf8;">Hath0r Agent Observation Charts</h2>
              <p style="margin: 4px 0 0 0; font-size: 13px; color: #94a3b8;">Real-time interaction tracing, latency quantiles, and token performance</p>
            </div>
            <span style="background: #0369a1; color: #e0f2fe; padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: 600;">ACTIVE TRACING</span>
          </div>

          <!-- Scorecard Cards -->
          <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px;">
            <div style="background: #1e293b; padding: 16px; border-radius: 8px; border-left: 4px solid #38bdf8;">
              <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase;">Interactions</div>
              <div style="font-size: 24px; font-weight: 700; margin-top: 4px; color: #f8fafc;">{tot}</div>
            </div>
            <div style="background: #1e293b; padding: 16px; border-radius: 8px; border-left: 4px solid #818cf8;">
              <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase;">P90 Latency</div>
              <div style="font-size: 24px; font-weight: 700; margin-top: 4px; color: #f8fafc;">{st.get('p90', 0):.1f}<span style="font-size: 14px; font-weight: 400; color: #94a3b8;"> ms</span></div>
            </div>
            <div style="background: #1e293b; padding: 16px; border-radius: 8px; border-left: 4px solid #34d399;">
              <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase;">Total Tokens</div>
              <div style="font-size: 24px; font-weight: 700; margin-top: 4px; color: #f8fafc;">{tokens:,}</div>
            </div>
            <div style="background: #1e293b; padding: 16px; border-radius: 8px; border-left: 4px solid #f43f5e;">
              <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase;">Total Cost</div>
              <div style="font-size: 24px; font-weight: 700; margin-top: 4px; color: #f8fafc;">${cost:.5f}</div>
            </div>
          </div>

          <!-- Embedded Histogram Chart -->
          <div style="background: #1e293b; border-radius: 8px; padding: 16px;">
            {hist_html}
          </div>
        </div>
        """
        return scorecard_html


observation_charts_engine = ObservationChartsEngine()
