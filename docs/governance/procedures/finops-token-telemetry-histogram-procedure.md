# FinOps Token Ingestion & Histogram Analytics Procedure

> Issue: #188 · Status: Approved · Role: Hath0r Cognitive Substrate FinOps

## Purpose

Define the formal operational procedures for capturing tokens sent to Hath0r agents, persisting telemetry records, retrieving filtered datasets, and generating statistical histograms.

## Procedure Steps

### 1. Telemetry Capture Initialization
- Ensure `.hath0r/finops/` directory exists within target workspace.
- Initialize `TokenTelemetryBot` with active workspace path.
- Configure default complexity tier and model pricing parameters.

### 2. Prompt Token Ingestion
- When sending a prompt to an agent or calling `AIGatewayClient.complete()`, provide:
  - `prompt`: raw text sent to agent
  - `user_id`: user/operator handle (e.g. `raybayly`, `dev-agent`)
  - `model`: target model name
  - `tier`: complexity tier (`light`, `standard`, `reasoning`)
  - `session_id`: active session or conversation ID
- The ingestion bot calculates:
  - `prompt_length_chars` = len(prompt)
  - `prompt_tokens` = max(1, len(prompt) // 4) or exact tokenizer count
  - `cost_usd` = unit cost formula
- Appends record to `.hath0r/finops/token_telemetry.jsonl`.

### 3. Record Querying & Filtering
- Retrieve records using `TokenTelemetryBot.query_records()`:
  - By user (`--user <user_id>`)
  - By date range (`--since <timestamp>`, `--until <timestamp>`)
  - By model or tier (`--model <model>`)
  - By record limit (`--limit <N>`)

### 4. Histogram Generation
- Execute `TokenHistogramBot.generate_histogram()`:
  - Select target metric (`prompt_tokens`, `prompt_length_chars`, `total_tokens`, `cost_usd`)
  - Define bin count (default 10 bins)
  - Extract statistical summary (`min`, `max`, `mean`, `median`, `p90`, `p95`, `p99`, `std_dev`)
  - Render ASCII frequency chart and emit JSON conforming to contract `hath0r-token-histogram-v1.schema.json`.
