# Bot Specification: AgentMetricsBot

> Canonical Bot Specification · Hath0r Agentic Framework  
> Updated: 2026-10-05

## 1. Role & Identity

- **Bot Name**: `agent-metrics-bot`
- **Class Name**: `AgentMetricsBot`
- **Subsystem**: `src/hath0r_engine/bots/agent_metrics_bot.py`
- **Primary Function**: Autonomous micro-bot servicing operator and agent requests for performance observability, token telemetry histograms, PMAT multi-dimensional code churn/provability stats, and dual-mode TUI/Markdown report rendering.

---

## 2. Supported Conversational Intents

1. `"show agent metrics"`
2. `"get agent metrics"`
3. `"agent metrics report"`
4. `"show metrics"`
5. `"get metrics"`
6. `"agent metrics"`
7. `"display agent metrics"`
8. `"view agent metrics"`
9. `"metrics report"`

---

## 3. RBAC Authorizations & Subsystems Interacted

- `ObservationChartsEngine`: Reads latency quantiles, total token counts, spend, and requests.
- `CICCCDTelemetryHook`: Reads calibration metrics and parameter drift.
- `TokenHistogramBot`: Reads percentile distributions and metric histogram bins.
- `PmatStatsEngine`: Reads polyglot code churn, AST complexity, formal provability scores, and hotspot risk indices.
- `AgentGraphEngine`: Ingests `bot_execution` nodes into the `ContextPlane`.
