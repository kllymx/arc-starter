#!/usr/bin/env python3
"""
GitHub preflight for the company-brain setup.

Gives the agent a clean, deterministic read of what it can automate via `gh`
before it guides the founder through creating the shared repo. Crucially:
`gh` CANNOT create an organization (there is no `gh org create`, and org
creation is not in the public API for normal accounts) — that one step is a
browser action. Everything after (repo create, invites, remote, push, PR) is
scriptable, so this report tells the agent which path and fallback to take.

Stdlib + gh/git subprocess only. Never throws: any probe failure → a False/None
field. Run: `uv run python scripts/github_status.py`
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys

ORG_CREATE_URL = "https://github.com/account/organizations/new"


def _run(args: list[str]) -> tuple[int, str]:
    try:
        out = subprocess.run(args, capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.SubprocessError):
        return 1, ""
    return out.returncode, out.stdout


def _user_and_scopes() -> tuple[str | None, list[str]]:
    """Return (login, oauth_scopes, scopes_known) from one authenticated call.

    `scopes_known` is False when no `x-oauth-scopes` header was present — which is
    the case for fine-grained PATs and GitHub App tokens. Those don't expose
    scopes, so an empty list must NOT be read as "no permissions".
    """
    code, out = _run(["gh", "api", "-i", "user"])
    if code != 0 or not out:
        return None, [], False

    # Split headers from JSON body.
    sep = "\r\n\r\n" if "\r\n\r\n" in out else "\n\n"
    head, _, body = out.partition(sep)

    scopes: list[str] = []
    scopes_known = False
    for line in head.splitlines():
        if line.lower().startswith("x-oauth-scopes:"):
            scopes_known = True
            raw = line.split(":", 1)[1]
            scopes = [s.strip() for s in raw.split(",") if s.strip()]
            break

    login = None
    try:
        login = json.loads(body).get("login")
    except (json.JSONDecodeError, AttributeError):
        pass
    return login, scopes, scopes_known


def _orgs() -> list[str]:
    code, out = _run(["gh", "api", "user/orgs", "--jq", ".[].login"])
    if code != 0:
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def _origin() -> str | None:
    code, out = _run(["git", "remote", "get-url", "origin"])
    return out.strip() if code == 0 and out.strip() else None


def _origin_owner_repo() -> str | None:
    """Parse OWNER/REPO from the origin URL (https or ssh form)."""
    url = _origin()
    if not url:
        return None
    match = re.search(r"[:/]([^/:]+/[^/:]+?)(?:\.git)?/?$", url)
    return match.group(1) if match else None


def _origin_visibility() -> str | None:
    # Pin the check to ORIGIN's owner/repo. `gh repo view` with no arg uses gh's
    # default repo, which in a fork setup (origin = company repo, upstream =
    # public arc-starter) can resolve to the wrong, public repo.
    target = _origin_owner_repo()
    args = ["gh", "repo", "view"]
    if target:
        args.append(target)
    args += ["--json", "visibility", "--jq", ".visibility"]
    code, out = _run(args)
    return out.strip() if code == 0 and out.strip() else None


def collect() -> dict:
    installed = shutil.which("gh") is not None
    if not installed:
        return {
            "gh_installed": False,
            "authenticated": False,
            "login": None,
            "scopes": [],
            "scopes_known": False,
            "can_create_repo": False,
            "can_admin_org": False,
            "orgs": [],
            "origin": _origin(),
            "origin_visibility": None,
        }

    code, _ = _run(["gh", "auth", "status"])
    authenticated = code == 0
    login, scopes, scopes_known = (
        _user_and_scopes() if authenticated else (None, [], False)
    )

    # When scopes are known (classic OAuth), report capability precisely. When
    # they aren't (fine-grained PAT / GitHub App), report None = "unknown" rather
    # than False, so the upgrade flow attempts the action instead of wrongly
    # telling the user they can't.
    can_create_repo = ("repo" in scopes) if scopes_known else (None if authenticated else False)
    can_admin_org = ("admin:org" in scopes) if scopes_known else (None if authenticated else False)

    return {
        "gh_installed": True,
        "authenticated": authenticated,
        "login": login,
        "scopes": scopes,
        "scopes_known": scopes_known,
        "can_create_repo": can_create_repo,
        "can_admin_org": can_admin_org,
        "orgs": _orgs() if authenticated else [],
        "origin": _origin(),
        "origin_visibility": _origin_visibility(),
    }


def render(status: dict) -> str:
    lines = ["# GitHub preflight", ""]
    if not status["gh_installed"]:
        lines.append("- `gh` CLI: NOT installed. Install it (https://cli.github.com) or")
        lines.append("  fall back to manual git remote setup in the browser.")
        if status["origin"]:
            lines.append(f"- origin: `{status['origin']}`")
        return "\n".join(lines)

    if not status["authenticated"]:
        lines.append("- `gh` installed but NOT authenticated. Run `gh auth login` first.")
        return "\n".join(lines)

    lines.append(f"- Authenticated as **{status['login']}**.")
    if not status.get("scopes_known", True):
        lines.append(
            "- Token scopes unavailable (fine-grained PAT or GitHub App) — I'll "
            "attempt repo creation and org invites and fall back (repo "
            "collaborators / web UI) only if GitHub actually refuses."
        )
    else:
        lines.append(
            f"- Can create repos (repo scope): {'yes' if status['can_create_repo'] else 'no'}."
        )
        lines.append(
            "- Can invite ORG members via API (admin:org scope): "
            + ("yes" if status["can_admin_org"] else "no — use repo collaborators, the "
               "web UI, or `gh auth refresh -s admin:org`.")
        )
    if status["orgs"]:
        lines.append(f"- Existing orgs you belong to: {', '.join(status['orgs'])}.")
    else:
        lines.append(
            "- No orgs found. Creating one is a browser step (gh cannot): "
            + ORG_CREATE_URL
        )
    if status["origin"]:
        vis = status["origin_visibility"] or "unknown"
        lines.append(f"- Current origin: `{status['origin']}` (visibility: {vis}).")
    else:
        lines.append("- No `origin` remote yet.")
    return "\n".join(lines)


def main() -> int:
    status = collect()
    if "--json" in sys.argv[1:]:
        print(json.dumps(status, indent=2))
    else:
        print(render(status))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
