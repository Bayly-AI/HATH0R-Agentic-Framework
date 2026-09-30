# Temporal Knowledge Graphs & Hybrid Tri-Graph Strategy

> **Status:** Ratified RFC & Architectural Specification  
> **Parent Issue:** Bayly-AI/HATH0R-Agentic-Framework#126  
> **Governing Standards:** `cr-cli-first-001`, `cr-kb-tower-001`, `cr-branch-gov-001`

---

## 1. Executive Summary

This strategy specifies the enhancement of Hath0r's Tri-Graph Engine (KnowledgeGraph, MemoryGraph, and ContextGraph) with:
1. **Temporal Edge & Node Validity Intervals:** Tracking facts, relationships, and state shifts across time with `valid_from`, `valid_to`, and `is_current` properties.
2. **Hybrid BM25 + Dense kNN Vector Search:** Unifying lexical FTS5 retrieval with dense vector cosine similarity for low-latency context queries and point-in-time snapshot reconstruction.
3. **Autonomous Memory Paging & Sleep Consolidation:** Implementing Letta-compatible memory primitives (`core_memory_append`, `core_memory_replace`, `archival_memory_insert`, `archival_memory_search`, `memory_prune`) alongside sleep-cycle consolidation routines.

---

## 2. Temporal Validity Interval Architecture

Every relational edge and memory node supports bitemporal validity tracking:
- `valid_from`: ISO 8601 timestamp representing when the relationship/fact became effective.
- `valid_to`: ISO 8601 timestamp when the relationship/fact was superseded or invalidated (null if currently active).
- `is_current`: Boolean flag indicating whether the relationship is active in the current state.

```mermaid
graph LR
    Alice["Node: User Alice"] -->|ROLE: Tech Lead (valid_from: 2026-01-01, valid_to: 2026-06-30, is_current: false)| Project["Node: Hath0r Framework"]
    Alice -->|ROLE: Principal Architect (valid_from: 2026-07-01, valid_to: null, is_current: true)| Project
```

---

## 3. Autonomous Memory Paging Primitives

1. **Core Memory Management:**
   - `core_memory_append(section, content)`: Append crucial agent persona or workspace context.
   - `core_memory_replace(section, old_content, new_content)`: Safely update existing core memory sections.
2. **Archival Memory Store:**
   - `archival_memory_insert(content, tags, importance)`: Vector & keyword indexed persistent memory.
   - `archival_memory_search(query, top_k, as_of)`: Point-in-time hybrid recall.
3. **Consolidation & Sleep Cycles:**
   - `consolidate_sleep_cycle()`: Background synthesis clustering episodic nodes into high-order conceptual insights.
