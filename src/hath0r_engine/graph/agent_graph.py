"""AgentGraph Unified Cognitive Substrate & Quad-Graph Engine.

Unifies KnowledgeGraph, ContextGraph, MemoryGraph, and AgentRulesGraph into a cohesive,
extensible cognitive substrate supporting deterministic rule inheritance, role-based
tool authorization (RBAC/ABAC), hybrid BM25 + dense search, bitemporal intervals,
and pluggable file/modality adapters.
"""

from __future__ import annotations

import ast
import datetime
import json
import math
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


class AgentGraphPlane(str, Enum):
    """The four canonical planes of the AgentGraph substrate, plus extensible planes."""

    KNOWLEDGE = "knowledge"  # Static documentation, specs, contracts, schemas
    CONTEXT = "context"      # Dynamic sessions, active subagents, tool spans
    MEMORY = "memory"        # Episodic recall, long-term facts, sleep reflections
    RULES = "rules"          # Agent roles, policy invariants, tool RBAC, delegation
    EXTENSIBLE = "extensible"# Pluggable modalities (AST code, vision patches, etc.)


class RulePriority(int, Enum):
    """Hierarchical precedence tiers for deterministic rule evaluation."""

    ROLE_GUIDELINE = 1    # Soft agent-level guidelines
    SUBSYSTEM_RULE = 2    # Subsystem-specific rules (e.g. src/hath0r_engine/AGENTS.md)
    REPO_STANDARD = 3     # Repository-level rules (e.g. root AGENTS.md)
    ORG_INVARIANT = 4     # Immutable org-wide policies (e.g. CR-CLI-ENTRY-001, CR-BAI-001)


class RuleConflictResolution(str, Enum):
    """Behavior when conflicting rule directives are detected."""

    HIGHER_PRECEDENCE_WINS = "higher_precedence_wins"
    ERROR_ON_CONFLICT = "error_on_conflict"


class RuleCycleError(Exception):
    """Raised when an inheritance or dependency cycle is detected in the rule DAG."""


class RuleConflictError(Exception):
    """Raised when opposing rule directives collide at the same priority tier."""


@dataclass
class AgentGraphNode:
    """Unified node in the AgentGraph cognitive substrate."""

    id: str
    plane: str  # knowledge | context | memory | rules | extensible
    type: str   # agent_role | rule_policy | document | contract | concept | task | etc.
    label: str
    content: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    is_current: bool = True
    created_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def is_valid_at(self, as_of: Optional[str] = None, only_current: bool = False) -> bool:
        """Evaluate bitemporal validity of this node."""
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
    def from_dict(cls, data: Dict[str, Any]) -> AgentGraphNode:
        return cls(**data)


@dataclass
class AgentGraphEdge:
    """Relational edge linking entities across any of the AgentGraph planes."""

    source: str
    target: str
    relation: str  # GOVERNS, INHERITS_FROM, AUTHORIZES_TOOL, RESTRICTED_BY, CAN_SPAWN, SUPERSEDES, etc.
    plane: Optional[str] = None
    weight: float = 1.0
    valid_from: Optional[str] = None
    valid_to: Optional[str] = None
    is_current: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_valid_at(self, as_of: Optional[str] = None, only_current: bool = False) -> bool:
        """Evaluate bitemporal validity of this edge."""
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
    def from_dict(cls, data: Dict[str, Any]) -> AgentGraphEdge:
        return cls(**data)


@dataclass
class ResolvedRuleSet:
    """The computed deterministic active rules and authorizations for an agent role."""

    role_id: str
    active_rules: List[AgentGraphNode] = field(default_factory=list)
    authorized_tools: Set[str] = field(default_factory=set)
    forbidden_tools: Set[str] = field(default_factory=set)
    restricted_actions: Set[str] = field(default_factory=set)
    allowed_actions: Set[str] = field(default_factory=set)
    lineage_path: List[str] = field(default_factory=list)
    governing_invariants: List[str] = field(default_factory=list)


@dataclass
class SearchResult:
    """A scored result from cross-plane hybrid retrieval."""

    node: AgentGraphNode
    score: float
    matched_plane: str
    highlights: List[str] = field(default_factory=list)


