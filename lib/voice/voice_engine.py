"""Core Voice Engine for HATH0R Agentic Framework.

Provides platform-agnostic, agent-agnostic, and model-agnostic speech-to-action
pipelines with low-latency System One (e.g. TypeSafe JEV) routing and System Two
agent escalation.
"""

from __future__ import annotations

import datetime
import os
import re
import shutil
import subprocess
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from lib.voice.voice_config import VoiceConfig, detect_platform


@dataclass
class VoiceAction:
    """Action contract matching schema hath0r.voice.action/1."""

    transcript: str
    routing_tier: str  # "system_one" | "system_two"
    intent: str  # "cli_command" | "computer_use" | "agent_delegate" | "system_control" | "unresolved"
    confidence: float
    payload: Dict[str, Any]
    platform: str = "agnostic"
    action_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat()
    )
    metadata: Dict[str, Any] = field(default_factory=dict)
    schema: str = "hath0r.voice.action/1"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return {
            "schema": self.schema,
            "action_id": self.action_id,
            "timestamp": self.timestamp,
            "transcript": self.transcript,
            "routing_tier": self.routing_tier,
            "intent": self.intent,
            "confidence": self.confidence,
            "platform": self.platform,
            "payload": self.payload,
            "metadata": self.metadata,
        }


# ============================================================================
# Platform Audio & TTS Adapters (Cross-Platform)
# ============================================================================


class PlatformAudioAdapter(ABC):
    """Abstract base class for operating system audio I/O & synthesis."""

    @abstractmethod
    def speak(self, text: str) -> bool:
        """Synthesize and speak text feedback to the user."""
        pass

    @abstractmethod
    def execute_computer_action(self, target: str, action: str, args: Optional[List[str]] = None) -> bool:
        """Execute a desktop / OS level automation action."""
        pass


class DarwinAudioAdapter(PlatformAudioAdapter):
    """macOS implementation utilizing native 'say' and AppleScript/osascript."""

    def speak(self, text: str) -> bool:
        clean_text = text.replace('"', '\\"')
        try:
            subprocess.run(["say", clean_text], check=False, timeout=5)
            return True
        except Exception:
            return False

    def execute_computer_action(self, target: str, action: str, args: Optional[List[str]] = None) -> bool:
        try:
            if action in ("open_app", "focus"):
                subprocess.run(["open", "-a", target], check=False, timeout=3)
                return True
            elif action == "open_url":
                subprocess.run(["open", target], check=False, timeout=3)
                return True
            elif action == "run_script":
                script = " ".join(args or [])
                subprocess.run(["osascript", "-e", script], check=False, timeout=5)
                return True
        except Exception:
            pass
        return False


class LinuxAudioAdapter(PlatformAudioAdapter):
    """Linux implementation utilizing eSpeak / Piper / xdg-open."""

    def speak(self, text: str) -> bool:
        cmd = None
        if shutil.which("espeak-ng"):
            cmd = ["espeak-ng", text]
        elif shutil.which("espeak"):
            cmd = ["espeak", text]

        if cmd:
            try:
                subprocess.run(cmd, check=False, timeout=5)
                return True
            except Exception:
                pass
        return False

    def execute_computer_action(self, target: str, action: str, args: Optional[List[str]] = None) -> bool:
        try:
            if action in ("open_app", "open_url"):
                subprocess.run(["xdg-open", target], check=False, timeout=3)
                return True
        except Exception:
            pass
        return False


class WindowsAudioAdapter(PlatformAudioAdapter):
    """Windows implementation utilizing PowerShell System.Speech.Synthesis."""

    def speak(self, text: str) -> bool:
        clean_text = text.replace("'", "''")
        ps_cmd = (
            f"Add-Type -AssemblyName System.Speech; "
            f"$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            f"$speak.Speak('{clean_text}')"
        )
        try:
            subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=False, timeout=5)
            return True
        except Exception:
            return False

    def execute_computer_action(self, target: str, action: str, args: Optional[List[str]] = None) -> bool:
        try:
            if action in ("open_app", "open_url"):
                subprocess.run(["powershell", "-NoProfile", "-Command", f"Start-Process '{target}'"], check=False, timeout=3)
                return True
        except Exception:
            pass
        return False


class MockAudioAdapter(PlatformAudioAdapter):
    """Mock / headless implementation for unit tests and headless environments."""

    def __init__(self) -> None:
        self.spoken_messages: List[str] = []
        self.executed_actions: List[Dict[str, Any]] = []

    def speak(self, text: str) -> bool:
        self.spoken_messages.append(text)
        return True

    def execute_computer_action(self, target: str, action: str, args: Optional[List[str]] = None) -> bool:
        self.executed_actions.append({"target": target, "action": action, "args": args or []})
        return True


def resolve_audio_adapter(platform_name: str) -> PlatformAudioAdapter:
    """Resolve the appropriate audio adapter for the current or configured platform."""
    if platform_name == "darwin":
        return DarwinAudioAdapter()
    elif platform_name == "linux":
        return LinuxAudioAdapter()
    elif platform_name == "win32":
        return WindowsAudioAdapter()
    return MockAudioAdapter()


# ============================================================================
# System 1: Fast Decision Routers (JEV / Heuristic)
# ============================================================================


class SystemOneRouter(ABC):
    """Abstract base class for ultra-fast, typed System 1 decision routing."""

    @abstractmethod
    def route(self, transcript: str) -> Optional[VoiceAction]:
        """Classify user utterance into a structured VoiceAction or return None to escalate."""
        pass


