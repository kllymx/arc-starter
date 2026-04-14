"""
Shared utilities for ARC automation scripts.
"""

import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

from scripts.config import (
    DAILY_DIR,
    STATE_FILE,
    WIKI_INDEX,
    WIKI_LOG,
    MAX_CONTEXT_CHARS,
)


def today_str() -> str:
    """Return today's date as YYYY-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")


def now_str() -> str:
    """Return current datetime as ISO format."""
    return datetime.now().isoformat()


def get_daily_log_path() -> Path:
    """Get path to today's daily log file."""
    return DAILY_DIR / f"{today_str()}.md"


def sha256(text: str) -> str:
    """Return SHA-256 hash of text."""
    return hashlib.sha256(text.encode()).hexdigest()


# --- State management ---

def load_state() -> dict:
    """Load persistent state from state.json."""
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {
        "last_flush_session": None,
        "last_flush_time": None,
        "compiled_hashes": {},
        "last_compile_time": None,
        "query_count": 0,
        "last_lint": None,
    }


def save_state(state: dict):
    """Save persistent state to state.json."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


# --- Transcript reading ---

def read_transcript_from_stdin(max_chars: int = 15_000) -> str:
    """
    Read conversation transcript from stdin.

    Supports two formats:
    - VS Code extension: a single JSON object with a transcript_path field
      pointing to a JSONL file on disk.
    - CLI: JSONL piped directly to stdin with role/content entries.

    Returns the last N characters of conversation turns.
    """
    raw_lines = []
    try:
        for line in sys.stdin:
            line = line.strip()
            if line:
                raw_lines.append(line)
    except Exception:
        pass

    if not raw_lines:
        return ""

    # Check if this is a VS Code-style metadata object with transcript_path
    transcript_lines = []
    if len(raw_lines) == 1:
        try:
            metadata = json.loads(raw_lines[0])
            transcript_path = metadata.get("transcript_path")
            if transcript_path:
                tp = Path(transcript_path)
                if tp.exists():
                    transcript_lines = [
                        l.strip() for l in tp.read_text().splitlines() if l.strip()
                    ]
        except (json.JSONDecodeError, TypeError):
            pass

    # Fallback: treat stdin lines as direct JSONL (CLI format)
    if not transcript_lines:
        transcript_lines = raw_lines

    # Parse JSONL and extract message content
    messages = []
    for line in transcript_lines:
        try:
            entry = json.loads(line)
            role = entry.get("role", "")
            content = entry.get("content", "")
            if isinstance(content, list):
                # Handle structured content blocks
                text_parts = []
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                content = "\n".join(text_parts)
            if content and role in ("user", "assistant"):
                messages.append(f"**{role.title()}:** {content}")
        except (json.JSONDecodeError, TypeError):
            continue

    # Take the last N chars worth of messages
    combined = "\n\n".join(messages)
    if len(combined) > max_chars:
        combined = combined[-max_chars:]

    return combined


def count_turns(transcript: str) -> int:
    """Count the number of conversation turns in a transcript."""
    return transcript.count("**User:**") + transcript.count("**Assistant:**")


# --- Wiki helpers ---

def read_wiki_index() -> str:
    """Read wiki/index.md content."""
    if WIKI_INDEX.exists():
        return WIKI_INDEX.read_text()
    return ""


def read_recent_daily_logs(max_chars: int = 5000) -> str:
    """Read recent daily log entries, newest first."""
    if not DAILY_DIR.exists():
        return ""

    log_files = sorted(DAILY_DIR.glob("*.md"), reverse=True)
    combined = []
    total_chars = 0

    for log_file in log_files[:7]:  # Last 7 days max
        content = log_file.read_text()
        if total_chars + len(content) > max_chars:
            break
        combined.append(f"--- {log_file.stem} ---\n{content}")
        total_chars += len(content)

    return "\n\n".join(combined)


def append_to_daily_log(content: str):
    """Append a session summary to today's daily log."""
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    log_path = get_daily_log_path()

    if not log_path.exists():
        log_path.write_text(f"# Daily Log — {today_str()}\n\n")

    with open(log_path, "a") as f:
        f.write(f"\n{content}\n")


def append_to_wiki_log(entry: str):
    """Append an operation entry to wiki/log.md."""
    if not WIKI_LOG.exists():
        return

    with open(WIKI_LOG, "a") as f:
        f.write(f"\n{entry}\n")
