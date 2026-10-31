"""Unit tests for Deep Telemetry Autoencoder and multivariate anomaly detection."""

from hath0r_engine.telemetry.autoencoder import (
    AnomalyDetectionReport,
    TelemetryAutoencoder,
)


def test_telemetry_autoencoder_forward_and_reconstruction():
    ae = TelemetryAutoencoder(random_seed=42)

    # Normal baseline feature row: [prompt_tokens, completion_tokens, latency_ms, cost_usd, step_count, tool_call_count]
    normal_row = [240.0, 48.0, 115.0, 0.00095, 3.0, 2.0]
    recon, loss, feat_errors = ae.forward(normal_row)

    assert len(recon) == 6
    assert isinstance(loss, float)
    assert set(feat_errors.keys()) == set(ae.FEATURE_NAMES)
    # On near-mean inputs, normalized reconstruction loss should be low
    assert loss < ae.threshold


def test_telemetry_autoencoder_detects_token_explosion():
    ae = TelemetryAutoencoder(random_seed=42)

    # Severe token tax spike: 50,000 prompt tokens (vs baseline 250)
    abnormal_span = {
        "span_id": "span_runaway_tax",
        "prompt_tokens": 50000.0,
        "completion_tokens": 80.0,
        "latency_ms": 3500.0,
        "cost_usd": 0.15,
        "step_count": 2.0,
        "tool_call_count": 1.0,
    }

    report = ae.detect_anomalies([abnormal_span])
    assert isinstance(report, AnomalyDetectionReport)
    assert report.total_spans_analyzed == 1
    assert report.anomalies_detected == 1
    assert report.anomaly_rate == 1.0

    record = report.anomalous_records[0]
    assert record.is_anomaly is True
    assert record.root_cause in ("PROMPT_TAX_EXPLOSION", "FINOPS_BUDGET_SPIKE", "LATENCY_STALL")
    assert record.reconstruction_loss > report.baseline_threshold


def test_telemetry_autoencoder_detects_recursive_tool_loop():
    ae = TelemetryAutoencoder(random_seed=42)

    # Recursive loop thrashing: 85 steps, 120 tool calls with near-zero completions
    loop_span = {
        "span_id": "span_infinite_loop",
        "prompt_tokens": 300.0,
        "completion_tokens": 10.0,
        "latency_ms": 4200.0,
        "cost_usd": 0.005,
        "step_count": 85.0,
        "tool_call_count": 120.0,
    }

    report = ae.detect_anomalies([loop_span])
    assert report.anomalies_detected == 1
    record = report.anomalous_records[0]
    assert record.root_cause == "RECURSIVE_TOOL_LOOP"


def test_telemetry_autoencoder_fit_baseline():
    ae = TelemetryAutoencoder(random_seed=42)
    baseline_spans = [
        {
            "prompt_tokens": 200.0 + i * 5,
            "completion_tokens": 40.0 + i,
            "latency_ms": 100.0 + i * 2,
            "cost_usd": 0.0008,
            "step_count": 2.0,
            "tool_call_count": 1.0,
        }
        for i in range(20)
    ]

    ae.fit_baseline(baseline_spans)
    assert ae.threshold > 0.0

    # Normal spans should not trigger anomaly
    clean_report = ae.detect_anomalies(baseline_spans[:5])
    assert clean_report.anomalies_detected == 0
