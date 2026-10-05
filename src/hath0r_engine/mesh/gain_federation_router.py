"""GAIN Federated Agent-to-Agent (A2A) Mesh Router Substrate."""

from __future__ import annotations

import datetime
import hashlib
import hmac
import json
import uuid
from typing import Any, Dict, List, Optional

from hath0r_engine.graph.agent_graph import AgentGraphEngine, AgentGraphNode, AgentGraphPlane


class GainFederationRouter:
    """Federated Peer-to-Peer Router for GAIN Agent-to-Agent mesh communications."""

    def __init__(self, agent_id: str = "agent-local", secret_key: str = "hath0r-gain-secret-key") -> None:
        self.agent_id = agent_id
        self.secret_key = secret_key.encode("utf-8")
        self.peers: Dict[str, Dict[str, Any]] = {}
        self.session_journal: List[Dict[str, Any]] = []

    def register_peer(self, peer_id: str, endpoint: str, capabilities: List[str]) -> None:
        """Register a peer agent node in the federation mesh."""
        self.peers[peer_id] = {
            "peer_id": peer_id,
            "endpoint": endpoint,
            "capabilities": capabilities,
            "last_seen": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }

    def sign_envelope(
        self,
        recipient_id: str,
        payload_type: str,
        payload: Dict[str, Any],
        allowed_tools: Optional[List[str]] = None,
        ttl_seconds: int = 300,
    ) -> Dict[str, Any]:
        """Serialize and cryptographically sign a GAIN A2A mesh envelope."""
        now = datetime.datetime.now(datetime.timezone.utc)
        until = now + datetime.timedelta(seconds=ttl_seconds)

        envelope = {
            "schema_version": "hath0r.gain.envelope/1",
            "envelope_id": f"env-{uuid.uuid4().hex[:12]}",
            "sender_agent_id": self.agent_id,
            "recipient_agent_id": recipient_id,
            "timestamp": now.isoformat(),
            "valid_until": until.isoformat(),
            "payload_type": payload_type,
            "payload": payload,
            "allowed_tools": allowed_tools or ["view_file", "search_code"],
        }

        # Sign canonical payload string with HMAC-SHA256
        message_bytes = json.dumps(envelope, sort_keys=True).encode("utf-8")
        sig = hmac.new(self.secret_key, message_bytes, hashlib.sha256).hexdigest()
        envelope["signature_hmac"] = sig

        self.session_journal.append(envelope)
        return envelope

    def verify_envelope(self, envelope: Dict[str, Any]) -> bool:
        """Validate HMAC SHA-256 signature and temporal validity of a GAIN envelope."""
        if envelope.get("schema_version") != "hath0r.gain.envelope/1":
            return False

        sig = envelope.get("signature_hmac", "")
        env_copy = dict(envelope)
        env_copy.pop("signature_hmac", None)

        message_bytes = json.dumps(env_copy, sort_keys=True).encode("utf-8")
        expected_sig = hmac.new(self.secret_key, message_bytes, hashlib.sha256).hexdigest()

        if not hmac.compare_digest(sig, expected_sig):
            return False

        # Check temporal validity
        valid_until_str = envelope.get("valid_until")
        if valid_until_str:
            try:
                until_dt = datetime.datetime.fromisoformat(valid_until_str)
                now_dt = datetime.datetime.now(datetime.timezone.utc)
                if now_dt > until_dt:
                    return False
            except ValueError:
                return False

        return True

    def route_agentgraph_query(self, peer_id: str, topic_query: str, agent_graph: AgentGraphEngine) -> Dict[str, Any]:
        """Route remote cross-workspace AgentGraph query through GAIN mesh."""
        payload = {"topic_query": topic_query, "as_of": datetime.datetime.now(datetime.timezone.utc).isoformat()}
        envelope = self.sign_envelope(recipient_id=peer_id, payload_type="AGENTGRAPH_QUERY", payload=payload)

        # Local resolution
        nodes = agent_graph.query(topic_query) if hasattr(agent_graph, "query") else []
        return {
            "envelope": envelope,
            "resolved_peer": peer_id,
            "nodes_found": len(nodes),
            "status": "DELIVERED",
        }


gain_federation_router = GainFederationRouter()