class HeuristicDecisionRouter(SystemOneRouter):
    """Deterministic, zero-latency rule-based router for quick commands."""

    def route(self, transcript: str) -> Optional[VoiceAction]:
        t = transcript.strip().lower()

        # Hath0r CLI direct commands
        if t.startswith("hathor ") or t.startswith("hath0r "):
            parts = t.split()
            subcmd = parts[1] if len(parts) > 1 else "doctor"
            args = parts[2:]
            return VoiceAction(
                transcript=transcript,
                routing_tier="system_one",
                intent="cli_command",
                confidence=0.98,
                payload={
                    "command": f"hath0r {subcmd}",
                    "args": args,
                    "feedback_text": f"Running Hathor {subcmd}",
                },
            )

        # Computer use / App opening
        open_match = re.match(r"^(?:open|launch|start)\s+([a-zA-Z0-9\s\.\-_]+)$", transcript.strip(), re.IGNORECASE)
        if open_match:
            app_name = open_match.group(1).strip()
            return VoiceAction(
                transcript=transcript,
                routing_tier="system_one",
                intent="computer_use",
                confidence=0.95,
                payload={
                    "target": app_name,
                    "action": "open_app",
                    "feedback_text": f"Opening {app_name}",
                },
            )

        # Basic system control
        if t in ("mute", "unmute", "stop listening", "cancel"):
            return VoiceAction(
                transcript=transcript,
                routing_tier="system_one",
                intent="system_control",
                confidence=0.99,
                payload={
                    "action": t,
                    "feedback_text": f"{t.capitalize()} acknowledged",
                },
            )

        return None


class JevDecisionRouter(SystemOneRouter):
    """TypeSafe AI JEV System One fast decision router.

    Uses Jev API or deterministic stub for sub-50ms typed routing.
    """

    def __init__(self, mode: str = "stub", min_confidence: float = 0.85) -> None:
        self.mode = mode
        self.min_confidence = min_confidence
        self.heuristic_fallback = HeuristicDecisionRouter()

    def route(self, transcript: str) -> Optional[VoiceAction]:
        start = time.perf_counter()

        # Check heuristic fast-path first
        fast_action = self.heuristic_fallback.route(transcript)
        if fast_action:
            elapsed_ms = (time.perf_counter() - start) * 1000
            fast_action.metadata["latency_ms"] = round(elapsed_ms, 2)
            fast_action.metadata["model_id"] = "typesafe-jev-fastpath"
            return fast_action

        # In stub mode or if no external API key, return None to escalate to System 2
        return None


# ============================================================================
# System 2: Agent-Agnostic & Model-Agnostic Dispatcher
# ============================================================================


class AgentDispatcher:
    """Agent-agnostic and model-agnostic dispatcher for HATHOR.

    Delegates unresolved actions to whichever agent or LLM is active in the
    framework (e.g. Claude, Gemini, GPT, local Bot Units, or CLI).
    """

    def __init__(
        self,
        cli_binary: str = "hath0r",
        agent_callback: Optional[Callable[[str], str]] = None,
    ) -> None:
        self.cli_binary = cli_binary
        self.agent_callback = agent_callback

    def dispatch_to_agent(self, transcript: str) -> VoiceAction:
        """Escalate to System Two (active model/agent) for multi-step reasoning."""
        response_text = ""
        if self.agent_callback:
            try:
                response_text = self.agent_callback(transcript)
            except Exception as e:
                response_text = f"Agent execution error: {e}"
        else:
            response_text = f"Delegating '{transcript}' to active Hathor agent."

        return VoiceAction(
            transcript=transcript,
            routing_tier="system_two",
            intent="agent_delegate",
            confidence=1.0,
            payload={
                "feedback_text": response_text,
                "target_agent": "active_framework_agent",
            },
            metadata={"delegated": True},
        )


# ============================================================================
# Main Voice Engine Orchestrator
# ============================================================================


class VoiceEngine:
    """Primary orchestrator for the HATH0R Voice Interface Subsystem."""

    def __init__(
        self,
        config: Optional[VoiceConfig] = None,
        audio_adapter: Optional[PlatformAudioAdapter] = None,
        router: Optional[SystemOneRouter] = None,
        agent_dispatcher: Optional[AgentDispatcher] = None,
    ) -> None:
        self.config = config or VoiceConfig.from_env()
        self.audio = audio_adapter or resolve_audio_adapter(self.config.platform)
        self.router = router or (
            JevDecisionRouter(mode=self.config.mode, min_confidence=self.config.min_confidence)
            if self.config.router_provider == "jev"
            else HeuristicDecisionRouter()
        )
        self.dispatcher = agent_dispatcher or AgentDispatcher(cli_binary=self.config.cli_binary)

    def process_utterance(self, transcript: str, speak_feedback: bool = True) -> VoiceAction:
        """Process a spoken text utterance through the System 1 / System 2 pipeline."""
        start_time = time.perf_counter()

        # Step 1: Attempt System 1 fast decision (Jev / Heuristic)
        action = self.router.route(transcript)

        # Step 2: Escalate to System 2 (Active Agent) if unresolved
        if not action or action.confidence < self.config.min_confidence:
            action = self.dispatcher.dispatch_to_agent(transcript)

        action.platform = self.config.platform
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        action.metadata["latency_ms"] = round(elapsed_ms, 2)

        # Step 3: Execute OS action if computer_use
        if action.intent == "computer_use":
            target = action.payload.get("target", "")
            act = action.payload.get("action", "")
            args = action.payload.get("args", [])
            self.audio.execute_computer_action(target=target, action=act, args=args)

        # Step 4: Spoken feedback if requested
        feedback = action.payload.get("feedback_text")
        if speak_feedback and feedback:
            self.audio.speak(feedback)

        return action
