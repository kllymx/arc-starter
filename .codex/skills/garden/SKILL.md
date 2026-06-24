---
name: garden
description: Lightweight daily wiki garden pass. Surfaces stale notes, orphans, weak links, sparse stubs, and daily promote candidates in wiki/garden-{date}.md for founder review before applying. Trigger when the user asks to garden the wiki, run daily maintenance, declutter the wiki, or uses "/garden".
metadata:
  short-description: Daily wiki hygiene pass — structural draft for review, never auto-applies
---

# garden

Run a lightweight maintenance pass over the wiki. The goal is quick hygiene
between heavyweight `consolidate` runs — surfacing stale notes, weak links,
orphans, low-signal stubs, and daily-log promote candidates for the founder
to approve.

This skill **never modifies the wiki directly**. It runs structural detection
via `scripts/garden.py`, then optionally enriches the draft with LLM
judgement. Only after the founder approves do you apply changes.

## When to run

Founder invokes this daily or every few days — the "7am garden" pattern
between big consolidations. Suggest it during `reflect` if you notice:

- Articles with old `updated:` frontmatter dates
- Orphan pages with no inbound links
- Sparse stubs under 200 words
- Recent `daily/` logs not yet compiled into the wiki
- Missing reciprocal [[wikilinks]] between related articles

If the wiki is empty, the script still writes a short draft saying there's
nothing to garden yet.

## Before You Start

Read:

- `context/workspace.md`, `context/overview.md`, `context/memory.md`
- `wiki/index.md`
- Recent `daily/` logs (last 30 days) and `wiki/log.md`

---

## Step 1 — Structural pass (script)

```bash
uv run python scripts/garden.py
```

Writes `wiki/garden-{YYYY-MM-DD}.md` with checklist items grouped as:

- **Archive** — stale articles (default: not updated in 60+ days)
- **Re-link** — orphans and missing backlinks
- **Promote** — recent uncompiled daily logs
- **Prune** — sparse / low-signal stubs

The script does **not** modify any existing wiki article.

## Step 2 — Agent review (optional enrichment)

Read the draft. Optionally enrich with LLM judgement on what's truly
low-signal vs intentional. Add brief rationale to high-signal items. Keep
the pass light — 3–7 minutes, not a full consolidation.

## Step 3 — Present to founder

Tell the founder where the draft lives, give a 1-line gist, and ask which
checklist items to apply. **Do not apply anything until they confirm.**

## Applying approved changes

When the founder approves:

1. Apply file changes in `wiki/concepts/`, `wiki/connections/`, or `wiki/qa/`
2. Update `wiki/index.md`
3. Append a garden entry to `wiki/log.md`
4. Move the draft to `wiki/garden-archive/{date}.md`

## Constraints

- Never auto-apply. Always require approval.
- Preserve the founder's voice — first-person prose stays exact.
- Don't edit `daily/`. Don't touch `imports/`.
- One pass per session — garden review should stay fast.

## Trigger examples

- "garden the wiki"
- "run daily maintenance on the wiki"
- "declutter the wiki"
- "/garden"