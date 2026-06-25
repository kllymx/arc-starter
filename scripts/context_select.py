"""
Tiered, budget-aware session context assembly for SessionStart injection.

Selects high-signal slices (overview, memory, index navigation, recent daily
heads) instead of dumping full wiki index and multi-day transcripts.
"""

from __future__ import annotations

import re
from pathlib import Path

from scripts.config import (
    DAILY_DIR,
    MEMORY_FILE,
    OVERVIEW_FILE,
    PRIVATE_WIKI_INDEX,
    SCRIPTS_DIR,
    WIKI_INDEX,
    get_mode,
)

INJECT_BUDGET_CHARS = 7000
OVERVIEW_MAX_CHARS = 2000
MEMORY_MAX_CHARS = 2000
INDEX_NAV_MAX_CHARS = 2500
DAILY_LOOKBACK_DAYS = 2
DAILY_ACTIVITY_MAX_CHARS = 1500
DAILY_EXCERPT_CHARS = 800
TRUNCATION_MARKER = "\n\n[...truncated]"

_WIKILINK_RE = re.compile(r"\[\[[^\]]+\]\]")
_PLACEHOLDER_MARKERS = {
    "overview": [
        "fast one-page summary of the business",
        "this file is created during /setup",
    ],
    "memory": [
        "lightweight preferences, corrections, and facts learned during conversations.",
        "this file stores two types of information:",
    ],
}


def has_meaningful_context(content: str, kind: str) -> bool:
    """Filter out starter template text so blank workspaces stay blank."""
    normalized = content.strip().lower()
    if not normalized:
        return False
    markers = _PLACEHOLDER_MARKERS[kind]
    return not all(marker in normalized for marker in markers)


def _truncate_text(text: str, max_chars: int, *, per_section: bool = True) -> str:
    text = text.strip()
    if not text or len(text) <= max_chars:
        return text
    cut = text[:max_chars]
    if per_section and max_chars > 40:
        last_break = max(cut.rfind("\n\n"), cut.rfind("\n"), cut.rfind(" "))
        if last_break > max_chars // 2:
            cut = cut[:last_break]
    return cut.rstrip() + "\n[...truncated]"


def _apply_total_budget(text: str, budget_chars: int) -> str:
    if len(text) <= budget_chars:
        return text
    marker = TRUNCATION_MARKER
    cut_at = max(0, budget_chars - len(marker))
    trimmed = text[:cut_at].rstrip()
    if "\n" in trimmed:
        trimmed = trimmed.rsplit("\n", 1)[0]
    return trimmed + marker


def _wiki_query_pointer() -> str:
    if (SCRIPTS_DIR / "wiki_query.py").exists():
        return (
            "Use `uv run python scripts/wiki_query.py` to search the wiki and "
            "retrieve relevant article excerpts on demand."
        )
    return (
        "Read full wiki articles from `wiki/` on demand when a topic needs depth — "
        "this injection is navigation only."
    )


def index_navigation(
    max_chars: int = INDEX_NAV_MAX_CHARS,
    *,
    wiki_index_path: Path | None = None,
) -> str:
    """Return compact index navigation: category headings and one-line summaries."""
    index_path = wiki_index_path or WIKI_INDEX
    if not index_path.exists():
        return ""

    raw = index_path.read_text()
    if not raw.strip() or "No articles yet" in raw:
        return ""

    lines: list[str] = []
    in_footer = False

    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("> **Last updated"):
            in_footer = True
        if in_footer:
            continue
        if stripped.startswith("# Wiki Index"):
            continue
        if stripped.startswith(">") and not _WIKILINK_RE.search(stripped):
            continue
        if stripped.startswith("---"):
            continue
        if stripped.startswith("## How to Read"):
            continue
        if "_No articles yet" in stripped or "_No connection articles yet" in stripped:
            continue

        is_heading = stripped.startswith("## ") or stripped.startswith("### ")
        has_wikilink = bool(_WIKILINK_RE.search(stripped))
        if is_heading or has_wikilink:
            lines.append(line.rstrip())

    if not lines:
        return ""

    pointer = _wiki_query_pointer()
    body = "\n".join(lines)
    body = _truncate_text(body, max(0, max_chars - len(pointer) - 2), per_section=True)
    return f"{body}\n\n{pointer}" if body else ""


