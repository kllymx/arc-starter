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

# Private tier (company mode) — local-only, never pushed to the shared remote.
# See .gitignore: the whole `private/` tree is excluded from git, so personal
# context stays on the founder's machine and never reaches teammates. It is
# created by /setup (empty) and populated by /upgrade-to-company and /promote.
PRIVATE_DIR = PROJECT_ROOT / "private"
PRIVATE_WIKI_DIR = PRIVATE_DIR / "wiki"
PRIVATE_CONCEPTS_DIR = PRIVATE_WIKI_DIR / "concepts"
PRIVATE_CONNECTIONS_DIR = PRIVATE_WIKI_DIR / "connections"
PRIVATE_QA_DIR = PRIVATE_WIKI_DIR / "qa"
PRIVATE_CONTEXT_DIR = PRIVATE_DIR / "context"

# Key files
WIKI_INDEX = WIKI_DIR / "index.md"
WIKI_LOG = WIKI_DIR / "log.md"
PRIVATE_WIKI_INDEX = PRIVATE_WIKI_DIR / "index.md"
OVERVIEW_FILE = CONTEXT_DIR / "overview.md"
WORKSPACE_FILE = CONTEXT_DIR / "workspace.md"
MEMORY_FILE = CONTEXT_DIR / "memory.md"
# Shared, committed sharing settings (Mode + Sync). Kept separate from the
# per-person workspace.md so the team's shared truth isn't a per-machine file.
SHARING_CONFIG_FILE = CONTEXT_DIR / "sharing.md"
STATE_FILE = SCRIPTS_DIR / "state.json"

# Compilation settings
COMPILE_AFTER_HOUR = 18  # Auto-compile after 6 PM local time
MAX_CONTEXT_CHARS = 20_000  # Max chars to inject at session start
MAX_TRANSCRIPT_CHARS = 15_000  # Max chars to send for summarization
MIN_TURNS_FOR_FLUSH = 3  # Minimum conversation turns before flushing

# LLM settings
CLAUDE_MODEL = "claude-sonnet-4-20250514"
OPENAI_MODEL = "gpt-4o"
CODEX_ENV_VARS = {
    "CODEX_CLI",
    "CODEX_THREAD_ID",
    "CODEX_MANAGED_BY_BUN",
    "CODEX_CI",
}


def _normalize_environment_label(value: str) -> str:
    normalized = value.strip().lower()
    if normalized in {"claude code", "claude-code", "claude code cli"}:
        return "claude-code"
    if normalized == "cursor":
        return "claude-code"
    if normalized == "codex":
        return "codex"
    return "unknown"


def detect_environment() -> str:
    """
    Detect which AI environment the founder is using.
    Returns: 'claude-code', 'codex', or 'unknown'

    Detection order:
    1. Read context/workspace.md for explicit environment setting
    2. Check environment variables
    3. Check for environment-specific markers when unambiguous
    """
    # 1. Check workspace.md
    if WORKSPACE_FILE.exists():
        content = WORKSPACE_FILE.read_text()
        patterns = [
            r"^\s*-\s*Primary environment:\s*(.+?)\s*$",
            r"^\s*-\s*Environment:\s*(.+?)\s*$",
            r"^\s*Primary environment:\s*(.+?)\s*$",
            r"^\s*Environment:\s*(.+?)\s*$",
        ]
        for pattern in patterns:
            match = re.search(pattern, content, re.MULTILINE)
            if match:
                environment = _normalize_environment_label(match.group(1))
                if environment != "unknown":
                    return environment

    # 2. Check environment variables
    if os.environ.get("ARC_ENVIRONMENT"):
        environment = _normalize_environment_label(os.environ["ARC_ENVIRONMENT"])
        if environment != "unknown":
            return environment
    if os.environ.get("CLAUDE_CODE"):
        return "claude-code"
    if any(os.environ.get(key) for key in CODEX_ENV_VARS):
        return "codex"

    # 3. Check for environment markers when only one integration is present.
    # This repo ships with both .claude and .codex, so marker presence alone
    # is not a reliable signal in a fresh clone.
    has_claude = (PROJECT_ROOT / ".claude").exists()
    has_codex = (PROJECT_ROOT / ".codex").exists()
    if has_claude and not has_codex:
        return "claude-code"
    if has_codex and not has_claude:
        return "codex"

    return "unknown"


