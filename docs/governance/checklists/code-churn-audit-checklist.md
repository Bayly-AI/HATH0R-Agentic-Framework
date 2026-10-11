# Checklist: Code Churn & Hotspot Audit

> Canonical Verification Checklist · Hath0r Agentic Framework  
> Updated: 2026-10-05

- [ ] Working tree is clean and git metadata is accessible (`hath0r churn doctor`).
- [ ] 30-day commit churn analysis executed (`hath0r churn analyze`).
- [ ] Schema contract `hath0r-pmat-churn-report-v1.schema.json` validated.
- [ ] Hotspot rankings inspected for `CRITICAL` or `HIGH` volatility files.
- [ ] PR risk diff evaluated against `development` branch (`hath0r churn pr-risk`).
- [ ] `AgentGraph` updated with `file_hotspot` nodes and `CO_CHANGES_WITH` edges.
- [ ] Generative UI Churn Heatmap verified with Playwright test coverage.
