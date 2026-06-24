"""
Link pass — proposes verified wikilinks and MOCs as a draft.

Scans wiki articles and recent daily logs, builds an index of real article
titles/slugs, proposes new [[wikilinks]] only to verified targets, and
suggests MOC files for thematic clusters. Never edits existing articles.

Usage:
    uv run python scripts/link_pass.py
"""

from __future__ import annotations

import logging
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.config import PROJECT_ROOT, WIKI_DIR  # noqa: E402
from scripts.utils import today_str  # noqa: E402

LOG_FILE = ROOT / "scripts" / "link-pass.log"
MIN_CLUSTER_SIZE = 3
MIN_ARTICLES_FOR_PASS = 2

WIKILINK_PATTERN = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
FRONTMATTER_PATTERN = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TITLE_PATTERN = re.compile(r"^title:\s*(.+?)\s*$", re.MULTILINE)
TAGS_PATTERN = re.compile(r"^tags:\s*(.+?)\s*$", re.MULTILINE)
INDEX_WIKILINK_PATTERN = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [link_pass] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


@dataclass
class Article:
    slug: str
    path: Path
    title: str
    tags: set[str] = field(default_factory=set)
    existing_links: set[str] = field(default_factory=set)


@dataclass
class LinkProposal:
    source_slug: str
    source_path: Path
    target_slug: str
    target_title: str
    context: str
    source_kind: str = "article"


@dataclass
class MocProposal:
    cluster_slug: str
    cluster_title: str
    articles: list[Article]
    shared_tags: list[str]


@dataclass
class BacklinkProposal:
    source_slug: str
    source_path: Path
    target_slug: str
    target_title: str


@dataclass
class LinkPassResult:
    draft_path: Path | None
    draft_content: str
    link_proposals: list[LinkProposal]
    moc_proposals: list[MocProposal]
    backlink_proposals: list[BacklinkProposal]
    skipped_unverified: list[str]


def normalize_slug(value: str) -> str:
    return value.strip().lower().replace(" ", "-")


def parse_frontmatter_field(content: str, pattern: re.Pattern[str]) -> str | None:
    match = FRONTMATTER_PATTERN.search(content)
    if not match:
        return None
    field_match = pattern.search(match.group(1))
    if not field_match:
        return None
    return field_match.group(1).strip()


def parse_tags(content: str) -> set[str]:
    raw = parse_frontmatter_field(content, TAGS_PATTERN)
    if not raw:
        return set()
    return {tag.strip().lower() for tag in raw.split(",") if tag.strip()}


def extract_wikilinks(content: str) -> set[str]:
    return {normalize_slug(link) for link in WIKILINK_PATTERN.findall(content)}


def strip_frontmatter(content: str) -> str:
    return FRONTMATTER_PATTERN.sub("", content, count=1)


def article_dirs(wiki_dir: Path) -> list[Path]:
    return [
        wiki_dir / "concepts",
        wiki_dir / "connections",
        wiki_dir / "qa",
    ]


def load_articles(wiki_dir: Path, wiki_index: Path | None = None) -> dict[str, Article]:
    articles: dict[str, Article] = {}
    index_titles: dict[str, str] = {}

    index_path = wiki_index or (wiki_dir / "index.md")
    if index_path.exists():
        for slug, display in INDEX_WIKILINK_PATTERN.findall(index_path.read_text()):
            index_titles[normalize_slug(slug)] = (display or slug).strip()

    for article_dir in article_dirs(wiki_dir):
        if not article_dir.exists():
            continue
        for path in sorted(article_dir.glob("*.md")):
            content = path.read_text(encoding="utf-8")
            slug = path.stem
            title = parse_frontmatter_field(content, TITLE_PATTERN) or index_titles.get(
                normalize_slug(slug), slug.replace("-", " ").title()
            )
            articles[slug] = Article(
                slug=slug,
                path=path,
                title=title,
                tags=parse_tags(content),
                existing_links=extract_wikilinks(content),
            )

    return articles


def resolve_target(slug_or_title: str, articles: dict[str, Article]) -> Article | None:
    normalized = normalize_slug(slug_or_title)
    if normalized in articles:
        return articles[normalized]
    for article in articles.values():
        if normalize_slug(article.title) == normalized:
            return article
    return None


def verify_link_target(target: str, articles: dict[str, Article]) -> Article | None:
    article = resolve_target(target, articles)
    if article is None:
        logging.info("Skipped unverified link target: %s", target)
    return article


def _mention_patterns(article: Article) -> list[re.Pattern[str]]:
    patterns = [
        re.compile(rf"\b{re.escape(article.title)}\b", re.IGNORECASE),
        re.compile(
            rf"\b{re.escape(article.slug.replace('-', ' '))}\b",
            re.IGNORECASE,
        ),
    ]
    return patterns


