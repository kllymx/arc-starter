#!/usr/bin/env python3
"""
ARC Wiki Compiler

Reads daily session logs and compiles them into structured wiki articles.
This is the "heavy" operation that promotes raw conversation knowledge into
the cross-referenced wiki.

Can be triggered:
- Automatically by session-end.py after COMPILE_AFTER_HOUR
- Manually via: uv run python scripts/compile.py
- With flags: --all (recompile everything), --file daily/2026-04-11.md (specific file)
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

# Recursion prevention
os.environ["ARC_HOOK_INVOKED"] = "1"

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.config import (
    DAILY_DIR,
    WIKI_DIR,
    WIKI_INDEX,
    WIKI_LOG,
    CONCEPTS_DIR,
    CONNECTIONS_DIR,
)
from scripts.utils import (
    load_state,
    save_state,
    sha256,
    now_str,
    today_str,
)

GUARD_VAR = "ARC_HOOK_INVOKED"

COMPILE_PROMPT = """You are an expert knowledge compiler for a founder's AI operating partner.

You are given:
1. The current wiki index (catalog of all existing articles)
2. All existing wiki articles (so you know what's already documented)
3. A daily session log containing summaries of conversations

Your job is to extract durable knowledge from the session log and either:
- CREATE new wiki articles for concepts, entities, or connections not yet documented
- UPDATE existing articles with new information
- FLAG contradictions where new info conflicts with existing articles

## Rules

- Every article MUST use this format:

```markdown
---
title: [Name]
type: concept | entity | connection
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
source: conversation
tags: [comma-separated]
---

# [Name]

[Content with [[wikilinks]] to related articles]

## Related
- [[Related 1]]
- [[Related 2]]
```

- Use [[wikilinks]] throughout — every mention of a concept that has its own article should link to it
- Connection articles go in wiki/connections/ and must link to 2+ concept articles
- Concept articles go in wiki/concepts/
- Keep articles atomic — one concept per file
- File names should be kebab-case: `business-model.md`, `sales-process.md`

## Output Format

Return a JSON object with this structure:

```json
{
  "created": [
    {"path": "wiki/concepts/example.md", "content": "full markdown content"},
  ],
  "updated": [
    {"path": "wiki/concepts/existing.md", "content": "full updated markdown content"},
  ],
  "index_update": "full updated wiki/index.md content",
  "log_entry": "## [date] compile | Description\\n- Created: ...\\n- Updated: ...",
  "contradictions": ["description of any contradictions found"]
}
```

If there is nothing worth compiling from the session log, return:
```json
{"skip": true, "reason": "No new durable knowledge found"}
```
"""


async def compile_daily_log(log_path: Path, dry_run: bool = False):
    """Compile a single daily log into wiki articles."""
    if not log_path.exists():
        print(f"Log file not found: {log_path}")
        return

    log_content = log_path.read_text()
    if not log_content.strip():
        return

    # Load current wiki state
    wiki_index = WIKI_INDEX.read_text() if WIKI_INDEX.exists() else ""

    existing_articles = []
    for article_dir in [CONCEPTS_DIR, CONNECTIONS_DIR]:
        if article_dir.exists():
            for article_file in article_dir.glob("*.md"):
                existing_articles.append(
                    f"--- {article_file.relative_to(WIKI_DIR)} ---\n{article_file.read_text()}"
                )

    existing_content = "\n\n".join(existing_articles) if existing_articles else "(no articles yet)"

    # Build the prompt
    full_prompt = f"""## Current Wiki Index

{wiki_index}

## Existing Wiki Articles

{existing_content}

## Daily Session Log to Compile

{log_content}

---

Now compile the session log into wiki articles. Return JSON as specified."""

    from scripts.config import llm_summarize
    import json

    try:
        os.environ[GUARD_VAR] = "1"

        result_text = await llm_summarize(full_prompt, COMPILE_PROMPT)

        # Extract JSON from response (handle markdown code blocks)
        json_text = result_text
        if "```json" in json_text:
            json_text = json_text.split("```json")[1].split("```")[0]
        elif "```" in json_text:
            json_text = json_text.split("```")[1].split("```")[0]

        result = json.loads(json_text.strip())

        if result.get("skip"):
            print(f"Skipped {log_path.name}: {result.get('reason', 'no new knowledge')}")
            return

        if dry_run:
            print(f"DRY RUN — Would create {len(result.get('created', []))} articles, "
                  f"update {len(result.get('updated', []))}")
            for item in result.get("created", []):
                print(f"  CREATE: {item['path']}")
            for item in result.get("updated", []):
                print(f"  UPDATE: {item['path']}")
            return

        # Write created articles
        for item in result.get("created", []):
            file_path = PROJECT_ROOT / item["path"]
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(item["content"])
            print(f"  Created: {item['path']}")

        # Write updated articles
        for item in result.get("updated", []):
            file_path = PROJECT_ROOT / item["path"]
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(item["content"])
            print(f"  Updated: {item['path']}")

        # Update index
        if result.get("index_update"):
            WIKI_INDEX.write_text(result["index_update"])
            print("  Updated: wiki/index.md")

        # Append to log
        if result.get("log_entry"):
            with open(WIKI_LOG, "a") as f:
                f.write(f"\n{result['log_entry']}\n")
            print("  Appended to: wiki/log.md")

        # Report contradictions
        for contradiction in result.get("contradictions", []):
            print(f"  CONTRADICTION: {contradiction}")

        # Update state
        state = load_state()
        state["compiled_hashes"][log_path.name] = sha256(log_content)
        state["last_compile_time"] = now_str()
        save_state(state)

        print(f"Compiled {log_path.name} successfully.")

    except Exception as e:
        print(f"Compile error for {log_path.name}: {e}", file=sys.stderr)


async def main():
    parser = argparse.ArgumentParser(description="ARC Wiki Compiler")
    parser.add_argument("--all", action="store_true", help="Recompile all daily logs")
    parser.add_argument("--file", type=str, help="Compile a specific daily log file")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing")
    args = parser.parse_args()

    if args.file:
        await compile_daily_log(Path(args.file), dry_run=args.dry_run)
        return

    if not DAILY_DIR.exists():
        print("No daily/ directory found.")
        return

    state = load_state()
    compiled_hashes = state.get("compiled_hashes", {})

    log_files = sorted(DAILY_DIR.glob("*.md"))
    if not log_files:
        print("No daily logs to compile.")
        return

    for log_file in log_files:
        content = log_file.read_text()
        current_hash = sha256(content)

        if not args.all and compiled_hashes.get(log_file.name) == current_hash:
            print(f"Skipping {log_file.name} (unchanged)")
            continue

        print(f"Compiling {log_file.name}...")
        await compile_daily_log(log_file, dry_run=args.dry_run)


if __name__ == "__main__":
    asyncio.run(main())
