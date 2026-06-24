# Wiki Retrieval — Find Articles Without Reading Everything

Your ARC wiki grows article by article. Reading the full index (or opening every file) burns context fast. **Wiki retrieval** returns only the slices that match your question — paths, summaries, and short excerpts you can follow up with a targeted Read.

No vectors, no external APIs. Just keyword overlap over plain markdown.

---

## When to Use It

| Situation | Use |
|-----------|-----|
| "What do we know about X?" | `wiki_query.py` — get top matches + excerpts |
| First session, wiki is empty | Read `wiki/index.md` (or run `/setup`) |
| You already know the article | Read the file directly |
| You need the full graph / catalog | Read `wiki/index.md` |
| Agent has MCP enabled | Call the `wiki_query` tool instead of shelling out |

**Rule of thumb:** Search first, read second. Pull full articles only when the excerpt isn't enough.

---

## CLI Usage

From the project root:

```bash
uv run python scripts/wiki_query.py "pricing strategy"
uv run python scripts/wiki_query.py "enterprise sales" --k 3
uv run python scripts/wiki_query.py "onboarding" --full
```

| Flag | Meaning |
|------|---------|
| `query` | Keywords or short phrase (required) |
| `--k N` | Max articles to return (default 5) |
| `--full` | Print whole article bodies instead of excerpts |

Output is compact markdown: relative path (clickable in most editors), title, one-line summary, score, and a short excerpt around the best matching lines.

On a blank wiki you get a clear message and exit code 0 — no crash.

### How ranking works

Deterministic keyword scoring (documented in `scripts/wiki_query.py`):

1. Query terms are tokenized (lowercase, min length 2).
2. Matches in **title** weigh most, then **tags**, **index summary**, then **body**.
3. Articles listed in the same `wiki/index.md` section as other query hits get a proximity boost.
4. Ties break alphabetically by path.

---

## Optional MCP Server

The MCP server wraps the same retrieval logic. It is **opt-in** — ARC hooks and session start do not require it.

**Tool:** `wiki_query(query, k?)` → same markdown as the CLI (excerpts, not `--full`).

### Register in Claude Code

Add to `.mcp.json` in the project root (or your user MCP settings):

```json
{
  "mcpServers": {
    "arc-wiki-query": {
      "command": "uv",
      "args": ["run", "python", "scripts/wiki_query_mcp.py"],
      "cwd": "/absolute/path/to/arc-starter"
    }
  }
}
```

Replace `cwd` with your workspace path. Restart Claude Code (or reload MCP) after saving.

A copy-paste template lives at `extensions/wiki-query-mcp.example.json`.

### Register in Codex

Add to `~/.codex/config.toml` or project `.codex/config.toml` (trusted projects):

```toml
[mcp_servers.arc-wiki-query]
command = "uv"
args = ["run", "python", "scripts/wiki_query_mcp.py"]
cwd = "/absolute/path/to/arc-starter"
```

Or use the CLI helper:

```bash
codex mcp add arc-wiki-query -- uv run python scripts/wiki_query_mcp.py
```

Run `/mcp` in the Codex TUI to confirm the server is active.

### Obsidian (optional)

Coding agents with direct filesystem access (Claude Code, Codex, Cursor) do **not** need an Obsidian bridge — they read `wiki/` directly.

If you use **Claude Desktop** or another client without FS access, community Obsidian MCP servers (Local REST API + `mcp-obsidian`) can expose your vault. Wiki retrieval is still useful inside ARC-native CLIs; see [MCPs — Connecting Your AI to External Tools](mcps-explained.md) for the general MCP picture.

---

## Security Note

The MCP server only reads markdown under `wiki/`. It does not write files or call external networks. Like any MCP, it runs as a local subprocess — register it only in workspaces you trust.

---

## Related

- [MCPs — Connecting Your AI to External Tools](mcps-explained.md)
- `wiki/index.md` — full catalog when you need the big picture
- `/setup` — populate the wiki if retrieval returns "no articles yet"