def get_mode() -> str:
    """Return the ARC sharing mode: 'personal' (default) or 'company'.

    Personal mode: a single founder's brain. Captured knowledge compiles
    straight into the shared `wiki/`.

    Company mode: a shared/team brain. New auto-captured knowledge compiles
    into the local-only `private/wiki/` first and only reaches the shared
    `wiki/` through a deliberate, reviewed step (/promote or the manifest in
    /upgrade-to-company). This keeps the personal-vs-company privacy boundary
    a fail-closed default rather than something the founder must remember.

    Resolution order:
    1. ARC_MODE environment variable ('personal' | 'company')
    2. context/sharing.md  ('- Mode: company')  — the shared, committed setting
    3. context/workspace.md  — back-compat fallback for older workspaces
    4. default 'personal'
    """
    env = os.environ.get("ARC_MODE", "").strip().lower()
    if env in {"personal", "company"}:
        return env

    value = _read_setting("Mode", SHARING_CONFIG_FILE, WORKSPACE_FILE)
    if value in {"personal", "company"}:
        return value
    return "personal"


def get_sync_strategy() -> str:
    """Return the company-mode sync strategy: 'pr' (default) or 'direct'.

    - 'pr': each person works on a personal branch and merges via pull requests.
      The safe default; nobody pushes shared main directly.
    - 'direct': small trusted teams work on main and `/sync` rebases onto
      origin/main, reconciles, and pushes main directly — no branches/PRs.

    Resolution: ARC_SYNC_STRATEGY env, then context/sharing.md ('- Sync: direct'),
    then context/workspace.md (back-compat), then 'pr'.
    """
    env = os.environ.get("ARC_SYNC_STRATEGY", "").strip().lower()
    if env in {"pr", "direct"}:
        return env

    value = _read_setting("Sync", SHARING_CONFIG_FILE, WORKSPACE_FILE)
    if value in {"pr", "direct"}:
        return value
    return "pr"


def _read_setting(key: str, *files: Path) -> str | None:
    """Read a `- <key>: <value>` line from the first file that has one."""
    pattern = re.compile(
        rf"^\s*-?\s*{re.escape(key)}:\s*([A-Za-z][\w-]*)\s*$",
        re.MULTILINE | re.IGNORECASE,
    )
    for path in files:
        if path.exists():
            match = pattern.search(path.read_text())
            if match:
                return match.group(1).lower()
    return None


def get_user_slug() -> str:
    """Return a filesystem/branch-safe slug identifying this person, used to
    name their personal company-mode branch (`arc/<slug>`).

    Derived from git config: the local-part of user.email, else user.name,
    else 'local'. Lowercased; only [a-z0-9._-] kept. Must stay in lockstep
    with the bash equivalent in hooks/git-push.sh.
    """
    import subprocess

    def _git_config(key: str) -> str:
        try:
            out = subprocess.run(
                ["git", "config", key],
                capture_output=True,
                text=True,
                cwd=str(PROJECT_ROOT),
                timeout=5,
            )
            return out.stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return ""

    raw = _git_config("user.email")
    if "@" in raw:
        raw = raw.split("@", 1)[0]
    # GitHub noreply addresses look like `12345+username` — prefer the username.
    if "+" in raw:
        raw = raw.rsplit("+", 1)[1]
    if not raw:
        raw = _git_config("user.name")

    slug = re.sub(r"[^a-z0-9._-]", "", raw.lower().replace(" ", "-"))
    return slug or "local"


def get_user_branch() -> str:
    """The personal branch this person works on in company mode."""
    return f"arc/{get_user_slug()}"


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
    if env == "claude-code":
        return {"type": "claude", "model": CLAUDE_MODEL}

    # Conservative fallback for local debugging and direct script runs.
    return {"type": "claude", "model": CLAUDE_MODEL}


async def llm_summarize(text: str, system_prompt: str) -> str:
    """
    Send text to the appropriate LLM for summarization.
    Routes to Claude Agent SDK or OpenAI based on environment.
    Falls back to Claude Agent SDK if OpenAI is unavailable.
    """
    backend = get_llm_backend()

    if backend["type"] == "openai":
        try:
            return await _openai_summarize(text, system_prompt, backend["model"])
        except Exception:
            # Fallback to Claude Agent SDK if OpenAI API key isn't set
            return await _claude_summarize(text, system_prompt, CLAUDE_MODEL)
    else:
        return await _claude_summarize(text, system_prompt, backend["model"])


async def _claude_summarize(text: str, system_prompt: str, model: str) -> str:
    """Summarize using Claude Agent SDK."""
    import tempfile
    from claude_agent_sdk import query, ClaudeAgentOptions

    messages = []
    async for msg in query(
        prompt=f"{system_prompt}\n\n---\n\n{text}",
        options=ClaudeAgentOptions(
            model=model,
            allowed_tools=[],
            max_turns=1,
            permission_mode="acceptEdits",
            cwd=tempfile.gettempdir(),
        ),
    ):
        if hasattr(msg, "content"):
            for block in (msg.content if isinstance(msg.content, list) else [msg.content]):
                if hasattr(block, "text"):
                    messages.append(block.text)
    return "\n".join(messages)


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
