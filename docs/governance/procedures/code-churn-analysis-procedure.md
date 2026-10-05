# Procedure: Code Churn & Hotspot Analysis

> Canonical Standard Operating Procedure · Hath0r Agentic Framework  
> Updated: 2026-10-05

## 1. Scope & Objective

This procedure details the step-by-step operational instructions for auditing code churn, generating architectural hotspot reports, evaluating PR risk, and injecting volatility data into AgentGraph.

---

## 2. CLI Execution & Automated Analysis

### Step 1: Pre-Audit Environment Validation
Verify that the repository working tree is accessible and clean:
```bash
hath0r churn doctor
```

### Step 2: Run Churn Analysis
Execute 30-day commit volatility analysis across the active repository:
```bash
hath0r churn analyze --days 30 --json
```

### Step 3: Inspect Hotspot Rankings
Retrieve the top 10 highest-volatility files in the workspace:
```bash
hath0r churn hotspots --limit 10
```

### Step 4: Evaluate PR Review Risk Gate
Before merging a feature branch, run PR risk evaluation against the target base:
```bash
hath0r churn pr-risk --base development
```

### Step 5: Render Generative UI Heatmap
Launch or view the interactive Generative UI dashboard:
```bash
hath0r churn ui
```

---

## 3. Contract Schema Compliance

All generated churn reports MUST validate against:
`contracts/hath0r-pmat-churn-report-v1.schema.json`
