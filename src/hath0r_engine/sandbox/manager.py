"""Sandbox Manager for Lifecycle Orchestration, Fallback Routing, and Telemetry."""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from hath0r_engine.sandbox.base import (
    ExecutionResult,
    SandboxConfig,
    SandboxProvider,
    SandboxType,
)
from hath0r_engine.sandbox.daytona_provider import DaytonaSandboxProvider
from hath0r_engine.sandbox.e2b_provider import E2BSandboxProvider
from hath0r_engine.sandbox.local_provider import LocalSandboxProvider
from hath0r_engine.telemetry.otel_tracer import OTELTracerBot


class SandboxManager:
    """Orchestrates zero-trust sandbox lifecycles, provider selection, and execution telemetry."""

    def __init__(self, tracer: Optional[OTELTracerBot] = None) -> None:
        self.tracer = tracer or OTELTracerBot(service_name="hath0r-sandbox-manager")
        self._factories: Dict[SandboxType, Callable[[], SandboxProvider]] = {
            SandboxType.E2B: lambda: E2BSandboxProvider(),
            SandboxType.DAYTONA: lambda: DaytonaSandboxProvider(),
            SandboxType.LOCAL: lambda: LocalSandboxProvider(),
            SandboxType.WASM: lambda: LocalSandboxProvider(),  # WASM fallback maps to local isolated container
        }
        self._active_sandboxes: Dict[str, SandboxProvider] = {}

    def register_provider_factory(
        self, sandbox_type: SandboxType, factory: Callable[[], SandboxProvider]
    ) -> None:
        """Register custom or third-party isolated compute provider factory."""
        self._factories[sandbox_type] = factory

    def create_sandbox(self, config: Optional[SandboxConfig] = None) -> SandboxProvider:
        """Create and start an isolated sandbox instance with fallback routing."""
        cfg = config or SandboxConfig(provider_type=SandboxType.LOCAL)
        target_type = cfg.provider_type

        # Attempt target provider instantiation
        factory = self._factories.get(target_type)
        if factory is None:
            factory = self._factories[SandboxType.LOCAL]

        provider: SandboxProvider
        try:
            provider = factory()
            instance_id = provider.start(cfg)
            self._active_sandboxes[instance_id] = provider
            return provider
        except Exception:
            # Fallback to local isolated provider
            provider = self._factories[SandboxType.LOCAL]()
            instance_id = provider.start(cfg)
            self._active_sandboxes[instance_id] = provider
            return provider

    def exec_in_sandbox(
        self,
        sandbox: SandboxProvider,
        command: str,
        timeout: Optional[float] = None,
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[str] = None,
    ) -> ExecutionResult:
        """Execute command inside sandbox and trace execution metrics."""
        span_name = f"sandbox.exec.{sandbox.config.provider_type.value if sandbox.config else 'unknown'}"
        with self.tracer.start_span(
            span_name,
            span_kind="TOOL",
            attributes={
                "command": command[:100],
                "instance_id": sandbox.instance_id or "unknown",
            },
        ) as span:
            result = sandbox.exec(command=command, timeout=timeout, env=env, cwd=cwd)
            span.attributes.update(
                {
                    "exit_code": result.exit_code,
                    "duration_ms": result.duration_ms,
                    "timed_out": result.timed_out,
                }
            )
            if not result.succeeded:
                span.finish(status="ERROR", error=result.stderr or "Command failed")
            return result

    def get_sandbox(self, instance_id: str) -> Optional[SandboxProvider]:
        """Retrieve an active sandbox instance by ID."""
        return self._active_sandboxes.get(instance_id)

    def list_active(self) -> List[Dict[str, Any]]:
        """List metadata for all active sandbox instances."""
        active = []
        for i_id, prov in self._active_sandboxes.items():
            if prov.is_running():
                active.append(
                    {
                        "instance_id": i_id,
                        "provider_type": prov.config.provider_type.value if prov.config else "unknown",
                        "running": prov.is_running(),
                    }
                )
        return active

    def terminate_all(self) -> int:
        """Terminate and clean up all active sandboxes."""
        count = 0
        for prov in self._active_sandboxes.values():
            if prov.is_running():
                prov.terminate()
                count += 1
        self._active_sandboxes.clear()
        return count
