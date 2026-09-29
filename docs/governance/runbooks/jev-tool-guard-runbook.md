# Runbook: JEV Tool-Guard Operations

> Document Type: **Runbook** (`cr-workflow-doc-001`)  
> Product: **HATH0R-Agentic-Framework** · Issue: #65 · SemVer: `minor`

## 1. Quick Operations Commands

### Run Unit Tests
```bash
PYTHONPATH=. pytest tests/test_jev_tool_guard.py -v
```

### Inspect Policy Catalog
```bash
cat lib/jev/jev.json
```

### Test Stub Interception in Python REPL
```python
import asyncio
from lib.jev.jev_client import JevClient, JevSettings
from lib.jev.jev_tool_guard import evaluate_tool_guard

client = JevClient(settings=JevSettings(enabled=True, mode="stub"))
result = asyncio.run(evaluate_tool_guard("fs_delete", {"path": "test.txt"}, client=client))
print(result.blocked, result.decision)
```
