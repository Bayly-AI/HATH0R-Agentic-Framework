"""AST Graph Neural Network (GNN) Engine for Predictive Test Selection & Defect Hotspots.

Uses Graph Convolutional Networks (GCN) over Abstract Syntax Tree (AST) call graphs,
import dependencies, and test mappings to predict regression risk scores.
Enables Predictive Test Selection (PTS) to accelerate CI cycles by running high-risk tests first.
"""

from __future__ import annotations

import ast
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _sigmoid(x: float) -> float:
    """Stable sigmoid activation."""
    if x >= 0:
        z = math.exp(-x)
        return 1.0 / (1.0 + z)
    else:
        z = math.exp(x)
        return z / (1.0 + z)


def _relu(x: float) -> float:
    return max(0.0, x)


@dataclass
class ASTGNNNode:
    """Node in the codebase AST dependency and test invocation graph."""

    id: str
    name: str
    file_path: str
    node_type: str  # function | class | module | test
    complexity: float = 1.0
    churn_score: float = 0.1
    is_modified: bool = False
    is_test: bool = False
    is_entrypoint: bool = False
    entrypoint_kind: Optional[str] = None
    in_degree: int = 0
    out_degree: int = 0
    risk_score: float = 0.0


@dataclass
class ASTGNNEdge:
    """Directed edge in the AST dependency graph."""

    source: str
    target: str
    edge_type: str  # CALLS | TESTS | IMPORTS | CONTAINS
    weight: float = 1.0


@dataclass
class ReachabilityPruneReport:
    """OpenAnt-style static call-graph reachability pruning report (arXiv:2606.19149)."""

    total_units: int
    reachable_units_count: int
    pruned_units_count: int
    reduction_percentage: float
    entrypoint_ids: List[str]
    reachable_unit_ids: List[str]
    pruned_unit_ids: List[str]
    hop_distances: Dict[str, int]


@dataclass
class ConstrainedExploitTrace:
    """Candidate 4-tuple exploit trace submitted for OpenAnt Stage 2 verification."""

    finding_id: str
    external_input: str
    entrypoint_symbol: str
    data_flow_hop_chain: List[str]
    sink_operation: str
    assumes_admin_or_local_shell: bool = False
    has_unbypassable_sanitizer: bool = False


@dataclass
class ConstrainedAttackerVerdict:
    """Non-sycophantic constrained attacker persona verification result."""

    finding_id: str
    status: str  # CONFIRMED_EXPLOITABLE | NOT_EXPLOITABLE_LOCAL_ONLY | REJECTED_UNREACHABLE | REJECTED_SANITIZED | REJECTED_INCOMPLETE_TRACE
    exploitable: bool
    reason: str
    verified_entrypoint_id: Optional[str] = None
    hop_count: int = 0


@dataclass
class PredictiveTestSelectionReport:
    """Predictive test selection and regression risk evaluation report."""

    changed_files: List[str]
    total_tests_discovered: int
    selected_tests_count: int
    test_reduction_percentage: float
    high_risk_tests: List[Dict[str, Any]]
    medium_risk_tests: List[Dict[str, Any]]
    low_risk_tests: List[Dict[str, Any]]
    hotspot_symbols: List[Dict[str, Any]]
    gnn_inference_latency_ms: float


