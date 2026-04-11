"""
ARC configuration and environment detection.

Reads context/workspace.md to determine which LLM SDK to use,
and provides shared configuration for all scripts.
"""

import os
import re
from pathlib import Path

# Project root — one level up from scripts/
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Key directories
CONTEXT_DIR = PROJECT_ROOT / "context"
WIKI_DIR = PROJECT_ROOT / "wiki"
CONCEPTS_DIR = WIKI_DIR / "concepts"
CONNECTIONS_DIR = WIKI_DIR / "connections"
DAILY_DIR = PROJECT_ROOT / "daily"
IMPORTS_DIR = PROJECT_ROOT / "imports"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

# Key files
WIKI_INDEX = WIKI_DIR / "index.md"
WIKI_LOG = WIKI_DIR / "log.md"
OVERVIEW_FILE = CONTEXT_DIR / "overview.md"
WORKSPACE_FILE = CONTEXT_DIR / "workspace.md"
MEMORY_FILE = CONTEXT_DIR / "memory.md"
STATE_FILE = SCRIPTS_DIR / "state.json"

# Compilation settings
COMPILE_AFTER_HOUR = 18  # Auto-compile after 6 PM local time
MAX_CONTEXT_CHARS = 20_000  # Max chars to inject at session start
MAX_TRANSCRIPT_CHARS = 15_000  # Max chars to send for summarization
MIN_TURNS_FOR_FLUSH = 3  # Minimum conversation turns before flushing

# LLM settings
CLAUDE_MODEL = "claude-sonnet-4-20250514"
OPENAI_MODEL = "gpt-4o"


def detect_environment() -> str:
    """
    Detect which AI environment the founder is using.
    Returns: 'claude-code', 'codex', or 'unknown'

    Detection order:
    1. Read context/workspace.md for explicit environment setting
    2. Check for environment-specific markers (.claude/ vs .codex/)
    3. Check environment variables
    """
    # 1. Check workspace.md
    if WORKSPACE_FILE.exists():
        content = WORKSPACE_FILE.read_text()
        content_lower = content.lower()
        if "claude code" in content_lower or "claude-code" in content_lower:
            return "claude-code"
        if "codex" in content_lower:
            return "codex"
        if "cursor" in content_lower:
            return "claude-code"  # Cursor uses Claude under the hood

    # 2. Check for environment markers
    if (PROJECT_ROOT / ".claude").exists():
        return "claude-code"
    if (PROJECT_ROOT / ".codex").exists():
        return "codex"

    # 3. Check environment variables
    if os.environ.get("CLAUDE_CODE"):
        return "claude-code"
    if os.environ.get("CODEX_CLI"):
        return "codex"

    return "unknown"


def get_llm_backend():
    """
    Returns the appropriate LLM backend based on detected environment.

    Returns a dict with:
    - 'type': 'claude' or 'openai'
    - 'model': model identifier string
    """
    env = detect_environment()

    if env == "codex":
        return {"type": "openai", "model": OPENAI_MODEL}
    else:
        # Default to Claude for claude-code, cursor, and unknown
        return {"type": "claude", "model": CLAUDE_MODEL}


async def llm_summarize(text: str, system_prompt: str) -> str:
    """
    Send text to the appropriate LLM for summarization.
    Routes to Claude Agent SDK or OpenAI based on environment.
    """
    backend = get_llm_backend()

    if backend["type"] == "claude":
        return await _claude_summarize(text, system_prompt, backend["model"])
    else:
        return await _openai_summarize(text, system_prompt, backend["model"])


async def _claude_summarize(text: str, system_prompt: str, model: str) -> str:
    """Summarize using Claude Agent SDK."""
    from claude_agent_sdk import query

    result = await query(
        prompt=text,
        system=system_prompt,
        model=model,
        allowed_tools=[],
        max_turns=2,
    )
    return result.text


async def _openai_summarize(text: str, system_prompt: str, model: str) -> str:
    """Summarize using OpenAI SDK."""
    from openai import AsyncOpenAI

    client = AsyncOpenAI()  # Uses OPENAI_API_KEY env var
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        max_tokens=4096,
    )
    return response.choices[0].message.content
