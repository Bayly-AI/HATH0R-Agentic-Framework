# FinOps Token Ingestion & Histogram Analytics Playbook

> Issue: #188 · Status: Approved · Role: Hath0r Cognitive Substrate FinOps

## Overview

Step-by-step diagnostic and operational playbook for configuring, testing, and troubleshooting token telemetry collection and histogram generation.

## Playbook Execution

### Step 1: Verify Telemetry Ledger
```bash
# Verify ledger exists and inspect recent token records
hath0r finops tokens list --limit 10
```

### Step 2: Ingest Sample Prompt Token Telemetry
```bash
# Record prompt telemetry directly
hath0r finops tokens record --user "raybayly" --prompt "Analyze system metrics" --model "claude-3-5-sonnet" --tier "standard"
```

### Step 3: Generate Token Length Histogram
```bash
# Render prompt token histogram across all users
hath0r finops tokens histogram --metric prompt_tokens --bins 10

# Filter histogram specifically for a user
hath0r finops tokens histogram --user "raybayly" --metric prompt_length_chars
```

### Step 4: Cost Analysis & Anomaly Detection
- If `p99` prompt tokens exceed 8,000 tokens, trigger prompt compression inspection (`hath0r finops tokenizer-tax`).
- Inspect total cost breakdown across user identifiers to identify high-cost anomalies.
