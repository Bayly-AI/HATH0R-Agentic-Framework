"""Comprehensive Tests for FinOps Token Telemetry and Histogram Analytics."""

import json
from pathlib import Path

import pytest

from hath0r_engine.gateway.base import (
    ComplexityTier,
    CompletionRequest,
    GatewayConfig,
    ModelProvider,
)
from hath0r_engine.gateway.client import AIGatewayClient
from hath0r_engine.telemetry.token_telemetry import (
    HistogramBin,
    TokenHistogramBot,
    TokenTelemetryBot,
    TokenTelemetryLedger,
    TokenTelemetryRecord,
)


class TestTokenTelemetryRecord:
    """Validate data model serialization and defaults."""

    def test_record_defaults_and_serialization(self):
        rec = TokenTelemetryRecord(
            user_id="alice",
            prompt_length_chars=40,
            prompt_tokens=10,
            completion_length_chars=20,
            completion_tokens=5,
            total_tokens=15,
            cost_usd=0.000105,
        )
        assert rec.id.startswith("tok_")
        assert rec.user_id == "alice"
        assert rec.total_tokens == 15

        data = rec.to_dict()
        assert data["user_id"] == "alice"
        assert data["cost_usd"] == 0.000105
        assert "timestamp" in data

        restored = TokenTelemetryRecord.from_dict(data)
        assert restored.id == rec.id
        assert restored.user_id == rec.user_id
        assert restored.total_tokens == 15


class TestTokenTelemetryLedger:
    """Validate append-only persistence and query filtering."""

    @pytest.fixture
    def temp_ledger(self, tmp_path: Path):
        ledger_file = tmp_path / "finops" / "test_tokens.jsonl"
        return TokenTelemetryLedger(ledger_path=ledger_file)

    def test_append_and_read(self, temp_ledger: TokenTelemetryLedger):
        assert temp_ledger.read_all() == []

        r1 = TokenTelemetryRecord(user_id="user_1", prompt_tokens=10, total_tokens=15)
        r2 = TokenTelemetryRecord(user_id="user_2", prompt_tokens=20, total_tokens=30)
        temp_ledger.append(r1)
        temp_ledger.append(r2)

        records = temp_ledger.read_all()
        assert len(records) == 2
        assert records[0].user_id == "user_1"
        assert records[1].user_id == "user_2"

    def test_query_filtering(self, temp_ledger: TokenTelemetryLedger):
        r1 = TokenTelemetryRecord(user_id="alice", model="claude-3-5-sonnet", tier="standard", prompt_tokens=100)
        r2 = TokenTelemetryRecord(user_id="bob", model="gpt-4o", tier="standard", prompt_tokens=200)
        r3 = TokenTelemetryRecord(user_id="alice", model="gpt-4o-mini", tier="light", prompt_tokens=50)

        temp_ledger.append(r1)
        temp_ledger.append(r2)
        temp_ledger.append(r3)

        # Filter by user
        alice_recs = temp_ledger.query(user_id="alice")
        assert len(alice_recs) == 2
        assert all(r.user_id == "alice" for r in alice_recs)

        # Filter by model
        gpt_recs = temp_ledger.query(model="gpt-4o")
        assert len(gpt_recs) == 1
        assert gpt_recs[0].user_id == "bob"

        # Limit
        limited = temp_ledger.query(limit=2)
        assert len(limited) == 2


class TestTokenTelemetryBot:
    """Validate prompt ingestion, cost calculation, and user summary metrics."""

    @pytest.fixture
    def telemetry_bot(self, tmp_path: Path):
        ledger_path = tmp_path / "telemetry.jsonl"
        return TokenTelemetryBot(ledger_path=ledger_path)

    def test_cost_calculation(self):
        # Light: $0.15 / 1M in, $0.60 / 1M out
        cost_light = TokenTelemetryBot.calculate_cost(prompt_tokens=1_000_000, completion_tokens=1_000_000, tier="light")
        assert pytest.approx(cost_light, rel=1e-5) == 0.75

        # Standard: $3.00 / 1M in, $15.00 / 1M out
        cost_standard = TokenTelemetryBot.calculate_cost(prompt_tokens=100_000, completion_tokens=10_000, tier="standard")
        # 100k * 3/1M = 0.30, 10k * 15/1M = 0.15 -> 0.45
        assert pytest.approx(cost_standard, rel=1e-5) == 0.45

    def test_record_prompt_ingestion(self, telemetry_bot: TokenTelemetryBot):
        prompt = "Hello agent, please review the pull request."
        rec = telemetry_bot.record_prompt(
            prompt=prompt,
            user_id="raybayly",
            model="claude-3-5-sonnet",
            tier="standard",
            completion="Review completed without issues.",
        )

        assert rec.user_id == "raybayly"
        assert rec.prompt_length_chars == len(prompt)
        assert rec.prompt_tokens > 0
        assert rec.cost_usd > 0.0

        records = telemetry_bot.query_records(user_id="raybayly")
        assert len(records) == 1
        assert records[0].id == rec.id

    def test_user_summary_aggregation(self, telemetry_bot: TokenTelemetryBot):
        telemetry_bot.record_prompt("Task 1", user_id="alice", tier="light")
        telemetry_bot.record_prompt("Task 2", user_id="alice", tier="standard")
        telemetry_bot.record_prompt("Task 3", user_id="bob", tier="reasoning")

        summary = telemetry_bot.get_user_summary()
        assert "alice" in summary
        assert "bob" in summary
        assert summary["alice"]["total_requests"] == 2
        assert summary["bob"]["total_requests"] == 1


