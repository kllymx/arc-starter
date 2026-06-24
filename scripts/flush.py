"""
Memory flush agent - extracts important knowledge from conversation context.

Spawned by session-end.py or pre-compact.py as a background process. Reads
pre-extracted conversation context from a .md file, uses the Claude Agent SDK
to decide what's worth saving, and appends the result to today's daily log.

Usage:
    uv run python scripts/flush.py <context_file.md> <session_id>
    uv run python scripts/flush.py <context_file.md> <session_id> --distill-only
"""

from __future__ import annotations

# Recursion prevention: set this BEFORE any imports that might trigger Claude
import os
os.environ["ARC_HOOK_INVOKED"] = "1"

import argparse
import asyncio
import json
import logging
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DAILY_DIR = ROOT / "daily"
SCRIPTS_DIR = ROOT / "scripts"
STATE_FILE = SCRIPTS_DIR / "last-flush.json"
LOG_FILE = SCRIPTS_DIR / "flush.log"

logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [flush] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

COMPILE_AFTER_HOUR = 18  # 6 PM local time


def load_flush_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_flush_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state), encoding="utf-8")


def append_to_daily_log(
    content: str,
    section: str = "Session",
    *,
    session_id: str | None = None,
    daily_dir: Path | None = None,
) -> None:
    """Append content to today's daily log with a provenance footer."""
    target_dir = daily_dir if daily_dir is not None else DAILY_DIR
    today = datetime.now(timezone.utc).astimezone()
    log_path = target_dir / f"{today.strftime('%Y-%m-%d')}.md"

    if not log_path.exists():
        target_dir.mkdir(parents=True, exist_ok=True)
        log_path.write_text(
            f"# Daily Log — {today.strftime('%Y-%m-%d')}\n\n",
            encoding="utf-8",
        )

    time_str = today.strftime("%H:%M")
    provenance_parts: list[str] = []
    if session_id:
        provenance_parts.append(f"session={session_id}")
    provenance_parts.append(f"captured={today.isoformat(timespec='seconds')}")
    footer = f"\n_provenance: {', '.join(provenance_parts)}_\n"
    entry = f"\n## {section} ({time_str})\n\n{content}{footer}\n"

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)


FLUSH_PROMPT = """Review the conversation context below and respond with a concise summary
of important items that should be preserved in the daily log.
Do NOT use any tools — just return plain text.

## Signal vs noise
Save only high-signal knowledge. SKIP (noise):
- Routine tool calls, file reads, directory listings, or command output
- Restated context already present in wiki/context files
- Trivial confirmations ("ok", "sounds good", "yes", "got it")
- Back-and-forth clarification with no lasting insight
- Obvious or redundant restatements of known facts

INCLUDE (signal):
- Decisions with rationale
- Non-obvious lessons, gotchas, and patterns
- Action items and concrete follow-ups
- Meaningful Q&A that changes how work is done

## Durability tagging
Tag every bullet or item with either [durable] or [ephemeral]:
- [durable] — worth promoting to the wiki (decisions, lessons, strategic context, commitments)
- [ephemeral] — useful short-term only (in-progress status, temporary blockers, session-only notes)

Format your response as a structured daily log entry with these sections:

**Context:** [One line about what the user was working on] [durable] or [ephemeral]

**Key Exchanges:**
- [durable] or [ephemeral] [Important Q&A or discussions]

**Decisions Made:**
- [durable] or [ephemeral] [Any decisions with rationale]

**Lessons Learned:**
- [durable] or [ephemeral] [Gotchas, patterns, or insights discovered]

**Action Items:**
- [durable] or [ephemeral] [Follow-ups or TODOs mentioned]

**Sources:**
- [Key files, imports, or wiki articles referenced — list paths or [[wikilinks]] if known]

Only include sections that have actual content. If nothing is worth saving,
respond with exactly: FLUSH_OK"""


async def run_flush(context: str) -> str:
    """Extract important knowledge using the appropriate LLM backend."""
    sys.path.insert(0, str(SCRIPTS_DIR.parent))
    from scripts.config import llm_summarize

    prompt = f"{FLUSH_PROMPT}\n\n## Conversation Context\n\n{context}"

    try:
        return await llm_summarize(prompt, "")
    except Exception as e:
        import traceback
        logging.error("LLM error: %s\n%s", e, traceback.format_exc())
        return f"FLUSH_ERROR: {type(e).__name__}: {e}"


