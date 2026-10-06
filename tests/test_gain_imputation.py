"""Unit tests for GAIN Telemetry Imputation & Taguchi Calibration Substrate."""

import datetime
from hath0r_engine.calibration.gain_imputation import GainImputationEngine, gain_imputation_engine


def test_impute_span_telemetry():
    engine = GainImputationEngine()
    spans = [
        {"span_id": "s1", "latency_ms": 120.0, "token_count": 300, "cost_usd": 0.0015},
        {"span_id": "s2", "latency_ms": None, "token_count": 400, "cost_usd": None},
        {"span_id": "s3", "latency_ms": 180.0, "token_count": None, "cost_usd": 0.0025},
    ]

    res = engine.impute_span_telemetry(spans)
    assert res["imputed_count"] == 3
    assert res["imputation_rate"] > 0.0
    assert len(res["records"]) == 3

    # Check imputed record values
    r2 = res["records"][1]
    assert r2["latency_ms"] is not None
    assert r2["cost_usd"] is not None
    assert r2["is_imputed"] is True


def test_evaluate_calibration_freshness():
    engine = GainImputationEngine()

    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    f1 = engine.evaluate_calibration_freshness(now_iso)
    assert f1["is_fresh"] is True
    assert f1["needs_recalibration"] is False

    old_iso = (datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=30)).isoformat()
    f2 = engine.evaluate_calibration_freshness(old_iso)
    assert f2["is_fresh"] is False
    assert f2["needs_recalibration"] is True
