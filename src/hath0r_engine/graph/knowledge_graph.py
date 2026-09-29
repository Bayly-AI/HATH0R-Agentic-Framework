"""Hath0r KnowledgeGraph Engine with Hybrid BM25 + Vector Embedding Search.

Extracts structured relational entity nodes and edges from Markdown files with YAML frontmatter,
and provides fast relational lineage traversal and hybrid semantic/lexical search.
"""

from __future__ import annotations

import datetime
import math
import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class KnowledgeNode:
    """An entity node in the KnowledgeGraph."""

    id: str
    type: str  # document | contract | procedure | strategy | playbook | runbook | checklist | policy | tool | bot | subsystem
    title: str
    path: str
    subsystem: str = "root"
    content: str = ""
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KnowledgeEdge:
    """A directed relational edge in the KnowledgeGraph."""

    source: str
    target: str
    relation: str  # depends_on | implements | references | governed_by | validates | contains | routes_to | invokes
    weight: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


class BM25Index:
    """Zero-dependency Okapi BM25 keyword index."""

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b
        self.doc_ids: List[str] = []
        self.doc_lengths: List[int] = []
        self.avg_doc_len: float = 0.0
        self.doc_term_freqs: List[Counter[str]] = []
        self.doc_freqs: Counter[str] = Counter()
        self.num_docs: int = 0

    @staticmethod
    def tokenize(text: str) -> List[str]:
        return [w.lower() for w in re.findall(r"\b[a-zA-Z0-9_\-\.]{2,}\b", text)]

    def index_documents(self, docs: Dict[str, str]) -> None:
        self.doc_ids = list(docs.keys())
        self.num_docs = len(self.doc_ids)
        if self.num_docs == 0:
            return

        self.doc_lengths = []
        self.doc_term_freqs = []
        self.doc_freqs = Counter()

        total_length = 0
        for doc_id in self.doc_ids:
            tokens = self.tokenize(docs[doc_id])
            doc_len = len(tokens)
            self.doc_lengths.append(doc_len)
            total_length += doc_len

            term_counts = Counter(tokens)
            self.doc_term_freqs.append(term_counts)

            for term in term_counts:
                self.doc_freqs[term] += 1

        self.avg_doc_len = total_length / self.num_docs if self.num_docs > 0 else 0.0

    def score(self, query: str) -> Dict[str, float]:
        query_tokens = self.tokenize(query)
        if not query_tokens or self.num_docs == 0:
            return {doc_id: 0.0 for doc_id in self.doc_ids}

        scores: Dict[str, float] = {doc_id: 0.0 for doc_id in self.doc_ids}

        for token in query_tokens:
            df = self.doc_freqs.get(token, 0)
            if df == 0:
                continue

            # Standard Robertson-Spärck Jones IDF
            idf = math.log(((self.num_docs - df + 0.5) / (df + 0.5)) + 1.0)

            for idx, doc_id in enumerate(self.doc_ids):
                tf = self.doc_term_freqs[idx].get(token, 0)
                if tf == 0:
                    continue

                doc_len = self.doc_lengths[idx]
                numerator = tf * (self.k1 + 1.0)
                denominator = tf + self.k1 * (1.0 - self.b + self.b * (doc_len / (self.avg_doc_len or 1.0)))
                scores[doc_id] += idf * (numerator / denominator)

        # Normalize BM25 scores to [0.0, 1.0]
        max_score = max(scores.values()) if scores else 0.0
        if max_score > 0.0:
            for doc_id in scores:
                scores[doc_id] /= max_score

        return scores


class LightweightVectorIndex:
    """Dense vector embedding index with zero external dependencies (hash/ngram projection fallback)."""

    def __init__(self, dim: int = 128) -> None:
        self.dim = dim
        self.doc_ids: List[str] = []
        self.vectors: Dict[str, List[float]] = {}

    def _embed_text(self, text: str) -> List[float]:
        tokens = BM25Index.tokenize(text)
        vec = [0.0] * self.dim
        if not tokens:
            return vec

        for token in tokens:
            # Word hash bucket
            h = hash(token) % self.dim
            vec[h] += 1.0

            # Subword character trigrams
            if len(token) >= 3:
                for i in range(len(token) - 2):
                    trigram = token[i : i + 3]
                    th = hash(trigram) % self.dim
                    vec[th] += 0.5

        # L2 normalize
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0.0:
            vec = [x / norm for x in vec]
        return vec

    def index_documents(self, docs: Dict[str, str]) -> None:
        self.doc_ids = list(docs.keys())
        self.vectors = {doc_id: self._embed_text(content) for doc_id, content in docs.items()}

    def score(self, query: str) -> Dict[str, float]:
        q_vec = self._embed_text(query)
        scores: Dict[str, float] = {}

        for doc_id, d_vec in self.vectors.items():
            # Cosine similarity
            dot = sum(q * d for q, d in zip(q_vec, d_vec))
            scores[doc_id] = max(0.0, min(1.0, dot))

        return scores