@dataclass
class AgentGraphValidationReport:
    """Health and consistency audit report for AgentGraph."""

    is_valid: bool
    total_nodes: int
    total_edges: int
    plane_counts: Dict[str, int]
    dangling_edges: List[Tuple[str, str]] = field(default_factory=list)
    detected_cycles: List[List[str]] = field(default_factory=list)
    conflicting_rules: List[str] = field(default_factory=list)
    temporal_anomalies: List[str] = field(default_factory=list)


# -------------------------------------------------------------------------
# Pluggable Modality Adapter Interface
# -------------------------------------------------------------------------

class BaseGraphAdapter:
    """Base interface for modality and file adapters in AgentGraph."""

    def can_handle(self, path: Path) -> bool:
        raise NotImplementedError

    def extract(self, path: Path) -> Tuple[List[AgentGraphNode], List[AgentGraphEdge]]:
        raise NotImplementedError


class MarkdownDocAdapter(BaseGraphAdapter):
    """Extracts document nodes and internal links from Markdown files."""

    def can_handle(self, path: Path) -> bool:
        return path.suffix.lower() in {".md", ".markdown"}

    def extract(self, path: Path) -> Tuple[List[AgentGraphNode], List[AgentGraphEdge]]:
        nodes: List[AgentGraphNode] = []
        edges: List[AgentGraphEdge] = []

        if not path.exists():
            return nodes, edges

        content = path.read_text(encoding="utf-8", errors="replace")
        title = path.stem.replace("-", " ").replace("_", " ").title()

        # Extract title from first H1 if present
        h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if h1_match:
            title = h1_match.group(1).strip()

        node_id = f"doc:{path.name}"
        node = AgentGraphNode(
            id=node_id,
            plane=AgentGraphPlane.KNOWLEDGE.value,
            type="document",
            label=title,
            content=content[:1000],
            properties={"path": str(path), "size": len(content)},
        )
        nodes.append(node)

        # Detect markdown link edges
        for target in re.findall(r"\[.*?\]\((.*?\.md)\)", content):
            target_name = Path(target).name
            edges.append(
                AgentGraphEdge(
                    source=node_id,
                    target=f"doc:{target_name}",
                    relation="references",
                    plane=AgentGraphPlane.KNOWLEDGE.value,
                )
            )

        return nodes, edges


class ASTCodeAdapter(BaseGraphAdapter):
    """Extracts classes, functions, and import dependencies from Python files."""

    def can_handle(self, path: Path) -> bool:
        return path.suffix.lower() == ".py"

    def extract(self, path: Path) -> Tuple[List[AgentGraphNode], List[AgentGraphEdge]]:
        nodes: List[AgentGraphNode] = []
        edges: List[AgentGraphEdge] = []

        if not path.exists():
            return nodes, edges

        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(content, filename=str(path))
        except SyntaxError:
            return nodes, edges

        module_id = f"module:{path.stem}"
        nodes.append(
            AgentGraphNode(
                id=module_id,
                plane=AgentGraphPlane.EXTENSIBLE.value,
                type="code_module",
                label=path.name,
                content="",
                properties={"path": str(path)},
            )
        )

        for stmt in tree.body:
            if isinstance(stmt, ast.ClassDef):
                class_id = f"class:{path.stem}.{stmt.name}"
                nodes.append(
                    AgentGraphNode(
                        id=class_id,
                        plane=AgentGraphPlane.EXTENSIBLE.value,
                        type="code_class",
                        label=stmt.name,
                        content=ast.get_docstring(stmt) or "",
                        properties={"module": path.stem},
                    )
                )
                edges.append(
                    AgentGraphEdge(
                        source=module_id,
                        target=class_id,
                        relation="contains",
                        plane=AgentGraphPlane.EXTENSIBLE.value,
                    )
                )
            elif isinstance(stmt, ast.FunctionDef):
                func_id = f"func:{path.stem}.{stmt.name}"
                nodes.append(
                    AgentGraphNode(
                        id=func_id,
                        plane=AgentGraphPlane.EXTENSIBLE.value,
                        type="code_function",
                        label=stmt.name,
                        content=ast.get_docstring(stmt) or "",
                        properties={"module": path.stem},
                    )
                )
                edges.append(
                    AgentGraphEdge(
                        source=module_id,
                        target=func_id,
                        relation="contains",
                        plane=AgentGraphPlane.EXTENSIBLE.value,
                    )
                )

        return nodes, edges


# -------------------------------------------------------------------------
# Core AgentGraph Substrate Engine
# -------------------------------------------------------------------------