def maybe_trigger_compilation() -> None:
    """If it's past the compile hour and today's log hasn't been compiled, run compile.py."""
    import subprocess as _sp

    compile_script = SCRIPTS_DIR / "compile.py"
    if not compile_script.exists():
        return

    now = datetime.now(timezone.utc).astimezone()

    # Check if today's log has already been compiled
    today_log = f"{now.strftime('%Y-%m-%d')}.md"
    state_file = SCRIPTS_DIR / "state.json"
    if state_file.exists():
        try:
            compile_state = json.loads(state_file.read_text(encoding="utf-8"))
            ingested = compile_state.get("ingested", {})
            compiled_hashes = compile_state.get("compiled_hashes", {})
            if today_log in ingested or today_log in compiled_hashes:
                from hashlib import sha256
                log_path = DAILY_DIR / today_log
                if log_path.exists():
                    current_hash = sha256(log_path.read_bytes()).hexdigest()[:16]
                    stored_hash = ingested.get(today_log, {}).get("hash", "") or compiled_hashes.get(today_log, "")
                    if current_hash == stored_hash:
                        return  # log unchanged since last compile
        except (json.JSONDecodeError, OSError):
            pass

    logging.info("End-of-day compilation triggered (after %d:00)", COMPILE_AFTER_HOUR)

    cmd = ["uv", "run", "--directory", str(ROOT), "python", str(compile_script)]

    kwargs: dict = {}
    if sys.platform == "win32":
        kwargs["creationflags"] = _sp.CREATE_NO_WINDOW
    else:
        kwargs["start_new_session"] = True

    try:
        _sp.Popen(cmd, stdout=_sp.DEVNULL, stderr=_sp.DEVNULL, cwd=str(ROOT), **kwargs)
    except Exception as e:
        logging.error("Failed to spawn compile.py: %s", e)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Distill conversation context into the daily log.",
    )
    parser.add_argument(
        "context_file",
        type=Path,
        help="Pre-extracted conversation context (.md)",
    )
    parser.add_argument(
        "session_id",
        help="Session identifier for deduplication and provenance",
    )
    parser.add_argument(
        "--distill-only",
        action="store_true",
        help="Print distillation result without writing daily log or triggering compilation",
    )
    return parser.parse_args(argv)


def run_flush_pipeline(
    context_file: Path,
    session_id: str,
    *,
    distill_only: bool = False,
) -> int:
    """Run distillation; write daily log and trigger compilation unless distill_only."""
    logging.info(
        "flush.py started for session %s, context: %s, distill_only=%s",
        session_id,
        context_file,
        distill_only,
    )

    if not context_file.exists():
        logging.error("Context file not found: %s", context_file)
        return 1

    if not distill_only:
        state = load_flush_state()
        if (
            state.get("session_id") == session_id
            and time.time() - state.get("timestamp", 0) < 60
        ):
            logging.info("Skipping duplicate flush for session %s", session_id)
            context_file.unlink(missing_ok=True)
            return 0

    context = context_file.read_text(encoding="utf-8").strip()
    if not context:
        logging.info("Context file is empty, skipping")
        if not distill_only:
            context_file.unlink(missing_ok=True)
        return 0

    logging.info("Flushing session %s: %d chars", session_id, len(context))

    response = asyncio.run(run_flush(context))

    if distill_only:
        print(response)
        logging.info("Distill-only complete for session %s", session_id)
        return 0

    if "FLUSH_OK" in response:
        logging.info("Result: FLUSH_OK — nothing worth saving")
    elif "FLUSH_ERROR" in response:
        logging.error("Result: %s", response)
    else:
        logging.info("Result: saved to daily log (%d chars)", len(response))
        append_to_daily_log(response, "Session", session_id=session_id)

    save_flush_state({"session_id": session_id, "timestamp": time.time()})
    context_file.unlink(missing_ok=True)
    maybe_trigger_compilation()
    logging.info("Flush complete for session %s", session_id)
    return 0


def main() -> None:
    args = parse_args()
    exit_code = run_flush_pipeline(
        args.context_file,
        args.session_id,
        distill_only=args.distill_only,
    )
    if exit_code:
        sys.exit(exit_code)


if __name__ == "__main__":
    main()