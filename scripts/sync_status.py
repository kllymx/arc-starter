#!/usr/bin/env python3
"""
Company-mode sync status for SessionStart injection.

Produces a short, agent-aware reminder so the agent prompts the founder to
push their personal branch and open/update a PR — at the start of each
session (and more urgently near end of day). Stdlib + git/gh subprocess only;
no third-party deps, so it runs even before `setup.sh`.

Prints nothing in personal mode, outside a git repo, with no origin remote,
or when there is nothing to say. Never fails loudly: any error → silent exit.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.config import get_mode, get_user_branch  # noqa: E402

# Past this local hour, escalate the reminder to "wrap up / open-or-merge a PR".
END_OF_DAY_HOUR = 18


def _git(*args: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip()


def _is_repo() -> bool:
    return _git("rev-parse", "--git-dir") is not None


def _has_origin() -> bool:
    return _git("remote", "get-url", "origin") is not None


def _current_branch() -> str:
    return _git("rev-parse", "--abbrev-ref", "HEAD") or ""


def _main_ref() -> str | None:
    """Prefer origin/main, fall back to origin/master if that's the default."""
    for ref in ("origin/main", "origin/master"):
        if _git("rev-parse", "--verify", "--quiet", ref) is not None:
            return ref
    return None


def _counts(left: str, right: str) -> tuple[int, int] | None:
    """Return (ahead, behind) of HEAD relative to `right` via left...right."""
    out = _git("rev-list", "--left-right", "--count", f"{left}...{right}")
    if not out:
        return None
    try:
        ahead_str, behind_str = out.split()
        return int(ahead_str), int(behind_str)
    except ValueError:
        return None


def _open_pr(branch: str) -> str | None:
    """Return an open PR number for `branch` via gh, or None. gh optional."""
    try:
        res = subprocess.run(
            ["gh", "pr", "view", branch, "--json", "number,state", "-q",
             'select(.state=="OPEN") | .number'],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    num = res.stdout.strip()
    return num or None


def _local_hour() -> int:
    # Avoid importing datetime.now at module import; called only at runtime.
    from datetime import datetime

    return datetime.now().hour


def build_sync_status() -> str:
    """Assemble the company-mode sync reminder (empty string when nothing to say)."""
    if get_mode() != "company":
        return ""
    if not _is_repo() or not _has_origin():
        return ""

    branch = _current_branch()
    personal = get_user_branch()
    main_ref = _main_ref()
    lines: list[str] = []

    # On main/master in company mode is the wrong place to work.
    if branch in ("main", "master"):
        lines.append(
            f"- You're on `{branch}`. In company mode, work happens on your own "
            f"branch `{personal}`. Say \"sync\" and I'll move your changes there "
            f"and open a PR — this protects the shared `{branch}`."
        )
    else:
        if main_ref:
            counts = _counts("HEAD", main_ref)
            if counts:
                ahead, behind = counts
                if behind:
                    lines.append(
                        f"- `{main_ref}` has {behind} new commit(s) you don't have "
                        f"yet. Say \"sync\" to integrate them (I'll reconcile any "
                        f"conflicts)."
                    )
                if ahead:
                    pr = _open_pr(branch)
                    if pr:
                        lines.append(
                            f"- {ahead} commit(s) on `{branch}` not in `main`. "
                            f"Open PR #{pr} — say \"sync\" to update it, or \"merge\" "
                            f"when you're ready to share."
                        )
                    else:
                        lines.append(
                            f"- {ahead} commit(s) on `{branch}` not yet shared and no "
                            f"open PR. Say \"sync\" to push and open one."
                        )

    if not lines:
        return ""

    if _local_hour() >= END_OF_DAY_HOUR:
        lines.append(
            "- It's end of day — a good time to sync and open/merge your PR so the "
            "team has your latest before tomorrow."
        )

    return "## ARC Sync (company mode)\n\n" + "\n".join(lines)


def main() -> None:
    status = build_sync_status()
    if status:
        print(status)


if __name__ == "__main__":
    main()
