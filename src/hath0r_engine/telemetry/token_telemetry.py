"""FinOps Token Telemetry Ingestion, Ledger Management, and Histogram Analytics.

Captures timestamp, user, character length, token counts, and cost for all agent interactions.
Provides append-only persistence, filtered retrieval, statistical distribution analysis,
and multi-modal histogram visualization (CLI ASCII / JSON / Generative UI).
Zero external runtime dependencies (pure Python standard library).
"""

from __future__ import annotations

import datetime
import json
import math
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

# Baseline pricing rates per 1,000,000 tokens (USD)
DEFAULT_TIER_PRICING: Dict[str, Dict[str, float]] = {
    "light": {"input": 0.15, "output": 0.60},        # e.g., haiku / 4o-mini / flash
    "standard": {"input": 3.00, "output": 15.00},    # e.g., sonnet-3.5 / gpt-4o
    "reasoning": {"input": 15.00, "output": 60.00},  # e.g., o3-mini / deepseek-r1 / opus
}


@dataclass
class TokenTelemetryRecord:
    """Canonical telemetry record for an agent token interaction."""

    id: str = field(default_factory=lambda: f"tok_{uuid.uuid4().hex[:12]}")
    timestamp: str = field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
    )
    timestamp_ns: int = field(
        default_factory=lambda: int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1_000_000_000)
    )
    user_id: str = "default_user"
    agent_id: str = "hath0r-agent"
    session_id: str = ""
    prompt_length_chars: int = 0
    prompt_tokens: int = 0
    completion_length_chars: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    model: str = "claude-3-5-sonnet"
    tier: str = "standard"
    cost_usd: float = 0.0
    latency_ms: float = 0.0
    cached: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert record to dictionary conforming to JSON schema."""
        data = asdict(self)
        data["cost_usd"] = round(self.cost_usd, 8)
        data["latency_ms"] = round(self.latency_ms, 2)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TokenTelemetryRecord:
        """Construct record from dictionary."""
        valid_fields = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**valid_fields)


class TokenTelemetryLedger:
    """Append-only storage and indexed retrieval for token telemetry records."""

    def __init__(self, ledger_path: Optional[Path | str] = None) -> None:
        if ledger_path is not None:
            self.ledger_path = Path(ledger_path)
        else:
            self.ledger_path = Path.cwd() / ".hath0r" / "finops" / "token_telemetry.jsonl"

    def _ensure_dir(self) -> None:
        self.ledger_path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, record: TokenTelemetryRecord) -> None:
        """Safely append a telemetry record to the JSONL ledger."""
        self._ensure_dir()
        with self.ledger_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record.to_dict()) + "\n")

    def read_all(self) -> List[TokenTelemetryRecord]:
        """Read all telemetry records from ledger."""
        if not self.ledger_path.exists():
            return []
        records: List[TokenTelemetryRecord] = []
        with self.ledger_path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    records.append(TokenTelemetryRecord.from_dict(data))
                except Exception:
                    continue
        return records

    def query(
        self,
        user_id: Optional[str] = None,
        model: Optional[str] = None,
        session_id: Optional[str] = None,
        tier: Optional[str] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[TokenTelemetryRecord]:
        """Retrieve filtered records matching specific criteria."""
        all_records = self.read_all()
        filtered: List[TokenTelemetryRecord] = []

        for r in all_records:
            if user_id and r.user_id != user_id:
                continue
            if model and r.model != model:
                continue
            if session_id and r.session_id != session_id:
                continue
            if tier and r.tier != tier:
                continue
            if since and r.timestamp < since:
                continue
            if until and r.timestamp > until:
                continue
            filtered.append(r)

        if limit is not None and limit > 0:
            return filtered[-limit:]
        return filtered

    def clear(self) -> None:
        """Purge all records in ledger (test utility)."""
        if self.ledger_path.exists():
            self.ledger_path.unlink()


class TokenTelemetryBot:
    """Manages token telemetry ingestion, cost calculation, and query operations."""

    def __init__(self, ledger_path: Optional[Path | str] = None) -> None:
        self.ledger = TokenTelemetryLedger(ledger_path)

    @staticmethod
    def calculate_cost(
        prompt_tokens: int,
        completion_tokens: int,
        tier: str = "standard",
    ) -> float:
        """Calculate inference cost in USD based on complexity tier rates."""
        tier_key = tier.lower() if tier.lower() in DEFAULT_TIER_PRICING else "standard"
        pricing = DEFAULT_TIER_PRICING[tier_key]
        input_cost = (prompt_tokens / 1_000_000.0) * pricing["input"]
        output_cost = (completion_tokens / 1_000_000.0) * pricing["output"]
        return round(input_cost + output_cost, 8)

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Heuristic subword token estimation (approx 4 characters per token)."""
        if not text:
            return 0
        return max(1, math.ceil(len(text) / 4.0))

    def record_prompt(
        self,
        prompt: str,
        user_id: str,
        model: str = "claude-3-5-sonnet",
        tier: str = "standard",
        completion: str = "",
        prompt_tokens: Optional[int] = None,
        completion_tokens: Optional[int] = None,
        latency_ms: float = 0.0,
        cached: bool = False,
        agent_id: str = "hath0r-agent",
        session_id: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> TokenTelemetryRecord:
        """Record and ingest an agent prompt and interaction into the telemetry ledger."""
        p_len = len(prompt)
        c_len = len(completion)
        p_tok = prompt_tokens if prompt_tokens is not None else self.estimate_tokens(prompt)
        c_tok = completion_tokens if completion_tokens is not None else self.estimate_tokens(completion)
        tot_tok = p_tok + c_tok

        cost = self.calculate_cost(prompt_tokens=p_tok, completion_tokens=c_tok, tier=tier)
        if cached:
            cost = 0.0

        record = TokenTelemetryRecord(
            user_id=user_id,
            agent_id=agent_id,
            session_id=session_id,
            prompt_length_chars=p_len,
            prompt_tokens=p_tok,
            completion_length_chars=c_len,
            completion_tokens=c_tok,
            total_tokens=tot_tok,
            model=model,
            tier=tier,
            cost_usd=cost,
            latency_ms=latency_ms,
            cached=cached,
            metadata=metadata or {},
        )

        self.ledger.append(record)
        return record

    def query_records(
        self,
        user_id: Optional[str] = None,
        model: Optional[str] = None,
        session_id: Optional[str] = None,
        tier: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[TokenTelemetryRecord]:
        """Query ingested records with filtering options."""
        return self.ledger.query(
            user_id=user_id,
            model=model,
            session_id=session_id,
            tier=tier,
            limit=limit,
        )

    def get_user_summary(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """Aggregate summary metrics by user identifier."""
        records = self.ledger.read_all()
        summary: Dict[str, Dict[str, Any]] = {}

        for r in records:
            uid = r.user_id
            if user_id and uid != user_id:
                continue
            if uid not in summary:
                summary[uid] = {
                    "total_requests": 0,
                    "total_prompt_chars": 0,
                    "total_prompt_tokens": 0,
                    "total_completion_tokens": 0,
                    "total_tokens": 0,
                    "total_cost_usd": 0.0,
                }
            s = summary[uid]
            s["total_requests"] += 1
            s["total_prompt_chars"] += r.prompt_length_chars
            s["total_prompt_tokens"] += r.prompt_tokens
            s["total_completion_tokens"] += r.completion_tokens
            s["total_tokens"] += r.total_tokens
            s["total_cost_usd"] = round(s["total_cost_usd"] + r.cost_usd, 6)

        return summary


@dataclass
class HistogramBin:
    """A single interval bucket within a statistical histogram."""

    bin_index: int
    bin_start: float
    bin_end: float
    count: int
    percentage: float
    cumulative_percentage: float
    ascii_bar: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bin_index": self.bin_index,
            "bin_start": round(self.bin_start, 2),
            "bin_end": round(self.bin_end, 2),
            "count": self.count,
            "percentage": round(self.percentage, 2),
            "cumulative_percentage": round(self.cumulative_percentage, 2),
            "ascii_bar": self.ascii_bar,
        }


class TokenHistogramBot:
    """Builds statistical distributions, percentiles, and visual histograms of agent token data."""

    VALID_METRICS = ["prompt_tokens", "prompt_length_chars", "total_tokens", "cost_usd"]

    @classmethod
    def _extract_metric_values(
        cls,
        records: List[TokenTelemetryRecord],
        metric: str,
    ) -> List[float]:
        values: List[float] = []
        for r in records:
            if metric == "prompt_tokens":
                values.append(float(r.prompt_tokens))
            elif metric == "prompt_length_chars":
                values.append(float(r.prompt_length_chars))
            elif metric == "total_tokens":
                values.append(float(r.total_tokens))
            elif metric == "cost_usd":
                values.append(float(r.cost_usd))
            else:
                values.append(float(r.prompt_tokens))
        return values

    @classmethod
    def _compute_stats(cls, values: List[float]) -> Dict[str, float]:
        if not values:
            return {
                "min": 0.0,
                "max": 0.0,
                "mean": 0.0,
                "median": 0.0,
                "p90": 0.0,
                "p95": 0.0,
                "p99": 0.0,
                "std_dev": 0.0,
            }
        s_vals = sorted(values)
        n = len(s_vals)
        v_min = s_vals[0]
        v_max = s_vals[-1]
        mean = sum(s_vals) / n

        def _percentile(p: float) -> float:
            k = (n - 1) * p
            f = math.floor(k)
            c = math.ceil(k)
            if f == c:
                return s_vals[int(k)]
            d0 = s_vals[int(f)] * (c - k)
            d1 = s_vals[int(c)] * (k - f)
            return d0 + d1

        median = _percentile(0.50)
        p90 = _percentile(0.90)
        p95 = _percentile(0.95)
        p99 = _percentile(0.99)

        variance = sum((x - mean) ** 2 for x in s_vals) / n
        std_dev = math.sqrt(variance)

        return {
            "min": round(v_min, 4),
            "max": round(v_max, 4),
            "mean": round(mean, 4),
            "median": round(median, 4),
            "p90": round(p90, 4),
            "p95": round(p95, 4),
            "p99": round(p99, 4),
            "std_dev": round(std_dev, 4),
        }

    @classmethod
    def build_histogram(
        cls,
        records: List[TokenTelemetryRecord],
        metric: str = "prompt_tokens",
        bins_count: int = 10,
        max_bar_width: int = 30,
    ) -> Dict[str, Any]:
        """Construct statistical histogram with bins, percentiles, and breakdown aggregates."""
        if metric not in cls.VALID_METRICS:
            metric = "prompt_tokens"

        total_records = len(records)
        total_tokens = sum(r.total_tokens for r in records)
        total_cost_usd = round(sum(r.cost_usd for r in records), 6)

        user_dist: Dict[str, Dict[str, Any]] = {}
        model_dist: Dict[str, Dict[str, Any]] = {}

        for r in records:
            # User aggregation
            if r.user_id not in user_dist:
                user_dist[r.user_id] = {"count": 0, "tokens": 0, "cost_usd": 0.0}
            user_dist[r.user_id]["count"] += 1
            user_dist[r.user_id]["tokens"] += r.total_tokens
            user_dist[r.user_id]["cost_usd"] = round(user_dist[r.user_id]["cost_usd"] + r.cost_usd, 6)

            # Model aggregation
            if r.model not in model_dist:
                model_dist[r.model] = {"count": 0, "tokens": 0, "cost_usd": 0.0}
            model_dist[r.model]["count"] += 1
            model_dist[r.model]["tokens"] += r.total_tokens
            model_dist[r.model]["cost_usd"] = round(model_dist[r.model]["cost_usd"] + r.cost_usd, 6)

        values = cls._extract_metric_values(records, metric)
        stats = cls._compute_stats(values)

        if not values or stats["min"] == stats["max"]:
            # Handle uniform or empty distribution
            single_val = stats["min"]
            bins = [
                HistogramBin(
                    bin_index=0,
                    bin_start=single_val,
                    bin_end=single_val,
                    count=total_records,
                    percentage=100.0 if total_records > 0 else 0.0,
                    cumulative_percentage=100.0 if total_records > 0 else 0.0,
                    ascii_bar="█" * max_bar_width if total_records > 0 else "",
                ).to_dict()
            ]
            return {
                "metric": metric,
                "total_records": total_records,
                "total_tokens": total_tokens,
                "total_cost_usd": total_cost_usd,
                "stats": stats,
                "bins": bins,
                "user_distribution": user_dist,
                "model_distribution": model_dist,
            }

        # Divide [min, max] into equal-width bins
        v_min = stats["min"]
        v_max = stats["max"]
        bin_width = (v_max - v_min) / float(bins_count)
        bin_counts = [0] * bins_count

        for v in values:
            idx = int((v - v_min) / bin_width)
            if idx >= bins_count:
                idx = bins_count - 1
            bin_counts[idx] += 1

        max_count = max(bin_counts) if bin_counts else 1
        cum_count = 0
        bin_objects: List[Dict[str, Any]] = []

        for i in range(bins_count):
            start = v_min + i * bin_width
            end = v_min + (i + 1) * bin_width
            cnt = bin_counts[i]
            pct = (cnt / total_records) * 100.0 if total_records > 0 else 0.0
            cum_count += cnt
            cum_pct = (cum_count / total_records) * 100.0 if total_records > 0 else 0.0

            bar_len = int((cnt / max_count) * max_bar_width) if max_count > 0 else 0
            ascii_bar = "█" * bar_len

            b = HistogramBin(
                bin_index=i,
                bin_start=start,
                bin_end=end,
                count=cnt,
                percentage=pct,
                cumulative_percentage=cum_pct,
                ascii_bar=ascii_bar,
            )
            bin_objects.append(b.to_dict())

        return {
            "metric": metric,
            "total_records": total_records,
            "total_tokens": total_tokens,
            "total_cost_usd": total_cost_usd,
            "stats": stats,
            "bins": bin_objects,
            "user_distribution": user_dist,
            "model_distribution": model_dist,
        }

    @classmethod
    def render_ascii(cls, histogram_data: Dict[str, Any]) -> str:
        """Render a clean ASCII distribution histogram for terminal output."""
        metric = histogram_data.get("metric", "prompt_tokens")
        tot = histogram_data.get("total_records", 0)
        st = histogram_data.get("stats", {})
        bins = histogram_data.get("bins", [])

        lines: List[str] = []
        lines.append(f"=== Hath0r FinOps Histogram [{metric}] (Total Records: {tot}) ===")
        lines.append(
            f"Mean: {st.get('mean', 0):.2f} | Median: {st.get('median', 0):.2f} | "
            f"P95: {st.get('p95', 0):.2f} | P99: {st.get('p99', 0):.2f} | StdDev: {st.get('std_dev', 0):.2f}"
        )
        lines.append("-" * 75)
        lines.append(f"{'Range':<22} | {'Count':<7} | {'%':<6} | {'Distribution'}")
        lines.append("-" * 75)

        for b in bins:
            start_str = f"{b['bin_start']:.1f}"
            end_str = f"{b['bin_end']:.1f}"
            rng = f"[{start_str} - {end_str}]"
            cnt = b["count"]
            pct = f"{b['percentage']:.1f}%"
            bar = b["ascii_bar"]
            lines.append(f"{rng:<22} | {cnt:<7} | {pct:<6} | {bar}")

        lines.append("-" * 75)
        return "\n".join(lines)

    @classmethod
    def generate_generative_ui_html(cls, histogram_data: Dict[str, Any]) -> str:
        """Generate standalone interactive Generative UI dashboard HTML widget."""
        metric = histogram_data.get("metric", "prompt_tokens")
        tot = histogram_data.get("total_records", 0)
        tot_tok = histogram_data.get("total_tokens", 0)
        cost = histogram_data.get("total_cost_usd", 0.0)
        st = histogram_data.get("stats", {})
        bins = histogram_data.get("bins", [])

        bin_bars = ""
        for b in bins:
            height_pct = max(4, int(b.get("percentage", 0)))
            bin_bars += f"""
            <div style="flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: flex-end; margin: 0 3px;">
              <div style="font-size: 10px; color: #64748b; margin-bottom: 4px;">{b['count']}</div>
              <div style="width: 100%; height: {height_pct * 2}px; background: linear-gradient(180deg, #3b82f6 0%, #1d4ed8 100%); border-radius: 4px 4px 0 0;" title="Range: {b['bin_start']} - {b['bin_end']} ({b['percentage']}%)"></div>
              <div style="font-size: 9px; color: #94a3b8; margin-top: 6px; transform: rotate(-45deg); white-space: nowrap;">{b['bin_start']:.0f}</div>
            </div>
            """

        html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Hath0r Token Telemetry Histogram</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 24px; margin: 0; }}
    .card {{ background: #1e293b; border-radius: 12px; padding: 24px; max-width: 800px; margin: 0 auto; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3); }}
    .title {{ font-size: 20px; font-weight: 700; color: #38bdf8; margin-bottom: 4px; }}
    .subtitle {{ font-size: 13px; color: #94a3b8; margin-bottom: 20px; }}
    .metrics-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 24px; }}
    .metric-box {{ background: #0f172a; padding: 12px; border-radius: 8px; border: 1px solid #334155; }}
    .metric-val {{ font-size: 18px; font-weight: 700; color: #f1f5f9; }}
    .metric-lbl {{ font-size: 11px; color: #64748b; text-transform: uppercase; margin-top: 2px; }}
    .chart-container {{ background: #0f172a; border-radius: 8px; padding: 20px; height: 260px; display: flex; align-items: flex-end; border: 1px solid #334155; margin-bottom: 20px; }}
  </style>
</head>
<body>
  <div class="card">
    <div class="title">Hath0r Agent Token Telemetry Histogram</div>
    <div class="subtitle">Dimension: <strong>{metric}</strong> • Ingested via TokenTelemetryBot</div>

    <div class="metrics-grid">
      <div class="metric-box">
        <div class="metric-val">{tot:,}</div>
        <div class="metric-lbl">Total Requests</div>
      </div>
      <div class="metric-box">
        <div class="metric-val">{tot_tok:,}</div>
        <div class="metric-lbl">Total Tokens</div>
      </div>
      <div class="metric-box">
        <div class="metric-val">${cost:.4f}</div>
        <div class="metric-lbl">Total Spend (USD)</div>
      </div>
      <div class="metric-box">
        <div class="metric-val">{st.get('median', 0):.1f}</div>
        <div class="metric-lbl">Median {metric}</div>
      </div>
    </div>

    <div class="chart-container">
      {bin_bars}
    </div>

    <div style="font-size: 12px; color: #64748b; text-align: right;">
      P95: {st.get('p95', 0):.1f} • P99: {st.get('p99', 0):.1f} • StdDev: {st.get('std_dev', 0):.2f}
    </div>
  </div>
</body>
</html>"""
        return html
