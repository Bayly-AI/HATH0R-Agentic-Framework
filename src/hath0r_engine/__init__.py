"""HATH0R Engine — Core Cognitive Substrate & Runtime Safety Engine."""

from __future__ import annotations

__version__ = "1.0.0"

from hath0r_engine.context.context_graph import ContextEdge, ContextGraph, ContextNode
from hath0r_engine.gateway.base import (
    CompletionRequest,
    CompletionResponse,
    ComplexityTier,
    GatewayConfig,
    ModelProvider,
)
from hath0r_engine.gateway.cache import SemanticCache
from hath0r_engine.gateway.client import AIGatewayClient
from hath0r_engine.gateway.routing import TieredRouter
from hath0r_engine.gateway.tokenizer_tax import (
    ScriptBreakdown,
    TaxAuditReport,
    TokenizerTaxAuditor,
    VocabVRAMFootprint,
)
from hath0r_engine.graph.agent_graph import (
    AgentGraphEdge,
    AgentGraphEngine,
    AgentGraphNode,
    AgentGraphPlane,
    AgentGraphValidationReport,
    ResolvedRuleSet,
    RuleConflictError,
    RuleCycleError,
    RulePriority,
)
from hath0r_engine.graph.knowledge_graph import KnowledgeEdge, KnowledgeGraph, KnowledgeGraphExtractor, KnowledgeNode
from hath0r_engine.graph.sqlite_graph import SQLiteGraphStore
from hath0r_engine.guardrails.ast_validator import SyntaxGuardrail
from hath0r_engine.guardrails.escalation import EscalationEvent, HumanEscalationAuditHook
from hath0r_engine.guardrails.manager import GuardrailsManager
from hath0r_engine.guardrails.models import (
    GuardrailAction,
    GuardrailEvaluation,
    ToolCallDescriptor,
)
from hath0r_engine.guardrails.schema_repair import SchemaRepairEngine
from hath0r_engine.jev.jev_client import JevClient, JevSettings, ToolGuardRequest, ToolGuardResult
from hath0r_engine.jev.jev_tool_guard import (
    build_tool_guard_request,
    evaluate_tool_guard,
    format_block_message,
    is_guarded_tool,
)
from hath0r_engine.mcp.identity import CallerIdentity
from hath0r_engine.mcp.schema_pruner import PruningMode, SchemaPruner
from hath0r_engine.mcp.telemetry import MCPRoutingTelemetry, RoutingMetric
from hath0r_engine.mcp.tool_router import DynamicToolRouter, ToolDefinition
from hath0r_engine.memory.memory_graph import MemoryEdge, MemoryGraph, MemoryNode
from hath0r_engine.memory.memory_tools import MemoryPagingManager
from hath0r_engine.memory.reflection import ReflectionEngine
from hath0r_engine.optimization import (
    ArrayType,
    ExperimentMatrix,
    ExperimentRun,
    Factor,
    FactorAnalysis,
    FactorLevelEffect,
    SNRType,
    TaguchiAnalysisResult,
    TaguchiEngine,
    TaguchiLossFunction,
    calculate_snr,
)
from hath0r_engine.orchestration.durable_agent import durable_task
from hath0r_engine.orchestration.hibernation import (
    GateStatus,
    HumanGateRequest,
    WorkflowSuspendedException,
)
from hath0r_engine.orchestration.journal import (
    EventJournal,
    EventRecord,
    EventType,
)
from hath0r_engine.orchestration.state_machine import (
    DurableWorkflowEngine,
    WorkflowStatus,
)
from hath0r_engine.pipeline.assertions import (
    Assert,
    SchemaAssertionError,
    SchemaSuggestionWarning,
    Suggest,
    validate_json_contract,
)
from hath0r_engine.pipeline.module import (
    ChainOfThought,
    PipelineModule,
    Predictor,
)
from hath0r_engine.pipeline.signature import (
    Field,
    InputField,
    OutputField,
    Prediction,
    Signature,
)
from hath0r_engine.pipeline.teleprompter import BootstrapFewShotCompiler
from hath0r_engine.sandbox.base import (
    ExecutionResult,
    NetworkPolicy,
    SandboxConfig,
    SandboxProvider,
    SandboxType,
)
from hath0r_engine.sandbox.daytona_provider import DaytonaSandboxProvider
from hath0r_engine.sandbox.e2b_provider import E2BSandboxProvider
from hath0r_engine.sandbox.local_provider import LocalSandboxProvider
from hath0r_engine.sandbox.manager import SandboxManager
from hath0r_engine.telemetry.otel_tracer import OTELTracerBot, TelemetrySpan
from hath0r_engine.testing.catalog import PlaywrightMasterCatalogManager
from hath0r_engine.testing.models import (
    PlaywrightActionType,
    PlaywrightBrowserType,
    PlaywrightCatalogMetadata,
    PlaywrightExecutionResult,
    PlaywrightMasterCatalog,
    PlaywrightStep,
    PlaywrightTestCase,
    PlaywrightTestStatus,
    PlaywrightTestSuite,
)
from hath0r_engine.testing.runner import PlaywrightTestRunner
from hath0r_engine.ui.components import UIComponentBuilder
from hath0r_engine.ui.crypto_signoff import generate_cryptographic_signature
from hath0r_engine.ui.protocol import (
    EvidenceComponent,
    EvidenceType,
    HandshakeSession,
    HandshakeState,
    SignOffRecord,
)
from hath0r_engine.ui.synchronizer import BiDirectionalStateSync
from hath0r_engine.vision import (
    DesignToCodeSynthesizer,
    DocumentLayoutParser,
    DocumentStructure,
    GroundedTarget,
    ImageMetadata,
    MultimodalPerceptionManager,
    VisionEngine,
    VisionResult,
    VisualGroundingEngine,
)
from hath0r_engine.voice.voice_config import VoiceConfig
from hath0r_engine.voice.voice_engine import VoiceEngine

