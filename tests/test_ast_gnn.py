"""Unit tests for AST Graph Neural Network (GNN) and Predictive Test Selection."""

from pathlib import Path

from hath0r_engine.analysis.ast_gnn import (
    ASTGNNEdge,
    ASTGNNNode,
    ASTGraphNeuralNetwork,
    PredictiveTestSelectionReport,
)


def test_ast_gnn_forward_pass_and_risk_propagation():
    gnn = ASTGraphNeuralNetwork(random_seed=42)

    # Synthetic graph: Module M -> Function F (modified) -> Called by Test T
    nodes = {
        "m1": ASTGNNNode(id="m1", name="module.py", file_path="src/module.py", node_type="module", is_modified=True),
        "f1": ASTGNNNode(id="f1", name="compute_tax", file_path="src/module.py", node_type="function", complexity=5.0, is_modified=True),
        "f2": ASTGNNNode(id="f2", name="unrelated_func", file_path="src/other.py", node_type="function", complexity=1.0, is_modified=False),
        "t1": ASTGNNNode(id="t1", name="test_compute_tax", file_path="tests/test_mod.py", node_type="test", is_test=True),
        "t2": ASTGNNNode(id="t2", name="test_other", file_path="tests/test_other.py", node_type="test", is_test=True),
    }

    edges = [
        ASTGNNEdge(source="m1", target="f1", edge_type="CONTAINS"),
        ASTGNNEdge(source="t1", target="f1", edge_type="TESTS", weight=1.0),
        ASTGNNEdge(source="t2", target="f2", edge_type="TESTS", weight=1.0),
    ]

    scores = gnn.forward(nodes, edges)
    assert len(scores) == 5
    assert all(0.0 <= s <= 1.0 for s in scores.values())

    # Risk of modified function and its testing function must be higher than unmodified function
    assert scores["f1"] > scores["f2"]
    assert scores["t1"] > scores["t2"]


def test_predict_test_selection_report():
    gnn = ASTGraphNeuralNetwork(random_seed=42)

    nodes = {
        "src/calc.py::add": ASTGNNNode(
            id="src/calc.py::add",
            name="add",
            file_path="src/calc.py",
            node_type="function",
            is_modified=True,
            complexity=2.0,
        ),
        "tests/test_calc.py::test_add": ASTGNNNode(
            id="tests/test_calc.py::test_add",
            name="test_add",
            file_path="tests/test_calc.py",
            node_type="test",
            is_test=True,
        ),
        "tests/test_unrelated.py::test_network": ASTGNNNode(
            id="tests/test_unrelated.py::test_network",
            name="test_network",
            file_path="tests/test_unrelated.py",
            node_type="test",
            is_test=True,
        ),
    }

    edges = [
        ASTGNNEdge(source="tests/test_calc.py::test_add", target="src/calc.py::add", edge_type="TESTS"),
    ]

    report = gnn.predict_test_selection(nodes, edges, changed_files=["src/calc.py"])
    assert isinstance(report, PredictiveTestSelectionReport)
    assert report.total_tests_discovered == 2
    assert report.gnn_inference_latency_ms < 50.0  # Fast inference
    assert len(report.high_risk_tests) + len(report.medium_risk_tests) >= 1
    # test_add has higher risk than test_network
    test_add_risk = nodes["tests/test_calc.py::test_add"].risk_score
    test_net_risk = nodes["tests/test_unrelated.py::test_network"].risk_score
    assert test_add_risk > test_net_risk


def test_build_graph_from_directory(tmp_path: Path):
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    (src_dir / "math_ops.py").write_text("def multiply(a, b):\n    return a * b\n")

    test_dir = tmp_path / "tests"
    test_dir.mkdir()
    (test_dir / "test_math.py").write_text("def test_multiply():\n    multiply(2, 3)\n")

    gnn = ASTGraphNeuralNetwork()
    nodes, edges = gnn.build_graph_from_directory(tmp_path, changed_files=["src/math_ops.py"])

    assert len(nodes) >= 2
    assert any(n.is_modified for n in nodes.values())
    assert any(n.is_test for n in nodes.values())
