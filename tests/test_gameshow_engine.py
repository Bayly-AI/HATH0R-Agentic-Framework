"""Unit tests for Hath0r Gameshow Engine, CAG Registry, Judge, and Models."""

import os
import tempfile

from hath0r_engine.calibration.cag_registry import CAGCalibrationRegistry
from hath0r_engine.training.gameshow_judge import GameshowJudge
from hath0r_engine.training.gameshow_models import (
    EvaluationCard,
    TournamentDeckState,
)


def test_gameshow_card_and_deck_model():
    """Verify serialization of EvaluationCard and TournamentDeckState."""
    card = EvaluationCard(
        card_id="CARD-0001",
        epoch=1,
        domain="security",
        question="What is the cryptographic hash used for git commits?",
        expected_answer="Git historically uses SHA-1 and supports SHA-256 object formats.",
        key_facts=["SHA-1", "SHA-256", "Git"],
        sql_provenance="RFC 4880",
    )
    assert card.card_id == "CARD-0001"
    assert card.status == "unanswered"
    assert not card.calibrated

    deck = TournamentDeckState(
        epoch=1,
        total_cards=1,
        cards={"CARD-0001": card},
    )
    assert deck.total_cards == 1
    assert deck.current_round == 0
    assert not deck.is_completed


def test_gameshow_judge_evaluation_pass():
    """Verify GameshowJudge fact matching and score calculation."""
    judge = GameshowJudge()
    card = EvaluationCard(
        card_id="CARD-0002",
        domain="infrastructure",
        question="What port does Postgres run on by default?",
        expected_answer="PostgreSQL listens on TCP port 5432 by default.",
        key_facts=["5432", "PostgreSQL", "TCP"],
    )

    good_response = "<p>PostgreSQL runs on TCP port 5432.</p>"
    is_correct, score, reason = judge.evaluate(card, good_response)
    assert is_correct is True
    assert score >= 0.65
    assert "key facts confirmed" in reason


def test_gameshow_judge_evaluation_missing_facts():
    """Verify GameshowJudge fails responses with missing key facts."""
    judge = GameshowJudge()
    card = EvaluationCard(
        card_id="CARD-0003",
        domain="networking",
        question="What are the three TCP handshake flags?",
        expected_answer="The three steps are SYN, SYN-ACK, and ACK.",
        key_facts=["SYN", "SYN-ACK", "ACK"],
    )

    incomplete_response = "<p>The handshake starts with SYN.</p>"
    is_correct, score, reason = judge.evaluate(card, incomplete_response)
    assert is_correct is False
    assert "Missing key facts" in reason


def test_gameshow_judge_directional_contradiction():
    """Verify GameshowJudge detects directional contradiction (Yea vs Nay)."""
    judge = GameshowJudge()
    card = EvaluationCard(
        card_id="CARD-0004",
        domain="governance",
        question="Did the proposal pass?",
        expected_answer="The motion passed with a Yea vote.",
        key_facts=["passed", "Yea"],
    )

    contra_response = "<p>The motion received a Nay vote and failed.</p>"
    is_correct, score, reason = judge.evaluate(card, contra_response)
    assert is_correct is False
    assert "contradiction" in reason.lower()


def test_cag_registry_lifecycle():
    """Verify CAGCalibrationRegistry training, Jaccard lookup, and persistence."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        cache_path = os.path.join(tmp_dir, "test_cag_cache.json")
        registry = CAGCalibrationRegistry(persistence_path=cache_path, similarity_threshold=0.80)

        card = EvaluationCard(
            card_id="CAL-0001",
            domain="protocols",
            question="What is the default port for HTTPS traffic?",
            expected_answer="HTTPS traffic defaults to TCP port 443.",
            key_facts=["443", "HTTPS"],
        )

        assert registry.count == 0
        registry.calibrate_card(card)
        assert registry.count == 1
        assert registry.is_calibrated("CAL-0001")

        # Test sub-millisecond lookup hit with exact and high token overlap
        match = registry.lookup_calibrated_fact("What is the default port for HTTPS traffic?")
        assert match is not None
        assert match["card_id"] == "CAL-0001"
        assert match["expected_answer"] == "HTTPS traffic defaults to TCP port 443."

        # Test lookup miss for unrelated question
        miss = registry.lookup_calibrated_fact("What is the capital of France?")
        assert miss is None

        # Test system prompt injection
        prompt_snippet = registry.get_active_calibration_prompt()
        assert "ACTIVE CAG CONTINUOUS CALIBRATION KNOWLEDGE" in prompt_snippet
        assert "HTTPS" in prompt_snippet

        # Test persistence
        registry.save_to_disk()
        assert os.path.exists(cache_path)

        # Reload in new instance
        new_registry = CAGCalibrationRegistry(persistence_path=cache_path)
        assert new_registry.count == 1
        re_match = new_registry.lookup_calibrated_fact("What is the default port for HTTPS traffic?")
        assert re_match is not None
        assert re_match["card_id"] == "CAL-0001"
