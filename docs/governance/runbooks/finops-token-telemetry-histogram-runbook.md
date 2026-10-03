# FinOps Token Ingestion & Histogram Analytics Runbook

> Issue: #188 · Status: Approved · Role: Hath0r Cognitive Substrate FinOps

## Operational Runbook

### Telemetry Ledger Storage
- Default location: `<workspace>/.hath0r/finops/token_telemetry.jsonl`
- Format: Line-delimited JSON (JSONL), UTF-8 encoded.
- Rotation Policy: If file exceeds 50MB, archive to `.hath0r/finops/token_telemetry.<YYYY-MM-DD>.jsonl.gz`.

### Metric Dimensions
- `prompt_tokens`: Number of tokens in user prompt input.
- `prompt_length_chars`: Character length of raw prompt string.
- `total_tokens`: Combined input and completion token count.
- `cost_usd`: Direct monetary cost calculated per model pricing tier.

### Troubleshooting
- **Missing Ledger Error**: Ensure directory `.hath0r/finops/` has write permissions.
- **Empty Histogram Error**: If no records match filter criteria, `TokenHistogramBot` returns a zero-record histogram schema without throwing uncaught exceptions.
- **Outlier Distortion**: High-token outliers are captured in the terminal bin; review `p99` vs `mean` to identify skewed distributions.
