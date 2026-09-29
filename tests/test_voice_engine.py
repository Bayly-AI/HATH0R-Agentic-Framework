"""Unit tests for HATH0R Voice Interface Subsystem."""

import os
from unittest.mock import patch

import pytest

from lib.voice.voice_config import VoiceConfig, detect_platform
from lib.voice.voice_engine import (
    AgentDispatcher,
    DarwinAudioAdapter,
    HeuristicDecisionRouter,
    JevDecisionRouter,
    LinuxAudioAdapter,
    MockAudioAdapter,
    VoiceAction,
    VoiceEngine,
    WindowsAudioAdapter,
    resolve_audio_adapter,
)


def test_detect_platform():
    platform = detect_platform()
    assert platform in ("darwin", "linux", "win32", "agnostic")


def test_voice_config_defaults():
    config = VoiceConfig()
    assert config.router_provider == "jev"
    assert config.min_confidence == 0.85
    assert config.cli_binary == "hath0r"


def test_voice_config_env_overrides():
    with patch.dict(
        os.environ,
        {
            "HATHOR_VOICE_MODE": "live",
            "HATHOR_VOICE_ROUTER": "heuristic",
            "HATHOR_VOICE_MIN_CONFIDENCE": "0.90",
            "HATHOR_CLI_BIN": "hath0r-custom",
        },
    ):
        config = VoiceConfig.from_env()
        assert config.mode == "live"
        assert config.router_provider == "heuristic"
        assert config.min_confidence == 0.90
        assert config.cli_binary == "hath0r-custom"


def test_resolve_audio_adapter():
    assert isinstance(resolve_audio_adapter("darwin"), DarwinAudioAdapter)
    assert isinstance(resolve_audio_adapter("linux"), LinuxAudioAdapter)
    assert isinstance(resolve_audio_adapter("win32"), WindowsAudioAdapter)
    assert isinstance(resolve_audio_adapter("unknown"), MockAudioAdapter)


def test_mock_audio_adapter():
    adapter = MockAudioAdapter()
    assert adapter.speak("Hello world") is True
    assert adapter.spoken_messages == ["Hello world"]

    assert adapter.execute_computer_action("Calculator", "open_app") is True
    assert len(adapter.executed_actions) == 1
    assert adapter.executed_actions[0]["target"] == "Calculator"


def test_heuristic_router_cli_command():
    router = HeuristicDecisionRouter()
    action = router.route("hathor doctor")
    assert action is not None
    assert action.routing_tier == "system_one"
    assert action.intent == "cli_command"
    assert action.payload["command"] == "hath0r doctor"
    assert action.confidence >= 0.95


def test_heuristic_router_computer_use():
    router = HeuristicDecisionRouter()
    action = router.route("open Slack")
    assert action is not None
    assert action.routing_tier == "system_one"
    assert action.intent == "computer_use"
    assert action.payload["target"] == "Slack"
    assert action.payload["action"] == "open_app"


def test_heuristic_router_system_control():
    router = HeuristicDecisionRouter()
    action = router.route("mute")
    assert action is not None
    assert action.routing_tier == "system_one"
    assert action.intent == "system_control"


def test_heuristic_router_unresolved():
    router = HeuristicDecisionRouter()
    action = router.route("Explain the Byzantine generals problem")
    assert action is None


def test_jev_router_fastpath():
    jev_router = JevDecisionRouter(mode="stub")
    action = jev_router.route("open Terminal")
    assert action is not None
    assert action.intent == "computer_use"
    assert "latency_ms" in action.metadata
    assert action.metadata["model_id"] == "typesafe-jev-fastpath"


def test_agent_dispatcher_custom_callback():
    def custom_model_callback(prompt: str) -> str:
        return f"Response to: {prompt}"

    dispatcher = AgentDispatcher(agent_callback=custom_model_callback)
    action = dispatcher.dispatch_to_agent("Complex coding question")

    assert action.routing_tier == "system_two"
    assert action.intent == "agent_delegate"
    assert action.payload["feedback_text"] == "Response to: Complex coding question"


def test_voice_engine_e2e_fastpath():
    adapter = MockAudioAdapter()
    engine = VoiceEngine(
        audio_adapter=adapter,
        config=VoiceConfig(platform="agnostic"),
    )

    action = engine.process_utterance("open Chrome", speak_feedback=True)
    assert action.routing_tier == "system_one"
    assert action.intent == "computer_use"
    assert len(adapter.executed_actions) == 1
    assert adapter.executed_actions[0]["target"] == "Chrome"
    assert len(adapter.spoken_messages) == 1
    assert "Opening Chrome" in adapter.spoken_messages[0]


def test_voice_engine_e2e_system_two_escalation():
    adapter = MockAudioAdapter()
    called = []

    def mock_agent(prompt: str) -> str:
        called.append(prompt)
        return "Agent analysis complete"

    dispatcher = AgentDispatcher(agent_callback=mock_agent)
    engine = VoiceEngine(
        audio_adapter=adapter,
        agent_dispatcher=dispatcher,
        config=VoiceConfig(platform="agnostic"),
    )

    action = engine.process_utterance("What is the status of PR 111?", speak_feedback=True)
    assert action.routing_tier == "system_two"
    assert action.intent == "agent_delegate"
    assert called == ["What is the status of PR 111?"]
    assert adapter.spoken_messages == ["Agent analysis complete"]


def test_voice_action_schema_contract():
    import json
    from pathlib import Path
    import jsonschema

    action = VoiceAction(
        transcript="test command",
        routing_tier="system_one",
        intent="cli_command",
        confidence=0.99,
        payload={"command": "hath0r version"},
    )
    d = action.to_dict()
    assert d["schema"] == "hath0r.voice.action/1"
    assert "action_id" in d
    assert "timestamp" in d
    assert "transcript" in d
    assert "routing_tier" in d
    assert "intent" in d
    assert "confidence" in d
    assert "payload" in d

    schema_path = Path("lib/schemas/hath0r-voice-action-v1.schema.json")
    if schema_path.is_file():
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
        jsonschema.validate(instance=d, schema=schema)

