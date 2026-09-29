# Strategy: Streaming Speech-to-Text and VAD Pipeline

> Document Type: **Strategy** (`cr-workflow-doc-001`)  
> Product: **HATH0R-Agentic-Framework** · Issue: #68 · SemVer: `minor`

## 1. Context & Motivation

To achieve conversational response times comparable to desktop native human-computer interfaces (<200ms end-to-end), spoken input cannot wait for complete phrase endpointing and silence detection before processing begins.

The streaming STT and VAD pipeline enables:
- Streaming voice activity detection (VAD) with minimal frame latency (sub-20ms) and adaptive noise estimation.
- Progressive token ingestion from real-time speech-to-text engines.
- Speculative execution of System 1 action routes on partial transcripts, committing early for unambiguous commands and cancelling cleanly if the speaker continues or clarifies.

## 2. Architecture & Guarantees

- **Sub-200ms latency guarantee**: High-confidence fast-path actions commit within 200ms of user utterance completion.
- **Graceful cancellation**: If an utterance partial matches an action prefix but随后 diverges, the speculative candidate is discarded without executing unapproved side-effects.
- **Pluggable adapters**: Support for native macOS speech recognition, Whisper/local engines, and in-memory mock harnesses.
