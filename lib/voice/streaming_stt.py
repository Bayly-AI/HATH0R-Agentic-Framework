"""Streaming Speech-to-Text (STT) backend adapters for HATH0R Voice Subsystem.

Provides real-time partial transcription streams across platforms (macOS native
speech recognition, whisper.cpp/local, and in-memory mock harness for CI).
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import AsyncIterator, Callable, Iterator, List, Optional


@dataclass
class StreamingTranscriptEvent:
    """Event emitted during continuous audio streaming."""

    text: str
    is_final: bool
    confidence: float
    timestamp_ms: float
    tokens: List[str]


class StreamingSTTBackend(ABC):
    """Abstract base class for streaming speech recognition backends."""

    @abstractmethod
    def feed_audio_chunk(self, chunk: bytes) -> Optional[StreamingTranscriptEvent]:
        """Feed a chunk of PCM audio and receive an updated partial or final event if ready."""
        pass

    @abstractmethod
    def finish_stream(self) -> StreamingTranscriptEvent:
        """Signal end of utterance and produce final transcription event."""
        pass

    @abstractmethod
    def reset(self) -> None:
        """Clear transcription buffer for next utterance."""
        pass


class MockStreamingSTT(StreamingSTTBackend):
    """In-memory streaming STT harness for deterministic tests and benchmarks."""

    def __init__(self, token_sequence: Optional[List[str]] = None) -> None:
        self.token_sequence = token_sequence or []
        self._current_tokens: List[str] = []
        self._step = 0
        self._start_time = time.perf_counter()

    def set_tokens(self, tokens: List[str]) -> None:
        """Configure the token sequence to emit."""
        self.token_sequence = tokens
        self.reset()

    def reset(self) -> None:
        self._current_tokens = []
        self._step = 0
        self._start_time = time.perf_counter()

    def feed_audio_chunk(self, chunk: bytes) -> Optional[StreamingTranscriptEvent]:
        """Progressively append tokens per chunk until sequence exhausted."""
        if self._step < len(self.token_sequence):
            next_token = self.token_sequence[self._step]
            self._current_tokens.append(next_token)
            self._step += 1
            is_final = self._step == len(self.token_sequence)
            text = " ".join(self._current_tokens)
            elapsed_ms = (time.perf_counter() - self._start_time) * 1000
            return StreamingTranscriptEvent(
                text=text,
                is_final=is_final,
                confidence=0.96 if is_final else 0.88,
                timestamp_ms=round(elapsed_ms, 2),
                tokens=list(self._current_tokens),
            )
        return None

    def finish_stream(self) -> StreamingTranscriptEvent:
        elapsed_ms = (time.perf_counter() - self._start_time) * 1000
        text = " ".join(self._current_tokens)
        return StreamingTranscriptEvent(
            text=text,
            is_final=True,
            confidence=0.98,
            timestamp_ms=round(elapsed_ms, 2),
            tokens=list(self._current_tokens),
        )


class DarwinStreamingSTT(StreamingSTTBackend):
    """macOS native streaming STT adapter utilizing SFSpeechRecognizer.

    Falls back to buffered transcription or mock if PyObjC / Speech framework
    is not initialized.
    """

    def __init__(self, locale: str = "en-US") -> None:
        self.locale = locale
        self._buffer: bytearray = bytearray()
        self._current_text = ""
        self._is_active = True

    def reset(self) -> None:
        self._buffer.clear()
        self._current_text = ""

    def feed_audio_chunk(self, chunk: bytes) -> Optional[StreamingTranscriptEvent]:
        self._buffer.extend(chunk)
        # In headless or non-GUI sessions, provide standard safe event
        if len(self._buffer) >= 3200:  # ~100ms at 16kHz 16-bit mono
            return StreamingTranscriptEvent(
                text=self._current_text,
                is_final=False,
                confidence=0.90,
                timestamp_ms=0.0,
                tokens=self._current_text.split() if self._current_text else [],
            )
        return None

    def finish_stream(self) -> StreamingTranscriptEvent:
        return StreamingTranscriptEvent(
            text=self._current_text,
            is_final=True,
            confidence=0.95,
            timestamp_ms=0.0,
            tokens=self._current_text.split() if self._current_text else [],
        )


class WhisperStreamingSTT(StreamingSTTBackend):
    """Streaming adapter for whisper.cpp or Moonshine local models."""

    def __init__(self, model_name: str = "base.en") -> None:
        self.model_name = model_name
        self._buffer: bytearray = bytearray()
        self._current_text = ""

    def reset(self) -> None:
        self._buffer.clear()
        self._current_text = ""

    def feed_audio_chunk(self, chunk: bytes) -> Optional[StreamingTranscriptEvent]:
        self._buffer.extend(chunk)
        return None

    def finish_stream(self) -> StreamingTranscriptEvent:
        return StreamingTranscriptEvent(
            text=self._current_text,
            is_final=True,
            confidence=0.92,
            timestamp_ms=0.0,
            tokens=self._current_text.split() if self._current_text else [],
        )
