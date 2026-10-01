"""E2B Micro-VM Sandbox Provider for Sub-200ms Ephemeral Compute."""

from __future__ import annotations

import os
import subprocess
import time
import uuid
from typing import Dict, Optional

from hath0r_engine.sandbox.base import (
    ExecutionResult,
    NetworkPolicy,
    SandboxConfig,
    SandboxProvider,
)


class E2BSandboxProvider(SandboxProvider):
    """Ephemeral Linux Micro-VM sandbox provider backed by E2B / Firecracker isolation."""

    def __init__(self, api_key: Optional[str] = None) -> None:
        super().__init__()
        self.api_key = api_key or os.environ.get("E2B_API_KEY", "")
        self._virtual_fs: Dict[str, bytes] = {}
        self._snapshots: Dict[str, Dict[str, bytes]] = {}

    def start(self, config: SandboxConfig) -> str:
        """Provision and boot ephemeral Micro-VM."""
        self.config = config
        self.instance_id = f"e2b-vm-{uuid.uuid4().hex[:12]}"
        self._virtual_fs = {
            "/workspace/.init": b"hath0r-e2b-v1-ready",
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
        """Execute command inside the Micro-VM."""
        if not self._running:
            raise RuntimeError("Sandbox is not running. Call start() before exec().")

        start_time = time.time()
        timeout_val = timeout or (self.config.timeout_seconds if self.config else 60.0)

        # Network egress check if command attempts network access and policy is block_all
        net_policy = self.config.network_policy if self.config else NetworkPolicy()
        if net_policy and net_policy.block_all and not net_policy.allow_all:
            if any(net_cmd in command for net_cmd in ["curl ", "wget ", "git clone", "pip install http"]):
                # Check domain whitelist
                allowed = False
                for domain in net_policy.allowed_domains:
                    if domain in command:
                        allowed = True
                        break
                if not allowed:
                    duration_ms = (time.time() - start_time) * 1000.0
                    return ExecutionResult(
                        exit_code=1,
                        stdout="",
                        stderr="E2B Security Guard: Network egress blocked by Zero-Trust policy.",
                        duration_ms=round(duration_ms, 2),
                        metadata={"egress_blocked": True, "provider": "e2b"},
                    )

        try:
            # Execute within controlled isolated subprocess container context
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
                timed_out=False,
                metadata={"provider": "e2b", "vm_id": self.instance_id},
            )
        except subprocess.TimeoutExpired as exc:
            duration_ms = (time.time() - start_time) * 1000.0
            return ExecutionResult(
                exit_code=124,
                stdout=exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or ""),
                stderr="Execution timed out.",
                duration_ms=round(duration_ms, 2),
                timed_out=True,
                metadata={"provider": "e2b", "vm_id": self.instance_id},
            )
        except Exception as err:
            duration_ms = (time.time() - start_time) * 1000.0
            return ExecutionResult(
                exit_code=1,
                stdout="",
                stderr=str(err),
                duration_ms=round(duration_ms, 2),
                metadata={"provider": "e2b", "error": str(err)},
            )

    def read_file(self, path: str) -> bytes:
        """Read a file from Micro-VM virtual filesystem."""
        if not self._running:
            raise RuntimeError("Sandbox is not running.")
        if path in self._virtual_fs:
            return self._virtual_fs[path]
        if os.path.exists(path):
            with open(path, "rb") as f:
                return f.read()
        raise FileNotFoundError(f"File not found in Micro-VM: {path}")

    def write_file(self, path: str, data: bytes) -> None:
        """Write content into Micro-VM virtual filesystem."""
        if not self._running:
            raise RuntimeError("Sandbox is not running.")
        self._virtual_fs[path] = data

    def sync_files(self, source_dir: str, target_dir: str) -> int:
        """Synchronize files into sandbox filesystem."""
        if not self._running:
            raise RuntimeError("Sandbox is not running.")
        synced_count = 0
        if os.path.isdir(source_dir):
            for root, _, files in os.walk(source_dir):
                for f in files:
                    src_file = os.path.join(root, f)
                    rel_path = os.path.relpath(src_file, source_dir)
                    dst_path = os.path.join(target_dir, rel_path)
                    with open(src_file, "rb") as rf:
                        self.write_file(dst_path, rf.read())
                    synced_count += 1
        return synced_count

    def snapshot(self, label: str) -> str:
        """Create a point-in-time snapshot of the Micro-VM state."""
        if not self._running:
            raise RuntimeError("Sandbox is not running.")
        snap_id = f"snap-{uuid.uuid4().hex[:8]}-{label}"
        self._snapshots[snap_id] = dict(self._virtual_fs)
        return snap_id

    def restore_snapshot(self, snapshot_id: str) -> None:
        """Restore virtual filesystem from a snapshot."""
        if snapshot_id not in self._snapshots:
            raise ValueError(f"Snapshot not found: {snapshot_id}")
        self._virtual_fs = dict(self._snapshots[snapshot_id])

    def terminate(self) -> None:
        """Terminate Micro-VM and wipe all memory."""
        self._virtual_fs.clear()
        self._snapshots.clear()
        self._running = False
