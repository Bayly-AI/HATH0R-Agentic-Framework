"""Autonomous Memory Paging Tools and Letta-compatible Memory Primitives for Hath0r.

Provides core memory paging (persona / human / context sections) and archival memory
vector and keyword retrieval with temporal interval validity support.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from hath0r_engine.graph.sqlite_graph import SQLiteGraphStore
from hath0r_engine.memory.memory_graph import MemoryGraph, MemoryNode
from hath0r_engine.memory.reflection import ReflectionEngine


class MemoryPagingManager:
    """Manages Letta-compatible core and archival memory paging for agents."""

    def __init__(
        self,
        memory_graph: Optional[MemoryGraph] = None,
        sqlite_store: Optional[SQLiteGraphStore] = None,
    ) -> None:
        self.memory_graph = memory_graph or MemoryGraph(graph_id="agent-core-memory")
        self.sqlite_store = sqlite_store or SQLiteGraphStore(":memory:")
        self.reflection_engine = ReflectionEngine()
        self.core_sections: Dict[str, str] = {
            "persona": "Hath0r Autonomous Agent with Tri-Graph and MCP capabilities.",
            "human": "Operator / Engineering user.",
            "task_context": "Initialized and standing by.",
        }

    # Core Memory Tools
    def core_memory_append(self, section: str, content: str) -> str:
        """Append text content to a core memory section."""
        existing = self.core_sections.get(section, "")
        if existing:
            updated = f"{existing}\n{content.strip()}"
        else:
            updated = content.strip()
        self.core_sections[section] = updated

        # Record update in working MemoryGraph
        node_id = f"core:{section}"
        node = MemoryNode(
            id=node_id,
            type="concept",
            label=f"Core Memory: {section}",
            content=updated,
            importance=1.0,
            tags=["core_memory", section],
        )
        self.memory_graph.add_node(node)
        return updated

    def core_memory_replace(self, section: str, old_content: str, new_content: str) -> str:
        """Replace specific target text within a core memory section."""
        current = self.core_sections.get(section, "")
        if old_content not in current:
            raise ValueError(f"Target text not found in core memory section '{section}'")

        updated = current.replace(old_content, new_content)
        self.core_sections[section] = updated

        node_id = f"core:{section}"
        node = MemoryNode(
            id=node_id,
            type="concept",
            label=f"Core Memory: {section}",
            content=updated,
            importance=1.0,
            tags=["core_memory", section],
        )
        self.memory_graph.add_node(node)
        return updated

    def core_memory_get(self, section: Optional[str] = None) -> Dict[str, str] | str:
        """Retrieve full core memory or a specific section."""
        if section:
            return self.core_sections.get(section, "")
        return dict(self.core_sections)

    # Archival Memory Tools
    def archival_memory_insert(
        self,
        content: str,
        tags: Optional[List[str]] = None,
        importance: float = 0.5,
        valid_from: Optional[str] = None,
        valid_to: Optional[str] = None,
        is_current: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Store information into persistent archival memory with temporal bounds."""
        mem_id = f"archival-{uuid.uuid4().hex[:10]}"
        now = datetime.now(timezone.utc).isoformat()
        all_tags = list(tags or [])
        if "archival" not in all_tags:
            all_tags.append("archival")

        node = MemoryNode(
            id=mem_id,
            type="fact",
            label=f"Archival Memory ({', '.join(all_tags[:2])})",
            content=content,
            importance=importance,
            tags=all_tags,
            valid_from=valid_from,
            valid_to=valid_to,
            is_current=is_current,
            created_at=now,
            updated_at=now,
            metadata=metadata or {},
        )
        self.memory_graph.add_node(node)

        # Persist to SQLite store
        self.sqlite_store.upsert_node(
            node_id=mem_id,
            node_type="fact",
            title=node.label,
            graph_type="memory",
            content=content,
            importance=importance,
            tags=all_tags,
            properties=metadata or {},
        )

        return mem_id

    def archival_memory_search(
        self,
        query: str,
        top_k: int = 5,
        as_of: Optional[str] = None,
        only_current: bool = False,
    ) -> List[Dict[str, Any]]:
        """Search archival memory using hybrid ranking with temporal interval validation."""
        ranked = self.reflection_engine.rank_memories(
            self.memory_graph,
            query=query,
            top_k=top_k,
            node_types=["fact", "episode", "decision", "concept", "insight"],
            as_of=as_of,
            only_current=only_current,
        )

        results = []
        for node, score_info in ranked:
            results.append(
                {
                    "id": node.id,
                    "label": node.label,
                    "content": node.content,
                    "importance": node.importance,
                    "tags": node.tags,
                    "valid_from": node.valid_from,
                    "valid_to": node.valid_to,
                    "is_current": node.is_current,
                    "relevance_score": score_info["composite"],
                }
            )
        return results

    def memory_prune(
        self,
        max_age_days: Optional[int] = None,
        min_importance: float = 0.2,
    ) -> int:
        """Prune stale, low-importance ephemeral memories."""
        now = datetime.now(timezone.utc)
        to_prune: List[str] = []

        for nid, node in self.memory_graph.nodes.items():
            if node.type in ("concept", "rule") or "core_memory" in node.tags:
                continue

            if node.importance < min_importance:
                to_prune.append(nid)
                continue

            if max_age_days is not None:
                try:
                    c_time = datetime.fromisoformat(node.created_at.replace("Z", "+00:00"))
                    if (now - c_time).days >= max_age_days and node.importance < 0.7:
                        to_prune.append(nid)
                except Exception:
                    pass

        for nid in to_prune:
            if nid in self.memory_graph.nodes:
                del self.memory_graph.nodes[nid]
            self.sqlite_store.delete_node(nid)

        self.memory_graph.edges = [
            e for e in self.memory_graph.edges if e.source not in to_prune and e.target not in to_prune
        ]

        return len(to_prune)

    def pack_block_aligned_context(
        self,
        dynamic_turns: Optional[List[str]] = None,
        max_tokens: int = 2048,
        block_size: int = 16,
    ) -> Dict[str, Any]:
        """Pack core memory and dynamic turns on PagedAttention chunk boundaries.

        Ensures `persona` and `human` sections remain pinned in `STATIC` prefix blocks,
        `task_context` resides in `SEMI_STATIC` blocks, and `dynamic_turns` are evicted
        in exact `block_size` multiples from `DYNAMIC_TAIL` without shifting prefix hashes.
        """
        from hath0r_engine.gateway.cache import ChunkAlignedKVEvictionPolicy, KVBlockChunk, KVBlockTier

        if not hasattr(self, "_kv_eviction_policy") or self._kv_eviction_policy.block_size != block_size:
            self._kv_eviction_policy = ChunkAlignedKVEvictionPolicy(block_size=block_size)

        chunks: List[KVBlockChunk] = [
            KVBlockChunk(
                chunk_id="core:persona",
                content=self.core_sections.get("persona", ""),
                tier=KVBlockTier.STATIC,
                pinned=True,
                priority=1.0,
            ),
            KVBlockChunk(
                chunk_id="core:human",
                content=self.core_sections.get("human", ""),
                tier=KVBlockTier.STATIC,
                pinned=True,
                priority=1.0,
            ),
            KVBlockChunk(
                chunk_id="core:task_context",
                content=self.core_sections.get("task_context", ""),
                tier=KVBlockTier.SEMI_STATIC,
                pinned=False,
                priority=0.8,
            ),
        ]

        for idx, turn_text in enumerate(dynamic_turns or []):
            chunks.append(
                KVBlockChunk(
                    chunk_id=f"turn:{idx}",
                    content=turn_text,
                    tier=KVBlockTier.DYNAMIC_TAIL,
                    pinned=False,
                    priority=0.2 + (0.01 * idx),
                )
            )

        return self._kv_eviction_policy.pack_and_evict(chunks=chunks, max_tokens=max_tokens)

