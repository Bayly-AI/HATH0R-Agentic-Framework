"""Deep Telemetry Autoencoder for Multivariate Anomaly & Token-Tax Drift Detection.

Implements an unsupervised bottleneck autoencoder network over multi-dimensional OpenInference
agent execution telemetry (prompt tokens, completion tokens, latency, cost, step count, tool calls).
Detects subtle multivariate execution anomalies, recursive agent thrashing, and token explosions.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


def _relu(x: float) -> float:
    return max(0.0, x)


@dataclass
class AnomalyRecord:
    """Individual telemetry anomaly detection result."""

    span_id: str
    reconstruction_loss: float
    threshold: float
    is_anomaly: bool
    root_cause: str
    feature_contributions: Dict[str, float]


@dataclass
class AnomalyDetectionReport:
    """Aggregated anomaly detection report across a batch of agent spans."""

    total_spans_analyzed: int
    anomalies_detected: int
    anomaly_rate: float
    baseline_threshold: float
    mean_reconstruction_loss: float
    anomalous_records: List[AnomalyRecord]


class TelemetryAutoencoder:
    """Deep autoencoder neural network for tabular agent telemetry representation and anomaly detection."""

    FEATURE_NAMES: List[str] = [
        "prompt_tokens",
        "completion_tokens",
        "latency_ms",
        "cost_usd",
        "step_count",
        "tool_call_count",
    ]
    INPUT_DIM: int = 6
    HIDDEN_DIM: int = 4
    LATENT_DIM: int = 2

    def __init__(self, random_seed: int = 42) -> None:
        self.random_seed = random_seed
        rng = random.Random(random_seed)

        # Baseline normalization statistics (mean and std per feature)
        self.feature_means: List[float] = [250.0, 50.0, 120.0, 0.001, 3.0, 2.0]
        self.feature_stds: List[float] = [150.0, 30.0, 60.0, 0.0008, 1.5, 1.2]
        self.threshold: float = 2.5

        # Encoder Layer 1: [INPUT_DIM -> HIDDEN_DIM]
        s1 = math.sqrt(2.0 / (self.INPUT_DIM + self.HIDDEN_DIM))
        self.w_enc1 = [[rng.gauss(0.0, s1) for _ in range(self.INPUT_DIM)] for _ in range(self.HIDDEN_DIM)]
        self.b_enc1 = [0.0] * self.HIDDEN_DIM

        # Encoder Layer 2: [HIDDEN_DIM -> LATENT_DIM]
        s2 = math.sqrt(2.0 / (self.HIDDEN_DIM + self.LATENT_DIM))
        self.w_enc2 = [[rng.gauss(0.0, s2) for _ in range(self.HIDDEN_DIM)] for _ in range(self.LATENT_DIM)]
        self.b_enc2 = [0.0] * self.LATENT_DIM

        # Decoder Layer 1: [LATENT_DIM -> HIDDEN_DIM]
        s3 = math.sqrt(2.0 / (self.LATENT_DIM + self.HIDDEN_DIM))
        self.w_dec1 = [[rng.gauss(0.0, s3) for _ in range(self.LATENT_DIM)] for _ in range(self.HIDDEN_DIM)]
        self.b_dec1 = [0.0] * self.HIDDEN_DIM

        # Decoder Layer 2: [HIDDEN_DIM -> INPUT_DIM]
        s4 = math.sqrt(2.0 / (self.HIDDEN_DIM + self.INPUT_DIM))
        self.w_dec2 = [[rng.gauss(0.0, s4) for _ in range(self.HIDDEN_DIM)] for _ in range(self.INPUT_DIM)]
        self.b_dec2 = [0.0] * self.INPUT_DIM

    def _normalize(self, raw_features: List[float]) -> List[float]:
        """Z-score normalization of raw telemetry features."""
        norm = []
        for i, val in enumerate(raw_features):
            m = self.feature_means[i]
            s = max(1e-6, self.feature_stds[i])
            norm.append((val - m) / s)
        return norm

    def encode(self, x: List[float]) -> List[float]:
        """Encode normalized features into 2D latent representation."""
        h1 = []
        for i in range(self.HIDDEN_DIM):
            z = sum(w * f for w, f in zip(self.w_enc1[i], x)) + self.b_enc1[i]
            h1.append(_relu(z))

        latent = []
        for i in range(self.LATENT_DIM):
            z = sum(w * h for w, h in zip(self.w_enc2[i], h1)) + self.b_enc2[i]
            latent.append(z)
        return latent

    def decode(self, latent: List[float]) -> List[float]:
        """Decode 2D latent representation back to reconstructed normalized features."""
        h1 = []
        for i in range(self.HIDDEN_DIM):
            z = sum(w * l for w, l in zip(self.w_dec1[i], latent)) + self.b_dec1[i]
            h1.append(_relu(z))

        recon = []
        for i in range(self.INPUT_DIM):
            z = sum(w * h for w, h in zip(self.w_dec2[i], h1)) + self.b_dec2[i]
            recon.append(z)
        return recon

    def forward(self, raw_features: List[float]) -> Tuple[List[float], float, Dict[str, float]]:
        """Forward pass computing reconstructed features, MSE loss, and feature errors."""
        norm_x = self._normalize(raw_features)
        latent = self.encode(norm_x)
        recon_x = self.decode(latent)

        # Feature-wise squared error
        feat_errors: Dict[str, float] = {}
        for i, name in enumerate(self.FEATURE_NAMES):
            diff = norm_x[i] - recon_x[i]
            feat_errors[name] = round(diff * diff, 4)

        # Mean Squared Reconstruction Error
        total_loss = sum(feat_errors.values()) / float(self.INPUT_DIM)
        return recon_x, round(total_loss, 4), feat_errors

    def _diagnose_root_cause(self, feat_errors: Dict[str, float]) -> str:
        """Diagnose anomaly root cause from dominant feature reconstruction error."""
        top_feature = max(feat_errors.items(), key=lambda x: x[1])[0]
        if top_feature in ("step_count", "tool_call_count"):
            return "RECURSIVE_TOOL_LOOP"
        if top_feature == "prompt_tokens":
            return "PROMPT_TAX_EXPLOSION"
        if top_feature == "latency_ms":
            return "LATENCY_STALL"
        if top_feature == "cost_usd":
            return "FINOPS_BUDGET_SPIKE"
        return f"ANOMALOUS_{top_feature.upper()}"

    def fit_baseline(self, healthy_spans: List[Dict[str, Any]]) -> None:
        """Calibrate normalization baseline and anomaly threshold from healthy spans."""
        if not healthy_spans:
            return

        feature_matrix = []
        for s in healthy_spans:
            row = [
                float(s.get("prompt_tokens", 250.0)),
                float(s.get("completion_tokens", 50.0)),
                float(s.get("latency_ms", 120.0)),
                float(s.get("cost_usd", 0.001)),
                float(s.get("step_count", 3.0)),
                float(s.get("tool_call_count", 2.0)),
            ]
            feature_matrix.append(row)

        n = len(feature_matrix)
        for i in range(self.INPUT_DIM):
            col = [row[i] for row in feature_matrix]
            m = sum(col) / n
            var = sum((c - m) ** 2 for c in col) / max(1, n - 1)
            self.feature_means[i] = m
            self.feature_stds[i] = math.sqrt(var)

        # Compute reconstruction errors on baseline to set 3-sigma threshold
        losses = []
        for row in feature_matrix:
            _, loss, _ = self.forward(row)
            losses.append(loss)

        mean_loss = sum(losses) / n
        std_loss = math.sqrt(sum((l - mean_loss) ** 2 for l in losses) / max(1, n - 1))
        self.threshold = round(mean_loss + 3.0 * std_loss, 4)

    def detect_anomalies(self, spans: List[Dict[str, Any]]) -> AnomalyDetectionReport:
        """Detect anomalies across a batch of OpenInference telemetry spans."""
        if not spans:
            return AnomalyDetectionReport(
                total_spans_analyzed=0,
                anomalies_detected=0,
                anomaly_rate=0.0,
                baseline_threshold=self.threshold,
                mean_reconstruction_loss=0.0,
                anomalous_records=[],
            )

        anomalous_records: List[AnomalyRecord] = []
        total_loss = 0.0

        for s in spans:
            span_id = str(s.get("span_id", s.get("id", "span-unknown")))
            row = [
                float(s.get("prompt_tokens", self.feature_means[0])),
                float(s.get("completion_tokens", self.feature_means[1])),
                float(s.get("latency_ms", self.feature_means[2])),
                float(s.get("cost_usd", self.feature_means[3])),
                float(s.get("step_count", self.feature_means[4])),
                float(s.get("tool_call_count", self.feature_means[5])),
            ]

            _, loss, feat_errors = self.forward(row)
            total_loss += loss
            is_anomaly = loss > self.threshold

            if is_anomaly:
                root_cause = self._diagnose_root_cause(feat_errors)
                anomalous_records.append(
                    AnomalyRecord(
                        span_id=span_id,
                        reconstruction_loss=loss,
                        threshold=self.threshold,
                        is_anomaly=True,
                        root_cause=root_cause,
                        feature_contributions=feat_errors,
                    )
                )

        mean_loss = round(total_loss / max(1, len(spans)), 4)
        anomaly_count = len(anomalous_records)
        rate = round(anomaly_count / max(1, len(spans)), 4)

        return AnomalyDetectionReport(
            total_spans_analyzed=len(spans),
            anomalies_detected=anomaly_count,
            anomaly_rate=rate,
            baseline_threshold=self.threshold,
            mean_reconstruction_loss=mean_loss,
            anomalous_records=anomalous_records,
        )


telemetry_autoencoder = TelemetryAutoencoder()
