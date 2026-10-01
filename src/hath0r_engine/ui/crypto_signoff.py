"""Cryptographic Signature Generation for Evidence Handshake Sign-Offs."""

from __future__ import annotations

import hashlib
import hmac
import json


def generate_cryptographic_signature(
    session_id: str,
    task_name: str,
    reviewer: str,
    decision: bool,
    timestamp: str,
    secret_key: str = "hath0r-handshake-secret",
) -> str:
    """Generate deterministic HMAC SHA-256 signature for immutable sign-off verification."""
    payload = {
        "session_id": session_id,
        "task_name": task_name,
        "reviewer": reviewer,
        "decision": decision,
        "timestamp": timestamp,
    }
    canonical_json = json.dumps(payload, sort_keys=True)
    return hmac.new(
        secret_key.encode("utf-8"),
        canonical_json.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
