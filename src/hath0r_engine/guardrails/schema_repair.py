"""Pydantic and JSON Schema Automatic Repair Engine for Tool Arguments."""

from __future__ import annotations

import json
from typing import Any, Dict, Tuple


class SchemaRepairEngine:
    """Repairs common LLM parameter formatting anomalies and coercions."""

    def repair_arguments(self, args: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
        """Perform automatic type repairs on tool argument dictionary."""
        repaired = dict(args)
        modified = False

        for key, val in list(repaired.items()):
            if isinstance(val, str):
                # 1. Boolean string coercion
                if val.lower() == "true":
                    repaired[key] = True
                    modified = True
                elif val.lower() == "false":
                    repaired[key] = False
                    modified = True
                # 2. Integer coercion
                elif val.isdigit() or (val.startswith("-") and val[1:].isdigit()):
                    repaired[key] = int(val)
                    modified = True
                # 3. Float coercion
                elif self._is_float(val):
                    repaired[key] = float(val)
                    modified = True
                # 4. Nested JSON string decoding
                elif (val.startswith("{") and val.endswith("}")) or (val.startswith("[") and val.endswith("]")):
                    try:
                        parsed = json.loads(val)
                        repaired[key] = parsed
                        modified = True
                    except Exception:
                        pass

        return repaired, modified

    def _is_float(self, val: str) -> bool:
        try:
            if "." in val:
                float(val)
                return True
        except ValueError:
            pass
        return False
