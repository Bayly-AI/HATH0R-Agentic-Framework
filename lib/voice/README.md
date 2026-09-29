# HATH0R Voice Interface Subsystem (`lib/voice`)

The **HATH0R Voice Interface Subsystem** provides a low-latency, cross-platform, agent-agnostic, and model-agnostic voice interaction loop for the HATHOR framework.

Inspired by real-time voice computer-use architectures (such as TypeSafe AI's JEV), it decouples **System 1 (sub-50ms deterministic action routing)** from **System 2 (deliberate agent reasoning)**.

---

## Key Architectural Principles

1. **Agent-Agnostic**: Does not assume a specific agent implementation. Dispatches structured intent payloads (`hath0r.voice.action/1`) to any Hath0r agent, Bot Unit, ATC orchestrator, or external agent framework.
2. **Model-Agnostic**: Works with whichever frontier model or local model is currently powering the framework (Claude, Gemini, GPT, DeepSeek, Llama, etc.). The agent reasoning tier is completely decoupled from speech capture.
3. **System 1 Fast Routing (TypeSafe JEV)**: Employs TypeSafe AI's Jev (or deterministic heuristics) as an ultra-fast probabilistic decision layer. When confidence $> 0.85$, actions execute in milliseconds before conversational token generation begins.
4. **Cross-Platform Compatibility**:
   - **macOS (`darwin`)**: Native `say` synthesis, AppleScript / `osascript` application control.
   - **Linux (`linux`)**: `espeak-ng` / `espeak` / `piper` synthesis, `xdg-open` application control.
   - **Windows (`win32`)**: PowerShell `System.Speech.Synthesis` and process execution.
   - **Headless / Agnostic**: Pure mock adapter for CI/CD testing, containerized nodes, and server environments.

---

## Data Flow

```text
[Spoken Audio Input]
         │
         ▼
[Speech-To-Text / VAD]
         │ Transcribed Text
         ▼
┌────────────────────────────────────────────────────────┐
│           System 1: TypeSafe JEV Fast Router           │
│   • Typed Action Classification (<50ms)                │
└──────────────────────────┬─────────────────────────────┘
                           │
             ┌─────────────┴─────────────┐
             │ High Confidence           │ Low Confidence / Complex
             ▼                           ▼
┌──────────────────────────┐    ┌───────────────────────────────────┐
│     Direct Execution     │    │  System 2: Active Hathor Agent    │
│ • hath0r CLI command     │    │ • Full codebase / context access  │
│ • OS / computer use      │    │ • Whichever model powers project  │
└────────────┬─────────────┘    └─────────────────┬─────────────────┘
             │                                    │
             └─────────────┬──────────────────────┘
                           │
                           ▼
              [Audio Feedback / TTS (say / espeak / sapi)]
```

---

## Machine Contract: `hath0r.voice.action/1`

All resolved actions conform to [`lib/schemas/hath0r-voice-action-v1.schema.json`](../schemas/hath0r-voice-action-v1.schema.json):

```json
{
  "schema": "hath0r.voice.action/1",
  "action_id": "c1f7a070-5b58-47bc-87c2-9029a8a61421",
  "timestamp": "2026-09-25T14:30:00Z",
  "transcript": "hathor doctor",
  "routing_tier": "system_one",
  "intent": "cli_command",
  "confidence": 0.98,
  "platform": "darwin",
  "payload": {
    "command": "hath0r doctor",
    "args": [],
    "feedback_text": "Running Hathor doctor"
  },
  "metadata": {
    "latency_ms": 1.25,
    "model_id": "typesafe-jev-fastpath"
  }
}
```

---

## Configuration

Default settings reside in `cfg/voice.json`. Environment variable overrides:

| Variable | Values | Default | Description |
|---|---|---|---|
| `HATHOR_VOICE_MODE` | `off`, `stub`, `live`, `auto` | `auto` | Operating mode |
| `HATHOR_VOICE_PLATFORM` | `darwin`, `linux`, `win32`, `agnostic` | Auto-detected | Target OS |
| `HATHOR_VOICE_ROUTER` | `jev`, `heuristic`, `agent_direct` | `jev` | System 1 decision engine |
| `HATHOR_VOICE_MIN_CONFIDENCE` | Float `0.0` - `1.0` | `0.85` | Confidence threshold for System 1 execution |
| `JEV_API_KEY` | Bearer Token | Optional | TypeSafe Jev API Key |

---

## Programmatic Usage

```python
from lib.voice import VoiceEngine, VoiceConfig, AgentDispatcher

# Define callback for whichever model is active in the project
def my_active_agent(prompt: str) -> str:
    # Delegate to active model (e.g. Gemini, Claude, GPT, or local agent)
    return f"Active agent received: {prompt}"

dispatcher = AgentDispatcher(agent_callback=my_active_agent)
engine = VoiceEngine(agent_dispatcher=dispatcher)

# Process incoming spoken utterance
action = engine.process_utterance("open Safari")
print(action.to_dict())
# -> Executes fast computer_use action via macOS adapter

action2 = engine.process_utterance("analyze our database schema and propose migrations")
print(action2.to_dict())
# -> Automatically escalates to System 2 active agent
```
