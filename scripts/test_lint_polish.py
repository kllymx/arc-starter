#!/usr/bin/env python3
"""Tests for lint provenance and staleness checks (Lane G)."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.lint import (
    STALE_DAYS_THRESHOLD,
    check_missing_provenance,
    check_stale_articles,
)


def make_article(path: Path, frontmatter: str, body: str = "# Test\n\nContent here.\n") -> None:
    path.write_text(f"---\n{frontmatter}\n---\n\n{body}")


def test_stale_articles() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        concepts = Path(tmp) / "concepts"
        concepts.mkdir()

        old_date = (date.today() - timedelta(days=STALE_DAYS_THRESHOLD + 1)).isoformat()
        recent_date = date.today().isoformat()

        stale_path = concepts / "old-article.md"
        fresh_path = concepts / "fresh-article.md"
        no_date_path = concepts / "no-date.md"

        make_article(
            stale_path,
            f"title: Old\ntype: concept\ncreated: 2024-01-01\nupdated: {old_date}\nsource: conversation",
        )
        make_article(
            fresh_path,
            f"title: Fresh\ntype: concept\ncreated: 2024-01-01\nupdated: {recent_date}\nsource: conversation",
        )
        make_article(
            no_date_path,
            "title: No Date\ntype: concept\ncreated: 2024-01-01\nsource: conversation",
        )

        articles = {
            "old-article": stale_path,
            "fresh-article": fresh_path,
            "no-date": no_date_path,
        }

        issues = check_stale_articles(articles)
        assert any("old-article" in issue for issue in issues), issues
        assert not any("fresh-article" in issue for issue in issues), issues
        assert not any("no-date" in issue for issue in issues), issues


def test_missing_provenance() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        concepts = Path(tmp) / "concepts"
        concepts.mkdir()

        missing_path = concepts / "no-source.md"
        present_path = concepts / "has-source.md"

        make_article(
            missing_path,
            "title: No Source\ntype: concept\ncreated: 2024-01-01\nupdated: 2024-01-01",
        )
        make_article(
            present_path,
            "title: Has Source\ntype: concept\ncreated: 2024-01-01\nupdated: 2024-01-01\nsource: setup",
        )

        articles = {
            "no-source": missing_path,
            "has-source": present_path,
        }

        issues = check_missing_provenance(articles)
        assert any("no-source" in issue for issue in issues), issues
        assert not any("has-source" in issue for issue in issues), issues


def test_blank_wiki_path_unchanged() -> None:
    result = subprocess.run(
        ["python3", "scripts/lint.py", "--structural-only"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    assert "No wiki articles found. Run /setup to build the wiki." in result.stdout


def main() -> None:
    tests = [
        test_stale_articles,
        test_missing_provenance,
        test_blank_wiki_path_unchanged,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")


if __name__ == "__main__":
    main()