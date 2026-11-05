"""AegisBrain Codebase AST Graph Indexer & Traversal Engine.

Reverse-engineered from Graphify architectural principles:
- Indexes repositories into an AST knowledge graph (files, classes, functions, imports, calls).
- Zero external dependencies: pure Python standard library (ast, re, json, collections).
- Zero visual bloat: no HTML, SVG, or rendering slop.
- Ultra-fast BFS/DFS graph traversal so AI agents locate symbols, callers, and dependencies
  in sub-milliseconds without crawling raw files repeatedly.
"""

import ast
import json
import os
import re
from collections import defaultdict, deque
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from .config import get_aegis_dir
from .db import get_connection

GRAPH_SCHEMA = """
CREATE TABLE IF NOT EXISTS graph_nodes (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    kind TEXT NOT NULL,  -- file, function, class, module
    file_path TEXT NOT NULL,
    line_start INTEGER DEFAULT 0,
    line_end INTEGER DEFAULT 0,
    docstring TEXT DEFAULT ''
);

CREATE TABLE IF NOT EXISTS graph_edges (
    source TEXT NOT NULL,
    target TEXT NOT NULL,
    relation TEXT NOT NULL,  -- defines, imports, calls, inherits
    PRIMARY KEY (source, target, relation)
);
"""


def init_graph_db() -> None:
    with get_connection() as conn:
        conn.executescript(GRAPH_SCHEMA)


