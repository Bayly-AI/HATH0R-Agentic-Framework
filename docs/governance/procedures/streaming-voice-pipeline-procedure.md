# Procedure: Streaming Voice Pipeline Operations

> Document Type: **Procedure** (`cr-workflow-doc-001`)  
> Product: **HATH0R-Agentic-Framework** · Issue: #68 · SemVer: `minor`

## 1. Scope

Normative procedure for running streaming speech-to-text, real-time VAD, and speculative routing.

## 2. Ingest and Evaluation Loop

```python
from lib.voice import (
    AdaptiveEnergyVAD,
    SpeculativeExecutionPipeline,
    VoiceEngine,
    VoiceTelemetry,
)

engine = VoiceEngine()
telemetry = VoiceTelemetry()
pipeline = SpeculativeExecutionPipeline(voice_engine=engine, telemetry=telemetry)
vad = AdaptiveEnergyVAD()

# Audio capture loop
pipeline.start_utterance()
# For each 20ms audio frame:
frame_result = vad.process_frame(pcm_chunk)
if frame_result.onset_detected:
    # Begin buffering/streaming to STT backend
    pass
# As STT produces partial events:
action = pipeline.on_partial_transcript(partial_event)
if action:
    # Fast path committed speculatively!
    pass
```

## 3. Verification

Run automated streaming and latency benchmark tests:
```bash
PYTHONPATH=. pytest tests/test_streaming_voice.py -v
```
