"""Semantic Prompt Caching Engine with Cosine Similarity Verification."""

from __future__ import annotations

import math
import re
import time
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from hath0r_engine.gateway.base import CompletionResponse


@dataclass
class CacheEntry:
    """Individual semantic cache entry."""

    prompt: str
    response: CompletionResponse
    vector: Dict[str, float]
    created_at: float = field(default_factory=time.time)
    hit_count: int = 0
    saved_cost_usd: float = 0.0


class SemanticCache:
    """Semantic vector cache for agentic verification and reflection loops."""

    def __init__(self, similarity_threshold: float = 0.90, ttl_seconds: float = 86400.0) -> None:
        self.similarity_threshold = similarity_threshold
        self.ttl_seconds = ttl_seconds
        self._entries: List[CacheEntry] = []
        self.total_hits: int = 0
        self.total_misses: int = 0
        self.total_saved_cost_usd: float = 0.0

    def _vectorize(self, text: str) -> Dict[str, float]:
        """Convert text into normalized term-frequency sparse vector."""
        tokens = re.findall(r"\b[a-zA-Z0-9_\-\.]{2,}\b", text.lower())
        if not tokens:
            return {}
        counts = Counter(tokens)
        norm = math.sqrt(sum(c * c for c in counts.values()))
        if norm == 0:
            return {}
        return {k: v / norm for k, v in counts.items()}

    def _cosine_similarity(self, v1: Dict[str, float], v2: Dict[str, float]) -> float:
        """Compute cosine similarity between two normalized sparse vectors."""
        if not v1 or not v2:
            return 0.0
        # Dot product
        intersection = set(v1.keys()) & set(v2.keys())
        return sum(v1[k] * v2[k] for k in intersection)

    def lookup(self, prompt: str) -> Optional[CompletionResponse]:
        """Look up matching cached completion if semantic similarity exceeds threshold."""
        now = time.time()
        # Clean expired
        self._entries = [e for e in self._entries if now - e.created_at < self.ttl_seconds]

        target_vec = self._vectorize(prompt)
        if not target_vec:
            self.total_misses += 1
            return None

        best_entry: Optional[CacheEntry] = None
        best_score = 0.0

        for entry in self._entries:
            sim = self._cosine_similarity(target_vec, entry.vector)
            if sim > best_score:
                best_score = sim
                best_entry = entry

        if best_entry and best_score >= self.similarity_threshold:
            best_entry.hit_count += 1
            best_entry.saved_cost_usd += best_entry.response.cost_usd
            self.total_hits += 1
            self.total_saved_cost_usd += best_entry.response.cost_usd

            cached_resp = CompletionResponse(
                content=best_entry.response.content,
                model_used=best_entry.response.model_used,
                provider_used=best_entry.response.provider_used,
                prompt_tokens=best_entry.response.prompt_tokens,
                completion_tokens=best_entry.response.completion_tokens,
                total_tokens=best_entry.response.total_tokens,
                cost_usd=0.0,  # Zero cost for cache hit
                latency_ms=0.5,
                cached=True,
                metadata={
                    "semantic_similarity": round(best_score, 4),
                    "original_cost_usd": best_entry.response.cost_usd,
                    "hit_count": best_entry.hit_count,
                },
            )
            return cached_resp

        self.total_misses += 1
        return None

    def store(self, prompt: str, response: CompletionResponse) -> None:
        """Store prompt-response pair in semantic cache."""
        target_vec = self._vectorize(prompt)
        if not target_vec:
            return
        entry = CacheEntry(
            prompt=prompt,
            response=response,
            vector=target_vec,
        )
        self._entries.append(entry)

    def clear(self) -> None:
        """Clear all cache entries and stats."""
        self._entries.clear()
        self.total_hits = 0
        self.total_misses = 0
        self.total_saved_cost_usd = 0.0

    def stats(self) -> Dict[str, Any]:
        """Return cache hit-rate and savings summary."""
        total_queries = self.total_hits + self.total_misses
        hit_rate = (self.total_hits / total_queries) if total_queries > 0 else 0.0
        return {
            "entry_count": len(self._entries),
            "total_hits": self.total_hits,
            "total_misses": self.total_misses,
            "hit_rate": round(hit_rate, 4),
            "total_saved_cost_usd": round(self.total_saved_cost_usd, 6),
        }
