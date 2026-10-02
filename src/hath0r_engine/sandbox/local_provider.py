"""Local Isolated Temporary Sandbox Provider."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import time
import uuid
from pathlib import Path
from typing import Dict, Optional

from hath0r_engine.sandbox.base import (
    ExecutionResult,
    NetworkPolicy,
    SandboxConfig,
    SandboxProvider,
)


class LocalSandboxProvider(SandboxProvider):
    """Local isolated directory sandbox provider for lightweight/offline execution."""

    def __init__(self) -> None:
        super().__init__()
        self._temp_dir: Optional[tempfile.TemporaryDirectory[str]] = None
        self._root_path: Optional[Path] = None
        self._snapshots: Dict[str, Dict[str, bytes]] = {}

    def start(self, config: SandboxConfig) -> str:
        """Create isolated scratch filesystem."""
        self.config = config
        self.instance_id = f"local-box-{uuid.uuid4().hex[:10]}"
        self._temp_dir = tempfile.TemporaryDirectory(prefix=f"hath0r-sandbox-{self.instance_id}-")
        self._root_path = Path(self._temp_dir.name)
        self._running = True
        return self.instance_id

    def exec(
        self,
        command: str,
        timeout: Optional[float] = None,
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[str] = None,
    ) -> ExecutionResult:
        """Execute command within isolated temp directory."""
        if not self._running or self._root_path is None:
            raise RuntimeError("Sandbox is not running.")

        start_time = time.time()
        timeout_val = timeout or (self.config.timeout_seconds if self.config else 60.0)

        # Network egress check
        net_policy = self.config.network_policy if self.config else NetworkPolicy()
        if net_policy and net_policy.block_all and not net_policy.allow_all:
            if any(net_cmd in command for net_cmd in ["curl ", "wget ", "git clone"]):
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
                        stderr="Local Sandbox Security Guard: Network egress blocked.",
                        duration_ms=round(duration_ms, 2),
                        metadata={"egress_blocked": True, "provider": "local"},
                    )

        target_cwd = cwd or str(self._root_path)
        merged_env = dict(os.environ)
        if self.config and self.config.env:
            merged_env.update(self.config.env)
        if env:
            merged_env.update(env)

        try:
            proc = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout_val,
                env=merged_env,
                cwd=target_cwd,
            )
            duration_ms = (time.time() - start_time) * 1000.0
            return ExecutionResult(
                exit_code=proc.returncode,
                stdout=proc.stdout,
                stderr=proc.stderr,
                duration_ms=round(duration_ms, 2),
                metadata={"provider": "local", "sandbox_id": self.instance_id},
            )
        except subprocess.TimeoutExpired as exc:
            duration_ms = (time.time() - start_time) * 1000.0
            return ExecutionResult(
                exit_code=124,
                stdout=exc.stdout.decode() if isinstance(exc.stdout, bytes) else (exc.stdout or ""),
                stderr="Local sandbox execution timed out.",
                duration_ms=round(duration_ms, 2),
                timed_out=True,
                metadata={"provider": "local", "sandbox_id": self.instance_id},
            )
        except Exception as err:
            duration_ms = (time.time() - start_time) * 1000.0
            return ExecutionResult(
                exit_code=1,
                stdout="",
                stderr=str(err),
                duration_ms=round(duration_ms, 2),
                metadata={"provider": "local", "error": str(err)},
            )

    def read_file(self, path: str) -> bytes:
        """Read file from isolated directory."""
        if not self._running or self._root_path is None:
            raise RuntimeError("Sandbox is not running.")
        target = self._resolve_path(path)
        if not target.exists():
            raise FileNotFoundError(f"File not found in local sandbox: {path}")
        return target.read_bytes()

    def write_file(self, path: str, data: bytes) -> None:
        """Write file into isolated directory."""
        if not self._running or self._root_path is None:
            raise RuntimeError("Sandbox is not running.")
        target = self._resolve_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def _resolve_path(self, path: str) -> Path:
        assert self._root_path is not None
        clean_rel = path.lstrip("/")
        return self._root_path / clean_rel

    def sync_files(self, source_dir: str, target_dir: str) -> int:
        """Sync directory into sandbox."""
        if not self._running or self._root_path is None:
            raise RuntimeError("Sandbox is not running.")
        synced = 0
        src = Path(source_dir)
        if src.is_dir():
            for f in src.rglob("*"):
                if f.is_file():
                    rel = f.relative_to(src)
                    dst = self._resolve_path(os.path.join(target_dir, str(rel)))
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(f, dst)
                    synced += 1
        return synced

    def snapshot(self, label: str) -> str:
        """Snapshot current directory state."""
        if not self._running or self._root_path is None:
            raise RuntimeError("Sandbox is not running.")
        snap_id = f"local-snap-{uuid.uuid4().hex[:8]}-{label}"
        data_map: Dict[str, bytes] = {}
        for f in self._root_path.rglob("*"):
            if f.is_file():
                rel = str(f.relative_to(self._root_path))
                data_map[rel] = f.read_bytes()
        self._snapshots[snap_id] = data_map
        return snap_id

    def terminate(self) -> None:
        """Wipe temp directory and cleanup."""
        if self._temp_dir:
            try:
                self._temp_dir.cleanup()
            except Exception:
                pass
            self._temp_dir = None
        self._root_path = None
        self._snapshots.clear()
        self._running = False
