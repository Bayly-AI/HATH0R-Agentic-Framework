"""Enterprise Caller Identity and Security Context for MCP Fleets."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class CallerIdentity:
    """Enterprise caller identity encapsulating tenant, user, scopes, and auth tokens."""

    tenant_id: str = "default"
    user_id: str = "anonymous"
    session_id: Optional[str] = None
    roles: List[str] = field(default_factory=list)
    scopes: List[str] = field(default_factory=list)
    auth_token: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def has_scope(self, required_scope: str) -> bool:
        """Check whether caller possesses a required scope or admin wildcard."""
        if "*" in self.scopes or "admin" in self.roles:
            return True
        return required_scope in self.scopes

    def to_headers(self) -> Dict[str, str]:
        """Generate downstream HTTP / MCP transport headers."""
        headers = {
            "X-Tenant-Id": self.tenant_id,
            "X-User-Id": self.user_id,
        }
        if self.session_id:
            headers["X-Session-Id"] = self.session_id
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        if self.scopes:
            headers["X-Auth-Scopes"] = ",".join(self.scopes)
        if self.roles:
            headers["X-Auth-Roles"] = ",".join(self.roles)
        return headers
