#!/usr/bin/env python3
"""
ARC Session Start Hook

Fires when a new Claude Code or Codex session begins.
Injects a tiered, budget-aware context slice (overview, memory, index
navigation, recent daily heads) so the agent starts lean.

Output goes to stdout as JSON — Claude Code/Codex reads this as system context.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.context_select import INJECT_BUDGET_CHARS, build_session_context


def main() -> None:
    """Assemble and output session context."""
    combined = build_session_context(budget_chars=INJECT_BUDGET_CHARS)
    if not combined:
        return

    output = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": combined,
        }
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()