---
description: Lightweight daily wiki garden pass. Surfaces hygiene issues and writes wiki/garden-{date}.md for founder review — never auto-applies.
---

# /garden

Run a lightweight maintenance pass over the wiki. The goal is quick hygiene
between heavyweight `/consolidate` runs — surfacing stale notes, weak links,
orphans, low-signal stubs, and daily-log promote candidates for the founder
to approve.

This command **never modifies the wiki directly**. It runs structural
detection via `scripts/garden.py`, then optionally enriches the draft with
LLM judgement. Only after the founder approves do you apply changes.

## When to run

Founder invokes this daily or every few days — the "7am garden" pattern
between big consolidations. Suggest it during `/reflect` if you notice:

- Articles with old `updated:` frontmatter dates
- Orphan pages with no inbound links
- Sparse stubs under 200 words
- Recent `daily/` logs not yet compiled into the wiki
- Missing reciprocal [[wikilinks]] between related articles

If the wiki is empty, the script still writes a short draft saying there's
nothing to garden yet.

## Before You Start

Read the context files:

- `context/workspace.md`
- `context/overview.md`
- `context/memory.md`

Read the wiki:

- `wiki/index.md`

Then check recent material:

- `daily/` — last 30 days of session logs (promote candidates)
- `wiki/log.md` — recent operations

---

## Step 1 — Structural pass (script)

Run the structural helper:

```bash
uv run python scripts/garden.py
```

This writes `wiki/garden-{YYYY-MM-DD}.md` with checklist items grouped as:

- **Archive** — stale articles (default: not updated in 60+ days)
- **Re-link** — orphans and missing backlinks
- **Promote** — recent uncompiled daily logs
- **Prune** — sparse / low-signal stubs

The script does **not** modify any existing wiki article.

## Step 2 — Agent review (optional enrichment)

Read the draft the script produced. Optionally enrich it with LLM judgement:

- Which sparse notes are intentional stubs vs true prune candidates?
- Which stale articles are still relevant reference vs archive fodder?
- Which daily-log insights are durable enough to promote?

Add brief rationale to high-signal items. **Do not remove** script-detected
items without noting why — the founder should see the full structural picture.

Keep the pass light: 3–7 minutes of review, not a full consolidation.

## Step 3 — Present to founder

Tell the founder:

> "I drafted a garden pass at `wiki/garden-{date}.md`. Gist: [1-line summary].
> Review when you have a few minutes. To apply some or all checklist items,
> say which ones — or 'apply all' if it looks right. To skip everything,
> delete the file."

**Do not apply anything yet.** Wait for founder approval.

## Applying approved changes

When the founder approves a subset (or all):

1. Make the approved file changes in `wiki/concepts/`, `wiki/connections/`,
   or `wiki/qa/` as appropriate
2. Update `wiki/index.md` with adds/removes/renames
3. Append a garden entry to `wiki/log.md`:

   ```markdown
   ## YYYY-MM-DD garden | Applied N checklist items
   - Archived: [[article]] (stale, superseded by daily/...)
   - Re-linked: [[A]] ↔ [[B]]
   - Promoted: daily/YYYY-MM-DD.md insight → [[New Article]]
   - Pruned: [[stub]] (low-signal ephemeral note)
   ```

4. Move the draft to `wiki/garden-archive/{date}.md` (create dir if needed)

## Constraints

- **Never auto-apply.** Always require approval, even for obvious hygiene fixes.
- **Preserve the founder's voice.** First-person prose stays exactly as written.
- **Don't edit `daily/`.** Daily logs are immutable raw sources.
- **Don't touch `imports/`.** External documents stay as-is.
- **One pass per session.** Garden review should stay fast.

## When this goes wrong

If the draft lists 15+ items, highlight the top 5 and tell the founder the
rest can wait. If structural detection looks noisy on a young wiki, say so
and suggest waiting until `/setup` and a few `/reflect` passes have built
more substance.
