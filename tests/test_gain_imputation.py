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


def test_gain_architecture_generator_discriminator():
    from hath0r_engine.calibration.gain_imputation import GAINGenerator, GAINDiscriminator

    gen = GAINGenerator(dim=3, hidden_dim=16)
    disc = GAINDiscriminator(dim=3, hidden_dim=16)

    # Generator forward pass
    x_tilde = [0.2, 0.5, 0.1]
    mask = [1.0, 0.0, 1.0]
    out_g = gen.forward(x_tilde, mask)
    assert len(out_g) == 3
    assert all(0.0 <= val <= 1.0 for val in out_g)

    # Discriminator forward pass
    hint = [1.0, 0.5, 1.0]
    out_d = disc.forward(out_g, hint)
    assert len(out_d) == 3
    assert all(0.0 <= p <= 1.0 for p in out_d)


def test_gain_adversarial_telemetry_reconstruction():
    engine = GainImputationEngine(random_seed=42)
    spans = [
        {"span_id": f"span_{i}", "latency_ms": 100.0 + i * 10, "token_count": 200 + i * 50, "cost_usd": 0.001 + i * 0.0002}
        for i in range(10)
    ]
    # Knock out 30% of fields
    spans[1]["latency_ms"] = None
    spans[3]["token_count"] = None
    spans[5]["cost_usd"] = None
    spans[7]["latency_ms"] = None
    spans[7]["cost_usd"] = None

    result = engine.impute_span_telemetry(spans)
    assert result["architecture"] == "GAIN"
    assert result["imputed_count"] == 5
    assert result["imputation_rate"] > 0.0
    assert "generator_loss" in result
    assert "discriminator_loss" in result
    assert result["generator_loss"] > 0.0
    assert result["discriminator_loss"] > 0.0

    # Ensure all imputed records are clean numbers
    for rec in result["records"]:
        assert isinstance(rec["latency_ms"], (int, float))
        assert isinstance(rec["token_count"], int)
        assert isinstance(rec["cost_usd"], (int, float))

