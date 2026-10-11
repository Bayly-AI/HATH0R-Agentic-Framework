"""SQLite-backed Vector & Property Graph Store for Hath0r.

Provides high-performance embedded ACID property graph persistence,
FTS5 full-text keyword indexing, and sub-millisecond vector similarity search.
"""

from __future__ import annotations

import json
import math
import sqlite3
import struct
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple


def _serialize_vector(vector: Sequence[float]) -> bytes:
    """Pack float array into binary float32 buffer."""
    return struct.pack(f"{len(vector)}f", *vector)


def _deserialize_vector(blob: bytes) -> List[float]:
    """Unpack binary float32 buffer into float array."""
    num_floats = len(blob) // 4
    if num_floats == 0:
        return []
    return list(struct.unpack(f"{num_floats}f", blob))


MEMORY_DB = ":memory:"


def _cosine_similarity(vec_a: Sequence[float], vec_b: Sequence[float]) -> float:
    """Compute cosine similarity between two float vectors."""
    if len(vec_a) != len(vec_b) or not vec_a:
        return 0.0
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))
    if norm_a < 1e-9 or norm_b < 1e-9:
        return 0.0
    return float(dot / (norm_a * norm_b))


class SQLiteGraphStore:
    """Embedded SQLite storage backend for KnowledgeGraph and MemoryGraph."""

    def __init__(self, db_path: str | Path = MEMORY_DB) -> None:
        self.db_path = str(db_path)
        if self.db_path != MEMORY_DB:
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._init_schema()

    def _init_schema(self) -> None:
        """Initialize database schema, indexes, and FTS5 virtual tables."""
        with self._conn:
            # Enable WAL mode for file-based DBs
            if self.db_path != MEMORY_DB:
                self._conn.execute("PRAGMA journal_mode=WAL;")
                self._conn.execute("PRAGMA synchronous=NORMAL;")

            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS nodes (
                    id TEXT PRIMARY KEY,
                    graph_type TEXT NOT NULL DEFAULT 'knowledge',
                    type TEXT NOT NULL,
                    title TEXT NOT NULL,
                    path TEXT NOT NULL DEFAULT '',
                    subsystem TEXT NOT NULL DEFAULT 'root',
                    content TEXT NOT NULL DEFAULT '',
                    importance REAL NOT NULL DEFAULT 0.5,
                    tags TEXT NOT NULL DEFAULT '[]',
                    properties TEXT NOT NULL DEFAULT '{}',
                    embedding_blob BLOB,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
            """)

            self._conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_nodes_graph_type ON nodes(graph_type);
            """)
            self._conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_nodes_type ON nodes(type);
            """)

            self._conn.execute("""
                CREATE TABLE IF NOT EXISTS edges (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    graph_type TEXT NOT NULL DEFAULT 'knowledge',
                    source TEXT NOT NULL,
                    target TEXT NOT NULL,
                    relation TEXT NOT NULL,
                    weight REAL NOT NULL DEFAULT 1.0,
                    valid_from TEXT,
                    valid_to TEXT,
                    is_current INTEGER NOT NULL DEFAULT 1,
                    metadata TEXT NOT NULL DEFAULT '{}',
                    FOREIGN KEY(source) REFERENCES nodes(id) ON DELETE CASCADE,
                    FOREIGN KEY(target) REFERENCES nodes(id) ON DELETE CASCADE
                );
            """)

            self._conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_edges_source ON edges(source);
            """)
            self._conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_edges_target ON edges(target);
            """)
            self._conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_edges_relation ON edges(relation);
            """)
            self._conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_edges_is_current ON edges(is_current);
            """)

            # Full Text Search virtual table (FTS5)
            self._conn.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS nodes_fts USING fts5(
                    id UNINDEXED,
                    title,
                    content,
                    tags,
                    tokenize='porter unicode61'
                );
            """)

    def close(self) -> None:
        """Close database connection."""
        self._conn.close()

    def upsert_node(
        self,
        node_id: str,
        node_type: str,
        title: str,
        *,
        graph_type: str = "knowledge",
        path: str = "",
        subsystem: str = "root",
        content: str = "",
        importance: float = 0.5,
        tags: Optional[List[str]] = None,
        properties: Optional[Dict[str, Any]] = None,
        embedding: Optional[Sequence[float]] = None,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
    ) -> None:
        """Insert or update a node and synchronize its FTS index."""
        now = datetime.now(timezone.utc).isoformat()
        c_at = created_at or now
        u_at = updated_at or now
        tags_json = json.dumps(tags or [])
        props_json = json.dumps(properties or {})
        blob = _serialize_vector(embedding) if embedding is not None else None

        with self._conn:
            self._conn.execute(
                """
                INSERT INTO nodes (
                    id, graph_type, type, title, path, subsystem, content,
                    importance, tags, properties, embedding_blob, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    graph_type=excluded.graph_type,
                    type=excluded.type,
                    title=excluded.title,
                    path=excluded.path,
                    subsystem=excluded.subsystem,
                    content=excluded.content,
                    importance=excluded.importance,
                    tags=excluded.tags,
                    properties=excluded.properties,
                    embedding_blob=COALESCE(excluded.embedding_blob, nodes.embedding_blob),
                    updated_at=excluded.updated_at;
                """,
                (
                    node_id,
                    graph_type,
                    node_type,
                    title,
                    path,
                    subsystem,
                    content,
                    importance,
                    tags_json,
                    props_json,
                    blob,
                    c_at,
                    u_at,
                ),
            )

            # Update FTS5 index
            self._conn.execute("DELETE FROM nodes_fts WHERE id = ?", (node_id,))
            self._conn.execute(
                "INSERT INTO nodes_fts (id, title, content, tags) VALUES (?, ?, ?, ?)",
                (node_id, title, content, " ".join(tags or [])),
            )

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve node by ID."""
        cursor = self._conn.execute(
            """
            SELECT id, graph_type, type, title, path, subsystem, content,
                   importance, tags, properties, embedding_blob, created_at, updated_at
            FROM nodes WHERE id = ?
            """,
            (node_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None
        return self._row_to_node_dict(row)

    def delete_node(self, node_id: str) -> bool:
        """Delete node and connected edges."""
        with self._conn:
            res = self._conn.execute("DELETE FROM nodes WHERE id = ?", (node_id,))
            self._conn.execute("DELETE FROM edges WHERE source = ? OR target = ?", (node_id, node_id))
            self._conn.execute("DELETE FROM nodes_fts WHERE id = ?", (node_id,))
            return res.rowcount > 0

    def add_edge(
        self,
        source: str,
        target: str,
        relation: str,
        *,
        graph_type: str = "knowledge",
        weight: float = 1.0,
        valid_from: Optional[str] = None,
        valid_to: Optional[str] = None,
        is_current: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Add a directed relational edge with optional temporal validity bounds."""
        meta_json = json.dumps(metadata or {})
        with self._conn:
            self._conn.execute(
                """
                INSERT INTO edges (graph_type, source, target, relation, weight, valid_from, valid_to, is_current, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (graph_type, source, target, relation, weight, valid_from, valid_to, 1 if is_current else 0, meta_json),
            )

    def get_edges(
        self,
        *,
        source: Optional[str] = None,
        target: Optional[str] = None,
        relation: Optional[str] = None,
        graph_type: Optional[str] = None,
        as_of: Optional[str] = None,
        only_current: bool = False,
    ) -> List[Dict[str, Any]]:
        """Query edges matching given criteria, including temporal interval filtering."""
        clauses = []
        params: List[Any] = []
        if source:
            clauses.append("source = ?")
            params.append(source)
        if target:
            clauses.append("target = ?")
            params.append(target)
        if relation:
            clauses.append("relation = ?")
            params.append(relation)
        if graph_type:
            clauses.append("graph_type = ?")
            params.append(graph_type)
        if only_current:
            clauses.append("is_current = 1")
        if as_of:
            clauses.append("(valid_from IS NULL OR valid_from <= ?)")
            params.append(as_of)
            clauses.append("(valid_to IS NULL OR valid_to >= ?)")
            params.append(as_of)

        where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        cursor = self._conn.execute(
            f"SELECT id, graph_type, source, target, relation, weight, valid_from, valid_to, is_current, metadata FROM edges {where}",
            params,
        )
        edges = []
        for row in cursor.fetchall():
            edges.append(
                {
                    "id": row["id"],
                    "graph_type": row["graph_type"],
                    "source": row["source"],
                    "target": row["target"],
                    "relation": row["relation"],
                    "weight": row["weight"],
                    "valid_from": row["valid_from"],
                    "valid_to": row["valid_to"],
                    "is_current": bool(row["is_current"]),
                    "metadata": json.loads(row["metadata"]),
                }
            )
        return edges

    def count_nodes(self, graph_type: Optional[str] = None) -> int:
        """Return total node count."""
        if graph_type:
            cursor = self._conn.execute("SELECT COUNT(*) FROM nodes WHERE graph_type = ?", (graph_type,))
        else:
            cursor = self._conn.execute("SELECT COUNT(*) FROM nodes")
        return int(cursor.fetchone()[0])

    def count_edges(self, graph_type: Optional[str] = None) -> int:
        """Return total edge count."""
        if graph_type:
            cursor = self._conn.execute("SELECT COUNT(*) FROM edges WHERE graph_type = ?", (graph_type,))
        else:
            cursor = self._conn.execute("SELECT COUNT(*) FROM edges")
        return int(cursor.fetchone()[0])

    def search_fts(self, query: str, limit: int = 10, graph_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Full-text BM25 search over nodes using SQLite FTS5."""
        clean_query = " ".join([w for w in query.replace('"', "").replace("'", "").split() if w])
        if not clean_query:
            return []

        sql = """
            SELECT n.id, n.graph_type, n.type, n.title, n.path, n.subsystem,
                   n.content, n.importance, n.tags, n.properties, n.embedding_blob,
                   n.created_at, n.updated_at, bm25(nodes_fts) AS rank
            FROM nodes_fts f
            JOIN nodes n ON f.id = n.id
            WHERE nodes_fts MATCH ?
        """
        params: List[Any] = [clean_query]
        if graph_type:
            sql += " AND n.graph_type = ?"
            params.append(graph_type)
        sql += " ORDER BY rank LIMIT ?"
        params.append(limit)

        try:
            cursor = self._conn.execute(sql, params)
            results = []
            for row in cursor.fetchall():
                node = self._row_to_node_dict(row)
                node["fts_rank"] = row["rank"]
                results.append(node)
            return results
        except sqlite3.OperationalError:
            # Fallback to LIKE query if FTS syntax is problematic
            return self._fallback_search(query, limit, graph_type)

    def _fallback_search(self, query: str, limit: int = 10, graph_type: Optional[str] = None) -> List[Dict[str, Any]]:
        sql = "SELECT * FROM nodes WHERE (title LIKE ? OR content LIKE ?)"
        params: List[Any] = [f"%{query}%", f"%{query}%"]
        if graph_type:
            sql += " AND graph_type = ?"
            params.append(graph_type)
        sql += " LIMIT ?"
        params.append(limit)
        cursor = self._conn.execute(sql, params)
        return [self._row_to_node_dict(r) for r in cursor.fetchall()]

    def search_vector(
        self,
        query_embedding: Sequence[float],
        top_k: int = 10,
        graph_type: Optional[str] = None,
    ) -> List[Tuple[Dict[str, Any], float]]:
        """Exact/ANN vector cosine similarity retrieval across nodes."""
        if not query_embedding:
            return []

        sql = "SELECT * FROM nodes WHERE embedding_blob IS NOT NULL"
        params: List[Any] = []
        if graph_type:
            sql += " AND graph_type = ?"
            params.append(graph_type)

        cursor = self._conn.execute(sql, params)
        scored: List[Tuple[Dict[str, Any], float]] = []

        for row in cursor.fetchall():
            blob = row["embedding_blob"]
            if not blob:
                continue
            node_vec = _deserialize_vector(blob)
            score = _cosine_similarity(query_embedding, node_vec)
            if score > 0.0:
                node = self._row_to_node_dict(row)
                scored.append((node, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    def search_hybrid(
        self,
        query: str,
        query_embedding: Optional[Sequence[float]] = None,
        *,
        alpha: float = 0.5,
        limit: int = 10,
        graph_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Hybrid search combining full-text FTS5 BM25 and dense vector cosine similarity."""
        fts_results = self.search_fts(query, limit=limit * 2, graph_type=graph_type)
        fts_map = {r["id"]: (1.0 / (1.0 + abs(r.get("fts_rank", 0.0)))) for r in fts_results}

        vec_map: Dict[str, float] = {}
        node_lookup: Dict[str, Dict[str, Any]] = {r["id"]: r for r in fts_results}

        if query_embedding:
            vec_results = self.search_vector(query_embedding, top_k=limit * 2, graph_type=graph_type)
            for node, sim in vec_results:
                nid = node["id"]
                vec_map[nid] = sim
                if nid not in node_lookup:
                    node_lookup[nid] = node

        all_ids = set(fts_map.keys()).union(vec_map.keys())
        scored: List[Tuple[Dict[str, Any], float]] = []

        for nid in all_ids:
            score_fts = fts_map.get(nid, 0.0)
            score_vec = vec_map.get(nid, 0.0)
            hybrid_score = (1.0 - alpha) * score_fts + alpha * score_vec
            node = node_lookup.get(nid)
            if node:
                node_copy = dict(node)
                node_copy["hybrid_score"] = round(hybrid_score, 4)
                node_copy["fts_score"] = round(score_fts, 4)
                node_copy["vec_score"] = round(score_vec, 4)
                scored.append((node_copy, hybrid_score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [item[0] for item in scored[:limit]]

    def _row_to_node_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """Convert a database row into a structured dictionary."""
        blob = row["embedding_blob"]
        emb = _deserialize_vector(blob) if blob else None
        return {
            "id": row["id"],
            "graph_type": row["graph_type"],
            "type": row["type"],
            "title": row["title"],
            "path": row["path"],
            "subsystem": row["subsystem"],
            "content": row["content"],
            "importance": row["importance"],
            "tags": json.loads(row["tags"]),
            "properties": json.loads(row["properties"]),
            "embedding": emb,
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
        }
