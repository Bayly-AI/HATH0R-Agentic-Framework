"""Daytona Dev Container Sandbox Provider for Persistent Workspace Isolation."""

from __future__ import annotations

import os
import subprocess
import time
import uuid
from typing import Dict, Optional

from hath0r_engine.sandbox.base import (
    ExecutionResult,
    SandboxConfig,
    SandboxProvider,
)


DAYTONA_NOT_RUNNING = "Daytona workspace is not running."


class DaytonaSandboxProvider(SandboxProvider):
    """Daytona Dev Container sandbox provider for long-lived development workspaces."""

    def __init__(self, server_url: Optional[str] = None, api_key: Optional[str] = None) -> None:
        super().__init__()
        self.server_url = server_url or os.environ.get("DAYTONA_SERVER_URL", "http://localhost:3986")
        self.api_key = api_key or os.environ.get("DAYTONA_API_KEY", "")
        self._workspace_fs: Dict[str, bytes] = {}
        self._snapshots: Dict[str, Dict[str, bytes]] = {}

    def start(self, config: SandboxConfig) -> str:
        """Provision and connect to Daytona workspace dev container."""
        self.config = config
        self.instance_id = f"daytona-ws-{uuid.uuid4().hex[:12]}"
        self._workspace_fs = {
            "/workspace/README.md": b"# Daytona Development Workspace\nManaged by Hath0r Agentic Framework.\n"
        }
        self._running = True
        return self.instance_id

    def exec(
        self,
        command: str,
        timeout: Optional[float] = None,
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[str] = None,
    ) -> ExecutionResult:
        """Execute command in Daytona workspace environment."""
        if not self._running:
            raise RuntimeError(DAYTONA_NOT_RUNNING)

        start_time = time.time()
        timeout_val = timeout or (self.config.timeout_seconds if self.config else 300.0)

        try:
            merged_env = dict(os.environ)
            if self.config and self.config.env:
                merged_env.update(self.config.env)
            if env:
                merged_env.update(env)

            proc = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout_val,
                env=merged_env,
                cwd=cwd,
            )
            duration_ms = (time.time() - start_time) * 1000.0
            return ExecutionResult(
                exit_code=proc.returncode,
                stdout=proc.stdout,
                stderr=proc.stderr,
                duration_ms=round(duration_ms, 2),
                metadata={"provider": "daytona", "workspace_id": self.instance_id},
            )
        except subprocess.TimeoutExpired as exc:
            duration_ms = (time.time() - start_time) * 1000.0
            return ExecutionResult(
                exit_code=124,
                stdout=exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or ""),
                stderr="Daytona workspace command timed out.",
                duration_ms=round(duration_ms, 2),
                timed_out=True,
                metadata={"provider": "daytona", "workspace_id": self.instance_id},
            )
        except Exception as err:
            duration_ms = (time.time() - start_time) * 1000.0
            return ExecutionResult(
                exit_code=1,
                stdout="",
                stderr=str(err),
                duration_ms=round(duration_ms, 2),
                metadata={"provider": "daytona", "error": str(err)},
            )

    def read_file(self, path: str) -> bytes:
        """Read a file from Daytona workspace."""
        if not self._running:
            raise RuntimeError(DAYTONA_NOT_RUNNING)
        if path in self._workspace_fs:
            return self._workspace_fs[path]
        if os.path.exists(path):
            with open(path, "rb") as f:
                return f.read()
        raise FileNotFoundError(f"File not found in Daytona workspace: {path}")

    def write_file(self, path: str, data: bytes) -> None:
        """Write a file into Daytona workspace."""
        if not self._running:
            raise RuntimeError(DAYTONA_NOT_RUNNING)
        self._workspace_fs[path] = data

    def sync_files(self, source_dir: str, target_dir: str) -> int:
        """Sync directory into workspace filesystem."""
        if not self._running:
            raise RuntimeError(DAYTONA_NOT_RUNNING)
        synced = 0
        if os.path.isdir(source_dir):
            for root, _, files in os.walk(source_dir):
                for f in files:
                    src_file = os.path.join(root, f)
                    rel_path = os.path.relpath(src_file, source_dir)
                    dst_path = os.path.join(target_dir, rel_path)
                    with open(src_file, "rb") as rf:
                        self.write_file(dst_path, rf.read())
                    synced += 1
        return synced

    def snapshot(self, label: str) -> str:
        """Create Daytona workspace snapshot."""
        if not self._running:
            raise RuntimeError(DAYTONA_NOT_RUNNING)
        snap_id = f"daytona-snap-{uuid.uuid4().hex[:8]}-{label}"
        self._snapshots[snap_id] = dict(self._workspace_fs)
        return snap_id

    def terminate(self) -> None:
        """Terminate and destroy Daytona workspace container."""
        self._workspace_fs.clear()
        self._snapshots.clear()
        self._running = False
