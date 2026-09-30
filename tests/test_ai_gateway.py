"""Unit tests for Multi-Provider AI Gateway, Tiered Routing, and Semantic Caching."""

import pytest

from hath0r_engine.gateway import (
    AIGatewayClient,
    CompletionRequest,
    CompletionResponse,
    ComplexityTier,
    GatewayConfig,
    ModelProvider,
    SemanticCache,
    TieredRouter,
)
from hath0r_engine.telemetry.otel_tracer import OTELTracerBot


def test_gateway_config_and_headers():
    # Portkey headers
    pk_config = GatewayConfig(
        gateway_type=ModelProvider.PORTKEY,
        api_key="pk-test-key",
        virtual_key="vkey-project-123",
    )
    client = AIGatewayClient(config=pk_config)
    headers = client.get_headers()
    assert headers["x-portkey-api-key"] == "pk-test-key"
    assert headers["x-portkey-virtual-key"] == "vkey-project-123"
    assert "x-portkey-trace-id" in headers

    # LiteLLM headers
    litellm_config = GatewayConfig(
        gateway_type=ModelProvider.LITELLM,
        api_key="sk-litellm-secret",
        virtual_key="cust-999",
    )
    litellm_client = AIGatewayClient(config=litellm_config)
    llm_headers = litellm_client.get_headers()
    assert llm_headers["Authorization"] == "Bearer sk-litellm-secret"
    assert llm_headers["x-litellm-key"] == "cust-999"


def test_tiered_router_model_selection_and_cost():
    router = TieredRouter()

    # Complexity tier model mapping
    assert router.select_model(ComplexityTier.LIGHT) == "claude-3-5-haiku"
    assert router.select_model(ComplexityTier.STANDARD) == "claude-3-5-sonnet"
    assert router.select_model(ComplexityTier.REASONING) == "o3-mini"

    # Explicit override
    assert router.select_model(ComplexityTier.LIGHT, override_model="custom-mistral") == "custom-mistral"

    # Fallback chain resolution
    chain = router.get_fallback_chain("claude-3-5-haiku")
    assert chain[0] == "claude-3-5-haiku"
    assert len(chain) > 1

    # Cost calculation: 100k prompt tokens, 10k completion tokens on gpt-4o ($2.50 / $10.00 per 1M)
    # in: 100_000/1_000_000 * 2.50 = $0.25
    # out: 10_000/1_000_000 * 10.00 = $0.10
    # total = $0.35
    cost = router.calculate_cost("gpt-4o", prompt_tokens=100_000, completion_tokens=10_000)
    assert cost == 0.35


def test_semantic_cache_hit_and_similarity():
    cache = SemanticCache(similarity_threshold=0.80)

    resp1 = CompletionResponse(
        content='{"status": "ok", "user": "alice"}',
        model_used="claude-3-5-haiku",
        provider_used="portkey",
        prompt_tokens=40,
        completion_tokens=10,
        total_tokens=50,
        cost_usd=0.0001,
        latency_ms=22.5,
    )

    prompt = "Extract json data for user profile with name Alice"
    cache.store(prompt, resp1)

    # Exact lookup
    hit_exact = cache.lookup(prompt)
    assert hit_exact is not None
    assert hit_exact.cached is True
    assert hit_exact.cost_usd == 0.0
    assert hit_exact.content == '{"status": "ok", "user": "alice"}'

    # Semantic similarity lookup (similar phrasing)
    similar_prompt = "Extract json data for user profile name Alice"
    hit_similar = cache.lookup(similar_prompt)
    assert hit_similar is not None
    assert hit_similar.cached is True
    assert hit_similar.metadata["semantic_similarity"] >= 0.80

    # Completely different prompt -> miss
    miss = cache.lookup("Write a Python sorting algorithm using quicksort")
    assert miss is None

    stats = cache.stats()
    assert stats["total_hits"] == 2
    assert stats["total_misses"] == 1
    assert stats["hit_rate"] == round(2 / 3, 4)
    assert stats["total_saved_cost_usd"] > 0.0


def test_ai_gateway_client_end_to_end_and_finops():
    tracer = OTELTracerBot(service_name="test-gateway-tracer")
    client = AIGatewayClient(
        config=GatewayConfig(
            gateway_type=ModelProvider.PORTKEY,
            semantic_cache_enabled=True,
            cache_threshold=0.85,
        ),
        tracer=tracer,
    )

    # Request 1: Light tier extraction (cache miss)
    req1 = CompletionRequest(
        prompt="Parse the incident ticket id from log trace 98234",
        tier=ComplexityTier.LIGHT,
    )
    res1 = client.complete(req1)
    assert res1.cached is False
    assert res1.model_used == "claude-3-5-haiku"
    assert res1.cost_usd > 0.0

    # Request 2: Semantic cache hit with same query
    res2 = client.complete(req1)
    assert res2.cached is True
    assert res2.cost_usd == 0.0

    # Request 3: Reasoning tier completion
    req3 = CompletionRequest(
        prompt="Design distributed Raft consensus multi-datacenter topology",
        tier=ComplexityTier.REASONING,
    )
    res3 = client.complete(req3)
    assert res3.cached is False
    assert res3.model_used == "o3-mini"

    # FinOps summary
    finops = client.get_finops_summary()
    assert finops["total_requests"] == 3
    assert finops["total_tokens"] > 0
    assert finops["cache"]["total_hits"] == 1
    assert finops["cache"]["total_misses"] == 2
