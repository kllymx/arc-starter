---
description: Manually pull, commit, and push ARC changes to GitHub. The manual path Codex users take in lieu of an auto-push hook.
---

# /sync

Push the founder's ARC changes to their git remote. This is the manual
version of what the auto-pull and auto-push hooks do at session
boundaries.

## When to use

- Founder wants to push captures right now without ending the session
- They're on Codex (which auto-pulls but doesn't auto-push) and want to commit
- They've made changes to context, wiki, or commands and want them safe in GitHub
- Before switching machines, they want the latest pushed

## Pre-sync check

Run `git status` and check the remote. If any of these is true, **stop
and tell the founder before running anything**:

- **Not a git repo** → tell them ARC works locally, but if they want sync,
  walk through `git init` + `gh repo create --private --source=. --push`
  (require `gh` CLI installed and `gh auth status` clean first)
- **No `origin` remote** → ask if they want a private GitHub repo created
  (`gh repo create arc-private --private --source=. --push --remote=origin`)
- **Origin points to upstream `kllymx/arc-starter`** → they don't have
  push access there. Suggest creating their own private fork as origin
  (and renaming the upstream to `upstream` for `/update-starter`)
- **Working tree has unrelated changes** in framework files (e.g.,
  experimental edits to `.claude/commands/`) → list them and ask before
  committing

If everything looks normal — wiki, daily, context updates — proceed.

## Phase 1 — Pull first

Always pull before pushing to avoid conflicts:

```bash
git pull --rebase --autostash
```

If pull fails (auth, network, conflict), report the error and stop.
Don't push on top of a failed pull.

## Phase 2 — Stage changes

```bash
git add -A
```

The `.gitignore` is the founder's safety net. If you're worried about
something, run `git status` first and show them what would be staged.

## Phase 3 — Commit

```bash
git commit -m "arc: $(date -u +%Y-%m-%d-%H%M)"
```

If the founder describes what they did, use that as the message
instead. Keep under 60 characters.

## Phase 4 — Push

```bash
git push
```

If push fails on auth: walk through `gh auth login` or check the
remote.

If push fails because origin is the public upstream: explain and offer
to create a private fork.

## Report

Tell the founder:
- What was committed (line count or short file list)
- That it's safely pushed (or what to do if push failed)
- Whether the remote is private (run `gh repo view --json visibility,url`
  to confirm and quote it back)

## Skip if nothing changed

If `git status` shows no changes, say *"nothing to sync — your ARC is
up to date"* and exit. Don't make empty commits.

## Notes

- This command is the **manual path Codex users take.** Codex's hook
  events don't fit auto-push (Stop fires after every turn), so `/sync`
  is how Codex users get the same outcome.
- Claude users have an auto-push hook on `SessionEnd`, so they
  typically don't need `/sync`. But it's still useful mid-session.
- **Never push to a public remote** unless the founder explicitly
  confirms. Run `gh repo view --json visibility` and warn if `PUBLIC`.
