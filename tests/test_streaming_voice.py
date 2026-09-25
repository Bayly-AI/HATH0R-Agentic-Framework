"""Unit and benchmark tests for streaming STT, VAD, and speculative execution."""

from __future__ import annotations

import math
import struct
import time
from typing import List

import pytest

from lib.voice import (
    AdaptiveEnergyVAD,
    MockAudioAdapter,
    MockStreamingSTT,
    MockVAD,
    SpeculativeExecutionPipeline,
    StreamingTranscriptEvent,
    VADState,
    VoiceConfig,
    VoiceEngine,
    VoiceTelemetry,
)


def _generate_pcm_tone(duration_ms: int = 20, frequency_hz: float = 440.0, amplitude: float = 8000.0) -> bytes:
    """Generate 16-bit PCM mono audio buffer for a tone."""
    sample_rate = 16000
    num_samples = (sample_rate * duration_ms) // 1000
    samples: List[int] = []
    for i in range(num_samples):
        val = int(amplitude * math.sin(2 * math.pi * frequency_hz * (i / sample_rate)))
        samples.append(max(-32768, min(32767, val)))
    return struct.pack(f"<{len(samples)}h", *samples)


def _generate_pcm_silence(duration_ms: int = 20) -> bytes:
    """Generate 16-bit PCM mono silence buffer."""
    num_samples = (16000 * duration_ms) // 1000
    return b"\x00" * (num_samples * 2)


def test_adaptive_energy_vad_silence():
    vad = AdaptiveEnergyVAD(sample_rate=16000, frame_duration_ms=20, sensitivity=0.6)
    silence = _generate_pcm_silence(20)

    for _ in range(5):
        res = vad.process_frame(silence)
        assert res.state == VADState.SILENCE
        assert res.is_speech is False
        assert res.onset_detected is False


def test_adaptive_energy_vad_speech_onset_and_hangover():
    vad = AdaptiveEnergyVAD(
        sample_rate=16000,
        frame_duration_ms=20,
        sensitivity=0.8,
        onset_frames_threshold=2,
        hangover_frames_threshold=3,
    )
    speech = _generate_pcm_tone(20, frequency_hz=300.0, amplitude=12000.0)
    silence = _generate_pcm_silence(20)

    # Frame 1: speech detected -> onset
    f1 = vad.process_frame(speech)
    assert f1.state == VADState.SPEECH_ONSET
    assert f1.onset_detected is False

    # Frame 2: speech detected -> active onset
    f2 = vad.process_frame(speech)
    assert f2.state == VADState.SPEECH_ACTIVE
    assert f2.onset_detected is True

    # Frame 3: speech continues
    f3 = vad.process_frame(speech)
    assert f3.state == VADState.SPEECH_ACTIVE

    # Frame 4: silence begins -> hangover
    f4 = vad.process_frame(silence)
    assert f4.state == VADState.SPEECH_HANGOVER

    # Frame 5: silence continues
    f5 = vad.process_frame(silence)
    assert f5.state == VADState.SPEECH_HANGOVER

    # Frame 6: 3rd silence frame reaches threshold -> terminated
    f6 = vad.process_frame(silence)
    assert f6.state == VADState.SPEECH_TERMINATED
    assert f6.termination_detected is True


def test_mock_vad():
    vad = MockVAD(predefined_results=[False, True, True, False])
    silence = _generate_pcm_silence(20)

    r1 = vad.process_frame(silence)
    assert r1.is_speech is False

    r2 = vad.process_frame(silence)
    assert r2.is_speech is True
    assert r2.onset_detected is True

    r3 = vad.process_frame(silence)
    assert r3.is_speech is True
    assert r3.onset_detected is False

    r4 = vad.process_frame(silence)
    assert r4.is_speech is False
    assert r4.termination_detected is True


def test_mock_streaming_stt():
    stt = MockStreamingSTT(token_sequence=["hath0r", "doctor"])
    chunk = _generate_pcm_tone(20)

    ev1 = stt.feed_audio_chunk(chunk)
    assert ev1 is not None
    assert ev1.text == "hath0r"
    assert ev1.is_final is False

    ev2 = stt.feed_audio_chunk(chunk)
    assert ev2 is not None
    assert ev2.text == "hath0r doctor"
    assert ev2.is_final is True

    ev3 = stt.feed_audio_chunk(chunk)
    assert ev3 is None

    final_ev = stt.finish_stream()
    assert final_ev.is_final is True
    assert final_ev.text == "hath0r doctor"


