# Hath0r MCP (Model Context Protocol) Tools Catalog

The **Hath0r MCP Server** (`hath0r-mcp`) exposes a standardized tool catalog allowing AI models, coding agents, and orchestrators to query knowledgebases, read documentation, inspect environments, execute runbooks, and control infrastructure over the standard Model Context Protocol (stdio, SSE, and streamable-http).

Endpoint: `http://127.0.0.1:38083` (Docker container: `Hath0r-MCP` on `hath0r-net`)

---

## 📚 1. KnowledgeBase & Semantic Search Tools

### `kb_search`
- **Description**: Search the canonical knowledgebase for relevant documents, architecture records, and rules using semantic vector and hybrid search.
- **Parameters**:
  - `query` (string, required): Search query or question.
  - `index` / `index_name` (string, optional): Specific index to search.
  - `group` (string, optional): Taxonomy top group filter (e.g. `hath0r-opensource`, `bai`).
  - `top_k` / `limit` (integer, optional): Maximum results to return (default: 5).
  - `min_score` (number, optional): Minimum similarity threshold (e.g. 0.7).
  - `full_content` (boolean, optional): Return entire content rather than excerpt preview (default: false).

### `kb_get_document`
- **Description**: Retrieve a complete document from the KnowledgeBase by index and document ID.
- **Parameters**:
  - `id` / `doc_id` (string, required): Unique document identifier.
  - `index` (string, optional): Target index name.

### `kb_index_list`
- **Description**: List all active knowledgebase search indices, document counts, and health status.
- **Parameters**: None.

### `kb_add_document` / `kb_add_file`
- **Description**: Index a new text document or local file into the KnowledgeBase with automated chunking and embeddings.
- **Parameters**:
  - `content` (string) or `file_path` (string, required).
  - `index` (string, optional): Target index.
  - `metadata` (object, optional): Tags, taxonomy, author, and source repo.

### `kb_sync_all`
- **Description**: Synchronize and re-index all canonical knowledgebase markdown files from disk.
- **Parameters**:
  - `force` (boolean, optional): Force re-indexing of unchanged files.

### `kb_health` & `kb_stats`
- **Description**: Check vector database connectivity, embedding model availability, and indexing metrics.

---

## 📖 2. Documentation Corpus Tools

### `docs_kb_list`
- **Description**: List all registered documentation hubs and canonical repositories.
- **Parameters**:
  - `group` (string, optional): Group filter.

### `docs_kb_search`
- **Description**: Execute keyword and BM25 search across all official product documentation.
- **Parameters**:
  - `query` (string, required): Search string.
  - `category` (string, optional): E.g. `governance`, `architecture`, `developers`.

### `docs_read_content`
- **Description**: Read raw or rendered content from a specific documentation path within the corpus.
- **Parameters**:
  - `path` (string, required): Relative path inside canonical documentation.

### `docs_list_dirs`
- **Description**: Explore directory hierarchies of the documentation corpus.

---

## ⚙️ 3. InfraOS & Environment Inspection Tools

### `infraos_context`
- **Description**: Retrieve current active operational context (workspace root, active member, control tower URI, Docker network status).
- **Parameters**: None.

### `infraos_ping` & `infraos_echo`
- **Description**: Low-latency heartbeat and echo probe to verify MCP connectivity.

### `infraos_env_get` & `infraos_env_list`
- **Description**: Safely query declared environment variables and non-sensitive system configuration.

---

## 🏃 4. Runbook Automation & Prompt Synthesis Tools

### `runbook_list`
- **Description**: List all available operational and development runbooks in the repository.
- **Parameters**:
  - `tag` (string, optional): Filter by topic tag (e.g. `deploy`, `init`, `reindex`).

### `runbook_get`
- **Description**: Retrieve the full text and execution steps of a specific runbook.
- **Parameters**:
  - `name` / `id` (string, required): Runbook name.

### `runbook_get_prompt`
- **Description**: Synthesize a formatted prompt containing the runbook instructions, context variables, and acceptance gates tailored for an autonomous agent.
- **Parameters**:
  - `runbook_name` (string, required): Name of the runbook to generate a prompt for.
  - `variables` (object, optional): Dynamic parameter substitutions.

### `runbook_log_create`
- **Description**: Record an execution audit entry documenting an agent's runbook execution result.

---

## 🔍 5. Advanced Search & RAG Configuration Tools

- `kb_search_config_get` / `kb_search_config_set`: Inspect or adjust hybrid search alpha weights (dense vector vs sparse BM25).
- `kb_rag_config_get` / `kb_rag_config_set`: Configure RAG chunk size, overlap window, and reranking models.
- `kb_taxonomy_list`: Retrieve hierarchical taxonomy classification tree.
- `kb_status_full`: Complete system diagnostic reporting on storage, embeddings, and API endpoints.
