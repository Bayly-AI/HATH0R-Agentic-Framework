# Runbook: Streaming Voice Pipeline Operations

> Document Type: **Runbook** (`cr-workflow-doc-001`)  
> Product: **HATH0R-Agentic-Framework** · Issue: #68 · SemVer: `minor`

## 1. Quick Operations Commands

### Run Streaming Unit & Benchmark Tests
```bash
PYTHONPATH=. pytest tests/test_streaming_voice.py -v
```

### Run Full Test Suite
```bash
PYTHONPATH=. pytest tests/ -v
```

### Inspect Latency Benchmark Metrics
```python
from lib.voice import VoiceTelemetry, VoiceLatencyMetrics

telemetry = VoiceTelemetry()
# Record operations...
benchmarks = telemetry.get_summary_benchmarks()
print("Latency summary:", benchmarks)
```
