"""Comprehensive Unit & Integration Tests for vLLM Gateway Adapter and Guided Decoding."""

from __future__ import annotations

import json
import urllib.error
from unittest.mock import MagicMock, patch

from hath0r_engine.gateway.base import (
    CompletionRequest,
    ComplexityTier,
    GatewayConfig,
    ModelProvider,
)
from hath0r_engine.gateway.client import AIGatewayClient
from hath0r_engine.gateway.routing import TieredRouter


def _build_mock_vllm_response(
    content: str = '{"status": "success"}',
    model: str = "meta-llama/Llama-3.3-70B-Instruct",
    prompt_tokens: int = 120,
    completion_tokens: int = 25,
) -> MagicMock:
    """Helper to mock urllib.request.urlopen returning vLLM OpenAI-compatible payload."""
    payload = {
        "id": "chatcmpl-vllm-test-001",
        "object": "chat.completion",
        "created": 1700000000,
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
        },
    }
    raw_bytes = json.dumps(payload).encode("utf-8")
    mock_resp = MagicMock()
    mock_resp.read.return_value = raw_bytes
    mock_resp.__enter__.return_value = mock_resp
    return mock_resp


def test_vllm_gateway_config_from_yaml():
    """Verify loading declarative gateway configuration from YAML."""
    config = GatewayConfig.from_yaml()
    assert config.gateway_type == ModelProvider.VLLM
    assert config.endpoint_url == "http://localhost:8000/v1"
    assert config.enable_prefix_caching is True
    assert config.guided_decoding_backend == "outlines"
    assert "meta-llama/Llama-3.3-70B-Instruct" in config.fallback_chain


def test_vllm_headers_and_auth():
    """Verify vLLM headers with bearer tokens and virtual keys."""
    config = GatewayConfig(
        gateway_type=ModelProvider.VLLM,
        endpoint_url="http://vllm-cluster:8000/v1",
        api_key="vllm-secret-token",
        virtual_key="vk-dept-ai",
    )
    client = AIGatewayClient(config=config)
    headers = client.get_headers()
    assert headers["Authorization"] == "Bearer vllm-secret-token"
    assert headers["x-vllm-key"] == "vk-dept-ai"
    assert headers["Content-Type"] == "application/json"


def test_tiered_router_vllm_defaults():
    """Verify TieredRouter maps complexity tiers to open-weight models for vLLM."""
    router = TieredRouter()

    # Complexity tier model mapping for vLLM
    assert router.select_model(ComplexityTier.LIGHT, provider=ModelProvider.VLLM) == "Qwen/Qwen2.5-Coder-7B-Instruct"
    assert router.select_model(ComplexityTier.STANDARD, provider=ModelProvider.VLLM) == "meta-llama/Llama-3.3-70B-Instruct"
    assert router.select_model(ComplexityTier.REASONING, provider=ModelProvider.VLLM) == "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"

    # Self-hosted pricing is $0.00
    cost_70b = router.calculate_cost("meta-llama/Llama-3.3-70B-Instruct", prompt_tokens=50000, completion_tokens=1000)
    assert cost_70b == 0.0

    cost_r1 = router.calculate_cost("deepseek-ai/DeepSeek-R1-Distill-Qwen-32B", prompt_tokens=25000, completion_tokens=5000)
    assert cost_r1 == 0.0


@patch("urllib.request.urlopen")
def test_vllm_execution_success(mock_urlopen):
    """Verify full completion flow against vLLM with OpenAI-compatible payload parsing."""
    mock_urlopen.return_value = _build_mock_vllm_response(
        content='{"execution": "ok", "action": "test_step"}',
        model="meta-llama/Llama-3.3-70B-Instruct",
        prompt_tokens=80,
        completion_tokens=20,
    )

    config = GatewayConfig(
        gateway_type=ModelProvider.VLLM,
        endpoint_url="http://localhost:8000/v1",
        semantic_cache_enabled=False,
    )
    client = AIGatewayClient(config=config)

    req = CompletionRequest(
        prompt="Execute unit test verification",
        tier=ComplexityTier.STANDARD,
    )
    resp = client.complete(req)

    assert resp.content == '{"execution": "ok", "action": "test_step"}'
    assert resp.model_used == "meta-llama/Llama-3.3-70B-Instruct"
    assert resp.provider_used == "vllm"
    assert resp.prompt_tokens == 80
    assert resp.completion_tokens == 20
    assert resp.cost_usd == 0.0
    assert resp.cached is False
    assert resp.metadata["vllm_endpoint"] == "http://localhost:8000/v1"

    # Verify request payload sent over wire
    called_req = mock_urlopen.call_args[0][0]
    assert called_req.full_url == "http://localhost:8000/v1/chat/completions"
    sent_payload = json.loads(called_req.data.decode("utf-8"))
    assert sent_payload["model"] == "meta-llama/Llama-3.3-70B-Instruct"
    assert sent_payload["messages"][0]["content"] == "Execute unit test verification"


