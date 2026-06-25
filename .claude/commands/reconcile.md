---
description: LLM-assisted resolution of git merge/rebase conflicts in the ARC wiki. Unions additive knowledge, flags genuine contradictions for the founder, and continues the operation.
---

# /reconcile

Resolve git conflicts in the ARC knowledge base intelligently. The wiki is an
**additive** knowledge base, so most conflicts are two people adding different
things to the same article — those should be **merged (unioned)**, not chosen
between. Only genuine semantic contradictions need a human decision.

Usually triggered from `/sync` when a rebase onto `main` hits conflicts, or run
directly when a merge/rebase is in progress.

## When to use

- `/sync` reported conflicts integrating `main`.
- `git status` shows "Unmerged paths" or you're mid-rebase/merge.
- The founder says "fix the conflicts", "reconcile", "merge these changes".

## Step 1 — Survey

```bash
uv run python scripts/conflicts.py state    # rebase | merge | none
uv run python scripts/conflicts.py list     # conflicted paths
```

If state is `none` and there are no conflicted files, tell the founder there's
nothing to reconcile and stop.

## Step 2 — Resolve each file

For every conflicted path:

```bash
uv run python scripts/conflicts.py show <path>
```

This prints the three versions: **base** (common ancestor), **ours**, and
**theirs**. Decide per file:

- **Wiki article / index / log / context note (the common case).** UNION the
  content. Keep every distinct fact, article, and `[[wikilink]]` from both
  sides. Merge bullet lists, combine sections, dedupe identical lines. For
  `wiki/index.md` and `wiki/log.md`, keep all entries from both sides in a
  sensible order. Preserve the founder's first-person voice exactly.
- **Genuine contradiction** (two sides assert incompatible facts about the same
  thing — a different price, a reversed decision). Do NOT silently pick. Keep
  both, mark them, and ask the founder which is current:
  `> ⚠ Conflict: [ours] vs [theirs] — which is right?`
- **Frontmatter.** Keep the latest `updated:` date; union `tags`; never lose a
  `visibility:` field — if either side marks it `private`, the merged article
  stays private (fail-closed).

Write the resolved file, then stage it:

```bash
git add <path>
```

## Step 3 — Continue the operation

```bash
# rebase:
git rebase --continue
# merge:
git commit --no-edit
```

If more conflicts surface on the next rebase step, repeat from Step 1.

## Step 4 — Report

Tell the founder, per file: merged cleanly, or merged-with-a-question-for-them.
List any `⚠ Conflict` markers you left so they can resolve the real
contradictions. Then hand back to `/sync` to push and update the PR.

## Rules

- **Never drop knowledge.** When unsure, keep both sides — losing a fact is worse
  than a little redundancy (a later `/garden` or `/consolidate` can dedupe).
- **Never resolve by blindly taking one side** (`-X ours`/`theirs`) for wiki
  content — that silently discards the other person's work.
- **Fail closed on privacy:** if either side has `visibility: private`, keep it
  private.
- If you cannot safely resolve a file, leave it conflicted, tell the founder
  exactly which file and why, and stop rather than guess.
