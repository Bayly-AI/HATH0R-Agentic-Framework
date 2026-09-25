# Runbook: HATH0R Voice Interface Subsystem Operations

> Document Type: **Runbook** (`cr-workflow-doc-001`)  
> Product: **HATH0R-Agentic-Framework** · Issue: #67 · SemVer: `minor`

## 1. Quick Operations Commands

### Run Unit Tests
```bash
PYTHONPATH=. pytest tests/test_voice_engine.py -v
```

### Validate Action Schema Against Metaschema
```bash
check-jsonschema --check-metaschema lib/schemas/hath0r-voice-action-v1.schema.json
```

### Smoke Test Voice Engine in Python REPL
```python
from lib.voice import VoiceConfig, VoiceEngine, MockAudioAdapter

engine = VoiceEngine(config=VoiceConfig(platform="agnostic"), audio_adapter=MockAudioAdapter())
action = engine.process_utterance("hath0r doctor")
assert action.routing_tier == "system_one"
print("Fast-path latency:", action.metadata.get("latency_ms"), "ms")
```
