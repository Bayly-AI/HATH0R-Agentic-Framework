"""HATH0R Voice Interface Subsystem.

A cross-platform, agent-agnostic, and model-agnostic voice interaction component
for the HATHOR framework.
"""

from lib.voice.voice_config import VoiceConfig
from lib.voice.voice_engine import (
    VoiceEngine,
    VoiceAction,
    SystemOneRouter,
    JevDecisionRouter,
    HeuristicDecisionRouter,
    AgentDispatcher,
    PlatformAudioAdapter,
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
]
