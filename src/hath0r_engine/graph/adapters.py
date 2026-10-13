"""Pluggable Modality and File Adapters for AgentGraph."""

from __future__ import annotations

import ast
import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .models import (
    RULES_MD_FILENAME,
    AgentGraphEdge,
    AgentGraphNode,
    AgentGraphPlane,
)


class BaseGraphAdapter:
    """Base interface for modality and file adapters in AgentGraph."""

    def can_handle(self, path: Path) -> bool:
        raise NotImplementedError

    def extract(self, path: Path) -> Tuple[List[AgentGraphNode], List[AgentGraphEdge]]:
        raise NotImplementedError


class MarkdownDocAdapter(BaseGraphAdapter):
    """Extracts document nodes and internal links from Markdown files."""

    def can_handle(self, path: Path) -> bool:
        assert path is not None, "path cannot be None"
        return path.suffix.lower() in {".md", ".markdown"}

    def extract(self, path: Path) -> Tuple[List[AgentGraphNode], List[AgentGraphEdge]]:
        assert path is not None, "path cannot be None"
        nodes: List[AgentGraphNode] = []
        edges: List[AgentGraphEdge] = []

        if not path.exists():
            return nodes, edges

        content = path.read_text(encoding="utf-8", errors="replace")
        title = self._extract_title(path, content)
        frontmatter = self._parse_frontmatter(content)

        node_id = f"doc:{path.name}"
        node = AgentGraphNode(
            id=node_id,
            plane=AgentGraphPlane.KNOWLEDGE.value,
            type="document",
            label=title,
            content=content[:1000],
            properties={"path": str(path), "size": len(content)},
        )
        nodes.append(node)

        # Process rule policy if this is a governance file
        if self._is_rule_policy_file(path, frontmatter):
            rule_nodes, rule_edges = self._build_rule_policy_entry(path, frontmatter, title, content)
            nodes.extend(rule_nodes)
            edges.extend(rule_edges)

        # Detect markdown link edges
        edges.extend(self._extract_markdown_links(node_id, content))
        return nodes, edges

    def _extract_title(self, path: Path, content: str) -> str:
        """Extract title from first H1 header or default from path stem."""
        h1_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
        if h1_match:
            return h1_match.group(1).strip()
        return path.stem.replace("-", " ").replace("_", " ").title()

    def _parse_frontmatter(self, content: str) -> Dict[str, Any]:
        """Parse YAML frontmatter key-value pairs if present."""
        frontmatter: Dict[str, Any] = {}
        fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
        if not fm_match:
            return frontmatter

        for line in fm_match.group(1).splitlines():
            if ":" not in line:
                continue
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"\'')
            if val.startswith("[") and val.endswith("]"):
                items = [x.strip().strip('"\'') for x in val[1:-1].split(",") if x.strip()]
                frontmatter[key] = items
            elif val.isdigit():
                frontmatter[key] = int(val)
            else:
                frontmatter[key] = val
        return frontmatter

    def _is_rule_policy_file(self, path: Path, frontmatter: Dict[str, Any]) -> bool:
        """Check if file represents a rule policy."""
        return (
            frontmatter.get("type") == "rule_policy"
            or path.name == RULES_MD_FILENAME
            or "governance/rules" in str(path)
        )

    def _build_rule_policy_entry(
        self,
        path: Path,
        frontmatter: Dict[str, Any],
        title: str,
        content: str,
    ) -> Tuple[List[AgentGraphNode], List[AgentGraphEdge]]:
        """Construct rule policy nodes and role governance edges."""
        nodes: List[AgentGraphNode] = []
        edges: List[AgentGraphEdge] = []

        rule_id = frontmatter.get("id")
        if not rule_id:
            if path.name == RULES_MD_FILENAME:
                parent_dir = path.parent.name
                rule_id = f"rule:subsystem-{parent_dir}"
            else:
                rule_id = f"rule:{path.stem}"

        rule_priority = frontmatter.get("priority", 3)
        if isinstance(rule_priority, str) and rule_priority.isdigit():
            rule_priority = int(rule_priority)

        target_scope = frontmatter.get("target_scope") or (
            path.parent.name if path.name == RULES_MD_FILENAME else "root"
        )

        rule_node = AgentGraphNode(
            id=rule_id,
            plane=AgentGraphPlane.RULES.value,
            type="rule_policy",
            label=frontmatter.get("title") or title,
            content=content,
            properties={
                "path": str(path),
                "priority": rule_priority,
                "target_scope": target_scope,
                "restricted_actions": frontmatter.get("restricted_actions", []),
                "governs_roles": frontmatter.get("governs_roles", []),
            },
        )
        nodes.append(rule_node)

        for role_name in frontmatter.get("governs_roles", []):
            edges.append(
                AgentGraphEdge(
                    source=rule_id,
                    target=f"role:{role_name}",
                    relation="GOVERNS",
                    plane=AgentGraphPlane.RULES.value,
                )
            )
        return nodes, edges

    def _extract_markdown_links(self, source_node_id: str, content: str) -> List[AgentGraphEdge]:
        """Extract markdown link target edges."""
        edges: List[AgentGraphEdge] = []
        for target in re.findall(r"\[.*?\]\((.*?\.md)\)", content):
            target_name = Path(target).name
            edges.append(
                AgentGraphEdge(
                    source=source_node_id,
                    target=f"doc:{target_name}",
                    relation="references",
                    plane=AgentGraphPlane.KNOWLEDGE.value,
                )
            )
        return edges


