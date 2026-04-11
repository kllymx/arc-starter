#!/usr/bin/env python3
"""
ARC Pre-Compact Hook (Claude Code only)

Fires before Claude Code compresses the context window.
Critical for long sessions — captures knowledge before it gets summarized away.

Same logic as session-end.py but with a higher minimum turn threshold
to avoid redundant captures in short sessions.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.config import MIN_TURNS_FOR_FLUSH
from scripts.utils import (
    read_transcript_from_stdin,
    count_turns,
    load_state,
    save_state,
    sha256,
    now_str,
)

GUARD_VAR = "ARC_HOOK_INVOKED"

FLUSH_PROMPT = """You are summarizing an AI coding/business assistant conversation for a founder's knowledge base.

This is a mid-session capture before context compression. Focus on what's been discussed so far.

Extract ONLY what's worth remembering long-term:
- Decisions made (and why)
- Lessons learned
- New business information discovered
- Action items or next steps
- Corrections the founder made

Format as a structured session entry:

## Session (mid-capture) — [brief topic description]

**Context:** [one line: what was being worked on]

**Key Exchanges:**
- [important point]

**Decisions Made:**
- [decision and reasoning]

**Lessons Learned:**
- [lesson]

If the conversation was trivial, respond with exactly: FLUSH_OK"""


async def main():
    if os.environ.get(GUARD_VAR):
        return

    transcript = read_transcript_from_stdin()
    if not transcript:
        return

    # Higher threshold for pre-compact — avoid redundant captures
    turns = count_turns(transcript)
    if turns < max(MIN_TURNS_FOR_FLUSH, 5):
        return

    state = load_state()
    transcript_hash = sha256(transcript[:1000])
    if state.get("last_flush_session") == transcript_hash:
        return

    from scripts.config import llm_summarize

    try:
        os.environ[GUARD_VAR] = "1"

        summary = await llm_summarize(transcript, FLUSH_PROMPT)

        if not summary or summary.strip() == "FLUSH_OK":
            state["last_flush_session"] = transcript_hash
            state["last_flush_time"] = now_str()
            save_state(state)
            return

        from scripts.utils import append_to_daily_log
        append_to_daily_log(summary)

        state["last_flush_session"] = transcript_hash
        state["last_flush_time"] = now_str()
        save_state(state)

    except Exception as e:
        print(f"ARC pre-compact error: {e}", file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(main())
