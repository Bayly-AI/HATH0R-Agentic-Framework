# Quad-Graph Substrate Architecture

Hath0r utilizes a unified four-plane graph substrate to model enterprise reality, eliminate prompt tax, and enable temporal memory compounding.

```text
┌─────────────────────────────────────────────────────────────┐
│                   Hath0r Quad-Graph Substrate               │
├──────────────────────────────┬──────────────────────────────┤
│ 1. KnowledgeGraph            │ 2. ContextGraph              │
│    Static architecture       │    Dynamic session state     │
│    Contracts & Schemas       │    Active subagent dispatches│
│    System specifications     │    Span lineages             │
├──────────────────────────────┼──────────────────────────────┤
│ 3. MemoryGraph               │ 4. RulesGraph                │
│    Temporal entity nodes     │    Deterministic rule DAG    │
│    Letta-style memory paging │    Role RBAC router          │
│    Consolidated reflections  │    Tool pruning filters      │
└──────────────────────────────┴──────────────────────────────┘
```

### 1. KnowledgeGraph (`lib.graph` / `contracts/` / `docs/`)
Represents immutable structural knowledge, JSON schemas, protocol definitions, and engineering specifications. Evaluated statically or via contract validators.

### 2. ContextGraph (`lib.context` / `hath0r context`)
Maintains dynamic ephemeral state: running subagents, active tool executions, intermediate results, and causal span lineages across conversational turns.

### 3. MemoryGraph (`hath0r_engine.memory` / `hath0r memory`)
Stores persistent long-term memories across task boundaries in `.hath0r/memory/graph.json`. Utilizes Letta-compatible memory paging (`MemoryPagingManager`) and reflection synthesis.

### 4. RulesGraph (`hath0r_engine.graph` / `hath0r agentgraph`)
Represents an acyclic rule hierarchy: $\text{Org Invariant} \succ \text{Repo Standard} \succ \text{Subsystem} \succ \text{Role}$. Used by `hath0r agentgraph route` to deterministically prune unauthorized tools before LLM dispatch.
