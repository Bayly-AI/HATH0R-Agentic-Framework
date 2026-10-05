# Procedure: Agent Metrics Extraction & Report Rendering

> Canonical Operational Procedure · Hath0r Agentic Framework  
> Updated: 2026-10-05

## 1. Scope & Prerequisites

This procedure outlines the step-by-step process for extracting telemetry, histogram distributions, and PMAT stats using `AgentMetricsBot`.

Prerequisites:
- Hath0r Framework repository context (`src/hath0r_engine/`)
- Active telemetry ledger (`.hath0r/finops/token_telemetry.jsonl` or fallback mock telemetry)
- Active AgentGraph substrate (`.hath0r/agentgraph/`)

---

## 2. Step-by-Step Execution Sequence

1. **Trigger Intent Matching**:
   Inspect operator request for trigger intents (e.g. `"show agent metrics"`, `"get agent metrics"`, `"agent metrics report"`).

2. **Query Subsystems**:
   - Query `ObservationChartsEngine.compute_performance_metrics()` for latencies, total requests, tokens, spend, and `CICCCDTelemetryHook` for calibration drift.
   - Query `TokenHistogramBot.build_histogram()` for metric statistical distributions and percentile bins.
   - Query `PmatStatsEngine.generate_multi_dimensional_report()` for churn volatility, formal provability, AST complexity, and hotspot risk indices.

3. **Contract Validation**:
   Validate aggregated report dictionary against `contracts/hath0r-agent-metrics-report-v1.schema.json`.

4. **Dual-Mode Rendering**:
   - Execute `AgentMetricsBot.render_tui(report)`.
   - If rendering succeeds, output styled TUI.
   - If TUI fails or markdown mode is requested, apply `AgentMetricsBot.render_markdown(report)` as graceful fallback.

5. **AgentGraph Context Ingestion**:
   Execute `AgentMetricsBot.ingest_into_agentgraph(report)` to update the framework's quad-graph memory.
