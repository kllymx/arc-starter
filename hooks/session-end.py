#!/usr/bin/env python3
"""
ARC Session End Hook

Fires when a Claude Code session ends (SessionEnd) or a Codex turn completes (Stop).
Reads the conversation transcript from stdin, sends it to an LLM for summarization,
and appends the summary to today's daily log.

If it's past COMPILE_AFTER_HOUR and the daily log has changed, spawns compile.py
as a background process to promote knowledge into the wiki.
"""

import asyncio
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.config import (
    COMPILE_AFTER_HOUR,
    MIN_TURNS_FOR_FLUSH,
    SCRIPTS_DIR,
)
from scripts.utils import (
    read_transcript_from_stdin,
    count_turns,
    load_state,
    save_state,
    sha256,
    now_str,
    get_daily_log_path,
)

# Recursion guard — prevent hooks from triggering on SDK-spawned sessions
GUARD_VAR = "ARC_HOOK_INVOKED"

# Summarization prompt
FLUSH_PROMPT = """You are summarizing an AI coding/business assistant conversation for a founder's knowledge base.

Extract ONLY what's worth remembering long-term. Focus on:
- Decisions made (and why)
- Lessons learned
- New business information discovered
- Action items or next steps
- Corrections the founder made to the agent's understanding

Format as a structured session entry:

## Session — [brief topic description]

**Context:** [one line: what was being worked on]

**Key Exchanges:**
- [important point 1]
- [important point 2]

**Decisions Made:**
- [decision and reasoning]

**Lessons Learned:**
- [lesson]

**Action Items:**
- [ ] [action item]

If the conversation was trivial or contained nothing worth saving, respond with exactly: FLUSH_OK"""


async def main():
    # Recursion guard
    if os.environ.get(GUARD_VAR):
        return

    # Read transcript from stdin
    transcript = read_transcript_from_stdin()
    if not transcript:
        return

    # Minimum turns check
    turns = count_turns(transcript)
    if turns < MIN_TURNS_FOR_FLUSH:
        return

    # Deduplication — don't flush the same session twice
    state = load_state()
    transcript_hash = sha256(transcript[:1000])  # Hash first 1K for dedup
    if state.get("last_flush_session") == transcript_hash:
        return

    # Import here to avoid slow startup if we bail early
    from scripts.config import llm_summarize

    try:
        # Set recursion guard for child processes
        os.environ[GUARD_VAR] = "1"

        summary = await llm_summarize(transcript, FLUSH_PROMPT)

        if not summary or summary.strip() == "FLUSH_OK":
            # Nothing worth saving
            state["last_flush_session"] = transcript_hash
            state["last_flush_time"] = now_str()
            save_state(state)
            return

        # Append to daily log
        from scripts.utils import append_to_daily_log
        append_to_daily_log(summary)

        # Update state
        state["last_flush_session"] = transcript_hash
        state["last_flush_time"] = now_str()
        save_state(state)

        # Check if we should auto-compile (past compile hour + daily log changed)
        current_hour = datetime.now().hour
        if current_hour >= COMPILE_AFTER_HOUR:
            daily_log = get_daily_log_path()
            if daily_log.exists():
                current_hash = sha256(daily_log.read_text())
                last_compiled_hash = state.get("compiled_hashes", {}).get(
                    daily_log.name, ""
                )
                if current_hash != last_compiled_hash:
                    # Spawn compile.py as detached background process
                    _spawn_compile()

    except Exception as e:
        # Don't crash the session — log error and move on
        print(f"ARC flush error: {e}", file=sys.stderr)


def _spawn_compile():
    """Spawn compile.py as a fully detached background process."""
    compile_script = SCRIPTS_DIR / "compile.py"
    if not compile_script.exists():
        return

    env = os.environ.copy()
    env[GUARD_VAR] = "1"

    try:
        if sys.platform == "win32":
            CREATE_NO_WINDOW = 0x08000000
            subprocess.Popen(
                [sys.executable, str(compile_script)],
                env=env,
                creationflags=CREATE_NO_WINDOW,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            subprocess.Popen(
                [sys.executable, str(compile_script)],
                env=env,
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
    except Exception:
        pass  # Don't crash the session


if __name__ == "__main__":
    asyncio.run(main())
