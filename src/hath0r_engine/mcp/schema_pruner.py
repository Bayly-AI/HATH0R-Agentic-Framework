"""MCP Gateway Schema Pruner.

Reduces schema overhead ("MCP Schema Tax") by stripping verbose descriptions,
nested schema bloat, and auxiliary properties before LLM prompt injection.
"""

from __future__ import annotations

import copy
import json
from enum import Enum
from typing import Any, Dict, List


class PruningMode(str, Enum):
    """Schema pruning aggressiveness mode."""

    AGGRESSIVE = "aggressive"  # Strips all descriptions, keep names/types/required only
    STANDARD = "standard"  # Truncates descriptions to <=80 chars, limits nesting
    MINIMAL = "minimal"  # Strips top-level schema metadata & auxiliary keys
    NONE = "none"  # Raw unmodified schema


class SchemaPruner:
    """Filters and compresses MCP tool JSON schemas for LLM context injection."""

    def __init__(self, max_description_len: int = 80, max_depth: int = 3) -> None:
        self.max_description_len = max_description_len
        self.max_depth = max_depth

    @staticmethod
    def estimate_tokens(data: Any) -> int:
        """Estimate token count for a JSON object or string using standard 4-char rule of thumb."""
        if isinstance(data, str):
            text = data
        else:
            text = json.dumps(data, separators=(",", ":"))
        return max(1, len(text) // 4)

    def prune_tool(self, tool_def: Dict[str, Any], mode: PruningMode = PruningMode.STANDARD) -> Dict[str, Any]:
        """Prune a single tool definition dictionary."""
        if mode == PruningMode.NONE:
            return copy.deepcopy(tool_def)

        pruned = {
            "name": tool_def.get("name", ""),
        }

        # Handle tool description
        raw_desc = tool_def.get("description", "")
        if mode == PruningMode.AGGRESSIVE:
            pruned["description"] = raw_desc.split(".")[0][:50] if raw_desc else ""
        elif mode == PruningMode.STANDARD:
            pruned["description"] = (
                (raw_desc[: self.max_description_len] + "...")
                if len(raw_desc) > self.max_description_len
                else raw_desc
            )
        else:
            pruned["description"] = raw_desc

        # Handle parameters schema
        params = tool_def.get("parameters") or tool_def.get("inputSchema") or {}
        pruned["parameters"] = self._prune_json_schema(params, mode, depth=0)

        return pruned

    def _prune_json_schema(
        self, schema: Dict[str, Any], mode: PruningMode, depth: int
    ) -> Dict[str, Any]:
        """Recursively prune JSON Schema dictionary."""
        if not isinstance(schema, dict) or depth > self.max_depth:
            return {}

        result: Dict[str, Any] = {}

        # Preserve core schema keys
        if "type" in schema:
            result["type"] = schema["type"]
        if "required" in schema:
            result["required"] = schema["required"]
        if "enum" in schema:
            result["enum"] = schema["enum"][:10]  # Cap lengthy enums

        # Handle description
        if "description" in schema:
            if mode == PruningMode.AGGRESSIVE:
                pass  # Strip parameter descriptions entirely
            elif mode == PruningMode.STANDARD:
                d_text = str(schema["description"])
                result["description"] = (
                    (d_text[: self.max_description_len] + "...")
                    if len(d_text) > self.max_description_len
                    else d_text
                )
            else:
                result["description"] = schema["description"]

        # Handle properties
        if "properties" in schema and isinstance(schema["properties"], dict):
            pruned_props = {}
            for prop_name, prop_val in schema["properties"].items():
                if isinstance(prop_val, dict):
                    pruned_props[prop_name] = self._prune_json_schema(prop_val, mode, depth + 1)
                else:
                    pruned_props[prop_name] = prop_val
            result["properties"] = pruned_props

        # Handle array items
        if "items" in schema and isinstance(schema["items"], dict):
            result["items"] = self._prune_json_schema(schema["items"], mode, depth + 1)

        return result

    def prune_tool_list(
        self, tools: List[Dict[str, Any]], mode: PruningMode = PruningMode.STANDARD
    ) -> List[Dict[str, Any]]:
        """Batch prune a list of tool definitions."""
        return [self.prune_tool(t, mode=mode) for t in tools]
