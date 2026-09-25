"""Telemetry and latency benchmarking for HATH0R Voice Interface Subsystem."""

from __future__ import annotations

import statistics
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class VoiceLatencyMetrics:
    """Latency measurements for a single voice-to-action event."""

    utterance_id: str
    transcript: str
    audio_duration_ms: float = 0.0
    vad_onset_latency_ms: float = 0.0
    vad_termination_latency_ms: float = 0.0
    stt_latency_ms: float = 0.0
    router_latency_ms: float = 0.0
    total_voice_to_action_latency_ms: float = 0.0
    speculative_hit: bool = False
    speculative_cancelled: bool = False
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        return {
            "utterance_id": self.utterance_id,
            "transcript": self.transcript,
            "audio_duration_ms": round(self.audio_duration_ms, 2),
            "vad_onset_latency_ms": round(self.vad_onset_latency_ms, 2),
            "vad_termination_latency_ms": round(self.vad_termination_latency_ms, 2),
            "stt_latency_ms": round(self.stt_latency_ms, 2),
            "router_latency_ms": round(self.router_latency_ms, 2),
            "total_voice_to_action_latency_ms": round(self.total_voice_to_action_latency_ms, 2),
            "speculative_hit": self.speculative_hit,
            "speculative_cancelled": self.speculative_cancelled,
            "timestamp": self.timestamp,
        }


class VoiceTelemetry:
    """In-memory telemetry collector and latency benchmark analyzer."""

    def __init__(self, max_history: int = 100) -> None:
        self.max_history = max_history
        self._history: List[VoiceLatencyMetrics] = []

    def record(self, metrics: VoiceLatencyMetrics) -> None:
        """Record a latency measurement."""
        self._history.append(metrics)
        if len(self._history) > self.max_history:
            self._history.pop(0)

    def get_summary_benchmarks(self) -> Dict[str, Any]:
        """Compute aggregate p50, p95, and average latency benchmarks."""
        if not self._history:
            return {
                "count": 0,
                "avg_total_latency_ms": 0.0,
                "p95_total_latency_ms": 0.0,
                "speculative_hit_rate": 0.0,
                "under_200ms_compliance": True,
            }

        total_latencies = [m.total_voice_to_action_latency_ms for m in self._history]
        router_latencies = [m.router_latency_ms for m in self._history]
        spec_hits = sum(1 for m in self._history if m.speculative_hit)

        sorted_totals = sorted(total_latencies)
        idx_p95 = min(len(sorted_totals) - 1, int(len(sorted_totals) * 0.95))

        under_200ms = all(lat <= 200.0 for lat in total_latencies)

        return {
            "count": len(self._history),
            "avg_total_latency_ms": round(statistics.mean(total_latencies), 2),
            "avg_router_latency_ms": round(statistics.mean(router_latencies), 2),
            "p50_total_latency_ms": round(statistics.median(total_latencies), 2),
            "p95_total_latency_ms": round(sorted_totals[idx_p95], 2),
            "speculative_hit_rate": round(spec_hits / len(self._history), 3),
            "under_200ms_compliance": under_200ms,
        }

    def clear(self) -> None:
        """Clear recorded telemetry."""
        self._history.clear()
