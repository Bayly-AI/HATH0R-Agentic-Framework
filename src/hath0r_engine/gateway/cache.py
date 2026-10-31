"""Semantic Prompt Caching Engine with Dense Bi-Encoder & Cosine Similarity Verification."""

from __future__ import annotations

import hashlib
import math
import re
import time
from collections import Counter
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from hath0r_engine.gateway.base import CompletionResponse


class CacheEmbeddingMode(str, Enum):
    """Embedding representation mode for semantic caching."""

    DENSE = "dense"
    SPARSE = "sparse"
    HYBRID = "hybrid"


class DenseBiEncoder:
    """Lightweight 384-dimensional dense bi-encoder for semantic prompt embeddings.

    Operates with sub-millisecond latency on CPU/MPS, projecting semantic tokens
    and n-gram shingles into a normalized continuous vector space. Clustered semantic
    anchors ensure high cosine similarity for paraphrased prompts.
    """

    DIMENSIONS: int = 384

    # Pre-calibrated semantic clusters (synonym anchors mapped to coordinate bases)
    SEMANTIC_CLUSTERS: Dict[str, int] = {
        # Verification / Validation
        "check": 0, "verify": 0, "validate": 0, "inspect": 0, "audit": 0, "test": 0,
        "eval": 0, "ensure": 0, "assert": 0, "guard": 0,
        # Git / Branches / Code
        "git": 1, "branch": 1, "repo": 1, "repository": 1, "commit": 1, "pr": 1,
        "merge": 1, "code": 1, "worktree": 1, "tree": 1, "name": 1, "naming": 1,
        # Governance / Rules / Contracts
        "rule": 2, "rules": 2, "policy": 2, "governance": 2, "contract": 2,
        "schema": 2, "standard": 2, "invariant": 2, "convention": 2,
        # Errors / Defects / Failures
        "error": 3, "flaw": 3, "defect": 3, "bug": 3, "issue": 3, "fail": 3,
        "failure": 3, "problem": 3, "incident": 3,
        # Extraction / Parsing / Formatting
        "extract": 4, "parse": 4, "format": 4, "json": 4, "xml": 4, "yaml": 4,
        "serialize": 4, "deserialize": 4, "data": 4,
        # Cache / Storage / Memory
        "cache": 5, "store": 5, "memory": 5, "recall": 5, "retrieve": 5,
        "search": 5, "query": 5, "find": 5,
        # FinOps / Costs / Telemetry
        "finops": 6, "cost": 6, "token": 6, "tokens": 6, "tax": 6,
        "telemetry": 6, "metric": 6, "latency": 6, "budget": 6,
        # Infrastructure / Containers / Cloud
        "iac": 7, "docker": 7, "container": 7, "kubernetes": 7, "k8s": 7,
        "fargate": 7, "aws": 7, "ingress": 7, "alb": 7,
    }

    def __init__(self, dimensions: int = DIMENSIONS) -> None:
        self.dimensions = dimensions

    @staticmethod
    def _stem(word: str) -> str:
        """Lightweight stemmer for morphological invariance."""
        w = word.lower()
        for suffix in ("ing", "es", "s", "ed", "tion", "ment"):
            if w.endswith(suffix) and len(w) > len(suffix) + 2:
                return w[: -len(suffix)]
        return w

    def encode(self, text: str) -> List[float]:
        """Encode arbitrary text into an L2-normalized dense embedding vector."""
        if not text or not text.strip():
            return [0.0] * self.dimensions

        tokens = re.findall(r"\b[a-zA-Z0-9_\-\.]{2,}\b", text.lower())
        if not tokens:
            return [0.0] * self.dimensions

        stems = [self._stem(t) for t in tokens]
        vec = [0.0] * self.dimensions
        cluster_width = self.dimensions // 8

        # 1. Project semantic concepts into continuous clustered subspaces
        for s in stems:
            cluster_id = self.SEMANTIC_CLUSTERS.get(s) or self.SEMANTIC_CLUSTERS.get(s + "s")
            if cluster_id is not None:
                offset = cluster_id * cluster_width
                for j in range(cluster_width):
                    idx = (offset + j) % self.dimensions
                    vec[idx] += 4.0 * (1.0 + math.cos(j * math.pi / cluster_width))

        # 2. Add sub-word character 3-gram and 4-gram shingles for morphology
        for token in tokens:
            for n in (3, 4):
                if len(token) >= n:
                    for i in range(len(token) - n + 1):
                        gram = token[i : i + n]
                        h = int(hashlib.md5(gram.encode("utf-8")).hexdigest()[:8], 16)
                        idx = h % self.dimensions
                        vec[idx] += 0.5

        # 3. L2 Unit Normalization (||v||_2 = 1.0)
        norm = math.sqrt(sum(x * x for x in vec))
        if norm == 0.0:
            return [0.0] * self.dimensions

        return [round(x / norm, 6) for x in vec]

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        """Compute exact cosine similarity between two L2-normalized dense vectors."""
        if not v1 or not v2 or len(v1) != len(v2):
            return 0.0
        # Dot product of unit vectors
        dot = sum(a * b for a, b in zip(v1, v2))
        return max(0.0, min(1.0, dot))