class CodebaseGraph:
    """In-memory and SQLite-backed AST dependency graph."""

    def __init__(self, workspace_path: Optional[Path] = None):
        self.workspace_path = workspace_path or Path.cwd()
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.adj_out: Dict[str, List[Tuple[str, str]]] = defaultdict(list)
        self.adj_in: Dict[str, List[Tuple[str, str]]] = defaultdict(list)

    def add_node(self, node_id: str, name: str, kind: str, file_path: str, line_start: int = 0, line_end: int = 0, docstring: str = "") -> None:
        self.nodes[node_id] = {
            "id": node_id,
            "name": name,
            "kind": kind,
            "file_path": file_path,
            "line_start": line_start,
            "line_end": line_end,
            "docstring": docstring,
        }

    def add_edge(self, source: str, target: str, relation: str) -> None:
        self.adj_out[source].append((target, relation))
        self.adj_in[target].append((source, relation))

    def index_workspace(self, root_dir: Optional[Path] = None, max_files: int = 300) -> Dict[str, Any]:
        """Scan and index all source files in workspace into AST graph nodes."""
        init_graph_db()
        root = (Path(root_dir) if root_dir else self.workspace_path).resolve()
        indexed_count = 0

        IGNORE_DIRS = {
            ".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build",
            ".pytest_cache", ".gemini", ".system_generated"
        }

        for path in root.rglob("*"):
            if indexed_count >= max_files:
                break
            if not path.is_file():
                continue
            if any(part in IGNORE_DIRS for part in path.parts):
                continue

            rel = str(path.relative_to(root)).replace("\\", "/")
            ext = path.suffix.lower()

            if ext in (".py", ".pyw"):
                self._index_python_file(path, rel)
                indexed_count += 1
            elif ext in (".js", ".ts", ".jsx", ".tsx", ".java", ".go"):
                self._index_generic_code_file(path, rel)
                indexed_count += 1

        # Persist to SQLite
        with get_connection() as conn:
            conn.execute("DELETE FROM graph_nodes")
            conn.execute("DELETE FROM graph_edges")

            for nid, n in self.nodes.items():
                conn.execute("""
                    INSERT OR REPLACE INTO graph_nodes (id, name, kind, file_path, line_start, line_end, docstring)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (n["id"], n["name"], n["kind"], n["file_path"], n["line_start"], n["line_end"], n["docstring"]))

            for src, edges in self.adj_out.items():
                for tgt, rel in edges:
                    conn.execute("""
                        INSERT OR REPLACE INTO graph_edges (source, target, relation)
                        VALUES (?, ?, ?)
                    """, (src, tgt, rel))

        return self.get_stats()

    def _index_python_file(self, full_path: Path, rel_path: str) -> None:
        file_node_id = f"file:{rel_path}"
        self.add_node(file_node_id, name=rel_path, kind="file", file_path=rel_path)

        try:
            content = full_path.read_text(encoding="utf-8", errors="replace")
            tree = ast.parse(content, filename=rel_path)
        except Exception:
            return

        for item in ast.walk(tree):
            if isinstance(item, ast.Import):
                for alias in item.names:
                    mod_id = f"mod:{alias.name}"
                    self.add_node(mod_id, name=alias.name, kind="module", file_path=rel_path)
                    self.add_edge(file_node_id, mod_id, "imports")

            elif isinstance(item, ast.ImportFrom):
                if item.module:
                    mod_id = f"mod:{item.module}"
                    self.add_node(mod_id, name=item.module, kind="module", file_path=rel_path)
                    self.add_edge(file_node_id, mod_id, "imports")

            elif isinstance(item, ast.FunctionDef):
                fn_id = f"func:{rel_path}:{item.name}"
                doc = ast.get_docstring(item) or ""
                end_lineno = getattr(item, "end_lineno", item.lineno)
                self.add_node(fn_id, name=item.name, kind="function", file_path=rel_path, line_start=item.lineno, line_end=end_lineno, docstring=doc)
                self.add_edge(file_node_id, fn_id, "defines")

                # Detect function calls
                for child in ast.walk(item):
                    if isinstance(child, ast.Call):
                        called_name = ""
                        if isinstance(child.func, ast.Name):
                            called_name = child.func.id
                        elif isinstance(child.func, ast.Attribute):
                            called_name = child.func.attr
                        if called_name:
                            self.add_edge(fn_id, f"call:{called_name}", "calls")

            elif isinstance(item, ast.ClassDef):
                cls_id = f"class:{rel_path}:{item.name}"
                doc = ast.get_docstring(item) or ""
                end_lineno = getattr(item, "end_lineno", item.lineno)
                self.add_node(cls_id, name=item.name, kind="class", file_path=rel_path, line_start=item.lineno, line_end=end_lineno, docstring=doc)
                self.add_edge(file_node_id, cls_id, "defines")

    def _index_generic_code_file(self, full_path: Path, rel_path: str) -> None:
        file_node_id = f"file:{rel_path}"
        self.add_node(file_node_id, name=rel_path, kind="file", file_path=rel_path)

        try:
            content = full_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            return

        # Simple high-velocity regex parser for imports & functions
        import_patterns = re.findall(r"(?:import|from)\s+['\"]([^'\"]+)['\"]", content)
        for imp in import_patterns:
            mod_id = f"mod:{imp}"
            self.add_node(mod_id, name=imp, kind="module", file_path=rel_path)
            self.add_edge(file_node_id, mod_id, "imports")

        func_patterns = re.findall(r"(?:function\s+([a-zA-Z0-9_]+)|def\s+([a-zA-Z0-9_]+)|const\s+([a-zA-Z0-9_]+)\s*=\s*(?:async\s*)?\()", content)
        for matches in func_patterns:
            name = next((m for m in matches if m), None)
            if name:
                fn_id = f"func:{rel_path}:{name}"
                self.add_node(fn_id, name=name, kind="function", file_path=rel_path)
                self.add_edge(file_node_id, fn_id, "defines")

    def query_graph(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Find matching nodes by keyword."""
        q_lower = query.lower()
        matches = []
        for n in self.nodes.values():
            if q_lower in n["name"].lower() or q_lower in n["file_path"].lower() or q_lower in n.get("docstring", "").lower():
                matches.append(n)
                if len(matches) >= limit:
                    break
        return matches

    def get_neighbors(self, node_id: str) -> Dict[str, Any]:
        """Return incoming (dependents) and outgoing (dependencies) edges."""
        outgoing = [{"target": tgt, "relation": rel} for tgt, rel in self.adj_out.get(node_id, [])]
        incoming = [{"source": src, "relation": rel} for src, rel in self.adj_in.get(node_id, [])]
        node = self.nodes.get(node_id, {"id": node_id, "name": node_id, "kind": "unknown"})
        return {"node": node, "outgoing": outgoing, "incoming": incoming}

    def shortest_path(self, start_id: str, target_id: str) -> Optional[List[str]]:
        """Breadth-first search for the shortest dependency path between two symbols."""
        if start_id not in self.nodes or target_id not in self.nodes:
            return None

        queue = deque([[start_id]])
        visited = {start_id}

        while queue:
            path = queue.popleft()
            curr = path[-1]

            if curr == target_id:
                return path

            for neighbor, _ in self.adj_out.get(curr, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])

        return None

    def get_stats(self) -> Dict[str, Any]:
        """Return total nodes, edges, and top central (God) nodes."""
        node_degrees = {nid: len(self.adj_in.get(nid, [])) + len(self.adj_out.get(nid, [])) for nid in self.nodes}
        top_nodes = sorted(node_degrees.items(), key=lambda x: x[1], reverse=True)[:5]

        god_nodes = []
        for nid, deg in top_nodes:
            n = self.nodes.get(nid, {})
            god_nodes.append({
                "id": nid,
                "name": n.get("name", nid),
                "kind": n.get("kind", "unknown"),
                "degree": deg,
                "file": n.get("file_path", "")
            })

        return {
            "total_nodes": len(self.nodes),
            "total_edges": sum(len(e) for e in self.adj_out.values()),
            "files_indexed": sum(1 for n in self.nodes.values() if n["kind"] == "file"),
            "functions_indexed": sum(1 for n in self.nodes.values() if n["kind"] == "function"),
            "god_nodes": god_nodes,
        }

    def format_summary(self) -> str:
        """Clean markdown presentation of the indexed graph."""
        stats = self.get_stats()
        lines = [
            "🕸️ *AegisBrain Native Codebase Graph (AST Engine)*",
            f"• *Indexed Nodes:* {stats['total_nodes']} symbols across {stats['files_indexed']} files",
            f"• *Total Edges:* {stats['total_edges']} dependency relationships",
            f"• *Functions Indexed:* {stats['functions_indexed']}",
            "",
            "👑 *Top Central (God) Nodes & Anchor Symbols:*"
        ]
        for g in stats["god_nodes"]:
            lines.append(f"• `{g['name']}` `[{g['kind'].upper()}]` in `{g['file']}` ({g['degree']} connected edges)")

        lines.append("")
        lines.append("⚡ *Fast Traversal:* Agents query caller/callee trees instantly in <1ms without file crawling.")
        return "\n".join(lines)


