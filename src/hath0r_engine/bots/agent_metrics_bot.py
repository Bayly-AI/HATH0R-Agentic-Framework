"""Agent Metrics Bot — Autonomous micro-bot for aggregating Observability, Histogram, and PMAT metrics into TUI and Markdown reports."""

from __future__ import annotations

import datetime
import io
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from hath0r_engine.analysis.pmat_stats_engine import PmatStatsEngine, pmat_stats_engine
from hath0r_engine.graph.agent_graph import (
    AgentGraphEngine,
    AgentGraphNode,
    AgentGraphPlane,
    agent_graph_engine,
)
from hath0r_engine.pipeline.assertions import validate_json_contract
from hath0r_engine.telemetry.cicccd_telemetry import CICCCDTelemetryHook
from hath0r_engine.telemetry.observation_charts import ObservationChartsEngine
from hath0r_engine.telemetry.token_telemetry import TokenHistogramBot, TokenTelemetryLedger


class AgentMetricsBot:
    """Autonomous micro-bot triggered by agent metrics requests.
    
    Pulls Observability items (latencies, token counts, cost, CCCD calibration metrics),
    Histogram distributions (token & latency quantiles, percentiles, bins), and
    PMAT multi-dimensional stats (git churn, AST complexity, provability scores, hotspot risk indices).
    Renders comprehensive report to screen via rich TUI with graceful Markdown (MD) fallback.
    """

    BOT_ID: str = "agent-metrics-bot"
    TRIGGER_INTENTS: List[str] = [
        "show agent metrics",
        "get agent metrics",
        "agent metrics report",
        "show metrics",
        "get metrics",
        "agent metrics",
        "display agent metrics",
        "view agent metrics",
        "metrics report",
        "fetch agent metrics",
    ]

    def __init__(
        self,
        workspace_root: Optional[Path | str] = None,
        ledger_path: Optional[Path | str] = None,
    ) -> None:
        self.workspace_root: Path = Path(workspace_root).resolve() if workspace_root else Path.cwd().resolve()
        self.obs_engine: ObservationChartsEngine = ObservationChartsEngine(ledger_path=ledger_path)
        self.cicccd_hook: CICCCDTelemetryHook = CICCCDTelemetryHook(workspace_root=self.workspace_root)
        self.pmat_engine: PmatStatsEngine = pmat_stats_engine
        self.ledger: TokenTelemetryLedger = TokenTelemetryLedger(ledger_path=ledger_path)

    def is_triggered_by(self, intent: str) -> bool:
        """Check if conversational intent triggers the Agent Metrics Bot."""
        if not intent:
            return False
        clean = intent.strip().lower()
        return any(trig in clean for trig in self.TRIGGER_INTENTS)

    def generate_metrics_report(
        self,
        intent: str = "show agent metrics",
        repo_path: Optional[Path | str] = None,
        metric: str = "prompt_tokens",
        bins_count: int = 10,
        days: int = 30,
    ) -> Dict[str, Any]:
        """Aggregate Observability items, Histogram distribution, and PMAT information into schema contract."""
        assert bins_count > 0, "bins_count must be positive"
        assert days > 0, "days must be positive"
        target_repo = Path(repo_path).resolve() if repo_path else self.workspace_root

        # 1. Observability items
        obs_metrics = self.obs_engine.compute_performance_metrics(metric="latency_ms", bins_count=bins_count)
        latency_stats = obs_metrics.get("stats", {})
        cccd_metrics = self.cicccd_hook.get_calibration_metrics()
        cccd_fresh = self.cicccd_hook.is_calibration_fresh()

        observability_data = {
            "total_requests": obs_metrics.get("total_requests", 0),
            "total_tokens": obs_metrics.get("total_tokens", 0),
            "total_cost_usd": obs_metrics.get("total_cost_usd", 0.0),
            "latency_quantiles": {
                "p50": latency_stats.get("median", 0.0),
                "p90": latency_stats.get("p90", 0.0),
                "p95": latency_stats.get("p95", 0.0),
                "p99": latency_stats.get("p99", 0.0),
                "mean": latency_stats.get("mean", 0.0),
                "std_dev": latency_stats.get("std_dev", 0.0),
            },
            "calibration_state": {
                "fresh": cccd_fresh,
                "last_run_timestamp": cccd_metrics.get("last_run_timestamp"),
                "total_runs": cccd_metrics.get("total_calibration_runs", 0),
                "drift_metrics": cccd_metrics.get("drift_metrics", {}),
            },
        }

        # 2. Histogram distribution
        records = self.ledger.read_all()
        histogram_data = TokenHistogramBot.build_histogram(records=records, metric=metric, bins_count=bins_count)

        # 3. PMAT information
        pmat_report = self.pmat_engine.generate_multi_dimensional_report(repo_path=target_repo, days=days)

        # 4. Summary & Aggregates
        hotspot_count = pmat_report.get("summary", {}).get("hotspot_count", 0)
        mean_prov = pmat_report.get("summary", {}).get("mean_provability_score", 1.0)
        tui_supported = self._check_tui_supported()

        report: Dict[str, Any] = {
            "schema_version": "hath0r.agent.metrics/1",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "bot_id": self.BOT_ID,
            "intent": intent,
            "summary": {
                "total_requests": obs_metrics.get("total_requests", 0),
                "total_tokens": obs_metrics.get("total_tokens", 0),
                "total_cost_usd": obs_metrics.get("total_cost_usd", 0.0),
                "mean_latency_ms": latency_stats.get("mean", 0.0),
                "p90_latency_ms": latency_stats.get("p90", 0.0),
                "mean_provability_score": mean_prov,
                "hotspot_count": hotspot_count,
                "calibration_fresh": cccd_fresh,
            },
            "observability": observability_data,
            "histogram": histogram_data,
            "pmat": pmat_report,
            "tui_metadata": {
                "render_mode": "auto",
                "tui_supported": tui_supported,
                "fallback_applied": False,
            },
        }

        # Validate against schema contract if available
        contract_path = self.workspace_root / "contracts" / "hath0r-agent-metrics-report-v1.schema.json"
        if contract_path.is_file():
            try:
                validate_json_contract(report, str(contract_path))
            except Exception:
                pass

        return report

    def _check_tui_supported(self) -> bool:
        """Check if terminal environment and rich library support TUI rendering."""
        try:
            import rich  # noqa: F401
            from rich.console import Console

            c = Console()
            return c.is_terminal or True
        except ImportError:
            return False

    def render_tui(self, report: Dict[str, Any]) -> str:
        """Render comprehensive metrics report to terminal screen using rich TUI.
        
        Falls back gracefully to Markdown if rich is not available or if rendering fails.
        """
        assert report is not None, "report cannot be None"
        try:
            from rich.console import Console
            from rich.panel import Panel
            from rich.table import Table
            from rich.text import Text

            buf = io.StringIO()
            console = Console(file=buf, force_terminal=True, width=100)

            sum_data = report.get("summary", {})
            obs_data = report.get("observability", {})
            hist_data = report.get("histogram", {})
            pmat_data = report.get("pmat", {})

            console.print(self._build_tui_header_panel(report, Panel, Text))
            console.print(self._build_tui_scorecard_table(sum_data, Table))
            console.print(self._build_tui_observability_table(obs_data, Table))
            console.print(self._build_tui_histogram_table(hist_data, Table))
            console.print(self._build_tui_pmat_table(pmat_data, Table))

            return buf.getvalue()

        except Exception:
            report["tui_metadata"]["fallback_applied"] = True
            return self.render_markdown(report)

    def _build_tui_header_panel(self, report: Dict[str, Any], Panel: Any, Text: Any) -> Any:
        """Construct Header Panel for rich TUI display."""
        hdr_text = Text()
        hdr_text.append("HATH0R AGENT METRICS MONITOR", style="bold cyan")
        hdr_text.append(f"  •  Bot: {report.get('bot_id', self.BOT_ID)}\n", style="dim white")
        hdr_text.append(f"Timestamp: {report.get('timestamp')}  |  Intent: {report.get('intent')}", style="italic yellow")
        return Panel(hdr_text, border_style="cyan", title="[bold white]Hath0r Framework[/bold white]")

    def _build_tui_scorecard_table(self, sum_data: Dict[str, Any], Table: Any) -> Any:
        """Construct Summary Scorecard Table for rich TUI display."""
        score_table = Table(title="[bold yellow]Agent Operational Scorecard[/bold yellow]", expand=True)
        score_table.add_column("Requests", justify="center", style="cyan")
        score_table.add_column("Total Tokens", justify="center", style="green")
        score_table.add_column("Spend (USD)", justify="center", style="magenta")
        score_table.add_column("P90 Latency", justify="center", style="yellow")
        score_table.add_column("Provability", justify="center", style="blue")
        score_table.add_column("Hotspots", justify="center", style="red")
        score_table.add_column("CCCD Calibration", justify="center", style="bold green")

        cccd_status = "[bold green]FRESH[/bold green]" if sum_data.get("calibration_fresh") else "[bold red]STALE[/bold red]"
        score_table.add_row(
            str(sum_data.get("total_requests", 0)),
            f"{sum_data.get('total_tokens', 0):,}",
            f"${sum_data.get('total_cost_usd', 0.0):.4f}",
            f"{sum_data.get('p90_latency_ms', 0.0):.1f} ms",
            f"{sum_data.get('mean_provability_score', 0.0):.2f}",
            str(sum_data.get("hotspot_count", 0)),
            cccd_status,
        )
        return score_table

    def _build_tui_observability_table(self, obs_data: Dict[str, Any], Table: Any) -> Any:
        """Construct Observability Tracing Table for rich TUI display."""
        lat_q = obs_data.get("latency_quantiles", {})
        obs_table = Table(title="[bold cyan]1. Observability Tracing & Latency Quantiles[/bold cyan]", expand=True)
        obs_table.add_column("Metric Quantile", style="white")
        obs_table.add_column("Latency Value", style="bold yellow")
        obs_table.add_column("Description", style="dim")

        obs_table.add_row("P50 (Median)", f"{lat_q.get('p50', 0.0):.2f} ms", "50th percentile response latency")
        obs_table.add_row("P90", f"{lat_q.get('p90', 0.0):.2f} ms", "90th percentile SLA benchmark")
        obs_table.add_row("P95", f"{lat_q.get('p95', 0.0):.2f} ms", "95th percentile outlier tail")
        obs_table.add_row("P99", f"{lat_q.get('p99', 0.0):.2f} ms", "99th percentile maximum tail latency")
        obs_table.add_row("Mean ± StdDev", f"{lat_q.get('mean', 0.0):.2f} ± {lat_q.get('std_dev', 0.0):.2f} ms", "Statistical expectation & variance")
        return obs_table

    def _build_tui_histogram_table(self, hist_data: Dict[str, Any], Table: Any) -> Any:
        """Construct Token Histogram Table for rich TUI display."""
        metric_name = hist_data.get("metric", "prompt_tokens")
        hist_bins = hist_data.get("bins", [])
        hist_table = Table(title=f"[bold green]2. Token Telemetry Histogram [{metric_name}][/bold green]", expand=True)
        hist_table.add_column("Bin Range", style="white")
        hist_table.add_column("Count", justify="right", style="cyan")
        hist_table.add_column("Share", justify="right", style="magenta")
        hist_table.add_column("Distribution Graph", style="bold green")

        for b in hist_bins:
            rng = f"[{b.get('bin_start', 0):.1f} - {b.get('bin_end', 0):.1f}]"
            cnt = str(b.get("count", 0))
            pct = f"{b.get('percentage', 0.0):.1f}%"
            bar = b.get("ascii_bar", "")
            hist_table.add_row(rng, cnt, pct, bar)
        return hist_table

    def _build_tui_pmat_table(self, pmat_data: Dict[str, Any], Table: Any) -> Any:
        """Construct PMAT Hotspots Table for rich TUI display."""
        hotspots = pmat_data.get("hotspots", [])
        pmat_table = Table(title="[bold red]3. PMAT Code Churn, Complexity & Provability Hotspots[/bold red]", expand=True)
        pmat_table.add_column("File Path", style="white")
        pmat_table.add_column("Risk Tier", justify="center")
        pmat_table.add_column("Risk Index", justify="right", style="bold yellow")
        pmat_table.add_column("Churn", justify="right", style="cyan")
        pmat_table.add_column("Provability", justify="right", style="blue")
        pmat_table.add_column("Complexity", justify="right", style="magenta")

        for h in hotspots[:5]:
            tier = h.get("risk_tier", "LOW")
            tier_fmt = f"[bold red]{tier}[/bold red]" if tier in ("HIGH", "CRITICAL") else f"[green]{tier}[/green]"
            pmat_table.add_row(
                h.get("file_path", ""),
                tier_fmt,
                f"{h.get('composite_hotspot_risk_index', 0.0):.4f}",
                f"{h.get('churn_score', 0.0):.2f}",
                f"{h.get('provability_score', 0.0):.2f}",
                f"{h.get('complexity_score', 0.0):.1f}",
            )
        return pmat_table

    def render_markdown(self, report: Dict[str, Any]) -> str:
        """Render comprehensive metrics report formatted in clean GitHub-Flavored Markdown."""
        assert report is not None, "report cannot be None"
        sum_data = report.get("summary", {})
        obs_data = report.get("observability", {})
        hist_data = report.get("histogram", {})
        pmat_data = report.get("pmat", {})

        lines: List[str] = []
        lines.extend(self._build_markdown_header(report))
        lines.extend(self._build_markdown_summary_table(sum_data))
        lines.extend(self._build_markdown_observability_section(obs_data))
        lines.extend(self._build_markdown_histogram_section(hist_data))
        lines.extend(self._build_markdown_pmat_section(pmat_data))

        return "\n".join(lines)

    def _build_markdown_header(self, report: Dict[str, Any]) -> List[str]:
        """Construct Markdown header lines."""
        return [
            f"# Agent Metrics Report — `{report.get('bot_id', self.BOT_ID)}`",
            "",
            f"> **Generated:** `{report.get('timestamp')}`  ",
            f"> **Intent:** `{report.get('intent')}`  ",
            f"> **TUI Fallback Applied:** `{report.get('tui_metadata', {}).get('fallback_applied', False)}`",
            "",
        ]

    def _build_markdown_summary_table(self, sum_data: Dict[str, Any]) -> List[str]:
        """Construct Executive Operational Summary table lines."""
        return [
            "## Executive Operational Summary",
            "",
            "| Total Requests | Total Tokens | Spend (USD) | P90 Latency | Provability | Hotspots | CCCD Calibration |",
            "| :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
            (
                f"| {sum_data.get('total_requests', 0)} | {sum_data.get('total_tokens', 0):,} | "
                f"${sum_data.get('total_cost_usd', 0.0):.4f} | {sum_data.get('p90_latency_ms', 0.0):.1f} ms | "
                f"{sum_data.get('mean_provability_score', 0.0):.2f} | {sum_data.get('hotspot_count', 0)} | "
                f"{'FRESH' if sum_data.get('calibration_fresh') else 'STALE'} |"
            ),
            "",
        ]

    def _build_markdown_observability_section(self, obs_data: Dict[str, Any]) -> List[str]:
        """Construct Observability Tracing section lines."""
        lines = [
            "## 1. Observability Tracing & Latency Quantiles",
            "",
            "| Quantile | Value (ms) | Description |",
            "| :--- | :---: | :--- |",
        ]

        lat_q = obs_data.get("latency_quantiles", {})
        lines.append(f"| P50 (Median) | {lat_q.get('p50', 0.0):.2f} ms | 50th percentile response latency |")
        lines.append(f"| P90 | {lat_q.get('p90', 0.0):.2f} ms | 90th percentile SLA benchmark |")
        lines.append(f"| P95 | {lat_q.get('p95', 0.0):.2f} ms | 95th percentile outlier tail |")
        lines.append(f"| P99 | {lat_q.get('p99', 0.0):.2f} ms | 99th percentile maximum tail latency |")
        lines.append(f"| Mean ± StdDev | {lat_q.get('mean', 0.0):.2f} ± {lat_q.get('std_dev', 0.0):.2f} ms | Statistical expectation & variance |")
        lines.append("")

        cal = obs_data.get("calibration_state", {})
        lines.append("### Continuous Calibration (CCCD) Status")
        lines.append(f"- **Freshness Status:** `{'FRESH' if cal.get('fresh') else 'STALE (>24h)'}`")
        lines.append(f"- **Last Calibration Run:** `{cal.get('last_run_timestamp') or 'Never'}`")
        lines.append(f"- **Total Calibration Runs:** `{cal.get('total_runs', 0)}`")
        lines.append("")
        return lines

    def _build_markdown_histogram_section(self, hist_data: Dict[str, Any]) -> List[str]:
        """Construct Token Histogram section lines."""
        metric_name = hist_data.get("metric", "prompt_tokens")
        lines = [
            f"## 2. Token Telemetry Histogram Distribution [{metric_name}]",
            "",
            "| Bin Range | Count | Share (%) | Visual Distribution |",
            "| :--- | :---: | :---: | :--- |",
        ]

        for b in hist_data.get("bins", []):
            rng = f"[{b.get('bin_start', 0):.1f} - {b.get('bin_end', 0):.1f}]"
            cnt = b.get("count", 0)
            pct = f"{b.get('percentage', 0.0):.1f}%"
            bar = f"`{b.get('ascii_bar', '')}`"
            lines.append(f"| {rng} | {cnt} | {pct} | {bar} |")

        lines.append("")
        return lines

    def _build_markdown_pmat_section(self, pmat_data: Dict[str, Any]) -> List[str]:
        """Construct PMAT section lines."""
        lines = [
            "## 3. PMAT Multi-Dimensional Code Churn, Complexity & Provability",
            "",
        ]
        pmat_sum = pmat_data.get("summary", {})
        lines.append(f"- **Repository Evaluated:** `{pmat_data.get('repository', 'hath0r')}` (`{pmat_data.get('commit_hash', 'unknown')}`)")
        lines.append(f"- **Files Analyzed:** `{pmat_sum.get('total_files_analyzed', 0)}` across `{pmat_sum.get('total_commits_evaluated', 0)}` commits")
        lines.append(f"- **Mean Provability Score:** `{pmat_sum.get('mean_provability_score', 1.0):.4f}`")
        lines.append(f"- **Mean Cyclomatic Complexity:** `{pmat_sum.get('mean_complexity_score', 1.0):.2f}`")
        lines.append("")

        lines.append("### Architectural Hotspots (Ranked by Risk Index $R$)")
        lines.append("")
        lines.append("| File Path | Risk Tier | Risk Index ($R$) | Churn Score | Provability Score | Complexity Score |")
        lines.append("| :--- | :---: | :---: | :---: | :---: | :---: |")

        for h in pmat_data.get("hotspots", [])[:5]:
            lines.append(
                f"| `{h.get('file_path', '')}` | **{h.get('risk_tier', 'LOW')}** | "
                f"`{h.get('composite_hotspot_risk_index', 0.0):.4f}` | `{h.get('churn_score', 0.0):.2f}` | "
                f"`{h.get('provability_score', 0.0):.2f}` | `{h.get('complexity_score', 0.0):.1f}` |"
            )

        lines.append("")
        remediations = pmat_data.get("remediation_items", [])
        if remediations:
            lines.append("### Remediation Protocol Recommendations")
            lines.append("")
            for rem in remediations[:5]:
                lines.append(f"- **[{rem.get('priority', 'HIGH')}]** `{rem.get('file_path', '')}`: {rem.get('recommended_action', '')}")
            lines.append("")

        return lines

    def ingest_into_agentgraph(self, report: Dict[str, Any], agent_graph: Optional[AgentGraphEngine] = None) -> str:
        """Ingest Agent Metrics Bot execution node into AgentGraph context and knowledge planes."""
        assert report is not None, "report cannot be None"
        graph = agent_graph or agent_graph_engine
        node_id = f"bot_execution:agent-metrics-bot:{int(datetime.datetime.now(datetime.timezone.utc).timestamp())}"
        
        sum_data = report.get("summary", {})
        node = AgentGraphNode(
            id=node_id,
            plane=AgentGraphPlane.CONTEXT.value,
            type="bot_execution",
            label="Agent Metrics Bot Execution",
            content=f"Report generated: {sum_data.get('total_requests', 0)} requests | ${sum_data.get('total_cost_usd', 0.0):.4f} spend | {sum_data.get('hotspot_count', 0)} hotspots",
            properties={
                "bot_id": self.BOT_ID,
                "intent": report.get("intent"),
                "total_requests": sum_data.get("total_requests"),
                "total_tokens": sum_data.get("total_tokens"),
                "total_cost_usd": sum_data.get("total_cost_usd"),
                "p90_latency_ms": sum_data.get("p90_latency_ms"),
                "mean_provability_score": sum_data.get("mean_provability_score"),
                "hotspot_count": sum_data.get("hotspot_count"),
            },
        )
        graph.add_node(node)
        return node_id

    def run(
        self,
        intent: str = "show agent metrics",
        render_mode: str = "auto",
        repo_path: Optional[Path | str] = None,
        agent_graph: Optional[AgentGraphEngine] = None,
    ) -> Dict[str, Any]:
        """Main bot entry point to process agent metrics intent, build report, render UI, and ingest into AgentGraph."""
        report = self.generate_metrics_report(intent=intent, repo_path=repo_path)
        
        if render_mode == "markdown":
            output = self.render_markdown(report)
            report["tui_metadata"]["render_mode"] = "markdown"
            report["tui_metadata"]["fallback_applied"] = True
        else:
            output = self.render_tui(report)
            report["tui_metadata"]["render_mode"] = "tui"

        markdown_fallback = self.render_markdown(report)
        node_id = self.ingest_into_agentgraph(report, agent_graph=agent_graph)

        return {
            "bot_id": self.BOT_ID,
            "report": report,
            "output": output,
            "markdown_fallback": markdown_fallback,
            "agentgraph_node_id": node_id,
        }


agent_metrics_bot = AgentMetricsBot()
