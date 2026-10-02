"""Unit tests for Durable Execution, Event-Sourced Checkpointing, and Human Hibernation Gate."""

import tempfile
from pathlib import Path

import pytest

from hath0r_engine.orchestration import (
    DurableWorkflowEngine,
    EventJournal,
    EventType,
    WorkflowStatus,
    WorkflowSuspendedException,
    durable_task,
)


def test_event_journal_append_and_query():
    journal = EventJournal(":memory:")
    wf_id = "wf-test-001"

    e1 = journal.append_event(
        workflow_id=wf_id,
        event_type=EventType.WORKFLOW_STARTED,
        payload={"task": "migration"},
    )
    assert e1.seq_num == 1
    assert e1.workflow_id == wf_id

    e2 = journal.append_event(
        workflow_id=wf_id,
        event_type=EventType.STEP_COMPLETED,
        step_name="step_extract",
        idempotency_key="step:extract",
        payload={"result": {"tables": ["users", "orders"]}},
    )
    assert e2.seq_num == 2

    # Query events
    events = journal.get_events(wf_id)
    assert len(events) == 2
    assert events[0].seq_num == 1
    assert events[1].seq_num == 2

    # Check memoized result
    cached = journal.find_step_result(wf_id, "step:extract")
    assert cached == {"tables": ["users", "orders"]}

    # Non-existent key
    assert journal.find_step_result(wf_id, "step:missing") is None


def test_durable_workflow_engine_step_memoization_and_replay():
    with tempfile.TemporaryDirectory() as tmp_dir:
        db_path = str(Path(tmp_dir) / "workflow.db")
        journal = EventJournal(db_path)
        wf_id = "wf-dedup-001"

        engine1 = DurableWorkflowEngine(workflow_id=wf_id, journal=journal)

        execution_counter = {"step1": 0, "step2": 0}

        def step1_fn():
            execution_counter["step1"] += 1
            return "step1_output"

        def step2_fn():
            execution_counter["step2"] += 1
            return "step2_output"

        # First run
        r1 = engine1.run_step("step1", step1_fn)
        r2 = engine1.run_step("step2", step2_fn)
        engine1.mutate_state("user_id", "usr_123")
        assert r1 == "step1_output"
        assert r2 == "step2_output"
        assert execution_counter["step1"] == 1
        assert execution_counter["step2"] == 1

        # Simulate process crash and restart: create new engine with same persistent journal
        journal2 = EventJournal(db_path)
        engine2 = DurableWorkflowEngine(workflow_id=wf_id, journal=journal2)

        # State should be reconstructed
        assert engine2.get_state("user_id") == "usr_123"
        assert engine2.status == WorkflowStatus.RUNNING

        # Re-running the steps MUST return cached result and NOT call step1_fn or step2_fn again!
        r1_cached = engine2.run_step("step1", step1_fn)
        r2_cached = engine2.run_step("step2", step2_fn)
        assert r1_cached == "step1_output"
        assert r2_cached == "step2_output"
        assert execution_counter["step1"] == 1
        assert execution_counter["step2"] == 1

        # Complete workflow
        engine2.complete(output={"status": "success", "processed": 2})
        assert engine2.status == WorkflowStatus.COMPLETED
        assert engine2.output == {"status": "success", "processed": 2}


def test_human_hibernation_gate_pause_and_resume():
    journal = EventJournal(":memory:")
    wf_id = "wf-gate-001"

    engine = DurableWorkflowEngine(workflow_id=wf_id, journal=journal)

    # Step 1 executes
    engine.run_step("prepare_payload", lambda: {"deploy_target": "production"})

    # Step 2: Hits Human Gate -> raises WorkflowSuspendedException
    with pytest.raises(WorkflowSuspendedException) as exc_info:
        engine.pause_for_human(
            gate_name="approve_prod_deploy",
            prompt="Authorize production deployment?",
            required_role="release_manager",
        )
    assert exc_info.value.gate_request.gate_name == "approve_prod_deploy"
    assert engine.status == WorkflowStatus.SUSPENDED

    # External signal arrives
    engine.signal_human_approval(
        gate_name="approve_prod_deploy",
        approved=True,
        payload={"reviewer": "somesayray", "timestamp": "2026-09-30T07:00:00Z"},
    )
    assert engine.status == WorkflowStatus.RUNNING

    # Resume execution of same workflow logic: pause_for_human now returns the decision
    approval = engine.pause_for_human(
        gate_name="approve_prod_deploy",
        prompt="Authorize production deployment?",
    )
    assert approval["approved"] is True
    assert approval["decision_payload"]["reviewer"] == "somesayray"

    # Step 3 completes after approval
    res = engine.run_step("deploy_production", lambda: {"deployed": True})
    assert res == {"deployed": True}
    engine.complete(output={"success": True})
    assert engine.status == WorkflowStatus.COMPLETED


def test_durable_task_decorator():
    @durable_task(workflow_id_param="task_id")
    def run_agent_job(task_id: str, workflow_engine: DurableWorkflowEngine = None):
        step_val = workflow_engine.run_step("compute", lambda: 100 * 2)
        workflow_engine.complete(output={"result": step_val})
        return workflow_engine.output

    out = run_agent_job(task_id="job-42")
    assert out == {"result": 200}
