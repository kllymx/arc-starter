# /reflect — Review, Compile, and Grow the Wiki

You are helping a founder make ARC smarter by reviewing what has happened recently and compiling durable knowledge into the wiki. This is the manual version of what the hooks do automatically — use it when you want a thorough, deliberate review.

---

## Before You Start

Read the context files:
- `context/workspace.md`
- `context/overview.md`
- `context/memory.md`

Read the wiki:
- `wiki/index.md`

Then check for recent material to review:
- `daily/` — recent session logs (the richest source of new knowledge)
- wiki articles with `type: exploration` that may have new insights
- recent files in `imports/` that may not have been ingested yet
- the current conversation itself

If there is no meaningful context loaded yet, stop and suggest running setup first.

---

## What Reflect Does

### 1. Review Recent Activity

Look for:
- **New business facts** — things the founder mentioned that aren't in the wiki yet
- **Changed priorities** — shifts in focus, new bottlenecks, resolved problems
- **Decisions made** — strategic choices that should be recorded
- **Lessons learned** — what worked, what didn't, what to avoid
- **Corrections** — mistakes you made and what the founder wanted instead
- **New concepts** — ideas, tools, strategies, or entities that deserve their own wiki article
- **New connections** — relationships between concepts that weren't previously documented
- **Stale content** — wiki articles that are now outdated

### 2. Compile into the Wiki

For each piece of durable knowledge:
- **Create new articles** in `wiki/concepts/` or `wiki/connections/` if the knowledge is substantial enough
- **Update existing articles** if the new information refines or extends what's already there
- **Flag contradictions** if new information conflicts with existing wiki content
- **Add cross-references** — update `[[wikilinks]]` in both new and existing articles

### 3. Update Supporting Files

- **`wiki/index.md`** — add any new articles, update summaries for modified ones
- **`wiki/log.md`** — append a reflection entry with what changed
- **`context/overview.md`** — update if priorities, bottlenecks, or the business snapshot has shifted
- **`context/memory.md`** — add any new preferences or corrections

---

## Output Format

Present a short review to the founder:

### What's New
- [new knowledge compiled into the wiki]

### What Changed
- [updated articles or shifted priorities]

### What to Watch
- [contradictions, stale content, or gaps worth investigating]

### Suggested Next Steps
- [workflow candidates, research questions, or actions worth exploring]

Then ask:

> "I've updated the wiki with [X] new articles and [Y] updates. Want me to walk through any of the changes?"

---

## Good Judgment

- Only create articles for durable knowledge — not every conversation detail deserves a wiki page.
- Prefer updating existing articles over creating new ones when the information fits.
- Keep corrections in `context/memory.md`, not in the wiki. The wiki stores business knowledge; memory stores agent behavior.
- If the daily logs have already been compiled by the automated hooks, don't double-process them — focus on what the hooks may have missed.
- If there is no durable learning, say so plainly. Do not force updates just because the command was run.
