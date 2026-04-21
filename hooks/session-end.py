"""
SessionEnd hook - captures conversation transcript for knowledge extraction.

Wired to Claude Code's SessionEnd event: fires exactly once when a session
terminates. Reads the transcript path from stdin, extracts the most recent
conversation context, and spawns flush.py as a background process to extract
knowledge into the daily log.

Long sessions that auto-compact are handled separately by pre-compact.py
(PreCompact event), which captures each pre-summarization slice so nothing
is lost to the compaction summary.

Codex has no SessionEnd event as of April 2026, so this script is not wired
up on the Codex side — Codex users run /reflect manually for capture. The
environment guard below stays in place as a safety net in case a hook is
mis-wired.

The hook itself does NO API calls - only local file I/O for speed (<10s).
The actual API work runs in the detached flush.py subprocess.
"""

from __future__ import annotations

import json
import logging
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Recursion guard: if we were spawned by flush.py (which calls Agent SDK,
# which runs Claude Code, which would fire this hook again), exit immediately.
if os.environ.get("ARC_HOOK_INVOKED"):
    sys.exit(0)

# Skip for Codex — it treats every message as a separate session,
# which would spawn a flush for every single exchange.
# Codex users capture knowledge via /reflect instead.
if any(os.environ.get(k) for k in ("CODEX_CLI", "CODEX_THREAD_ID", "CODEX_MANAGED_BY_BUN", "CODEX_CI")):
    sys.exit(0)

ROOT = Path(__file__).resolve().parent.parent
DAILY_DIR = ROOT / "daily"
SCRIPTS_DIR = ROOT / "scripts"

logging.basicConfig(
    filename=str(SCRIPTS_DIR / "flush.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [session-end] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

MAX_TURNS = 30
MAX_CONTEXT_CHARS = 15_000
MIN_TURNS_TO_FLUSH = 3


def extract_conversation_context(transcript_path: Path) -> tuple[str, int]:
    """Read JSONL transcript and extract last ~N conversation turns as markdown."""
    turns: list[str] = []

    with open(transcript_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue

            # Handle three transcript formats:
            # 1. Claude Code CLI: {"role": "user", "content": [...]}
            # 2. Claude Code VS Code: {"message": {"role": "user", "content": [...]}}
            # 3. Codex: {"type": "response_item", "payload": {"role": "user", "content": [...]}}
            payload = entry.get("payload", {})
            msg = entry.get("message", payload if isinstance(payload, dict) else {})
            if isinstance(msg, dict):
                role = msg.get("role", "")
                content = msg.get("content", "")
            else:
                role = entry.get("role", "")
                content = entry.get("content", "")

            if role not in ("user", "assistant"):
                continue

            if isinstance(content, list):
                text_parts = []
                for block in content:
                    if isinstance(block, dict):
                        # Claude uses "text", Codex uses "input_text" and "output_text"
                        text = (
                            block.get("text", "")
                            or block.get("input_text", "")
                            or block.get("output_text", "")
                        )
                        if text:
                            text_parts.append(text)
                    elif isinstance(block, str):
                        text_parts.append(block)
                content = "\n".join(text_parts)

            if isinstance(content, str) and content.strip():
                label = "User" if role == "user" else "Assistant"
                turns.append(f"**{label}:** {content.strip()}\n")

    recent = turns[-MAX_TURNS:]
    context = "\n".join(recent)

    if len(context) > MAX_CONTEXT_CHARS:
        context = context[-MAX_CONTEXT_CHARS:]
        boundary = context.find("\n**")
        if boundary > 0:
            context = context[boundary + 1:]

    return context, len(recent)


def main() -> None:
    # Read hook input from stdin
    try:
        raw_input = sys.stdin.read()
        try:
            hook_input: dict = json.loads(raw_input)
        except json.JSONDecodeError:
            # Windows may pass paths with unescaped backslashes
            fixed_input = re.sub(r'(?<!\\)\\(?!["\\])', r'\\\\', raw_input)
            hook_input = json.loads(fixed_input)
    except (json.JSONDecodeError, ValueError, EOFError) as e:
        logging.error("Failed to parse stdin: %s", e)
        return

    session_id = hook_input.get("session_id", "unknown")
    transcript_path_str = hook_input.get("transcript_path", "")

    logging.info("SessionEnd hook fired: session=%s", session_id)

    if not transcript_path_str or not isinstance(transcript_path_str, str):
        logging.info("SKIP: no transcript path")
        return

    transcript_path = Path(transcript_path_str)
    if not transcript_path.exists():
        logging.info("SKIP: transcript missing: %s", transcript_path_str)
        return

    # Extract conversation context in the hook (fast, no API calls)
    try:
        context, turn_count = extract_conversation_context(transcript_path)
    except Exception as e:
        logging.error("Context extraction failed: %s", e)
        return

    if not context.strip():
        logging.info("SKIP: empty context")
        return

    if turn_count < MIN_TURNS_TO_FLUSH:
        logging.info("SKIP: only %d turns (min %d)", turn_count, MIN_TURNS_TO_FLUSH)
        return

    # Write context to a temp file for the background process
    timestamp = datetime.now(timezone.utc).astimezone().strftime("%Y%m%d-%H%M%S")
    context_file = SCRIPTS_DIR / f"session-flush-{session_id}-{timestamp}.md"
    context_file.write_text(context, encoding="utf-8")

    # Spawn flush.py as a background process (outside hook timeout)
    flush_script = SCRIPTS_DIR / "flush.py"

    cmd = [
        "uv",
        "run",
        "--directory",
        str(ROOT),
        "python",
        str(flush_script),
        str(context_file),
        session_id,
    ]

    creation_flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

    try:
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creation_flags,
        )
        logging.info(
            "Spawned flush.py for session %s (%d turns, %d chars)",
            session_id, turn_count, len(context),
        )
    except Exception as e:
        logging.error("Failed to spawn flush.py: %s", e)


if __name__ == "__main__":
    main()
