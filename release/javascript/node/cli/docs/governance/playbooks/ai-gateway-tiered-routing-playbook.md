# Multi-Provider AI Gateway Playbook

> **Status:** Active  
> **Parent Issue:** Bayly-AI/HATH0R-Agentic-Framework#130  
> **Target Subsystem:** `src/hath0r_engine/gateway`

---

## 1. Overview

This playbook provides practical guides and configuration recipes for executing model completions through the Hath0r AI Gateway with tiered routing, multi-provider failover, and semantic caching.

---

## 2. Usage Examples

### 2.1 Basic Completion with Tiered Routing

```python
from hath0r_engine.gateway import (
    AIGatewayClient,
    GatewayConfig,
    ComplexityTier,
    CompletionRequest,
    ModelProvider,
)

gateway = AIGatewayClient(
    config=GatewayConfig(
        gateway_type=ModelProvider.LITELLM,
        endpoint_url="http://localhost:4000/v1",
        api_key="sk-litellm-proxy-key",
        semantic_cache_enabled=True,
    )
)

# Request a light, cheap completion for JSON extraction
resp = gateway.complete(
    CompletionRequest(
        prompt="Extract the JSON object from the following logs: ...",
        tier=ComplexityTier.LIGHT,
        temperature=0.0,
    )
)

print(f"Content: {resp.content}")
print(f"Model used: {resp.model_used}")
print(f"Cost USD: ${resp.cost_usd:.6f}")
print(f"Cached: {resp.cached}")
```

### 2.2 Semantic Cache Hit

```python
# Similar prompt will hit semantic cache directly:
resp_cached = gateway.complete(
    CompletionRequest(
        prompt="Extract the JSON object from these logs: ...",
        tier=ComplexityTier.LIGHT,
    )
)
assert resp_cached.cached is True
assert resp_cached.cost_usd == 0.0
```
