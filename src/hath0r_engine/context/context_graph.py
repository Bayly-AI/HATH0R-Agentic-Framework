"""Hath0r ContextGraph Runtime Engine.

Tracks ephemeral multi-agent session state, subagent topologies, tool execution graphs,
and JEV security validations.
"""

from __future__ import annotations

import datetime
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class ContextNode:
    """A runtime node representing an agent, subagent, tool, or artifact."""

    id: str
    type: str  # agent | subagent | task | tool_invocation | jev_guard | context_slice | artifact
    label: str
    state: str = "running"  # pending | running | completed | failed | cancelled
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContextEdge:
    """A dynamic runtime relationship edge between context entities."""

    source: str
    target: str
    relation: str  # spawned_by | delegated_to | executed_tool | guarded_by | produced_artifact | consumed_context
    metadata: Dict[str, Any] = field(default_factory=dict)


class ContextGraph:
    """Dynamic session context graph."""

    def __init__(self, session_id: Optional[str] = None) -> None:
        self.session_id: str = session_id or str(uuid.uuid4())
        self.schema_version: str = "hath0r.contextgraph/1"
        self.nodes: Dict[str, ContextNode] = {}
        self.edges: List[ContextEdge] = []
        self.active_subagent_id: Optional[str] = None

    def add_node(self, node: ContextNode) -> None:
        """Register a runtime node."""
        self.nodes[node.id] = node

    def add_edge(self, edge: ContextEdge) -> None:
        """Add a dynamic context relationship."""
        self.edges.append(edge)

    def register_subagent(self, subagent_id: str, label: str, parent_id: Optional[str] = None) -> ContextNode:
        """Track subagent invocation and link to parent."""
        node = ContextNode(id=subagent_id, type="subagent", label=label, state="running")
        self.add_node(node)
        self.active_subagent_id = subagent_id
        if parent_id and parent_id in self.nodes:
            self.add_edge(ContextEdge(source=parent_id, target=subagent_id, relation="delegated_to"))
        return node

    def record_tool_execution(
        self,
        tool_name: str,
        caller_id: str,
        jev_status: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Record tool execution node and optional JEV guard validation."""
        invoc_id = f"tool-{uuid.uuid4().hex[:8]}"
        tool_node = ContextNode(
            id=invoc_id,
            type="tool_invocation",
            label=f"invoke:{tool_name}",
            state="completed",
            properties=properties or {},
        )
        self.add_node(tool_node)
        self.add_edge(ContextEdge(source=caller_id, target=invoc_id, relation="executed_tool"))

        if jev_status:
            guard_id = f"jev-{uuid.uuid4().hex[:8]}"
            guard_node = ContextNode(
                id=guard_id,
                type="jev_guard",
                label=f"jev:{jev_status}",
                state="completed",
                properties={"status": jev_status},
            )
            self.add_node(guard_node)
            self.add_edge(ContextEdge(source=invoc_id, target=guard_id, relation="guarded_by"))

        return invoc_id

    def to_dict(self) -> Dict[str, Any]:
        """Export session ContextGraph snapshot conforming to hath0r-contextgraph-v1 schema."""
        return {
            "schema_version": self.schema_version,
            "session_id": self.session_id,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "active_subagent_id": self.active_subagent_id,
            "nodes": [asdict(n) for n in self.nodes.values()],
            "edges": [asdict(e) for e in self.edges],
        }

    def save_to_file(self, file_path: Path | str) -> None:
        """Persist ContextGraph snapshot to a JSON file."""
        import json
        from pathlib import Path
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    @classmethod
    def load_from_file(cls, file_path: Path | str) -> ContextGraph:
        """Load ContextGraph from a JSON snapshot file."""
        import json
        from pathlib import Path
        path = Path(file_path)
        data = json.loads(path.read_text(encoding="utf-8"))
        cg = cls(session_id=data.get("session_id"))
        cg.schema_version = data.get("schema_version", "hath0r.contextgraph/1")
        cg.active_subagent_id = data.get("active_subagent_id")
        for n_dict in data.get("nodes", []):
            cg.add_node(ContextNode(**n_dict))
        for e_dict in data.get("edges", []):
            cg.add_edge(ContextEdge(**e_dict))
        return cg