def find_mention_context(text: str, article: Article) -> str | None:
    for pattern in _mention_patterns(article):
        match = pattern.search(text)
        if match:
            start = max(0, match.start() - 40)
            end = min(len(text), match.end() + 40)
            snippet = text[start:end].replace("\n", " ").strip()
            return f"...{snippet}..."
    return None


def scan_text_for_links(
    text: str,
    source_slug: str,
    source_path: Path,
    articles: dict[str, Article],
    source_kind: str = "article",
) -> tuple[list[LinkProposal], list[str]]:
    proposals: list[LinkProposal] = []
    skipped: list[str] = []

    cleaned = strip_frontmatter(text)
    cleaned = WIKILINK_PATTERN.sub(" ", cleaned)

    for target_slug, target in articles.items():
        if target_slug == source_slug:
            continue
        if target_slug in extract_wikilinks(text):
            continue

        context = find_mention_context(cleaned, target)
        if not context:
            continue

        verified = verify_link_target(target_slug, articles)
        if verified is None:
            skipped.append(target_slug)
            continue

        proposals.append(
            LinkProposal(
                source_slug=source_slug,
                source_path=source_path,
                target_slug=verified.slug,
                target_title=verified.title,
                context=context,
                source_kind=source_kind,
            )
        )

    return proposals, skipped


def find_link_proposals(
    articles: dict[str, Article],
    daily_dir: Path,
) -> tuple[list[LinkProposal], list[str]]:
    proposals: list[LinkProposal] = []
    skipped: list[str] = []

    for slug, article in articles.items():
        content = article.path.read_text(encoding="utf-8")
        found, skipped_targets = scan_text_for_links(
            content,
            slug,
            article.path,
            articles,
            source_kind="article",
        )
        proposals.extend(found)
        skipped.extend(skipped_targets)

    if daily_dir.exists():
        for daily_path in sorted(daily_dir.glob("*.md"), reverse=True)[:7]:
            content = daily_path.read_text(encoding="utf-8")
            found, skipped_targets = scan_text_for_links(
                content,
                daily_path.stem,
                daily_path,
                articles,
                source_kind="daily",
            )
            proposals.extend(found)
            skipped.extend(skipped_targets)

    deduped: dict[tuple[str, str, str], LinkProposal] = {}
    for proposal in proposals:
        key = (proposal.source_kind, proposal.source_slug, proposal.target_slug)
        deduped[key] = proposal

    return list(deduped.values()), skipped


def detect_moc_clusters(articles: dict[str, Article]) -> list[MocProposal]:
    tag_to_articles: dict[str, list[Article]] = defaultdict(list)
    for article in articles.values():
        for tag in article.tags:
            tag_to_articles[tag].append(article)

    proposals: list[MocProposal] = []
    seen_slugs: set[str] = set()

    for tag, cluster in sorted(tag_to_articles.items()):
        if len(cluster) < MIN_CLUSTER_SIZE:
            continue
        cluster_slug = normalize_slug(tag)
        if cluster_slug in seen_slugs:
            continue
        seen_slugs.add(cluster_slug)
        proposals.append(
            MocProposal(
                cluster_slug=cluster_slug,
                cluster_title=tag.replace("-", " ").title(),
                articles=sorted(cluster, key=lambda item: item.slug),
                shared_tags=[tag],
            )
        )

    return proposals


def find_backlink_fixes(articles: dict[str, Article]) -> list[BacklinkProposal]:
    proposals: list[BacklinkProposal] = []

    for source_slug, source in articles.items():
        content = source.path.read_text(encoding="utf-8")
        for link_slug in extract_wikilinks(content):
            target = articles.get(link_slug)
            if target is None:
                continue
            if source_slug in target.existing_links:
                continue
            proposals.append(
                BacklinkProposal(
                    source_slug=source_slug,
                    source_path=source.path,
                    target_slug=target.slug,
                    target_title=target.title,
                )
            )

    return proposals


def render_moc_content(proposal: MocProposal) -> str:
    links = "\n".join(
        f"- [[{article.slug}|{article.title}]]"
        for article in proposal.articles
    )
    return f"""---
title: {proposal.cluster_title}
type: moc
created: {today_str()}
updated: {today_str()}
source: link-pass
tags: {", ".join(proposal.shared_tags)}
---

# {proposal.cluster_title}

Curated map of related articles sharing the `{proposal.shared_tags[0]}` theme.

## Core articles
{links}
"""


