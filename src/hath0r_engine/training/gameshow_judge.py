"""Evaluation judge for Gameshow benchmark tournaments.

Evaluates candidate agent responses against ground-truth answers, key facts,
directional contradiction rules, and entity guardrail constraints.
"""

from __future__ import annotations

import re
from typing import Callable, List, Optional, Tuple

from hath0r_engine.training.gameshow_models import EvaluationCard


class GameshowJudge:
    """Evaluates agent responses against card ground truth and required key facts."""

    def __init__(
        self,
        custom_rules: Optional[List[Callable[[EvaluationCard, str], Optional[Tuple[bool, float, str]]]]] = None,
    ) -> None:
        self.custom_rules = custom_rules or []

    @staticmethod
    def strip_html(html_text: str) -> str:
        """Strip HTML tags and normalize spacing."""
        text = re.sub(r"<[^>]+>", " ", html_text)
        return " ".join(text.split()).strip()

    def evaluate(
        self,
        card: EvaluationCard,
        agent_response: str,
    ) -> Tuple[bool, float, str]:
        """Judge an agent response against card ground truth.

        Returns: (is_correct, score 0.0-1.0, reason_explanation)
        """
        if not agent_response or len(agent_response.strip()) < 10:
            return False, 0.0, "Empty or truncated agent response"

        clean_resp = self.strip_html(agent_response).lower()
        clean_resp_norm = " ".join(re.sub(r"[^\w\s]", " ", clean_resp).split())

        # Check for obvious error signals
        if "unable to process" in clean_resp or "encountered an error" in clean_resp:
            return False, 0.0, "Agent returned error message"

        # Execute custom user/domain rules first
        for rule_fn in self.custom_rules:
            res = rule_fn(card, clean_resp)
            if res is not None:
                return res

        key_facts = card.key_facts or []
        if not key_facts:
            # Fall back to token overlap with expected answer
            clean_expected = card.expected_answer.lower()
            exp_tokens = [w for w in re.sub(r"[^\w\s]", " ", clean_expected).split() if len(w) > 3]
            if not exp_tokens:
                return True, 1.0, "Accepted (no strict key facts)"
            overlap = sum(1 for w in exp_tokens if w in clean_resp)
            ratio = overlap / len(exp_tokens)
            return (ratio >= 0.50), ratio, f"Token overlap: {overlap}/{len(exp_tokens)}"

        # Check if full expected answer is incorporated (e.g., from CAG memory recall)
        clean_exp_norm = " ".join(re.sub(r"[^\w\s]", " ", card.expected_answer.lower()).split())
        if clean_exp_norm in clean_resp_norm:
            return True, 1.0, f"Passed: Complete verified answer confirmed ({len(key_facts)}/{len(key_facts)} facts)"

        matched_facts = 0
        missing_facts = []

        for fact in key_facts:
            fact_clean = fact.lower().strip()
            fact_norm = " ".join(re.sub(r"[^\w\s]", " ", fact_clean).split())

            # 1. Exact or normalized phrase match
            if fact_clean in clean_resp or fact_norm in clean_resp_norm:
                matched_facts += 1
                continue

            # 2. Number or percentage match (e.g., '98.6%' vs '98.57%')
            pct_match = re.search(r"(\d+(?:\.\d+)?)%", fact_clean)
            if pct_match:
                num_val = float(pct_match.group(1))
                if (
                    f"{num_val:.1f}%" in clean_resp
                    or f"{int(num_val)}%" in clean_resp
                    or f"{num_val}" in clean_resp
                ):
                    matched_facts += 1
                    continue

            # 3. Entity token match for multi-word phrases
            words = [
                w for w in fact_norm.split()
                if len(w) >= 2 and w not in {"the", "and", "rep", "sen", "for", "act", "of", "in", "to", "is"}
            ]
            if len(words) >= 2:
                w_matches = sum(1 for w in words if w in clean_resp_norm.split())
                if w_matches / len(words) >= 0.60:
                    matched_facts += 1
                    continue
            elif len(words) == 1:
                if words[0] in clean_resp_norm.split():
                    matched_facts += 1
                    continue

            missing_facts.append(fact)

        score = matched_facts / len(key_facts)

        # Directional contradiction checks
        exp_lower = card.expected_answer.lower()
        if "yea" in exp_lower and "nay" in clean_resp and "yea" not in clean_resp:
            return False, 0.2, "Direction contradiction (expected Yea, found Nay)"
        if "nay" in exp_lower and "yea" in clean_resp and "nay" not in clean_resp:
            return False, 0.2, "Direction contradiction (expected Nay, found Yea)"

        # Passing threshold: all facts matched, or at least 65% of facts matched
        is_pass = (matched_facts == len(key_facts)) or (len(key_facts) >= 2 and score >= 0.65)

        if is_pass:
            return True, score, f"Passed: {matched_facts}/{len(key_facts)} key facts confirmed"
        return False, score, f"Missing key facts: {', '.join(missing_facts)}"
