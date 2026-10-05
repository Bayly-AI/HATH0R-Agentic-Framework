"""Generative UI Churn Heatmap Widget & Evidence Component.

Renders interactive scatter plots and volatility grids (churn frequency vs. complexity)
with cryptographic evidence handshakes conforming to CR-PLAYWRIGHT-UI-001.
"""

from __future__ import annotations

import json
import uuid
from typing import Any, Dict, Optional

from hath0r_engine.ui.protocol import EvidenceComponent, EvidenceType


class ChurnHeatmapComponent:
    """Builder and renderer for interactive code churn & architectural hotspot visualizations."""

    def __init__(
        self,
        report_data: Dict[str, Any],
        title: str = "PMAT Code Churn & Architectural Hotspot Heatmap",
        component_id: Optional[str] = None,
    ) -> None:
        self.report_data = report_data
        self.title = title
        self.component_id = component_id or f"heatmap-{uuid.uuid4().hex[:8]}"

    def to_evidence_component(self) -> EvidenceComponent:
        """Serialize as an interactive EvidenceComponent."""
        hotspots = self.report_data.get("hotspots", [])
        summary = self.report_data.get("summary", {})

        points = []
        for h in hotspots:
            points.append(
                {
                    "file_path": h["file_path"],
                    "churn_count": h["churn_count"],
                    "complexity_score": h["complexity_score"],
                    "volatility_score": h["volatility_score"],
                    "total_churn_lines": h["lines_added"] + h["lines_deleted"],
                    "risk_tier": h["risk_tier"],
                    "co_changing_files": h.get("co_changing_files", []),
                }
            )

        return EvidenceComponent(
            component_id=self.component_id,
            type=EvidenceType.CHURN_HEATMAP,
            title=self.title,
            props={
                "repository": self.report_data.get("repository", "unknown"),
                "commit_hash": self.report_data.get("commit_hash", "HEAD"),
                "summary": summary,
                "data_points": points,
                "recommendations": self.report_data.get("recommendations", []),
            },
        )

    def render_html(self) -> str:
        """Render a self-contained, interactive HTML widget for dashboard & Playwright UI testing."""
        props = self.to_evidence_component().props
        points_json = json.dumps(props["data_points"])
        summary = props["summary"]

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{self.title}</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0d1117; color: #c9d1d9; margin: 0; padding: 24px; }}
    .card {{ background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 20px; max-width: 900px; margin: 0 auto; box-shadow: 0 4px 12px rgba(0,0,0,0.5); }}
    .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #30363d; padding-bottom: 12px; margin-bottom: 16px; }}
    .title {{ font-size: 18px; font-weight: 600; color: #58a6ff; margin: 0; }}
    .badge {{ background: #238636; color: white; padding: 4px 8px; border-radius: 12px; font-size: 12px; font-weight: 600; }}
    .badge.CRITICAL {{ background: #da3633; }}
    .badge.HIGH {{ background: #d29922; }}
    .badge.MEDIUM {{ background: #1f6feb; }}
    .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 20px; }}
    .stat-box {{ background: #21262d; border-radius: 6px; padding: 12px; text-align: center; }}
    .stat-val {{ font-size: 20px; font-weight: 700; color: #f0f6fc; }}
    .stat-lbl {{ font-size: 11px; color: #8b949e; text-transform: uppercase; margin-top: 4px; }}
    .hotspot-table {{ width: 100%; border-collapse: collapse; margin-top: 16px; font-size: 13px; }}
    .hotspot-table th, .hotspot-table td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid #21262d; }}
    .hotspot-table th {{ color: #8b949e; font-weight: 600; background: #1c2128; }}
    .hotspot-table tr:hover {{ background: #1f242c; }}
  </style>
</head>
<body>
  <div class="card" id="{self.component_id}" data-testid="churn-heatmap-widget">
    <div class="header">
      <h2 class="title">{self.title}</h2>
      <span class="badge" data-testid="hotspot-count-badge">{summary.get("hotspot_count", 0)} Hotspots</span>
    </div>
    <div class="stats-grid">
      <div class="stat-box">
        <div class="stat-val" data-testid="stat-files">{summary.get("total_files_analyzed", 0)}</div>
        <div class="stat-lbl">Files Analyzed</div>
      </div>
      <div class="stat-box">
        <div class="stat-val" data-testid="stat-commits">{summary.get("total_commits_evaluated", 0)}</div>
        <div class="stat-lbl">Commits</div>
      </div>
      <div class="stat-box">
        <div class="stat-val" data-testid="stat-churn">{summary.get("total_churn_lines", 0)}</div>
        <div class="stat-lbl">Total Churn (Lines)</div>
      </div>
      <div class="stat-box">
        <div class="stat-val" data-testid="stat-mean-vol">{summary.get("mean_volatility_score", 0.0)}</div>
        <div class="stat-lbl">Mean Volatility</div>
      </div>
    </div>

    <table class="hotspot-table" data-testid="hotspot-table">
      <thead>
        <tr>
          <th>File Path</th>
          <th>Churn Count</th>
          <th>Complexity</th>
          <th>Volatility Score</th>
          <th>Risk Tier</th>
        </tr>
      </thead>
      <tbody id="hotspot-rows">
      </tbody>
    </table>
  </div>

  <script>
    const points = {points_json};
    const tbody = document.getElementById('hotspot-rows');
    points.forEach(p => {{
      const tr = document.createElement('tr');
      tr.setAttribute('data-testid', 'hotspot-row-' + p.risk_tier.toLowerCase());
      tr.innerHTML = `
        <td style="font-family: monospace; color: #58a6ff;">${{p.file_path}}</td>
        <td>${{p.churn_count}}</td>
        <td>${{p.complexity_score}}</td>
        <td>${{p.volatility_score}}</td>
        <td><span class="badge ${{p.risk_tier}}">${{p.risk_tier}}</span></td>
      `;
      tbody.appendChild(tr);
    }});
  </script>
</body>
</html>
"""
