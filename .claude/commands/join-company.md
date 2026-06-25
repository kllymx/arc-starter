---
description: Join an existing ARC company brain. For a teammate who has cloned the shared company repo and wants to get set up — without re-running the business interview.
---

# /join-company

Set this person up on an **existing** company brain they've just cloned. The wiki is
already built; this flow configures *them* (their environment, their private tier,
their personal branch) and gets them syncing. It does NOT re-interview the business.

## First: clone the right thing

A teammate does **not** clone `arc-starter`. They clone the **company brain repo** from
the org (it already contains the full framework plus the team's wiki). The founder sends
them: "run `gh auth login` as yourself, `git clone <org>/<repo>`, open it in your agent,
and say *join the company brain*."

## When to use

- The user says "join the company brain", "join an existing company", "I was added to
  the team brain", "/join-company".
- Or you detect at session start that this is a cloned company brain and the person
  isn't set up yet (Mode is `company`, the wiki is populated, but they're on `main` with
  no personal `arc/<slug>` branch).

## Step 1 — Confirm this really is a company brain

- `context/workspace.md` has `- Mode: company` AND the wiki is populated (not the
  starter placeholder).
- `origin` is the team's private repo, **not** the public `kllymx/arc-starter` upstream.

If instead this looks like a fresh arc-starter (placeholder wiki, no company markers, or
origin is the upstream), STOP and say: "This looks like a fresh ARC workspace, not a
company brain — run `/setup` to start your own." Don't run the join flow.

## Step 2 — Confirm their GitHub identity

```bash
uv run python scripts/github_status.py
```

They must be authenticated as **themselves** (not the founder). If not authenticated,
walk them through `gh auth login`. They already have access since they cloned the repo.

## Step 3 — Install capture + their private tier

Run `setup.sh` (macOS/Linux/Git Bash) or `setup.ps1` (Windows). This installs the
capture tooling and creates their own local, gitignored `private/` tier via
`scripts/scaffold_private.py`. If `.venv` already exists, just run
`uv run python scripts/scaffold_private.py` to ensure the private tier.

**Heads up about hooks:** the repo ships with hooks wired in `.claude/settings.json` /
`.codex/hooks.json`, but a freshly cloned project asks the user to **trust/approve the
hooks once** before they run (a security prompt). Tell them to approve it — that's what
enables auto-capture and the session-start sync reminder. Until then, those won't fire.

## Step 4 — Configure their environment (keep Mode)

Ask the two setup questions and write THEIR answers into `context/workspace.md`, leaving
`- Mode: company` untouched:

> "What are you using ARC in — Claude Code, Cursor, Codex, Claude Desktop? And how
> technical should I be: non-technical, somewhat technical, technical?"

(The Environment / Founder Preferences sections are per-person; Mode is shared.)

## Step 5 — Put them on their own branch

```bash
git fetch origin main
git switch -c arc/<slug>     # <slug> = git config user.email before @, lowercased
```

If the branch already exists remotely (they've joined before from another machine):
`git switch arc/<slug>` then `git rebase origin/main`.

## Step 6 — Orient them

They're in. Briefly explain the team workflow:

- The wiki is already here — ask it anything about the business; retrieval works now.
- New captures land in their local `private/wiki/` by default; `/promote` shares one.
- `/sync` pushes their branch and opens/updates a PR into `main`; ARC reminds them at
  session start when there's unsynced work.
- `private/` is theirs and never leaves their machine. Keep secrets in `.env`.

Do a first `/sync` so their branch exists on the remote and they see the loop work.
