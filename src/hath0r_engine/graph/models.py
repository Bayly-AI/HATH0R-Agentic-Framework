"""AgentGraph Data Models, Enums, and Validation Reports."""

from __future__ import annotations

import datetime
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

RULES_MD_FILENAME = "rules.md"


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
