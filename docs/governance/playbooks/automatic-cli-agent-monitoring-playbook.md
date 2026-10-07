# Automatic CLI Agent Progress Monitoring Playbook

> Role: **Hath0r Control Tower & Framework Governance**  
> Status: **Approved**  
> Updated: **2026-10-07**

## Overview

This playbook documents the operational and automated architecture for watching agents in real-time as they execute commands via the Operator CLI (`hath0r`).

## Automated Entry Gate Architecture

When an agent enters the CLI (`hath0r <command>`), the CLI execution engine automatically triggers the following monitors:

1. **FinOps Token & Telemetry Recording (`TokenTelemetryCLIBot`)**:
   - Ingests CLI prompt arguments, command execution metadata, latency, and estimated subword token costs into `.hath0r/finops/token_telemetry.jsonl`.
2. **Continuous Calibration & Drift Monitor (`CICCCDTelemetryHook`)**:
   - Records span metrics and parameter drift (`accuracy_drift`, `latency_drift_ms`, `token_tax_drift`) into `.hath0r/cccd_state.json`.
3. **Live Agent Progression Stream (`.hath0r/events.jsonl`)**:
   - Emits structured execution events (`agent_command_start`, `agent_command_complete`, `agent_command_error`) for consumption by `hath0r serve` (web dashboard SSE stream) and `hath0r tui` (live terminal monitoring).

## Operational CLI Commands

### 1. View FinOps Token Cost Ledger
```bash
hath0r finops tokens check
```

### 2. View Real-Time Drift & Calibration Status
```bash
hath0r cicccd status
```

### 3. Launch Live Real-Time Monitoring Web Server
```bash
hath0r serve --daemon
```

### 4. Launch Live Terminal Dashboard
```bash
hath0r tui --mode live
```

## Governance & Verification Checklist

- [x] Automatic initialization in CLI entrypoint (`cli.py`).
- [x] Zero-tax telemetry recording without blocking CLI user interactions.
- [x] Schema contract compliance (`hath0r.finops.token_telemetry.v1.schema.json`).
