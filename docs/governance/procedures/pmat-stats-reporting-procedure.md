# Procedure: PMAT Multi-Dimensional Stats Reporting

> Canonical Standard Operating Procedure · Hath0r Agentic Framework  
> Updated: 2026-10-05

## 1. Scope & Objective

Defines operational steps to query PMAT multi-dimensional stats, generate provability/complexity reports, and validate against `contracts/hath0r-pmat-stats-report-v1.schema.json`.

---

## 2. Step-by-Step Instructions

### Step 1: Health Diagnostic
```bash
hath0r pmat doctor
```

### Step 2: Generate Full Stats Report
```bash
hath0r pmat stats --target . --window 30 --format table
```

### Step 3: Provability & Complexity Breakdown
```bash
hath0r pmat stats --provability --complexity --format json
```

### Step 4: Schema Validation
```bash
hath0r contracts validate --file contracts/hath0r-pmat-stats-report-v1.schema.json
```
