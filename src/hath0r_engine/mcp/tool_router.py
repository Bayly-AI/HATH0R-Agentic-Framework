"""Dynamic Semantic Tool Router for Enterprise MCP Fleets.

Vector-indexes tool descriptions, parameter schemas, and metadata across hundreds of
microservice tools, dynamically retrieving and pruning the top-k tools for agent context windows.
"""

from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from hath0r_engine.graph.knowledge_graph import BM25Index, LightweightVectorIndex
from hath0r_engine.mcp.identity import CallerIdentity
from hath0r_engine.mcp.schema_pruner import PruningMode, SchemaPruner
from hath0r_engine.mcp.telemetry import MCPRoutingTelemetry, RoutingMetric


@dataclass
class ToolDefinition:
    """Registration record for an MCP tool."""

    server_id: str
    name: str
    description: str
    parameters: Dict[str, Any]
    tags: List[str] = field(default_factory=list)
    required_scopes: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def qualified_name(self) -> str:
        return f"{self.server_id}:{self.name}"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class DynamicToolRouter:
    """Indexes and routes tools across large enterprise MCP fleets."""

    def __init__(
        self,
        pruner: Optional[SchemaPruner] = None,
        telemetry: Optional[MCPRoutingTelemetry] = None,
    ) -> None:
        self.tools: Dict[str, ToolDefinition] = {}
        self.pruner = pruner or SchemaPruner()
        self.telemetry = telemetry or MCPRoutingTelemetry()
        self._bm25_index: Optional[BM25Index] = None
        self._vector_index: Optional[LightweightVectorIndex] = None

    def register_tool(
        self,
        server_id: str,
        name: str,
        description: str,
        parameters: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        required_scopes: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ToolDefinition:
        """Register a tool definition into the router."""
        tool = ToolDefinition(
            server_id=server_id,
            name=name,
            description=description,
            parameters=parameters or {},
            tags=tags or [],
            required_scopes=required_scopes or [],
            metadata=metadata or {},
        )
        self.tools[tool.qualified_name] = tool
        self._invalidate_indices()
        return tool

    def register_mcp_server_manifest(self, server_id: str, manifest: Dict[str, Any]) -> int:
        """Register all tools declared in an MCP server manifest or discovery response."""
        tools_list = manifest.get("tools", [])
        registered_count = 0
        for t in tools_list:
            name = t.get("name", "")
            if not name:
                continue
            desc = t.get("description", "")
            params = t.get("inputSchema") or t.get("parameters") or {}
            tags = t.get("tags") or []
            scopes = t.get("required_scopes") or []
            self.register_tool(
                server_id=server_id,
                name=name,
                description=desc,
                parameters=params,
                tags=tags,
                required_scopes=scopes,
            )
            registered_count += 1
        return registered_count

    def _invalidate_indices(self) -> None:
        """Invalidate search indices upon tool registry changes."""
        self._bm25_index = None
        self._vector_index = None

    def _build_indices(self) -> None:
        """Build BM25 and vector indices across tool descriptions."""
        corpus: Dict[str, str] = {}
        for qname, tool in self.tools.items():
            text = f"{tool.name} {tool.description} {' '.join(tool.tags)}"
            corpus[qname] = text

        self._bm25_index = BM25Index()
        self._bm25_index.index_documents(corpus)

        self._vector_index = LightweightVectorIndex()
        self._vector_index.index_documents(corpus)

    def route_tools(
        self,
        query: str,
        top_k: int = 5,
        caller: Optional[CallerIdentity] = None,
        min_score: float = 0.0,
    ) -> List[Tuple[ToolDefinition, float]]:
        """Retrieve top-k tools matching query semantics and caller authorization."""
        if not self.tools:
            return []

        if self._bm25_index is None or self._vector_index is None:
            self._build_indices()

        # Score with BM25
        bm25_scores = self._bm25_index.score(query) if self._bm25_index else {}
        # Score with Vector Cosine
        vec_scores = self._vector_index.score(query) if self._vector_index else {}

        # Normalize BM25
        max_bm25 = max(bm25_scores.values()) if bm25_scores and max(bm25_scores.values()) > 0 else 1.0
        normalized_bm25 = {k: v / max_bm25 for k, v in bm25_scores.items()}

        candidate_scores: List[Tuple[ToolDefinition, float]] = []

        for qname, tool in self.tools.items():
            # Check caller authorization scopes if caller is provided
            if caller and tool.required_scopes:
                if not any(caller.has_scope(s) for s in tool.required_scopes):
                    continue

            b_score = normalized_bm25.get(qname, 0.0)
            v_score = vec_scores.get(qname, 0.0)

            hybrid_score = 0.5 * b_score + 0.5 * v_score
            if hybrid_score >= min_score or not query:
                candidate_scores.append((tool, round(hybrid_score, 4)))

        candidate_scores.sort(key=lambda x: x[1], reverse=True)
        return candidate_scores[:top_k]

    def get_pruned_tools_for_llm(
        self,
        query: str,
        top_k: int = 5,
        mode: PruningMode = PruningMode.STANDARD,
        caller: Optional[CallerIdentity] = None,
    ) -> List[Dict[str, Any]]:
        """Route, prune, and format tools for LLM prompt context, capturing telemetry."""
        start_time = time.time()

        # Calculate fleet-wide unpruned baseline tokens
        unpruned_fleet = [
            {"name": t.name, "description": t.description, "parameters": t.parameters}
            for t in self.tools.values()
        ]
        unpruned_tokens = self.pruner.estimate_tokens(unpruned_fleet)

        # Route top-k tools
        routed = self.route_tools(query=query, top_k=top_k, caller=caller)
        selected_tool_dicts = [
            {"name": tool.name, "description": tool.description, "parameters": tool.parameters}
            for tool, _ in routed
        ]

        # Prune candidate tools
        pruned_tools = self.pruner.prune_tool_list(selected_tool_dicts, mode=mode)
        pruned_tokens = self.pruner.estimate_tokens(pruned_tools)

        tokens_saved = max(0, unpruned_tokens - pruned_tokens)
        reduction_pct = (
            round((tokens_saved / unpruned_tokens) * 100.0, 2) if unpruned_tokens > 0 else 0.0
        )
        latency_ms = round((time.time() - start_time) * 1000.0, 2)

        # Record telemetry
        self.telemetry.record(
            RoutingMetric(
                query=query,
                total_fleet_tools=len(self.tools),
                routed_tools_count=len(pruned_tools),
                unpruned_tokens=unpruned_tokens,
                pruned_tokens=pruned_tokens,
                tokens_saved=tokens_saved,
                reduction_pct=reduction_pct,
                latency_ms=latency_ms,
            )
        )

        return pruned_tools

    def get_telemetry_summary(self) -> Dict[str, Any]:
        """Retrieve aggregated routing telemetry summary."""
        return self.telemetry.get_summary()
