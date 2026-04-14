#!/usr/bin/env python3
"""
ARC Wiki Compiler

Reads daily session logs and compiles them into structured wiki articles.
Uses the Claude Agent SDK with full file tools so the agent can directly
read existing articles, create new ones, edit, and update the index.

Can be triggered:
- Automatically by flush.py after each session
- Manually via: uv run python scripts/compile.py
- With flags: --all (recompile everything), --file daily/2026-04-11.md (specific file)
"""

from __future__ import annotations

# Recursion prevention: set BEFORE imports that might trigger Claude
import os
os.environ["ARC_HOOK_INVOKED"] = "1"

import argparse
import asyncio
import json
import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

DAILY_DIR = PROJECT_ROOT / "daily"
WIKI_DIR = PROJECT_ROOT / "wiki"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
STATE_FILE = SCRIPTS_DIR / "state.json"
LOG_FILE = SCRIPTS_DIR / "compile.log"

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [compile] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def file_hash(path: Path) -> str:
    from hashlib import sha256
    return sha256(path.read_bytes()).hexdigest()[:16]


def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_state(state: dict) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def list_daily_logs() -> list[Path]:
    if not DAILY_DIR.exists():
        return []
    return sorted(DAILY_DIR.glob("*.md"))


def now_iso() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


LOCK_FILE = SCRIPTS_DIR / "compile.lock"
LOCK_TIMEOUT = 300  # 5 minutes — if lock is older, assume stale


def acquire_lock() -> bool:
    """Try to acquire the compile lock. Returns False if another compile is running."""
    import time
    if LOCK_FILE.exists():
        try:
            lock_age = time.time() - LOCK_FILE.stat().st_mtime
            if lock_age < LOCK_TIMEOUT:
                return False  # another compile is running
            # Stale lock — remove it
            logging.info("Removing stale lock (%.0fs old)", lock_age)
        except OSError:
            pass
    LOCK_FILE.write_text(str(os.getpid()), encoding="utf-8")
    return True


def release_lock():
    """Release the compile lock."""
    LOCK_FILE.unlink(missing_ok=True)


