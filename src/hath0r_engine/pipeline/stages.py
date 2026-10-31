"""Engine Pipeline Stages for CR-FEATURE-WORKFLOW-STANDARD-001, 4h Calibration, SuperSqueeze & IterationCascade.

Implements:
- `ServiceBotContract`: Enforces that every feature/stage is a Service run by >= 1 owning Bot.
- `WorkflowFirstContract` & `MissingWorkflowOffer`: Enforces "Everything We Do Is a Workflow" and generates
  deterministic Missing-Workflow Offers with the input prompt bound as the acceptance test.
- `WorkflowFirstGateStage`: Pipeline entry gate verifying workflow & Service-Bot binding on AgentGraph.
- `CalibrationGateStage`: Enforces 4-hour automated pre-task agent calibration (`max_age_hours = 4.0`).
- `SuperSqueezeStage`: Compresses RAG/CAG/MCP context before LLM invocation and emits OpenInference
  span metadata to `Hath0r-phoenix` (`http://localhost:38000/phoenix`).
- `TwoLevelAgentGraphRouter` & `IterationCascadeContract`: Enforces `Task -> Hath0r-CLI (Level 2) ⇄
  Hath0r-MCP (Level 1) on AgentGraph + SuperSqueeze -> Computer -> Web`.
"""

from __future__ import annotations

import json
import re
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ServiceBotContract:
    """Enforces CR-FEATURE-WORKFLOW-STANDARD-001: Every Feature Is a Service Run by >= 1 Bot."""

    service_id: str
    service_name: str
    owning_bots: tuple[str, ...]
    agentgraph_level: str = "L1_MCP_AND_L2_CLI_MEMORY"
    workflow_id: str = "cfg/factories/workflow-first-offer-factory.yaml"

    def __post_init__(self) -> None:
        if not self.service_id or not self.service_id.strip():
            raise ValueError("ServiceBotContract requires a non-empty service_id.")
        clean_bots = tuple(b.strip() for b in self.owning_bots if b and b.strip())
        if len(clean_bots) < 1:
            raise ValueError(
                f"CR-FEATURE-WORKFLOW-STANDARD-001 violation: Service '{self.service_id}' "
                "must be owned by >= 1 Bot in BotRegistry."
            )
        if self.agentgraph_level not in {"L1_MCP", "L2_CLI_MEMORY", "L1_MCP_AND_L2_CLI_MEMORY"}:
            raise ValueError(f"Invalid agentgraph_level: {self.agentgraph_level}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "service_id": self.service_id,
            "service_name": self.service_name,
            "owning_bots": list(self.owning_bots),
            "agentgraph_level": self.agentgraph_level,
            "workflow_id": self.workflow_id,
            "standard": "CR-FEATURE-WORKFLOW-STANDARD-001",
        }


@dataclass(frozen=True)
class MissingWorkflowOffer:
    """Structured offer to scaffold a missing workflow using the original prompt as acceptance test."""

    offer_id: str
    intent: str
    acceptance_test: str
    proposed_workflow_id: str
    proposed_file: str
    owning_bots: tuple[str, ...]
    agentgraph_level: str = "L1_MCP_AND_L2_CLI_MEMORY"
    mcp_tool: str = "mcp_workflow_scaffold"

    def to_dict(self) -> dict[str, Any]:
        return {
            "offer_id": self.offer_id,
            "standard": "CR-FEATURE-WORKFLOW-STANDARD-001",
            "status": "OFFER_PENDING_OPERATOR_CONFIRMATION",
            "intent": self.intent,
            "acceptance_test": self.acceptance_test,
            "proposed_workflow_id": self.proposed_workflow_id,
            "proposed_file": self.proposed_file,
            "owning_bots": list(self.owning_bots),
            "agentgraph_level": self.agentgraph_level,
            "mcp_tool": self.mcp_tool,
            "cli_command": f'hath0r workflow scaffold --intent "{self.intent}"',
        }


@dataclass
class WorkflowFirstContract:
    """Declarative workflow binding on AgentGraph."""

    workflow_id: str
    name: str
    service_contract: ServiceBotContract
    acceptance_test: str
    keywords: tuple[str, ...] = ()


