---
name: update-starter
description: Pull the latest framework updates from the arc-starter repo while preserving all of the user's context work. Trigger when the user asks to update arc-starter, pull the latest, upgrade the starter kit, or uses "/update-starter".
metadata:
  short-description: Safe update of framework files, preserving user context
---

# update-starter

Update this arc-starter repo to the latest version from origin/main.
Preserve all user-authored context. Overwrite only framework files.

## The contract

**NEVER touch these paths.** They are user work:

- `context/**`
- `daily/**`
- `wiki/**`
- `imports/**`
- Any file not in the framework allowlist below.

**OVERWRITE these (safe, no founder customization expected):**

- `.claude/commands/**`
- `.claude/skills/**`
- `.codex/skills/**`
- `.codex/hooks.json`
- `scripts/**`
- `hooks/**`
- `guides/**`
- `arc_starter/**`
- `setup.sh`
- `setup.ps1`
- `.gitattributes`
- `pyproject.toml`
- `uv.lock`
- `CHANGELOG.md`

**MERGE CAREFULLY (founder agents may have added preferences):**

- `AGENTS.md`
- `CLAUDE.md`
- `README.md`

For MERGE CAREFULLY paths: read local + `git show origin/main:<path>`,
preserve sections present only locally (founder additions), add sections
present only upstream (new framework content), and STOP + ask if the
same section differs in ways that look like founder customization vs
minor upstream rewording. Full protocol in
`guides/update-prompt.md` on origin/main.

When unsure, ASK. Don't guess.

## Steps

1. **Protect local work.**
   `git stash push -u -m "arc-update-$(date +%s)"`
   Report the stash ref.

2. **Fetch.**
   `git fetch origin main`

3. **Read CHANGELOG diff.**
   Compare local `CHANGELOG.md` to `origin/main:CHANGELOG.md`. Summarise
   in 3-6 bullets of plain English.

4. **Apply framework updates, path by path.**

   For each path in the **OVERWRITE** list, run:
   `git checkout origin/main -- <path>`
   Skip paths that don't exist on origin/main.

   For each path in the **MERGE CAREFULLY** list:
   - Read local + `git show origin/main:<path>`
   - If identical, skip.
   - If only upstream changed, `git checkout origin/main -- <path>`.
   - If local has founder additions, merge: preserve local-only
     sections, add upstream-only sections, STOP + ask if the same
     section differs in non-trivial ways.
   - Report what was preserved and what was added from upstream.

5. **Report.**
   - What was updated (list files changed)
   - What was preserved (point at context/, daily/, wiki/, imports/)
   - Whether anything was stashed and how to recover
   - One suggested next move

6. **Do not commit.** Leave the tree for the user to review.

## Guardrails

- **Pre-flight.** Run `git status`. Dirty framework files split into:
  - Dirty OVERWRITE paths → unexpected. STOP, list, ask: keep / overwrite / move-to-backup.
  - Dirty MERGE CAREFULLY paths (`AGENTS.md`, `CLAUDE.md`, `README.md`)
    → expected. Continue; merge protocol at step 4 handles them.
  - Dirty files outside the allowlist → user-owned, leave alone.
- If fetch fails, STOP. Report exactly what went wrong.
- If CHANGELOG diff is empty: "already on latest."
- NEVER `git reset --hard`, `git clean -fd`, or `git push`.
- NEVER touch non-allowlist paths.

## Trigger examples

- "update arc-starter"
- "pull the latest starter"
- "upgrade my arc-starter"
- "/update-starter"
