# Workflow: Automated Code Churn Audit

> Canonical Workflow Definition · Hath0r Agentic Framework  
> Updated: 2026-10-05

```mermaid
flowchart TD
    A["Trigger: Scheduled Cron / PR Opening"] --> B["Execute hath0r churn analyze"]
    B --> C["Extract Hotspots & Volatility Scores"]
    C --> D{"Max Volatility >= 0.75?"}
    D -- Yes --> E["Mark PR Risk as CRITICAL"]
    E --> F["Escalate TieredRouter to REASONING (o3-mini)"]
    F --> G["Propose Modular Refactoring Plan via HotspotRefactorBot"]
    D -- No --> H["Ingest Volatility Nodes into AgentGraph"]
    H --> I["Generate Generative UI Churn Heatmap"]
    I --> J["Pass Clean Repo Gate (Step 7)"]
```

## Step Details
1. **Trigger**: Scheduled heartbeat or PR pre-flight evaluation.
2. **Analysis**: Fast extraction via `PmatAdapter`.
3. **Graph Ingestion**: Write `file_hotspot` nodes and `CO_CHANGES_WITH` edges to `AgentGraph`.
4. **Evidence Emission**: Emit `ChurnHeatmapComponent` for operator inspection.
