"""AST Graph Neural Network (GNN) Engine for Predictive Test Selection & Defect Hotspots.

Uses Graph Convolutional Networks (GCN) over Abstract Syntax Tree (AST) call graphs,
import dependencies, and test mappings to predict regression risk scores.
Enables Predictive Test Selection (PTS) to accelerate CI cycles by running high-risk tests first.
"""

from __future__ import annotations

import ast
import math
import os
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


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
                fn_node = ASTGNNNode(
                    id=fn_id,
                    name=stmt.name,
                    file_path=rel_path,
                    node_type="test" if is_test_fn else "function",
                    complexity=float(1 + branches),
                    is_test=is_test_fn,
                )
                nodes.append(fn_node)
                edges.append(ASTGNNEdge(source=file_node_id, target=fn_id, edge_type="CONTAINS", weight=0.5))

                # Extract calls inside function
                for sub in ast.walk(stmt):
                    if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name):
                        called_target = sub.func.id
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

        # Resolve edge degrees
        for e in all_edges:
            if e.source in all_nodes:
                all_nodes[e.source].out_degree += 1
            if e.target in all_nodes:
                all_nodes[e.target].in_degree += 1

        return all_nodes, all_edges

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
        risk_scores = self.forward(nodes, edges)
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


ast_gnn_engine = ASTGraphNeuralNetwork()
