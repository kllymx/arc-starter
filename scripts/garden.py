#!/usr/bin/env python3
"""
ARC Garden — lightweight wiki maintenance draft generator.

Performs structural hygiene checks (staleness, orphans, weak links, sparse
notes, daily promote candidates) and writes a review draft to
wiki/garden-{YYYY-MM-DD}.md. Never modifies existing wiki articles.

Usage: uv run python scripts/garden.py [--wiki-dir PATH] [--daily-dir PATH]
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.config import (  # noqa: E402
    CONNECTIONS_DIR,
    CONCEPTS_DIR,
    DAILY_DIR,
    WIKI_DIR,
    WIKI_LOG,
)
from scripts.lint import (  # noqa: E402
    check_missing_backlinks,
    check_orphan_pages,
    check_sparse_articles,
)
from scripts.utils import load_state, today_str  # noqa: E402

LOG_FILE = PROJECT_ROOT / "scripts" / "garden.log"

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [garden] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

STALE_THRESHOLD_DAYS = 60
SPARSE_WORD_THRESHOLD = 200
RECENT_DAILY_DAYS = 30

FRONTMATTER_DATE_RE = re.compile(
    r"^---\s*\n(?:.*\n)*?"
    r"(?:updated|created):\s*(\d{4}-\d{2}-\d{2})",
    re.MULTILINE,
)
UPDATED_RE = re.compile(r"^updated:\s*(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)
CREATED_RE = re.compile(r"^created:\s*(\d{4}-\d{2}-\d{2})\s*$", re.MULTILINE)


@dataclass(frozen=True)
class GardenPaths:
    wiki_dir: Path
    daily_dir: Path
    wiki_log: Path

    @property
    def concepts_dir(self) -> Path:
        return self.wiki_dir / "concepts"

    @property
    def connections_dir(self) -> Path:
        return self.wiki_dir / "connections"

    @property
    def qa_dir(self) -> Path:
        return self.wiki_dir / "qa"


def default_paths() -> GardenPaths:
    return GardenPaths(wiki_dir=WIKI_DIR, daily_dir=DAILY_DIR, wiki_log=WIKI_LOG)


def collect_articles(paths: GardenPaths) -> dict[str, Path]:
    """Collect wiki articles as {stem: path} from concepts/, connections/, and qa/."""
    articles: dict[str, Path] = {}
    for article_dir in (paths.concepts_dir, paths.connections_dir, paths.qa_dir):
        if article_dir.exists():
            for path in article_dir.glob("*.md"):
                articles[path.stem] = path
    return articles


def _parse_date(value: str) -> date | None:
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None


def article_last_updated(path: Path, *, today: date | None = None) -> date | None:
    """Return the best available updated/created date from frontmatter."""
    content = path.read_text(encoding="utf-8")
    updated_match = UPDATED_RE.search(content)
    if updated_match:
        return _parse_date(updated_match.group(1))
    created_match = CREATED_RE.search(content)
    if created_match:
        return _parse_date(created_match.group(1))
    return None


def find_stale_articles(
    articles: dict[str, Path],
    *,
    threshold_days: int = STALE_THRESHOLD_DAYS,
    today: date | None = None,
) -> list[tuple[str, Path, int]]:
    """Return (title, path, days_since_update) for articles older than threshold."""
    reference = today or date.today()
    stale: list[tuple[str, Path, int]] = []
    for title, path in sorted(articles.items()):
        last_updated = article_last_updated(path, today=reference)
        if last_updated is None:
            continue
        age_days = (reference - last_updated).days
        if age_days >= threshold_days:
            stale.append((title, path, age_days))
    return stale


def find_promote_candidates(paths: GardenPaths) -> list[str]:
    """Surface recent daily logs not yet compiled into the wiki."""
    candidates: list[str] = []
    if not paths.daily_dir.exists():
        return candidates

    state = load_state()
    compiled_hashes = state.get("compiled_hashes", {})
    cutoff = date.today() - timedelta(days=RECENT_DAILY_DAYS)

    for daily_path in sorted(paths.daily_dir.glob("*.md")):
        try:
            log_date = datetime.strptime(daily_path.stem, "%Y-%m-%d").date()
        except ValueError:
            continue
        if log_date < cutoff:
            continue
        if daily_path.name not in compiled_hashes:
            candidates.append(f"daily/{daily_path.name}")
    return candidates


def _relative_wiki_path(path: Path, wiki_dir: Path) -> str:
    try:
        return str(path.relative_to(wiki_dir)).replace("\\", "/")
    except ValueError:
        return str(path)


def _parse_lint_title(issue: str, prefix: str) -> str | None:
    if not issue.startswith(prefix):
        return None
    return issue[len(prefix) :].strip()


def build_draft_content(
    paths: GardenPaths,
    *,
    date_str: str | None = None,
    today: date | None = None,
) -> str:
    """Build the garden draft markdown body."""
    draft_date = date_str or today_str()
    reference = today or date.today()
    articles = collect_articles(paths)

    if not articles:
        return (
            f"# Garden Draft — {draft_date}\n\n"
            "> Generated by `/garden`. **Not yet applied.** To apply: tell me which\n"
            "> checklist items to keep. To skip everything: delete this file.\n\n"
            "Nothing to garden yet — no wiki articles found. Run `/setup` to build "
            "the wiki, or `/reflect` after your next session.\n"
        )

    archive_items: list[str] = []
    for title, path, age_days in find_stale_articles(
        articles, today=reference
    ):
        rel = _relative_wiki_path(path, paths.wiki_dir)
        archive_items.append(
            f"- [ ] **{title}** — `{rel}` — last updated {age_days} days ago "
            f"(>{STALE_THRESHOLD_DAYS}-day threshold); consider archiving or refreshing"
        )

    relink_items: list[str] = []
    for issue in check_orphan_pages(articles):
        title = _parse_lint_title(issue, "Orphan page (no inbound links):")
        if title:
            path = articles[title]
            rel = _relative_wiki_path(path, paths.wiki_dir)
            relink_items.append(
                f"- [ ] **{title}** — `{rel}` — no inbound [[wikilinks]]; "
                "add links from index or related articles"
            )

    for issue in check_missing_backlinks(articles):
        relink_items.append(
            f"- [ ] **Weak link** — {issue}; add reciprocal [[wikilinks]]"
        )

    promote_items: list[str] = []
    for daily_ref in find_promote_candidates(paths):
        promote_items.append(
            f"- [ ] **{daily_ref}** — recent daily log not yet compiled; "
            "review for durable insights worth promoting to the wiki"
        )

    prune_items: list[str] = []
    for issue in check_sparse_articles(articles, min_words=SPARSE_WORD_THRESHOLD):
        title = _parse_lint_title(issue, "Sparse article (")
        if title:
            # title is like "45 words): foo" — extract article name
            match = re.match(r"\d+ words\): (.+)$", title)
            article_title = match.group(1) if match else title
            if article_title in articles:
                path = articles[article_title]
                rel = _relative_wiki_path(path, paths.wiki_dir)
                word_count = len(path.read_text(encoding="utf-8").split())
                prune_items.append(
                    f"- [ ] **{article_title}** — `{rel}` — {word_count} words "
                    f"(<{SPARSE_WORD_THRESHOLD}); low-signal stub — prune or flesh out"
                )

    lines = [
        f"# Garden Draft — {draft_date}",
        "",
        "> Generated by `/garden`. **Not yet applied.** To apply: tell me which",
        "> checklist items to keep. To skip everything: delete this file.",
        "",
        "## Summary",
        f"- {len(archive_items)} archive candidates",
        f"- {len(relink_items)} re-link candidates",
        f"- {len(promote_items)} promote candidates",
        f"- {len(prune_items)} prune candidates",
        "",
        "---",
        "",
        "## Archive",
    ]
    lines.extend(archive_items or ["- _None detected._"])
    lines.extend(["", "## Re-link"])
    lines.extend(relink_items or ["- _None detected._"])
    lines.extend(["", "## Promote"])
    lines.extend(promote_items or ["- _None detected._"])
    lines.extend(["", "## Prune"])
    lines.extend(prune_items or ["- _None detected._"])
    lines.append("")
    return "\n".join(lines)


def draft_path(paths: GardenPaths, date_str: str | None = None) -> Path:
    return paths.wiki_dir / f"garden-{date_str or today_str()}.md"


def run_garden(
    paths: GardenPaths | None = None,
    *,
    date_str: str | None = None,
    today: date | None = None,
) -> Path:
    """Run structural garden pass and write the draft. Returns draft path."""
    resolved = paths or default_paths()
    resolved.wiki_dir.mkdir(parents=True, exist_ok=True)
    content = build_draft_content(resolved, date_str=date_str, today=today)
    output = draft_path(resolved, date_str=date_str)
    output.write_text(content, encoding="utf-8")
    logging.info("Wrote garden draft to %s", output)
    return output


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ARC Garden — wiki maintenance draft")
    parser.add_argument(
        "--wiki-dir",
        type=Path,
        default=None,
        help="Override wiki directory (for tests)",
    )
    parser.add_argument(
        "--daily-dir",
        type=Path,
        default=None,
        help="Override daily directory (for tests)",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="Draft date suffix YYYY-MM-DD (default: today)",
    )
    args = parser.parse_args(argv)

    if args.wiki_dir:
        paths = GardenPaths(
            wiki_dir=args.wiki_dir.resolve(),
            daily_dir=(args.daily_dir or args.wiki_dir.parent / "daily").resolve(),
            wiki_log=args.wiki_dir.resolve() / "log.md",
        )
    else:
        paths = default_paths()
        if args.daily_dir:
            paths = GardenPaths(
                wiki_dir=paths.wiki_dir,
                daily_dir=args.daily_dir.resolve(),
                wiki_log=paths.wiki_log,
            )

    output = run_garden(paths, date_str=args.date)
    print(f"Garden draft written to {output.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())