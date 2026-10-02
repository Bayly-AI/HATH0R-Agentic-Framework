"""Unit tests for Zero-Trust Isolated Compute Providers and SandboxManager."""

import tempfile
from pathlib import Path

from hath0r_engine.sandbox import (
    DaytonaSandboxProvider,
    E2BSandboxProvider,
    LocalSandboxProvider,
    NetworkPolicy,
    SandboxConfig,
    SandboxManager,
    SandboxType,
)
from hath0r_engine.telemetry.otel_tracer import OTELTracerBot


def test_e2b_sandbox_lifecycle_and_virtual_fs():
    provider = E2BSandboxProvider()
    config = SandboxConfig(
        provider_type=SandboxType.E2B,
        timeout_seconds=30.0,
        network_policy=NetworkPolicy(block_all=True),
    )

    instance_id = provider.start(config)
    assert instance_id.startswith("e2b-vm-")
    assert provider.is_running() is True

    # Virtual filesystem read / write
    provider.write_file("/workspace/hello.txt", b"Hello from E2B")
    data = provider.read_file("/workspace/hello.txt")
    assert data == b"Hello from E2B"

    # Execution test
    result = provider.exec("echo 'Compute Test'")
    assert result.exit_code == 0
    assert "Compute Test" in result.stdout
    assert result.succeeded is True

    # Network egress blocking check
    egress_result = provider.exec("curl https://unauthorized-exfil.com/data")
    assert egress_result.exit_code == 1
    assert "Network egress blocked" in egress_result.stderr

    # Snapshot test
    snap_id = provider.snapshot("test-snap")
    assert "test-snap" in snap_id

    # Terminate
    provider.terminate()
    assert provider.is_running() is False


def test_daytona_sandbox_lifecycle():
    provider = DaytonaSandboxProvider()
    config = SandboxConfig(
        provider_type=SandboxType.DAYTONA,
        timeout_seconds=60.0,
    )

    instance_id = provider.start(config)
    assert instance_id.startswith("daytona-ws-")
    assert provider.is_running() is True

    # File write and read
    provider.write_file("/workspace/app.py", b"print(42)")
    content = provider.read_file("/workspace/app.py")
    assert content == b"print(42)"

    # Execution
    result = provider.exec("python3 -c 'print(6 * 7)'")
    assert result.exit_code == 0
    assert "42" in result.stdout

    # Terminate
    provider.terminate()
    assert provider.is_running() is False


def test_local_sandbox_provider():
    provider = LocalSandboxProvider()
    config = SandboxConfig(
        provider_type=SandboxType.LOCAL,
        timeout_seconds=10.0,
    )

    instance_id = provider.start(config)
    assert instance_id.startswith("local-box-")
    assert provider.is_running() is True

    # File ops
    provider.write_file("sub/test.txt", b"local data")
    assert provider.read_file("sub/test.txt") == b"local data"

    # Directory sync
    with tempfile.TemporaryDirectory() as src_dir:
        src_path = Path(src_dir)
        (src_path / "file1.txt").write_text("file 1 content")
        (src_path / "file2.txt").write_text("file 2 content")

        synced = provider.sync_files(src_dir, "synced_dir")
        assert synced == 2
        assert provider.read_file("synced_dir/file1.txt") == b"file 1 content"

    # Snapshot
    snap_id = provider.snapshot("base")
    assert "base" in snap_id

    # Terminate
    provider.terminate()
    assert provider.is_running() is False


def test_sandbox_manager_orchestration_and_telemetry():
    tracer = OTELTracerBot(service_name="test-sandbox-tracer")
    manager = SandboxManager(tracer=tracer)

    # Create E2B sandbox via manager
    e2b_box = manager.create_sandbox(
        SandboxConfig(
            provider_type=SandboxType.E2B,
            timeout_seconds=15.0,
        )
    )
    assert e2b_box.is_running() is True

    # Execute with traced telemetry
    res = manager.exec_in_sandbox(e2b_box, "echo 'Traced Exec'")
    assert res.exit_code == 0
    assert "Traced Exec" in res.stdout

    # List active
    active = manager.list_active()
    assert len(active) >= 1
    assert active[0]["instance_id"] == e2b_box.instance_id

    # Fallback routing test for custom provider
    fallback_box = manager.create_sandbox(
        SandboxConfig(provider_type=SandboxType.WASM)
    )
    assert fallback_box.is_running() is True

    # Terminate all
    count = manager.terminate_all()
    assert count >= 2
    assert len(manager.list_active()) == 0
