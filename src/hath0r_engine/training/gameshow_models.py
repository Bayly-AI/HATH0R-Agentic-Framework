"""Domain-agnostic Pydantic models for Hath0r Gameshow RAG/CAG Evaluation & Calibration Substrate."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CardAttempt(BaseModel):
    """Record of a single attempt on an evaluation card during a tournament round."""

    round_num: int = Field(description="Tournament round number (1, 2, ...)")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    question: str = Field(description="Prompt or question submitted to the agent")
    agent_response: str = Field(description="Raw text or HTML response returned by the agent")
    model_used: str = Field(default="embedded_agent", description="Model identifier or engine that generated the response")
    tools_executed: List[str] = Field(default_factory=list, description="List of tool names executed during resolution")
    is_correct: bool = Field(description="Judge evaluation verdict")
    score: float = Field(default=0.0, ge=0.0, le=1.0, description="Normalized score from 0.0 to 1.0")
    reason: str = Field(description="Detailed explanation of the judge's verdict")
    latency_ms: Optional[int] = Field(default=None, description="Response time in milliseconds")


class EvaluationCard(BaseModel):
    """An atomic evaluation card in a benchmark tournament deck."""

    card_id: str = Field(description="Unique card identifier, e.g. 'CARD-0001'")
    epoch: int = Field(default=1, description="Epoch index (1-based)")
    domain: str = Field(description="Domain or category tag for grouping and domain convergence tracking")
    question: str = Field(description="Natural language prompt or query")
    expected_answer: str = Field(description="Authoritative ground-truth answer")
    key_facts: List[str] = Field(
        default_factory=list,
        description="Essential entity names, numeric values, or key phrases required for passing",
    )
    sql_provenance: Optional[str] = Field(default="", description="Primary source or query provenance")
    status: str = Field(
        default="unanswered",
        description="Card state: 'unanswered', 'correct', 'incorrect'",
    )
    calibrated: bool = Field(
        default=False,
        description="Whether this card has been ingested into CAG calibration memory",
    )
    attempts: List[CardAttempt] = Field(
        default_factory=list,
        description="Chronological log of attempts across tournament rounds",
    )


# Backward-compatible alias
GameshowCard = EvaluationCard


class TournamentRoundStats(BaseModel):
    """Statistical summary of a tournament evaluation round."""

    round_num: int
    started_at: str
    completed_at: str
    total_cards: int
    cards_evaluated: int
    correct_cards: int
    incorrect_cards: int
    accuracy_pct: float
    domain_breakdown: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    calibrated_before_round: int = 0
    incorrect_card_ids: List[str] = Field(default_factory=list)


# Backward-compatible alias
GameshowRoundStats = TournamentRoundStats


class TournamentDeckState(BaseModel):
    """Persistent state of a tournament benchmark epoch."""

    epoch: int = 1
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    total_cards: int = 1000
    current_round: int = 0
    is_completed: bool = False
    rounds: List[TournamentRoundStats] = Field(default_factory=list)
    cards: Dict[str, EvaluationCard] = Field(default_factory=dict)


# Backward-compatible alias
GameshowDeckState = TournamentDeckState