async def compile_daily_log(log_path: Path, state: dict) -> float:
    """Compile a single daily log into knowledge articles.

    The agent gets full file tools and multiple turns to:
    - Read existing wiki articles
    - Create new concept/connection articles
    - Update existing articles with new information
    - Update wiki/index.md
    - Append to wiki/log.md
    - Cross-reference everything with [[wikilinks]]

    Returns the API cost of the compilation.
    """
    from claude_agent_sdk import (
        AssistantMessage,
        ClaudeAgentOptions,
        ResultMessage,
        TextBlock,
        query,
    )

    log_content = log_path.read_text(encoding="utf-8")

    prompt = f"""You are a knowledge compiler for an ARC workspace. Your job is to read a daily
conversation log and compile durable knowledge into wiki articles.

## Daily Log to Compile

**File:** {log_path.name}

{log_content}

## Your Task

1. Read `wiki/index.md` to see what articles already exist
2. Read relevant existing articles to understand what's already documented
3. Extract key concepts, decisions, lessons, and connections from the daily log
4. For each piece of durable knowledge:
   - If a relevant article exists: UPDATE it with new information
   - If no article exists: CREATE a new one in `wiki/concepts/`
   - If the log reveals non-obvious connections between 2+ concepts: CREATE a connection article in `wiki/connections/`
5. Update `wiki/index.md` with any new articles
6. Append a timestamped entry to `wiki/log.md`

## Article Format

Every wiki article must use this format:

```markdown
---
title: [Name]
type: concept | entity | connection | exploration
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
source: conversation | setup | import | exploration
tags: [comma-separated]
---

# [Name]

[Content with [[wikilinks]] to related articles]

## Related
- [[Related Article 1]]
- [[Related Article 2]]
```

## Rules
- **NEVER modify files in `daily/` — they are immutable inputs. Only write to `wiki/`.**
- Use [[wikilinks]] throughout — every mention of a concept that has its own article should link to it
- Keep articles atomic — one concept per file
- File names: kebab-case (e.g., `business-model.md`, `sales-process.md`)
- Only compile knowledge worth keeping long-term — skip trivial exchanges
- If the daily log contains nothing NEW worth compiling, just say so and stop
- This daily log may contain sessions that were already compiled earlier today.
  Read existing wiki articles first — if content is already captured, skip it.
  Only compile genuinely new knowledge that isn't already in the wiki.

## Quality Standards
- Every article must link to at least 2 other articles via [[wikilinks]]
- Connection articles must reference 2+ concept articles
- Update the Related section of any article you link TO (bidirectional linking)
"""

    cost = 0.0
    logging.info("Compiling %s...", log_path.name)

    try:
        async for message in query(
            prompt=prompt,
            options=ClaudeAgentOptions(
                cwd=str(PROJECT_ROOT),
                system_prompt={"type": "preset", "preset": "claude_code"},
                allowed_tools=["Read", "Write", "Edit", "Glob", "Grep"],
                permission_mode="acceptEdits",
                max_turns=30,
            ),
        ):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        pass  # agent writes files directly
            elif isinstance(message, ResultMessage):
                cost = message.total_cost_usd or 0.0
                logging.info("Compilation cost: $%.4f", cost)
    except Exception as e:
        import traceback
        logging.error("Compile error: %s\n%s", e, traceback.format_exc())
        return 0.0

    # Update state
    rel_path = log_path.name
    state.setdefault("ingested", {})[rel_path] = {
        "hash": file_hash(log_path),
        "compiled_at": now_iso(),
        "cost_usd": cost,
    }
    state["total_cost"] = state.get("total_cost", 0.0) + cost
    save_state(state)

    logging.info("Compiled %s successfully.", log_path.name)
    return cost


def main():
    parser = argparse.ArgumentParser(description="ARC Wiki Compiler")
    parser.add_argument("--all", action="store_true", help="Force recompile all logs")
    parser.add_argument("--file", type=str, help="Compile a specific daily log file")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be compiled")
    args = parser.parse_args()

    state = load_state()

    # Determine which files to compile
    if args.file:
        target = Path(args.file)
        if not target.is_absolute():
            target = DAILY_DIR / target.name
        if not target.exists():
            target = PROJECT_ROOT / args.file
        if not target.exists():
            print(f"Error: {args.file} not found")
            sys.exit(1)
        to_compile = [target]
    else:
        all_logs = list_daily_logs()
        if args.all:
            to_compile = all_logs
        else:
            to_compile = []
            for log_path in all_logs:
                rel = log_path.name
                prev = state.get("ingested", {}).get(rel, {})
                if not prev or prev.get("hash") != file_hash(log_path):
                    to_compile.append(log_path)

    if not to_compile:
        logging.info("Nothing to compile — all daily logs are up to date.")
        print("Nothing to compile - all daily logs are up to date.")
        return

    if args.dry_run:
        print(f"[DRY RUN] Files to compile ({len(to_compile)}):")
        for f in to_compile:
            print(f"  - {f.name}")
        return

    # Acquire lock to prevent concurrent compilations
    if not acquire_lock():
        logging.info("Another compilation is running — skipping.")
        print("Another compilation is running — skipping.")
        return

    try:
        logging.info("Compiling %d daily log(s)...", len(to_compile))

        total_cost = 0.0
        for i, log_path in enumerate(to_compile, 1):
            print(f"[{i}/{len(to_compile)}] Compiling {log_path.name}...")
            cost = asyncio.run(compile_daily_log(log_path, state))
            total_cost += cost

        logging.info("Compilation complete. Total cost: $%.2f", total_cost)
        print(f"\nCompilation complete. Total cost: ${total_cost:.2f}")
    finally:
        release_lock()


if __name__ == "__main__":
    main()
