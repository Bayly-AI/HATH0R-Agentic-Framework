"""Unit tests for Dynamic MCP Tool Router, Schema Pruner, Identity Context, and Telemetry."""


from hath0r_engine.mcp import (
    CallerIdentity,
    DynamicToolRouter,
    PruningMode,
    SchemaPruner,
)


def test_schema_pruner_modes():
    pruner = SchemaPruner(max_description_len=40)

    raw_tool = {
        "name": "sql_query_executor",
        "description": "Executes read-only SQL queries against the analytical data warehouse cluster.",
        "parameters": {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "required": ["query"],
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The SQL query string to run against analytical database engine.",
                },
                "max_rows": {
                    "type": "integer",
                    "description": "Maximum number of rows to return from the analytical database cursor.",
                    "default": 100,
                },
            },
        },
    }

    # NONE mode
    unpruned = pruner.prune_tool(raw_tool, mode=PruningMode.NONE)
    assert unpruned == raw_tool

    # AGGRESSIVE mode: strips parameter descriptions
    aggressive = pruner.prune_tool(raw_tool, mode=PruningMode.AGGRESSIVE)
    assert "description" not in aggressive["parameters"]["properties"]["query"]
    assert aggressive["parameters"]["properties"]["query"]["type"] == "string"

    # STANDARD mode: truncates long parameter descriptions
    standard = pruner.prune_tool(raw_tool, mode=PruningMode.STANDARD)
    assert len(standard["parameters"]["properties"]["query"]["description"]) <= 45  # 40 + '...'


def test_caller_identity_authorization_and_headers():
    caller = CallerIdentity(
        tenant_id="tenant-acme",
        user_id="user-123",
        session_id="sess-xyz",
        roles=["developer"],
        scopes=["github:read", "database:read"],
        auth_token="jwt.token.here",
    )

    assert caller.has_scope("github:read") is True
    assert caller.has_scope("database:write") is False

    headers = caller.to_headers()
    assert headers["X-Tenant-Id"] == "tenant-acme"
    assert headers["X-User-Id"] == "user-123"
    assert headers["X-Session-Id"] == "sess-xyz"
    assert headers["Authorization"] == "Bearer jwt.token.here"
    assert "github:read" in headers["X-Auth-Scopes"]


def test_dynamic_tool_router_indexing_and_routing():
    router = DynamicToolRouter()

    # Register a fleet of diverse enterprise tools
    router.register_tool(
        server_id="github-mcp",
        name="github_create_issue",
        description="Creates an issue in a GitHub repository with title, markdown body, and labels.",
        parameters={
            "type": "object",
            "properties": {
                "repo": {"type": "string", "description": "Repository path"},
                "title": {"type": "string", "description": "Issue title"},
            },
            "required": ["repo", "title"],
        },
        tags=["git", "issue", "github"],
        required_scopes=["github:write"],
    )

    router.register_tool(
        server_id="github-mcp",
        name="github_list_pull_requests",
        description="Lists open and closed pull requests for a given repository.",
        parameters={
            "type": "object",
            "properties": {
                "repo": {"type": "string", "description": "Repository path"},
            },
            "required": ["repo"],
        },
        tags=["git", "pr", "github"],
        required_scopes=["github:read"],
    )

    router.register_tool(
        server_id="db-mcp",
        name="database_execute_query",
        description="Executes a SQL query against PostgreSQL relational database.",
        parameters={
            "type": "object",
            "properties": {
                "sql": {"type": "string", "description": "SQL statement"},
            },
            "required": ["sql"],
        },
        tags=["sql", "postgres", "database"],
        required_scopes=["database:read"],
    )

    # Search for git pull requests query
    results = router.route_tools("show me open pull requests", top_k=2)
    assert len(results) >= 1
    assert results[0][0].name == "github_list_pull_requests"

    # Search for SQL database query
    sql_results = router.route_tools("run a query on the postgres database", top_k=2)
    assert len(sql_results) >= 1
    assert sql_results[0][0].name == "database_execute_query"


def test_scope_filtered_routing():
    router = DynamicToolRouter()

    router.register_tool(
        server_id="admin-mcp",
        name="delete_production_cluster",
        description="Destroys a Kubernetes production cluster and releases cloud infrastructure.",
        parameters={"type": "object", "properties": {}},
        required_scopes=["cluster:admin"],
    )

    router.register_tool(
        server_id="read-mcp",
        name="get_cluster_status",
        description="Retrieves health metrics and pod status for Kubernetes cluster.",
        parameters={"type": "object", "properties": {}},
        required_scopes=["cluster:read"],
    )

    read_caller = CallerIdentity(scopes=["cluster:read"])
    admin_caller = CallerIdentity(roles=["admin"])

    # Read-only caller should only see status tool, not delete tool
    read_routed = router.route_tools("cluster operations", top_k=5, caller=read_caller)
    names = [t.name for t, _ in read_routed]
    assert "get_cluster_status" in names
    assert "delete_production_cluster" not in names

    # Admin caller sees both
    admin_routed = router.route_tools("cluster operations", top_k=5, caller=admin_caller)
    admin_names = [t.name for t, _ in admin_routed]
    assert "delete_production_cluster" in admin_names


def test_mcp_server_manifest_registration_and_pruned_llm_tools():
    router = DynamicToolRouter()

    manifest = {
        "tools": [
            {
                "name": "voice_synthesizer",
                "description": "Synthesizes real-time streaming audio from markdown text using neural voice engine.",
                "tags": ["synthesizer", "tts", "speech", "synthesize"],
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to synthesize into audio stream"},
                        "voice": {"type": "string", "description": "Voice profile identifier"},
                    },
                    "required": ["text"],
                },
            },
            {
                "name": "voice_transcriber",
                "description": "Transcribes incoming PCM streaming audio buffers into text transcript.",
                "tags": ["transcription", "stt", "transcribe"],
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "audio_bytes": {"type": "string", "description": "Base64 encoded audio chunk"},
                    },
                    "required": ["audio_bytes"],
                },
            },
        ]
    }

    count = router.register_mcp_server_manifest("voice-gateway", manifest)
    assert count == 2

    # Request pruned tools for voice synthesis prompt
    pruned_tools = router.get_pruned_tools_for_llm(
        query="synthesize speech audio for response",
        top_k=1,
        mode=PruningMode.STANDARD,
    )
    assert len(pruned_tools) == 1
    assert pruned_tools[0]["name"] == "voice_synthesizer"

    # Verify telemetry was captured
    summary = router.get_telemetry_summary()
    assert summary["total_queries"] == 1
    assert summary["total_tokens_saved"] > 0
    assert summary["avg_reduction_pct"] > 0.0
