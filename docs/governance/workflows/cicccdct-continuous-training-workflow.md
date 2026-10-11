# Workflow: CIC³DCT Continuous Training Lifecycle (CIC{qubed}DCT)

> **Document Type:** Workflow  
> **Status:** Ratified  
> **Governing Standards:** `CR-CICCCDCT-001`, `CR-BAI-001`  
> **Tracking Issues:** Bayly-AI/HATH0R-Agentic-Framework#255, #258

---

## 1. Trigger & Prerequisites

- **Schedule Trigger:** Weekly automated cron (`0 2 * * 0`) or drift event alert.
- **Prerequisites:** MLflow container running, OTel span logs available, golden benchmark suite present.

---

## 2. GitHub Actions / Local Workflow Sequence

```yaml
name: CICCCDCT Continuous Training & Evaluation

on:
  schedule:
    - cron: '0 2 * * 0' # Every Sunday at 02:00 UTC
  workflow_dispatch:

jobs:
  cicccdct-pipeline:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Validate Contracts & Schema (CI)
        run: hath0r contracts validate

      - name: Verify Calibration Freshness (CC)
        run: hath0r cicccdct calibrate

      - name: Curate Execution Traces (CT)
        run: hath0r cicccdct dataset curate --min-reward 0.75

      - name: Execute Model Fine-Tuning & Prompt Optimization (CT)
        run: hath0r cicccdct train run --target reasoning_slm --epochs 3

      - name: Multi-Stage Gate Validation (CI/CC/CD/CT)
        run: hath0r cicccdct validate
```
