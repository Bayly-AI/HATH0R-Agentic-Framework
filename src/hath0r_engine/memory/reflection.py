"""Autonomous Episodic Reflection & Memory Synthesis Engine for Hath0r.

Provides memory decay ranking, associative recall scoring, and episodic memory
consolidation into high-order conceptual insight nodes.
"""

from __future__ import annotations

import math
from collections import Counter
from datetime import datetime, timezone
from typing import Dict, List, Optional, Sequence, Tuple

from hath0r_engine.graph.knowledge_graph import BM25Index, KnowledgeGraph, KnowledgeNode
from hath0r_engine.memory.memory_graph import MemoryEdge, MemoryGraph, MemoryNode


def _parse_iso(timestamp_str: str) -> datetime:
    """Parse ISO timestamp with fallback to current time."""
    try:
        if timestamp_str.endswith("Z"):
            timestamp_str = timestamp_str[:-1] + "+00:00"
        return datetime.fromisoformat(timestamp_str)
    except Exception:
        return datetime.now(timezone.utc)


class ReflectionEngine:
    """Manages memory retrieval weighting, decay curves, and reflection synthesis."""

    def __init__(
        self,
        decay_rate_per_hour: float = 0.05,
        weight_recency: float = 0.3,
        weight_importance: float = 0.3,
        weight_similarity: float = 0.4,
    ) -> None:
        self.decay_rate_per_hour = decay_rate_per_hour
        self.w_recency = weight_recency
        self.w_importance = weight_importance
        self.w_similarity = weight_similarity

    def score_recency(self, created_at: str, reference_time: Optional[datetime] = None) -> float:
        """Calculate exponential recency decay score in range [0.0, 1.0]."""
        ref = reference_time or datetime.now(timezone.utc)
        node_time = _parse_iso(created_at)
        if node_time.tzinfo is None:
            node_time = node_time.replace(tzinfo=timezone.utc)
        if ref.tzinfo is None:
            ref = ref.replace(tzinfo=timezone.utc)

        delta_hours = max(0.0, (ref - node_time).total_seconds() / 3600.0)
        return float(math.exp(-self.decay_rate_per_hour * delta_hours))

    def score_relevance(
        self,
        node: MemoryNode,
        query: str = "",
        reference_time: Optional[datetime] = None,
        as_of: Optional[str] = None,
        only_current: bool = False,
    ) -> Dict[str, float]:
        """Compute composite retrieval relevance score for a memory node with temporal filtering."""
        if not node.is_valid_at(as_of=as_of, only_current=only_current):
            return {"composite": 0.0, "recency": 0.0, "importance": 0.0, "similarity": 0.0}

        recency = self.score_recency(node.created_at, reference_time=reference_time)
        importance = max(0.0, min(1.0, float(node.importance)))

        similarity = 0.0
        if query:
            q_tokens = set(BM25Index.tokenize(query))
            n_tokens = set(BM25Index.tokenize(f"{node.label} {node.content} {' '.join(node.tags)}"))
            if q_tokens and n_tokens:
                overlap = len(q_tokens.intersection(n_tokens))
                similarity = float(overlap / len(q_tokens))
        else:
            similarity = 1.0

        composite = self.w_recency * recency + self.w_importance * importance + self.w_similarity * similarity

        return {
            "composite": round(composite, 4),
            "recency": round(recency, 4),
            "importance": round(importance, 4),
            "similarity": round(similarity, 4),
        }

    def rank_memories(
        self,
        memory_graph: MemoryGraph,
        query: str = "",
        top_k: int = 10,
        node_types: Optional[Sequence[str]] = None,
        as_of: Optional[str] = None,
        only_current: bool = False,
    ) -> List[Tuple[MemoryNode, Dict[str, float]]]:
        """Rank memory nodes by composite relevance score with temporal filtering."""
        allowed_types = set(node_types) if node_types else None
        scored: List[Tuple[MemoryNode, Dict[str, float]]] = []

        for node in memory_graph.nodes.values():
            if allowed_types and node.type not in allowed_types:
                continue
            if not node.is_valid_at(as_of=as_of, only_current=only_current):
                continue
            scores = self.score_relevance(node, query=query, as_of=as_of, only_current=only_current)
            if scores["composite"] > 0.0:
                scored.append((node, scores))

        scored.sort(key=lambda x: x[1]["composite"], reverse=True)
        return scored[:top_k]

    def consolidate_sleep_cycle(
        self,
        memory_graph: MemoryGraph,
        cluster_threshold: int = 2,
        max_insights: int = 5,
        prune_below_importance: float = 0.1,
    ) -> Dict[str, Any]:
        """Execute autonomous sleep-cycle memory consolidation.

        Clusters episodic memories into insights, links them via relational edges,
        and prunes stale low-importance ephemeral nodes.
        """
        new_insights = self.synthesize_reflections(
            memory_graph, cluster_threshold=cluster_threshold, max_insights=max_insights
        )

        # Prune very low importance ephemeral nodes
        pruned_ids = []
        for nid, node in list(memory_graph.nodes.items()):
            if node.type in ("episode", "topic") and node.importance < prune_below_importance:
                del memory_graph.nodes[nid]
                memory_graph.edges = [e for e in memory_graph.edges if e.source != nid and e.target != nid]
                pruned_ids.append(nid)

        return {
            "insights_generated": len(new_insights),
            "insights": [n.to_dict() for n in new_insights],
            "pruned_nodes_count": len(pruned_ids),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def synthesize_reflections(
        self,
        memory_graph: MemoryGraph,
        cluster_threshold: int = 2,
        max_insights: int = 5,
    ) -> List[MemoryNode]:
        """Analyze recent episodic memories and generate high-level insight nodes.

        Clusters related episodes by shared tags and semantic themes, creates synthesized
        insight nodes, links them via DERIVES_FROM edges, and adds them to the memory graph.
        """
        episodes = [n for n in memory_graph.nodes.values() if n.type in ("episode", "decision", "fact")]
        if not episodes:
            return []

        # Tag-based and keyword clustering
        tag_clusters: Dict[str, List[MemoryNode]] = {}
        for ep in episodes:
            for tag in ep.tags:
                tag_clusters.setdefault(tag, []).append(ep)

        new_insights: List[MemoryNode] = []
        now = datetime.now(timezone.utc).isoformat()

        for tag, cluster in tag_clusters.items():
            if len(cluster) < cluster_threshold:
                continue

            insight_id = f"insight:{tag}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
            # Check if an insight for this tag cluster already exists
            existing = [n for n in memory_graph.nodes.values() if n.type == "insight" and tag in n.tags]
            if len(existing) >= 2:
                continue

            # Summarize content and extract high frequency terms
            all_text = " ".join([f"{n.label}: {n.content}" for n in cluster])
            tokens = [t for t in BM25Index.tokenize(all_text) if len(t) > 3]
            top_terms = [word for word, _ in Counter(tokens).most_common(4)]

            insight_label = f"Synthesized Insight on {tag.capitalize()}"
            insight_content = (
                f"Consolidated from {len(cluster)} episodes/decisions regarding '{tag}'. "
                f"Key recurring patterns: {', '.join(top_terms)}. "
                f"Summary: {cluster[0].content[:150]}"
            )

            # Insight importance is the aggregate max of its constituent memories
            avg_importance = sum(n.importance for n in cluster) / len(cluster)
            insight_importance = min(1.0, round(avg_importance + 0.2, 2))

            insight_node = MemoryNode(
                id=insight_id,
                type="insight",
                label=insight_label,
                content=insight_content,
                importance=insight_importance,
                tags=[tag, "reflection", "synthesized"],
                created_at=now,
                updated_at=now,
                metadata={"constituent_count": len(cluster), "source_tag": tag},
            )

            memory_graph.add_node(insight_node)
            for src_node in cluster:
                try:
                    memory_graph.add_edge(
                        MemoryEdge(
                            source=insight_id,
                            target=src_node.id,
                            relation="DERIVES_FROM",
                            weight=1.0,
                        )
                    )
                except Exception:
                    pass

            new_insights.append(insight_node)
            if len(new_insights) >= max_insights:
                break

        return new_insights

    def promote_to_knowledge(
        self,
        memory_graph: MemoryGraph,
        knowledge_graph: KnowledgeGraph,
        min_importance: float = 0.7,
    ) -> List[KnowledgeNode]:
        """Promote high-importance synthesized insights to canonical KnowledgeGraph nodes."""
        promoted: List[KnowledgeNode] = []
        insights = [
            n
            for n in memory_graph.nodes.values()
            if n.type in ("insight", "rule", "decision") and n.importance >= min_importance
        ]

        for mem in insights:
            k_id = f"promoted:{mem.id}"
            if k_id in knowledge_graph.nodes:
                continue

            k_node = KnowledgeNode(
                id=k_id,
                type="concept" if mem.type == "insight" else "policy",
                title=mem.label,
                path=f"memory/promoted/{mem.id}.md",
                subsystem="memory",
                content=mem.content,
                properties={
                    "source_memory_id": mem.id,
                    "importance": mem.importance,
                    "tags": mem.tags,
                },
            )
            knowledge_graph.add_node(k_node)
            promoted.append(k_node)

        return promoted
