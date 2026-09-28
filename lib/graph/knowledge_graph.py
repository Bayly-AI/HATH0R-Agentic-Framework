"""Hath0r KnowledgeGraph Engine.

Extracts structured relational entity nodes and edges from Markdown files with YAML frontmatter,
and provides fast relational traversal and lineage analysis.
"""

from __future__ import annotations

import datetime
import os
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


@dataclass
class KnowledgeNode:
    """An entity node in the KnowledgeGraph."""

    id: str
    type: str  # document | contract | procedure | strategy | playbook | runbook | checklist | policy | tool | bot | subsystem
    title: str
    path: str
    subsystem: str = "root"
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KnowledgeEdge:
    """A directed relational edge in the KnowledgeGraph."""

    source: str
    target: str
    relation: str  # depends_on | implements | references | governed_by | validates | contains | routes_to | invokes
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class KnowledgeGraph:
    """In-memory KnowledgeGraph representation and query interface."""

    def __init__(self, schema_version: str = "hath0r.knowledgegraph/1") -> None:
        self.schema_version = schema_version
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.edges: List[KnowledgeEdge] = []
        self._adjacency: Dict[str, List[KnowledgeEdge]] = {}

    def add_node(self, node: KnowledgeNode) -> None:
        """Add or update an entity node."""
        self.nodes[node.id] = node
        if node.id not in self._adjacency:
            self._adjacency[node.id] = []

    def add_edge(self, edge: KnowledgeEdge) -> None:
        """Add a directed edge between nodes."""
        self.edges.append(edge)
        if edge.source not in self._adjacency:
            self._adjacency[edge.source] = []
        self._adjacency[edge.source].append(edge)

    def get_neighbors(self, node_id: str, relation: Optional[str] = None) -> List[KnowledgeNode]:
        """Find neighboring nodes for a given entity."""
        neighbors = []
        for edge in self._adjacency.get(node_id, []):
            if relation is None or edge.relation == relation:
                if edge.target in self.nodes:
                    neighbors.append(self.nodes[edge.target])
        return neighbors

    def get_lineage(self, node_id: str, max_depth: int = 3) -> Dict[str, Any]:
        """Traverse upstream/downstream lineage tree for a given entity."""
        visited: Set[str] = set()
        tree: Dict[str, Any] = {"id": node_id, "children": []}

        def _traverse(current_id: str, current_tree: Dict[str, Any], depth: int) -> None:
            if depth >= max_depth or current_id in visited:
                return
            visited.add(current_id)
            for edge in self._adjacency.get(current_id, []):
                child_node = self.nodes.get(edge.target)
                child_repr = {
                    "id": edge.target,
                    "relation": edge.relation,
                    "title": child_node.title if child_node else edge.target,
                    "type": child_node.type if child_node else "unknown",
                    "children": [],
                }
                current_tree["children"].append(child_repr)
                _traverse(edge.target, child_repr, depth + 1)

        _traverse(node_id, tree, 0)
        return tree

    def to_dict(self) -> Dict[str, Any]:
        """Export graph snapshot conforming to hath0r-knowledgegraph-v1 schema."""
        return {
            "schema_version": self.schema_version,
            "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "nodes": [asdict(n) for n in self.nodes.values()],
            "edges": [asdict(e) for e in self.edges],
        }


class KnowledgeGraphExtractor:
    """Parses repository directories and Markdown frontmatter to build KnowledgeGraph."""

    @staticmethod
    def parse_frontmatter(content: str) -> Dict[str, Any]:
        """Simple, zero-dependency YAML frontmatter parser."""
        if not content.startswith("---"):
            return {}
        parts = content.split("---", 2)
        if len(parts) < 3:
            return {}
        yaml_text = parts[1].strip()
        data: Dict[str, Any] = {}
        for line in yaml_text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                key = k.strip()
                val = v.strip().strip('"\'')
                # Simple list parsing [a, b]
                if val.startswith("[") and val.endswith("]"):
                    items = [x.strip().strip('"\'') for x in val[1:-1].split(",") if x.strip()]
                    data[key] = items
                else:
                    data[key] = val
        return data

    @classmethod
    def scan_directory(cls, root_path: Path | str) -> KnowledgeGraph:
        """Scan directory tree for Markdown and contract files to build the graph."""
        root = Path(root_path)
        kg = KnowledgeGraph()

        for file_path in root.rglob("*.md"):
            # Skip hidden folders except .hath0r
            parts = file_path.relative_to(root).parts
            if any(p.startswith(".") and p != ".hath0r" for p in parts[:-1]):
                continue

            try:
                content = file_path.read_text(encoding="utf-8")
            except Exception:
                continue

            rel_str = str(file_path.relative_to(root))
            fm = cls.parse_frontmatter(content)
            
            # Determine node type and title
            node_id = fm.get("id") or rel_str
            node_type = fm.get("type") or ("procedure" if "procedure" in rel_str else "document")
            
            # Extract first heading if title missing
            title = fm.get("title")
            if not title:
                match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                title = match.group(1).strip() if match else file_path.stem

            subsystem = parts[0] if len(parts) > 1 else "root"

            node = KnowledgeNode(
                id=node_id,
                type=node_type,
                title=title,
                path=rel_str,
                subsystem=subsystem,
                properties=fm,
            )
            kg.add_node(node)

            # Extract frontmatter edges
            for dep in fm.get("depends_on", []) if isinstance(fm.get("depends_on"), list) else [fm.get("depends_on")] if fm.get("depends_on") else []:
                kg.add_edge(KnowledgeEdge(source=node_id, target=dep, relation="depends_on"))
            for imp in fm.get("implements", []) if isinstance(fm.get("implements"), list) else [fm.get("implements")] if fm.get("implements") else []:
                kg.add_edge(KnowledgeEdge(source=node_id, target=imp, relation="implements"))
            for gov in fm.get("governed_by", []) if isinstance(fm.get("governed_by"), list) else [fm.get("governed_by")] if fm.get("governed_by") else []:
                kg.add_edge(KnowledgeEdge(source=node_id, target=gov, relation="governed_by"))

        return kg
