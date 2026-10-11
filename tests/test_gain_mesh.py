"""Unit tests for GAIN Federated Agent-to-Agent (A2A) Mesh Router."""

import datetime
from hath0r_engine.mesh.gain_federation_router import GainFederationRouter, gain_federation_router
from hath0r_engine.graph.agent_graph import AgentGraphEngine


def test_sign_and_verify_envelope():
    router = GainFederationRouter(agent_id="agent-01", secret_key="test-key")
    env = router.sign_envelope(
        recipient_id="agent-02",
        payload_type="TASK_DELEGATION",
        payload={"task": "Run security audit"},
        ttl_seconds=300,
    )

    assert env["schema_version"] == "hath0r.gain.envelope/1"
    assert env["sender_agent_id"] == "agent-01"
    assert env["recipient_agent_id"] == "agent-02"
    assert "signature_hmac" in env

    assert router.verify_envelope(env) is True


def test_tampered_envelope_rejected():
    router = GainFederationRouter(agent_id="agent-01", secret_key="test-key")
    env = router.sign_envelope(
        recipient_id="agent-02",
        payload_type="TASK_DELEGATION",
        payload={"task": "Run security audit"},
    )

    # Tamper with payload
    env["payload"]["task"] = "Malicious injection"
    assert router.verify_envelope(env) is False


def test_expired_envelope_rejected():
    router = GainFederationRouter(agent_id="agent-01", secret_key="test-key")
    env = router.sign_envelope(
        recipient_id="agent-02",
        payload_type="TASK_DELEGATION",
        payload={"task": "Quick check"},
        ttl_seconds=-10,  # Expired
    )

    assert router.verify_envelope(env) is False


def test_route_agentgraph_query():
    router = GainFederationRouter(agent_id="agent-01", secret_key="test-key")
    ag_engine = AgentGraphEngine()

    res = router.route_agentgraph_query(peer_id="agent-02", topic_query="governance", agent_graph=ag_engine)
    assert res["status"] == "DELIVERED"
    assert res["resolved_peer"] == "agent-02"
    assert router.verify_envelope(res["envelope"]) is True
