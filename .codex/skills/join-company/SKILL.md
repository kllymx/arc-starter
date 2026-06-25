---
name: join-company
description: Join an existing ARC company brain. For a teammate who has cloned the shared company repo and wants to get set up without re-running the business interview. Trigger on "join the company brain", "join an existing company", "I was added to the team brain", or "/join-company".
metadata:
  short-description: Onboard a teammate onto an existing shared brain
---

# join-company

Set this person up on an **existing** company brain they've just cloned. The wiki is
already built — configure *them* (environment, private tier, personal branch) and get
them syncing. Do NOT re-interview the business.

## Clone the right thing

A teammate clones the **company brain repo** from the org (it has the full framework +
the team wiki), NOT `arc-starter`. Founder sends them: `gh auth login` as themselves →
`git clone <org>/<repo>` → open in agent → say "join the company brain".

## Steps

1. **Confirm it's a company brain.** `context/workspace.md` has `- Mode: company` AND the
   wiki is populated; `origin` is the team's private repo, not the public
   `kllymx/arc-starter`. If it looks like a fresh arc-starter, STOP and tell them to run
   `setup` to start their own.
2. **Confirm their identity:** `uv run python scripts/github_status.py` — they must be
   authenticated as **themselves**. If not, walk through `gh auth login`.
3. **Install + private tier:** run `setup.sh` (or `setup.ps1`). Creates their own local
   gitignored `private/` tier. If `.venv` exists, run
   `uv run python scripts/scaffold_private.py`.
4. **Configure their environment** in `context/workspace.md` (harness + technical
   comfort), leaving `- Mode: company` untouched (Mode is shared; environment is
   per-person).
5. **Personal branch:** `git fetch origin main` then `git switch -c arc/<slug>` (`<slug>`
   = git email before `@`, lowercased). If it already exists remotely, `git switch
   arc/<slug>` then `git rebase origin/main`.
6. **Orient them:** wiki is already here (ask it anything); captures land in
   `private/wiki/` by default, `/promote` to share; `sync` pushes their branch + opens a
   PR; `private/` is theirs. Do a first `sync` so their branch lands on the remote.

## Trigger examples

- "join the company brain"
- "I was added to the team brain"
- "/join-company"
