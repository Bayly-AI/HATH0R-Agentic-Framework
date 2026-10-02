"""Bi-Directional State Synchronization between Dashboard and Agent State."""

from __future__ import annotations

from typing import Any, Callable, Dict, List


class BiDirectionalStateSync:
    """Synchronizes parameter changes made by humans on dashboard cards into active agent state."""

    def __init__(self) -> None:
        self._listeners: List[Callable[[str, Any], None]] = []

    def register_listener(self, callback: Callable[[str, Any], None]) -> None:
        """Register callback invoked whenever state is synced."""
        self._listeners.append(callback)

    def apply_update(
        self,
        target_state: Dict[str, Any],
        param_key: str,
        new_val: Any,
    ) -> bool:
        """Apply human modification to agent state dictionary and notify listeners."""
        target_state[param_key] = new_val
        for listener in self._listeners:
            try:
                listener(param_key, new_val)
            except Exception:
                pass
        return True
