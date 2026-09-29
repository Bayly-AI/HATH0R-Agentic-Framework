# Playbook: JEV Tool-Guard Troubleshooting and Policy Remediation

> Document Type: **Playbook** (`cr-workflow-doc-001`)  
> Product: **HATH0R-Agentic-Framework** · Issue: #65 · SemVer: `minor`

## 1. Scenario: Tool Blocked with `deny`

When a tool returns `jev_tool_guard_blocked` with `decision: deny`:
1. Check the `tool` and `arguments_summary` in the block payload.
2. If the tool is a destructive operation (`fs_delete`, `kb_index_delete`):
   - The action is blocked per baseline security policy.
   - Obtain operator confirmation or perform non-destructive alternative.
3. If running in CI or test suites:
   - Use `JevClient(settings=JevSettings(enabled=False))` or mock the guard client.

## 2. Scenario: JEV API Unreachable or Network Failure

If live JEV times out or returns HTTP 5xx:
1. When configured with `on_error: deny`, the tool call will fail closed to protect the host.
2. Check `JEV_ENDPOINT` connectivity.
3. For local development or disconnected testing, switch to `JEV_MODE=stub`.
