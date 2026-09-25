"""HATH0R Voice Interface Subsystem.

A cross-platform, agent-agnostic, and model-agnostic voice interaction component
for the HATHOR framework.
"""

from lib.voice.speculative import SpeculativeCandidate, SpeculativeExecutionPipeline
from lib.voice.streaming_stt import (
    DarwinStreamingSTT,
    MockStreamingSTT,
    StreamingSTTBackend,
    StreamingTranscriptEvent,
    WhisperStreamingSTT,
)
from lib.voice.telemetry import VoiceLatencyMetrics, VoiceTelemetry
from lib.voice.vad import (
    AdaptiveEnergyVAD,
    BaseStreamingVAD,
    MockVAD,
    VADFrameResult,
    VADState,
)
from lib.voice.voice_config import VoiceConfig
from lib.voice.voice_engine import (
    AgentDispatcher,
    DarwinAudioAdapter,
    HeuristicDecisionRouter,
    JevDecisionRouter,
    LinuxAudioAdapter,
    MockAudioAdapter,
    PlatformAudioAdapter,
    SystemOneRouter,
    VoiceAction,
    VoiceEngine,
    WindowsAudioAdapter,
    resolve_audio_adapter,
)

__all__ = [
    "VoiceConfig",
    "VoiceEngine",
    "VoiceAction",
    "SystemOneRouter",
    "JevDecisionRouter",
    "HeuristicDecisionRouter",
    "AgentDispatcher",
    "PlatformAudioAdapter",
    "resolve_audio_adapter",
    "BaseStreamingVAD",
    "AdaptiveEnergyVAD",
    "MockVAD",
    "VADState",
    "VADFrameResult",
    "StreamingTranscriptEvent",
    "StreamingSTTBackend",
    "MockStreamingSTT",
    "DarwinStreamingSTT",
    "WhisperStreamingSTT",
    "SpeculativeExecutionPipeline",
    "SpeculativeCandidate",
    "VoiceLatencyMetrics",
    "VoiceTelemetry",
]
