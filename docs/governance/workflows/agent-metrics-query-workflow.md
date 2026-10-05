# Workflow: Agent Metrics Query & Report Generation Workflow

> Canonical Workflow Definition · Hath0r Agentic Framework  
> Updated: 2026-10-05

```mermaid
flowchart TD
    A["Trigger: Request for Agent Metrics ('show agent metrics')"] --> B["Initialize AgentMetricsBot"]
    B --> C["Extract Observability Metrics & Latency Quantiles"]
    B --> D["Extract Token Telemetry Histogram Distribution"]
    B --> E["Extract PMAT Code Churn, Complexity & Provability"]
    C & D & E --> F["Construct Schema Payload hath0r-agent-metrics-report-v1.schema.json"]
    F --> G{"TUI Format Requested & Environment Supported?"}
    G -- Yes --> H["Render Rich TUI Scorecard & Charts"]
    G -- No --> I["Render Graceful Markdown (MD) Fallback"]
    H & I --> J["Ingest Node into AgentGraph ContextPlane"]
    J --> K["Return Operational Report to User / TUI"]
```

## Supported Intent Triggers
1. `"show agent metrics"`
2. `"get agent metrics"`
3. `"agent metrics report"`
4. `"show metrics"`
5. `"display agent metrics"`
