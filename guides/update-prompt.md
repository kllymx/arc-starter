# Update arc-starter prompt

This is the canonical instruction the agent should follow when asked to
update arc-starter. The on-screen prompt in Session 2 is a one-line
pointer to this file. From Session 3 onwards, `/update-starter` does
the same thing.

---

Update my arc-starter to the latest version from `origin/main`. Preserve
all of my context work. Overwrite only framework files.

## Rules

**NEVER touch these paths.** They are my work:

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

**MERGE CAREFULLY (founder agents may have added preferences over time):**

- `AGENTS.md`
- `CLAUDE.md`
- `README.md`

For every MERGE CAREFULLY path, do this instead of a straight checkout:

1. Read the current local file (`cat <path>` or file-read tool).
2. Read the upstream file (`git show origin/main:<path>`).
3. Compare section by section:
   - **Sections present ONLY in local** → founder or founder's agent added
     these. PRESERVE them exactly. Common targets: personal preferences,
     saved workflows, project-specific notes, "## Memory and Learning"
     extensions.
   - **Sections present ONLY upstream** → new framework content, like
     new guidance, new capabilities, new harness notes. ADD them to the
     local file in the same position they sit upstream.
   - **Sections present in both but differ** → the hard case. If the
     difference is minor rewording/clarification from upstream, prefer
     upstream. If the difference looks like founder customization
     (tone changes, added bullets, reordered priorities), STOP and ask
     the founder which to keep.
4. Write the merged result back to disk.
5. Report a short diff-summary to the founder so they can see what you
   preserved and what you updated.

If the file has less than ~5% drift from upstream, a straight checkout is
fine — note this and proceed. Only engage the careful merge if there's
meaningful founder content at stake.

If unsure whether a path is framework or user work, ASK. Don't guess.

## Steps

1. **Protect local work first.**
   Stash any uncommitted changes with a unique timestamped label. Use
   whatever shell syntax is correct for the user's environment
   (bash `$(date +%s)`, PowerShell `$(Get-Date -UFormat %s)`, or a
   plain ISO timestamp if unsure). Report the stash ref.

2. **Fetch without merging.**
   `git fetch origin main`

   If the user downloaded arc-starter as a zip instead of cloning (no
   `.git` directory, or `origin` remote doesn't exist), do this first:
   - Initialize: `git init`
   - Add the canonical remote: `git remote add origin https://github.com/kllymx/arc-starter.git`
   - Fetch: `git fetch origin main`
   - Do NOT reset their working tree afterwards. Continue from step 3
     with the allowlist checkout. Their local files are preserved
     because `git checkout origin/main -- <path>` only touches the
     paths you hand it.

   If `git fetch` stalls for more than ~20 seconds (likely auth prompt
   on HTTPS), STOP and tell the user: "your git remote needs credentials.
   Cache them with `git config --global credential.helper osxkeychain`
   (macOS) / `manager` (Windows) / `store` (Linux), then retry."

3. **Read the CHANGELOG diff.**
   Compare local `CHANGELOG.md` at HEAD to `origin/main:CHANGELOG.md`.
   Summarise in plain English. 3-6 bullets max.

4. **Apply framework updates, path by path.**

   For each path in the **OVERWRITE** list, run:
   `git checkout origin/main -- <path>`
   If a path doesn't exist on origin/main, skip silently.

   For each path in the **MERGE CAREFULLY** list, follow the merge
   protocol described in the Rules section above: read local + upstream,
   preserve sections present only locally (founder additions), add
   sections present only upstream (new framework content), and STOP +
   ask if the same section differs in a non-trivial way. After writing
   the merged file, report which sections were preserved and which were
   added from upstream so the founder can verify.

5. **Report.**
   - Which update this was, based on the CHANGELOG header you
     summarised in step 3 (e.g. "Session 2 update — here's what landed")
   - What was overwritten (list the files)
   - What was merged (list the files + a short summary of what was
     preserved from the local version)
   - What was preserved untouched (point at `context/`, `daily/`,
     `wiki/`, `imports/`)
   - Whether anything was stashed and how to recover (`git stash list`,
     `git stash pop`)
   - One concrete next move picked from the CHANGELOG you just read —
     not a generic example. If the CHANGELOG added a new slash command,
     name it and suggest something the founder could try with it right
     now, using a real entity from their context layer when possible.

6. **Do not commit.** Leave the working tree for me to review.

## Guardrails

- **Pre-flight check for dirty framework files.** Run `git status` and
  split any dirty framework files into two groups based on the
  allowlist:

  - Dirty files in **OVERWRITE** paths are unexpected (these aren't
    files founders usually edit). For these, STOP, list them, and ask:
    keep (abort update), overwrite (proceed and replace from upstream),
    or move-to-backup (copy to `*.backup-<timestamp>` before
    overwriting). Show a short diff summary when you ask so the
    founder can decide.

  - Dirty files in **MERGE CAREFULLY** paths are *expected* — these are
    the files founders and their agents naturally customize. Do NOT
    stop for these. Continue to step 1, and handle them via the merge
    protocol at step 4.

  - Dirty files outside the allowlist (e.g. `context/`, `daily/`,
    `wiki/`, `imports/`, `.obsidian/`) are user-owned. Leave them
    alone and don't mention them in the pre-flight report.

- If fetch fails (network, auth, missing remote), STOP and report
  exactly what went wrong. Do not attempt offline guesses.
- If the CHANGELOG diff is empty, exit early: "already on latest."
- NEVER run `git reset --hard`, `git clean -fd`, or `git push`. Not part
  of this job.
- NEVER touch paths outside the framework allowlist.