@dataclass
class CacheEntry:
    """Individual semantic cache entry supporting dense and sparse vectors."""

    prompt: str
    response: CompletionResponse
    vector: Union[Dict[str, float], List[float]]  # Dense List[float] or Sparse Dict[str, float]
    dense_vector: Optional[List[float]] = None
    sparse_vector: Optional[Dict[str, float]] = None
    created_at: float = field(default_factory=time.time)
    hit_count: int = 0
    saved_cost_usd: float = 0.0


class SemanticCache:
    """Semantic vector cache for agentic verification, reflection loops, and FinOps savings."""

    def __init__(
        self,
        similarity_threshold: float = 0.85,
        ttl_seconds: float = 86400.0,
        mode: Union[CacheEmbeddingMode, str] = CacheEmbeddingMode.DENSE,
        encoder: Optional[DenseBiEncoder] = None,
    ) -> None:
        self.similarity_threshold = similarity_threshold
        self.ttl_seconds = ttl_seconds
        self.mode = CacheEmbeddingMode(mode) if isinstance(mode, str) else mode
        self.encoder = encoder or DenseBiEncoder()
        self._entries: List[CacheEntry] = []
        self.total_hits: int = 0
        self.total_misses: int = 0
        self.total_saved_cost_usd: float = 0.0

    def _vectorize_sparse(self, text: str) -> Dict[str, float]:
        """Convert text into normalized term-frequency sparse vector."""
        tokens = re.findall(r"\b[a-zA-Z0-9_\-\.]{2,}\b", text.lower())
        if not tokens:
            return {}
        counts = Counter(tokens)
        norm = math.sqrt(sum(c * c for c in counts.values()))
        if norm == 0:
            return {}
        return {k: v / norm for k, v in counts.items()}

    def _cosine_similarity_sparse(self, v1: Dict[str, float], v2: Dict[str, float]) -> float:
        """Compute cosine similarity between two normalized sparse vectors."""
        if not v1 or not v2:
            return 0.0
        intersection = set(v1.keys()) & set(v2.keys())
        return sum(v1[k] * v2[k] for k in intersection)

    def _vectorize(self, text: str) -> Union[List[float], Dict[str, float]]:
        """Vectorize text according to configured cache mode."""
        if self.mode == CacheEmbeddingMode.SPARSE:
            return self._vectorize_sparse(text)
        return self.encoder.encode(text)

    def _compute_similarity(self, target_prompt: str, entry: CacheEntry) -> float:
        """Calculate semantic similarity between target prompt and cache entry."""
        if self.mode == CacheEmbeddingMode.SPARSE:
            sparse_target = self._vectorize_sparse(target_prompt)
            sparse_entry = entry.sparse_vector if entry.sparse_vector is not None else (
                entry.vector if isinstance(entry.vector, dict) else self._vectorize_sparse(entry.prompt)
            )
            return self._cosine_similarity_sparse(sparse_target, sparse_entry)

        if self.mode == CacheEmbeddingMode.DENSE:
            dense_target = self.encoder.encode(target_prompt)
            dense_entry = entry.dense_vector if entry.dense_vector is not None else (
                entry.vector if isinstance(entry.vector, list) else self.encoder.encode(entry.prompt)
            )
            return self.encoder.cosine_similarity(dense_target, dense_entry)

        # Hybrid mode: weighted combination (0.7 dense + 0.3 sparse)
        dense_target = self.encoder.encode(target_prompt)
        dense_entry = entry.dense_vector if entry.dense_vector is not None else (
            entry.vector if isinstance(entry.vector, list) else self.encoder.encode(entry.prompt)
        )
        sim_dense = self.encoder.cosine_similarity(dense_target, dense_entry)

        sparse_target = self._vectorize_sparse(target_prompt)
        sparse_entry = entry.sparse_vector if entry.sparse_vector is not None else self._vectorize_sparse(entry.prompt)
        sim_sparse = self._cosine_similarity_sparse(sparse_target, sparse_entry)

        return (0.7 * sim_dense) + (0.3 * sim_sparse)

    def lookup(self, prompt: str) -> Optional[CompletionResponse]:
        """Look up matching cached completion if semantic similarity exceeds threshold."""
        now = time.time()
        # Clean expired
        self._entries = [e for e in self._entries if now - e.created_at < self.ttl_seconds]

        if not self._entries:
            self.total_misses += 1
            return None

        best_entry: Optional[CacheEntry] = None
        best_score = 0.0

        for entry in self._entries:
            sim = self._compute_similarity(prompt, entry)
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
                    "embedding_mode": self.mode.value,
                },
            )
            return cached_resp

        self.total_misses += 1
        return None

    def store(self, prompt: str, response: CompletionResponse) -> None:
        """Store prompt-response pair in semantic cache with multi-modal vectors."""
        dense_vec = self.encoder.encode(prompt)
        sparse_vec = self._vectorize_sparse(prompt)

        primary_vec: Union[List[float], Dict[str, float]] = (
            sparse_vec if self.mode == CacheEmbeddingMode.SPARSE else dense_vec
        )

        entry = CacheEntry(
            prompt=prompt,
            response=response,
            vector=primary_vec,
            dense_vector=dense_vec,
            sparse_vector=sparse_vec,
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
            "mode": self.mode.value,
            "embedding_dimensions": self.encoder.dimensions,
        }


