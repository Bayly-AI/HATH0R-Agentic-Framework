# Temporal Knowledge Graphs & Memory Paging Playbook

> **Status:** Active  
> **Parent Issue:** Bayly-AI/HATH0R-Agentic-Framework#126  
> **Target Subsystem:** `src/hath0r_engine/graph`, `src/hath0r_engine/memory`

---

## 1. Overview

This playbook provides operational procedures and developer guidelines for managing temporal graph relationships, querying point-in-time states, and executing autonomous memory paging operations in Hath0r.

---

## 2. Temporal Edge Operations

### 2.1 Inserting Temporal Edges
When adding or updating relationships that evolve over time:
```python
from hath0r_engine.graph.knowledge_graph import KnowledgeEdge, KnowledgeGraph

kg = KnowledgeGraph()
kg.add_edge(
    KnowledgeEdge(
        source="user:alice",
        target="team:core-engine",
        relation="leads",
        valid_from="2026-01-01T00:00:00Z",
        valid_to="2026-06-30T23:59:59Z",
        is_current=False
    )
)
```

### 2.2 Point-in-Time Traversal
Querying neighbors or graph edges as of a specific date:
```python
# Query active leadership as of March 2026
q1_neighbors = kg.get_neighbors("user:alice", relation="leads", as_of="2026-03-15T00:00:00Z")
```

---

## 3. Autonomous Memory Paging

### 3.1 Paging Tools
Use the Letta-compatible memory primitives in `hath0r_engine.memory.memory_tools`:
```python
from hath0r_engine.memory.memory_tools import MemoryPagingManager

manager = MemoryPagingManager()
manager.core_memory_append("persona", "Specialized in distributed systems architecture.")
manager.archival_memory_insert("Migrated database schemas in sprint 44", tags=["migration", "sqlite"])
results = manager.archival_memory_search("database migration")
```
