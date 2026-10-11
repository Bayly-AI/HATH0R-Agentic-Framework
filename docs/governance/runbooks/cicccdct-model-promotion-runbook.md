# Runbook: MLflow Model Registry Promotion & Rollback (CIC³DCT / CIC{qubed}DCT)

> **Document Type:** Runbook  
> **Status:** Ratified  
> **Governing Standards:** `CR-CICCCDCT-001`, `CR-BAI-001`  
> **Tracking Issues:** Bayly-AI/HATH0R-Agentic-Framework#255, #258

---

## 1. Overview

This runbook guides operators through managing model versions in the MLflow Model Registry across promotion stages (`None`, `Staging`, `Production`) and rolling back to known good checkpoints during regressions.

---

## 2. Model Registry Stages

- `None`: Newly trained candidate model, awaiting benchmark evaluation.
- `Staging`: Candidate model passed benchmark improvement ($R_{\text{cand}} \ge R_{\text{prod}} + 0.02$) and undergoing integration testing in the `testing`/`staging` branches.
- `Production`: Actively serving inference queries via the AI Gateway (`AIGatewayClient`).

---

## 3. Operator Commands

### Inspect Registered Models:
```bash
hath0r cicccdct model list
```

### Promote Model to Staging:
```bash
hath0r cicccdct model promote --model-name reasoning_slm --version <version_id> --stage Staging
```

### Promote Model to Production:
```bash
hath0r cicccdct model promote --model-name reasoning_slm --version <version_id> --stage Production
```

### Emergency Rollback:
If production regressions occur after promotion:
```bash
# Demote active version back to Staging
hath0r cicccdct model promote --model-name reasoning_slm --version <current_version> --stage Staging

# Restore previous known good production version
hath0r cicccdct model promote --model-name reasoning_slm --version <previous_version> --stage Production

# Force calibration refresh
hath0r cicccdct calibrate
```
