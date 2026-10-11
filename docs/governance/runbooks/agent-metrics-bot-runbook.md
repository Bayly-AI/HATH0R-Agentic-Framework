# Runbook: Agent Metrics Bot Operational Runbook

> Canonical Operational Runbook · Hath0r Agentic Framework  
> Updated: 2026-10-05

## 1. System Overview

`AgentMetricsBot` services operator and agent requests for performance observability, token telemetry histograms, and PMAT multi-dimensional code churn / provability stats. It displays rich TUI dashboards on interactive terminals with graceful Markdown fallbacks.

---

## 2. Diagnostics & Operator Commands

### Run via Operator CLI / Python Subsystem
```python
from hath0r_engine.bots import agent_metrics_bot

# Process intent and return full payload with TUI / Markdown output
result = agent_metrics_bot.run(intent="show agent metrics")
print(result["output"])
```

### CLI Command Execution
```bash
hath0r bot run agent-metrics-bot --intent "show agent metrics"
```

---

## 3. Troubleshooting & Failure Modes

| Issue | Cause | Resolution |
| :--- | :--- | :--- |
| TUI Rendering Distorted | Terminal lacks rich formatting support | Bot automatically applies Markdown fallback (`render_markdown`) |
| Empty Telemetry Ledger | No interactions recorded yet | Engine generates baseline synthetic telemetry for display |
| Stale Calibration Warning | `cccd_state.json` missing or $> 24\text{h}$ old | Run `hath0r cccd calibrate` to re-synchronize |