def _daily_head_excerpt(content: str, max_chars: int = DAILY_EXCERPT_CHARS) -> str:
    content = content.strip()
    if not content:
        return ""

    lines = content.splitlines()
    excerpt_lines: list[str] = []
    for line in lines:
        if line.startswith("## ") and excerpt_lines:
            break
        excerpt_lines.append(line)
        if len("\n".join(excerpt_lines)) >= max_chars:
            break

    excerpt = "\n".join(excerpt_lines).strip()
    if len(excerpt) > max_chars:
        excerpt = _truncate_text(excerpt, max_chars, per_section=False)
    elif len(content) > len(excerpt):
        excerpt += "\n[...truncated]"
    return excerpt


def recent_activity(
    days: int = DAILY_LOOKBACK_DAYS,
    max_chars: int = DAILY_ACTIVITY_MAX_CHARS,
    *,
    daily_dir: Path | None = None,
) -> str:
    """Return short head excerpts from the most recent daily logs."""
    logs_dir = daily_dir or DAILY_DIR
    if not logs_dir.exists():
        return ""

    log_files = sorted(logs_dir.glob("*.md"), reverse=True)[:days]
    if not log_files:
        return ""

    combined: list[str] = []
    total_chars = 0

    for log_file in log_files:
        content = log_file.read_text()
        excerpt = _daily_head_excerpt(content)
        if not excerpt:
            continue
        block = f"--- {log_file.stem} ---\n{excerpt}"
        if total_chars + len(block) > max_chars:
            remaining = max_chars - total_chars
            if remaining > 40:
                block = _truncate_text(block, remaining, per_section=False)
                combined.append(block)
            break
        combined.append(block)
        total_chars += len(block) + 2

    return "\n\n".join(combined)


def build_session_context(
    budget_chars: int = INJECT_BUDGET_CHARS,
    *,
    overview_path: Path | None = None,
    memory_path: Path | None = None,
    wiki_index_path: Path | None = None,
    daily_dir: Path | None = None,
) -> str:
    """Assemble tiered session context markdown (no JSON envelope)."""
    parts: list[str] = []

    overview_file = overview_path or OVERVIEW_FILE
    if overview_file.exists():
        overview = overview_file.read_text().strip()
        if has_meaningful_context(overview, "overview"):
            overview = _truncate_text(overview, OVERVIEW_MAX_CHARS)
            parts.append(f"## Business Overview\n\n{overview}")

    memory_file = memory_path or MEMORY_FILE
    if memory_file.exists():
        memory = memory_file.read_text().strip()
        if has_meaningful_context(memory, "memory"):
            memory = _truncate_text(memory, MEMORY_MAX_CHARS)
            parts.append(f"## Memory\n\n{memory}")

    wiki_nav = index_navigation(wiki_index_path=wiki_index_path)
    if wiki_nav:
        parts.append(f"## Wiki Index\n\n{wiki_nav}")

    # Company mode: also surface the local-only private wiki so the founder's
    # own connections keep appearing at session start. Teammates never have a
    # private/ tree (it is gitignored), so this is a no-op for them.
    if wiki_index_path is None and get_mode() == "company":
        private_nav = index_navigation(wiki_index_path=PRIVATE_WIKI_INDEX)
        if private_nav:
            parts.append(f"## Private Wiki Index (local only)\n\n{private_nav}")

    activity = recent_activity(daily_dir=daily_dir)
    if activity:
        parts.append(f"## Recent Session Logs\n\n{activity}")

    if not parts:
        return ""

    combined = "\n\n---\n\n".join(parts)
    return _apply_total_budget(combined, budget_chars)


def main() -> None:
    print(build_session_context())


if __name__ == "__main__":
    main()