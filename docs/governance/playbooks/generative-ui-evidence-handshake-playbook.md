# Generative UI & Evidence Handshake Protocol Playbook

> **Status:** Active  
> **Parent Issue:** Bayly-AI/HATH0R-Agentic-Framework#133  
> **Target Subsystem:** `src/hath0r_engine/ui`

---

## 1. Overview

This playbook shows how agents construct Generative UI components, stream evidence handshakes to the Hath0r Dashboard, handle bi-directional parameter adjustments, and verify cryptographic sign-offs.

---

## 2. Usage Examples

### 2.1 Emitting Visual Diff and Parameter Slider Components

```python
from hath0r_engine.ui import (
    HandshakeSession,
    UIComponentBuilder,
    BiDirectionalStateSync,
)

session = HandshakeSession(session_id="promo-sess-001", task_name="v2_auth_migration")

# Build Diff Viewer and Test Badges
diff_card = UIComponentBuilder.build_diff_viewer(
    file_path="src/auth.py",
    old_code="def login(): pass",
    new_code="def login(token: str): verify(token)",
)
test_badge = UIComponentBuilder.build_test_badge(
    suite_name="Auth Tests",
    passed=12,
    failed=0,
    coverage_pct=98.5,
)
slider = UIComponentBuilder.build_parameter_slider(
    param_key="batch_size",
    min_val=10,
    max_val=1000,
    current_val=100,
)

session.add_components([diff_card, test_badge, slider])
payload = session.export_payload()
```

### 2.2 Bi-Directional State Synchronization and Sign-Off

```python
# Human updates parameter on dashboard
sync = BiDirectionalStateSync()
agent_context = {"batch_size": 100}
sync.apply_update(agent_context, "batch_size", 250)
assert agent_context["batch_size"] == 250

# Human signs off promotion
sign_off = session.sign_off(
    reviewer="somesayray",
    role="lead_architect",
    decision=True,
)
assert sign_off.signature is not None
```
