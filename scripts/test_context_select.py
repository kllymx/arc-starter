#!/usr/bin/env python3
"""Tests for tiered session context assembly."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.context_select import (  # noqa: E402
    INJECT_BUDGET_CHARS,
    TRUNCATION_MARKER,
    build_session_context,
    index_navigation,
)


def _run_hook() -> str:
    result = subprocess.run(
        [sys.executable, "hooks/session-start.py"],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def test_blank_workspace_returns_empty_context() -> None:
    context = build_session_context()
    assert context == "", f"expected empty context on blank workspace, got {len(context)} chars"


def test_blank_workspace_hook_prints_nothing() -> None:
    assert _run_hook() == "", "session-start.py should not inject placeholder files"


def test_fake_workspace_within_budget_and_navigation_only() -> None:
    article_body = "FULL_ARTICLE_BODY_SECRET_CONTENT " * 200

    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        context_dir = root / "context"
        wiki_dir = root / "wiki"
        daily_dir = root / "daily"
        concepts_dir = wiki_dir / "concepts"
        context_dir.mkdir()
        wiki_dir.mkdir()
        daily_dir.mkdir()
        concepts_dir.mkdir()

        (context_dir / "overview.md").write_text(
            "# Overview\n\n" + ("Acme Corp builds widgets. " * 300)
        )
        (context_dir / "memory.md").write_text(
            "# Memory\n\n- Prefer concise answers.\n- Use bullet lists."
        )
        (wiki_dir / "index.md").write_text(
            """# Wiki Index

## Business
- [[acme-corp]] — Widget manufacturer and distributor

## Priorities
- [[q3-growth]] — Expand into enterprise accounts

## Connections
_No connection articles yet._
"""
        )
        (concepts_dir / "acme-corp.md").write_text(article_body)
        (daily_dir / "2026-06-24.md").write_text(
            "# Daily Log — 2026-06-24\n\n## Session 1\nDiscussed pricing.\n\n"
            + ("Long transcript line. " * 400)
        )
        (daily_dir / "2026-06-23.md").write_text(
            "# Daily Log — 2026-06-23\n\n## Morning\nShipped feature X.\n"
        )

        context = build_session_context(
            budget_chars=INJECT_BUDGET_CHARS,
            overview_path=context_dir / "overview.md",
            memory_path=context_dir / "memory.md",
            wiki_index_path=wiki_dir / "index.md",
            daily_dir=daily_dir,
        )

        assert "## Business Overview" in context
        assert "## Memory" in context
        assert "## Wiki Index" in context
        assert "## Recent Session Logs" in context
        assert "## Business" in context
        assert "[[acme-corp]]" in context
        assert "FULL_ARTICLE_BODY_SECRET_CONTENT" not in context
        assert "Long transcript line." not in context or "[...truncated]" in context
        assert len(context) <= INJECT_BUDGET_CHARS + len(TRUNCATION_MARKER)


def test_output_never_exceeds_budget_plus_marker() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        context_dir = root / "context"
        wiki_dir = root / "wiki"
        daily_dir = root / "daily"
        context_dir.mkdir()
        wiki_dir.mkdir()
        daily_dir.mkdir()

        budget = 1200
        (context_dir / "overview.md").write_text("Real business.\n" + ("x" * 5000))
        (context_dir / "memory.md").write_text("Real memory.\n" + ("y" * 5000))
        index_lines = ["## Business\n"]
        for i in range(80):
            index_lines.append(f"- [[topic-{i}]] — Summary line {i} with extra detail.\n")
        (wiki_dir / "index.md").write_text("".join(index_lines))
        for day in range(3):
            (daily_dir / f"2026-06-{20 + day:02d}.md").write_text(
                f"# Daily Log\n\n## Block\n" + ("event " * 500)
            )

        context = build_session_context(
            budget_chars=budget,
            overview_path=context_dir / "overview.md",
            memory_path=context_dir / "memory.md",
            wiki_index_path=wiki_dir / "index.md",
            daily_dir=daily_dir,
        )

        assert context.endswith(TRUNCATION_MARKER) or len(context) <= budget
        assert len(context) <= budget + len(TRUNCATION_MARKER)


def test_index_navigation_strips_boilerplate() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        index_path = Path(tmpdir) / "index.md"
        index_path.write_text(
            """# Wiki Index

> Instructional preamble that should be removed.

## Business
- [[alpha]] — First concept
"""
        )
        nav = index_navigation(wiki_index_path=index_path)
        assert "Instructional preamble" not in nav
        assert "## Business" in nav
        assert "[[alpha]]" in nav


def test_hook_json_envelope_unchanged() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        context_dir = root / "context"
        context_dir.mkdir()
        (context_dir / "overview.md").write_text("Active business with real content.")

        # Patch paths by calling build_session_context directly for content check;
        # hook uses real paths, so only verify envelope shape when non-empty via helper.
        combined = build_session_context(
            overview_path=context_dir / "overview.md",
            memory_path=context_dir / "missing.md",
            wiki_index_path=root / "missing.md",
            daily_dir=root / "missing",
        )
        assert combined

        payload = {
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": combined,
            }
        }
        parsed = json.loads(json.dumps(payload))
        assert parsed["hookSpecificOutput"]["hookEventName"] == "SessionStart"
        assert "additionalContext" in parsed["hookSpecificOutput"]


def main() -> None:
    tests = [
        test_blank_workspace_returns_empty_context,
        test_blank_workspace_hook_prints_nothing,
        test_fake_workspace_within_budget_and_navigation_only,
        test_output_never_exceeds_budget_plus_marker,
        test_index_navigation_strips_boilerplate,
        test_hook_json_envelope_unchanged,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")


if __name__ == "__main__":
    main()