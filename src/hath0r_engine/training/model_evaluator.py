"""Candidate Model Evaluator and Benchmark Harness for Continuous Training."""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence


@dataclass
class CandidateModelEvaluator:
    """Evaluates candidate trained models against golden datasets, baseline models, and Taguchi loss functions."""

    w_accuracy: float = 0.50
    w_finops: float = 0.25
    w_latency: float = 0.15
    w_constraint: float = 0.10
    token_budget: int = 2048
    target_latency_ms: float = 120.0
    epsilon_improvement: float = 0.02

    def calculate_reward(
        self,
        accuracy: float,
        tokens_used: int,
        latency_ms: float,
        constraint_violated: bool = False,
    ) -> Dict[str, Any]:
        """Compute multi-objective reward R = w1*R_acc + w2*R_finops - w3*R_lat - w4*R_constraint."""
        r_acc = max(0.0, min(1.0, accuracy))
        r_finops = max(0.0, 1.0 - (tokens_used / self.token_budget))
        r_lat = min(1.0, latency_ms / self.target_latency_ms)
        r_constraint = 1.0 if constraint_violated else 0.0

        total_reward = (
            self.w_accuracy * r_acc
            + self.w_finops * r_finops
            - self.w_latency * r_lat
            - self.w_constraint * r_constraint
        )

        return {
            "total_reward": round(total_reward, 4),
            "components": {
                "r_accuracy": round(r_acc, 4),
                "r_finops": round(r_finops, 4),
                "r_latency_penalty": round(r_lat, 4),
                "r_constraint_penalty": round(r_constraint, 4),
            },
        }

    def evaluate_benchmark(
        self,
        candidate_results: Sequence[Dict[str, Any]],
        baseline_results: Optional[Sequence[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Run benchmark evaluation and compare candidate model against baseline."""
        cand_rewards: List[float] = []
        latencies: List[float] = []

        for item in candidate_results:
            reward = self.calculate_reward(
                accuracy=item.get("accuracy", 0.85),
                tokens_used=item.get("tokens_used", 1000),
                latency_ms=item.get("latency_ms", 80.0),
                constraint_violated=item.get("constraint_violated", False),
            )
            cand_rewards.append(reward["total_reward"])
            latencies.append(item.get("latency_ms", 80.0))

        mean_cand_reward = sum(cand_rewards) / len(cand_rewards) if cand_rewards else 0.0

        # Calculate Signal-to-Noise Ratio (SNR) for latency (smaller is better)
        msd = sum(lat ** 2 for lat in latencies) / len(latencies) if latencies else 1.0
        snr_db = -10.0 * math.log10(msd) if msd > 0 else 0.0

        # Quality Loss Function L = k * (y - m)^2
        k = 0.01
        quality_loss = k * sum((lat - self.target_latency_ms) ** 2 for lat in latencies) / len(latencies) if latencies else 0.0

        result: Dict[str, Any] = {
            "candidate_mean_reward": round(mean_cand_reward, 4),
            "snr_db": round(snr_db, 2),
            "quality_loss": round(quality_loss, 4),
            "samples_evaluated": len(candidate_results),
            "promotable": True,
        }

        if baseline_results:
            base_rewards = [
                self.calculate_reward(
                    accuracy=item.get("accuracy", 0.75),
                    tokens_used=item.get("tokens_used", 1400),
                    latency_ms=item.get("latency_ms", 110.0),
                    constraint_violated=item.get("constraint_violated", False),
                )["total_reward"]
                for item in baseline_results
            ]
            mean_base_reward = sum(base_rewards) / len(base_rewards) if base_rewards else 0.0
            improvement = mean_cand_reward - mean_base_reward
            promotable = improvement >= self.epsilon_improvement

            result["baseline_mean_reward"] = round(mean_base_reward, 4)
            result["improvement"] = round(improvement, 4)
            result["promotable"] = promotable
            result["promotion_verdict"] = (
                f"Candidate improves by {improvement:+.4f} (>= {self.epsilon_improvement} threshold). PASS."
                if promotable
                else f"Candidate fails improvement gate ({improvement:+.4f} < {self.epsilon_improvement}). REJECT."
            )

        return result
