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
    Read conversation transcript via Claude Code hook stdin.

    Supports two formats:
    - VS Code extension: a single JSON metadata object with a
      transcript_path field pointing to a JSONL file on disk.
    - CLI: JSONL piped directly to stdin with role/content entries.

    Returns the last N characters of conversation turns.
    """
    raw = ""
    try:
        raw = sys.stdin.read()
    except Exception:
        pass

    if not raw.strip():
        return ""

    # Try parsing as hook metadata (single JSON object with transcript_path)
    lines = []
    try:
        metadata = json.loads(raw)
        if isinstance(metadata, dict) and "transcript_path" in metadata:
            transcript_file = Path(metadata["transcript_path"])
            if transcript_file.exists():
                with open(transcript_file) as f:
                    lines = [line.strip() for line in f if line.strip()]
    except (json.JSONDecodeError, TypeError):
        pass

    # Fallback: treat stdin as JSONL directly
    if not lines:
        lines = [line.strip() for line in raw.splitlines() if line.strip()]

    if not lines:
        return ""

    # Parse JSONL and extract message content
    # Claude Code transcript format nests messages:
    #   {"type": "user", "message": {"role": "user", "content": [...]}}
    messages = []
    for line in lines:
        try:
            entry = json.loads(line)

            # Extract role and content — handle both nested and flat formats
            msg = entry.get("message", entry)
            role = msg.get("role", "") or entry.get("type", "")
            content = msg.get("content", "")

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
