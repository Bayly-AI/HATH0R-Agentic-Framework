# Dynamic MCP Tool Router & Schema Pruning Strategy

> **Status:** Ratified RFC & Architectural Specification  
> **Parent Issue:** Bayly-AI/HATH0R-Agentic-Framework#127  
> **Governing Standards:** `cr-cli-first-001`, `cr-kb-tower-001`, `cr-branch-gov-001`

---

## 1. Executive Summary

As enterprise MCP fleets scale to hundreds of microservice tools, injecting exhaustive JSON schema catalogs into LLM context windows causes severe context window bloat ("the MCP schema tax"), degraded reasoning performance, and high latency/token costs.

This strategy establishes a two-stage MCP Gateway optimization layer:
1. **Dynamic Semantic Tool Router:** Ingests large tool manifests, indexes descriptions using hybrid BM25 and dense embeddings, and routes only the top-k relevant tools for any given task or prompt.
2. **Gateway Schema Pruning Filter:** Strips redundant descriptions, deeply nested properties, and schema noise prior to prompt injection.
3. **Enterprise Identity & Token Propagation:** Securely injects caller tenant identity, user claims, and authorization tokens into downstream MCP execution calls.
4. **Token Savings Telemetry:** Measures unpruned vs pruned schema token footprints and emits observability metrics.

```mermaid
graph TD
    Prompt["Agent Intent / User Prompt"] --> Router["Dynamic Semantic Tool Router"]
    Catalog["Enterprise MCP Fleet (200+ Tools)"] -->|Hybrid Indexing| Router
    Router -->|Top-K Candidate Tools (e.g. 5)| Pruner["Gateway Schema Pruner"]
    Pruner -->|Stripped Schemas (-70% Tokens)| LLM["LLM Agent Context Window"]
    LLM -->|Selected Tool Call| Gateway["MCP Gateway"]
    Context["Caller Identity (JWT / Tenant)"] --> Gateway
    Gateway --> Downstream["Downstream MCP Server"]
```

---

## 2. Key Components

### 2.1 Dynamic Tool Router (`src/hath0r_engine/mcp/tool_router.py`)
- Ingests tool catalogs from multiple MCP servers.
- Maintains lexical (Okapi BM25) and dense semantic indices over tool names, descriptions, parameters, and tags.
- Provides `route_tools(query: str, top_k: int = 5, min_score: float = 0.1) -> List[Dict[str, Any]]`.

### 2.2 Schema Pruner (`src/hath0r_engine/mcp/schema_pruner.py`)
- Modes:
  - `AGGRESSIVE`: Keeps only parameter names, types, and required flags; strips detailed prose descriptions.
  - `STANDARD`: Truncates property descriptions to concise summaries (e.g. 80 chars max) and trims deeply nested objects.
  - `MINIMAL`: Removes auxiliary schema metadata (`$schema`, `title`, redundant comments) while keeping descriptions.
  - `NONE`: Raw unpruned schema.

### 2.3 Caller Identity (`src/hath0r_engine/mcp/identity.py`)
- Encapsulates `CallerIdentity(tenant_id, user_id, session_id, roles, scopes, auth_token)`.
- Injects authentication headers and correlation IDs into MCP dispatch payloads.

### 2.4 Routing Telemetry (`src/hath0r_engine/mcp/telemetry.py`)
- Measures token estimates (unpruned total catalog vs pruned top-k schema).
- Computes savings percentage and tracks routing latency.
