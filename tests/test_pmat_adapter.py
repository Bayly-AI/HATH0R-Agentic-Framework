"""Unit and integration tests for PMAT Churn Engine Substrate and Generative UI."""

from pathlib import Path

from hath0r_engine.analysis.pmat_adapter import PmatAdapter
from hath0r_engine.gateway.base import ComplexityTier
from hath0r_engine.gateway.routing import TieredRouter
from hath0r_engine.graph.agent_graph import AgentGraphEngine
from hath0r_engine.ui.churn_heatmap import ChurnHeatmapComponent
from hath0r_engine.ui.protocol import EvidenceType


def test_pmat_adapter_git_analysis():
    repo_root = Path(__file__).parent.parent
    adapter = PmatAdapter()

    report = adapter.analyze_churn(repo_root, days=60)
    assert report["schema_version"] == "hath0r.pmat.churn/1"
    assert "summary" in report
    assert "hotspots" in report

    summary = report["summary"]
    assert summary["total_files_analyzed"] >= 1
    assert summary["total_commits_evaluated"] >= 1
    assert summary["total_churn_lines"] >= 1
    assert 0.0 <= summary["mean_volatility_score"] <= 1.0

    hotspots = report["hotspots"]
    assert len(hotspots) >= 1
    first = hotspots[0]
    assert "file_path" in first
    assert "churn_count" in first
    assert "complexity_score" in first
    assert "volatility_score" in first
    assert first["risk_tier"] in ("LOW", "MEDIUM", "HIGH", "CRITICAL")


def test_pmat_adapter_hotspots_and_pr_risk():
    repo_root = Path(__file__).parent.parent
    adapter = PmatAdapter()

    hotspots = adapter.get_hotspots(repo_root, days=60, limit=5)
    assert len(hotspots) <= 5
    if len(hotspots) > 1:
        assert hotspots[0]["volatility_score"] >= hotspots[1]["volatility_score"]

    risk_eval = adapter.evaluate_pr_risk(repo_root, base_branch="development")
    assert "overall_risk_tier" in risk_eval
    assert "safe_to_merge" in risk_eval
    assert "recommended_reasoning_tier" in risk_eval
    assert risk_eval["recommended_reasoning_tier"] in ("LIGHT", "STANDARD", "REASONING")


def test_pmat_adapter_agentgraph_ingestion():
    repo_root = Path(__file__).parent.parent
    adapter = PmatAdapter()
    agent_graph = AgentGraphEngine()

    report = adapter.analyze_churn(repo_root, days=60)
    ingested = adapter.ingest_into_agentgraph(report, agent_graph)
    assert ingested > 0

    # Verify nodes in knowledge plane
    knowledge_nodes = [n for n in agent_graph.nodes.values() if n.plane == "knowledge"]
    assert len(knowledge_nodes) > 0


def test_tiered_router_volatility_escalation():
    router = TieredRouter()
    assert router.escalate_tier_from_volatility(0.85) == ComplexityTier.REASONING
    assert router.escalate_tier_from_volatility(0.45) == ComplexityTier.STANDARD
    assert router.escalate_tier_from_volatility(0.15) == ComplexityTier.LIGHT


def test_churn_heatmap_generative_ui_and_html():
    sample_report = {
        "schema_version": "hath0r.pmat.churn/1",
        "repository": "hath0r-framework",
        "commit_hash": "a1b2c3d4",
        "analysis_window_days": 30,
        "summary": {
            "total_files_analyzed": 12,
            "total_commits_evaluated": 45,
            "total_churn_lines": 3400,
            "mean_volatility_score": 0.42,
            "hotspot_count": 3,
        },
        "hotspots": [
            {
                "file_path": "src/hath0r_engine/gateway/client.py",
                "churn_count": 8,
                "lines_added": 300,
                "lines_deleted": 120,
                "complexity_score": 14.5,
                "volatility_score": 0.82,
                "risk_tier": "CRITICAL",
                "co_changing_files": ["src/hath0r_engine/telemetry/otel_tracer.py"],
            },
            {
                "file_path": "src/hath0r_engine/telemetry/otel_tracer.py",
                "churn_count": 6,
                "lines_added": 180,
                "lines_deleted": 40,
                "complexity_score": 8.0,
                "volatility_score": 0.55,
                "risk_tier": "HIGH",
                "co_changing_files": ["src/hath0r_engine/gateway/client.py"],
            },
        ],
        "recommendations": ["Refactor client.py to isolate provider implementations"],
    }

    comp = ChurnHeatmapComponent(report_data=sample_report)
    evidence = comp.to_evidence_component()
    assert evidence.type == EvidenceType.CHURN_HEATMAP
    assert evidence.props["repository"] == "hath0r-framework"
    assert len(evidence.props["data_points"]) == 2

    html = comp.render_html()
    assert "<!DOCTYPE html>" in html
    assert "data-testid=\"churn-heatmap-widget\"" in html
    assert "data-testid=\"hotspot-table\"" in html
    assert "src/hath0r_engine/gateway/client.py" in html