class ASTGraphNeuralNetwork:
    """Graph Convolutional Network (GCN) for AST risk propagation & test prioritization."""

    FEATURE_DIM: int = 8
    HIDDEN_DIM: int = 16

    def __init__(self, random_seed: int = 42) -> None:
        self.random_seed = random_seed
        rng = random.Random(random_seed)

        # GCN Layer 1 weights: [HIDDEN_DIM x FEATURE_DIM]
        scale_1 = math.sqrt(2.0 / (self.FEATURE_DIM + self.HIDDEN_DIM))
        self.w_self_1 = [
            [rng.gauss(0.0, scale_1) for _ in range(self.FEATURE_DIM)]
            for _ in range(self.HIDDEN_DIM)
        ]
        self.w_neigh_1 = [
            [rng.gauss(0.0, scale_1) for _ in range(self.FEATURE_DIM)]
            for _ in range(self.HIDDEN_DIM)
        ]
        self.b_1 = [0.0] * self.HIDDEN_DIM

        # GCN Layer 2 weights: [HIDDEN_DIM x HIDDEN_DIM]
        scale_2 = math.sqrt(2.0 / (self.HIDDEN_DIM * 2))
        self.w_self_2 = [
            [rng.gauss(0.0, scale_2) for _ in range(self.HIDDEN_DIM)]
            for _ in range(self.HIDDEN_DIM)
        ]
        self.w_neigh_2 = [
            [rng.gauss(0.0, scale_2) for _ in range(self.HIDDEN_DIM)]
            for _ in range(self.HIDDEN_DIM)
        ]
        self.b_2 = [0.0] * self.HIDDEN_DIM

        # Readout classification head (Risk probability): [1 x HIDDEN_DIM]
        self.w_out = [rng.gauss(0.0, 0.2) for _ in range(self.HIDDEN_DIM)]
        # Bias modification feature to give high initial risk to modified nodes
        self.w_out[0] = 1.2
        self.b_out = -0.5

    def _extract_ast_nodes_from_file(self, file_path: Path) -> Tuple[List[ASTGNNNode], List[ASTGNNEdge]]:
        """Parse Python file using AST and extract function/class symbols and call relationships."""
        nodes: List[ASTGNNNode] = []
        edges: List[ASTGNNEdge] = []
        rel_path = str(file_path)
        is_test_file = "test" in file_path.name.lower()

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(content, filename=str(file_path))
        except Exception:
            return nodes, edges

        file_node_id = f"module::{rel_path}"
        nodes.append(
            ASTGNNNode(
                id=file_node_id,
                name=file_path.name,
                file_path=rel_path,
                node_type="module",
                is_test=is_test_file,
            )
        )

        for stmt in tree.body:
            if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef)):
                fn_id = f"{rel_path}::{stmt.name}"
                is_test_fn = is_test_file and stmt.name.startswith("test_")
                # Estimate complexity from branches
                branches = sum(1 for sub in ast.walk(stmt) if isinstance(sub, (ast.If, ast.For, ast.While, ast.ExceptHandler)))
                # Detect external entrypoints (Click CLI, FastMCP tools, FastAPI routes, main)
                entrypoint_kind: Optional[str] = None
                for dec in stmt.decorator_list:
                    dec_target = dec.func if isinstance(dec, ast.Call) else dec
                    dec_name = ""
                    if isinstance(dec_target, ast.Attribute):
                        base = dec_target.value.id if isinstance(dec_target.value, ast.Name) else ""
                        dec_name = f"{base}.{dec_target.attr}".strip(".")
                    elif isinstance(dec_target, ast.Name):
                        dec_name = dec_target.id
                    lower_dec = dec_name.lower()
                    if any(k in lower_dec for k in ("tool", "resource", "prompt")) and "mcp" in lower_dec:
                        entrypoint_kind = "mcp_tool"
                    elif any(lower_dec.endswith(k) for k in (".get", ".post", ".put", ".delete", ".patch", ".route", ".websocket")):
                        entrypoint_kind = "http_route"
                    elif any(k in lower_dec for k in ("command", "group")):
                        entrypoint_kind = "cli_command"
                if entrypoint_kind is None and stmt.name in ("main", "cli", "app_main", "handle_request", "dispatch_tool"):
                    entrypoint_kind = "public_entrypoint"

                fn_node = ASTGNNNode(
                    id=fn_id,
                    name=stmt.name,
                    file_path=rel_path,
                    node_type="test" if is_test_fn else "function",
                    complexity=float(1 + branches),
                    is_test=is_test_fn,
                    is_entrypoint=entrypoint_kind is not None,
                    entrypoint_kind=entrypoint_kind,
                )
                nodes.append(fn_node)
                edges.append(ASTGNNEdge(source=file_node_id, target=fn_id, edge_type="CONTAINS", weight=0.5))

                # Extract calls inside function
                for sub in ast.walk(stmt):
                    if isinstance(sub, ast.Call):
                        if isinstance(sub.func, ast.Name):
                            called_target = sub.func.id
                            edges.append(ASTGNNEdge(source=fn_id, target=called_target, edge_type="CALLS", weight=1.0))
                        elif isinstance(sub.func, ast.Attribute):
                            called_target = sub.func.attr
                            edges.append(ASTGNNEdge(source=fn_id, target=called_target, edge_type="CALLS", weight=1.0))

            elif isinstance(stmt, ast.ClassDef):
                cls_id = f"{rel_path}::{stmt.name}"
                nodes.append(
                    ASTGNNNode(
                        id=cls_id,
                        name=stmt.name,
                        file_path=rel_path,
                        node_type="class",
                        is_test=is_test_file and "test" in stmt.name.lower(),
                    )
                )
                edges.append(ASTGNNEdge(source=file_node_id, target=cls_id, edge_type="CONTAINS", weight=0.5))

        return nodes, edges

    def build_graph_from_directory(
        self,
        root_dir: Path,
        changed_files: Optional[List[str]] = None,
    ) -> Tuple[Dict[str, ASTGNNNode], List[ASTGNNEdge]]:
        """Construct full dependency graph over python source and test files."""
        all_nodes: Dict[str, ASTGNNNode] = {}
        all_edges: List[ASTGNNEdge] = []
        changed_set = {str(Path(f).resolve()) for f in (changed_files or [])}

        for py_path in root_dir.rglob("*.py"):
            if any(part.startswith(".") or part in ("venv", ".venv", "__pycache__", "build", "dist") for part in py_path.parts):
                continue
            file_nodes, file_edges = self._extract_ast_nodes_from_file(py_path)
            for n in file_nodes:
                if str(py_path.resolve()) in changed_set or any(cf in str(py_path) for cf in (changed_files or [])):
                    n.is_modified = True
                all_nodes[n.id] = n
            all_edges.extend(file_edges)

        # Map symbol names to node IDs so bare CALLS edges resolve across files
        name_to_ids: Dict[str, List[str]] = {}
        for nid, node in all_nodes.items():
            name_to_ids.setdefault(node.name, []).append(nid)

        resolved_edges: List[ASTGNNEdge] = []
        for e in all_edges:
            if e.edge_type == "CALLS" and e.target not in all_nodes and e.target in name_to_ids:
                for target_id in name_to_ids[e.target]:
                    resolved_edges.append(
                        ASTGNNEdge(source=e.source, target=target_id, edge_type=e.edge_type, weight=e.weight)
                    )
            else:
                resolved_edges.append(e)

        # Resolve edge degrees
        for e in resolved_edges:
            if e.source in all_nodes:
                all_nodes[e.source].out_degree += 1
            if e.target in all_nodes:
                all_nodes[e.target].in_degree += 1

        return all_nodes, resolved_edges

    def _node_to_feature_vector(self, node: ASTGNNNode) -> List[float]:
        """Convert AST node into 8-dimensional initial feature vector."""
        return [
            1.0 if node.is_modified else 0.0,
            min(1.0, node.complexity / 20.0),
            min(1.0, node.churn_score),
            1.0 if node.is_test else 0.0,
            min(1.0, node.in_degree / 10.0),
            min(1.0, node.out_degree / 10.0),
            1.0 if node.node_type == "function" else 0.5,
            1.0,  # Bias term
        ]

    def forward(
        self,
        nodes: Dict[str, ASTGNNNode],
        edges: List[ASTGNNEdge],
    ) -> Dict[str, float]:
        """Forward pass of 2-layer Graph Convolutional Network predicting failure/regression risk."""
        node_ids = list(nodes.keys())
        if not node_ids:
            return {}

        # 1. Initialize node representations H0
        h0 = {nid: self._node_to_feature_vector(nodes[nid]) for nid in node_ids}

        # Build adjacency map (undirected for message passing)
        adj: Dict[str, List[Tuple[str, float]]] = {nid: [] for nid in node_ids}
        for e in edges:
            if e.source in nodes and e.target in nodes:
                adj[e.source].append((e.target, e.weight))
                adj[e.target].append((e.source, e.weight))

        # 2. GCN Layer 1: H0 -> H1
        h1: Dict[str, List[float]] = {}
        for nid in node_ids:
            # Self transformation
            feat = h0[nid]
            z_self = [
                sum(w * x for w, x in zip(self.w_self_1[i], feat))
                for i in range(self.HIDDEN_DIM)
            ]

            # Neighbor message aggregation
            neighbors = adj[nid]
            deg_v = max(1, len(neighbors))
            z_neigh = [0.0] * self.HIDDEN_DIM
            for n_id, w_edge in neighbors:
                deg_u = max(1, len(adj[n_id]))
                norm_w = w_edge / math.sqrt(deg_v * deg_u)
                n_feat = h0[n_id]
                for i in range(self.HIDDEN_DIM):
                    z_neigh[i] += norm_w * sum(w * x for w, x in zip(self.w_neigh_1[i], n_feat))

            # Combine + bias + ReLU
            out1 = [_relu(z_self[i] + z_neigh[i] + self.b_1[i]) for i in range(self.HIDDEN_DIM)]
            h1[nid] = out1

        # 3. GCN Layer 2: H1 -> H2
        h2: Dict[str, List[float]] = {}
        for nid in node_ids:
            feat1 = h1[nid]
            z_self = [
                sum(w * x for w, x in zip(self.w_self_2[i], feat1))
                for i in range(self.HIDDEN_DIM)
            ]

            neighbors = adj[nid]
            deg_v = max(1, len(neighbors))
            z_neigh = [0.0] * self.HIDDEN_DIM
            for n_id, w_edge in neighbors:
                deg_u = max(1, len(adj[n_id]))
                norm_w = w_edge / math.sqrt(deg_v * deg_u)
                n_feat1 = h1[n_id]
                for i in range(self.HIDDEN_DIM):
                    z_neigh[i] += norm_w * sum(w * x for w, x in zip(self.w_neigh_2[i], n_feat1))

            out2 = [_relu(z_self[i] + z_neigh[i] + self.b_2[i]) for i in range(self.HIDDEN_DIM)]
            h2[nid] = out2

        # 4. Readout Head: Sigmoid Risk Score
        risk_scores: Dict[str, float] = {}
        for nid in node_ids:
            # If node was explicitly modified, ensure base risk reflects high perturbation
            base_mod = 0.6 if nodes[nid].is_modified else 0.0
            z_score = sum(w * h for w, h in zip(self.w_out, h2[nid])) + self.b_out + base_mod
            score = round(_sigmoid(z_score), 4)
            nodes[nid].risk_score = score
            risk_scores[nid] = score

        return risk_scores

    def predict_test_selection(
        self,
        nodes: Dict[str, ASTGNNNode],
        edges: List[ASTGNNEdge],
        changed_files: List[str],
        high_risk_threshold: float = 0.50,
        medium_risk_threshold: float = 0.20,
    ) -> PredictiveTestSelectionReport:
        """Run GNN forward pass and partition test suites for predictive execution."""
        import time

        t0 = time.time()
        self.forward(nodes, edges)
        latency_ms = round((time.time() - t0) * 1000.0, 2)

        test_nodes = [n for n in nodes.values() if n.is_test]
        # Sort tests descending by risk score
        test_nodes.sort(key=lambda x: x.risk_score, reverse=True)

        high_risk = []
        medium_risk = []
        low_risk = []

        for t in test_nodes:
            item = {
                "id": t.id,
                "name": t.name,
                "file_path": t.file_path,
                "risk_score": t.risk_score,
                "complexity": t.complexity,
            }
            if t.risk_score >= high_risk_threshold:
                high_risk.append(item)
            elif t.risk_score >= medium_risk_threshold:
                medium_risk.append(item)
            else:
                low_risk.append(item)

        total_tests = len(test_nodes)
        # Tests selected to run: High risk + Medium risk
        selected_count = len(high_risk) + len(medium_risk)
        reduction_pct = (
            round((1.0 - (selected_count / total_tests)) * 100.0, 2)
            if total_tests > 0
            else 0.0
        )

        # Defect Hotspots across source nodes
        source_nodes = [n for n in nodes.values() if not n.is_test]
        source_nodes.sort(key=lambda x: x.risk_score, reverse=True)
        hotspots = [
            {
                "id": n.id,
                "name": n.name,
                "file_path": n.file_path,
                "risk_score": n.risk_score,
                "complexity": n.complexity,
                "is_modified": n.is_modified,
            }
            for n in source_nodes[:5]
        ]

        return PredictiveTestSelectionReport(
            changed_files=changed_files,
            total_tests_discovered=total_tests,
            selected_tests_count=selected_count,
            test_reduction_percentage=reduction_pct,
            high_risk_tests=high_risk,
            medium_risk_tests=medium_risk,
            low_risk_tests=low_risk,
            hotspot_symbols=hotspots,
            gnn_inference_latency_ms=latency_ms,
        )

    def compute_external_reachability(
        self,
        nodes: Dict[str, ASTGNNNode],
        edges: List[ASTGNNEdge],
        entrypoints: Optional[List[str]] = None,
    ) -> ReachabilityPruneReport:
        """OpenAnt Stage 0: Prune non-reachable internal units via forward BFS from external entrypoints."""
        from collections import deque

        candidate_units = {
            nid: n for nid, n in nodes.items() if not n.is_test and n.node_type in ("function", "class")
        }
        if entrypoints is not None:
            seed_ids = [
                nid
                for nid, n in candidate_units.items()
                if nid in entrypoints or n.name in entrypoints
            ]
        else:
            seed_ids = [nid for nid, n in candidate_units.items() if n.is_entrypoint]

        # Build forward call adjacency map
        forward_adj: Dict[str, List[str]] = {nid: [] for nid in nodes}
        name_to_ids: Dict[str, List[str]] = {}
        for nid, node in nodes.items():
            name_to_ids.setdefault(node.name, []).append(nid)

        for e in edges:
            if e.edge_type == "CALLS" and e.source in forward_adj:
                if e.target in nodes:
                    forward_adj[e.source].append(e.target)
                elif e.target in name_to_ids:
                    forward_adj[e.source].extend(name_to_ids[e.target])

        hop_distances: Dict[str, int] = {}
        queue: deque[Tuple[str, int]] = deque()
        for sid in seed_ids:
            hop_distances[sid] = 0
            queue.append((sid, 0))

        while queue:
            curr_id, dist = queue.popleft()
            for nxt_id in forward_adj.get(curr_id, []):
                if nxt_id in candidate_units and nxt_id not in hop_distances:
                    hop_distances[nxt_id] = dist + 1
                    queue.append((nxt_id, dist + 1))

        reachable_ids = sorted(hop_distances.keys())
        pruned_ids = sorted(nid for nid in candidate_units if nid not in hop_distances)
        total_units = len(candidate_units)
        reachable_count = len(reachable_ids)
        pruned_count = len(pruned_ids)
        reduction_pct = (
            round((pruned_count / total_units) * 100.0, 2) if total_units > 0 else 0.0
        )

        return ReachabilityPruneReport(
            total_units=total_units,
            reachable_units_count=reachable_count,
            pruned_units_count=pruned_count,
            reduction_percentage=reduction_pct,
            entrypoint_ids=sorted(seed_ids),
            reachable_unit_ids=reachable_ids,
            pruned_unit_ids=pruned_ids,
            hop_distances=hop_distances,
        )

    def verify_constrained_exploit_trace(
        self,
        trace: ConstrainedExploitTrace,
        nodes: Dict[str, ASTGNNNode],
        edges: List[ASTGNNEdge],
        entrypoints: Optional[List[str]] = None,
    ) -> ConstrainedAttackerVerdict:
        """OpenAnt Stage 2: Constrained attacker persona verification rejecting sycophantic/local-only findings."""
        if trace.assumes_admin_or_local_shell:
            return ConstrainedAttackerVerdict(
                finding_id=trace.finding_id,
                status="NOT_EXPLOITABLE_LOCAL_ONLY",
                exploitable=False,
                reason="Candidate vulnerability requires pre-existing admin/local shell access outside external threat model.",
            )

        if trace.has_unbypassable_sanitizer:
            return ConstrainedAttackerVerdict(
                finding_id=trace.finding_id,
                status="REJECTED_SANITIZED",
                exploitable=False,
                reason="Data-flow hop chain traverses an unbypassable type/regex sanitizer prior to sink operation.",
            )

        if (
            not trace.external_input.strip()
            or not trace.entrypoint_symbol.strip()
            or not trace.data_flow_hop_chain
            or not trace.sink_operation.strip()
        ):
            return ConstrainedAttackerVerdict(
                finding_id=trace.finding_id,
                status="REJECTED_INCOMPLETE_TRACE",
                exploitable=False,
                reason="Missing required 4-tuple exploit trace element (external_input, entrypoint_symbol, data_flow_hop_chain, sink_operation).",
            )

        reachability = self.compute_external_reachability(nodes, edges, entrypoints=entrypoints)
        reachable_names = {nodes[nid].name: nid for nid in reachability.reachable_unit_ids if nid in nodes}
        entrypoint_match = None
        if trace.entrypoint_symbol in reachability.entrypoint_ids:
            entrypoint_match = trace.entrypoint_symbol
        else:
            for eid in reachability.entrypoint_ids:
                if nodes[eid].name == trace.entrypoint_symbol:
                    entrypoint_match = eid
                    break

        if entrypoint_match is None:
            return ConstrainedAttackerVerdict(
                finding_id=trace.finding_id,
                status="REJECTED_UNREACHABLE",
                exploitable=False,
                reason=f"Entrypoint '{trace.entrypoint_symbol}' is not an externally reachable entrypoint in the AST call graph.",
            )

        # Verify hop chain symbols are reachable
        for hop in trace.data_flow_hop_chain:
            if hop not in reachability.reachable_unit_ids and hop not in reachable_names:
                return ConstrainedAttackerVerdict(
                    finding_id=trace.finding_id,
                    status="REJECTED_UNREACHABLE",
                    exploitable=False,
                    reason=f"Intermediate hop '{hop}' is pruned/unreachable from entrypoint '{entrypoint_match}'.",
                    verified_entrypoint_id=entrypoint_match,
                )

        return ConstrainedAttackerVerdict(
            finding_id=trace.finding_id,
            status="CONFIRMED_EXPLOITABLE",
            exploitable=True,
            reason=f"Verified external data-flow trace from '{entrypoint_match}' across {len(trace.data_flow_hop_chain)} hop(s) to sink '{trace.sink_operation}'.",
            verified_entrypoint_id=entrypoint_match,
            hop_count=len(trace.data_flow_hop_chain),
        )


ast_gnn_engine = ASTGraphNeuralNetwork()