class KnowledgeGraph:
    """In-memory KnowledgeGraph representation, query interface, and hybrid search engine."""

    def __init__(self, schema_version: str = "hath0r.knowledgegraph/1") -> None:
        self.schema_version = schema_version
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.edges: List[KnowledgeEdge] = []
        self._adjacency: Dict[str, List[KnowledgeEdge]] = {}
        self._bm25_index: Optional[BM25Index] = None
        self._vector_index: Optional[LightweightVectorIndex] = None

    def add_node(self, node: KnowledgeNode) -> None:
        """Add or update an entity node."""
        self.nodes[node.id] = node
        if node.id not in self._adjacency:
            self._adjacency[node.id] = []
        self._bm25_index = None  # invalidate search cache

    def add_edge(self, edge: KnowledgeEdge) -> None:
        """Add a directed edge between nodes."""
        self.edges.append(edge)
        if edge.source not in self._adjacency:
            self._adjacency[edge.source] = []
        self._adjacency[edge.source].append(edge)

    def get_neighbors(self, node_id: str, relation: Optional[str] = None) -> List[KnowledgeNode]:
        """Find neighboring nodes for a given entity."""
        neighbors = []
        for edge in self._adjacency.get(node_id, []):
            if relation is None or edge.relation == relation:
                if edge.target in self.nodes:
                    neighbors.append(self.nodes[edge.target])
        return neighbors

    def get_lineage(self, node_id: str, max_depth: int = 3) -> Dict[str, Any]:
        """Traverse upstream/downstream lineage tree for a given entity."""
        visited: Set[str] = set()
        tree: Dict[str, Any] = {"id": node_id, "children": []}

        def _traverse(current_id: str, current_tree: Dict[str, Any], depth: int) -> None:
            if depth >= max_depth or current_id in visited:
                return
            visited.add(current_id)
            for edge in self._adjacency.get(current_id, []):
                child_node = self.nodes.get(edge.target)
                child_repr = {
                    "id": edge.target,
                    "relation": edge.relation,
                    "title": child_node.title if child_node else edge.target,
                    "type": child_node.type if child_node else "unknown",
                    "children": [],
                }
                current_tree["children"].append(child_repr)
                _traverse(edge.target, child_repr, depth + 1)

        _traverse(node_id, tree, 0)
        return tree

    def _build_search_index(self) -> None:
        """Build BM25 and Vector search indexes across all node corpus content."""
        docs: Dict[str, str] = {}
        for nid, node in self.nodes.items():
            props_text = " ".join(f"{k}: {v}" for k, v in node.properties.items())
            full_text = f"{node.title}\n{node.subsystem}\n{node.type}\n{props_text}\n{node.content}"
            docs[nid] = full_text

        self._bm25_index = BM25Index()
        self._bm25_index.index_documents(docs)

        self._vector_index = LightweightVectorIndex()
        self._vector_index.index_documents(docs)

    def search(
        self,
        query: str,
        top_k: int = 5,
        alpha: float = 0.5,
        subsystem: Optional[str] = None,
        node_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Hybrid search returning ranked, context-relevant documentation and rule nodes.

        Args:
            query: Natural language or keyword query string.
            top_k: Maximum number of ranked results to return.
            alpha: Hybrid weight (1.0 = pure BM25 keyword, 0.0 = pure dense vector, 0.5 = balanced).
            subsystem: Optional subsystem filter.
            node_type: Optional node type filter.

        Returns:
            List of result dictionaries containing node info, relevance scores, and matched snippet.
        """
        if not self._bm25_index or not self._vector_index:
            self._build_search_index()

        assert self._bm25_index is not None
        assert self._vector_index is not None

        bm25_scores = self._bm25_index.score(query)
        vec_scores = self._vector_index.score(query)

        candidates: List[Tuple[float, float, float, KnowledgeNode]] = []

        for nid, node in self.nodes.items():
            if subsystem and node.subsystem.lower() != subsystem.lower():
                continue
            if node_type and node.type.lower() != node_type.lower():
                continue

            b_score = bm25_scores.get(nid, 0.0)
            v_score = vec_scores.get(nid, 0.0)
            hybrid_score = (alpha * b_score) + ((1.0 - alpha) * v_score)

            if hybrid_score > 0.001:
                candidates.append((hybrid_score, b_score, v_score, node))

        # Sort descending by hybrid score
        candidates.sort(key=lambda x: x[0], reverse=True)

        results: List[Dict[str, Any]] = []
        for h_score, b_score, v_score, node in candidates[:top_k]:
            snippet = self._extract_snippet(node.content or node.title, query)
            results.append(
                {
                    "id": node.id,
                    "title": node.title,
                    "type": node.type,
                    "subsystem": node.subsystem,
                    "path": node.path,
                    "hybrid_score": round(h_score, 4),
                    "bm25_score": round(b_score, 4),
                    "vector_score": round(v_score, 4),
                    "snippet": snippet,
                }
            )

        return results

    @staticmethod
    def _extract_snippet(content: str, query: str, max_chars: int = 180) -> str:
        """Extract a representative text snippet matching query keywords."""
        if not content:
            return ""
        tokens = BM25Index.tokenize(query)
        lines = [line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")]
        if not lines:
            return content[:max_chars].strip()

        best_line = lines[0]
        max_matches = -1

        for line in lines:
            line_lower = line.lower()
            matches = sum(1 for t in tokens if t in line_lower)
            if matches > max_matches:
                max_matches = matches
                best_line = line

        if len(best_line) > max_chars:
            return best_line[:max_chars].rstrip() + "..."
        return best_line

    def to_dict(self) -> Dict[str, Any]:
        """Export graph snapshot conforming to hath0r-knowledgegraph-v1 schema."""
        return {
            "schema_version": self.schema_version,
            "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "nodes": [asdict(n) for n in self.nodes.values()],
            "edges": [asdict(e) for e in self.edges],
        }

    def save_to_file(self, file_path: Path | str) -> None:
        """Persist KnowledgeGraph snapshot to a JSON file."""
        import json
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    @classmethod
    def load_from_file(cls, file_path: Path | str) -> KnowledgeGraph:
        """Load KnowledgeGraph from a JSON snapshot file."""
        import json
        path = Path(file_path)
        data = json.loads(path.read_text(encoding="utf-8"))
        kg = cls(schema_version=data.get("schema_version", "hath0r.knowledgegraph/1"))
        for n_dict in data.get("nodes", []):
            kg.add_node(KnowledgeNode(**n_dict))
        for e_dict in data.get("edges", []):
            kg.add_edge(KnowledgeEdge(**e_dict))
        return kg


class KnowledgeGraphExtractor:
    """Parses repository directories and Markdown frontmatter to build KnowledgeGraph."""

    @staticmethod
    def parse_frontmatter(content: str) -> Dict[str, Any]:
        """Simple, zero-dependency YAML frontmatter parser."""
        if not content.startswith("---"):
            return {}
        parts = content.split("---", 2)
        if len(parts) < 3:
            return {}
        yaml_text = parts[1].strip()
        data: Dict[str, Any] = {}
        for line in yaml_text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                k, v = line.split(":", 1)
                key = k.strip()
                val = v.strip().strip('"\'')
                # Simple list parsing [a, b]
                if val.startswith("[") and val.endswith("]"):
                    items = [x.strip().strip('"\'') for x in val[1:-1].split(",") if x.strip()]
                    data[key] = items
                else:
                    data[key] = val
        return data

    @classmethod
    def scan_directory(cls, root_path: Path | str) -> KnowledgeGraph:
        """Scan directory tree for Markdown and contract files to build the graph."""
        root = Path(root_path)
        kg = KnowledgeGraph()

        for file_path in root.rglob("*.md"):
            # Skip hidden folders except .hath0r
            parts = file_path.relative_to(root).parts
            if any(p.startswith(".") and p != ".hath0r" for p in parts[:-1]):
                continue

            try:
                content = file_path.read_text(encoding="utf-8")
            except Exception:
                continue

            rel_str = str(file_path.relative_to(root))
            fm = cls.parse_frontmatter(content)

            # Determine node type and title
            node_id = fm.get("id") or rel_str
            node_type = fm.get("type") or ("procedure" if "procedure" in rel_str else "document")

            # Extract first heading if title missing
            title = fm.get("title")
            if not title:
                match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
                title = match.group(1).strip() if match else file_path.stem

            subsystem = parts[0] if len(parts) > 1 else "root"

            node = KnowledgeNode(
                id=node_id,
                type=node_type,
                title=title,
                path=rel_str,
                subsystem=subsystem,
                content=content,
                properties=fm,
            )
            kg.add_node(node)

            # Extract frontmatter edges
            for dep in fm.get("depends_on", []) if isinstance(fm.get("depends_on"), list) else [fm.get("depends_on")] if fm.get("depends_on") else []:
                kg.add_edge(KnowledgeEdge(source=node_id, target=dep, relation="depends_on"))
            for imp in fm.get("implements", []) if isinstance(fm.get("implements"), list) else [fm.get("implements")] if fm.get("implements") else []:
                kg.add_edge(KnowledgeEdge(source=node_id, target=imp, relation="implements"))
            for gov in fm.get("governed_by", []) if isinstance(fm.get("governed_by"), list) else [fm.get("governed_by")] if fm.get("governed_by") else []:
                kg.add_edge(KnowledgeEdge(source=node_id, target=gov, relation="governed_by"))

            # Extract markdown link references: [text](path.md)
            for m in re.finditer(r"\[([^\]]+)\]\(([^)]+\.md)\)", content):
                target_link = m.group(2).strip()
                if not target_link.startswith("http"):
                    kg.add_edge(KnowledgeEdge(source=node_id, target=target_link, relation="references"))

        return kg
