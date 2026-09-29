"""Speculative execution pipeline for low-latency voice action routing.

Evaluates streaming partial transcripts directly against the System 1 router,
enabling fast-path tool execution without waiting for speech pause or full endpointing.
Gracefully cancels if the transcript disambiguates away from the speculative intent.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Callable, Optional

from lib.voice.streaming_stt import StreamingTranscriptEvent
from lib.voice.telemetry import VoiceLatencyMetrics, VoiceTelemetry
from lib.voice.voice_engine import SystemOneRouter, VoiceAction, VoiceEngine


@dataclass
class SpeculativeCandidate:
    """A pending speculative action triggered by partial speech recognition."""

    action: VoiceAction
    trigger_transcript: str
    created_at_ms: float
    confirmed: bool = False
    cancelled: bool = False
    cancellation_reason: Optional[str] = None


class SpeculativeExecutionPipeline:
    """Speculative execution engine for streaming voice input."""

    def __init__(
        self,
        voice_engine: VoiceEngine,
        telemetry: Optional[VoiceTelemetry] = None,
        on_action_committed: Optional[Callable[[VoiceAction], None]] = None,
    ) -> None:
        self.engine = voice_engine
        self.telemetry = telemetry or VoiceTelemetry()
        self.on_action_committed = on_action_committed
        self._current_candidate: Optional[SpeculativeCandidate] = None
        self._utterance_id: str = str(uuid.uuid4())
        self._start_time: float = time.perf_counter()

    def start_utterance(self) -> None:
        """Reset state for a new incoming utterance."""
        self._utterance_id = str(uuid.uuid4())
        self._current_candidate = None
        self._start_time = time.perf_counter()

    @property
    def current_candidate(self) -> Optional[SpeculativeCandidate]:
        """Return the active speculative candidate if any."""
        return self._current_candidate

    def on_partial_transcript(self, event: StreamingTranscriptEvent) -> Optional[VoiceAction]:
        """Evaluate a partial streaming transcript event.

        Returns VoiceAction if speculative execution commits, or None.
        """
        router_start = time.perf_counter()
        transcript = event.text.strip()
        if not transcript:
            return None

        # If we have an existing candidate, check if new partial still agrees
        if self._current_candidate and not self._current_candidate.cancelled:
            cand = self._current_candidate
            # Check if previous candidate intent was invalidated
            # If the user continued speaking and the command is no longer matching:
            new_action = self.engine.router.route(transcript)
            if new_action is None:
                # Disambiguated away from command (e.g. "open" became "open source licenses")
                cand.cancelled = True
                cand.cancellation_reason = f"Transcript '{transcript}' diverted from '{cand.trigger_transcript}'"
                self._current_candidate = None
                return None
            elif (
                new_action.intent == cand.action.intent
                and new_action.payload.get("target") == cand.action.payload.get("target")
                and new_action.payload.get("command") == cand.action.payload.get("command")
            ):
                # Reinforced: if confidence is high, we can commit early
                if new_action.confidence >= self.engine.config.min_confidence and not cand.confirmed:
                    cand.confirmed = True
                    return self._commit_action(new_action, is_speculative=True)

        # No candidate currently, evaluate router for early prefix match
        candidate_action = self.engine.router.route(transcript)
        router_latency_ms = (time.perf_counter() - router_start) * 1000

        if candidate_action and candidate_action.confidence >= self.engine.config.min_confidence:
            elapsed_ms = (time.perf_counter() - self._start_time) * 1000
            self._current_candidate = SpeculativeCandidate(
                action=candidate_action,
                trigger_transcript=transcript,
                created_at_ms=elapsed_ms,
            )
            # If the event is already final or complete command phrase, commit immediately
            if event.is_final or self._is_complete_command(transcript, candidate_action):
                self._current_candidate.confirmed = True
                return self._commit_action(candidate_action, is_speculative=True)

        return None

    def on_final_transcript(self, event: StreamingTranscriptEvent) -> VoiceAction:
        """Process the final transcript event after speech endpointing."""
        transcript = event.text.strip()
        router_start = time.perf_counter()

        # If a speculative candidate was already confirmed for this exact transcript, return it
        if (
            self._current_candidate
            and self._current_candidate.confirmed
            and self._current_candidate.trigger_transcript.lower() in transcript.lower()
        ):
            return self._current_candidate.action

        # If candidate existed but didn't confirm or cancelled, evaluate full utterance
        action = self.engine.process_utterance(transcript, speak_feedback=False)
        router_latency_ms = (time.perf_counter() - router_start) * 1000

        total_latency_ms = (time.perf_counter() - self._start_time) * 1000
        metrics = VoiceLatencyMetrics(
            utterance_id=self._utterance_id,
            transcript=transcript,
            audio_duration_ms=event.timestamp_ms,
            router_latency_ms=router_latency_ms,
            total_voice_to_action_latency_ms=total_latency_ms,
            speculative_hit=False,
            speculative_cancelled=self._current_candidate.cancelled if self._current_candidate else False,
        )
        self.telemetry.record(metrics)

        if self.on_action_committed:
            self.on_action_committed(action)

        return action

    def _is_complete_command(self, transcript: str, action: VoiceAction) -> bool:
        """Heuristic check whether transcript is complete enough to execute immediately."""
        t = transcript.strip().lower()
        if action.intent == "system_control":
            return t in ("mute", "unmute", "stop listening", "cancel")
        if action.intent == "cli_command":
            parts = t.split()
            return len(parts) >= 2
        if action.intent == "computer_use":
            parts = t.split()
            return len(parts) >= 2
        return False

    def _commit_action(self, action: VoiceAction, is_speculative: bool) -> VoiceAction:
        """Execute committed action and record telemetry."""
        total_latency_ms = (time.perf_counter() - self._start_time) * 1000
        action.metadata["speculative_execution"] = is_speculative
        action.metadata["latency_ms"] = round(total_latency_ms, 2)

        # Execute OS computer action if needed
        if action.intent == "computer_use":
            target = action.payload.get("target", "")
            act = action.payload.get("action", "")
            args = action.payload.get("args", [])
            self.engine.audio.execute_computer_action(target=target, action=act, args=args)

        metrics = VoiceLatencyMetrics(
            utterance_id=self._utterance_id,
            transcript=action.transcript,
            total_voice_to_action_latency_ms=total_latency_ms,
            speculative_hit=is_speculative,
            speculative_cancelled=False,
        )
        self.telemetry.record(metrics)

        if self.on_action_committed:
            self.on_action_committed(action)

        return action
