# Runbook: Hath0r Workspace & Infrastructure Bootstrap

**Runbook ID**: `RB-HATH0R-BOOTSTRAP-001`  
**Classification**: Core Operational Runbook  

---

## 🎯 Purpose
Initialize or verify a Hath0r workspace, ensuring all required directories, contracts, and memory graphs are present and compliant.

---

## 📋 Execution Steps

### 1. Verify Layout Completeness
Ensure required paths exist:
- `AGENTS.md`
- `cfg/suite.yaml`
- `contracts/exit-codes.yaml`
- `contracts/hath0r-cli-response-v1.schema.json`
- `.hath0r/memory/graph.json`

### 2. Verify Hidden Root Invariant
Ensure forbidden legacy roots do NOT exist (`.ai`, `.customerSystem`, `.infraOS`):
```bash
for bad in .ai .customerSystem .infraOS; do
  if [[ -e "$bad" ]]; then
    echo "FAIL: Forbidden legacy root $bad found."
    exit 1
  fi
done
```

### 3. Check CLI Operator Health
```bash
hath0r --version
hath0r doctor
```
