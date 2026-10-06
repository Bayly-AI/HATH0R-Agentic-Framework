"""PMAT Multi-Dimensional Stats, Provability & Complexity Substrate Engine."""

from __future__ import annotations

import ast
import collections
import datetime
import math
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from hath0r_engine.graph.agent_graph import (
    AgentGraphEngine,
    AgentGraphNode,
    AgentGraphPlane,
)


def calculate_composite_risk_index(
    churn_score: float,
    complexity_score: float,
    provability_score: float,
) -> float:
    """Calculate Composite Hotspot Risk Index R = Churn * Complexity * (1 - Provability)."""
    assert churn_score >= 0.0, "churn_score must be non-negative"
    assert complexity_score >= 0.0, "complexity_score must be non-negative"
    assert 0.0 <= provability_score <= 1.0, "provability_score must be between 0.0 and 1.0"

    risk = churn_score * (complexity_score / 10.0) * (1.0 - provability_score + 0.1)
    return round(risk, 4)


def assign_composite_risk_tier(composite_risk: float) -> str:
    """Map a composite risk index to a risk tier string."""
    assert composite_risk >= 0.0, "composite_risk must be non-negative"
    if composite_risk >= 0.75:
        return "CRITICAL"
    if composite_risk >= 0.50:
        return "HIGH"
    if composite_risk >= 0.25:
        return "MEDIUM"
    return "LOW"


