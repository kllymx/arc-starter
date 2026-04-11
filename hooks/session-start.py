#!/usr/bin/env python3
"""
ARC Session Start Hook

Fires when a new Claude Code or Codex session begins.
Injects the wiki index + business overview + recent daily logs into the session
so the agent starts with full context.

Output goes to stdout as JSON — Claude Code/Codex reads this as system context.
"""

import json
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.config import (
    WIKI_INDEX,
    OVERVIEW_FILE,
    MEMORY_FILE,
    MAX_CONTEXT_CHARS,
)
from scripts.utils import read_wiki_index, read_recent_daily_logs


def _has_meaningful_context(content: str, kind: str) -> bool:
    """Filter out starter template text so blank workspaces stay blank."""
    normalized = content.strip().lower()
    if not normalized:
        return False

    placeholder_markers = {
        "overview": [
            "fast one-page summary of the business",
            "this file is created during /setup",
        ],
        "memory": [
            "lightweight preferences, corrections, and facts learned during conversations.",
            "this file stores two types of information:",
        ],
    }

    return not all(marker in normalized for marker in placeholder_markers[kind])


def main():
    """Assemble and output session context."""
    parts = []

    # 1. Business overview (fast snapshot)
    if OVERVIEW_FILE.exists():
        overview = OVERVIEW_FILE.read_text().strip()
        if _has_meaningful_context(overview, "overview"):
            parts.append(f"## Business Overview\n\n{overview}")

    # 2. Memory (preferences + corrections)
    if MEMORY_FILE.exists():
        memory = MEMORY_FILE.read_text().strip()
        if _has_meaningful_context(memory, "memory"):
            parts.append(f"## Memory\n\n{memory}")

    # 3. Wiki index (navigation layer)
    wiki_index = read_wiki_index()
    if wiki_index and "No articles yet" not in wiki_index:
        parts.append(f"## Wiki Index\n\n{wiki_index}")

    # 4. Recent daily logs (what happened recently)
    recent_logs = read_recent_daily_logs(max_chars=3000)
    if recent_logs:
        parts.append(f"## Recent Session Logs\n\n{recent_logs}")

    if not parts:
        # Nothing to inject — wiki hasn't been set up yet
        return

    # Combine and truncate if needed
    combined = "\n\n---\n\n".join(parts)
    if len(combined) > MAX_CONTEXT_CHARS:
        combined = combined[:MAX_CONTEXT_CHARS] + "\n\n[... truncated for context limit]"

    # Output as JSON for the hook system
    output = {
        "message": combined
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
