# Playbook: Streaming Voice Pipeline Troubleshooting

> Document Type: **Playbook** (`cr-workflow-doc-001`)  
> Product: **HATH0R-Agentic-Framework** · Issue: #68 · SemVer: `minor`

## 1. Scenario: High False Positive Onset in Noisy Environments

When ambient noise repeatedly triggers `SPEECH_ONSET`:
1. Increase `AdaptiveEnergyVAD(sensitivity=...)` down to 0.4 or 0.3.
2. Increase `onset_frames_threshold` from 3 frames (60ms) to 4-5 frames (80-100ms).
3. Verify microphone input gain and physical placement.

## 2. Scenario: Premature Utterance Termination During Speech Pauses

When user pauses mid-sentence and speech cuts off prematurely:
1. Increase `hangover_frames_threshold` from 12 frames (240ms) to 20-25 frames (400-500ms).
2. Inspect `VADFrameResult.energy` and ambient noise floor convergence.
