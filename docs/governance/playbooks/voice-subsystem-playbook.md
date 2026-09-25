# Playbook: HATH0R Voice Interface Subsystem Troubleshooting

> Document Type: **Playbook** (`cr-workflow-doc-001`)  
> Product: **HATH0R-Agentic-Framework** · Issue: #67 · SemVer: `minor`

## 1. Scenario: Spoken Audio Fails to Route via System 1 Fast-Path

When a spoken utterance falls through to System 2 despite being a standard command:
1. Verify utterance transcript accuracy. Fast-path heuristic router expects prefixes like `hathor <cmd>`, `hath0r <cmd>`, `open <app>`, or exact system control phrases (`mute`, `cancel`).
2. Verify confidence threshold: if `confidence < min_confidence` (default 0.85), escalation occurs.
3. Check `action.metadata["latency_ms"]` to inspect decision timing.

## 2. Scenario: Audio Adapter Synthesis Error on Host OS

If platform TTS fails:
1. macOS: Verify `/usr/bin/say` exists and audio output device is connected.
2. Linux: Check for `espeak-ng` or `piper` in PATH (`which espeak-ng`).
3. Windows: Ensure PowerShell `System.Speech.Synthesis` is available.
4. CI/Headless: Use `MockAudioAdapter` or `platform="agnostic"` to prevent OS-level subprocess execution.
