"""MemoryGraph: Semantic and Episodic Memory Graph engine for Hath0r.

Represents working memory, rules, architectural decisions, and episodic learnings
as an interconnected semantic network for autonomous agents.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


@dataclass
class MemoryNode:
    """A node in the Hath0r Memory Graph with temporal interval support."""

    id: str
    type: str  # rule, concept, decision, fact, episode, topic, insight
    label: str
    content: str
    importance: float = 0.5
    tags: List[str] = field(default_factory=list)
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    is_current: bool = True
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_valid_at(self, as_of: Optional[str] = None, only_current: bool = False) -> bool:
        """Check whether this node is valid at a given timestamp or in the current state."""
        if only_current and not self.is_current:
            return False
        if not as_of:
            return True if not only_current else self.is_current
        if self.valid_from and self.valid_from > as_of:
            return False
        if self.valid_to and self.valid_to < as_of:
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MemoryNode:
        return cls(
            id=data["id"],
            type=data["type"],
            label=data["label"],
            content=data["content"],
            importance=data.get("importance", 0.5),
            tags=data.get("tags", []),
            valid_from=data.get("valid_from"),
            valid_to=data.get("valid_to"),
            is_current=data.get("is_current", True),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat()),
            metadata=data.get("metadata", {}),
        )


@dataclass
class MemoryEdge:
    """A relational edge between two memory nodes with temporal interval support."""

    source: str
    target: str
    relation: str  # ENFORCES, REQUIRES, DERIVES_FROM, RELATES_TO, RESOLVES, PRECEDES, SUPERSEDES
    weight: float = 1.0
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    is_current: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_valid_at(self, as_of: Optional[str] = None, only_current: bool = False) -> bool:
        """Check whether this edge is valid at a given timestamp or in the current state."""
        if only_current and not self.is_current:
            return False
        if not as_of:
            return True if not only_current else self.is_current
        if self.valid_from and self.valid_from > as_of:
            return False
        if self.valid_to and self.valid_to < as_of:
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MemoryEdge:
        return cls(
            source=data["source"],
            target=data["target"],
            relation=data["relation"],
            weight=data.get("weight", 1.0),
            valid_from=data.get("valid_from"),
            valid_to=data.get("valid_to"),
            is_current=data.get("is_current", True),
            metadata=data.get("metadata", {}),
        )


class MemoryGraph:
    """Manages the semantic working memory graph for Hath0r agents."""

    def __init__(self, graph_id: str = "default-memory-space"):
        self.schema_version = "1.0.0"
        self.graph_id = graph_id
        self.updated_at = datetime.now(timezone.utc).isoformat()
        self.metadata: Dict[str, Any] = {}
        self.nodes: Dict[str, MemoryNode] = {}
        self.edges: List[MemoryEdge] = []

    def add_node(self, node: MemoryNode) -> None:
        """Add or update a memory node."""
        node.updated_at = datetime.now(timezone.utc).isoformat()
        self.nodes[node.id] = node
        self._touch()

    def get_node(self, node_id: str) -> Optional[MemoryNode]:
        """Retrieve a memory node by ID."""
        return self.nodes.get(node_id)

    def add_edge(self, edge: MemoryEdge) -> None:
        """Add a relational edge between memory nodes."""
        if edge.source not in self.nodes:
            raise ValueError(f"Source node '{edge.source}' does not exist.")
        if edge.target not in self.nodes:
            raise ValueError(f"Target node '{edge.target}' does not exist.")

        # Avoid exact duplicate edge
        for existing in self.edges:
            if existing.source == edge.source and existing.target == edge.target and existing.relation == edge.relation:
                existing.weight = edge.weight
                existing.metadata = edge.metadata
                self._touch()
                return

        self.edges.append(edge)
        self._touch()

    def get_edges_for_node(
        self,
        node_id: str,
        as_of: Optional[str] = None,
        only_current: bool = False,
    ) -> List[MemoryEdge]:
        """Get all incoming and outgoing edges for a given node with temporal filtering."""
        return [
            e
            for e in self.edges
            if (e.source == node_id or e.target == node_id)
            and e.is_valid_at(as_of=as_of, only_current=only_current)
        ]

    def find_nodes(
        self,
        node_type: Optional[str] = None,
        tag: Optional[str] = None,
        min_importance: float = 0.0,
        as_of: Optional[str] = None,
        only_current: bool = False,
    ) -> List[MemoryNode]:
        """Find memory nodes matching specified criteria and temporal validity."""
        results = []
        for node in self.nodes.values():
            if node_type and node.type != node_type:
                continue
            if tag and tag not in node.tags:
                continue
            if node.importance < min_importance:
                continue
            if not node.is_valid_at(as_of=as_of, only_current=only_current):
                continue
            results.append(node)
        return results

    def get_neighborhood(
        self,
        node_id: str,
        depth: int = 1,
        as_of: Optional[str] = None,
        only_current: bool = False,
    ) -> Dict[str, Any]:
        """Extract a subgraph neighborhood around a central node up to a given depth with temporal filtering."""
        if node_id not in self.nodes:
            return {"nodes": [], "edges": []}

        visited_nodes: Set[str] = {node_id}
        current_frontier: Set[str] = {node_id}

        for _ in range(depth):
            next_frontier: Set[str] = set()
            for curr in current_frontier:
                for edge in self.edges:
                    if not edge.is_valid_at(as_of=as_of, only_current=only_current):
                        continue
                    if edge.source == curr and edge.target not in visited_nodes:
                        next_frontier.add(edge.target)
                        visited_nodes.add(edge.target)
                    elif edge.target == curr and edge.source not in visited_nodes:
                        next_frontier.add(edge.source)
                        visited_nodes.add(edge.source)
            current_frontier = next_frontier
            if not current_frontier:
                break

        sub_nodes = [self.nodes[n].to_dict() for n in visited_nodes]
        sub_edges = [
            e.to_dict()
            for e in self.edges
            if e.source in visited_nodes
            and e.target in visited_nodes
            and e.is_valid_at(as_of=as_of, only_current=only_current)
        ]

        return {"nodes": sub_nodes, "edges": sub_edges}

    def ingest_markdown_documents(self, docs_root: Path | str) -> int:
        """Scan and ingest playbooks, runbooks, policies, procedures, and strategies into MemoryGraph."""
        import re

        root = Path(docs_root)
        ingested_count = 0

        # Type mapping based on directory or filename patterns
        type_patterns = {
            "playbook": "concept",
            "runbook": "concept",
            "rule": "rule",
            "policy": "rule",
            "procedure": "concept",
            "strategy": "concept",
            "decision": "decision",
            "adr": "decision",
        }

        for md_path in root.rglob("*.md"):
            # Skip hidden except .hath0r
            parts = md_path.relative_to(root).parts
            if any(p.startswith(".") and p != ".hath0r" for p in parts[:-1]):
                continue

            try:
                content = md_path.read_text(encoding="utf-8")
            except Exception:
                continue

            rel_str = str(md_path.relative_to(root))
            stem_lower = md_path.stem.lower()

            # Determine type
            inferred_type = "topic"
            for keyword, mapped_type in type_patterns.items():
                if keyword in stem_lower or keyword in rel_str.lower():
                    inferred_type = mapped_type
                    break

            # Extract title / heading
            match_title = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
            label = match_title.group(1).strip() if match_title else md_path.stem

            node_id = f"doc:{rel_str}"
            importance = 0.9 if inferred_type == "rule" else 0.7

            # Extract tags
            tags = [p for p in parts[:-1]]
            if inferred_type not in tags:
                tags.append(inferred_type)

            node = MemoryNode(
                id=node_id,
                type=inferred_type,
                label=label,
                content=content[:2000],  # Bounded summary content for memory
                importance=importance,
                tags=tags,
                metadata={"path": rel_str, "file_name": md_path.name},
            )
            self.add_node(node)
            ingested_count += 1

            # Extract markdown references and create RELATES_TO or ENFORCES edges
            for m in re.finditer(r"\[([^\]]+)\]\(([^)]+\.md)\)", content):
                target_file = m.group(2).strip()
                target_id = f"doc:{target_file}" if not target_file.startswith("http") else target_file
                if not target_file.startswith("http") and target_id in self.nodes:
                    rel = "ENFORCES" if inferred_type == "rule" else "RELATES_TO"
                    self.add_edge(MemoryEdge(source=node_id, target=target_id, relation=rel))

        return ingested_count

    CANONICAL_SEED_NODE_IDS: Set[str] = {
        "rule:cr-cli-entry-001",
        "rule:cr-bai-001",
        "rule:cr-memory-compound-001",
        "concept:tri-graph",
    }

    def compound_knowledge(
        self,
        label: str,
        content: str,
        node_type: str = "episode",
        node_id: Optional[str] = None,
        importance: float = 0.8,
        tags: Optional[List[str]] = None,
        relates_to: Optional[List[str]] = None,
        relation: str = "DERIVES_FROM",
        supersedes: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        run_reflection: bool = True,
    ) -> Dict[str, Any]:
        """Compound a structured knowledge node and relational edges into MemoryGraph."""
        import re

        now = datetime.now(timezone.utc).isoformat()
        slug = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")[:48] or "task"
        resolved_id = node_id or f"{node_type}:{slug}"
        resolved_tags = list(dict.fromkeys((tags or []) + [node_type, "compounded"]))

        node = MemoryNode(
            id=resolved_id,
            type=node_type,
            label=label,
            content=content,
            importance=max(0.0, min(1.0, float(importance))),
            tags=resolved_tags,
            valid_from=now,
            is_current=True,
            created_at=now,
            updated_at=now,
            metadata=metadata or {},
        )
        self.add_node(node)

        edges_added: List[Dict[str, Any]] = []
        if supersedes and supersedes in self.nodes and supersedes != resolved_id:
            old_node = self.nodes[supersedes]
            old_node.is_current = False
            old_node.valid_to = now
            sup_edge = MemoryEdge(
                source=resolved_id,
                target=supersedes,
                relation="SUPERSEDES",
                weight=1.0,
                valid_from=now,
                is_current=True,
            )
            self.add_edge(sup_edge)
            edges_added.append(sup_edge.to_dict())

        targets = list(relates_to or [])
        if not targets and "concept:tri-graph" in self.nodes and resolved_id != "concept:tri-graph":
            targets.append("concept:tri-graph")

        for tgt in targets:
            if tgt in self.nodes and tgt != resolved_id:
                rel_edge = MemoryEdge(
                    source=resolved_id,
                    target=tgt,
                    relation=relation,
                    weight=1.0,
                    valid_from=now,
                    is_current=True,
                )
                self.add_edge(rel_edge)
                edges_added.append(rel_edge.to_dict())

        reflection_res: Dict[str, Any] = {"insights_generated": 0, "insights": []}
        if run_reflection:
            from hath0r_engine.memory.reflection import ReflectionEngine

            reflection_res = ReflectionEngine().consolidate_sleep_cycle(self)

        return {
            "node": node.to_dict(),
            "edges_added": edges_added,
            "reflection": reflection_res,
        }

    def verify_compounded(
        self,
        seed_ids: Optional[Set[str]] = None,
        since: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Verify that MemoryGraph contains compounded task knowledge beyond static seed nodes."""
        ignored_seeds = seed_ids if seed_ids is not None else self.CANONICAL_SEED_NODE_IDS
        compounded_nodes: List[MemoryNode] = []
        for nid, node in self.nodes.items():
            if nid in ignored_seeds:
                continue
            if since and node.updated_at < since:
                continue
            compounded_nodes.append(node)

        compounded_nodes.sort(key=lambda n: n.updated_at, reverse=True)
        latest = compounded_nodes[0].to_dict() if compounded_nodes else None
        return {
            "compounded": len(compounded_nodes) > 0,
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "compounded_nodes_count": len(compounded_nodes),
            "latest_node": latest,
        }

    @classmethod
    def ensure_repo_memory(cls, repo_root: Path | str) -> MemoryGraph:
        """Ensure .hath0r/memory/graph.json exists for a repository and seed initial repo memory."""
        root = Path(repo_root).resolve()
        mem_dir = root / ".hath0r" / "memory"
        mem_dir.mkdir(parents=True, exist_ok=True)
        graph_file = mem_dir / "graph.json"
        core_file = mem_dir / "core_rules.md"
        arch_file = mem_dir / "architecture.md"

        if not core_file.is_file():
            core_file.write_text(
                "# Core Hath0r Rules\n"
                "1. CLI-First (CR-CLI-ENTRY-001): Always start with the CLI capabilities before improvising.\n"
                "2. Memory Compounding (CR-MEMORY-COMPOUND-001): Every task must compound knowledge into .hath0r/memory/graph.json prior to announcing complete.\n"
                "3. Hyper-Context (CR-AGENTGRAPH-001): Query AgentGraph and MemoryGraph rather than loading unbounded files.\n"
                "4. Promotion Path (CR-BAI-001): local -> development -> testing -> staging -> master.\n",
                encoding="utf-8",
            )
        if not arch_file.is_file():
            arch_file.write_text(
                f"# Canonical Architecture — {root.name}\n"
                "Agents orienting to this repository MUST read and compound into `.hath0r/memory/graph.json` "
                "prior to completing any task.\n",
                encoding="utf-8",
            )

        if graph_file.is_file():
            try:
                graph = cls.load_from_file(graph_file)
            except Exception:
                graph = cls(graph_id=f"memory-{root.name}")
        else:
            graph = cls(graph_id=f"memory-{root.name}")

        # Ensure canonical seed rules & concepts exist
        if "rule:cr-cli-entry-001" not in graph.nodes:
            graph.add_node(
                MemoryNode(
                    id="rule:cr-cli-entry-001",
                    type="rule",
                    label="Start with CLI Rule",
                    content="Always start with hath0r operator CLI before inventing ad-hoc actions.",
                    importance=1.0,
                    tags=["rule", "governance", "cli"],
                )
            )
        if "rule:cr-bai-001" not in graph.nodes:
            graph.add_node(
                MemoryNode(
                    id="rule:cr-bai-001",
                    type="rule",
                    label="Promotion Path Policy",
                    content="Promotion order: local -> development -> testing -> staging -> master.",
                    importance=1.0,
                    tags=["rule", "governance", "ci"],
                )
            )
        if "rule:cr-memory-compound-001" not in graph.nodes:
            graph.add_node(
                MemoryNode(
                    id="rule:cr-memory-compound-001",
                    type="rule",
                    label="Mandatory MemoryGraph Compounding Rule",
                    content="Every project repo must have .hath0r/memory/graph.json and every task must compound knowledge prior to announcing complete.",
                    importance=1.0,
                    tags=["rule", "governance", "memorygraph", "cr-memory-compound-001"],
                )
            )
        if "concept:tri-graph" not in graph.nodes:
            graph.add_node(
                MemoryNode(
                    id="concept:tri-graph",
                    type="concept",
                    label="Quad-Graph Cognitive Substrate",
                    content="Unified cognitive graph architecture: KnowledgeGraph, ContextGraph, MemoryGraph, RulesGraph.",
                    importance=0.95,
                    tags=["architecture", "substrate", "tri-graph", "agentgraph"],
                )
            )

        graph.add_edge(MemoryEdge(source="rule:cr-cli-entry-001", target="concept:tri-graph", relation="ENFORCES"))
        graph.add_edge(
            MemoryEdge(source="rule:cr-memory-compound-001", target="concept:tri-graph", relation="ENFORCES")
        )

        # Ensure repository-specific orientation memory node exists
        repo_node_id = f"fact:repo-{root.name.lower().replace(' ', '-')}-orientation"
        if repo_node_id not in graph.nodes:
            summary = f"Repository '{root.name}' at {root.name} initialized with canonical .hath0r/memory/graph.json."
            for doc_candidate in (root / "README.md", root / "AGENTS.md"):
                if doc_candidate.is_file():
                    try:
                        lines = [
                            ln.strip()
                            for ln in doc_candidate.read_text(encoding="utf-8", errors="ignore").splitlines()
                            if ln.strip() and not ln.strip().startswith("#")
                        ]
                        if lines:
                            summary = f"{root.name}: {' '.join(lines[:3])[:400]}"
                            break
                    except Exception:
                        pass
            graph.compound_knowledge(
                node_id=repo_node_id,
                node_type="fact",
                label=f"{root.name} Repository Orientation Memory",
                content=summary,
                importance=0.85,
                tags=["orientation", "repository", root.name.lower().replace(" ", "-")],
                relates_to=["concept:tri-graph", "rule:cr-memory-compound-001"],
                relation="RELATES_TO",
                run_reflection=False,
            )

        graph.save_to_file(graph_file)
        return graph

    def _touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Serialize memory graph to dictionary."""
        return {
            "schema_version": self.schema_version,
            "graph_id": self.graph_id,
            "updated_at": self.updated_at,
            "metadata": self.metadata,
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges],
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize memory graph to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    def save_to_file(self, file_path: Path | str) -> None:
        """Save graph to JSON file."""
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.to_json(), encoding="utf-8")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MemoryGraph:
        """Construct MemoryGraph instance from dictionary."""
        graph = cls(graph_id=data.get("graph_id", "default-memory-space"))
        graph.schema_version = data.get("schema_version", "1.0.0")
        graph.updated_at = data.get("updated_at", datetime.now(timezone.utc).isoformat())
        graph.metadata = data.get("metadata", {})

        for node_dict in data.get("nodes", []):
            node = MemoryNode.from_dict(node_dict)
            graph.nodes[node.id] = node

        for edge_dict in data.get("edges", []):
            edge = MemoryEdge.from_dict(edge_dict)
            graph.edges.append(edge)

        return graph

    @classmethod
    def load_from_file(cls, file_path: Path | str) -> MemoryGraph:
        """Load graph from JSON file."""
        path = Path(file_path)
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls.from_dict(data)

    def to_sqlite(self, db_path_or_store: Any) -> Any:
        """Persist MemoryGraph snapshot into SQLiteGraphStore."""
        from hath0r_engine.graph.sqlite_graph import SQLiteGraphStore

        store = (
            db_path_or_store if isinstance(db_path_or_store, SQLiteGraphStore) else SQLiteGraphStore(db_path_or_store)
        )
        for node in self.nodes.values():
            store.upsert_node(
                node_id=node.id,
                node_type=node.type,
                title=node.label,
                graph_type="memory",
                content=node.content,
                importance=node.importance,
                tags=node.tags,
                properties=node.metadata,
                created_at=node.created_at,
                updated_at=node.updated_at,
            )
        for edge in self.edges:
            store.add_edge(
                source=edge.source,
                target=edge.target,
                relation=edge.relation,
                graph_type="memory",
                weight=edge.weight,
                valid_from=edge.valid_from,
                valid_to=edge.valid_to,
                is_current=edge.is_current,
                metadata=edge.metadata,
            )
        return store

    @classmethod
    def load_from_sqlite(cls, db_path_or_store: Any, graph_id: str = "default-memory-space") -> MemoryGraph:
        """Load MemoryGraph snapshot from SQLiteGraphStore."""
        from hath0r_engine.graph.sqlite_graph import SQLiteGraphStore

        store = (
            db_path_or_store if isinstance(db_path_or_store, SQLiteGraphStore) else SQLiteGraphStore(db_path_or_store)
        )
        graph = cls(graph_id=graph_id)
        cursor = store._conn.execute("SELECT * FROM nodes WHERE graph_type = 'memory'")
        for row in cursor.fetchall():
            node_dict = store._row_to_node_dict(row)
            node = MemoryNode(
                id=node_dict["id"],
                type=node_dict["type"],
                label=node_dict["title"],
                content=node_dict["content"],
                importance=node_dict["importance"],
                tags=node_dict["tags"],
                created_at=node_dict["created_at"],
                updated_at=node_dict["updated_at"],
                metadata=node_dict["properties"],
            )
            graph.nodes[node.id] = node

        edges = store.get_edges(graph_type="memory")
        for e in edges:
            graph.edges.append(
                MemoryEdge(
                    source=e["source"],
                    target=e["target"],
                    relation=e["relation"],
                    weight=e["weight"],
                    valid_from=e.get("valid_from"),
                    valid_to=e.get("valid_to"),
                    is_current=e.get("is_current", True),
                    metadata=e["metadata"],
                )
            )
        return graph
