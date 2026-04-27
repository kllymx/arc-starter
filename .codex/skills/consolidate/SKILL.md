---
name: consolidate
description: Three-phase wiki consolidation pass. Drafts proposed merges, edits, prunes, and promotions to wiki/consolidation-{date}.md for founder review before applying. Trigger when the user asks to consolidate the wiki, clean up the wiki, merge duplicate articles, or uses "/consolidate".
metadata:
  short-description: Periodic wiki cleanup pipeline (proposer → adversary → judge), drafts changes for review
---

# consolidate

Run a three-phase consolidation pass over the wiki. The goal is to keep
the knowledge base sharp by surfacing duplicates, contradictions, and
stale content — and proposing fixes for the founder to approve.

This skill **never modifies the wiki directly**. It writes a draft to
`wiki/consolidation-{YYYY-MM-DD}.md`. Only after the founder approves
do you apply the changes.

## When to run

Founder invokes this every 2–4 weeks for a healthy wiki. Suggest it
during `/reflect` if you notice:

- Multiple articles covering overlapping ground
- Articles flagged as contradictory in `wiki/log.md`
- Articles unchanged for 90+ days but still relevant
- `wiki/concepts/` has grown past 30+ articles without recent cleanup

If the wiki has fewer than 10 articles, decline gracefully — not enough
to consolidate yet.

## Use sub-agents for large wikis

**If the wiki has more than ~30 articles, use sub-agents.** A single
turn can't hold 100+ articles in context without quality loss.

### Critical: keep spawn prompts small

The most common failure mode is "prompt is too long" when spawning a
sub-agent. This happens when the parent embeds article CONTENT in the
spawn prompt instead of just paths. **Don't do that.**

- The parent does NOT read articles itself in Phase 1. Read only
  `wiki/index.md`, `wiki/log.md`, and recent `daily/` logs to scope
  the work and identify which paths to assign.
- Pass each sub-agent only **file paths**, not file contents. Each
  sub-agent uses its own tools to load files inside its own context.
- Each sub-agent returns a **small structured summary** (a few
  hundred tokens), not full article content.

If the parent has somehow already loaded article content into context,
clear that context (or omit it from the spawn prompt) before spawning.

### Use the named sub-agents (not generic spawn_agent)

Spawn the dedicated sub-agents shipped with the starter:

- `.codex/agents/wiki-reader.toml` — sandbox `read-only`, restricted
  toolset. Spawns reliably even in MCP-heavy sessions (generic
  `spawn_agent` calls inherit the full session toolset and fail with
  "prompt is too long" at startup).
- `.codex/agents/wiki-adversary.toml` — same restricted setup.

Invoke via `spawn_agent` (or `spawn_agents_on_csv` for batch lists)
naming `wiki_reader` or `wiki_adversary` as the agent name. Don't use
generic spawns.

### The pattern

- **Phase 1 (Proposer)** — split article paths into batches of 10–15.
  Use `spawn_agents_on_csv` (or repeated `spawn_agent`) calling
  `wiki_reader`, each given:
  - the list of file paths for its batch (paths only, no content)
  - the structured-summary format to return
  Each returns a small JSON array of `(title, type, updated,
  key_claims, references, candidate_flags)` per article. Main agent
  collects summaries (NOT article content) and identifies cross-batch
  patterns.
- **Phase 2 (Adversary)** — spawn ONE `wiki_adversary`. Pass it ONLY
  the proposals from Phase 1 (a few KB of structured text, not
  article content). Its job: challenge each independently. Returns
  JSON array with `keep / modify / drop` verdict + reason. If a
  proposal needs deeper context, the adversary reads articles itself.
  Optionally configure the agent with a cheaper model
  (e.g., gpt-5.3-codex-spark) — adversaries don't need full reasoning
  depth.
- **Phase 3 (Judge)** — runs in the main conversation. Main agent has
  proposals + challenges (small structured payloads), reads any
  specific articles needed for final wording, writes the draft.

### Fallback if sub-agents aren't available

If `spawn_agent` isn't available, process in chunks within the main
turn: read 20 articles → summarize to a small structured note → clear
that context → read next 20. Slower and rougher, but works.

### Skip for small wikis

For wikis under ~30 articles, sub-agents are overkill — run all three
phases in one cohesive pass.

---

## Phase 1 — Proposer

Read the wiki end to end (directly, or via reader sub-agents per
above):

1. `wiki/index.md` — full catalog
2. `wiki/log.md` — recent operations and flagged contradictions
3. `wiki/concepts/` — all atomic articles
4. `wiki/connections/` — all cross-cutting articles
5. `wiki/qa/` — filed Q&A (if present)
6. Recent `daily/` logs (last 30 days)

Then propose:

- **Merge candidates** — overlapping articles
- **Edit candidates** — partially stale or contradicted articles
- **Prune candidates** — no-longer-relevant articles
- **Promote candidates** — durable daily-log captures
- **Cross-link candidates** — articles that should reference each other

Each gets a 2–3 sentence rationale. Pick **5–10 highest-impact**
proposals. Don't be exhaustive.

## Phase 2 — Adversary

Challenge each proposal:

- What nuance does this lose?
- Is there real evidence, or two valid framings?
- Does founder intent matter here?
- Is this contradiction or evolution?

For each: defend, withdraw, or modify. Default outcome: fewer changes
than initially proposed.

## Phase 3 — Judge

Write each surviving proposal as the **exact change** in a draft to
`wiki/consolidation-{YYYY-MM-DD}.md`:

```markdown
# Consolidation Draft — YYYY-MM-DD

> Generated by consolidate. Not yet applied. To apply: tell me which
> proposals to keep. To skip: delete this file.

## Summary
- N merges proposed
- N edits proposed
- N prunes proposed
- N promotions proposed
- N cross-links proposed

---

## Proposal 1 — [type]: [short title]
**Affected:** `wiki/concepts/foo.md`, `wiki/concepts/bar.md`
**Why:** [rationale]
**Change:** [full proposed content]
```

Order by impact, highest first.

## After writing the draft

Tell the founder where the draft lives, give a 1-line gist, and ask
which proposals to apply. Do not apply anything until they confirm.

## Applying approved changes

When the founder approves:

1. Apply the file changes in `wiki/concepts/` or `wiki/connections/`
2. Update `wiki/index.md`
3. Append a consolidation entry to `wiki/log.md`
4. Move the draft to `wiki/consolidation-archive/{date}.md`

## Constraints

- Never auto-apply. Always require approval.
- Preserve attribution when merging.
- Preserve the founder's voice — first-person prose stays exact.
- Don't consolidate `daily/`. Don't touch `imports/`.
- One pass per session — review is mentally heavy.

## Trigger examples

- "consolidate the wiki"
- "clean up the wiki"
- "merge duplicate articles"
- "/consolidate"