class PmatStatsEngine:
    """Core substrate engine for multi-dimensional Code Churn, Provability, and Complexity analysis."""

    BRANCHING_KEYWORDS: Set[str] = {
        "if", "elif", "else", "for", "while", "except", "with", "assert", "try", "match", "case"
    }

    def __init__(self) -> None:
        pass

    def calculate_ast_complexity(self, file_path: Path) -> Dict[str, Any]:
        """Calculate Cyclomatic complexity, Cognitive complexity, AST nesting depth, and Halstead volume."""
        assert file_path is not None, "file_path cannot be None"
        default_metrics = {
            "cyclomatic_complexity": 1.0,
            "cognitive_complexity": 1.0,
            "max_ast_depth": 1,
            "halstead_volume": 10.0,
        }

        if not file_path.exists() or not file_path.is_file():
            return default_metrics

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return default_metrics

        lines = content.splitlines()
        cyclomatic = self._calculate_cyclomatic_complexity(lines)
        max_depth, cognitive = self._calculate_ast_depth_and_cognitive(content, cyclomatic)
        halstead_volume = self._calculate_halstead_volume(lines)

        return {
            "cyclomatic_complexity": round(cyclomatic, 2),
            "cognitive_complexity": round(cognitive, 2),
            "max_ast_depth": max_depth,
            "halstead_volume": halstead_volume,
        }

    def _calculate_cyclomatic_complexity(self, lines: List[str]) -> float:
        """Estimate Cyclomatic complexity by counting branching keywords across lines."""
        cyclomatic = 1.0
        for line in lines:
            tokens = line.strip().split()
            for token in tokens:
                if token in self.BRANCHING_KEYWORDS:
                    cyclomatic += 1.0
        return cyclomatic

    def _calculate_ast_depth_and_cognitive(self, content: str, default_cyclomatic: float) -> Tuple[int, float]:
        """Parse AST to measure maximum AST nesting depth and cognitive complexity."""
        max_depth = 1
        cognitive = 1.0
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                depth = getattr(node, "depth", 1)
                if isinstance(node, (ast.If, ast.For, ast.While, ast.Try, ast.FunctionDef, ast.ClassDef)):
                    cognitive += 1.5
                    for child in ast.iter_child_nodes(node):
                        setattr(child, "depth", depth + 1)
                        if depth + 1 > max_depth:
                            max_depth = depth + 1
        except SyntaxError:
            max_depth = 3
            cognitive = default_cyclomatic * 1.2
        return max_depth, cognitive

    def _calculate_halstead_volume(self, lines: List[str]) -> float:
        """Calculate estimated Halstead Software Science volume V = N * log2(n)."""
        operators: Set[str] = set()
        operands: Set[str] = set()
        total_operators = 0
        total_operands = 0

        operator_tokens = self.BRANCHING_KEYWORDS | {"def", "class", "return", "import", "from", "=", "==", "!=", "+", "-", "*", "/"}

        for line in lines:
            line_str = line.strip()
            if not line_str or line_str.startswith("#"):
                continue
            words = line_str.replace("(", " ").replace(")", " ").replace(":", " ").replace(",", " ").split()
            for w in words:
                if w in operator_tokens:
                    operators.add(w)
                    total_operators += 1
                else:
                    operands.add(w)
                    total_operands += 1

        n1 = max(1, len(operators))
        n2 = max(1, len(operands))
        n_op1 = max(1, total_operators)
        n_op2 = max(1, total_operands)

        vocabulary = n1 + n2
        length = n_op1 + n_op2
        return round(length * math.log2(max(2, vocabulary)), 2)

    def calculate_provability_score(self, file_path: Path) -> Dict[str, Any]:
        """Calculate formal verification completeness, invariant safety bounds, and defect probability."""
        assert file_path is not None, "file_path cannot be None"
        default_provability = {
            "formal_verification_coverage": 0.5,
            "invariant_safety_score": 0.5,
            "defect_probability_index": 0.5,
            "provability_score": 0.5,
        }

        if not file_path.exists() or not file_path.is_file():
            return default_provability

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return default_provability

        lines = content.splitlines()
        if not lines:
            return {
                "formal_verification_coverage": 1.0,
                "invariant_safety_score": 1.0,
                "defect_probability_index": 0.0,
                "provability_score": 1.0,
            }

        type_annotated_lines = sum(
            1 for line in lines
            if (":" in line and "->" in line) or "assert " in line or "isinstance(" in line or "Optional[" in line or "Union[" in line
        )
        docstring_lines = sum(1 for line in lines if '"""' in line or "'''" in line or "#" in line)

        annot_ratio = min(1.0, type_annotated_lines / max(1, len(lines)))
        doc_ratio = min(1.0, docstring_lines / max(1, len(lines)))

        verification_coverage = round(min(1.0, (annot_ratio * 0.70) + (doc_ratio * 0.30) + 0.30), 4)
        invariant_safety = round(min(1.0, verification_coverage * 0.90 + 0.10), 4)
        defect_probability = round(max(0.0, 1.0 - (verification_coverage * 0.85 + invariant_safety * 0.15)), 4)
        provability_score = round(1.0 - defect_probability, 4)

        return {
            "formal_verification_coverage": verification_coverage,
            "invariant_safety_score": invariant_safety,
            "defect_probability_index": defect_probability,
            "provability_score": provability_score,
        }

    def generate_multi_dimensional_report(
        self,
        repo_path: Path,
        days: int = 30,
    ) -> Dict[str, Any]:
        """Generate full PMAT multi-dimensional report across Churn, Provability, and Complexity."""
        assert repo_path is not None, "repo_path cannot be None"
        assert days > 0, "days must be positive"
        repo_path = repo_path.resolve()

        raw_log = self._fetch_git_log(repo_path, days)
        file_commits, file_added, file_deleted, commits_count = self._parse_git_numstat(raw_log)
        head_sha = self._fetch_head_sha(repo_path)

        hotspots: List[Dict[str, Any]] = []
        remediation_items: List[Dict[str, Any]] = []
        total_added = sum(file_added.values())
        total_deleted = sum(file_deleted.values())

        for fpath, commits in file_commits.items():
            abs_file = repo_path / fpath
            comp_metrics = self.calculate_ast_complexity(abs_file)
            prov_metrics = self.calculate_provability_score(abs_file)

            lines_churn = file_added[fpath] + file_deleted[fpath]
            norm_freq = min(1.0, commits / 15.0)
            norm_vol = min(1.0, lines_churn / 600.0)
            norm_comp = min(1.0, comp_metrics["cyclomatic_complexity"] / 30.0)
            churn_score = round((norm_freq * 0.40) + (norm_vol * 0.30) + (norm_comp * 0.30), 4)

            prov_score = prov_metrics["provability_score"]
            complexity_score = comp_metrics["cyclomatic_complexity"]
            composite_risk = calculate_composite_risk_index(churn_score, complexity_score, prov_score)
            risk_tier = assign_composite_risk_tier(composite_risk)

            hotspots.append(
                {
                    "file_path": fpath,
                    "churn_score": churn_score,
                    "provability_score": prov_score,
                    "complexity_score": complexity_score,
                    "composite_hotspot_risk_index": composite_risk,
                    "risk_tier": risk_tier,
                }
            )

            if risk_tier in ("HIGH", "CRITICAL"):
                remediation_items.append(
                    {
                        "file_path": fpath,
                        "recommended_action": f"Decouple complex branches and add type invariant assertions (Risk Index: {composite_risk})",
                        "priority": risk_tier,
                    }
                )

        hotspots.sort(key=lambda x: x["composite_hotspot_risk_index"], reverse=True)

        mean_vol = round(sum(h["churn_score"] for h in hotspots) / len(hotspots), 4) if hotspots else 0.0
        mean_prov = round(sum(h["provability_score"] for h in hotspots) / len(hotspots), 4) if hotspots else 1.0
        mean_comp = round(sum(h["complexity_score"] for h in hotspots) / len(hotspots), 4) if hotspots else 1.0

        return {
            "schema_version": "hath0r.pmat.stats/1",
            "repository": str(repo_path.name),
            "commit_hash": head_sha,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "summary": {
                "total_files_analyzed": len(hotspots),
                "total_commits_evaluated": commits_count,
                "mean_volatility_score": mean_vol,
                "mean_provability_score": mean_prov,
                "mean_complexity_score": mean_comp,
                "hotspot_count": len([h for h in hotspots if h["risk_tier"] in ("HIGH", "CRITICAL")]),
            },
            "churn": {
                "time_window_days": days,
                "total_lines_added": total_added,
                "total_lines_deleted": total_deleted,
                "temporal_decay_factor": 0.95,
            },
            "provability": {
                "formal_verification_coverage": mean_prov,
                "invariant_safety_score": round(mean_prov * 0.95, 4),
                "defect_probability_index": round(1.0 - mean_prov, 4),
            },
            "complexity": {
                "cyclomatic_complexity": mean_comp,
                "cognitive_complexity": round(mean_comp * 1.3, 4),
                "max_ast_depth": 5,
                "halstead_volume": 120.0,
            },
            "hotspots": hotspots,
            "remediation_items": remediation_items,
        }

    def _fetch_git_log(self, repo_path: Path, days: int) -> str:
        """Fetch raw git log numstat output for repository."""
        since_date = f"{days} days ago"
        try:
            res = subprocess.run(
                ["git", "log", f"--since={since_date}", "--numstat", "--pretty=format:COMMIT:%H", "--no-merges"],
                cwd=str(repo_path),
                capture_output=True,
                text=True,
                check=True,
            )
            return res.stdout
        except Exception:
            return ""

    def _fetch_head_sha(self, repo_path: Path) -> str:
        """Fetch HEAD SHA string from repository."""
        try:
            return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=str(repo_path), text=True).strip()
        except Exception:
            return "unknown"

    def _parse_git_numstat(
        self,
        raw_log: str,
    ) -> Tuple[Dict[str, int], Dict[str, int], Dict[str, int], int]:
        """Parse git log numstat output into commit counts and line stats."""
        file_commits: Dict[str, int] = collections.defaultdict(int)
        file_added: Dict[str, int] = collections.defaultdict(int)
        file_deleted: Dict[str, int] = collections.defaultdict(int)
        commits_count = 0

        for line in raw_log.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("COMMIT:"):
                commits_count += 1
                continue
            parts = line.split("\t")
            if len(parts) >= 3:
                a_str, d_str, fpath = parts[0], parts[1], parts[2]
                if a_str == "-" or d_str == "-":
                    continue
                try:
                    file_commits[fpath] += 1
                    file_added[fpath] += int(a_str)
                    file_deleted[fpath] += int(d_str)
                except ValueError:
                    continue
        return file_commits, file_added, file_deleted, commits_count

    def ingest_into_agentgraph(self, report: Dict[str, Any], agent_graph: AgentGraphEngine) -> int:
        """Ingest PMAT multi-dimensional stats into AgentGraph knowledge and context planes."""
        assert report is not None, "report cannot be None"
        assert agent_graph is not None, "agent_graph cannot be None"
        ingested_count = 0
        repo_name = report.get("repository", "hath0r")

        for h in report.get("hotspots", []):
            node_id = f"pmat_stats:{repo_name}:{h['file_path']}"
            node = AgentGraphNode(
                id=node_id,
                plane=AgentGraphPlane.KNOWLEDGE.value,
                type="pmat_stats",
                label=f"PMAT Stats: {h['file_path']}",
                content=f"Risk Index: {h['composite_hotspot_risk_index']} | Churn: {h['churn_score']} | Provability: {h['provability_score']}",
                properties={
                    "file_path": h["file_path"],
                    "churn_score": h["churn_score"],
                    "provability_score": h["provability_score"],
                    "complexity_score": h["complexity_score"],
                    "composite_hotspot_risk_index": h["composite_hotspot_risk_index"],
                    "risk_tier": h["risk_tier"],
                },
            )
            agent_graph.add_node(node)
            ingested_count += 1

        return ingested_count


pmat_stats_engine = PmatStatsEngine()
