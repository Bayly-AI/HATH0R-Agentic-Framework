"""Data Models and Interfaces for the Unified AI Gateway Adapter."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class ComplexityTier(str, Enum):
    """Task complexity tiers for cost-optimized dynamic routing."""

    LIGHT = "light"          # Fast, cheap JSON extraction / triage (haiku / 4o-mini / flash)
    STANDARD = "standard"    # General tool execution & coding (sonnet-3.5 / gpt-4o)
    REASONING = "reasoning"  # High-order architectural synthesis (o3-mini / deepseek-r1 / opus)


class ModelProvider(str, Enum):
    """Supported AI gateway backends and model providers."""

    PORTKEY = "portkey"
    LITELLM = "litellm"
    ANTHROPIC = "anthropic"
    OPENAI = "openai"
    BEDROCK = "bedrock"
    VERTEX = "vertex"
    OLLAMA = "ollama"
    VLLM = "vllm"
    MOCK = "mock"


@dataclass
class GatewayConfig:
    """Configuration for AI Gateway adapter."""

    gateway_type: ModelProvider = ModelProvider.MOCK
    endpoint_url: Optional[str] = None
    api_key: Optional[str] = None
    fallback_chain: List[str] = field(
        default_factory=lambda: ["claude-3-5-sonnet", "gpt-4o", "mistral-large"]
    )
    semantic_cache_enabled: bool = True
    cache_threshold: float = 0.90
    virtual_key: Optional[str] = None
    timeout_seconds: float = 60.0
    vllm_api_base: Optional[str] = None
    enable_prefix_caching: bool = True
    kv_block_size: int = 16
    enable_chunked_prefill: bool = True
    chunk_aligned_eviction: bool = True
    guided_decoding_backend: str = "outlines"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["gateway_type"] = self.gateway_type.value
        return data

    @classmethod
    def from_yaml(cls, config_path: Optional[str] = None) -> "GatewayConfig":
        """Load gateway configuration from YAML file."""
        from pathlib import Path

        import yaml

        target_path: Optional[Path] = None
        if config_path:
            target_path = Path(config_path)
        else:
            candidates = [
                Path.cwd() / "cfg" / "gateway.yaml",
                Path(__file__).resolve().parents[3] / "cfg" / "gateway.yaml",
            ]
            for cand in candidates:
                if cand.is_file():
                    target_path = cand
                    break

        if not target_path or not target_path.is_file():
            return cls()

        with open(target_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}

        prov_str = str(cfg.get("default_provider", "mock")).lower()
        try:
            gw_type = ModelProvider(prov_str)
        except ValueError:
            gw_type = ModelProvider.MOCK

        vllm_cfg = cfg.get("vllm", {})
        cache_cfg = cfg.get("cache", {})
        fallbacks = cfg.get("fallback_chain", ["claude-3-5-sonnet", "gpt-4o", "mistral-large"])

        endpoint = vllm_cfg.get("endpoint_url") if gw_type == ModelProvider.VLLM else None
        api_key = vllm_cfg.get("api_key") if gw_type == ModelProvider.VLLM else None

        return cls(
            gateway_type=gw_type,
            endpoint_url=endpoint,
            api_key=api_key,
            fallback_chain=fallbacks,
            semantic_cache_enabled=bool(cache_cfg.get("enabled", True)),
            cache_threshold=float(cache_cfg.get("similarity_threshold", 0.90)),
            timeout_seconds=float(vllm_cfg.get("timeout_seconds", 60.0)),
            vllm_api_base=vllm_cfg.get("endpoint_url"),
            enable_prefix_caching=bool(vllm_cfg.get("enable_prefix_caching", True)),
            kv_block_size=int(vllm_cfg.get("kv_block_size", 16)),
            enable_chunked_prefill=bool(vllm_cfg.get("enable_chunked_prefill", True)),
            chunk_aligned_eviction=bool(vllm_cfg.get("chunk_aligned_eviction", True)),
            guided_decoding_backend=str(vllm_cfg.get("guided_decoding_backend", "outlines")),
            metadata={"raw_config": cfg},
        )


@dataclass
class CompletionRequest:
    """Unified completion request across all providers and tiers."""

    prompt: str = ""
    messages: List[Dict[str, str]] = field(default_factory=list)
    tier: ComplexityTier = ComplexityTier.STANDARD
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 2048
    virtual_key: Optional[str] = None
    guided_json: Optional[Dict[str, Any] | str] = None
    guided_regex: Optional[str] = None
    guided_choice: Optional[List[str]] = None
    contract_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def get_full_prompt(self) -> str:
        """Combine prompt string and message list into single text representation."""
        if self.prompt:
            return self.prompt
        if self.messages:
            return "\n".join(f"{m.get('role', 'user')}: {m.get('content', '')}" for m in self.messages)
        return ""


@dataclass
class CompletionResponse:
    """Unified response descriptor including token metrics, FinOps cost, and cache state."""

    content: str
    model_used: str
    provider_used: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    cost_usd: float = 0.0
    latency_ms: float = 0.0
    cached: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
