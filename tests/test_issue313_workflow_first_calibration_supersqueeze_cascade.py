"""Unit tests for Issue #313: ServiceBotContract, WorkflowFirstGateStage, CalibrationGateStage, SuperSqueezeStage & IterationCascadeContract."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from hath0r_engine import (
    CalibrationGateStage,
    IterationCascadeContract,
    ServiceBotContract,
    SuperSqueezeStage,
    TwoLevelAgentGraphRouter,
    WorkflowFirstGateStage,
)


def test_service_bot_contract_requires_at_least_one_bot() -> None:
    """Verify ServiceBotContract enforces >= 1 owning Bot per CR-FEATURE-WORKFLOW-STANDARD-001."""
    contract = ServiceBotContract(
        service_id="mcp.kb_search",
        service_name="Knowledgebase Search Service",
        owning_bots=("cag-rag-router-bot",),
    )
    assert contract.to_dict()["owning_bots"] == ["cag-rag-router-bot"]

    with pytest.raises(ValueError, match="CR-FEATURE-WORKFLOW-STANDARD-001"):
        ServiceBotContract(
            service_id="orphan.service",
            service_name="Orphan Service",
            owning_bots=(),
        )


def test_workflow_first_gate_stage_matches_or_offers_missing_workflow() -> None:
    """Verify WorkflowFirstGateStage resolves registered workflows or emits MissingWorkflowOffer."""
    stage = WorkflowFirstGateStage(strict_offer=True)

    res_match = stage.evaluate("search knowledgebase for architecture rules")
    assert res_match["allowed"] is True
    assert res_match["matched"] is True
    assert res_match["workflow_id"] == "mcp-kb-retrieval-workflow"

    unmatched_prompt = "synthesize interplanetary gravimetric telemetry"
    res_offer = stage.evaluate(unmatched_prompt)
    assert res_offer["allowed"] is False
    assert res_offer["matched"] is False
    assert res_offer["offer"]["acceptance_test"] == unmatched_prompt
    assert res_offer["offer"]["owning_bots"] == ["mcp-workflow-engine-bot", "factory-manager-bot"]


def test_calibration_gate_stage_enforces_4h_auto_calibration(tmp_path: Path) -> None:
    """Verify CalibrationGateStage auto-calibrates when .hath0r/cccd_state.json is older than 4.0h."""
    state_file = tmp_path / ".hath0r" / "cccd_state.json"
    state_file.parent.mkdir(parents=True)
    now = datetime(2026, 10, 31, 12, 0, 0, tzinfo=timezone.utc)
    expired_ts = (now - timedelta(hours=5, minutes=30)).isoformat()
    state_file.write_text(json.dumps({"calibration_id": 10, "last_calibrated_at": expired_ts}), encoding="utf-8")

    stage = CalibrationGateStage(tmp_path, max_age_hours=4.0)
    res = stage.ensure_calibrated(now=now)
    assert res["is_fresh"] is True
    assert res["auto_calibrated"] is True
    assert res["age_hours"] == 0.0

    # Immediate re-check within 4.0h does not re-trigger calibration
    res_fresh = stage.ensure_calibrated(now=now + timedelta(hours=1))
    assert res_fresh["is_fresh"] is True
    assert res_fresh["auto_calibrated"] is False
    assert res_fresh["age_hours"] == 1.0


def test_supersqueeze_stage_and_iteration_cascade_contract(tmp_path: Path) -> None:
    """Verify SuperSqueezeStage compression, TwoLevelAgentGraphRouter, and IterationCascadeContract."""
    squeeze = SuperSqueezeStage(enabled=True, target_ratio=0.50)
    verbose_context = (
        "# Architecture Header\n"
        "AgentGraph governs Level 1 HATH0R-MCP and Level 2 HATH0R-CLI memory.\n"
        "Unrelated filler sentence number one that does not match query.\n"
        "Unrelated filler sentence number two that does not match query.\n"
        "Unrelated filler sentence number three that does not match query.\n"
        "Unrelated filler sentence number four that does not match query.\n"
    )
    sq_res = squeeze.compress("AgentGraph Level 1 HATH0R-MCP", verbose_context)
    assert sq_res["reduction_ratio"] > 0.0
    assert sq_res["phoenix_span"]["endpoint"] == "http://localhost:38000/phoenix"

    router = TwoLevelAgentGraphRouter()
    assert router.route("kb_search")["level"] == "L1_MCP"
    assert router.route("memory.read")["level"] == "L2_CLI_MEMORY"

    cascade = IterationCascadeContract(tmp_path, strict_order=True, strict_workflow_first=True)
    # Out-of-order Stage 2 is blocked
    assert cascade.run_stage2_cli_mcp("query", verbose_context)["success"] is False

    # Stage 1 -> Stage 2 -> Stage 3 with high confidence blocks Stage 4 (Web)
    assert cascade.run_stage1_task("search knowledgebase")["success"] is True
    assert cascade.run_stage2_cli_mcp("AgentGraph", verbose_context, confidence=0.92)["success"] is True
    assert cascade.run_stage3_computer(confidence=0.90)["success"] is True
    s4_blocked = cascade.run_stage4_web("AgentGraph", verbose_context)
    assert s4_blocked["success"] is False
    assert s4_blocked["status"] == "BLOCKED_LOCAL_KNOWLEDGE_SUFFICIENT"

    # Low confidence (< 0.70) on Stage 2 and Stage 3 permits Stage 4 (Web)
    cascade.stage2_confidence = 0.45
    cascade.stage3_confidence = 0.50
    s4_allowed = cascade.run_stage4_web("AgentGraph", verbose_context)
    assert s4_allowed["success"] is True
    assert s4_allowed["status"] == "STAGE4_COMPLETED_AND_COMPOUNDED"