__all__ = [
    "__version__",
    "AgentGraphEngine",
    "AgentGraphNode",
    "AgentGraphEdge",
    "AgentGraphPlane",
    "RulePriority",
    "ResolvedRuleSet",
    "RuleCycleError",
    "RuleConflictError",
    "AgentGraphValidationReport",
    "KnowledgeGraph",
    "KnowledgeNode",
    "KnowledgeEdge",
    "KnowledgeGraphExtractor",
    "SQLiteGraphStore",
    "ContextGraph",
    "ContextNode",
    "ContextEdge",
    "MemoryGraph",
    "MemoryNode",
    "MemoryEdge",
    "MemoryPagingManager",
    "ReflectionEngine",
    "DynamicToolRouter",
    "ToolDefinition",
    "SchemaPruner",
    "PruningMode",
    "CallerIdentity",
    "MCPRoutingTelemetry",
    "RoutingMetric",
    "SandboxType",
    "NetworkPolicy",
    "SandboxConfig",
    "ExecutionResult",
    "SandboxProvider",
    "E2BSandboxProvider",
    "DaytonaSandboxProvider",
    "LocalSandboxProvider",
    "SandboxManager",
    "EventType",
    "EventRecord",
    "EventJournal",
    "GateStatus",
    "HumanGateRequest",
    "WorkflowSuspendedException",
    "WorkflowStatus",
    "DurableWorkflowEngine",
    "durable_task",
    "Field",
    "InputField",
    "OutputField",
    "Prediction",
    "Signature",
    "SchemaAssertionError",
    "SchemaSuggestionWarning",
    "Assert",
    "Suggest",
    "validate_json_contract",
    "PipelineModule",
    "Predictor",
    "ChainOfThought",
    "BootstrapFewShotCompiler",
    "GuardrailAction",
    "ToolCallDescriptor",
    "GuardrailEvaluation",
    "SyntaxGuardrail",
    "SchemaRepairEngine",
    "EscalationEvent",
    "HumanEscalationAuditHook",
    "GuardrailsManager",
    "ComplexityTier",
    "ModelProvider",
    "GatewayConfig",
    "CompletionRequest",
    "CompletionResponse",
    "SemanticCache",
    "TieredRouter",
    "AIGatewayClient",
    "ScriptBreakdown",
    "VocabVRAMFootprint",
    "TaxAuditReport",
    "TokenizerTaxAuditor",
    "OTELTracerBot",
    "TelemetrySpan",
    "EvidenceType",
    "HandshakeState",
    "EvidenceComponent",
    "SignOffRecord",
    "HandshakeSession",
    "UIComponentBuilder",
    "BiDirectionalStateSync",
    "generate_cryptographic_signature",
    "JevClient",
    "JevSettings",
    "ToolGuardRequest",
    "ToolGuardResult",
    "is_guarded_tool",
    "evaluate_tool_guard",
    "build_tool_guard_request",
    "format_block_message",
    "VoiceEngine",
    "VoiceConfig",
    "VisionEngine",
    "MultimodalPerceptionManager",
    "VisualGroundingEngine",
    "DocumentLayoutParser",
    "DesignToCodeSynthesizer",
    "ImageMetadata",
    "VisionResult",
    "DocumentStructure",
    "GroundedTarget",
    "PlaywrightBrowserType",
    "PlaywrightTestStatus",
    "PlaywrightActionType",
    "PlaywrightStep",
    "PlaywrightTestCase",
    "PlaywrightTestSuite",
    "PlaywrightCatalogMetadata",
    "PlaywrightMasterCatalog",
    "PlaywrightExecutionResult",
    "PlaywrightMasterCatalogManager",
    "PlaywrightTestRunner",
    "ArrayType",
    "Factor",
    "ExperimentRun",
    "ExperimentMatrix",
    "FactorLevelEffect",
    "FactorAnalysis",
    "TaguchiAnalysisResult",
    "TaguchiLossFunction",
    "SNRType",
    "calculate_snr",
    "TaguchiEngine",
]