class TestTokenHistogramBot:
    """Validate statistical calculation, bin distribution, and visualizations."""

    def test_histogram_empty_records(self):
        hist = TokenHistogramBot.build_histogram([])
        assert hist["total_records"] == 0
        assert hist["total_tokens"] == 0
        assert hist["stats"]["mean"] == 0.0
        assert len(hist["bins"]) == 1

    def test_histogram_distribution_and_stats(self):
        records = [
            TokenTelemetryRecord(user_id="u1", prompt_tokens=10, prompt_length_chars=40, total_tokens=15, cost_usd=0.01),
            TokenTelemetryRecord(user_id="u1", prompt_tokens=20, prompt_length_chars=80, total_tokens=30, cost_usd=0.02),
            TokenTelemetryRecord(user_id="u2", prompt_tokens=30, prompt_length_chars=120, total_tokens=45, cost_usd=0.03),
            TokenTelemetryRecord(user_id="u2", prompt_tokens=40, prompt_length_chars=160, total_tokens=60, cost_usd=0.04),
            TokenTelemetryRecord(user_id="u3", prompt_tokens=100, prompt_length_chars=400, total_tokens=150, cost_usd=0.10),
        ]

        hist = TokenHistogramBot.build_histogram(records, metric="prompt_tokens", bins_count=5)

        assert hist["total_records"] == 5
        assert hist["total_tokens"] == 15 + 30 + 45 + 60 + 150
        assert hist["stats"]["min"] == 10.0
        assert hist["stats"]["max"] == 100.0
        assert hist["stats"]["mean"] == 40.0
        assert hist["stats"]["median"] == 30.0
        assert len(hist["bins"]) == 5

        # Check bin sum
        sum_counts = sum(b["count"] for b in hist["bins"])
        assert sum_counts == 5

        # Verify distributions
        assert "u1" in hist["user_distribution"]
        assert "u2" in hist["user_distribution"]
        assert hist["user_distribution"]["u1"]["count"] == 2

    def test_ascii_and_generative_ui_rendering(self):
        records = [
            TokenTelemetryRecord(user_id="u1", prompt_tokens=10, total_tokens=20, cost_usd=0.005),
            TokenTelemetryRecord(user_id="u2", prompt_tokens=50, total_tokens=100, cost_usd=0.025),
        ]
        hist = TokenHistogramBot.build_histogram(records, metric="prompt_tokens", bins_count=2)

        # ASCII render
        ascii_out = TokenHistogramBot.render_ascii(hist)
        assert "Hath0r FinOps Histogram" in ascii_out
        assert "Range" in ascii_out
        assert "Distribution" in ascii_out

        # Generative UI HTML render
        html_out = TokenHistogramBot.generate_generative_ui_html(hist)
        assert "<!DOCTYPE html>" in html_out
        assert "Hath0r Agent Token Telemetry Histogram" in html_out
        assert "Total Spend" in html_out


class TestAIGatewayIntegration:
    """Validate automatic prompt token telemetry capture via AIGatewayClient."""

    def test_gateway_automatic_telemetry_capture(self, tmp_path: Path):
        ledger_path = tmp_path / "gw_tokens.jsonl"
        telemetry_bot = TokenTelemetryBot(ledger_path=ledger_path)

        client = AIGatewayClient(
            config=GatewayConfig(gateway_type=ModelProvider.MOCK, semantic_cache_enabled=False),
            token_telemetry=telemetry_bot,
        )

        req = CompletionRequest(
            prompt="Summarize the deployment logs for cluster A.",
            tier=ComplexityTier.STANDARD,
            metadata={"user_id": "operator_42", "session_id": "sess_abc"},
        )

        resp = client.complete(req)
        assert resp.total_tokens > 0

        # Check telemetry ledger
        records = telemetry_bot.query_records(user_id="operator_42")
        assert len(records) == 1
        r = records[0]
        assert r.user_id == "operator_42"
        assert r.session_id == "sess_abc"
        assert r.prompt_length_chars == len(req.prompt)
        assert r.total_tokens == resp.total_tokens
        assert r.cost_usd > 0.0
