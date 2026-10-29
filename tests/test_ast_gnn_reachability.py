"""Unit tests for OpenAnt Static Call-Graph Reachability Pruning & Constrained Attacker Persona (#309)."""

from __future__ import annotations

from pathlib import Path

from hath0r_engine.analysis.ast_gnn import (
    ASTGraphNeuralNetwork,
    ConstrainedExploitTrace,
)


def test_compute_external_reachability_prunes_dead_internal_helpers(tmp_path: Path) -> None:
    src_file = tmp_path / "service.py"
    src_file.write_text(
        '''
import click

@click.command()
def cli_entry(user_query: str) -> str:
    return reachable_helper(user_query)

def reachable_helper(q: str) -> str:
    return sink_runner(q)

def sink_runner(q: str) -> str:
    return q.strip()

def dead_internal_helper(x: int) -> int:
    return orphan_leaf(x + 1)

def orphan_leaf(y: int) -> int:
    return y * 2
''',
        encoding="utf-8",
    )

    gnn = ASTGraphNeuralNetwork()
    nodes, edges = gnn.build_graph_from_directory(tmp_path)
    report = gnn.compute_external_reachability(nodes, edges)

    assert report.total_units == 5
    assert report.reachable_units_count == 3
    assert report.pruned_units_count == 2
    assert report.reduction_percentage == 40.0
    reachable_names = {nodes[nid].name for nid in report.reachable_unit_ids}
    pruned_names = {nodes[nid].name for nid in report.pruned_unit_ids}
    assert reachable_names == {"cli_entry", "reachable_helper", "sink_runner"}
    assert pruned_names == {"dead_internal_helper", "orphan_leaf"}


def test_verify_constrained_exploit_trace_verdicts(tmp_path: Path) -> None:
    src_file = tmp_path / "mcp_handler.py"
    src_file.write_text(
        '''
class DummyMCP:
    def tool(self):
        def dec(fn):
            return fn
        return dec

mcp = DummyMCP()

@mcp.tool()
def kb_query_tool(raw_payload: str) -> str:
    return parse_query(raw_payload)

def parse_query(raw_payload: str) -> str:
    return execute_sink(raw_payload)

def execute_sink(cmd: str) -> str:
    return cmd

def unreachable_admin_debug(cmd: str) -> str:
    return cmd
''',
        encoding="utf-8",
    )

    gnn = ASTGraphNeuralNetwork()
    nodes, edges = gnn.build_graph_from_directory(tmp_path)

    # 1. Valid reachable trace -> CONFIRMED_EXPLOITABLE
    valid_trace = ConstrainedExploitTrace(
        finding_id="FIND-001",
        external_input="JSON-RPC arguments.raw_payload",
        entrypoint_symbol="kb_query_tool",
        data_flow_hop_chain=["kb_query_tool", "parse_query", "execute_sink"],
        sink_operation="subprocess.Popen",
    )
    verdict_ok = gnn.verify_constrained_exploit_trace(valid_trace, nodes, edges)
    assert verdict_ok.exploitable is True
    assert verdict_ok.status == "CONFIRMED_EXPLOITABLE"
    assert verdict_ok.hop_count == 3

    # 2. Local-only / admin assumption -> NOT_EXPLOITABLE_LOCAL_ONLY
    local_trace = ConstrainedExploitTrace(
        finding_id="FIND-002",
        external_input="Local shell argv",
        entrypoint_symbol="kb_query_tool",
        data_flow_hop_chain=["kb_query_tool"],
        sink_operation="os.system",
        assumes_admin_or_local_shell=True,
    )
    verdict_local = gnn.verify_constrained_exploit_trace(local_trace, nodes, edges)
    assert verdict_local.exploitable is False
    assert verdict_local.status == "NOT_EXPLOITABLE_LOCAL_ONLY"

    # 3. Unreachable hop -> REJECTED_UNREACHABLE
    unreachable_trace = ConstrainedExploitTrace(
        finding_id="FIND-003",
        external_input="HTTP body",
        entrypoint_symbol="kb_query_tool",
        data_flow_hop_chain=["kb_query_tool", "unreachable_admin_debug"],
        sink_operation="eval",
    )
    verdict_unreach = gnn.verify_constrained_exploit_trace(unreachable_trace, nodes, edges)
    assert verdict_unreach.exploitable is False
    assert verdict_unreach.status == "REJECTED_UNREACHABLE"

    # 4. Sanitized path -> REJECTED_SANITIZED
    sanitized_trace = ConstrainedExploitTrace(
        finding_id="FIND-004",
        external_input="HTTP body",
        entrypoint_symbol="kb_query_tool",
        data_flow_hop_chain=["kb_query_tool", "parse_query"],
        sink_operation="sql.execute",
        has_unbypassable_sanitizer=True,
    )
    verdict_sanitized = gnn.verify_constrained_exploit_trace(sanitized_trace, nodes, edges)
    assert verdict_sanitized.exploitable is False
    assert verdict_sanitized.status == "REJECTED_SANITIZED"
