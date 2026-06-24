#!/usr/bin/env python3
"""Tests for scripts/link_pass.py (stdlib-only)."""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.link_pass import run_link_pass  # noqa: E402


def _write_article(
    concepts_dir: Path,
    slug: str,
    *,
    title: str,
    body: str,
    tags: str = "",
) -> None:
    tag_line = f"tags: {tags}\n" if tags else ""
    concepts_dir.mkdir(parents=True, exist_ok=True)
    concepts_dir.joinpath(f"{slug}.md").write_text(
        f"""---
title: {title}
type: concept
created: 2026-06-24
updated: 2026-06-24
source: test
{tag_line}---

# {title}

{body}

## Related
""",
        encoding="utf-8",
    )


def test_verified_link_proposed_and_unverified_skipped() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        wiki = root / "wiki"
        concepts = wiki / "concepts"
        daily = root / "daily"

        _write_article(
            concepts,
            "pricing",
            title="Pricing",
            body="Our pricing model for SaaS.",
            tags="revenue",
        )
        _write_article(
            concepts,
            "business-model",
            title="Business Model",
            body=(
                "We need to revisit Pricing before launch. "
                "Also considering PhantomFeature that does not exist yet."
            ),
            tags="strategy",
        )

        result = run_link_pass(
            project_root=root,
            wiki_dir=wiki,
            daily_dir=daily,
            output_path=wiki / "link-pass-test.md",
        )

        assert "[[Pricing]]" in result.draft_content
        assert any(
            proposal.target_title == "Pricing"
            for proposal in result.link_proposals
        )
        assert "PhantomFeature" not in result.draft_content
        assert "[[PhantomFeature]]" not in result.draft_content


def test_tag_cluster_proposes_moc() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        wiki = root / "wiki"
        concepts = wiki / "concepts"

        for slug, title in [
            ("growth-loop", "Growth Loop"),
            ("channel-strategy", "Channel Strategy"),
            ("retention-playbook", "Retention Playbook"),
        ]:
            _write_article(
                concepts,
                slug,
                title=title,
                body=f"Notes about {title.lower()}.",
                tags="go-to-market",
            )

        result = run_link_pass(
            project_root=root,
            wiki_dir=wiki,
            daily_dir=root / "daily",
            output_path=wiki / "link-pass-test.md",
        )

        assert result.moc_proposals, "Expected a MOC proposal for shared-tag cluster"
        assert "wiki/mocs/go-to-market.md" in result.draft_content
        assert "## New-MOC proposals" in result.draft_content


def test_blank_wiki_exits_cleanly() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        wiki = root / "wiki"
        wiki.mkdir(parents=True)

        result = run_link_pass(
            project_root=root,
            wiki_dir=wiki,
            daily_dir=root / "daily",
            output_path=wiki / "link-pass-test.md",
            write_draft=True,
        )

        assert "not enough articles to link yet" in result.draft_content.lower()
        assert result.link_proposals == []
        assert result.moc_proposals == []


def test_blank_workspace_repo_does_not_crash() -> None:
    """Ensure the real repo wiki (often blank) does not crash the pass."""
    wiki_dir = ROOT / "wiki"
    draft_path = wiki_dir / "link-pass-test-blank.md"
    try:
        result = run_link_pass(
            project_root=ROOT,
            wiki_dir=wiki_dir,
            daily_dir=ROOT / "daily",
            output_path=draft_path,
        )
        assert result.draft_content
    finally:
        if draft_path.exists():
            draft_path.unlink()


def main() -> int:
    tests = [
        test_verified_link_proposed_and_unverified_skipped,
        test_tag_cluster_proposes_moc,
        test_blank_wiki_exits_cleanly,
        test_blank_workspace_repo_does_not_crash,
    ]

    for test in tests:
        test()
        print(f"ok {test.__name__}")

    print(f"All {len(tests)} tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())