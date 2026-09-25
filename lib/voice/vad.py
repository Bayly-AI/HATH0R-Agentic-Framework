"""Streaming Voice Activity Detection (VAD) for HATH0R Voice Interface Subsystem.

Provides real-time, low-latency speech onset and termination detection using
frame-by-frame energy and zero-crossing analysis with dynamic noise floor adaptation,
as well as pluggable neural/WebRTC VAD backends.
"""

from __future__ import annotations

import math
import struct
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple


class VADState(str, Enum):
    """Lifecycle states of speech activity."""

    SILENCE = "silence"
    SPEECH_ONSET = "speech_onset"
    SPEECH_ACTIVE = "speech_active"
    SPEECH_HANGOVER = "speech_hangover"
    SPEECH_TERMINATED = "speech_terminated"


@dataclass
class VADFrameResult:
    """Detection result for a single audio frame."""

    state: VADState
    is_speech: bool
    energy: float
    confidence: float
    frame_index: int
    onset_detected: bool = False
    termination_detected: bool = False


class BaseStreamingVAD(ABC):
    """Abstract base class for streaming voice activity detectors."""

    @abstractmethod
    def process_frame(self, pcm_bytes: bytes) -> VADFrameResult:
        """Process a raw 16-bit PCM mono audio frame."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Reset internal filter states and hangover buffers."""
        pass


class AdaptiveEnergyVAD(BaseStreamingVAD):
    """Ultra-low latency real-time VAD based on adaptive energy and zero-crossing.

    Operates in sub-millisecond per frame, adapting to background ambient noise
    and identifying speech onset and termination without external heavy models.
    """

    def __init__(
        self,
        sample_rate: int = 16000,
        frame_duration_ms: int = 20,
        sensitivity: float = 0.6,
        onset_frames_threshold: int = 3,
        hangover_frames_threshold: int = 12,
    ) -> None:
        self.sample_rate = sample_rate
        self.frame_duration_ms = frame_duration_ms
        self.frame_samples = (sample_rate * frame_duration_ms) // 1000
        self.expected_bytes = self.frame_samples * 2  # 16-bit = 2 bytes per sample
        self.sensitivity = max(0.1, min(1.0, sensitivity))
        self.onset_frames_threshold = onset_frames_threshold
        self.hangover_frames_threshold = hangover_frames_threshold

        # Dynamic state
        self._noise_floor = 150.0
        self._noise_adaptation_rate = 0.05
        self._state = VADState.SILENCE
        self._consecutive_speech_frames = 0
        self._consecutive_silence_frames = 0
        self._frame_index = 0

    def reset(self) -> None:
        """Reset VAD internal state."""
        self._state = VADState.SILENCE
        self._consecutive_speech_frames = 0
        self._consecutive_silence_frames = 0
        self._frame_index = 0

    def _compute_frame_metrics(self, pcm_bytes: bytes) -> Tuple[float, float]:
        """Compute RMS energy and zero-crossing rate from 16-bit PCM bytes."""
        num_samples = len(pcm_bytes) // 2
        if num_samples == 0:
            return 0.0, 0.0

        samples = struct.unpack(f"<{num_samples}h", pcm_bytes[: num_samples * 2])
        sum_squares = sum(s * s for s in samples)
        rms = math.sqrt(sum_squares / num_samples)

        zero_crossings = 0
        for i in range(1, num_samples):
            if (samples[i] >= 0 and samples[i - 1] < 0) or (samples[i] < 0 and samples[i - 1] >= 0):
                zero_crossings += 1

        zcr = zero_crossings / num_samples
        return rms, zcr

    def process_frame(self, pcm_bytes: bytes) -> VADFrameResult:
        """Analyze a frame and update speech state machine."""
        self._frame_index += 1
        rms, zcr = self._compute_frame_metrics(pcm_bytes)

        # Dynamic speech threshold based on sensitivity and estimated noise floor
        # Sensitivity 1.0 -> lower threshold (more sensitive to quiet speech)
        multiplier = 1.5 + (1.0 - self.sensitivity) * 3.5
        threshold = max(200.0, self._noise_floor * multiplier)

        is_voice_frame = rms > threshold and (zcr > 0.02)

        onset_detected = False
        termination_detected = False

        if is_voice_frame:
            self._consecutive_speech_frames += 1
            self._consecutive_silence_frames = 0

            if self._state == VADState.SILENCE:
                if self._consecutive_speech_frames >= self.onset_frames_threshold:
                    self._state = VADState.SPEECH_ACTIVE
                    onset_detected = True
                else:
                    self._state = VADState.SPEECH_ONSET
            elif self._state == VADState.SPEECH_ONSET:
                if self._consecutive_speech_frames >= self.onset_frames_threshold:
                    self._state = VADState.SPEECH_ACTIVE
                    onset_detected = True
            elif self._state == VADState.SPEECH_HANGOVER:
                self._state = VADState.SPEECH_ACTIVE
        else:
            self._consecutive_silence_frames += 1
            self._consecutive_speech_frames = 0

            # Update noise floor estimate when calm
            if self._state == VADState.SILENCE:
                self._noise_floor = (1.0 - self._noise_adaptation_rate) * self._noise_floor + (
                    self._noise_adaptation_rate * rms
                )

            if self._state == VADState.SPEECH_ACTIVE:
                self._state = VADState.SPEECH_HANGOVER
            elif self._state == VADState.SPEECH_HANGOVER:
                if self._consecutive_silence_frames >= self.hangover_frames_threshold:
                    self._state = VADState.SPEECH_TERMINATED
                    termination_detected = True
            elif self._state == VADState.SPEECH_TERMINATED:
                self._state = VADState.SILENCE
            elif self._state == VADState.SPEECH_ONSET:
                self._state = VADState.SILENCE

        confidence = min(1.0, max(0.0, (rms - self._noise_floor) / max(1.0, threshold))) if is_voice_frame else 0.0

        return VADFrameResult(
            state=self._state,
            is_speech=is_voice_frame or (self._state in (VADState.SPEECH_ACTIVE, VADState.SPEECH_HANGOVER)),
            energy=round(rms, 2),
            confidence=round(confidence, 3),
            frame_index=self._frame_index,
            onset_detected=onset_detected,
            termination_detected=termination_detected,
        )


class MockVAD(BaseStreamingVAD):
    """Deterministic mock VAD for unit testing and deterministic simulation."""

    def __init__(self, predefined_results: Optional[List[bool]] = None) -> None:
        self.predefined_results = predefined_results or []
        self._current_index = 0
        self._frame_index = 0
        self._was_speech = False

    def reset(self) -> None:
        self._current_index = 0
        self._frame_index = 0
        self._was_speech = False

    def process_frame(self, pcm_bytes: bytes) -> VADFrameResult:
        self._frame_index += 1
        is_speech = False
        if self._current_index < len(self.predefined_results):
            is_speech = self.predefined_results[self._current_index]
            self._current_index += 1

        onset = is_speech and not self._was_speech
        termination = not is_speech and self._was_speech
        self._was_speech = is_speech

        state = VADState.SPEECH_ACTIVE if is_speech else VADState.SILENCE
        if termination:
            state = VADState.SPEECH_TERMINATED

        return VADFrameResult(
            state=state,
            is_speech=is_speech,
            energy=500.0 if is_speech else 50.0,
            confidence=0.95 if is_speech else 0.0,
            frame_index=self._frame_index,
            onset_detected=onset,
            termination_detected=termination,
        )
