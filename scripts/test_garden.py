#!/usr/bin/env python3
"""Tests for scripts/garden.py — stdlib only, safe on blank workspaces."""

from __future__ import annotations

import shutil
import sys
import tempfile
from datetime import date, timedelta
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.garden import GardenPaths, collect_articles, run_garden  # noqa: E402


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def assert_equal(actual, expected, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def test_blank_wiki_writes_nothing_to_garden_yet() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        wiki_dir = Path(tmp) / "wiki"
        wiki_dir.mkdir()
        daily_dir = Path(tmp) / "daily"
        daily_dir.mkdir()
        paths = GardenPaths(wiki_dir=wiki_dir, daily_dir=daily_dir, wiki_log=wiki_dir / "log.md")

        output = run_garden(paths, date_str="2099-01-01")
        content = output.read_text(encoding="utf-8")

        assert_true(output.exists(), "draft file should exist for blank wiki")
        assert_true(
            "nothing to garden yet" in content.lower(),
            "blank wiki draft should say nothing to garden yet",
        )
        assert_equal(collect_articles(paths), {}, "blank wiki should have no articles")


def test_stale_and_orphan_articles_in_draft() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        wiki_dir = Path(tmp) / "wiki"
        concepts = wiki_dir / "concepts"
        concepts.mkdir(parents=True)
        daily_dir = Path(tmp) / "daily"
        daily_dir.mkdir()

        stale_date = (date.today() - timedelta(days=90)).isoformat()
        stale_path = concepts / "stale-topic.md"
        stale_path.write_text(
            f"""---
title: Stale Topic
type: concept
created: 2023-01-01
updated: {stale_date}
tags: test
---

# Stale Topic

This article has not been refreshed recently.
""",
            encoding="utf-8",
        )

        orphan_path = concepts / "orphan-note.md"
        orphan_path.write_text(
            """---
title: Orphan Note
type: concept
created: 2026-06-01
updated: 2026-06-01
tags: test
---

# Orphan Note

No other article links here.
""",
            encoding="utf-8",
        )

        linked_path = concepts / "hub-article.md"
        linked_path.write_text(
            """---
title: Hub Article
type: concept
created: 2026-06-01
updated: 2026-06-01
tags: test
---

# Hub Article

See [[stale-topic]] for background.
""",
            encoding="utf-8",
        )

        stale_before = stale_path.read_text(encoding="utf-8")
        orphan_before = orphan_path.read_text(encoding="utf-8")
        linked_before = linked_path.read_text(encoding="utf-8")

        paths = GardenPaths(wiki_dir=wiki_dir, daily_dir=daily_dir, wiki_log=wiki_dir / "log.md")
        output = run_garden(paths, date_str="2099-06-24", today=date(2026, 6, 24))
        content = output.read_text(encoding="utf-8")

        assert_true(output.name == "garden-2099-06-24.md", "draft should use provided date")
        assert_true("## Archive" in content, "draft should have Archive section")
        assert_true("## Re-link" in content, "draft should have Re-link section")
        assert_true("stale-topic" in content, "draft should mention stale article")
        assert_true("orphan-note" in content, "draft should mention orphan article")

        archive_pos = content.index("## Archive")
        relink_pos = content.index("## Re-link")
        stale_pos = content.index("stale-topic")
        orphan_pos = content.index("orphan-note")
        assert_true(
            archive_pos < stale_pos < relink_pos,
            "stale article should appear under Archive before Re-link section",
        )
        assert_true(
            relink_pos < orphan_pos,
            "orphan article should appear under Re-link",
        )

        assert_equal(stale_path.read_text(encoding="utf-8"), stale_before, "stale article untouched")
        assert_equal(orphan_path.read_text(encoding="utf-8"), orphan_before, "orphan article untouched")
        assert_equal(linked_path.read_text(encoding="utf-8"), linked_before, "linked article untouched")


def main() -> int:
    tests = [
        test_blank_wiki_writes_nothing_to_garden_yet,
        test_stale_and_orphan_articles_in_draft,
    ]
    for test in tests:
        test()
        print(f"ok {test.__name__}")
    print(f"All {len(tests)} tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())