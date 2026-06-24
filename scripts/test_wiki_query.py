#!/usr/bin/env python3
"""Stdlib-only tests for wiki_query retrieval."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.wiki_query import (  # noqa: E402
    BLANK_MESSAGE,
    WikiPaths,
    query_wiki,
    run_query,
)


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def assert_equal(actual, expected, message: str) -> None:
    if actual != expected:
        raise AssertionError(f"{message}: expected {expected!r}, got {actual!r}")


def write_article(path: Path, title: str, tags: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"""---
title: {title}
type: concept
tags: {tags}
---

# {title}

{body}
"""
    )


def build_temp_wiki(root: Path) -> WikiPaths:
    wiki = root / "wiki"
    concepts = wiki / "concepts"
    connections = wiki / "connections"
    qa = wiki / "qa"
    for directory in (concepts, connections, qa):
        directory.mkdir(parents=True)

    write_article(
        concepts / "revenue-model.md",
        "Revenue Model",
        "pricing, revenue, saas",
        "Our recurring revenue comes from subscription tiers.\n"
        "Enterprise deals close through direct sales.",
    )
    write_article(
        concepts / "team-lunch.md",
        "Team Lunch",
        "culture, social",
        "We order pizza on Fridays for the team.",
    )
    write_article(
        qa / "pricing-faq.md",
        "Pricing FAQ",
        "pricing, customers",
        "Customers often ask about annual billing discounts.",
    )

    index = wiki / "index.md"
    index.write_text(
        """# Wiki Index

## Business

- [[revenue-model]] — How we make money from subscriptions
- [[team-lunch]] — Friday pizza tradition

## Q&A

- [[pricing-faq]] — Common customer pricing questions
"""
    )

    return WikiPaths(
        wiki_dir=wiki,
        concepts_dir=concepts,
        connections_dir=connections,
        qa_dir=qa,
        wiki_index=index,
        project_root=root,
    )


def test_ranking_and_excerpts() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        paths = build_temp_wiki(Path(tmp))
        hits = query_wiki("revenue subscription", k=3, paths=paths)

        assert_true(len(hits) >= 1, "expected at least one hit")
        assert_equal(
            hits[0].path.stem,
            "revenue-model",
            "most relevant article should rank first",
        )
        assert_true(hits[0].excerpt.strip(), "excerpt should be non-empty")
        assert_true("subscription" in hits[0].excerpt.lower(), "excerpt should match query")


def test_blank_temp_wiki() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        wiki = root / "wiki"
        concepts = wiki / "concepts"
        connections = wiki / "connections"
        qa = wiki / "qa"
        for directory in (concepts, connections, qa):
            directory.mkdir(parents=True)

        paths = WikiPaths(
            wiki_dir=wiki,
            concepts_dir=concepts,
            connections_dir=connections,
            qa_dir=qa,
            wiki_index=wiki / "index.md",
            project_root=root,
        )
        hits = query_wiki("anything", paths=paths)
        assert_equal(hits, [], "empty wiki should return no hits")
        output = run_query("anything", paths=paths)
        assert_equal(output, BLANK_MESSAGE, "blank wiki message")


def test_blank_workspace_cli() -> None:
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "wiki_query.py"), "test"],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert_equal(result.returncode, 0, "blank workspace CLI exit code")
    assert_true(BLANK_MESSAGE in result.stdout, "blank workspace CLI message")
    assert_true(not result.stderr.strip(), "blank workspace should not error on stderr")


def main() -> int:
    test_ranking_and_excerpts()
    test_blank_temp_wiki()
    test_blank_workspace_cli()
    print("All wiki_query tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())