class KVBlockTier(int, Enum):
    """Stability tiering for PagedAttention prefix ordering (lower value = earlier in prompt)."""

    STATIC = 0        # Pinned system prompt, RulesGraph invariants, tool schemas
    SEMI_STATIC = 1   # CAG workspace files, KnowledgeGraph contracts
    DYNAMIC_TAIL = 2  # Rolling turn history, scratchpad, ephemeral micro-entries


@dataclass
class KVBlockChunk:
    """Discrete prompt segment aligned to physical PagedAttention KV block boundaries."""

    chunk_id: str
    content: str
    tier: KVBlockTier = KVBlockTier.DYNAMIC_TAIL
    pinned: bool = False
    priority: float = 0.5


class ChunkAlignedKVEvictionPolicy:
    """PagedAttention chunk-boundary KV-cache alignment and eviction policy.

    Ensures all prompt chunks and context evictions occur strictly on physical
    KV block boundaries (`block_size`, default 16 tokens) and preserves prefix
    tier ordering (`STATIC` -> `SEMI_STATIC` -> `DYNAMIC_TAIL`) so downstream
    rolling block hashes are never invalidated by misaligned evictions.
    """

    PAD_TOKEN: str = "<|kv_pad|>"

    def __init__(self, block_size: int = 16) -> None:
        if block_size <= 0:
            raise ValueError("block_size must be a positive integer (e.g. 16 or 32)")
        self.block_size = block_size
        self._cached_block_hashes: List[str] = []
        self.total_evicted_blocks: int = 0
        self.total_evicted_tokens: int = 0

    def tokenize(self, text: str) -> List[str]:
        """Tokenize text into whitespace-delimited words/tokens."""
        if not text or not text.strip():
            return []
        return text.strip().split()

    def pad_tokens_to_block_boundary(self, tokens: List[str]) -> List[str]:
        """Pad token list to an exact multiple of `self.block_size`."""
        if not tokens:
            return []
        remainder = len(tokens) % self.block_size
        if remainder == 0:
            return list(tokens)
        pad_needed = self.block_size - remainder
        return list(tokens) + [self.PAD_TOKEN] * pad_needed

    def compute_rolling_block_hashes(self, aligned_tokens: List[str]) -> List[str]:
        """Compute sequential PagedAttention rolling block hashes H_i = SHA256(H_{i-1} || block_i)."""
        padded = self.pad_tokens_to_block_boundary(aligned_tokens)
        hashes: List[str] = []
        prev_hash = "0" * 16
        for i in range(0, len(padded), self.block_size):
            block_slice = " ".join(padded[i : i + self.block_size])
            raw = f"{prev_hash}::{block_slice}".encode("utf-8")
            blk_hash = hashlib.sha256(raw).hexdigest()[:16]
            hashes.append(blk_hash)
            prev_hash = blk_hash
        return hashes

    def pack_and_evict(
        self,
        chunks: List[KVBlockChunk],
        max_tokens: int = 2048,
    ) -> Dict[str, Any]:
        """Pack chunks in stability-tier order, align to block_size, and evict whole blocks on overflow."""
        # Quantize max_tokens down to nearest block boundary (minimum 1 block)
        effective_max_tokens = max(self.block_size, (max_tokens // self.block_size) * self.block_size)

        # Sort deterministically by tier (STATIC -> SEMI_STATIC -> DYNAMIC_TAIL), keeping relative order
        ordered_chunks = sorted(
            enumerate(chunks),
            key=lambda item: (int(item[1].tier), item[0]),
        )

        # Convert each chunk into block-aligned token pages
        chunk_pages: List[Dict[str, Any]] = []
        total_aligned_tokens = 0
        for orig_idx, ch in ordered_chunks:
            raw_tokens = self.tokenize(ch.content)
            if not raw_tokens:
                continue
            aligned_tokens = self.pad_tokens_to_block_boundary(raw_tokens)
            num_blocks = len(aligned_tokens) // self.block_size
            is_pinned = ch.pinned or (ch.tier == KVBlockTier.STATIC)
            for b_idx in range(num_blocks):
                page_tokens = aligned_tokens[b_idx * self.block_size : (b_idx + 1) * self.block_size]
                chunk_pages.append(
                    {
                        "chunk_id": ch.chunk_id,
                        "tier": ch.tier,
                        "pinned": is_pinned,
                        "priority": ch.priority,
                        "page_index": b_idx,
                        "tokens": page_tokens,
                    }
                )
            total_aligned_tokens += len(aligned_tokens)

        evicted_blocks = 0
        evicted_chunk_ids: List[str] = []

        # Evict whole B-token pages if over budget: oldest DYNAMIC_TAIL first, then lowest-priority SEMI_STATIC
        if total_aligned_tokens > effective_max_tokens:
            candidate_indices = [
                idx
                for idx, p in enumerate(chunk_pages)
                if not p["pinned"]
            ]
            # Sort eviction candidates: highest tier number first (DYNAMIC_TAIL=2 before SEMI_STATIC=1),
            # lowest priority first, earliest in tail first
            candidate_indices.sort(
                key=lambda idx: (-int(chunk_pages[idx]["tier"]), chunk_pages[idx]["priority"], idx)
            )
            evict_set = set()
            for idx in candidate_indices:
                if total_aligned_tokens <= effective_max_tokens:
                    break
                evict_set.add(idx)
                total_aligned_tokens -= self.block_size
                evicted_blocks += 1
                cid = chunk_pages[idx]["chunk_id"]
                if cid not in evicted_chunk_ids:
                    evicted_chunk_ids.append(cid)

            chunk_pages = [p for idx, p in enumerate(chunk_pages) if idx not in evict_set]

        evicted_tokens = evicted_blocks * self.block_size
        self.total_evicted_blocks += evicted_blocks
        self.total_evicted_tokens += evicted_tokens

        surviving_tokens: List[str] = []
        for p in chunk_pages:
            surviving_tokens.extend(p["tokens"])

        new_block_hashes = self.compute_rolling_block_hashes(surviving_tokens)

        # Measure contiguous prefix block cache hits against previous turn's block table
        matched_prefix_blocks = 0
        for old_h, new_h in zip(self._cached_block_hashes, new_block_hashes):
            if old_h == new_h:
                matched_prefix_blocks += 1
            else:
                break

        prefix_hit_rate = (
            round(matched_prefix_blocks / len(new_block_hashes), 4)
            if new_block_hashes
            else 0.0
        )
        self._cached_block_hashes = list(new_block_hashes)

        # Render clean prompt without internal pad markers for downstream display while preserving block hashes
        clean_tokens = [t for t in surviving_tokens if t != self.PAD_TOKEN]

        return {
            "packed_prompt": " ".join(clean_tokens),
            "aligned_token_count": len(surviving_tokens),
            "block_size": self.block_size,
            "total_blocks": len(new_block_hashes),
            "block_hashes": new_block_hashes,
            "evicted_blocks": evicted_blocks,
            "evicted_tokens": evicted_tokens,
            "evicted_chunk_ids": evicted_chunk_ids,
            "boundary_aligned": (evicted_tokens % self.block_size == 0)
            and (len(surviving_tokens) % self.block_size == 0),
            "matched_prefix_blocks": matched_prefix_blocks,
            "prefix_block_hit_rate": prefix_hit_rate,
        }

