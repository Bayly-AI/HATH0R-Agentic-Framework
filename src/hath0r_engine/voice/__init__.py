"""HATH0R Voice Interface Subsystem.

A cross-platform, agent-agnostic, and model-agnostic voice interaction component
for the HATHOR framework.
"""

from .speculative import SpeculativeCandidate, SpeculativeExecutionPipeline
from .streaming_stt import (
    DarwinStreamingSTT,
    MockStreamingSTT,
    StreamingSTTBackend,
    StreamingTranscriptEvent,
    WhisperStreamingSTT,
)
from .telemetry import VoiceLatencyMetrics, VoiceTelemetry
from .vad import (
    AdaptiveEnergyVAD,
    BaseStreamingVAD,
    MockVAD,
    VADFrameResult,
    VADState,
)
from .voice_config import VoiceConfig
from .voice_engine import (
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
    "DarwinAudioAdapter",
    "LinuxAudioAdapter",
    "MockAudioAdapter",
    "WindowsAudioAdapter",
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