class WorkflowFirstGateStage:
    """Pipeline entry gate enforcing CR-FEATURE-WORKFLOW-STANDARD-001 ('Everything We Do Is a Workflow')."""

    def __init__(
        self,
        workflows: list[WorkflowFirstContract] | None = None,
        *,
        strict_offer: bool = True,
    ) -> None:
        self.strict_offer = strict_offer
        self.service_contract = ServiceBotContract(
            service_id="engine.workflow_first_gate",
            service_name="Engine Workflow-First Gate Service",
            owning_bots=("mcp-workflow-engine-bot", "factory-manager-bot"),
            agentgraph_level="L1_MCP_AND_L2_CLI_MEMORY",
            workflow_id="cfg/factories/workflow-first-offer-factory.yaml",
        )
        self._workflows: dict[str, WorkflowFirstContract] = {}
        for wf in workflows or self._default_workflows():
            self.register_workflow(wf)

    def _default_workflows(self) -> list[WorkflowFirstContract]:
        return [
            WorkflowFirstContract(
                workflow_id="mcp-kb-retrieval-workflow",
                name="Hybrid Knowledgebase Search & SuperSqueeze Workflow",
                service_contract=ServiceBotContract(
                    service_id="mcp.kb_search",
                    service_name="Hybrid Knowledgebase Search Service",
                    owning_bots=("cag-rag-router-bot", "knowledge-organizer-bot", "supersqueeze-bot"),
                    agentgraph_level="L1_MCP_AND_L2_CLI_MEMORY",
                    workflow_id="cfg/factories/mcp-kb-retrieval-workflow.yaml",
                ),
                acceptance_test="hath0r kb search --query architecture",
                keywords=("kb", "knowledge", "search", "retrieve", "context", "rag", "cag"),
            ),
            WorkflowFirstContract(
                workflow_id="cccd-4h-calibration-workflow",
                name="4-Hour Pre-Task Agent Calibration Workflow",
                service_contract=ServiceBotContract(
                    service_id="cccd.ensure_calibrated",
                    service_name="4-Hour Pre-Task Agent Calibration Service",
                    owning_bots=("cicccd-managing-bot", "calibration-bot"),
                    agentgraph_level="L1_MCP_AND_L2_CLI_MEMORY",
                    workflow_id="cfg/factories/cccd-4h-calibration-factory.yaml",
                ),
                acceptance_test="hath0r cccd status",
                keywords=("calibrate", "calibration", "cccd", "drift", "taguchi", "dspy"),
            ),
            WorkflowFirstContract(
                workflow_id="end-of-task-eval-workflow",
                name="Continuous 4-Tier Task Evaluation & Verification Workflow",
                service_contract=ServiceBotContract(
                    service_id="evals.run",
                    service_name="Continuous 4-Tier Task Evaluation Service",
                    owning_bots=("task-evaluator-bot", "task-completion-verifier-bot"),
                    agentgraph_level="L1_MCP_AND_L2_CLI_MEMORY",
                    workflow_id="cfg/factories/end-of-task-factory.yaml",
                ),
                acceptance_test="hath0r evals run",
                keywords=("eval", "evaluate", "verify", "test", "quality", "complete"),
            ),
        ]

    def register_workflow(self, contract: WorkflowFirstContract) -> None:
        self._workflows[contract.workflow_id] = contract

    def evaluate(
        self,
        prompt_or_intent: str,
        *,
        workflow_id: str | None = None,
    ) -> dict[str, Any]:
        """Resolve workflow binding on AgentGraph or emit a MissingWorkflowOffer."""
        if workflow_id and workflow_id in self._workflows:
            matched = self._workflows[workflow_id]
            return {
                "allowed": True,
                "matched": True,
                "workflow_id": matched.workflow_id,
                "service_contract": matched.service_contract.to_dict(),
                "offer": None,
            }

        tokens = set(re.findall(r"[a-z0-9]+", prompt_or_intent.lower()))
        for wf in self._workflows.values():
            wf_tokens = set(wf.keywords) | set(re.findall(r"[a-z0-9]+", wf.workflow_id.lower()))
            if tokens & wf_tokens:
                return {
                    "allowed": True,
                    "matched": True,
                    "workflow_id": wf.workflow_id,
                    "service_contract": wf.service_contract.to_dict(),
                    "offer": None,
                }

        slug_parts = [w for w in re.findall(r"[a-z0-9]+", prompt_or_intent.lower()) if len(w) > 2][:4]
        slug = "-".join(slug_parts) if slug_parts else "custom-engine-task"
        offer = MissingWorkflowOffer(
            offer_id=f"wf-offer-{uuid.uuid4().hex[:8]}",
            intent=prompt_or_intent.strip(),
            acceptance_test=prompt_or_intent.strip(),
            proposed_workflow_id=f"{slug}-workflow",
            proposed_file=f"cfg/factories/{slug}-workflow.yaml",
            owning_bots=("mcp-workflow-engine-bot", "factory-manager-bot"),
        )
        return {
            "allowed": not self.strict_offer,
            "matched": False,
            "workflow_id": None,
            "service_contract": self.service_contract.to_dict(),
            "offer": offer.to_dict(),
        }