def test_speculative_execution_fast_path_commit():
    audio = MockAudioAdapter()
    engine = VoiceEngine(config=VoiceConfig(platform="agnostic"), audio_adapter=audio)
    telemetry = VoiceTelemetry()

    committed_actions = []
    pipeline = SpeculativeExecutionPipeline(
        voice_engine=engine,
        telemetry=telemetry,
        on_action_committed=lambda a: committed_actions.append(a),
    )

    pipeline.start_utterance()

    # Step 1: partial event with incomplete command
    event1 = StreamingTranscriptEvent(
        text="open",
        is_final=False,
        confidence=0.88,
        timestamp_ms=45.0,
        tokens=["open"],
    )
    act1 = pipeline.on_partial_transcript(event1)
    # "open" alone is not a complete command
    assert act1 is None

    # Step 2: partial event completed command "open Calculator"
    event2 = StreamingTranscriptEvent(
        text="open Calculator",
        is_final=False,
        confidence=0.96,
        timestamp_ms=90.0,
        tokens=["open", "Calculator"],
    )
    act2 = pipeline.on_partial_transcript(event2)
    assert act2 is not None
    assert act2.routing_tier == "system_one"
    assert act2.intent == "computer_use"
    assert act2.payload["target"] == "Calculator"
    assert act2.metadata.get("speculative_execution") is True

    # OS action executed
    assert len(audio.executed_actions) == 1
    assert audio.executed_actions[0]["target"] == "Calculator"
    assert len(committed_actions) == 1

    # End of utterance
    final_event = StreamingTranscriptEvent(
        text="open Calculator",
        is_final=True,
        confidence=0.98,
        timestamp_ms=130.0,
        tokens=["open", "Calculator"],
    )
    final_act = pipeline.on_final_transcript(final_event)
    assert final_act.action_id == act2.action_id


def test_speculative_execution_graceful_cancellation_on_disambiguation():
    audio = MockAudioAdapter()
    engine = VoiceEngine(config=VoiceConfig(platform="agnostic"), audio_adapter=audio)
    telemetry = VoiceTelemetry()

    pipeline = SpeculativeExecutionPipeline(
        voice_engine=engine,
        telemetry=telemetry,
    )
    pipeline.start_utterance()

    # Partial event 1: Hath0r CLI prefix
    event1 = StreamingTranscriptEvent(
        text="hathor",
        is_final=False,
        confidence=0.90,
        timestamp_ms=40.0,
        tokens=["hathor"],
    )
    pipeline.on_partial_transcript(event1)
    cand = pipeline.current_candidate
    assert cand is not None
    assert cand.action.intent == "cli_command"

    # User continues speaking something else that diverges from CLI command
    event2 = StreamingTranscriptEvent(
        text="hathor is an ancient Egyptian deity of love and joy",
        is_final=False,
        confidence=0.92,
        timestamp_ms=110.0,
        tokens=["hathor", "is", "an", "ancient", "Egyptian", "deity"],
    )
    pipeline.on_partial_transcript(event2)

    # Candidate was gracefully cancelled
    assert pipeline.current_candidate is None

    # Final event escalates to System 2 agent reasoning
    final_event = StreamingTranscriptEvent(
        text="hathor is an ancient Egyptian deity of love and joy",
        is_final=True,
        confidence=0.95,
        timestamp_ms=160.0,
        tokens=event2.tokens,
    )
    final_act = pipeline.on_final_transcript(final_event)
    assert final_act.routing_tier == "system_two"
    assert final_act.intent == "agent_delegate"

    # Telemetry records cancellation
    summary = telemetry.get_summary_benchmarks()
    assert summary["count"] == 1


def test_end_to_end_latency_benchmark_under_200ms():
    audio = MockAudioAdapter()
    engine = VoiceEngine(config=VoiceConfig(platform="agnostic"), audio_adapter=audio)
    telemetry = VoiceTelemetry()
    pipeline = SpeculativeExecutionPipeline(voice_engine=engine, telemetry=telemetry)

    latencies = []
    for cmd in ["open Slack", "hath0r doctor", "mute", "open Terminal"]:
        pipeline.start_utterance()
        start = time.perf_counter()
        ev = StreamingTranscriptEvent(
            text=cmd,
            is_final=True,
            confidence=0.95,
            timestamp_ms=50.0,
            tokens=cmd.split(),
        )
        action = pipeline.on_partial_transcript(ev)
        elapsed_ms = (time.perf_counter() - start) * 1000
        latencies.append(elapsed_ms)
        assert action is not None
        assert action.routing_tier == "system_one"

    summary = telemetry.get_summary_benchmarks()
    assert summary["under_200ms_compliance"] is True
    assert summary["avg_total_latency_ms"] < 200.0
    assert summary["p95_total_latency_ms"] < 200.0
