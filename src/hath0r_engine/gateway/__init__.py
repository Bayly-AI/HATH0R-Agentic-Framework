"""AI Gateway adapter package for Hath0r."""

from hath0r_engine.gateway.base import (
    CompletionRequest,
    CompletionResponse,
    ComplexityTier,
    GatewayConfig,
    ModelProvider,
)
from hath0r_engine.gateway.cache import CacheEmbeddingMode, CacheEntry, DenseBiEncoder, SemanticCache
from hath0r_engine.gateway.client import AIGatewayClient
from hath0r_engine.gateway.routing import TieredRouter
from hath0r_engine.gateway.tokenizer_tax import (
    ScriptBreakdown,
    TaxAuditReport,
    TokenizerTaxAuditor,
    VocabVRAMFootprint,
)

__all__ = [
    "ComplexityTier",
    "ModelProvider",
    "GatewayConfig",
    "CompletionRequest",
    "CompletionResponse",
    "CacheEmbeddingMode",
    "CacheEntry",
    "DenseBiEncoder",
    "SemanticCache",
    "TieredRouter",
    "AIGatewayClient",
    "ScriptBreakdown",
    "VocabVRAMFootprint",
    "TaxAuditReport",
    "TokenizerTaxAuditor",
]