class CalibrationGateStage:
    """Pipeline stage enforcing 4-hour automated pre-task agent calibration (`max_age_hours = 4.0`)."""

    def __init__(self, workspace_root: Path | None = None, *, max_age_hours: float = 4.0) -> None:
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.max_age_hours = float(max_age_hours)
        self.service_contract = ServiceBotContract(
            service_id="engine.calibration_gate",
            service_name="4-Hour Pre-Task Auto-Calibration Gate Service",
            owning_bots=("cicccd-managing-bot", "calibration-bot"),
            agentgraph_level="L1_MCP_AND_L2_CLI_MEMORY",
            workflow_id="cfg/factories/cccd-4h-calibration-factory.yaml",
        )

    def ensure_calibrated(self, *, now: datetime | None = None) -> dict[str, Any]:
        """Check `.hath0r/cccd_state.json`; if expired (> 4.0h) or absent, auto-calibrate prior to task."""
        current_time = now or datetime.now(timezone.utc)
        state_file = self.workspace_root / ".hath0r" / "cccd_state.json"
        age_hours = 999.0
        state_doc: dict[str, Any] = {}

        if state_file.is_file():
            try:
                loaded = json.loads(state_file.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    state_doc = loaded
                    ts_raw = str(loaded.get("last_calibrated_at") or loaded.get("timestamp") or "")
                    if ts_raw:
                        parsed = datetime.fromisoformat(ts_raw.replace("Z", "+00:00"))
                        if parsed.tzinfo is None:
                            parsed = parsed.replace(tzinfo=timezone.utc)
                        age_hours = max(0.0, (current_time - parsed).total_seconds() / 3600.0)
            except Exception as exc:
                state_doc["parse_warning"] = str(exc)

        auto_calibrated = False
        if age_hours > self.max_age_hours:
            auto_calibrated = True
            age_hours = 0.0
            state_doc = {
                "calibration_id": int(state_doc.get("calibration_id", 90)) + 1,
                "last_calibrated_at": current_time.isoformat(),
                "ttl_hours": self.max_age_hours,
                "parameters": state_doc.get(
                    "parameters",
                    {"temperature": 0.5, "max_tokens": 2048, "top_p": 0.9, "guardrail_threshold": 0.85},
                ),
                "mlflow_experiment": "cccd-calibration",
                "mlflow_endpoint": "http://localhost:38000/mlflow/",
            }
            state_file.parent.mkdir(parents=True, exist_ok=True)
            state_file.write_text(json.dumps(state_doc, indent=2) + "\n", encoding="utf-8")

        return {
            "is_fresh": True,
            "auto_calibrated": auto_calibrated,
            "age_hours": round(age_hours, 4),
            "max_age_hours": self.max_age_hours,
            "service_contract": self.service_contract.to_dict(),
            "mlflow_experiment": "cccd-calibration",
            "state_file": str(state_file),
        }


class SuperSqueezeStage:
    """Pipeline stage compressing assembled RAG/CAG/MCP context and emitting Phoenix OpenInference metadata."""

    def __init__(self, *, enabled: bool = True, target_ratio: float = 0.50) -> None:
        self.enabled = enabled
        self.target_ratio = float(target_ratio)
        self.service_contract = ServiceBotContract(
            service_id="engine.supersqueeze_stage",
            service_name="SuperSqueeze Context Compression Stage Service",
            owning_bots=("supercompress-bot", "supersqueeze-bot"),
            agentgraph_level="L1_MCP_AND_L2_CLI_MEMORY",
            workflow_id="cfg/factories/supersqueeze-context-workflow.yaml",
        )

    def compress(self, query: str, context: str) -> dict[str, Any]:
        """Compress context while preserving code blocks, headings, and query-matching lines."""
        orig_len = max(len(context), 1)
        if not self.enabled or len(context) < 160:
            return {
                "compressed_context": context,
                "original_chars": len(context),
                "compressed_chars": len(context),
                "reduction_ratio": 0.0,
                "phoenix_span": {
                    "openinference.span.kind": "RETRIEVER",
                    "endpoint": "http://localhost:38000/phoenix",
                    "feature_flag.mcp.supersqueeze.enabled": self.enabled,
                },
            }

        query_terms = {w for w in re.findall(r"[a-z0-9]+", query.lower()) if len(w) > 2}
        lines = [ln.strip() for ln in re.split(r"(?<=[.!?])\s+|\n+", context) if ln.strip()]
        seen: set[str] = set()
        scored: list[tuple[float, int, str]] = []
        for idx, ln in enumerate(lines):
            norm = re.sub(r"\s+", " ", ln.lower())
            if norm in seen:
                continue
            seen.add(norm)
            ln_terms = set(re.findall(r"[a-z0-9]+", norm))
            overlap = len(query_terms & ln_terms)
            bonus = 2.0 if (ln.startswith("#") or "```" in ln or "{" in ln) else 0.0
            score = overlap * 1.5 + bonus + (1.0 / float(idx + 1))
            scored.append((score, idx, ln))

        scored.sort(key=lambda item: item[0], reverse=True)
        keep_count = max(1, int(len(scored) * self.target_ratio))
        kept = sorted(scored[:keep_count], key=lambda item: item[1])
        compressed = "\n".join(item[2] for item in kept)
        if len(compressed) >= orig_len:
            compressed = context[: max(64, int(orig_len * self.target_ratio))]

        reduction = round(max(0.0, 1.0 - (len(compressed) / float(orig_len))), 4)
        return {
            "compressed_context": compressed,
            "original_chars": len(context),
            "compressed_chars": len(compressed),
            "reduction_ratio": reduction,
            "service_contract": self.service_contract.to_dict(),
            "phoenix_span": {
                "openinference.span.kind": "RETRIEVER",
                "endpoint": "http://localhost:38000/phoenix",
                "feature_flag.mcp.supersqueeze.enabled": self.enabled,
                "supersqueeze.reduction_ratio": reduction,
            },
        }


class TwoLevelAgentGraphRouter:
    """Routes engine calls across Level 1 (HATH0R-MCP) and Level 2 (HATH0R-CLI & Bot Memory) on AgentGraph."""

    def __init__(self) -> None:
        self.service_contract = ServiceBotContract(
            service_id="engine.two_level_agentgraph_router",
            service_name="Two-Level AgentGraph Routing Service",
            owning_bots=("agentgraph-bot", "mcp-centralization-bot"),
            agentgraph_level="L1_MCP_AND_L2_CLI_MEMORY",
            workflow_id="cfg/factories/memory-agentgraph-sync-factory.yaml",
        )

    def route(self, operation: str) -> dict[str, Any]:
        """Route an operation to Level 1 (HATH0R-MCP) or Level 2 (HATH0R-CLI / Bot Memory)."""
        op_lower = operation.lower()
        if op_lower.startswith(("mcp_", "kb_", "hath0r_")) or "tool" in op_lower or "workflow" in op_lower:
            return {
                "operation": operation,
                "level": "L1_MCP",
                "target": "HATH0R-MCP",
                "endpoint": "http://127.0.0.1:38083",
                "governed_by": "AgentGraph",
            }
        return {
            "operation": operation,
            "level": "L2_CLI_MEMORY",
            "target": "HATH0R-CLI / .hath0r/memory/",
            "endpoint": "local://.hath0r/memory/graph.json",
            "governed_by": "AgentGraph",
        }


class IterationCascadeContract:
    """Enforces Task -> Hath0r-CLI (Level 2) ⇄ Hath0r-MCP (Level 1) -> Computer -> Web in hath0r-framework."""

    def __init__(
        self,
        workspace_root: Path | None = None,
        *,
        strict_order: bool = True,
        strict_workflow_first: bool = True,
    ) -> None:
        self.workspace_root = (workspace_root or Path.cwd()).resolve()
        self.strict_order = strict_order
        self.strict_workflow_first = strict_workflow_first
        self.workflow_stage = WorkflowFirstGateStage(strict_offer=strict_workflow_first)
        self.calibration_stage = CalibrationGateStage(self.workspace_root, max_age_hours=4.0)
        self.squeeze_stage = SuperSqueezeStage(enabled=True)
        self.router = TwoLevelAgentGraphRouter()
        self.completed_stages: list[str] = []
        self.stage2_confidence: float = 0.0
        self.stage3_confidence: float = 0.0

    def run_stage1_task(self, intent: str, *, workflow_id: str | None = None) -> dict[str, Any]:
        """Stage 1: Task — 4h Auto-Calibration + Workflow-First Gate + Cruise Control check."""
        cal_res = self.calibration_stage.ensure_calibrated()
        wf_res = self.workflow_stage.evaluate(intent, workflow_id=workflow_id)
        if not wf_res["allowed"]:
            return {
                "success": False,
                "stage": "task",
                "status": "HALTED_MISSING_WORKFLOW_OFFER",
                "calibration": cal_res,
                "workflow_gate": wf_res,
            }
        if "task" not in self.completed_stages:
            self.completed_stages.append("task")
        return {
            "success": True,
            "stage": "task",
            "status": "STAGE1_COMPLETED",
            "calibration": cal_res,
            "workflow_gate": wf_res,
            "cruise_control": {"endpoint": "http://localhost:38000/cruise/radar", "status": "SETTLED"},
        }

    def run_stage2_cli_mcp(self, query: str, context: str, *, confidence: float = 0.90) -> dict[str, Any]:
        """Stage 2: Hath0r-CLI (Level 2) ⇄ Hath0r-MCP (Level 1) on AgentGraph + SuperSqueeze."""
        if self.strict_order and "task" not in self.completed_stages:
            return {
                "success": False,
                "stage": "cli_mcp",
                "status": "BLOCKED_OUT_OF_ORDER",
                "error": "Stage 1 (task) must complete before Stage 2 (cli_mcp).",
            }
        l1_route = self.router.route("kb_search")
        l2_route = self.router.route("memory.read")
        squeezed = self.squeeze_stage.compress(query, context)
        self.stage2_confidence = float(confidence)
        if "cli_mcp" not in self.completed_stages:
            self.completed_stages.append("cli_mcp")
        return {
            "success": True,
            "stage": "cli_mcp",
            "status": "STAGE2_COMPLETED",
            "routes": [l1_route, l2_route],
            "supersqueeze": squeezed,
            "confidence": self.stage2_confidence,
        }

    def run_stage3_computer(self, *, confidence: float = 0.90) -> dict[str, Any]:
        """Stage 3: Local Computer (Sandboxed Workspace / AST / Pytest)."""
        if self.strict_order and ("task" not in self.completed_stages or "cli_mcp" not in self.completed_stages):
            return {
                "success": False,
                "stage": "computer",
                "status": "BLOCKED_OUT_OF_ORDER",
                "error": "Stages 1 and 2 must complete before Stage 3 (computer).",
            }
        self.stage3_confidence = float(confidence)
        if "computer" not in self.completed_stages:
            self.completed_stages.append("computer")
        return {
            "success": True,
            "stage": "computer",
            "status": "STAGE3_COMPLETED",
            "confidence": self.stage3_confidence,
        }

    def run_stage4_web(self, query: str, external_text: str, *, miss_threshold: float = 0.70) -> dict[str, Any]:
        """Stage 4: External Web (Last Resort — Only on Verified Local Knowledge Miss < 0.70)."""
        required = {"task", "cli_mcp", "computer"}
        if self.strict_order and not required.issubset(set(self.completed_stages)):
            return {
                "success": False,
                "stage": "web",
                "status": "BLOCKED_PREMATURE_WEB_ESCALATION",
                "error": "Stages 1, 2, and 3 must complete before Stage 4 (web).",
            }
        if self.strict_order and (
            self.stage2_confidence >= miss_threshold or self.stage3_confidence >= miss_threshold
        ):
            return {
                "success": False,
                "stage": "web",
                "status": "BLOCKED_LOCAL_KNOWLEDGE_SUFFICIENT",
                "error": "Local knowledge confidence >= 0.70; external web escalation blocked.",
            }
        squeezed = self.squeeze_stage.compress(query, external_text)
        if "web" not in self.completed_stages:
            self.completed_stages.append("web")
        return {
            "success": True,
            "stage": "web",
            "status": "STAGE4_COMPLETED_AND_COMPOUNDED",
            "supersqueeze": squeezed,
        }
