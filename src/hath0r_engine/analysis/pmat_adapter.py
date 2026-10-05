"""PMAT (Pragmatic Multi-language Agent Toolkit) Churn & Hotspot Analysis Adapter.

Provides zero-overhead AST and git-volatility analysis, AgentGraph integration,
and dynamic LLM reasoning escalation based on code churn. Conforms to CR-CICCCD-001.
"""

from __future__ import annotations

import collections
import datetime
import json
import logging
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger("hath0r.analysis.pmat")


class PmatAdapter:
    """Adapter bridging PMAT CLI/MCP engine and Hath0r cognitive substrates."""

    def __init__(
        self,
        pmat_bin: str = "pmat",
        mcp_router: Optional[Any] = None,
    ) -> None:
        self.pmat_bin = pmat_bin
        self.mcp_router = mcp_router

    def is_pmat_available(self) -> bool:
        """Check if native PMAT binary is installed in system PATH."""
        return shutil.which(self.pmat_bin) is not None

    def analyze_churn(
        self,
        repo_path: str | Path,
        days: int = 30,
    ) -> Dict[str, Any]:
        """Perform comprehensive code churn and architectural hotspot analysis.

        Falls back to high-performance git log parsing if native pmat binary is absent.
        """
        target_path = Path(repo_path).resolve()
        if not target_path.exists():
            raise FileNotFoundError(f"Repository path does not exist: {target_path}")

        # Attempt native PMAT binary execution if present
        if self.is_pmat_available():
            try:
                res = subprocess.run(
                    [self.pmat_bin, "churn", "--days", str(days), "--json"],
                    cwd=str(target_path),
                    capture_output=True,
                    text=True,
                    check=False,
                )
                if res.returncode == 0 and res.stdout.strip():
                    data = json.loads(res.stdout)
                    if isinstance(data, dict) and "hotspots" in data:
                        return data
            except Exception as e:
                logger.warning("Native pmat execution failed, falling back to git: %s", e)

        return self._analyze_churn_via_git(target_path, days=days)

    def _analyze_churn_via_git(
        self,
        repo_path: Path,
        days: int = 30,
    ) -> Dict[str, Any]:
        """High-speed git log parser extracting commit churn, lines changed, and co-changes."""
        since_date = f"{days} days ago"

        # 1. Extract commit metadata and file stats
        cmd = [
            "git",
            "log",
            f"--since={since_date}",
            "--numstat",
            "--pretty=format:COMMIT:%H",
            "--no-merges",
        ]

        try:
            res = subprocess.run(
                cmd,
                cwd=str(repo_path),
                capture_output=True,
                text=True,
                check=True,
            )
            raw_output = res.stdout
        except Exception as e:
            logger.error("Git log execution failed: %s", e)
            raw_output = ""

        # Parse output
        file_churn: Dict[str, int] = collections.defaultdict(int)
        file_added: Dict[str, int] = collections.defaultdict(int)
        file_deleted: Dict[str, int] = collections.defaultdict(int)
        co_changes: Dict[str, Set[str]] = collections.defaultdict(set)

        current_commit_files: List[str] = []
        commits_evaluated = 0

        for line in raw_output.splitlines():
            line = line.strip()
            if not line:
                continue
            if line.startswith("COMMIT:"):
                commits_evaluated += 1
                if current_commit_files:
                    for f1 in current_commit_files:
                        for f2 in current_commit_files:
                            if f1 != f2:
                                co_changes[f1].add(f2)
                current_commit_files = []
                continue

            parts = line.split("\t")
            if len(parts) >= 3:
                added_str, deleted_str, path_str = parts[0], parts[1], parts[2]
                # Filter out binary files and common non-code files
                if added_str == "-" or deleted_str == "-":
                    continue
                try:
                    added = int(added_str)
                    deleted = int(deleted_str)
                except ValueError:
                    continue

                file_churn[path_str] += 1
                file_added[path_str] += added
                file_deleted[path_str] += deleted
                current_commit_files.append(path_str)

        if current_commit_files:
            for f1 in current_commit_files:
                for f2 in current_commit_files:
                    if f1 != f2:
                        co_changes[f1].add(f2)

        # 2. Extract commit hash
        try:
            head_sha = (
                subprocess.check_output(
                    ["git", "rev-parse", "HEAD"],
                    cwd=str(repo_path),
                    text=True,
                )
                .strip()
            )
        except Exception:
            head_sha = "unknown"

        # 3. Calculate complexity and volatility scores
        hotspots: List[Dict[str, Any]] = []
        total_churn_lines = 0

        for fpath, churn_count in file_churn.items():
            added = file_added[fpath]
            deleted = file_deleted[fpath]
            lines_churn = added + deleted
            total_churn_lines += lines_churn

            # Estimate complexity based on file size, indentation, or AST
            abs_file = repo_path / fpath
            complexity_score = self._estimate_file_complexity(abs_file)

            # Volatility Score Calculation: (Normalized 0.0 - 1.0)
            # Weighted formula: 40% churn frequency, 30% volume, 30% complexity
            norm_freq = min(1.0, churn_count / 15.0)
            norm_vol = min(1.0, lines_churn / 600.0)
            norm_comp = min(1.0, complexity_score / 30.0)
            volatility_score = round((norm_freq * 0.40) + (norm_vol * 0.30) + (norm_comp * 0.30), 4)

            # Assign Risk Tier
            if volatility_score >= 0.75:
                risk_tier = "CRITICAL"
            elif volatility_score >= 0.50:
                risk_tier = "HIGH"
            elif volatility_score >= 0.25:
                risk_tier = "MEDIUM"
            else:
                risk_tier = "LOW"

            co_list = sorted(list(co_changes[fpath]))[:5]

            hotspots.append(
                {
                    "file_path": fpath,
                    "churn_count": churn_count,
                    "lines_added": added,
                    "lines_deleted": deleted,
                    "complexity_score": complexity_score,
                    "volatility_score": volatility_score,
                    "risk_tier": risk_tier,
                    "co_changing_files": co_list,
                }
            )

        # Sort hotspots by volatility descending
        hotspots.sort(key=lambda x: x["volatility_score"], reverse=True)

        mean_vol = (
            round(sum(h["volatility_score"] for h in hotspots) / len(hotspots), 4)
            if hotspots
            else 0.0
        )

        recommendations: List[str] = []
        critical_hotspots = [h for h in hotspots if h["risk_tier"] == "CRITICAL"]
        if critical_hotspots:
            recommendations.append(
                f"Refactor critical hotspot '{critical_hotspots[0]['file_path']}' with high volatility score {critical_hotspots[0]['volatility_score']}."
            )
        high_co_change = [h for h in hotspots if len(h["co_changing_files"]) >= 3]
        if high_co_change:
            recommendations.append(
                f"Module '{high_co_change[0]['file_path']}' has tight coupling with {len(high_co_change[0]['co_changing_files'])} co-changing files; consider applying Facade or Event Dispatcher pattern."
            )

        report = {
            "schema_version": "hath0r.pmat.churn/1",
            "repository": str(repo_path.name),
            "commit_hash": head_sha,
            "analysis_window_days": days,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "summary": {
                "total_files_analyzed": len(hotspots),
                "total_commits_evaluated": commits_evaluated,
                "total_churn_lines": total_churn_lines,
                "mean_volatility_score": mean_vol,
                "hotspot_count": len([h for h in hotspots if h["risk_tier"] in ("HIGH", "CRITICAL")]),
            },
            "hotspots": hotspots,
            "recommendations": recommendations,
        }
        return report

    def _estimate_file_complexity(self, file_path: Path) -> float:
        """Estimate file cyclomatic and syntactic complexity without heavy AST parse tax."""
        if not file_path.exists() or not file_path.is_file():
            return 1.0

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return 1.0

        lines = content.splitlines()
        if not lines:
            return 1.0

        # Branching keyword count heuristics (if, elif, for, while, switch, case, catch, match)
        branching_keywords = {"if ", "elif ", "for ", "while ", "case ", "catch ", "except ", "match "}
        branch_count = sum(
            1 for line in lines for kw in branching_keywords if kw in line.strip()
        )
        # Indentation depth penalty
        deep_indent_count = sum(1 for line in lines if len(line) - len(line.lstrip(" ")) >= 12)

        raw_score = 1.0 + (branch_count * 0.5) + (deep_indent_count * 0.2)
        return round(min(50.0, raw_score), 2)

    def get_hotspots(
        self,
        repo_path: str | Path,
        days: int = 30,
        limit: int = 10,
    ) -> List[Dict[str, Any]]:
        """Return top N hotspot files sorted by volatility score."""
        report = self.analyze_churn(repo_path, days=days)
        return report.get("hotspots", [])[:limit]

    def evaluate_pr_risk(
        self,
        repo_path: str | Path,
        base_branch: str = "development",
    ) -> Dict[str, Any]:
        """Evaluate git diff churn risk for PR review gates."""
        target_path = Path(repo_path).resolve()
        report = self.analyze_churn(target_path, days=30)
        hotspot_map = {h["file_path"]: h for h in report.get("hotspots", [])}

        # Get changed files in current branch vs base
        try:
            diff_files_raw = subprocess.check_output(
                ["git", "diff", "--name-only", f"origin/{base_branch}...HEAD"],
                cwd=str(target_path),
                text=True,
            )
        except Exception:
            try:
                diff_files_raw = subprocess.check_output(
                    ["git", "diff", "--name-only", f"{base_branch}...HEAD"],
                    cwd=str(target_path),
                    text=True,
                )
            except Exception:
                diff_files_raw = ""

        changed_files = [f.strip() for f in diff_files_raw.splitlines() if f.strip()]
        touched_hotspots: List[Dict[str, Any]] = []
        max_volatility = 0.0

        for f in changed_files:
            if f in hotspot_map:
                h = hotspot_map[f]
                touched_hotspots.append(h)
                if h["volatility_score"] > max_volatility:
                    max_volatility = h["volatility_score"]

        # Risk Decision
        if max_volatility >= 0.75:
            overall_risk = "CRITICAL"
            safe_to_merge = False
            recommended_tier = "REASONING"
        elif max_volatility >= 0.50:
            overall_risk = "HIGH"
            safe_to_merge = True
            recommended_tier = "REASONING"
        elif max_volatility >= 0.25:
            overall_risk = "MEDIUM"
            safe_to_merge = True
            recommended_tier = "STANDARD"
        else:
            overall_risk = "LOW"
            safe_to_merge = True
            recommended_tier = "LIGHT"

        return {
            "branch_evaluated": "HEAD",
            "base_branch": base_branch,
            "changed_files_count": len(changed_files),
            "touched_hotspots": touched_hotspots,
            "max_volatility_score": max_volatility,
            "overall_risk_tier": overall_risk,
            "safe_to_merge": safe_to_merge,
            "recommended_reasoning_tier": recommended_tier,
        }

    def ingest_into_agentgraph(
        self,
        report: Dict[str, Any],
        agent_graph: Any,
    ) -> int:
        """Inject file volatility weights and co-changing relation edges into AgentGraph."""
        from hath0r_engine.graph.agent_graph import AgentGraphEdge, AgentGraphNode, AgentGraphPlane

        updated_count = 0
        hotspots = report.get("hotspots", [])

        for h in hotspots:
            node_id = f"file:{h['file_path']}"
            properties = {
                "file_path": h["file_path"],
                "volatility_score": h["volatility_score"],
                "churn_count": h["churn_count"],
                "complexity_score": h["complexity_score"],
                "risk_tier": h["risk_tier"],
            }
            if hasattr(agent_graph, "add_node"):
                try:
                    node = AgentGraphNode(
                        id=node_id,
                        plane=AgentGraphPlane.KNOWLEDGE.value,
                        type="file_hotspot",
                        label=h["file_path"],
                        content=f"Hotspot file {h['file_path']} with volatility score {h['volatility_score']}",
                        properties=properties,
                    )
                    agent_graph.add_node(node)
                    updated_count += 1
                except Exception as e:
                    logger.debug("Failed adding node %s to agent_graph: %s", node_id, e)

            # Ingest co-changing relational edges
            for co_f in h.get("co_changing_files", []):
                target_id = f"file:{co_f}"
                if hasattr(agent_graph, "add_edge"):
                    try:
                        edge = AgentGraphEdge(
                            source=node_id,
                            target=target_id,
                            relation="CO_CHANGES_WITH",
                            plane=AgentGraphPlane.KNOWLEDGE.value,
                            weight=round(h["volatility_score"], 2),
                        )
                        agent_graph.add_edge(edge)
                        updated_count += 1
                    except Exception as e:
                        logger.debug("Failed adding edge %s -> %s: %s", node_id, target_id, e)

        return updated_count


pmat_adapter = PmatAdapter()
