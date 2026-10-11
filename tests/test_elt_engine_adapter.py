"""Unit tests for ELTEngineAdapter in Hath0r Cognitive Substrate."""

from pathlib import Path

import pytest

from hath0r_engine.graph.knowledge_graph import KnowledgeGraph
from hath0r_engine.orchestration.elt_adapter import ELTEngineAdapter
from hath0r_engine.orchestration.journal import EventRecord, EventType


@pytest.fixture
def temp_adapter(tmp_path: Path) -> ELTEngineAdapter:
    """Fixture providing isolated ELTEngineAdapter with temp SQLite store."""
    db_file = tmp_path / "raw_staging.sqlite"
    return ELTEngineAdapter(db_path=db_file)


def test_stage_event_and_deduplication(temp_adapter: ELTEngineAdapter):
    """Verify event staging and cryptographic deduplication."""
    evt = EventRecord(
        workflow_id="wf-test-1",
        seq_num=1,
        event_type=EventType.STEP_COMPLETED,
        step_name="verify_auth",
        payload={"result": "ok", "duration_ms": 12.5},
    )

    res1 = temp_adapter.stage_event(evt)
    assert res1["status"] == "staged"
    assert res1["is_duplicate"] is False
    assert res1["record_id"] > 0

    # Staging same event should detect duplicate
    res2 = temp_adapter.stage_event(evt)
    assert res2["is_duplicate"] is True
    assert res2["record_id"] == res1["record_id"]


def test_project_to_agentgraph(temp_adapter: ELTEngineAdapter):
    """Verify raw document staging and projection into KnowledgeGraph."""
    doc_path = "docs/governance/test-policy.md"
    doc_content = "# Governance Policy\n\nAll PRs require issue tracking."
    temp_adapter.stage_document(path=doc_path, content=doc_content)

    kg = KnowledgeGraph()
    count = temp_adapter.project_to_agentgraph(kg)
    assert count == 1

    # Verify node in KnowledgeGraph
    node = kg.nodes.get("doc:docs_governance_test-policy_md")
    assert node is not None
    assert node.title == "Governance Policy"
    assert "All PRs require issue tracking" in node.content

    # Re-projecting should be idempotent (0 newly projected)
    count2 = temp_adapter.project_to_agentgraph(kg)
    assert count2 == 0


def test_reflection_event_retrieval(temp_adapter: ELTEngineAdapter):
    """Verify retrieving raw events for MemoryGraph reflection consolidation."""
    for i in range(3):
        temp_adapter.stage_event(
            {"workflow_id": "wf-agent", "seq_num": i, "action": f"tool_call_{i}"}
        )

    events = temp_adapter.get_events_for_reflection(limit=10)
    assert len(events) == 3
    assert events[0]["payload"]["action"] == "tool_call_0"
    assert events[2]["payload"]["action"] == "tool_call_2"
