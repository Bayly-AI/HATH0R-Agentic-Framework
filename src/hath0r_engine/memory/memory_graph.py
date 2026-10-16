"""MemoryGraph: Semantic and Episodic Memory Graph engine for Hath0r.

Represents working memory, rules, architectural decisions, and episodic learnings
as an interconnected semantic network for autonomous agents.
"""

from __future__ import annotations

import hashlib
import json
import os
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


class MemoryHashConflictError(RuntimeError):
    """Raised when an explicit SHA-256 CAS check or concurrent incompatible write conflict occurs."""


def compute_sha256_bytes(data: bytes) -> str:
    """Compute canonical sha256:<hex> digest for raw bytes."""
    return f"sha256:{hashlib.sha256(data).hexdigest()}"


def compute_file_sha256(file_path: Path | str) -> Optional[str]:
    """Compute canonical sha256:<hex> digest for an on-disk file, or None if missing."""
    path = Path(file_path)
    if not path.is_file():
        return None
    return compute_sha256_bytes(path.read_bytes())


def atomic_write_text(file_path: Path | str, text: str) -> str:
    """Write text atomically via a temporary sibling file and os.replace, returning sha256:<hex>."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = text.encode("utf-8")
    tmp_path = path.parent / f".{path.name}.tmp.{uuid.uuid4().hex[:8]}"
    tmp_path.write_bytes(raw)
    os.replace(tmp_path, path)
    return compute_sha256_bytes(raw)


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


@dataclass
class MicroMemoryEntry:
    """A single compact micro-memory observation or decision recorded during an active session."""

    timestamp: str
    kind: str  # observation, decision, tool, hypothesis, blocker, milestone, compound
    summary: str
    tags: List[str] = field(default_factory=list)
    node_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MicroMemoryEntry:
        return cls(
            timestamp=data.get("timestamp", datetime.now(timezone.utc).isoformat()),
            kind=data.get("kind", "observation"),
            summary=str(data.get("summary", ""))[:240],
            tags=list(data.get("tags", [])),
            node_id=data.get("node_id"),
        )


@dataclass
class MicroMemorySession:
    """Compact (<2KB) Micro Memory Session capsule read and written on every session."""

    MAX_CAPSULE_BYTES: int = 2048
    MAX_MICRO_ENTRIES: int = 8
    MAX_RECALLED_NODES: int = 5

    session_id: str = field(
        default_factory=lambda: f"sess-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
    )
    schema_version: str = "hath0r.micro_session/1"
    prior_session_id: Optional[str] = None
    repo_name: str = ""
    status: str = "active"  # active | flushed
    started_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    ended_at: Optional[str] = None
    read_count: int = 0
    write_count: int = 0
    revision: int = 1
    content_hash: str = ""
    base_graph_hash: Optional[str] = None
    last_read_at: Optional[str] = None
    last_write_at: Optional[str] = None
    active_focus: str = ""
    prior_summary: str = ""
    recalled_nodes: List[Dict[str, Any]] = field(default_factory=list)
    micro_entries: List[Dict[str, Any]] = field(default_factory=list)
    next_steps: List[str] = field(default_factory=list)
    compounded_node_ids: List[str] = field(default_factory=list)
    _loaded_file_hash: Optional[str] = field(default=None, init=False, repr=False, compare=False)

    def compute_content_hash(self) -> str:
        """Compute deterministic SHA-256 digest of the session capsule (excluding content_hash itself)."""
        payload = self.to_dict()
        payload["content_hash"] = ""
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        return compute_sha256_bytes(canonical)

    def enforce_budget(self) -> None:
        """Guarantee serialized capsule stays strictly under MAX_CAPSULE_BYTES (<2KB)."""
        self.active_focus = self.active_focus[:160]
        self.prior_summary = self.prior_summary[:200]
        self.recalled_nodes = self.recalled_nodes[: self.MAX_RECALLED_NODES]
        for rnode in self.recalled_nodes:
            if "snippet" in rnode and isinstance(rnode["snippet"], str):
                rnode["snippet"] = rnode["snippet"][:90]
            if "label" in rnode and isinstance(rnode["label"], str):
                rnode["label"] = rnode["label"][:60]
        self.next_steps = [str(s)[:100] for s in self.next_steps[:4]]
        self.compounded_node_ids = list(dict.fromkeys(self.compounded_node_ids))[-6:]
        while len(self.micro_entries) > self.MAX_MICRO_ENTRIES:
            evicted = self.micro_entries.pop(0)
            ev_sum = str(evicted.get("summary", ""))[:60]
            if ev_sum:
                self.prior_summary = f"{self.prior_summary}; {ev_sum}".strip("; ")[-200:]

        self.content_hash = self.compute_content_hash()
        # Hard byte-budget enforcement (<2KB)
        while len(self.to_json(indent=2).encode("utf-8")) > self.MAX_CAPSULE_BYTES:
            if len(self.recalled_nodes) > 1:
                self.recalled_nodes.pop()
            elif len(self.micro_entries) > 1:
                evicted = self.micro_entries.pop(0)
                ev_sum = str(evicted.get("summary", ""))[:40]
                if ev_sum:
                    self.prior_summary = f"{self.prior_summary}; {ev_sum}".strip("; ")[-120:]
            elif len(self.prior_summary) > 60:
                self.prior_summary = self.prior_summary[-60:]
            elif len(self.recalled_nodes) > 0:
                self.recalled_nodes.pop()
            else:
                break
            self.content_hash = self.compute_content_hash()

    def byte_size(self) -> int:
        """Return UTF-8 byte length of the formatted capsule JSON."""
        return len(self.to_json(indent=2).encode("utf-8"))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "session_id": self.session_id,
            "prior_session_id": self.prior_session_id,
            "repo_name": self.repo_name,
            "status": self.status,
            "started_at": self.started_at,
            "updated_at": self.updated_at,
            "ended_at": self.ended_at,
            "read_count": self.read_count,
            "write_count": self.write_count,
            "revision": self.revision,
            "content_hash": self.content_hash,
            "base_graph_hash": self.base_graph_hash,
            "last_read_at": self.last_read_at,
            "last_write_at": self.last_write_at,
            "active_focus": self.active_focus,
            "prior_summary": self.prior_summary,
            "recalled_nodes": self.recalled_nodes,
            "micro_entries": self.micro_entries,
            "next_steps": self.next_steps,
            "compounded_node_ids": self.compounded_node_ids,
        }

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MicroMemorySession:
        sess = cls(
            session_id=data.get("session_id", f"sess-{uuid.uuid4().hex[:8]}"),
            schema_version=data.get("schema_version", "hath0r.micro_session/1"),
            prior_session_id=data.get("prior_session_id"),
            repo_name=data.get("repo_name", ""),
            status=data.get("status", "active"),
            started_at=data.get("started_at", datetime.now(timezone.utc).isoformat()),
            updated_at=data.get("updated_at", datetime.now(timezone.utc).isoformat()),
            ended_at=data.get("ended_at"),
            read_count=int(data.get("read_count", 0)),
            write_count=int(data.get("write_count", 0)),
            revision=int(data.get("revision", 1)),
            content_hash=str(data.get("content_hash", "")),
            base_graph_hash=data.get("base_graph_hash"),
            last_read_at=data.get("last_read_at"),
            last_write_at=data.get("last_write_at"),
            active_focus=data.get("active_focus", ""),
            prior_summary=data.get("prior_summary", ""),
            recalled_nodes=list(data.get("recalled_nodes", [])),
            micro_entries=list(data.get("micro_entries", [])),
            next_steps=list(data.get("next_steps", [])),
            compounded_node_ids=list(data.get("compounded_node_ids", [])),
        )
        if not sess.content_hash:
            sess.content_hash = sess.compute_content_hash()
        return sess

    def merge_from(self, other: MicroMemorySession) -> None:
        """Deterministically auto-merge concurrent non-conflicting micro-session entries."""
        if other.session_id != self.session_id:
            return
        seen_keys = {(e.get("timestamp"), e.get("summary")) for e in self.micro_entries}
        merged_entries = list(other.micro_entries)
        for entry in self.micro_entries:
            key = (entry.get("timestamp"), entry.get("summary"))
            if key not in {(e.get("timestamp"), e.get("summary")) for e in merged_entries}:
                merged_entries.append(entry)
            seen_keys.add(key)
        merged_entries.sort(key=lambda e: str(e.get("timestamp", "")))
        self.micro_entries = merged_entries
        self.compounded_node_ids = list(dict.fromkeys(other.compounded_node_ids + self.compounded_node_ids))
        self.read_count = max(self.read_count, other.read_count)
        self.write_count = max(self.write_count, other.write_count, len(self.micro_entries))
        self.revision = max(self.revision, other.revision) + 1

    def save_to_file(
        self,
        file_path: Path | str,
        expected_hash: Optional[str] = None,
        auto_merge: bool = True,
    ) -> str:
        path = Path(file_path)
        if path.is_file():
            disk_file_hash = compute_file_sha256(path)
            try:
                disk_sess = self.load_from_file(path)
            except Exception:
                disk_sess = None
            if expected_hash is not None:
                disk_content_hash = disk_sess.content_hash if disk_sess else None
                if expected_hash not in (disk_file_hash, disk_content_hash):
                    raise MemoryHashConflictError(
                        f"Session hash conflict on {path}: expected {expected_hash}, "
                        f"found file={disk_file_hash} content={disk_content_hash}"
                    )
            if (
                auto_merge
                and disk_sess is not None
                and self._loaded_file_hash is not None
                and disk_file_hash != self._loaded_file_hash
            ):
                self.merge_from(disk_sess)
            elif disk_sess is not None and disk_sess.session_id == self.session_id:
                self.revision = max(self.revision, disk_sess.revision + 1)

        self.enforce_budget()
        self.content_hash = self.compute_content_hash()
        file_hash = atomic_write_text(path, self.to_json(indent=2))
        self._loaded_file_hash = file_hash
        return file_hash

    @classmethod
    def load_from_file(cls, file_path: Path | str) -> MicroMemorySession:
        path = Path(file_path)
        raw = path.read_bytes()
        data = json.loads(raw.decode("utf-8"))
        sess = cls.from_dict(data)
        sess._loaded_file_hash = compute_sha256_bytes(raw)
        return sess

    def to_memory_node(self) -> MemoryNode:
        """Convert this MicroMemorySession into a MemoryNode for MemoryGraph persistence."""
        entry_summaries = "; ".join(str(e.get("summary", "")) for e in self.micro_entries[-4:] if e.get("summary"))
        content = (
            f"Micro Session {self.session_id} [{self.status}] | Focus: {self.active_focus or 'General'} | "
            f"Reads: {self.read_count}, Writes: {self.write_count} | "
            f"Entries: {entry_summaries or self.prior_summary or 'Initialized'}"
        )
        return MemoryNode(
            id=f"session:{self.session_id}",
            type="session",
            label=f"Micro Session {self.session_id}",
            content=content[:600],
            importance=0.75,
            tags=["session", "micro-session", self.status],
            valid_from=self.started_at,
            valid_to=self.ended_at,
            is_current=True,
            created_at=self.started_at,
            updated_at=self.updated_at,
            metadata={
                "session_id": self.session_id,
                "prior_session_id": self.prior_session_id,
                "read_count": self.read_count,
                "write_count": self.write_count,
                "revision": self.revision,
                "content_hash": self.content_hash,
                "status": self.status,
                "byte_size": self.byte_size(),
            },
        )


class MemoryGraph:
    """Manages the semantic working memory graph for Hath0r agents."""

    def __init__(self, graph_id: str = "default-memory-space"):
        self.schema_version = "1.0.0"
        self.graph_id = graph_id
        self.revision: int = 1
        self.content_hash: str = ""
        self.updated_at = datetime.now(timezone.utc).isoformat()
        self.metadata: Dict[str, Any] = {}
        self.nodes: Dict[str, MemoryNode] = {}
        self.edges: List[MemoryEdge] = []
        self._loaded_file_hash: Optional[str] = None
        self._loaded_node_hashes: Dict[str, str] = {}

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

    CANONICAL_GRAPH_PATHS: tuple[str, ...] = (
        ".hath0r/memory/graph.json",
        ".hath0r/memory/hashes.json",
        ".hath0r/memory/sessions/current.json",
        ".hath0r/agentgraph/snapshot.json",
        ".hath0r/graphs/default.json",
        ".hath0r/state/cache/knowledge.json",
        ".hath0r/state/context/session_init.json",
    )

    CANONICAL_GITIGNORE_NEGATIONS: tuple[str, ...] = (
        "!.hath0r/",
        "!.hath0r/memory/",
        "!.hath0r/memory/**",
        "!.hath0r/memory/sessions/",
        "!.hath0r/memory/sessions/**",
        "!.hath0r/agentgraph/",
        "!.hath0r/agentgraph/**",
        "!.hath0r/graphs/",
        "!.hath0r/graphs/**",
        "!.hath0r/state/",
        "!.hath0r/state/cache/",
        "!.hath0r/state/cache/**",
        "!.hath0r/state/context/",
        "!.hath0r/state/context/**",
    )

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
        source_files: Optional[List[str]] = None,
        repo_root: Optional[Path | str] = None,
        run_reflection: bool = True,
    ) -> Dict[str, Any]:
        """Compound a structured knowledge node and relational edges into MemoryGraph."""
        import re

        now = datetime.now(timezone.utc).isoformat()
        slug = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")[:48] or "task"
        resolved_id = node_id or f"{node_type}:{slug}"
        resolved_tags = list(dict.fromkeys((tags or []) + [node_type, "compounded"]))

        resolved_meta = dict(metadata or {})
        if source_files:
            src_hashes: Dict[str, str] = dict(resolved_meta.get("source_files") or {})
            base_dir = Path(repo_root).resolve() if repo_root is not None else Path.cwd().resolve()
            for sf in source_files:
                if not sf:
                    continue
                sf_path = Path(sf)
                abs_sf = sf_path.resolve() if sf_path.is_absolute() else (base_dir / sf_path).resolve()
                try:
                    rel_key = str(abs_sf.relative_to(base_dir))
                except ValueError:
                    rel_key = str(sf)
                fhash = compute_file_sha256(abs_sf)
                if fhash:
                    src_hashes[rel_key] = fhash
            if src_hashes:
                resolved_meta["source_files"] = src_hashes

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
            metadata=resolved_meta,
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
        repo_root: Optional[Path | str] = None,
        require_session: bool = False,
        require_hashes: bool = False,
    ) -> Dict[str, Any]:
        """Verify that MemoryGraph contains compounded task knowledge, micro session R/W, and up-to-date file hashes."""
        ignored_seeds = seed_ids if seed_ids is not None else self.CANONICAL_SEED_NODE_IDS
        compounded_nodes: List[MemoryNode] = []
        for nid, node in self.nodes.items():
            if nid in ignored_seeds or node.type == "session":
                continue
            if since and node.updated_at < since:
                continue
            compounded_nodes.append(node)

        compounded_nodes.sort(key=lambda n: n.updated_at, reverse=True)
        latest = compounded_nodes[0].to_dict() if compounded_nodes else None

        session_info: Optional[Dict[str, Any]] = None
        session_ok = True
        hashes_info: Optional[Dict[str, Any]] = None
        hashes_ok = True
        graphs_not_ignored = True
        if repo_root is not None:
            session_info = self.get_micro_session_status(repo_root)
            if require_session:
                session_ok = bool(session_info.get("read_verified") and session_info.get("write_verified"))
            hashes_info = self.verify_repo_hashes(repo_root)
            graphs_not_ignored = bool(hashes_info.get("graphs_not_ignored", True))
            if require_hashes:
                hashes_ok = bool(hashes_info.get("verified")) and graphs_not_ignored

        compounded_ok = len(compounded_nodes) > 0 and session_ok and hashes_ok and graphs_not_ignored
        return {
            "compounded": compounded_ok,
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "compounded_nodes_count": len(compounded_nodes),
            "latest_node": latest,
            "session": session_info,
            "hashes": hashes_info,
            "hashes_verified": hashes_ok,
            "graphs_not_ignored": graphs_not_ignored,
        }

    def _recall_top_nodes_compact(self, query: str = "", top_k: int = 5) -> List[Dict[str, Any]]:
        """Return compact summaries of top-ranked active memory nodes for micro-session recall."""
        matches: List[MemoryNode] = []
        if query:
            try:
                from hath0r_engine.memory.reflection import ReflectionEngine

                ranked = ReflectionEngine().rank_memories(
                    self,
                    query=query,
                    top_k=top_k,
                    node_types=["episode", "decision", "insight", "fact", "concept", "rule"],
                    only_current=True,
                )
                matches = [n for n, _ in ranked if n.type != "session"][:top_k]
            except Exception:
                matches = []

        if not matches:
            candidates = [
                n for n in self.nodes.values()
                if n.is_current and n.id not in self.CANONICAL_SEED_NODE_IDS and n.type != "session"
            ]
            if not candidates:
                candidates = [n for n in self.nodes.values() if n.is_current and n.type != "session"]
            candidates.sort(key=lambda n: (n.importance, n.updated_at), reverse=True)
            matches = candidates[:top_k]

        return [
            {
                "id": n.id,
                "type": n.type,
                "label": n.label[:60],
                "snippet": n.content[:90],
            }
            for n in matches
        ]

    def _sync_session_node(self, session: MicroMemorySession) -> None:
        """Upsert session:<session_id> node and PRECEDES / DERIVES_FROM edges into MemoryGraph."""
        now = datetime.now(timezone.utc).isoformat()
        snode = session.to_memory_node()
        self.add_node(snode)

        if session.prior_session_id and session.prior_session_id != session.session_id:
            prior_nid = f"session:{session.prior_session_id}"
            if prior_nid in self.nodes:
                self.add_edge(
                    MemoryEdge(
                        source=prior_nid,
                        target=snode.id,
                        relation="PRECEDES",
                        weight=1.0,
                        valid_from=now,
                        is_current=True,
                    )
                )

        if "concept:tri-graph" in self.nodes:
            self.add_edge(
                MemoryEdge(
                    source=snode.id,
                    target="concept:tri-graph",
                    relation="RELATES_TO",
                    weight=0.8,
                    valid_from=now,
                    is_current=True,
                )
            )

        for cid in session.compounded_node_ids:
            if cid in self.nodes and cid != snode.id:
                self.add_edge(
                    MemoryEdge(
                        source=cid,
                        target=snode.id,
                        relation="DERIVES_FROM",
                        weight=1.0,
                        valid_from=now,
                        is_current=True,
                    )
                )

    @classmethod
    def start_micro_session(
        cls,
        repo_root: Path | str,
        session_id: Optional[str] = None,
        focus: Optional[str] = None,
        top_k: int = 5,
    ) -> MicroMemorySession:
        """Start a new Micro Memory Session (.hath0r/memory/sessions/current.json), reading prior session & graph."""
        root = Path(repo_root).resolve()
        mem_dir = root / ".hath0r" / "memory"
        sessions_dir = mem_dir / "sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)
        graph_file = mem_dir / "graph.json"

        graph = cls.load_from_file(graph_file) if graph_file.is_file() else cls(graph_id=f"memory-{root.name}")

        prior_session_id: Optional[str] = None
        prior_summary = ""
        for candidate in (sessions_dir / "latest.json", sessions_dir / "current.json"):
            if candidate.is_file():
                try:
                    prev = MicroMemorySession.load_from_file(candidate)
                    prior_session_id = prev.session_id
                    last_entries = [str(e.get("summary", "")) for e in prev.micro_entries[-2:] if e.get("summary")]
                    prior_summary = "; ".join(last_entries) or prev.active_focus or prev.prior_summary
                    break
                except Exception:
                    pass

        now = datetime.now(timezone.utc).isoformat()
        resolved_sid = session_id or f"sess-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"
        recalled = graph._recall_top_nodes_compact(query=focus or "", top_k=top_k)

        session = MicroMemorySession(
            session_id=resolved_sid,
            prior_session_id=prior_session_id if prior_session_id != resolved_sid else None,
            repo_name=root.name,
            status="active",
            started_at=now,
            updated_at=now,
            read_count=1,
            write_count=0,
            revision=1,
            base_graph_hash=graph.content_hash or graph.compute_content_hash(),
            last_read_at=now,
            active_focus=focus or f"Active working session in {root.name}",
            prior_summary=prior_summary[:200],
            recalled_nodes=recalled,
        )

        if focus:
            entry = MicroMemoryEntry(
                timestamp=now,
                kind="observation",
                summary=f"Started session focus: {focus}"[:240],
                tags=["session-start"],
            )
            session.micro_entries.append(entry.to_dict())
            session.write_count = 1
            session.last_write_at = now

        session.save_to_file(sessions_dir / "current.json", auto_merge=False)
        session.save_to_file(sessions_dir / "latest.json", auto_merge=False)
        session.save_to_file(sessions_dir / f"{session.session_id}.json", auto_merge=False)

        graph._sync_session_node(session)
        graph.save_to_file(graph_file)
        return session

    @classmethod
    def read_micro_session(
        cls,
        repo_root: Path | str,
        focus: Optional[str] = None,
        top_k: int = 5,
    ) -> MicroMemorySession:
        """Read active Micro Memory Session (.hath0r/memory/sessions/current.json), auto-starting if absent."""
        root = Path(repo_root).resolve()
        mem_dir = root / ".hath0r" / "memory"
        sessions_dir = mem_dir / "sessions"
        current_file = sessions_dir / "current.json"
        graph_file = mem_dir / "graph.json"

        if not current_file.is_file():
            return cls.start_micro_session(root, focus=focus, top_k=top_k)

        try:
            session = MicroMemorySession.load_from_file(current_file)
        except Exception:
            return cls.start_micro_session(root, focus=focus, top_k=top_k)

        graph = cls.load_from_file(graph_file) if graph_file.is_file() else cls(graph_id=f"memory-{root.name}")
        now = datetime.now(timezone.utc).isoformat()
        if focus:
            session.active_focus = focus[:160]
        session.recalled_nodes = graph._recall_top_nodes_compact(query=focus or session.active_focus, top_k=top_k)
        session.base_graph_hash = graph.content_hash or graph.compute_content_hash()
        session.read_count += 1
        session.last_read_at = now
        session.updated_at = now

        session.save_to_file(current_file)
        session.save_to_file(sessions_dir / "latest.json", auto_merge=False)
        session.save_to_file(sessions_dir / f"{session.session_id}.json", auto_merge=False)

        graph._sync_session_node(session)
        graph.save_to_file(graph_file)
        return session

    @classmethod
    def write_micro_session(
        cls,
        repo_root: Path | str,
        summary: str,
        kind: str = "observation",
        tags: Optional[List[str]] = None,
        active_focus: Optional[str] = None,
        next_steps: Optional[List[str]] = None,
        linked_node_id: Optional[str] = None,
        expected_hash: Optional[str] = None,
    ) -> MicroMemorySession:
        """Write a compact micro-memory entry into .hath0r/memory/sessions/current.json and sync graph.json."""
        root = Path(repo_root).resolve()
        mem_dir = root / ".hath0r" / "memory"
        sessions_dir = mem_dir / "sessions"
        current_file = sessions_dir / "current.json"
        graph_file = mem_dir / "graph.json"

        if not current_file.is_file():
            session = cls.start_micro_session(root, focus=active_focus or summary[:120])
        else:
            try:
                session = MicroMemorySession.load_from_file(current_file)
            except Exception:
                session = cls.start_micro_session(root, focus=active_focus or summary[:120])

        now = datetime.now(timezone.utc).isoformat()
        if session.read_count < 1:
            session.read_count = 1
            session.last_read_at = now

        entry = MicroMemoryEntry(
            timestamp=now,
            kind=kind,
            summary=summary[:240],
            tags=list(tags or []),
            node_id=linked_node_id,
        )
        session.micro_entries.append(entry.to_dict())
        session.write_count += 1
        session.last_write_at = now
        session.updated_at = now
        if active_focus:
            session.active_focus = active_focus[:160]
        if next_steps is not None:
            session.next_steps = [str(s)[:100] for s in next_steps[:4]]
        if linked_node_id and linked_node_id not in session.compounded_node_ids:
            session.compounded_node_ids.append(linked_node_id)

        session.save_to_file(current_file, expected_hash=expected_hash)
        session.save_to_file(sessions_dir / "latest.json", auto_merge=False)
        session.save_to_file(sessions_dir / f"{session.session_id}.json", auto_merge=False)

        graph = cls.load_from_file(graph_file) if graph_file.is_file() else cls(graph_id=f"memory-{root.name}")
        graph._sync_session_node(session)
        graph.save_to_file(graph_file)
        return session

    @classmethod
    def end_micro_session(
        cls,
        repo_root: Path | str,
        summary: Optional[str] = None,
        next_steps: Optional[List[str]] = None,
    ) -> MicroMemorySession:
        """Flush and finalize the active Micro Memory Session into .hath0r/memory/sessions/ and graph.json."""
        root = Path(repo_root).resolve()
        mem_dir = root / ".hath0r" / "memory"
        sessions_dir = mem_dir / "sessions"
        current_file = sessions_dir / "current.json"
        graph_file = mem_dir / "graph.json"

        if not current_file.is_file():
            session = cls.start_micro_session(root, focus=summary or f"Session completed in {root.name}")
        else:
            try:
                session = MicroMemorySession.load_from_file(current_file)
            except Exception:
                session = cls.start_micro_session(root, focus=summary or f"Session completed in {root.name}")

        now = datetime.now(timezone.utc).isoformat()
        if session.read_count < 1:
            session.read_count = 1
            session.last_read_at = now

        if summary:
            entry = MicroMemoryEntry(
                timestamp=now,
                kind="milestone",
                summary=summary[:240],
                tags=["session-end"],
            )
            session.micro_entries.append(entry.to_dict())
            session.write_count += 1
            session.last_write_at = now
        elif session.write_count < 1:
            entry = MicroMemoryEntry(
                timestamp=now,
                kind="milestone",
                summary=f"Completed micro memory session {session.session_id}",
                tags=["session-end"],
            )
            session.micro_entries.append(entry.to_dict())
            session.write_count = 1
            session.last_write_at = now

        if next_steps is not None:
            session.next_steps = [str(s)[:100] for s in next_steps[:4]]

        session.status = "flushed"
        session.ended_at = now
        session.updated_at = now

        session.save_to_file(current_file)
        session.save_to_file(sessions_dir / "latest.json", auto_merge=False)
        session.save_to_file(sessions_dir / f"{session.session_id}.json", auto_merge=False)

        graph = cls.load_from_file(graph_file) if graph_file.is_file() else cls(graph_id=f"memory-{root.name}")
        graph._sync_session_node(session)
        graph.save_to_file(graph_file)
        return session

    @classmethod
    def get_micro_session_status(cls, repo_root: Path | str) -> Dict[str, Any]:
        """Inspect the repository's micro memory session read/write verification status."""
        root = Path(repo_root).resolve()
        sessions_dir = root / ".hath0r" / "memory" / "sessions"
        current_file = sessions_dir / "current.json"
        latest_file = sessions_dir / "latest.json"
        target_file = current_file if current_file.is_file() else latest_file

        if not target_file.is_file():
            return {
                "exists": False,
                "session_id": None,
                "read_count": 0,
                "write_count": 0,
                "revision": 0,
                "content_hash": None,
                "read_verified": False,
                "write_verified": False,
                "byte_size": 0,
                "file": str(current_file),
            }

        try:
            session = MicroMemorySession.load_from_file(target_file)
            return {
                "exists": True,
                "session_id": session.session_id,
                "prior_session_id": session.prior_session_id,
                "status": session.status,
                "read_count": session.read_count,
                "write_count": session.write_count,
                "revision": session.revision,
                "content_hash": session.content_hash,
                "file_hash": compute_file_sha256(target_file),
                "read_verified": session.read_count >= 1,
                "write_verified": session.write_count >= 1,
                "active_focus": session.active_focus,
                "entries_count": len(session.micro_entries),
                "recalled_nodes_count": len(session.recalled_nodes),
                "byte_size": session.byte_size(),
                "file": str(target_file),
                "session": session.to_dict(),
            }
        except Exception as exc:
            return {
                "exists": False,
                "session_id": None,
                "read_count": 0,
                "write_count": 0,
                "revision": 0,
                "content_hash": None,
                "read_verified": False,
                "write_verified": False,
                "byte_size": 0,
                "file": str(target_file),
                "error": str(exc),
            }

    @classmethod
    def ensure_gitignore_unignores_graphs(
        cls,
        repo_root: Path | str,
        dry_run: bool = False,
        create_if_missing: bool = False,
    ) -> Dict[str, Any]:
        """Ensure .gitignore never ignores .hath0r/memory, .hath0r/agentgraph, .hath0r/graphs, .hath0r/state/cache, or .hath0r/state/context."""
        root = Path(repo_root).resolve()
        gitignore_file = root / ".gitignore"
        has_git = (root / ".git").exists()

        if not gitignore_file.is_file() and not create_if_missing and not has_git:
            return {
                "updated": False,
                "gitignore_file": str(gitignore_file),
                "rewritten_rules": [],
                "removed_rules": [],
                "appended_negations": [],
            }

        raw_text = gitignore_file.read_text(encoding="utf-8", errors="ignore") if gitignore_file.is_file() else ""
        lines = raw_text.splitlines()

        forbidden_exact = {
            ".hath0r/memory",
            ".hath0r/memory/",
            ".hath0r/memory/*",
            ".hath0r/memory/**",
            ".hath0r/memory/sessions",
            ".hath0r/memory/sessions/",
            ".hath0r/memory/sessions/*",
            ".hath0r/memory/sessions/**",
            ".hath0r/memory/graph.json",
            ".hath0r/memory/hashes.json",
            ".hath0r/agentgraph",
            ".hath0r/agentgraph/",
            ".hath0r/agentgraph/*",
            ".hath0r/agentgraph/**",
            ".hath0r/agentgraph/snapshot.json",
            ".hath0r/graphs",
            ".hath0r/graphs/",
            ".hath0r/graphs/*",
            ".hath0r/graphs/**",
            ".hath0r/state/cache",
            ".hath0r/state/cache/",
            ".hath0r/state/cache/*",
            ".hath0r/state/cache/**",
            ".hath0r/state/context",
            ".hath0r/state/context/",
            ".hath0r/state/context/*",
            ".hath0r/state/context/**",
            ".agentguard/graph.db",
        }

        new_lines: List[str] = []
        rewritten_rules: List[str] = []
        removed_rules: List[str] = []

        for line in lines:
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("!"):
                new_lines.append(line)
                continue

            normalized = stripped.lstrip("/")
            if normalized in (".hath0r", ".hath0r/"):
                new_lines.append(".hath0r/*")
                rewritten_rules.append(f"{stripped} -> .hath0r/*")
            elif normalized in (".hath0r/state", ".hath0r/state/"):
                new_lines.append(".hath0r/state/*")
                rewritten_rules.append(f"{stripped} -> .hath0r/state/*")
            elif normalized in forbidden_exact:
                removed_rules.append(stripped)
            else:
                new_lines.append(line)

        existing_stripped = {ln.strip() for ln in new_lines}
        missing_negations = [neg for neg in cls.CANONICAL_GITIGNORE_NEGATIONS if neg not in existing_stripped]
        if missing_negations:
            if new_lines and new_lines[-1].strip() != "":
                new_lines.append("")
            header = "# Canonical Hath0r Graph Folders (NEVER ignore — CR-MEMORY-COMPOUND-001 & CR-AGENTGRAPH-001)"
            if header not in existing_stripped:
                new_lines.append(header)
            for neg in missing_negations:
                new_lines.append(neg)

        updated_text = "\n".join(new_lines) + ("\n" if new_lines else "")
        changed = updated_text != raw_text
        if changed and not dry_run:
            atomic_write_text(gitignore_file, updated_text)

        return {
            "updated": changed,
            "gitignore_file": str(gitignore_file),
            "rewritten_rules": rewritten_rules,
            "removed_rules": removed_rules,
            "appended_negations": missing_negations,
        }

    @classmethod
    def verify_graphs_not_gitignored(cls, repo_root: Path | str) -> Dict[str, Any]:
        """Verify that no canonical Hath0r cognitive graph folder or file is ignored by Git."""
        import subprocess

        root = Path(repo_root).resolve()
        gitignore_file = root / ".gitignore"
        forbidden_rules: List[str] = []
        ignored_paths: List[str] = []

        if gitignore_file.is_file():
            raw_lines = [
                ln.strip()
                for ln in gitignore_file.read_text(encoding="utf-8", errors="ignore").splitlines()
                if ln.strip() and not ln.strip().startswith("#")
            ]
            forbidden_exact = {
                ".hath0r",
                ".hath0r/",
                ".hath0r/state",
                ".hath0r/state/",
                ".hath0r/memory",
                ".hath0r/memory/",
                ".hath0r/memory/*",
                ".hath0r/memory/**",
                ".hath0r/memory/sessions",
                ".hath0r/memory/sessions/",
                ".hath0r/memory/sessions/*",
                ".hath0r/memory/sessions/**",
                ".hath0r/memory/graph.json",
                ".hath0r/memory/hashes.json",
                ".hath0r/agentgraph",
                ".hath0r/agentgraph/",
                ".hath0r/agentgraph/*",
                ".hath0r/agentgraph/**",
                ".hath0r/agentgraph/snapshot.json",
                ".hath0r/graphs",
                ".hath0r/graphs/",
                ".hath0r/graphs/*",
                ".hath0r/graphs/**",
                ".hath0r/state/cache",
                ".hath0r/state/cache/",
                ".hath0r/state/cache/*",
                ".hath0r/state/cache/**",
                ".hath0r/state/context",
                ".hath0r/state/context/",
                ".hath0r/state/context/*",
                ".hath0r/state/context/**",
                ".agentguard/graph.db",
            }
            for ln in raw_lines:
                if not ln.startswith("!") and ln.lstrip("/") in forbidden_exact:
                    forbidden_rules.append(ln)

            has_wildcard_hath0r = any(
                not ln.startswith("!")
                and ln.lstrip("/") in (".hath0r/*", ".hath0r/state/*", ".hath0r/*.json", "*.json")
                for ln in raw_lines
            )
            if has_wildcard_hath0r:
                line_set = set(raw_lines)
                for req_neg in (
                    "!.hath0r/memory/**",
                    "!.hath0r/agentgraph/**",
                    "!.hath0r/graphs/**",
                    "!.hath0r/state/cache/**",
                    "!.hath0r/state/context/**",
                ):
                    if req_neg not in line_set:
                        forbidden_rules.append(f"missing_negation:{req_neg}")

        if (root / ".git").exists():
            try:
                proc = subprocess.run(
                    ["git", "-C", str(root), "check-ignore", "--no-index", *cls.CANONICAL_GRAPH_PATHS],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=False,
                )
                if proc.returncode == 0 and proc.stdout.strip():
                    for out_line in proc.stdout.strip().splitlines():
                        if out_line.strip():
                            ignored_paths.append(out_line.strip())
            except Exception:
                pass

        if forbidden_rules and not ignored_paths:
            ignored_paths.extend(forbidden_rules)

        graphs_not_ignored = len(ignored_paths) == 0 and len(forbidden_rules) == 0
        return {
            "graphs_not_ignored": graphs_not_ignored,
            "ignored_paths": ignored_paths,
            "forbidden_rules": forbidden_rules,
            "gitignore_file": str(gitignore_file),
        }

    @classmethod
    def sync_repo_hashes(
        cls,
        repo_root: Path | str,
        extra_files: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Compute and persist SHA-256 digests for .hath0r/memory/* and referenced source_files in hashes.json."""
        root = Path(repo_root).resolve()
        cls.ensure_gitignore_unignores_graphs(root)
        mem_dir = root / ".hath0r" / "memory"
        mem_dir.mkdir(parents=True, exist_ok=True)
        hashes_file = mem_dir / "hashes.json"
        graph_file = mem_dir / "graph.json"

        prev_rev = 0
        prev_source_files: Dict[str, Any] = {}
        if hashes_file.is_file():
            try:
                prev_data = json.loads(hashes_file.read_text(encoding="utf-8"))
                prev_rev = int(prev_data.get("revision", 0))
                prev_source_files = dict(prev_data.get("source_files", {}))
            except Exception:
                prev_rev = 0

        memory_files: Dict[str, Dict[str, Any]] = {}
        candidates = sorted(
            [p for p in mem_dir.rglob("*") if p.is_file() and p.name != "hashes.json" and ".tmp." not in p.name]
        )
        for fpath in candidates:
            rel = str(fpath.relative_to(mem_dir)).replace("\\", "/")
            raw = fpath.read_bytes()
            entry_info: Dict[str, Any] = {
                "sha256": compute_sha256_bytes(raw),
                "bytes": len(raw),
            }
            if fpath.suffix == ".json":
                try:
                    jdoc = json.loads(raw.decode("utf-8"))
                    if isinstance(jdoc, dict):
                        if "content_hash" in jdoc:
                            entry_info["content_hash"] = jdoc["content_hash"]
                        if "revision" in jdoc:
                            entry_info["revision"] = jdoc["revision"]
                except Exception:
                    pass
            memory_files[rel] = entry_info

        tracked_sources: Dict[str, List[str]] = {}
        for rel_sf, sf_info in prev_source_files.items():
            if isinstance(sf_info, dict):
                tracked_sources[rel_sf] = list(sf_info.get("referenced_by", []))

        if graph_file.is_file():
            try:
                graph = cls.load_from_file(graph_file)
                for node in graph.nodes.values():
                    sfiles = (node.metadata or {}).get("source_files") or {}
                    if isinstance(sfiles, dict):
                        for rel_sf in sfiles:
                            refs = tracked_sources.setdefault(str(rel_sf), [])
                            if node.id not in refs:
                                refs.append(node.id)
            except Exception:
                pass

        for ef in extra_files or []:
            if not ef:
                continue
            ef_path = Path(ef)
            abs_ef = ef_path.resolve() if ef_path.is_absolute() else (root / ef_path).resolve()
            try:
                rel_ef = str(abs_ef.relative_to(root)).replace("\\", "/")
            except ValueError:
                rel_ef = str(ef)
            tracked_sources.setdefault(rel_ef, [])

        source_files_manifest: Dict[str, Dict[str, Any]] = {}
        for rel_sf, refs in sorted(tracked_sources.items()):
            abs_sf = (root / rel_sf).resolve() if not Path(rel_sf).is_absolute() else Path(rel_sf).resolve()
            if abs_sf.is_file():
                raw_sf = abs_sf.read_bytes()
                source_files_manifest[rel_sf] = {
                    "sha256": compute_sha256_bytes(raw_sf),
                    "bytes": len(raw_sf),
                    "referenced_by": sorted(set(refs)),
                }

        # Also update node.metadata.source_files in graph.json if any tracked source file was refreshed
        if graph_file.is_file() and source_files_manifest:
            try:
                g_obj = cls.load_from_file(graph_file)
                changed = False
                for node in g_obj.nodes.values():
                    sfiles = (node.metadata or {}).get("source_files")
                    if isinstance(sfiles, dict):
                        for rel_sf in list(sfiles.keys()):
                            if rel_sf in source_files_manifest:
                                new_h = source_files_manifest[rel_sf]["sha256"]
                                if sfiles.get(rel_sf) != new_h:
                                    sfiles[rel_sf] = new_h
                                    changed = True
                if changed:
                    g_obj.save_to_file(graph_file, sync_hashes=False)
                    raw_g = graph_file.read_bytes()
                    memory_files["graph.json"] = {
                        "sha256": compute_sha256_bytes(raw_g),
                        "bytes": len(raw_g),
                        "content_hash": g_obj.content_hash,
                        "revision": g_obj.revision,
                    }
            except Exception:
                pass

        now = datetime.now(timezone.utc).isoformat()
        manifest: Dict[str, Any] = {
            "schema_version": "hath0r.memory_hashes/1",
            "repo_name": root.name,
            "revision": prev_rev + 1,
            "updated_at": now,
            "manifest_hash": "",
            "memory_files": memory_files,
            "source_files": source_files_manifest,
        }
        canonical_manifest = json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8")
        manifest["manifest_hash"] = compute_sha256_bytes(canonical_manifest)
        atomic_write_text(hashes_file, json.dumps(manifest, indent=2))
        return manifest

    @classmethod
    def verify_repo_hashes(cls, repo_root: Path | str) -> Dict[str, Any]:
        """Verify that all .hath0r/memory/* files and tracked source_files match their SHA-256 digests and zero graph folders are gitignored."""
        root = Path(repo_root).resolve()
        mem_dir = root / ".hath0r" / "memory"
        hashes_file = mem_dir / "hashes.json"
        graph_file = mem_dir / "graph.json"
        gitignore_check = cls.verify_graphs_not_gitignored(root)
        graphs_not_ignored = bool(gitignore_check.get("graphs_not_ignored", True))

        if not hashes_file.is_file():
            return {
                "verified": False,
                "up_to_date": False,
                "manifest_exists": False,
                "hashes_file": str(hashes_file),
                "graphs_not_ignored": graphs_not_ignored,
                "ignored_graph_paths": gitignore_check.get("ignored_paths", []),
                "stale_memory_files": [],
                "stale_source_files": [],
                "missing_files": [str(hashes_file)],
                "conflicts": ["Missing .hath0r/memory/hashes.json integrity manifest."],
            }

        try:
            manifest = json.loads(hashes_file.read_text(encoding="utf-8"))
        except Exception as exc:
            return {
                "verified": False,
                "up_to_date": False,
                "manifest_exists": True,
                "hashes_file": str(hashes_file),
                "graphs_not_ignored": graphs_not_ignored,
                "ignored_graph_paths": gitignore_check.get("ignored_paths", []),
                "stale_memory_files": [],
                "stale_source_files": [],
                "missing_files": [],
                "conflicts": [f"Corrupt hashes.json: {exc}"],
            }

        stale_memory: List[str] = []
        stale_sources: List[str] = []
        missing_files: List[str] = []
        conflicts: List[str] = []
        if not graphs_not_ignored:
            conflicts.append(
                f"Graph folders ignored by .gitignore: {', '.join(gitignore_check.get('ignored_paths', []))}"
            )

        mem_entries = manifest.get("memory_files", {})
        for rel_path, info in mem_entries.items():
            fpath = mem_dir / rel_path
            if not fpath.is_file():
                missing_files.append(rel_path)
                continue
            actual_sha = compute_file_sha256(fpath)
            expected_sha = info.get("sha256")
            if actual_sha != expected_sha:
                stale_memory.append(rel_path)

        src_entries = manifest.get("source_files", {})
        for rel_sf, info in src_entries.items():
            sf_path = (root / rel_sf).resolve() if not Path(rel_sf).is_absolute() else Path(rel_sf).resolve()
            if not sf_path.is_file():
                missing_files.append(rel_sf)
                continue
            actual_sha = compute_file_sha256(sf_path)
            expected_sha = info.get("sha256")
            if actual_sha != expected_sha:
                stale_sources.append(rel_sf)

        if graph_file.is_file():
            try:
                g = cls.load_from_file(graph_file)
                computed_ch = g.compute_content_hash()
                if g.content_hash and g.content_hash != computed_ch:
                    conflicts.append(
                        f"graph.json content_hash mismatch: recorded={g.content_hash}, computed={computed_ch}"
                    )
                for node in g.nodes.values():
                    sfiles = (node.metadata or {}).get("source_files") or {}
                    if isinstance(sfiles, dict):
                        for rel_sf, recorded_sha in sfiles.items():
                            sf_path = (root / rel_sf).resolve() if not Path(rel_sf).is_absolute() else Path(rel_sf).resolve()
                            actual_sha = compute_file_sha256(sf_path)
                            if actual_sha != recorded_sha and rel_sf not in stale_sources:
                                stale_sources.append(rel_sf)
            except Exception as exc:
                conflicts.append(f"Failed to verify graph.json content_hash: {exc}")

        up_to_date = (
            not stale_memory
            and not stale_sources
            and not missing_files
            and not conflicts
            and graphs_not_ignored
        )
        return {
            "verified": up_to_date,
            "up_to_date": up_to_date,
            "manifest_exists": True,
            "hashes_file": str(hashes_file),
            "revision": manifest.get("revision", 1),
            "manifest_hash": manifest.get("manifest_hash"),
            "graphs_not_ignored": graphs_not_ignored,
            "ignored_graph_paths": gitignore_check.get("ignored_paths", []),
            "memory_files_count": len(mem_entries),
            "source_files_count": len(src_entries),
            "stale_memory_files": stale_memory,
            "stale_source_files": stale_sources,
            "missing_files": missing_files,
            "conflicts": conflicts,
        }


    @classmethod
    def ensure_repo_memory(cls, repo_root: Path | str) -> MemoryGraph:
        """Ensure .hath0r/memory/graph.json, .hath0r/memory/sessions/, and .hath0r/memory/hashes.json exist."""
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
                "2. Memory Compounding (CR-MEMORY-COMPOUND-001): Every session must read/write a micro memory session and every task must compound knowledge into .hath0r/memory/graph.json prior to announcing complete.\n"
                "3. Hyper-Context (CR-AGENTGRAPH-001): Query AgentGraph and MemoryGraph rather than loading unbounded files.\n"
                "4. Promotion Path (CR-BAI-001): local -> development -> testing -> staging -> master.\n",
                encoding="utf-8",
            )
        if not arch_file.is_file():
            arch_file.write_text(
                f"# Canonical Architecture — {root.name}\n"
                "Agents orienting to this repository MUST read/write `.hath0r/memory/sessions/current.json` and compound into `.hath0r/memory/graph.json` "
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
                    content="Every project repo must have .hath0r/memory/graph.json and .hath0r/memory/sessions/, read/write micro sessions, and compound knowledge prior to announcing complete.",
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

        # Ensure .hath0r/memory/sessions/current.json and latest.json exist and satisfy read/write baseline
        sessions_dir = mem_dir / "sessions"
        current_file = sessions_dir / "current.json"
        if not current_file.is_file():
            cls.start_micro_session(
                root,
                focus=f"Repository orientation & memory space initialized for {root.name}",
            )
            graph = cls.load_from_file(graph_file)
        else:
            status = cls.get_micro_session_status(root)
            if not status.get("read_verified"):
                cls.read_micro_session(root)
            if not status.get("write_verified"):
                cls.write_micro_session(
                    root,
                    summary=f"Verified micro memory session for {root.name}",
                    kind="observation",
                    tags=["orientation"],
                    linked_node_id=repo_node_id,
                )
            graph = cls.load_from_file(graph_file)

        cls.sync_repo_hashes(root)
        return graph

    def _touch(self) -> None:
        self.updated_at = datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _node_digest(node: MemoryNode) -> str:
        payload = {
            "id": node.id,
            "type": node.type,
            "label": node.label,
            "content": node.content,
            "importance": node.importance,
            "tags": sorted(node.tags),
            "is_current": node.is_current,
            "metadata": node.metadata,
        }
        return compute_sha256_bytes(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8"))

    def compute_content_hash(self) -> str:
        """Compute deterministic SHA-256 digest of all nodes and edges in this MemoryGraph."""
        sorted_nodes = [self.nodes[k].to_dict() for k in sorted(self.nodes.keys())]
        sorted_edges = sorted(
            [e.to_dict() for e in self.edges],
            key=lambda e: (str(e.get("source", "")), str(e.get("target", "")), str(e.get("relation", ""))),
        )
        canonical = json.dumps(
            {
                "schema_version": self.schema_version,
                "graph_id": self.graph_id,
                "nodes": sorted_nodes,
                "edges": sorted_edges,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return compute_sha256_bytes(canonical)

    def merge_from(self, other: MemoryGraph, strict_same_id: bool = True) -> None:
        """Deterministically merge nodes and edges from a concurrent MemoryGraph snapshot."""
        for nid, onode in other.nodes.items():
            if nid not in self.nodes:
                self.nodes[nid] = onode
            else:
                lnode = self.nodes[nid]
                l_digest = self._node_digest(lnode)
                o_digest = self._node_digest(onode)
                if l_digest != o_digest and nid != "session" and not nid.startswith("session:"):
                    base_digest = self._loaded_node_hashes.get(nid)
                    if (
                        strict_same_id
                        and base_digest is not None
                        and l_digest != base_digest
                        and o_digest != base_digest
                    ):
                        raise MemoryHashConflictError(
                            f"Concurrent modification conflict on node '{nid}': both local and on-disk graphs mutated this node."
                        )
                    if o_digest != base_digest and l_digest == base_digest:
                        self.nodes[nid] = onode

        existing_edges = {(e.source, e.target, e.relation) for e in self.edges}
        for oedge in other.edges:
            if oedge.source in self.nodes and oedge.target in self.nodes:
                ekey = (oedge.source, oedge.target, oedge.relation)
                if ekey not in existing_edges:
                    self.edges.append(oedge)
                    existing_edges.add(ekey)

        self.revision = max(self.revision, other.revision) + 1

    def to_dict(self) -> Dict[str, Any]:
        """Serialize memory graph to dictionary."""
        if not self.content_hash:
            self.content_hash = self.compute_content_hash()
        return {
            "schema_version": self.schema_version,
            "graph_id": self.graph_id,
            "revision": self.revision,
            "content_hash": self.content_hash,
            "updated_at": self.updated_at,
            "metadata": self.metadata,
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges],
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize memory graph to JSON string."""
        return json.dumps(self.to_dict(), indent=indent)

    def save_to_file(
        self,
        file_path: Path | str,
        expected_hash: Optional[str] = None,
        auto_merge: bool = True,
        sync_hashes: bool = True,
    ) -> str:
        """Save graph to JSON file with CAS check, deterministic auto-merge, and atomic file replacement."""
        path = Path(file_path)
        if path.is_file():
            disk_file_hash = compute_file_sha256(path)
            try:
                disk_graph = self.load_from_file(path)
            except Exception:
                disk_graph = None

            if expected_hash is not None:
                disk_content_hash = disk_graph.content_hash if disk_graph else None
                if expected_hash not in (disk_file_hash, disk_content_hash):
                    raise MemoryHashConflictError(
                        f"Graph hash conflict on {path}: expected {expected_hash}, "
                        f"found file={disk_file_hash} content={disk_content_hash}"
                    )

            if (
                auto_merge
                and disk_graph is not None
                and self._loaded_file_hash is not None
                and disk_file_hash != self._loaded_file_hash
            ):
                self.merge_from(disk_graph, strict_same_id=True)
            elif disk_graph is not None:
                self.revision = max(self.revision, disk_graph.revision + 1)

        self.content_hash = self.compute_content_hash()
        file_hash = atomic_write_text(path, self.to_json())
        self._loaded_file_hash = file_hash
        self._loaded_node_hashes = {nid: self._node_digest(n) for nid, n in self.nodes.items()}

        if sync_hashes and path.name == "graph.json" and path.parent.name == "memory":
            try:
                repo_root = path.parent.parent.parent
                if repo_root.is_dir():
                    self.sync_repo_hashes(repo_root)
            except Exception:
                pass

        return file_hash

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> MemoryGraph:
        """Construct MemoryGraph instance from dictionary."""
        graph = cls(graph_id=data.get("graph_id", "default-memory-space"))
        graph.schema_version = data.get("schema_version", "1.0.0")
        graph.revision = int(data.get("revision", 1))
        graph.content_hash = str(data.get("content_hash", ""))
        graph.updated_at = data.get("updated_at", datetime.now(timezone.utc).isoformat())
        graph.metadata = data.get("metadata", {})

        for node_dict in data.get("nodes", []):
            node = MemoryNode.from_dict(node_dict)
            graph.nodes[node.id] = node

        for edge_dict in data.get("edges", []):
            edge = MemoryEdge.from_dict(edge_dict)
            graph.edges.append(edge)

        if not graph.content_hash:
            graph.content_hash = graph.compute_content_hash()
        graph._loaded_node_hashes = {nid: cls._node_digest(n) for nid, n in graph.nodes.items()}
        return graph

    @classmethod
    def load_from_file(cls, file_path: Path | str) -> MemoryGraph:
        """Load graph from JSON file and record its SHA-256 digest for CAS."""
        path = Path(file_path)
        raw = path.read_bytes()
        data = json.loads(raw.decode("utf-8"))
        graph = cls.from_dict(data)
        graph._loaded_file_hash = compute_sha256_bytes(raw)
        return graph

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
