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
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["gateway_type"] = self.gateway_type.value
        return data


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
    metadata: Dict[str, Any] = field(default_factory=dict)

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
