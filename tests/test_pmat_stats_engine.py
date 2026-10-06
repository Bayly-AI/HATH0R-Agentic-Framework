"""Unit tests for PmatStatsEngine substrate."""

from pathlib import Path
import pytest

from hath0r_engine.analysis.pmat_stats_engine import PmatStatsEngine, pmat_stats_engine
from hath0r_engine.graph.agent_graph import AgentGraphEngine


def test_calculate_ast_complexity(tmp_path: Path):
    sample_file = tmp_path / "sample.py"
    sample_file.write_text(
        """
def complex_fn(a, b):
    if a > 0:
        for i in range(b):
            if i % 2 == 0:
                print("even")
            else:
                print("odd")
    return a + b
"""
    )
    engine = PmatStatsEngine()
    metrics = engine.calculate_ast_complexity(sample_file)

    assert metrics["cyclomatic_complexity"] >= 4.0
    assert metrics["cognitive_complexity"] >= 2.0
    assert metrics["max_ast_depth"] >= 2
    assert metrics["halstead_volume"] > 0.0


def test_calculate_provability_score(tmp_path: Path):
    sample_file = tmp_path / "typed_sample.py"
    sample_file.write_text(
        """
from typing import Optional

def safe_add(a: int, b: int) -> int:
    \"\"\"Calculates sum of two integers safely.\"\"\"
    assert isinstance(a, int)
    assert isinstance(b, int)
    return a + b
"""
    )
    engine = PmatStatsEngine()
    prov = engine.calculate_provability_score(sample_file)

    assert prov["formal_verification_coverage"] > 0.50
    assert prov["invariant_safety_score"] > 0.50
    assert prov["defect_probability_index"] < 0.50
    assert prov["provability_score"] > 0.50


def test_generate_multi_dimensional_report(tmp_path: Path):
    engine = PmatStatsEngine()
    report = engine.generate_multi_dimensional_report(repo_path=Path("."), days=30)

    assert report["schema_version"] == "hath0r.pmat.stats/1"
    assert "summary" in report
    assert "churn" in report
    assert "provability" in report
    assert "complexity" in report
    assert "hotspots" in report
    assert isinstance(report["hotspots"], list)


def test_ingest_into_agentgraph(tmp_path: Path):
    engine = PmatStatsEngine()
    report = engine.generate_multi_dimensional_report(repo_path=Path("."), days=30)

    ag_engine = AgentGraphEngine()
    count = engine.ingest_into_agentgraph(report, ag_engine)
    assert count == len(report["hotspots"])