@patch("urllib.request.urlopen")
def test_vllm_guided_decoding_json_and_regex(mock_urlopen):
    """Verify guided_json and guided_regex parameters are injected into vLLM payload."""
    mock_urlopen.return_value = _build_mock_vllm_response(content='{"name": "Alice", "age": 30}')

    config = GatewayConfig(
        gateway_type=ModelProvider.VLLM,
        endpoint_url="http://localhost:8000/v1",
        semantic_cache_enabled=False,
    )
    client = AIGatewayClient(config=config)

    # 1. Guided JSON (Schema dict)
    json_schema = {
        "type": "object",
        "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
        "required": ["name", "age"],
    }
    req_json = CompletionRequest(
        prompt="Generate person record",
        guided_json=json_schema,
    )
    resp_json = client.complete(req_json)
    assert resp_json.metadata["guided_decoding"] == "json"

    sent_payload = json.loads(mock_urlopen.call_args[0][0].data.decode("utf-8"))
    assert sent_payload["guided_json"] == json.dumps(json_schema)

    # 2. Guided Regex
    req_regex = CompletionRequest(
        prompt="Generate semver tag",
        guided_regex=r"v[0-9]+\.[0-9]+\.[0-9]+",
    )
    resp_regex = client.complete(req_regex)
    assert resp_regex.metadata["guided_decoding"] == "regex"

    sent_payload_regex = json.loads(mock_urlopen.call_args[0][0].data.decode("utf-8"))
    assert sent_payload_regex["guided_regex"] == r"v[0-9]+\.[0-9]+\.[0-9]+"

    # 3. Guided Choice
    req_choice = CompletionRequest(
        prompt="Classify intent",
        guided_choice=["allow", "deny", "review"],
    )
    resp_choice = client.complete(req_choice)
    assert resp_choice.metadata["guided_decoding"] == "choice"

    sent_payload_choice = json.loads(mock_urlopen.call_args[0][0].data.decode("utf-8"))
    assert sent_payload_choice["guided_choice"] == ["allow", "deny", "review"]


@patch("urllib.request.urlopen")
def test_vllm_contract_schema_resolution(mock_urlopen):
    """Verify request specifying a Hath0r contract_id resolves schema from contracts/."""
    mock_urlopen.return_value = _build_mock_vllm_response(content='{"testCaseId": "tc-001"}')

    config = GatewayConfig(
        gateway_type=ModelProvider.VLLM,
        endpoint_url="http://localhost:8000/v1",
        semantic_cache_enabled=False,
    )
    client = AIGatewayClient(config=config)

    req = CompletionRequest(
        prompt="Generate playwright test spec",
        contract_id="hath0r-playwright-test-spec-v1",
    )
    resp = client.complete(req)
    assert resp.metadata["contract_id"] == "hath0r-playwright-test-spec-v1"
    assert resp.metadata["guided_decoding"] == "json"

    sent_payload = json.loads(mock_urlopen.call_args[0][0].data.decode("utf-8"))
    assert "guided_json" in sent_payload
    loaded_schema = json.loads(sent_payload["guided_json"])
    assert "$schema" in loaded_schema
    assert loaded_schema["title"] == "hath0r.playwright.testspec/1"


