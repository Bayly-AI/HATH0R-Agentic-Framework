"""AST and Static Syntax Security Validators for Tool Invocations."""

from __future__ import annotations

import ast
import re
from typing import List


class SyntaxGuardrail:
    """Evaluates Python code snippets, bash commands, and SQL queries against security invariants."""

    DANGEROUS_PYTHON_CALLS = {"os.system", "subprocess.call", "subprocess.Popen", "subprocess.run", "eval", "exec"}
    DANGEROUS_BASH_PATTERNS = [
        r"\brm\s+-(?:r|f|rf|fr)\s+/(?:\s|$)",
        r"\brm\s+-(?:r|f|rf|fr)\s+~(?:\s|$)",
        r"\bchmod\s+777\s+/",
        r"\bmkfs\b",
        r"\bdd\s+if=",
        r":\(\)\s*\{\s*:\s*\|\s*:\s*&\s*\}\s*;\s*:",  # fork bomb
    ]
    DESTRUCTIVE_SQL_PATTERNS = [
        r"\bDROP\s+(?:DATABASE|SCHEMA|TABLE)\b",
        r"\bTRUNCATE\s+TABLE\b",
        r"\bALTER\s+TABLE\s+.*\bDROP\s+COLUMN\b",
    ]

    def validate_python_code(self, code_str: str) -> List[str]:
        """Parse Python AST and detect forbidden execution calls."""
        violations: List[str] = []
        try:
            tree = ast.parse(code_str)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    # Check direct function call: eval(), exec()
                    if isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec"):
                        violations.append(f"Forbidden dynamic execution function: {node.func.id}")
                    # Check attribute call: os.system(), subprocess.run()
                    elif isinstance(node.func, ast.Attribute):
                        full_name = self._get_attr_name(node.func)
                        if full_name in self.DANGEROUS_PYTHON_CALLS:
                            violations.append(f"Forbidden OS execution call: {full_name}")
        except SyntaxError as err:
            violations.append(f"Syntax error in code payload: {err.msg}")
        except Exception as err:
            violations.append(f"AST parsing exception: {str(err)}")
        return violations

    def validate_bash_command(self, cmd_str: str) -> List[str]:
        """Detect destructive bash commands."""
        violations: List[str] = []
        for pattern in self.DANGEROUS_BASH_PATTERNS:
            if re.search(pattern, cmd_str, re.IGNORECASE):
                violations.append(f"Destructive shell pattern detected: {pattern}")
        return violations

    def validate_sql_query(self, sql_str: str) -> List[str]:
        """Detect destructive schema mutations or unconstrained DELETE queries."""
        violations: List[str] = []
        for pattern in self.DESTRUCTIVE_SQL_PATTERNS:
            if re.search(pattern, sql_str, re.IGNORECASE):
                violations.append(f"Destructive SQL operation detected matching pattern: {pattern}")

        # Check for unconstrained DELETE
        if re.search(r"\bDELETE\s+FROM\s+\w+\s*(?:;|$)", sql_str, re.IGNORECASE):
            violations.append("Destructive SQL operation: DELETE statement missing WHERE clause.")
        return violations

    def _get_attr_name(self, node: ast.Attribute) -> str:
        parts = [node.attr]
        curr = node.value
        while isinstance(curr, ast.Attribute):
            parts.append(curr.attr)
            curr = curr.value
        if isinstance(curr, ast.Name):
            parts.append(curr.id)
        return ".".join(reversed(parts))
