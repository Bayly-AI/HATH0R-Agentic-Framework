"""Continuous Calibration & Cache-Augmented Generation (CAG) Registry for Hath0r.

Provides dynamic agent training, memory augmentation, and sub-millisecond CAG
ground-truth recall for LLM agents. Incorrect cards from evaluation tournament
rounds are ingested into the registry to calibrate agent outputs dynamically
without retraining model weights.
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any, Dict, List, Optional, Set

from hath0r_engine.training.gameshow_models import EvaluationCard

logger = logging.getLogger("hath0r_engine.calibration.cag_registry")

DEFAULT_STOPWORDS: Set[str] = {
    "a", "an", "the", "and", "or", "of", "to", "in", "on", "at", "by", "for",
    "with", "about", "is", "are", "was", "were", "be", "been", "being", "have",
    "has", "had", "do", "does", "did", "who", "what", "where", "when", "why",
    "how", "can", "tell", "give", "me", "please", "my", "your", "their", "it",
}


class CAGCalibrationRegistry:
    """In-memory and file-backed calibration store for dynamic agent memory augmentation."""

    def __init__(
        self,
        persistence_path: Optional[str] = None,
        similarity_threshold: float = 0.85,
        stopwords: Optional[Set[str]] = None,
    ) -> None:
        self._persistence_path = persistence_path
        self.similarity_threshold = similarity_threshold
        self.stopwords = stopwords or DEFAULT_STOPWORDS
        self._calibrated_cards: Dict[str, Dict[str, Any]] = {}
        self._question_patterns: List[Dict[str, Any]] = []
        self._domain_knowledge: Dict[str, List[str]] = {}

        if self._persistence_path and os.path.exists(self._persistence_path):
            self.load_from_disk()

    @property
    def count(self) -> int:
        """Total number of calibrated cards."""
        return len(self._calibrated_cards)

    def is_calibrated(self, card_id: str) -> bool:
        """Check if a card ID has already been trained/calibrated."""
        return card_id in self._calibrated_cards

    def clear(self) -> None:
        """Clear all calibrated knowledge from memory and disk."""
        self._calibrated_cards.clear()
        self._question_patterns.clear()
        self._domain_knowledge.clear()
        if self._persistence_path and os.path.exists(self._persistence_path):
            try:
                os.remove(self._persistence_path)
            except Exception as exc:
                logger.warning("Could not remove calibration cache file: %s", exc)

    def _tokenize(self, text: str) -> Set[str]:
        """Normalize string and extract non-stopword tokens."""
        norm_q = " ".join(re.sub(r"[^\w\s]", " ", text.lower()).split())
        return {t for t in norm_q.split() if len(t) >= 2 and t not in self.stopwords}

    def calibrate_card(self, card: EvaluationCard) -> bool:
        """Train the registry on an individual card."""
        if not card.card_id:
            return False

        card_entry = {
            "card_id": card.card_id,
            "domain": card.domain,
            "question": card.question,
            "expected_answer": card.expected_answer,
            "key_facts": card.key_facts,
            "sql_provenance": card.sql_provenance or "",
        }
        self._calibrated_cards[card.card_id] = card_entry

        norm_q = " ".join(re.sub(r"[^\w\s]", " ", card.question.lower()).split())
        tokens = self._tokenize(card.question)

        self._question_patterns.append({
            "card_id": card.card_id,
            "domain": card.domain,
            "raw_question": card.question,
            "clean_question": norm_q,
            "tokens": tokens,
            "expected_answer": card.expected_answer,
            "key_facts": card.key_facts,
            "sql_provenance": card.sql_provenance or "",
        })

        if card.domain not in self._domain_knowledge:
            self._domain_knowledge[card.domain] = []
        fact_summary = f"Q: {card.question} -> Verified Fact: {card.expected_answer}"
        if fact_summary not in self._domain_knowledge[card.domain]:
            self._domain_knowledge[card.domain].append(fact_summary)

        return True

    def calibrate_cards(self, cards: List[EvaluationCard]) -> int:
        """Train the registry on a batch of cards."""
        added = 0
        for c in cards:
            if self.calibrate_card(c):
                added += 1
        if self._persistence_path and added > 0:
            self.save_to_disk()
        return added

    def lookup_calibrated_fact(self, user_prompt: str) -> Optional[Dict[str, Any]]:
        """Perform sub-millisecond similarity matching against calibrated ground truth.

        Returns matching card dictionary if similarity meets or exceeds threshold.
        """
        if not self._question_patterns:
            return None

        clean_user = " ".join(re.sub(r"[^\w\s]", " ", user_prompt.lower()).split())
        user_tokens = self._tokenize(user_prompt)

        if not user_tokens:
            return None

        best_match: Optional[Dict[str, Any]] = None
        best_score = 0.0

        for pattern in self._question_patterns:
            # 1. Exact string normalization match (score 1.0)
            if clean_user == pattern["clean_question"]:
                return pattern

            pattern_tokens = pattern["tokens"]
            if not pattern_tokens:
                continue

            # 2. Tokenized Jaccard similarity
            intersection = len(user_tokens.intersection(pattern_tokens))
            union = len(user_tokens.union(pattern_tokens))
            jaccard = intersection / union if union > 0 else 0.0

            # 3. Containment boost if all key tokens exist in user prompt
            if pattern_tokens.issubset(user_tokens):
                jaccard = max(jaccard, 0.90)

            if jaccard > best_score:
                best_score = jaccard
                best_match = pattern

        if best_match and best_score >= self.similarity_threshold:
            logger.debug(
                "CAG match hit for '%s' (Card %s, score=%.2f)",
                user_prompt[:30],
                best_match["card_id"],
                best_score,
            )
            return best_match

        return None

    def get_active_calibration_prompt(self, max_facts: int = 100) -> str:
        """Synthesize dynamic prompt instructions from calibrated facts to augment system prompts."""
        if not self._domain_knowledge:
            return ""

        sections = ["### ACTIVE CAG CONTINUOUS CALIBRATION KNOWLEDGE:"]
        facts_emitted = 0

        for domain, facts in self._domain_knowledge.items():
            if facts_emitted >= max_facts:
                break
            domain_label = domain.replace("_", " ").title()
            sections.append(f"#### Domain: {domain_label}")
            for f in facts:
                if facts_emitted >= max_facts:
                    break
                sections.append(f"- {f}")
                facts_emitted += 1

        sections.append(
            "\nPrioritize verified facts above over ungrounded speculation or generic summaries."
        )
        return "\n".join(sections)

    def save_to_disk(self, target_path: Optional[str] = None) -> None:
        """Persist calibrated ground-truth registry to disk."""
        path = target_path or self._persistence_path
        if not path:
            return
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        serializable = {
            "count": len(self._calibrated_cards),
            "similarity_threshold": self.similarity_threshold,
            "calibrated_cards": self._calibrated_cards,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, indent=2)
        logger.info("Saved %d calibrated cards to %s", len(self._calibrated_cards), path)

    def load_from_disk(self, source_path: Optional[str] = None) -> int:
        """Load calibrated knowledge from disk into memory."""
        path = source_path or self._persistence_path
        if not path or not os.path.exists(path):
            return 0
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            cards_dict = data.get("cards", data.get("calibrated_cards", {}))
            self._calibrated_cards.clear()
            self._question_patterns.clear()
            self._domain_knowledge.clear()

            for cdata in cards_dict.values():
                card = EvaluationCard(
                    card_id=cdata["card_id"],
                    domain=cdata["domain"],
                    question=cdata["question"],
                    expected_answer=cdata["expected_answer"],
                    key_facts=cdata.get("key_facts", []),
                    sql_provenance=cdata.get("sql_provenance", ""),
                    calibrated=True,
                )
                self.calibrate_card(card)

            logger.info("Loaded %d calibrated cards from %s", len(self._calibrated_cards), path)
            return len(self._calibrated_cards)
        except Exception as exc:
            logger.error("Failed to load calibration cache from %s: %s", path, exc)
            return 0
