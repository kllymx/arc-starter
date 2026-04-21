---
description: Pull the latest framework updates from arc-starter, preserving your context
---

# /update-starter

Update this arc-starter to the latest version from the official repo.
Preserve all of my context work. Overwrite only framework files.

## The contract

**NEVER touch these paths under any circumstance.** These are my work:

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
preserve any sections present only locally (founder additions), add any
sections present only upstream (new framework content), and STOP + ask
if the same section differs in ways that look like founder customization
vs minor upstream rewording. Full protocol is in
`guides/update-prompt.md` on origin/main.

If unsure whether a path is framework or user, ASK. Don't guess.

## Steps

1. **Protect local work first.**
   Stash any uncommitted changes with a unique timestamped label. Use
   whatever shell syntax is correct for the user's environment
   (bash `$(date +%s)`, PowerShell `$(Get-Date -UFormat %s)`, or a
   plain ISO timestamp if unsure). Report the stash ref.

2. **Fetch without merging.**
   `git fetch origin main`

3. **Read the CHANGELOG diff.**
   Compare my `CHANGELOG.md` at HEAD to `origin/main:CHANGELOG.md`.
   Summarise in plain English what's new. 3-6 bullets max.

4. **Apply framework updates, path by path.**

   For each path in the **OVERWRITE** list, run:
   `git checkout origin/main -- <path>`
   If the path doesn't exist on origin/main, skip silently.

   For each path in the **MERGE CAREFULLY** list:
   - Read the local file and `git show origin/main:<path>`
   - If the files are identical, skip silently.
   - If only upstream changed (no founder edits since clone), run
     `git checkout origin/main -- <path>` — same as overwrite.
   - If the local file has founder additions (new sections,
     preference notes, extra bullets), MERGE:
     · Preserve every section present only locally.
     · Add every section present only upstream.
     · If a section exists in both but differs meaningfully, STOP and
       ask the founder which version to keep.
     · Write the merged result back.
   - After merging, report what you preserved and what you added from
     upstream so the founder can verify.

5. **Report.**
   Tell me:
   - What was updated (list the files that changed)
   - What was preserved (point at my context/, daily/, wiki/, imports/)
   - Whether anything in my local work was stashed — if so, how to
     recover it (`git stash list`, `git stash pop`)
   - One suggested next move to try a new command/skill

6. **Do not commit.** Leave the working tree for me to review.

## Guardrails

- If `git status` shows local modifications to framework files before
  we start, STOP. List them. Ask whether I want to keep them (abort),
  overwrite (proceed), or move them somewhere safe first.
- If fetch fails (no network, no remote, auth issue), STOP and tell me
  exactly what went wrong. Do not attempt offline guesses.
- If the CHANGELOG diff is empty, exit early: "already on latest."
- NEVER run `git reset --hard`, `git clean -fd`, or `git push`. Not part
  of this job.
- NEVER touch paths outside the framework allowlist, even if they look
  like they should be framework. When in doubt, ask.
