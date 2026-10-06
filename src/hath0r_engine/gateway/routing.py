"""Tiered Complexity Routing and Provider Failover Manager."""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

from hath0r_engine.gateway.base import ComplexityTier


class TieredRouter:
    """Routes completion requests based on task complexity and manages failovers."""

    DEFAULT_TIER_MODELS: Dict[ComplexityTier, str] = {
        ComplexityTier.LIGHT: "claude-3-5-haiku",
        ComplexityTier.STANDARD: "claude-3-5-sonnet",
        ComplexityTier.REASONING: "o3-mini",
    }

    # Rates per 1M tokens (input_cost_per_1m, output_cost_per_1m)
    MODEL_PRICING_PER_1M: Dict[str, Tuple[float, float]] = {
        # Light
        "claude-3-5-haiku": (0.80, 4.00),
        "gpt-4o-mini": (0.15, 0.60),
        "gemini-1.5-flash": (0.075, 0.30),
        # Standard
        "claude-3-5-sonnet": (3.00, 15.00),
        "gpt-4o": (2.50, 10.00),
        "mistral-large": (2.00, 6.00),
        # Reasoning
        "o3-mini": (1.10, 4.40),
        "deepseek-r1": (0.55, 2.19),
        "claude-3-opus": (15.00, 75.00),
    }

    def __init__(self, custom_tier_models: Optional[Dict[ComplexityTier, str]] = None) -> None:
        self.tier_models = dict(self.DEFAULT_TIER_MODELS)
        if custom_tier_models:
            self.tier_models.update(custom_tier_models)

    def select_model(self, tier: ComplexityTier, override_model: Optional[str] = None) -> str:
        """Select cost-appropriate model based on tier or explicit override."""
        if override_model:
            return override_model
        return self.tier_models.get(tier, self.DEFAULT_TIER_MODELS[ComplexityTier.STANDARD])

    def get_fallback_chain(self, primary_model: str, configured_fallbacks: Optional[List[str]] = None) -> List[str]:
        """Construct prioritized failover sequence starting with primary model."""
        chain = [primary_model]
        fallbacks = configured_fallbacks or ["gpt-4o", "claude-3-5-sonnet", "gemini-1.5-flash", "mock-model"]
        for fb in fallbacks:
            if fb not in chain:
                chain.append(fb)
        return chain

    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate USD cost from token count and pricing rates."""
        pricing = self.MODEL_PRICING_PER_1M.get(model.lower())
        if not pricing:
            # Default fallback rate: $1.00 input, $3.00 output per 1M tokens
            pricing = (1.00, 3.00)

        in_rate, out_rate = pricing
        in_cost = (prompt_tokens / 1_000_000.0) * in_rate
        out_cost = (completion_tokens / 1_000_000.0) * out_rate
        return round(in_cost + out_cost, 6)

    def escalate_tier_from_volatility(self, volatility_score: float) -> ComplexityTier:
        """Escalate LLM reasoning tier based on code churn volatility score."""
        if volatility_score >= 0.70:
            return ComplexityTier.REASONING
        if volatility_score >= 0.30:
            return ComplexityTier.STANDARD
        return ComplexityTier.LIGHT


