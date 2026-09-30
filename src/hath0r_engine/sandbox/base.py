"""Zero-Trust Isolated Compute Provider Base Interfaces and Data Models."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class SandboxType(str, Enum):
    """Supported sandbox provider backends."""

    E2B = "e2b"
    DAYTONA = "daytona"
    LOCAL = "local"
    WASM = "wasm"


@dataclass
class NetworkPolicy:
    """Network egress restrictions for isolated sandbox instances."""

    block_all: bool = True
    allow_all: bool = False
    allowed_domains: List[str] = field(default_factory=list)

    def is_domain_allowed(self, domain: str) -> bool:
        if self.allow_all:
            return True
        if self.block_all and not self.allowed_domains:
            return False
        return domain.lower() in [d.lower() for d in self.allowed_domains]


@dataclass
class SandboxConfig:
    """Configuration options for launching isolated sandbox instances."""

    provider_type: SandboxType = SandboxType.LOCAL
    template: str = "default"
    timeout_seconds: float = 300.0
    network_policy: Optional[NetworkPolicy] = None
    env: Dict[str, str] = field(default_factory=dict)
    memory_mb: int = 1024
    cpu_count: int = 2
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ExecutionResult:
    """Output and performance metrics from sandboxed command execution."""

    exit_code: int
    stdout: str
    stderr: str
    duration_ms: float
    timed_out: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def succeeded(self) -> bool:
        return self.exit_code == 0 and not self.timed_out

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SandboxProvider(ABC):
    """Abstract interface for all zero-trust isolated compute providers."""

    def __init__(self) -> None:
        self.instance_id: Optional[str] = None
        self.config: Optional[SandboxConfig] = None
        self._running: bool = False

    @abstractmethod
    def start(self, config: SandboxConfig) -> str:
        """Provision and launch the isolated sandbox environment."""
        pass

    @abstractmethod
    def exec(
        self,
        command: str,
        timeout: Optional[float] = None,
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[str] = None,
    ) -> ExecutionResult:
        """Execute a command within the isolated sandbox."""
        pass

    @abstractmethod
    def read_file(self, path: str) -> bytes:
        """Read a file from the sandbox filesystem."""
        pass

    @abstractmethod
    def write_file(self, path: str, data: bytes) -> None:
        """Write content to a file inside the sandbox filesystem."""
        pass

    @abstractmethod
    def sync_files(self, source_dir: str, target_dir: str) -> int:
        """Synchronize files between local host filesystem and sandbox."""
        pass

    @abstractmethod
    def snapshot(self, label: str) -> str:
        """Create a point-in-time snapshot of the sandbox state."""
        pass

    @abstractmethod
    def terminate(self) -> None:
        """Terminate the sandbox and securely wipe all compute and filesystem state."""
        pass

    def is_running(self) -> bool:
        """Check whether the sandbox instance is active."""
        return self._running
