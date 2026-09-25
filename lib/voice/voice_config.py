"""Configuration loader for HATH0R Voice Interface Subsystem."""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional


def detect_platform() -> str:
    """Detect host platform: darwin, linux, win32, or agnostic."""
    if sys.platform.startswith("darwin"):
        return "darwin"
    elif sys.platform.startswith("linux"):
        return "linux"
    elif sys.platform.startswith("win32") or sys.platform.startswith("cygwin"):
        return "win32"
    return "agnostic"


@dataclass
class VoiceConfig:
    """Runtime configuration for Hath0r Voice Engine."""

    enabled: bool = False
    mode: str = "auto"  # off | stub | live | auto
    platform: str = field(default_factory=detect_platform)
    stt_provider: str = "auto"  # auto | native | whisper | websocket | stub
    tts_provider: str = "auto"  # auto | native | say | espeak | sapi | stub
    router_provider: str = "jev"  # jev | heuristic | agent_direct
    min_confidence: float = 0.85
    timeout_ms: int = 250
    cli_binary: str = "hath0r"
    sample_rate: int = 16000
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_env(cls, config_path: Optional[Path | str] = None) -> VoiceConfig:
        """Create configuration merging file config and environment variables."""
        cfg_dict: Dict[str, Any] = {}

        # Resolve config file path
        if config_path is None:
            candidate = Path("cfg/voice.json")
            if candidate.is_file():
                config_path = candidate

        if config_path and Path(config_path).is_file():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        cfg_dict = data
            except Exception:
                pass

        # Environment variable overrides
        mode_env = os.getenv("HATHOR_VOICE_MODE") or os.getenv("JEV_MODE")
        if mode_env:
            cfg_dict["mode"] = mode_env.strip().lower()

        stt_env = os.getenv("HATHOR_VOICE_STT")
        if stt_env:
            cfg_dict["stt_provider"] = stt_env.strip().lower()
            if isinstance(cfg_dict.get("stt"), dict):
                cfg_dict["stt"]["provider"] = stt_env.strip().lower()

        tts_env = os.getenv("HATHOR_VOICE_TTS")
        if tts_env:
            cfg_dict["tts_provider"] = tts_env.strip().lower()
            if isinstance(cfg_dict.get("tts"), dict):
                cfg_dict["tts"]["provider"] = tts_env.strip().lower()

        router_env = os.getenv("HATHOR_VOICE_ROUTER")
        if router_env:
            cfg_dict["router_provider"] = router_env.strip().lower()
            if isinstance(cfg_dict.get("router"), dict):
                cfg_dict["router"]["provider"] = router_env.strip().lower()

        cli_env = os.getenv("HATHOR_CLI_BIN")
        if cli_env:
            cfg_dict["cli_binary"] = cli_env.strip()
            if isinstance(cfg_dict.get("agent_dispatcher"), dict):
                cfg_dict["agent_dispatcher"]["cli_binary"] = cli_env.strip()

        min_conf_env = os.getenv("HATHOR_VOICE_MIN_CONFIDENCE")
        if min_conf_env:
            try:
                val = float(min_conf_env)
                cfg_dict["min_confidence"] = val
                if isinstance(cfg_dict.get("router"), dict):
                    cfg_dict["router"]["min_confidence"] = val
            except ValueError:
                pass

        platform_val = cfg_dict.get("platform")
        if not platform_val or platform_val == "auto":
            platform_val = detect_platform()

        stt_val = cfg_dict.get("stt", {}).get("provider") if isinstance(cfg_dict.get("stt"), dict) else cfg_dict.get("stt_provider")
        tts_val = cfg_dict.get("tts", {}).get("provider") if isinstance(cfg_dict.get("tts"), dict) else cfg_dict.get("tts_provider")
        router_val = cfg_dict.get("router", {}).get("provider") if isinstance(cfg_dict.get("router"), dict) else cfg_dict.get("router_provider")

        return cls(
            enabled=bool(cfg_dict.get("enabled", False) or mode_env in ("stub", "live")),
            mode=str(cfg_dict.get("mode", "auto")),
            platform=platform_val,
            stt_provider=str(stt_val or "auto"),
            tts_provider=str(tts_val or "auto"),
            router_provider=str(router_val or "jev"),
            min_confidence=float(cfg_dict.get("router", {}).get("min_confidence", cfg_dict.get("min_confidence", 0.85))),
            timeout_ms=int(cfg_dict.get("router", {}).get("timeout_ms", cfg_dict.get("timeout_ms", 250))),
            cli_binary=str(cfg_dict.get("agent_dispatcher", {}).get("cli_binary", cfg_dict.get("cli_binary", "hath0r"))),
            extra=cfg_dict,
        )