class ASTCodeAdapter(BaseGraphAdapter):
    """Extracts classes, functions, and import dependencies from Python files."""

    def can_handle(self, path: Path) -> bool:
        assert path is not None, "path cannot be None"
        return path.suffix.lower() == ".py"

    def extract(self, path: Path) -> Tuple[List[AgentGraphNode], List[AgentGraphEdge]]:
        assert path is not None, "path cannot be None"
        nodes: List[AgentGraphNode] = []
        edges: List[AgentGraphEdge] = []

        if not path.exists():
            return nodes, edges

        try:
            content = path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(content, filename=str(path))
        except SyntaxError:
            return nodes, edges

        module_id = f"module:{path.stem}"
        nodes.append(
            AgentGraphNode(
                id=module_id,
                plane=AgentGraphPlane.EXTENSIBLE.value,
                type="code_module",
                label=path.name,
                content="",
                properties={"path": str(path)},
            )
        )

        for stmt in tree.body:
            if isinstance(stmt, ast.ClassDef):
                self._extract_class_def(path, module_id, stmt, nodes, edges)
            elif isinstance(stmt, ast.FunctionDef):
                self._extract_function_def(path, module_id, stmt, nodes, edges)

        return nodes, edges

    def _extract_class_def(
        self,
        path: Path,
        module_id: str,
        stmt: ast.ClassDef,
        nodes: List[AgentGraphNode],
        edges: List[AgentGraphEdge],
    ) -> None:
        class_id = f"class:{path.stem}.{stmt.name}"
        nodes.append(
            AgentGraphNode(
                id=class_id,
                plane=AgentGraphPlane.EXTENSIBLE.value,
                type="code_class",
                label=stmt.name,
                content=ast.get_docstring(stmt) or "",
                properties={"module": path.stem},
            )
        )
        edges.append(
            AgentGraphEdge(
                source=module_id,
                target=class_id,
                relation="contains",
                plane=AgentGraphPlane.EXTENSIBLE.value,
            )
        )

    def _extract_function_def(
        self,
        path: Path,
        module_id: str,
        stmt: ast.FunctionDef,
        nodes: List[AgentGraphNode],
        edges: List[AgentGraphEdge],
    ) -> None:
        func_id = f"func:{path.stem}.{stmt.name}"
        nodes.append(
            AgentGraphNode(
                id=func_id,
                plane=AgentGraphPlane.EXTENSIBLE.value,
                type="code_function",
                label=stmt.name,
                content=ast.get_docstring(stmt) or "",
                properties={"module": path.stem},
            )
        )
        edges.append(
            AgentGraphEdge(
                source=module_id,
                target=func_id,
                relation="contains",
                plane=AgentGraphPlane.EXTENSIBLE.value,
            )
        )
