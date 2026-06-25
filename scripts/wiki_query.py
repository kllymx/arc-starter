#!/usr/bin/env python3
"""
Targeted wiki retrieval for ARC.

Ranks wiki articles by keyword overlap (no embeddings) and returns compact
markdown with paths, summaries, and excerpts agents can act on.

Usage:
    uv run python scripts/wiki_query.py "<query>" [--k 5] [--full]

Scoring (deterministic; higher = more relevant):
1. Query terms are lowercased and split on non-alphanumeric boundaries (min length 2).
2. Per-article field weights (matching term count × weight):
   - title: 5
   - frontmatter tags: 4
   - index one-line summary (from wiki/index.md): 3
   - body text: 1
3. Index proximity boost: +2 per query term found in the article's index section
   (section heading plus sibling index lines in the same ## block).
4. Tie-break: relative path ascending (alphabetical).
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.config import (  # noqa: E402
    CONNECTIONS_DIR,
    CONCEPTS_DIR,
    PRIVATE_CONCEPTS_DIR,
    PRIVATE_CONNECTIONS_DIR,
    PRIVATE_QA_DIR,
    PRIVATE_WIKI_DIR,
    PROJECT_ROOT as CONFIG_PROJECT_ROOT,
    WIKI_DIR,
    WIKI_INDEX,
    get_mode,
)

LOG_FILE = PROJECT_ROOT / "scripts" / "wiki_query.log"

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [wiki_query] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

QA_DIR = WIKI_DIR / "qa"

TERM_SPLIT = re.compile(r"[^a-z0-9]+")
WIKILINK_PATTERN = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
INDEX_ENTRY = re.compile(
    r"^\s*-\s*\[\[([^\]|]+)(?:\|[^\]]+)?\]\]\s*[—\-]\s*(.+?)\s*$",
    re.MULTILINE,
)

WEIGHT_TITLE = 5
WEIGHT_TAGS = 4
WEIGHT_INDEX_SUMMARY = 3
WEIGHT_BODY = 1
WEIGHT_INDEX_PROXIMITY = 2

BLANK_MESSAGE = (
    "No wiki articles yet. Run /setup to populate the knowledge base."
)


@dataclass(frozen=True)
class WikiPaths:
    """Filesystem roots for wiki retrieval (overridable in tests).

    `extra_dirs` holds additional article directories searched alongside the
    shared wiki. In company mode the default() factory adds the local-only
    `private/wiki/` directories here so the founder's retrieval spans their
    whole brain. The private tier is gitignored, so a teammate's clone has no
    `private/` dirs and simply searches the shared wiki only.
    """

    wiki_dir: Path
    concepts_dir: Path
    connections_dir: Path
    qa_dir: Path
    wiki_index: Path
    project_root: Path
    extra_dirs: tuple[Path, ...] = ()

    @classmethod
    def default(cls) -> WikiPaths:
        # Only fold in the local private tier in company mode — that's the only
        # mode where the private/shared split is meaningful. In personal mode the
        # founder's knowledge lives in wiki/ and private/ may not be used.
        extra: tuple[Path, ...] = ()
        if get_mode() == "company" and PRIVATE_WIKI_DIR.exists():
            extra = (PRIVATE_CONCEPTS_DIR, PRIVATE_CONNECTIONS_DIR, PRIVATE_QA_DIR)
        return cls(
            wiki_dir=WIKI_DIR,
            concepts_dir=CONCEPTS_DIR,
            connections_dir=CONNECTIONS_DIR,
            qa_dir=QA_DIR,
            wiki_index=WIKI_INDEX,
            project_root=CONFIG_PROJECT_ROOT,
            extra_dirs=extra,
        )


@dataclass
class WikiHit:
    path: Path
    title: str
    summary: str
    score: float
    excerpt: str
    full_text: str


def tokenize(text: str) -> list[str]:
    return [t for t in TERM_SPLIT.split(text.lower()) if len(t) >= 2]


def normalize_slug(value: str) -> str:
    return value.strip().lower().replace(" ", "-")


def parse_frontmatter(content: str) -> tuple[dict[str, str], str]:
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    meta: dict[str, str] = {}
    for line in parts[1].strip().splitlines():
        if ":" not in line:
            continue
        key, _, raw = line.partition(":")
        meta[key.strip().lower()] = raw.strip()

    return meta, parts[2].lstrip("\n")


def parse_tags(meta: dict[str, str]) -> str:
    raw = meta.get("tags", "")
    if not raw:
        return ""
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        raw = raw[1:-1]
    return raw.replace(",", " ")


def parse_index(index_text: str) -> tuple[dict[str, str], dict[str, str]]:
    """
    Return (slug -> summary, slug -> section text) from wiki/index.md.
    Section text includes the ## heading and all lines until the next ##.
    """
    summaries: dict[str, str] = {}
    sections: dict[str, str] = {}
    current_section = ""
    section_lines: list[str] = []

    def flush_section() -> None:
        nonlocal current_section, section_lines
        if not current_section:
            return
        section_blob = "\n".join(section_lines)
        for match in INDEX_ENTRY.finditer(section_blob):
            slug = normalize_slug(match.group(1))
            summaries[slug] = match.group(2).strip()
            sections[slug] = section_blob
        section_lines = []

    for line in index_text.splitlines():
        if line.startswith("## "):
            flush_section()
            current_section = line[3:].strip()
            section_lines = [line]
            continue
        if current_section:
            section_lines.append(line)

    flush_section()
    return summaries, sections


def count_term_hits(terms: list[str], text: str) -> int:
    if not terms or not text:
        return 0
    lowered = text.lower()
    return sum(lowered.count(term) for term in terms)


def extract_excerpt(body: str, terms: list[str], window: int = 2) -> str:
    lines = [ln for ln in body.splitlines() if ln.strip()]
    if not lines:
        return ""

    best_idx = 0
    best_score = -1
    for idx, line in enumerate(lines):
        score = count_term_hits(terms, line)
        if score > best_score:
            best_score = score
            best_idx = idx

    if best_score <= 0:
        snippet = lines[: min(3, len(lines))]
        return "\n".join(snippet)

    start = max(0, best_idx - window)
    end = min(len(lines), best_idx + window + 1)
    return "\n".join(lines[start:end])


def iter_article_paths(paths: WikiPaths) -> list[Path]:
    articles: list[Path] = []
    search_dirs = (paths.concepts_dir, paths.connections_dir, paths.qa_dir)
    search_dirs += tuple(paths.extra_dirs)
    for article_dir in search_dirs:
        if not article_dir.exists():
            continue
        articles.extend(sorted(article_dir.glob("*.md")))
    return articles


def score_article(
    path: Path,
    content: str,
    terms: list[str],
    index_summaries: dict[str, str],
    index_sections: dict[str, str],
) -> tuple[float, str, str, str]:
    meta, body = parse_frontmatter(content)
    slug = normalize_slug(path.stem)
    title = meta.get("title") or path.stem.replace("-", " ").title()
    tags_text = parse_tags(meta)
    index_summary = index_summaries.get(slug, "")
    summary = index_summary or meta.get("summary", "") or title

    score = 0.0
    score += count_term_hits(terms, title) * WEIGHT_TITLE
    score += count_term_hits(terms, tags_text) * WEIGHT_TAGS
    score += count_term_hits(terms, index_summary) * WEIGHT_INDEX_SUMMARY
    score += count_term_hits(terms, body) * WEIGHT_BODY

    section_text = index_sections.get(slug, "")
    if section_text:
        for term in terms:
            if term in section_text.lower():
                score += WEIGHT_INDEX_PROXIMITY

    excerpt = extract_excerpt(body, terms)
    return score, title, summary, excerpt


def query_wiki(
    query: str,
    k: int = 5,
    paths: WikiPaths | None = None,
) -> list[WikiHit]:
    """Return top-k wiki hits for a query, highest score first."""
    if not query.strip():
        return []

    paths = paths or WikiPaths.default()
    terms = tokenize(query)
    if not terms:
        return []

    index_text = paths.wiki_index.read_text() if paths.wiki_index.exists() else ""
    index_summaries, index_sections = parse_index(index_text)

    hits: list[WikiHit] = []
    for article_path in iter_article_paths(paths):
        content = article_path.read_text()
        score, title, summary, excerpt = score_article(
            article_path,
            content,
            terms,
            index_summaries,
            index_sections,
        )
        if score <= 0:
            continue
        hits.append(
            WikiHit(
                path=article_path,
                title=title,
                summary=summary,
                score=score,
                excerpt=excerpt,
                full_text=content,
            )
        )

    hits.sort(key=lambda h: (-h.score, str(h.path)))
    return hits[:k]


def format_results(
    query: str,
    hits: list[WikiHit],
    *,
    full: bool = False,
    paths: WikiPaths | None = None,
) -> str:
    paths = paths or WikiPaths.default()
    if not hits:
        return BLANK_MESSAGE

    lines = [f'# Wiki query: "{query}"', ""]
    lines.append(f"Found {len(hits)} article(s).")
    lines.append("")

    for idx, hit in enumerate(hits, start=1):
        try:
            rel_path = hit.path.relative_to(paths.project_root)
        except ValueError:
            rel_path = hit.path

        lines.append(f"## {idx}. {hit.path.stem} — {hit.title}")
        lines.append(f"**Path:** `{rel_path}`")
        lines.append(f"**Summary:** {hit.summary}")
        lines.append(f"**Score:** {hit.score:g}")
        lines.append("")

        if full:
            lines.append(hit.full_text.rstrip())
        elif hit.excerpt:
            lines.append("**Excerpt:**")
            lines.append("```")
            lines.append(hit.excerpt.rstrip())
            lines.append("```")

        lines.append("")
        lines.append("---")
        lines.append("")

    if lines and lines[-1] == "":
        lines.pop()
    if lines and lines[-1] == "---":
        lines.pop()
    if lines and lines[-1] == "":
        lines.pop()

    return "\n".join(lines)


def run_query(
    query: str,
    k: int = 5,
    full: bool = False,
    paths: WikiPaths | None = None,
) -> str:
    hits = query_wiki(query, k=k, paths=paths)
    return format_results(query, hits, full=full, paths=paths)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Search the ARC wiki and return compact, ranked markdown."
    )
    parser.add_argument("query", help="Search terms")
    parser.add_argument(
        "--k",
        type=int,
        default=5,
        help="Maximum number of articles to return (default: 5)",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Print full article bodies instead of excerpts",
    )
    args = parser.parse_args(argv)

    if args.k < 1:
        print("--k must be at least 1", file=sys.stderr)
        return 1

    output = run_query(args.query, k=args.k, full=args.full)
    print(output)
    logging.info("query=%r k=%d hits_chars=%d", args.query, args.k, len(output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())