@patch("urllib.request.urlopen")
def test_vllm_failover_and_error_handling(mock_urlopen):
    """Verify graceful handling when vLLM endpoint is unavailable."""
    # Simulate network error connecting to vLLM
    mock_urlopen.side_effect = urllib.error.URLError("Connection refused")

    config = GatewayConfig(
        gateway_type=ModelProvider.VLLM,
        endpoint_url="http://unreachable-cluster:8000/v1",
        fallback_chain=["meta-llama/Llama-3.3-70B-Instruct"],
        semantic_cache_enabled=False,
    )
    client = AIGatewayClient(config=config)

    req = CompletionRequest(prompt="Test connection failure")
    try:
        client.complete(req)
        assert False, "Should have raised RuntimeError on connection failure"
    except RuntimeError as err:
        assert "call failed" in str(err)


@patch("urllib.request.urlopen")
def test_vllm_semantic_cache_deduplication(mock_urlopen):
    """Verify vLLM completions leverage semantic caching to prevent duplicate network calls."""
    mock_urlopen.return_value = _build_mock_vllm_response(content='{"cached_payload": 42}')

    config = GatewayConfig(
        gateway_type=ModelProvider.VLLM,
        endpoint_url="http://localhost:8000/v1",
        semantic_cache_enabled=True,
    )
    client = AIGatewayClient(config=config)

    req1 = CompletionRequest(prompt="Extract data for entity alpha")
    resp1 = client.complete(req1)
    assert resp1.cached is False
    assert mock_urlopen.call_count == 1

    # Exact prompt repetition should hit cache without calling urlopen again
    req2 = CompletionRequest(prompt="Extract data for entity alpha")
    resp2 = client.complete(req2)
    assert resp2.cached is True
    assert mock_urlopen.call_count == 1


def test_pagedattention_chunk_aligned_kv_eviction_policy():
    """Verify PagedAttention KV eviction respects chunk boundaries and preserves prefix block hashes."""
    from hath0r_engine.gateway.cache import ChunkAlignedKVEvictionPolicy, KVBlockChunk, KVBlockTier
    from hath0r_engine.memory.memory_tools import MemoryPagingManager

    config = GatewayConfig.from_yaml()
    assert config.kv_block_size == 16
    assert config.enable_chunked_prefill is True
    assert config.chunk_aligned_eviction is True

    policy = ChunkAlignedKVEvictionPolicy(block_size=16)
    chunks_turn1 = [
        KVBlockChunk(chunk_id="sys:rules", content=" ".join(f"sys_{i}" for i in range(18)), tier=KVBlockTier.STATIC, pinned=True),
        KVBlockChunk(chunk_id="cag:contract", content=" ".join(f"cag_{i}" for i in range(12)), tier=KVBlockTier.SEMI_STATIC),
        KVBlockChunk(chunk_id="turn:1", content=" ".join(f"t1_{i}" for i in range(20)), tier=KVBlockTier.DYNAMIC_TAIL, priority=0.1),
    ]
    res1 = policy.pack_and_evict(chunks_turn1, max_tokens=128)
    assert res1["boundary_aligned"] is True
    assert res1["aligned_token_count"] % 16 == 0
    assert res1["evicted_tokens"] == 0
    prefix_hashes_turn1 = res1["block_hashes"][:3]  # 2 blocks of sys + 1 block of cag

    # Turn 2: add more dynamic tail turns that exceed max_tokens=64 (4 blocks), forcing tail eviction
    chunks_turn2 = chunks_turn1 + [
        KVBlockChunk(chunk_id="turn:2", content=" ".join(f"t2_{i}" for i in range(20)), tier=KVBlockTier.DYNAMIC_TAIL, priority=0.9),
    ]
    res2 = policy.pack_and_evict(chunks_turn2, max_tokens=64)
    assert res2["boundary_aligned"] is True
    assert res2["evicted_tokens"] % 16 == 0
    assert res2["evicted_blocks"] > 0
    assert "turn:1" in res2["evicted_chunk_ids"]
    # Static + semi-static prefix hashes must be 100% preserved without page reload jitter
    assert res2["block_hashes"][:3] == prefix_hashes_turn1
    assert res2["matched_prefix_blocks"] >= 3

    # Verify MemoryPagingManager integration
    mp = MemoryPagingManager()
    mp_res = mp.pack_block_aligned_context(
        dynamic_turns=[" ".join(f"msgA_{i}" for i in range(20)), " ".join(f"msgB_{i}" for i in range(20))],
        max_tokens=64,
        block_size=16,
    )
    assert mp_res["boundary_aligned"] is True
    assert mp_res["evicted_tokens"] % 16 == 0

