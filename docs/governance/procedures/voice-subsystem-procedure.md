# Procedure: HATH0R Voice Interface Subsystem

> Document Type: **Procedure** (`cr-workflow-doc-001`)  
> Product: **HATH0R-Agentic-Framework** · Issue: #67 · SemVer: `minor`

## 1. Scope

Normative procedure for initializing, configuring, testing, and invoking the Voice Interface Subsystem.

## 2. Steps

### Step 1: Configuration
Voice subsystem parameters are defined in `cfg/voice.json` and overridable via environment variables:
- `HATHOR_VOICE_MODE`: `off` | `stub` | `live` | `auto`
- `HATHOR_VOICE_ROUTER`: `jev` | `heuristic` | `agent_direct`
- `HATHOR_VOICE_MIN_CONFIDENCE`: float threshold (default `0.85`)
- `HATHOR_CLI_BIN`: path or binary name for Hath0r CLI

### Step 2: Initialize VoiceEngine
Instantiate `VoiceEngine` with desired adapters:
```python
from lib.voice import VoiceConfig, VoiceEngine, resolve_audio_adapter

config = VoiceConfig.from_env()
engine = VoiceEngine(config=config)
```

### Step 3: Process Voice Utterance
Feed transcribed speech into `process_utterance()`:
```python
action = engine.process_utterance("hathor doctor", speak_feedback=True)
print(action.routing_tier, action.intent, action.payload)
```

### Step 4: Verification and Schema Conformance
Validate that emitted actions satisfy `hath0r.voice.action/1`:
```bash
PYTHONPATH=. pytest tests/test_voice_engine.py -v
```
