#!/usr/bin/env python3
"""
ARC Wiki Linter

Performs health checks on the wiki to ensure accuracy, completeness,
and proper cross-referencing.

Usage: uv run python scripts/lint.py [--structural-only]
"""

import argparse
import re
import sys
from pathlib import Path
from collections import defaultdict

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.config import (
    WIKI_DIR,
    CONCEPTS_DIR,
    CONNECTIONS_DIR,
    DAILY_DIR,
    IMPORTS_DIR,
    WIKI_LOG,
)
from scripts.utils import today_str


WIKILINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")


def get_all_articles() -> dict[str, Path]:
    """Get all wiki articles as {title: path} mapping."""
    articles = {}
    for article_dir in [CONCEPTS_DIR, CONNECTIONS_DIR]:
        if article_dir.exists():
            for f in article_dir.glob("*.md"):
                # Title is the filename without extension
                title = f.stem
                articles[title] = f
    return articles


def extract_wikilinks(content: str) -> list[str]:
    """Extract all [[wikilink]] targets from content."""
    return WIKILINK_PATTERN.findall(content)


def check_broken_links(articles: dict[str, Path]) -> list[str]:
    """Find wikilinks that point to non-existent articles."""
    issues = []
    article_titles = set(articles.keys())

    for title, path in articles.items():
        content = path.read_text()
        links = extract_wikilinks(content)
        for link in links:
            # Normalize link target to kebab-case filename
            link_normalized = link.lower().replace(" ", "-")
            if link_normalized not in article_titles and link not in article_titles:
                issues.append(f"Broken link: [[{link}]] in {path.relative_to(WIKI_DIR)}")

    return issues


def check_orphan_pages(articles: dict[str, Path]) -> list[str]:
    """Find articles with zero inbound links."""
    inbound_counts = defaultdict(int)

    for title, path in articles.items():
        content = path.read_text()
        links = extract_wikilinks(content)
        for link in links:
            link_normalized = link.lower().replace(" ", "-")
            inbound_counts[link_normalized] += 1

    orphans = []
    for title in articles:
        if inbound_counts.get(title, 0) == 0:
            orphans.append(f"Orphan page (no inbound links): {title}")

    return orphans


def check_unprocessed_sources() -> list[str]:
    """Check for imports and daily logs not yet processed."""
    issues = []

    # Check wiki log for what's been ingested
    processed_files = set()
    if WIKI_LOG.exists():
        log_content = WIKI_LOG.read_text()
        # Simple heuristic: look for filenames mentioned in log
        processed_files = set(re.findall(r"(?:imports|daily)/[\w\-\.]+", log_content))

    # Check imports
    if IMPORTS_DIR.exists():
        for f in IMPORTS_DIR.iterdir():
            if f.is_file() and not f.name.startswith("."):
                ref = f"imports/{f.name}"
                if ref not in processed_files:
                    issues.append(f"Unprocessed import: {f.name}")

    # Check daily logs
    if DAILY_DIR.exists():
        from scripts.utils import load_state
        state = load_state()
        compiled_hashes = state.get("compiled_hashes", {})
        for f in DAILY_DIR.glob("*.md"):
            if f.name not in compiled_hashes:
                issues.append(f"Uncompiled daily log: {f.name}")

    return issues


def check_sparse_articles(articles: dict[str, Path], min_words: int = 200) -> list[str]:
    """Find articles under the minimum word count."""
    issues = []
    for title, path in articles.items():
        content = path.read_text()
        word_count = len(content.split())
        if word_count < min_words:
            issues.append(f"Sparse article ({word_count} words): {title}")
    return issues


def check_missing_backlinks(articles: dict[str, Path]) -> list[str]:
    """Find asymmetric links (A links to B but B doesn't link to A)."""
    issues = []
    links_map = {}

    for title, path in articles.items():
        content = path.read_text()
        links = extract_wikilinks(content)
        links_map[title] = set(link.lower().replace(" ", "-") for link in links)

    for title, outbound in links_map.items():
        for target in outbound:
            if target in links_map:
                if title not in links_map[target]:
                    issues.append(
                        f"Missing backlink: {target} does not link back to {title}"
                    )

    return issues


def main():
    parser = argparse.ArgumentParser(description="ARC Wiki Linter")
    parser.add_argument(
        "--structural-only",
        action="store_true",
        help="Skip LLM-based contradiction checks (free, fast)",
    )
    args = parser.parse_args()

    articles = get_all_articles()

    if not articles:
        print("No wiki articles found. Run /setup to build the wiki.")
        return

    print(f"Linting {len(articles)} wiki articles...\n")

    all_issues = {
        "broken_links": check_broken_links(articles),
        "orphan_pages": check_orphan_pages(articles),
        "unprocessed": check_unprocessed_sources(),
        "sparse": check_sparse_articles(articles),
        "missing_backlinks": check_missing_backlinks(articles),
    }

    # Print report
    total_issues = sum(len(v) for v in all_issues.values())

    print(f"## Wiki Health Report — {today_str()}\n")
    print(f"### Summary")
    print(f"- Total articles: {len(articles)}")
    print(f"- Broken links: {len(all_issues['broken_links'])}")
    print(f"- Orphan pages: {len(all_issues['orphan_pages'])}")
    print(f"- Unprocessed sources: {len(all_issues['unprocessed'])}")
    print(f"- Sparse articles: {len(all_issues['sparse'])}")
    print(f"- Missing backlinks: {len(all_issues['missing_backlinks'])}")
    print()

    if total_issues == 0:
        print("Wiki is healthy. No issues found.")
    else:
        print(f"### Issues ({total_issues} total)\n")
        for category, issues in all_issues.items():
            if issues:
                print(f"#### {category.replace('_', ' ').title()}")
                for issue in issues:
                    print(f"- {issue}")
                print()

    if not args.structural_only:
        print("\nNote: Contradiction checks require LLM analysis.")
        print("Run /lint in your agent session for full analysis.")


if __name__ == "__main__":
    main()
