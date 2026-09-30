# Zero-Trust Isolated Compute Provider Playbook

> **Status:** Active  
> **Parent Issue:** Bayly-AI/HATH0R-Agentic-Framework#128  
> **Target Subsystem:** `src/hath0r_engine/sandbox`

---

## 1. Overview

This playbook describes how to instantiate, execute, and monitor isolated compute sandboxes across E2B Micro-VM, Daytona Dev Containers, and local fallback runtimes.

---

## 2. Usage Examples

### 2.1 Basic Execution with SandboxManager

```python
from hath0r_engine.sandbox import SandboxManager, SandboxConfig, SandboxType

manager = SandboxManager()

# 1. Start an ephemeral E2B Micro-VM sandbox
sandbox = manager.create_sandbox(
    SandboxConfig(
        provider_type=SandboxType.E2B,
        template="python3-datascience",
        timeout_seconds=120,
        network_egress_allowed=False,
    )
)

# 2. Write code into sandbox
sandbox.write_file("/workspace/script.py", b"print('Hello from isolated Micro-VM!')")

# 3. Execute script securely
result = sandbox.exec("python3 /workspace/script.py")
print(f"Exit code: {result.exit_code}")
print(f"Output: {result.stdout}")

# 4. Terminate sandbox
sandbox.terminate()
```

### 2.2 Snapshotting and State Branching

```python
# Create snapshot before experimental refactor
snapshot_id = sandbox.snapshot("pre-migration")

# Execute mutation
sandbox.exec("pip install -U risky-package")

# Cleanup
manager.terminate_all()
```
