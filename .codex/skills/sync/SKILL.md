---
name: sync
description: Manually pull, commit, and push ARC changes to GitHub. The primary git-sync path for Codex users (since Codex's Stop event doesn't fit auto-push). Trigger when the user asks to push their changes, sync to GitHub, save to GitHub, or uses "/sync".
metadata:
  short-description: Manual git sync — pull, commit, push the founder's ARC to their remote
---

# sync

Push the founder's ARC changes to their git remote. This is the manual
version of what the auto-pull hook does at session start. Codex's Stop
event fires per-turn so we don't auto-push — sync runs explicitly.

## When to use

- Founder wants to push captures without ending the session
- They've made changes to context, wiki, or commands and want them safe
- Before switching machines, they want the latest pushed
- Auto-pull on session start hasn't pushed their pending work yet

## Pre-sync check

Run `git status` and check the remote. If any is true, **stop and ask
before running anything**:

- **Not a git repo** → tell them ARC works locally, offer to walk
  through `git init` + `gh repo create --private --source=. --push`
  (require `gh` CLI + `gh auth status` clean first)
- **No `origin` remote** → ask if they want a private GitHub repo
  created
- **Origin points to upstream `kllymx/arc-starter`** → they don't have
  push access. Suggest creating their own private fork as origin
- **Working tree has unrelated changes** in framework files → list and
  ask before committing

If everything looks normal — wiki, daily, context updates — proceed.

## Phase 1 — Pull

```bash
git pull --rebase --autostash
```

If pull fails (auth, network, conflict), report and stop. Don't push on
top of a failed pull.

## Phase 2 — Stage

```bash
git add -A
```

The `.gitignore` is the founder's safety net.

## Phase 3 — Commit

```bash
git commit -m "arc: $(date -u +%Y-%m-%d-%H%M)"
```

If the founder describes what changed, use that as the message
(under 60 chars).

## Phase 4 — Push

```bash
git push
```

If push fails on auth: walk through `gh auth login`.

If push fails because origin is the public upstream: explain and offer
to create a private fork.

## Report

- What was committed
- Whether push succeeded (or what to retry)
- Confirm visibility is private (`gh repo view --json visibility,url`)

## Skip if nothing changed

If `git status` shows nothing, say *"nothing to sync"* and exit. No
empty commits.

## Constraints

- Never push to a public remote unless the founder explicitly confirms.
- Never run `git reset --hard` or `git push --force`.
- Never touch paths outside the framework allowlist.

## Trigger examples

- "push my changes"
- "sync to github"
- "save to github"
- "/sync"
