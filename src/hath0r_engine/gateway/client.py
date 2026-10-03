"""Unified AI Gateway Client with Portkey/LiteLLM Support, Failover, and FinOps Tracking."""

from __future__ import annotations

import os
import time
import uuid
from typing import Any, Dict, Optional

from hath0r_engine.gateway.base import (
    CompletionRequest,
    CompletionResponse,
    GatewayConfig,
    ModelProvider,
)
from hath0r_engine.gateway.cache import SemanticCache
from hath0r_engine.gateway.routing import TieredRouter
from hath0r_engine.telemetry.otel_tracer import OTELTracerBot
from hath0r_engine.telemetry.token_telemetry import TokenTelemetryBot


class AIGatewayClient:
    """Unified client orchestrating multi-provider gateways, tiered routing, and semantic caching."""

    def __init__(
        self,
        config: Optional[GatewayConfig] = None,
        router: Optional[TieredRouter] = None,
        cache: Optional[SemanticCache] = None,
        tracer: Optional[OTELTracerBot] = None,
        token_telemetry: Optional[TokenTelemetryBot] = None,
    ) -> None:
        self.config = config or GatewayConfig()
        self.router = router or TieredRouter()
        self.cache = cache or (
            SemanticCache(similarity_threshold=self.config.cache_threshold)
            if self.config.semantic_cache_enabled
            else None
        )
        self.tracer = tracer or OTELTracerBot(service_name="hath0r-ai-gateway")
        self.token_telemetry = (
            token_telemetry if token_telemetry is not None else TokenTelemetryBot()
        )

        # FinOps Aggregators
        self.total_requests: int = 0
        self.total_prompt_tokens: int = 0
        self.total_completion_tokens: int = 0
        self.total_spend_usd: float = 0.0

    def get_headers(self, virtual_key: Optional[str] = None) -> Dict[str, str]:
        """Construct provider-specific gateway headers (e.g. Portkey, LiteLLM)."""
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Hath0r-AI-Gateway/1.0.0",
        }
        vkey = virtual_key or self.config.virtual_key

        if self.config.gateway_type == ModelProvider.PORTKEY:
            if self.config.api_key:
                headers["x-portkey-api-key"] = self.config.api_key
            if vkey:
                headers["x-portkey-virtual-key"] = vkey
            headers["x-portkey-trace-id"] = uuid.uuid4().hex

        elif self.config.gateway_type == ModelProvider.LITELLM:
            if self.config.api_key:
                headers["Authorization"] = f"Bearer {self.config.api_key}"
            if vkey:
                headers["x-litellm-key"] = vkey

        elif self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"

        return headers

    def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Execute a model completion with semantic cache lookup, tiered routing, and OTEL telemetry."""
        full_prompt = request.get_full_prompt()
        self.total_requests += 1

        # 1. Semantic Cache Lookup
        if self.cache and self.config.semantic_cache_enabled:
            cached_resp = self.cache.lookup(full_prompt)
            if cached_resp:
                if self.token_telemetry:
                    req_meta = request.metadata or {}
                    user_id = str(
                        req_meta.get("user_id")
                        or req_meta.get("user")
                        or os.environ.get("USER")
                        or "default_user"
                    )
                    agent_id = str(
                        req_meta.get("agent_id")
                        or req_meta.get("agent")
                        or "hath0r-agent"
                    )
                    session_id = str(
                        req_meta.get("session_id")
                        or req_meta.get("session")
                        or ""
                    )
                    self.token_telemetry.record_prompt(
                        prompt=full_prompt,
                        user_id=user_id,
                        model=cached_resp.model_used,
                        tier=request.tier.value,
                        completion=cached_resp.content,
                        prompt_tokens=cached_resp.prompt_tokens,
                        completion_tokens=cached_resp.completion_tokens,
                        latency_ms=cached_resp.latency_ms,
                        cached=True,
                        agent_id=agent_id,
                        session_id=session_id,
                        metadata=req_meta,
                    )
                return cached_resp

        # 2. Tiered Routing Model Selection
        target_model = self.router.select_model(request.tier, request.model)
        fallback_chain = self.router.get_fallback_chain(target_model, self.config.fallback_chain)

        # 3. Execution with Fallback Chain
        start_time = time.time()
        span_name = f"gateway.complete.{request.tier.value}"

        with self.tracer.start_span(
            span_name,
            span_kind="LLM",
            attributes={
                "gateway.provider": self.config.gateway_type.value,
                "gateway.tier": request.tier.value,
                "llm.model_name": target_model,
            },
        ) as span:
            response: Optional[CompletionResponse] = None
            last_err: Optional[Exception] = None

            for model_candidate in fallback_chain:
                try:
                    response = self._execute_model_call(
                        model=model_candidate,
                        request=request,
                        start_time=start_time,
                    )
                    break
                except Exception as err:
                    last_err = err
                    span.add_event("failover_triggered", {"failed_model": model_candidate, "error": str(err)})
                    continue

            if response is None:
                err_msg = f"All models in fallback chain failed: {last_err}"
                span.finish(status="ERROR", error=err_msg)
                raise RuntimeError(err_msg)

            # Record FinOps Metrics
            self.total_prompt_tokens += response.prompt_tokens
            self.total_completion_tokens += response.completion_tokens
            self.total_spend_usd += response.cost_usd

            span.attributes.update(
                {
                    "llm.token_count.prompt": response.prompt_tokens,
                    "llm.token_count.completion": response.completion_tokens,
                    "llm.token_count.total": response.total_tokens,
                    "finops.cost_usd": response.cost_usd,
                    "response.model_used": response.model_used,
                }
            )

            # 4. Store in Semantic Cache
            if self.cache and self.config.semantic_cache_enabled:
                self.cache.store(full_prompt, response)

            # 5. Record Token Telemetry Ledger
            if self.token_telemetry:
                req_meta = request.metadata or {}
                user_id = str(
                    req_meta.get("user_id")
                    or req_meta.get("user")
                    or os.environ.get("USER")
                    or "default_user"
                )
                agent_id = str(
                    req_meta.get("agent_id")
                    or req_meta.get("agent")
                    or "hath0r-agent"
                )
                session_id = str(
                    req_meta.get("session_id")
                    or req_meta.get("session")
                    or ""
                )
                self.token_telemetry.record_prompt(
                    prompt=full_prompt,
                    user_id=user_id,
                    model=response.model_used,
                    tier=request.tier.value,
                    completion=response.content,
                    prompt_tokens=response.prompt_tokens,
                    completion_tokens=response.completion_tokens,
                    latency_ms=response.latency_ms,
                    cached=False,
                    agent_id=agent_id,
                    session_id=session_id,
                    metadata=req_meta,
                )

            return response

    def _execute_model_call(
        self,
        model: str,
        request: CompletionRequest,
        start_time: float,
    ) -> CompletionResponse:
        """Execute single model call or mock response."""
        latency_ms = (time.time() - start_time) * 1000.0

        # Token count estimation (4 chars ~ 1 token)
        full_text = request.get_full_prompt()
        prompt_tokens = max(1, len(full_text) // 4)
        mock_output = f"Hath0r AI Gateway [{self.config.gateway_type.value}] response via {model}."
        completion_tokens = max(1, len(mock_output) // 4)
        total_tokens = prompt_tokens + completion_tokens

        cost_usd = self.router.calculate_cost(model, prompt_tokens, completion_tokens)

        return CompletionResponse(
            content=mock_output,
            model_used=model,
            provider_used=self.config.gateway_type.value,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            cost_usd=cost_usd,
            latency_ms=round(latency_ms, 2),
            cached=False,
            metadata={"tier": request.tier.value, "virtual_key": request.virtual_key or self.config.virtual_key},
        )

    def get_finops_summary(self) -> Dict[str, Any]:
        """Aggregate total token spend, cost estimations, and semantic cache savings."""
        cache_stats = self.cache.stats() if self.cache else {}
        return {
            "total_requests": self.total_requests,
            "total_prompt_tokens": self.total_prompt_tokens,
            "total_completion_tokens": self.total_completion_tokens,
            "total_tokens": self.total_prompt_tokens + self.total_completion_tokens,
            "total_spend_usd": round(self.total_spend_usd, 6),
            "cache": cache_stats,
        }