_active_graph_instance: Optional[CodebaseGraph] = None


def get_active_graph(workspace: Optional[Path] = None) -> CodebaseGraph:
    global _active_graph_instance
    if _active_graph_instance is None or (_active_graph_instance.workspace_path != (workspace or Path.cwd())):
        _active_graph_instance = CodebaseGraph(workspace)
        _active_graph_instance.index_workspace()
    return _active_graph_instance


def traverse_or_fallback(
    query: str,
    workspace: Optional[Path] = None,
    max_results: int = 10,
    workspace_dir: Optional[Path] = None,
) -> Dict[str, Any]:
    """Traverse codebase knowledge base using AST Graph first; natively fall back to file tree if not found."""
    target_ws = workspace or workspace_dir
    graph = get_active_graph(target_ws)
    matches = graph.query_graph(query, limit=max_results)

    if matches:
        enriched = []
        for m in matches:
            nid = m.get("id")
            neighbors = graph.get_neighbors(nid) if nid else {"incoming": [], "outgoing": []}
            enriched.append({
                "name": m.get("name"),
                "kind": m.get("kind"),
                "file_path": m.get("file_path"),
                "lines": f"{m.get('line_start')}-{m.get('line_end')}",
                "docstring": m.get("docstring"),
                "callers": [inc["source"] for inc in neighbors["incoming"][:3]],
                "callees": [out["target"] for out in neighbors["outgoing"][:3]],
            })
        return {
            "query": query,
            "strategy": "ast_graph",
            "matches": enriched,
            "results": enriched,
            "matches_count": len(enriched),
            "fallback_used": False,
        }

    # Fallback to native recursive file search
    ws = (target_ws or Path.cwd()).resolve()
    fallback_matches = []
    q_lower = query.lower()
    for root, dirs, files in os.walk(ws):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", ".venv", "__pycache__", ".pytest_cache"}]
        for fname in files:
            if fname.endswith((".py", ".ts", ".js", ".json", ".md", ".toml", ".txt")):
                fp = Path(root) / fname
                try:
                    rel_p = str(fp.relative_to(ws))
                    if q_lower in fname.lower():
                        fallback_matches.append({"name": fname, "kind": "file", "file_path": rel_p})
                    else:
                        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                            for idx, line in enumerate(f, 1):
                                if q_lower in line.lower():
                                    fallback_matches.append({
                                        "name": fname,
                                        "kind": "text_match",
                                        "file_path": rel_p,
                                        "line": idx,
                                        "snippet": line.strip()[:100],
                                    })
                                    if len(fallback_matches) >= max_results:
                                        break
                except Exception:
                    continue
        if len(fallback_matches) >= max_results:
            break

    return {
        "query": query,
        "strategy": "filesystem_fallback",
        "matches": fallback_matches,
        "results": fallback_matches,
        "matches_count": len(fallback_matches),
        "fallback_used": True,
    }
