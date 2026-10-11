# Runbook: PMAT Analysis Engine Operations

> Canonical Operational Runbook · Hath0r Agentic Framework  
> Updated: 2026-10-05

## 1. System Overview

The PMAT (Pragmatic Multi-language Agent Toolkit) subsystem powers zero-prompt-tax code analysis, git churn calculation, and hotspot detection across all repositories.

## 2. Health Check & Diagnostics

Check adapter and CLI status:
```bash
hath0r churn doctor
```

Expected Output:
- PMAT CLI Adapter: Native / Git Fallback OK
- Git Repository Context: Valid HEAD
- Schema Contract: `contracts/hath0r-pmat-churn-report-v1.schema.json` verified

## 3. Troubleshooting & Failure Modes

| Issue | Cause | Resolution |
| :--- | :--- | :--- |
| `FileNotFoundError` | Target path is not a git workspace | Navigate to a valid git repository or specify `--repo <path>` |
| Stale Volatility Metrics | Commits older than analysis window | Increase analysis window: `--days 90` |
| Native PMAT binary missing | `pmat` not in system PATH | Subsystem automatically falls back to native git log parsing |