class AgentGraphEngine:
    """Unified Quad-Graph Cognitive Substrate Engine.

    Seamlessly unifies:
      - KnowledgeGraph (static specs, schemas, documentation)
      - ContextGraph (dynamic sessions, subagents, tool spans)
      - MemoryGraph (temporal entities, reflections, Letta paging)
      - RulesGraph (agent roles, governance policies, tool RBAC)
    """

    def __init__(self, graph_id: str = "canonical-agentgraph") -> None:
        self.graph_id = graph_id
        self.schema_version = "hath0r.agentgraph/1"
        self.nodes: Dict[str, AgentGraphNode] = {}
        self.edges: List[AgentGraphEdge] = []
        self.adapters: List[BaseGraphAdapter] = [MarkdownDocAdapter(), ASTCodeAdapter()]

        # Adjacency indexes for O(1) edge traversal
        self._outgoing: Dict[str, List[AgentGraphEdge]] = defaultdict(list)
        self._incoming: Dict[str, List[AgentGraphEdge]] = defaultdict(list)

        # Lexical search index cache
        self._bm25_docs: Dict[str, str] = {}
        self._bm25_term_freqs: Dict[str, Counter[str]] = {}
        self._bm25_doc_lengths: Dict[str, int] = {}
        self._bm25_avg_len: float = 0.0
        self._bm25_df: Counter[str] = Counter()

    def register_adapter(self, adapter: BaseGraphAdapter) -> None:
        """Register a pluggable modality adapter."""
        self.adapters.insert(0, adapter)

    def add_node(self, node: AgentGraphNode) -> None:
        """Add or update an AgentGraph node."""
        node.updated_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        self.nodes[node.id] = node
        self._index_node_bm25(node)

    def get_node(self, node_id: str) -> Optional[AgentGraphNode]:
        """Retrieve node by unique ID."""
        return self.nodes.get(node_id)

    def add_edge(self, edge: AgentGraphEdge) -> None:
        """Add a relational edge between entities."""
        self.edges.append(edge)
        self._outgoing[edge.source].append(edge)
        self._incoming[edge.target].append(edge)

    def get_outgoing_edges(self, source_id: str, relation: Optional[str] = None) -> List[AgentGraphEdge]:
        """Return all outgoing edges from source, optionally filtered by relation."""
        edges = self._outgoing.get(source_id, [])
        if relation:
            return [e for e in edges if e.relation == relation]
        return list(edges)

    def get_incoming_edges(self, target_id: str, relation: Optional[str] = None) -> List[AgentGraphEdge]:
        """Return all incoming edges to target, optionally filtered by relation."""
        edges = self._incoming.get(target_id, [])
        if relation:
            return [e for e in edges if e.relation == relation]
        return list(edges)

    # ---------------------------------------------------------------------
    # Deterministic Rule Inheritance & Authorization Engine
    # ---------------------------------------------------------------------

    def register_agent_role(
        self,
        role_id: str,
        role_name: str,
        scope: str = "root",
        permitted_tools: Optional[List[str]] = None,
        forbidden_tools: Optional[List[str]] = None,
        parent_role_id: Optional[str] = None,
    ) -> AgentGraphNode:
        """Register an agent role with tool capabilities."""
        node = AgentGraphNode(
            id=role_id,
            plane=AgentGraphPlane.RULES.value,
            type="agent_role",
            label=role_name,
            content=f"Agent role {role_name} operating in scope {scope}.",
            properties={
                "role_name": role_name,
                "scope": scope,
                "permitted_tools": permitted_tools or [],
                "forbidden_tools": forbidden_tools or [],
            },
        )
        self.add_node(node)

        # Link permitted tools
        for tool in permitted_tools or []:
            self.add_edge(
                AgentGraphEdge(
                    source=role_id,
                    target=f"tool:{tool}",
                    relation="AUTHORIZES_TOOL",
                    plane=AgentGraphPlane.RULES.value,
                )
            )

        # Link parent role inheritance
        if parent_role_id:
            self.add_edge(
                AgentGraphEdge(
                    source=role_id,
                    target=parent_role_id,
                    relation="INHERITS_FROM",
                    plane=AgentGraphPlane.RULES.value,
                )
            )

        return node

    def register_rule_policy(
        self,
        rule_id: str,
        title: str,
        content: str,
        priority: RulePriority = RulePriority.REPO_STANDARD,
        target_scope: str = "root",
        governs_roles: Optional[List[str]] = None,
        restricted_actions: Optional[List[str]] = None,
        allowed_actions: Optional[List[str]] = None,
        supersedes_rule_id: Optional[str] = None,
    ) -> AgentGraphNode:
        """Register a governance rule or invariant."""
        node = AgentGraphNode(
            id=rule_id,
            plane=AgentGraphPlane.RULES.value,
            type="rule_policy",
            label=title,
            content=content,
            properties={
                "priority": int(priority),
                "priority_name": priority.name,
                "target_scope": target_scope,
                "restricted_actions": restricted_actions or [],
                "allowed_actions": allowed_actions or [],
            },
        )
        self.add_node(node)

        # Link roles governed by this rule
        for role_id in governs_roles or []:
            self.add_edge(
                AgentGraphEdge(
                    source=rule_id,
                    target=role_id,
                    relation="GOVERNS",
                    plane=AgentGraphPlane.RULES.value,
                )
            )

        # Handle superseding
        if supersedes_rule_id:
            self.add_edge(
                AgentGraphEdge(
                    source=rule_id,
                    target=supersedes_rule_id,
                    relation="SUPERSEDES",
                    plane=AgentGraphPlane.RULES.value,
                )
            )
            # Mark superseded rule as non-current
            old_node = self.get_node(supersedes_rule_id)
            if old_node:
                old_node.is_current = False
                old_node.valid_to = datetime.datetime.now(datetime.timezone.utc).isoformat()

        return node

    def resolve_agent_rules(
        self,
        role_id: str,
        scope: Optional[str] = None,
        as_of: Optional[str] = None,
        only_current: bool = True,
    ) -> ResolvedRuleSet:
        """Deterministically resolve active rules, tool authorizations, and constraints for an agent role.

        Traverses role inheritance DAG, collects applicable scoped rules, detects cycles,
        and applies precedence conflict resolution.
        """
        role_node = self.get_node(role_id)
        if not role_node:
            raise ValueError(f"Agent role '{role_id}' not found in AgentGraph.")

        # 1. Traverse role inheritance DAG (detecting cycles)
        role_lineage: List[str] = []
        visited_roles: Set[str] = set()
        curr_role: Optional[str] = role_id

        while curr_role:
            if curr_role in visited_roles:
                raise RuleCycleError(f"Cycle detected in agent role inheritance: {' -> '.join(role_lineage)} -> {curr_role}")
            visited_roles.add(curr_role)
            role_lineage.append(curr_role)

            parent_edges = [
                e for e in self.get_outgoing_edges(curr_role, relation="INHERITS_FROM")
                if e.is_valid_at(as_of=as_of, only_current=only_current)
            ]
            curr_role = parent_edges[0].target if parent_edges else None

        # 2. Collect authorized tools across role inheritance
        authorized_tools: Set[str] = set()
        forbidden_tools: Set[str] = set()

        for r_id in role_lineage:
            r_node = self.get_node(r_id)
            if r_node:
                authorized_tools.update(r_node.properties.get("permitted_tools", []))
                forbidden_tools.update(r_node.properties.get("forbidden_tools", []))

            for e in self.get_outgoing_edges(r_id, relation="AUTHORIZES_TOOL"):
                if e.is_valid_at(as_of=as_of, only_current=only_current):
                    tool_name = e.target.removeprefix("tool:")
                    authorized_tools.add(tool_name)

        # Prune forbidden tools
        authorized_tools.difference_update(forbidden_tools)

        # 3. Collect active rules governing these roles or active scope
        applicable_rules: Dict[str, AgentGraphNode] = {}
        for r_id in role_lineage:
            for inc in self.get_incoming_edges(r_id, relation="GOVERNS"):
                if inc.is_valid_at(as_of=as_of, only_current=only_current):
                    rule_node = self.get_node(inc.source)
                    if rule_node and rule_node.is_valid_at(as_of=as_of, only_current=only_current):
                        applicable_rules[rule_node.id] = rule_node

        # Also collect scope-matching rules
        effective_scope = scope or role_node.properties.get("scope", "root")
        for node in self.nodes.values():
            if node.plane == AgentGraphPlane.RULES.value and node.type == "rule_policy":
                if node.is_valid_at(as_of=as_of, only_current=only_current):
                    rule_scope = node.properties.get("target_scope", "root")
                    if rule_scope in ("root", effective_scope):
                        applicable_rules[node.id] = node

        # 4. Resolve action restrictions and allowances by priority tier
        active_rules_list = sorted(
            applicable_rules.values(),
            key=lambda r: r.properties.get("priority", 1),
            reverse=True,
        )

        restricted_actions: Set[str] = set()
        allowed_actions: Set[str] = set()
        governing_invariants: List[str] = []

        action_precedence: Dict[str, Tuple[int, bool]] = {}  # action -> (priority, is_allowed)

        for rule in active_rules_list:
            priority = rule.properties.get("priority", 1)
            if priority == int(RulePriority.ORG_INVARIANT):
                governing_invariants.append(rule.label)

            for act in rule.properties.get("restricted_actions", []):
                if act in action_precedence:
                    prev_prio, prev_allowed = action_precedence[act]
                    if priority > prev_prio:
                        action_precedence[act] = (priority, False)
                    elif priority == prev_prio and prev_allowed:
                        raise RuleConflictError(
                            f"Rule conflict detected: action '{act}' simultaneously restricted by {rule.id} "
                            f"and allowed at priority tier {priority}."
                        )
                else:
                    action_precedence[act] = (priority, False)

            for act in rule.properties.get("allowed_actions", []):
                if act in action_precedence:
                    prev_prio, prev_allowed = action_precedence[act]
                    if priority > prev_prio:
                        action_precedence[act] = (priority, True)
                    elif priority == prev_prio and not prev_allowed:
                        raise RuleConflictError(
                            f"Rule conflict detected: action '{act}' simultaneously allowed by {rule.id} "
                            f"and restricted at priority tier {priority}."
                        )
                else:
                    action_precedence[act] = (priority, True)

        for act, (_, is_allowed) in action_precedence.items():
            if is_allowed:
                allowed_actions.add(act)
            else:
                restricted_actions.add(act)

        return ResolvedRuleSet(
            role_id=role_id,
            active_rules=active_rules_list,
            authorized_tools=authorized_tools,
            forbidden_tools=forbidden_tools,
            restricted_actions=restricted_actions,
            allowed_actions=allowed_actions,
            lineage_path=role_lineage,
            governing_invariants=governing_invariants,
        )

    # ---------------------------------------------------------------------
    # Ingestion & Modality Adapters
    # ---------------------------------------------------------------------

    def ingest_path(self, path: Path) -> int:
        """Ingest a file or directory using registered modality adapters."""
        if not path.exists():
            return 0

        ingested_count = 0
        files = [path] if path.is_file() else [p for p in path.rglob("*") if p.is_file()]

        for file_path in files:
            for adapter in self.adapters:
                if adapter.can_handle(file_path):
                    nodes, edges = adapter.extract(file_path)
                    for n in nodes:
                        self.add_node(n)
                        ingested_count += 1
                    for e in edges:
                        self.add_edge(e)
                    break

        return ingested_count

    # ---------------------------------------------------------------------
    # Hybrid BM25 Lexical & Property Search
    # ---------------------------------------------------------------------

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        return [w.lower() for w in re.findall(r"\b[a-zA-Z0-9_\-\.]{2,}\b", text)]

    def _index_node_bm25(self, node: AgentGraphNode) -> None:
        """Incrementally index node into Okapi BM25 table."""
        full_text = f"{node.label} {node.type} {node.plane} {node.content} " + " ".join(
            str(v) for v in node.properties.values()
        )
        tokens = self._tokenize(full_text)
        doc_len = len(tokens)
        self._bm25_docs[node.id] = full_text
        self._bm25_doc_lengths[node.id] = doc_len
        tf = Counter(tokens)
        self._bm25_term_freqs[node.id] = tf

        for term in tf:
            self._bm25_df[term] += 1

        total_len = sum(self._bm25_doc_lengths.values())
        self._bm25_avg_len = total_len / len(self._bm25_doc_lengths) if self._bm25_doc_lengths else 0.0

    def query_hybrid(
        self,
        query: str,
        planes: Optional[List[str]] = None,
        limit: int = 10,
        as_of: Optional[str] = None,
        only_current: bool = True,
        k1: float = 1.5,
        b: float = 0.75,
    ) -> List[SearchResult]:
        """Perform cross-plane hybrid BM25 and keyword search with temporal validity filtering."""
        query_tokens = self._tokenize(query)
        if not query_tokens or not self._bm25_doc_lengths:
            return []

        scores: Dict[str, float] = defaultdict(float)
        num_docs = len(self._bm25_doc_lengths)

        for term in query_tokens:
            df = self._bm25_df.get(term, 0)
            if df == 0:
                continue
            idf = math.log((num_docs - df + 0.5) / (df + 0.5) + 1.0)

            for doc_id, tf_map in self._bm25_term_freqs.items():
                node = self.nodes.get(doc_id)
                if not node:
                    continue
                if planes and node.plane not in planes:
                    continue
                if not node.is_valid_at(as_of=as_of, only_current=only_current):
                    continue

                freq = tf_map.get(term, 0)
                if freq == 0:
                    continue

                doc_len = self._bm25_doc_lengths[doc_id]
                denom = freq + k1 * (1.0 - b + b * (doc_len / self._bm25_avg_len))
                scores[doc_id] += idf * (freq * (k1 + 1.0)) / denom

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:limit]
        results: List[SearchResult] = []
        for doc_id, score in ranked:
            node = self.nodes[doc_id]
            results.append(
                SearchResult(
                    node=node,
                    score=round(score, 4),
                    matched_plane=node.plane,
                    highlights=[t for t in query_tokens if t in self._bm25_term_freqs.get(doc_id, {})],
                )
            )

        return results

    # ---------------------------------------------------------------------
    # Validation & Graph Health Audit
    # ---------------------------------------------------------------------

    def validate_integrity(self) -> AgentGraphValidationReport:
        """Run comprehensive consistency, dangling-edge, and cycle detection audits."""
        plane_counts = Counter(n.plane for n in self.nodes.values())
        dangling: List[Tuple[str, str]] = []
        temporal_anomalies: List[str] = []

        for e in self.edges:
            if e.source not in self.nodes or (not e.target.startswith("tool:") and e.target not in self.nodes):
                dangling.append((e.source, e.target))
            if e.valid_from and e.valid_to and e.valid_from > e.valid_to:
                temporal_anomalies.append(f"Edge {e.source}->{e.target} valid_from ({e.valid_from}) > valid_to ({e.valid_to})")

        for n in self.nodes.values():
            if n.valid_from and n.valid_to and n.valid_from > n.valid_to:
                temporal_anomalies.append(f"Node {n.id} valid_from ({n.valid_from}) > valid_to ({n.valid_to})")

        # Cycle detection in INHERITS_FROM DAG
        detected_cycles: List[List[str]] = []
        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def dfs(node_id: str, path: List[str]) -> None:
            visited.add(node_id)
            rec_stack.add(node_id)
            path.append(node_id)

            for edge in self.get_outgoing_edges(node_id, relation="INHERITS_FROM"):
                neighbor = edge.target
                if neighbor not in visited:
                    dfs(neighbor, path)
                elif neighbor in rec_stack:
                    cycle_start = path.index(neighbor)
                    detected_cycles.append(path[cycle_start:] + [neighbor])

            path.pop()
            rec_stack.remove(node_id)

        for n_id, node in self.nodes.items():
            if node.plane == AgentGraphPlane.RULES.value and n_id not in visited:
                dfs(n_id, [])

        is_valid = len(dangling) == 0 and len(detected_cycles) == 0 and len(temporal_anomalies) == 0

        return AgentGraphValidationReport(
            is_valid=is_valid,
            total_nodes=len(self.nodes),
            total_edges=len(self.edges),
            plane_counts=dict(plane_counts),
            dangling_edges=dangling,
            detected_cycles=detected_cycles,
            temporal_anomalies=temporal_anomalies,
        )

    # ---------------------------------------------------------------------
    # Serialization & Snapshots
    # ---------------------------------------------------------------------

    def export_snapshot(self, path: Path) -> None:
        """Export full graph state to JSON."""
        data = {
            "schema_version": self.schema_version,
            "graph_id": self.graph_id,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges],
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def import_snapshot(self, path: Path) -> None:
        """Import graph state from JSON snapshot."""
        if not path.exists():
            raise FileNotFoundError(f"Snapshot not found at {path}")
        data = json.loads(path.read_text(encoding="utf-8"))
        for n_dict in data.get("nodes", []):
            self.add_node(AgentGraphNode.from_dict(n_dict))
        for e_dict in data.get("edges", []):
            self.add_edge(AgentGraphEdge.from_dict(e_dict))
