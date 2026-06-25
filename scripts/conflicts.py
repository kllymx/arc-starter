#!/usr/bin/env python3
"""
Conflict inspection backend for ARC's LLM-assisted /reconcile.

Wiki articles are an *additive* knowledge base: most "conflicts" are two people
adding different things to the same file and should be UNIONED, not chosen
between. This module gives the agent clean, structured inputs to do that:
the base / ours / theirs versions of each conflicted file, pulled from git's
merge stages (robust — no fragile parsing of <<<<<<< markers).

Stdlib + git subprocess only. Usage:
    uv run python scripts/conflicts.py list           # conflicted paths, one per line
    uv run python scripts/conflicts.py show <path>     # base/ours/theirs blocks
    uv run python scripts/conflicts.py state           # merge | rebase | none
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _git(*args: str) -> tuple[int, str]:
    try:
        out = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            timeout=15,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return 1, str(exc)
    return out.returncode, out.stdout


def operation_state() -> str:
    """Return 'rebase', 'merge', or 'none' for the in-progress git operation."""
    code, git_dir = _git("rev-parse", "--git-dir")
    if code != 0:
        return "none"
    gd = Path(git_dir.strip())
    if not gd.is_absolute():
        gd = PROJECT_ROOT / gd
    if (gd / "rebase-merge").exists() or (gd / "rebase-apply").exists():
        return "rebase"
    if (gd / "MERGE_HEAD").exists():
        return "merge"
    return "none"


def conflicted_files() -> list[str]:
    """Paths with unresolved merge conflicts (unmerged index entries)."""
    code, out = _git("diff", "--name-only", "--diff-filter=U")
    if code != 0:
        return []
    return [line for line in out.splitlines() if line.strip()]


def _stage(stage_no: int, path: str) -> str | None:
    """Return the content of a merge stage (1=base, 2=ours, 3=theirs) or None
    if that stage is absent (e.g. add/add conflicts have no base)."""
    code, out = _git("show", f":{stage_no}:{path}")
    if code != 0:
        return None
    return out


def file_stages(path: str) -> dict[str, str | None]:
    """Return {'base', 'ours', 'theirs'} content for a conflicted path.

    For a rebase, 'ours' is the rebase target (shared main being replayed onto)
    and 'theirs' is your replayed commit — git's stage semantics during rebase
    are inverted vs a merge, so the /reconcile prompt labels them by meaning,
    not by side.
    """
    return {
        "base": _stage(1, path),
        "ours": _stage(2, path),
        "theirs": _stage(3, path),
    }


def _format_show(path: str) -> str:
    stages = file_stages(path)
    parts = [f"# Conflict: {path}", f"(git operation: {operation_state()})", ""]
    for label in ("base", "ours", "theirs"):
        content = stages[label]
        parts.append(f"## {label}")
        if content is None:
            parts.append("(absent — this side did not have the file)")
        else:
            parts.append("```")
            parts.append(content.rstrip("\n"))
            parts.append("```")
        parts.append("")
    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    cmd = args[0] if args else "list"

    if cmd == "state":
        print(operation_state())
        return 0

    if cmd == "list":
        files = conflicted_files()
        if not files:
            print("No conflicted files.")
            return 0
        for f in files:
            print(f)
        return 0

    if cmd == "show":
        if len(args) < 2:
            print("usage: conflicts.py show <path>", file=sys.stderr)
            return 1
        print(_format_show(args[1]))
        return 0

    print(f"unknown command: {cmd}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
