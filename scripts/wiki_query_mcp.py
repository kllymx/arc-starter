#!/usr/bin/env python3
"""
Optional stdio MCP server exposing ARC wiki retrieval.

Follows Model Context Protocol (2024-11-05) over newline-delimited JSON-RPC.
Opt-in: register manually in Claude Code or Codex — not required by ARC hooks.

Usage:
    uv run python scripts/wiki_query_mcp.py
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.wiki_query import run_query  # noqa: E402

LOG_FILE = PROJECT_ROOT / "scripts" / "wiki_query_mcp.log"

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [wiki_query_mcp] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

PROTOCOL_VERSION = "2024-11-05"
SERVER_NAME = "arc-wiki-query"
SERVER_VERSION = "1.0.0"

WIKI_QUERY_TOOL = {
    "name": "wiki_query",
    "description": (
        "Search the ARC wiki for articles relevant to a query. Returns compact "
        "markdown with paths, summaries, and excerpts — no vectors, stdlib-only."
    ),
    "inputSchema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search terms (keywords or short phrase).",
            },
            "k": {
                "type": "integer",
                "description": "Maximum articles to return (default 5).",
                "minimum": 1,
                "default": 5,
            },
        },
        "required": ["query"],
    },
}


def _send(message: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(message, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def _error_response(req_id: Any, code: int, message: str) -> None:
    _send(
        {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": code, "message": message},
        }
    )


def _result_response(req_id: Any, result: dict[str, Any]) -> None:
    _send({"jsonrpc": "2.0", "id": req_id, "result": result})


def handle_initialize(req_id: Any, params: dict[str, Any]) -> None:
    client_version = params.get("protocolVersion", PROTOCOL_VERSION)
    if client_version != PROTOCOL_VERSION:
        logging.warning("client protocol %s, replying with %s", client_version, PROTOCOL_VERSION)

    _result_response(
        req_id,
        {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {"listChanged": False}},
            "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
            "instructions": (
                "Use wiki_query to find relevant ARC wiki articles before reading "
                "full files. Pass a short keyword query; read returned paths only "
                "when you need full context."
            ),
        },
    )


def handle_tools_list(req_id: Any) -> None:
    _result_response(req_id, {"tools": [WIKI_QUERY_TOOL]})


def handle_tools_call(req_id: Any, params: dict[str, Any]) -> None:
    name = params.get("name")
    if name != "wiki_query":
        _error_response(req_id, -32602, f"Unknown tool: {name}")
        return

    arguments = params.get("arguments") or {}
    query = arguments.get("query")
    if not isinstance(query, str) or not query.strip():
        _result_response(
            req_id,
            {
                "content": [
                    {
                        "type": "text",
                        "text": "wiki_query requires a non-empty `query` string.",
                    }
                ],
                "isError": True,
            },
        )
        return

    k = arguments.get("k", 5)
    try:
        k_int = int(k)
    except (TypeError, ValueError):
        _result_response(
            req_id,
            {
                "content": [{"type": "text", "text": "`k` must be a positive integer."}],
                "isError": True,
            },
        )
        return

    if k_int < 1:
        _result_response(
            req_id,
            {
                "content": [{"type": "text", "text": "`k` must be at least 1."}],
                "isError": True,
            },
        )
        return

    try:
        text = run_query(query.strip(), k=k_int, full=False)
    except Exception as exc:  # noqa: BLE001 — surface tool errors to client
        logging.exception("wiki_query tool failed")
        _result_response(
            req_id,
            {
                "content": [{"type": "text", "text": f"wiki_query failed: {exc}"}],
                "isError": True,
            },
        )
        return

    logging.info("tool wiki_query query=%r k=%d", query, k_int)
    _result_response(
        req_id,
        {"content": [{"type": "text", "text": text}], "isError": False},
    )


def handle_request(message: dict[str, Any]) -> None:
    method = message.get("method")
    req_id = message.get("id")
    params = message.get("params") or {}

    if method == "initialize":
        handle_initialize(req_id, params)
        return

    if method == "ping":
        if req_id is not None:
            _result_response(req_id, {})
        return

    if method in {"notifications/initialized", "initialized"}:
        return

    if method == "tools/list":
        handle_tools_list(req_id)
        return

    if method == "tools/call":
        handle_tools_call(req_id, params)
        return

    if req_id is not None:
        _error_response(req_id, -32601, f"Method not found: {method}")


def serve() -> None:
    for raw_line in sys.stdin:
        line = raw_line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            logging.warning("invalid JSON on stdin")
            continue
        if not isinstance(message, dict):
            continue
        try:
            handle_request(message)
        except Exception:
            logging.exception("unhandled MCP request")
            req_id = message.get("id")
            if req_id is not None:
                _error_response(req_id, -32603, "Internal error")


def main() -> int:
    serve()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())