def render_draft(
    link_proposals: list[LinkProposal],
    moc_proposals: list[MocProposal],
    backlink_proposals: list[BacklinkProposal],
    skipped_unverified: list[str],
    *,
    insufficient_articles: bool,
) -> str:
    date = today_str()
    if insufficient_articles:
        return f"""# Link Pass Draft — {date}

> Generated by `/link`. **Not yet applied.** To apply: tell me which proposals to keep.
> To skip everything: delete this file.

## Summary

Not enough articles to link yet. Add at least {MIN_ARTICLES_FOR_PASS} wiki articles,
then run `/link` again.

## Add-link proposals

_None — insufficient articles._

## New-MOC proposals

_None — insufficient articles._

## Backlink-fix proposals

_None — insufficient articles._
"""

    lines = [
        f"# Link Pass Draft — {date}",
        "",
        "> Generated by `/link`. **Not yet applied.** To apply: tell me which proposals",
        "> to keep. To skip everything: delete this file.",
        "",
        "## Summary",
        f"- {len(link_proposals)} add-link proposals",
        f"- {len(moc_proposals)} new-MOC proposals",
        f"- {len(backlink_proposals)} backlink-fix proposals",
        "",
    ]

    if skipped_unverified:
        lines.extend(
            [
                f"- {len(skipped_unverified)} unverified mentions skipped",
                "",
            ]
        )

    lines.extend(["## Add-link proposals", ""])
    if link_proposals:
        for index, proposal in enumerate(link_proposals, start=1):
            rel_path = proposal.source_path
            lines.extend(
                [
                    f"### Proposal {index}",
                    f"**Source ({proposal.source_kind}):** `{rel_path}`",
                    f"**Add:** `[[{proposal.target_title}]]` → resolves to `{proposal.target_slug}`",
                    f"**Context:** {proposal.context}",
                    "**Suggested placement:** `## Related` section or inline at first mention",
                    "",
                ]
            )
    else:
        lines.extend(["_No new verified links proposed._", ""])

    lines.extend(["## New-MOC proposals", ""])
    if moc_proposals:
        for proposal in moc_proposals:
            rel_moc = f"wiki/mocs/{proposal.cluster_slug}.md"
            lines.extend(
                [
                    f"### MOC: {proposal.cluster_title}",
                    f"**Path:** `{rel_moc}`",
                    f"**Shared tags:** {', '.join(proposal.shared_tags)}",
                    "**Articles:** "
                    + ", ".join(f"[[{item.title}]]" for item in proposal.articles),
                    "",
                    "**Proposed content:**",
                    "",
                    "```markdown",
                    render_moc_content(proposal).rstrip(),
                    "```",
                    "",
                ]
            )
    else:
        lines.extend(["_No thematic clusters large enough for a MOC yet._", ""])

    lines.extend(["## Backlink-fix proposals", ""])
    if backlink_proposals:
        for index, proposal in enumerate(backlink_proposals, start=1):
            lines.extend(
                [
                    f"### Backlink {index}",
                    f"**Target:** `wiki/concepts/{proposal.target_slug}.md` (or connections/)",
                    f"**Add to `## Related`:** `[[{proposal.source_slug}]]`",
                    f"**Because:** `{proposal.source_path}` already links to [[{proposal.target_title}]]",
                    "",
                ]
            )
    else:
        lines.extend(["_No missing backlinks detected._", ""])

    return "\n".join(lines).rstrip() + "\n"


def run_link_pass(
    *,
    project_root: Path | None = None,
    wiki_dir: Path | None = None,
    daily_dir: Path | None = None,
    wiki_index: Path | None = None,
    output_path: Path | None = None,
    write_draft: bool = True,
) -> LinkPassResult:
    root = project_root or PROJECT_ROOT
    wiki = wiki_dir or (root / "wiki")
    daily = daily_dir or (root / "daily")
    index_path = wiki_index or (wiki / "index.md")

    articles = load_articles(wiki, index_path)
    insufficient = len(articles) < MIN_ARTICLES_FOR_PASS

    link_proposals: list[LinkProposal] = []
    moc_proposals: list[MocProposal] = []
    backlink_proposals: list[BacklinkProposal] = []
    skipped: list[str] = []

    if not insufficient:
        link_proposals, skipped = find_link_proposals(articles, daily)
        moc_proposals = detect_moc_clusters(articles)
        backlink_proposals = find_backlink_fixes(articles)

    draft_content = render_draft(
        link_proposals,
        moc_proposals,
        backlink_proposals,
        skipped,
        insufficient_articles=insufficient,
    )

    draft_path = output_path or (wiki / f"link-pass-{today_str()}.md")
    if write_draft:
        wiki.mkdir(parents=True, exist_ok=True)
        draft_path.write_text(draft_content, encoding="utf-8")
        logging.info("Wrote link pass draft to %s", draft_path)

    return LinkPassResult(
        draft_path=draft_path if write_draft else None,
        draft_content=draft_content,
        link_proposals=link_proposals,
        moc_proposals=moc_proposals,
        backlink_proposals=backlink_proposals,
        skipped_unverified=skipped,
    )


def main() -> int:
    try:
        result = run_link_pass()
        print(result.draft_content)
        return 0
    except Exception:
        logging.exception("Link pass failed")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())