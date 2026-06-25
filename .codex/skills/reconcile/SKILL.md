---
name: reconcile
description: LLM-assisted resolution of git merge/rebase conflicts in the ARC wiki. Unions additive knowledge, flags genuine contradictions for the founder, and continues the operation. Trigger on "fix the conflicts", "reconcile", "merge these changes", or when a rebase/merge is in progress with unmerged paths.
metadata:
  short-description: Smart, union-first conflict resolution for the shared wiki
---

# reconcile

Resolve git conflicts in the ARC knowledge base intelligently. The wiki is an
**additive** knowledge base, so most conflicts are two people adding different
things to the same article — UNION them, don't choose between them. Only genuine
semantic contradictions need a human decision. Usually triggered from `sync` when a
rebase onto `main` hits conflicts.

## Step 1 — Survey

```bash
uv run python scripts/conflicts.py state    # rebase | merge | none
uv run python scripts/conflicts.py list     # conflicted paths
```

If nothing is conflicted, say so and stop.

## Step 2 — Resolve each file

```bash
uv run python scripts/conflicts.py show <path>   # prints base / ours / theirs
```

- **Wiki article / index / log / context (common case):** UNION the content. Keep
  every distinct fact, article, and `[[wikilink]]` from both sides; dedupe identical
  lines; preserve the founder's first-person voice. For `index.md`/`log.md`, keep all
  entries from both sides.
- **Genuine contradiction** (incompatible facts — a different price, a reversed
  decision): keep both, mark `> ⚠ Conflict: [ours] vs [theirs] — which is right?`,
  and ask the founder. Never silently pick.
- **Frontmatter:** keep the latest `updated:`, union `tags`, and if either side is
  `visibility: private`, the merged article stays private (fail-closed).

Then `git add <path>`.

## Step 3 — Continue

```bash
git rebase --continue   # (rebase)   — or —   git commit --no-edit   # (merge)
```

Repeat from Step 1 if more conflicts surface.

## Rules

- Never drop knowledge — when unsure, keep both sides.
- Never resolve wiki content with blanket `-X ours/theirs`.
- Fail closed on privacy.
- If you can't safely resolve a file, leave it, name it, and stop.

## Trigger examples

- "reconcile the conflicts"
- "merge these changes"
- "/reconcile"
