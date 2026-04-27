---
description: Three-phase wiki consolidation. Drafts proposed merges, edits, prunes, and promotions to wiki/consolidation-{date}.md for founder review before applying.
---

# /consolidate

Run a three-phase consolidation pass over the wiki. The goal is to keep
the knowledge base sharp by surfacing duplicates, contradictions, and
stale content — and proposing fixes for the founder to approve.

This command **never modifies the wiki directly**. It writes a draft to
`wiki/consolidation-{YYYY-MM-DD}.md`. Only after the founder approves
do you apply the changes.

## When to run

Founder invokes this every 2–4 weeks for a healthy wiki. You can also
suggest it during `/reflect` if you notice:

- Multiple articles covering overlapping ground
- Articles flagged as contradictory in `wiki/log.md`
- Articles unchanged for 90+ days but still relevant
- `wiki/concepts/` has grown past 30+ articles without a recent cleanup

If the wiki has fewer than 10 articles, decline gracefully — there's
not enough to consolidate yet.

## Use sub-agents for large wikis

**If the wiki has more than ~30 articles, use sub-agents.** A single
conversation can't hold 100+ articles in context without quality loss,
and you'll burn through the window before reaching the Judge phase.

### Critical: keep spawn prompts small

The most common failure mode is "prompt is too long" when spawning a
sub-agent. This happens when the parent embeds article CONTENT in the
spawn prompt instead of just paths. **Don't do that.**

- The parent does NOT read articles itself in Phase 1. Read only
  `wiki/index.md`, `wiki/log.md`, and recent `daily/` logs to scope
  the work and identify which paths to assign.
- Pass each sub-agent only **file paths**, not file contents. Each
  sub-agent uses its own Read/Glob tools to load its assigned files
  inside its own context window.
- Each sub-agent returns a **small structured summary** (a few
  hundred tokens of JSON or markdown), not full article content.

If the parent has somehow already loaded article content into context,
clear that context (or drop it from the spawn prompt) before spawning.

### Use the named sub-agents (not generic Task)

Spawn the dedicated sub-agents shipped with the starter:

- `.claude/agents/wiki-reader.md` — restricted to `Read, Glob, Grep`.
  No MCPs in its system prompt. Spawns reliably even in MCP-heavy
  sessions (the most common failure mode for generic Task spawns is
  the parent's MCP toolset bloating the sub-agent's system prompt
  past the budget at startup).
- `.claude/agents/wiki-adversary.md` — same restricted toolset.

Invoke via the Task tool with `subagent_type: "wiki-reader"` and
`subagent_type: "wiki-adversary"` respectively. Don't use generic Task
spawns — they inherit the full session toolset and will fail with
"prompt is too long" before processing.

### The pattern

- **Phase 1 (Proposer)** — split article paths into batches of 10–15.
  Spawn parallel `wiki-reader` sub-agents, each given:
  - the list of file paths for its batch (paths only, no content)
  - the structured-summary format to return
  Each returns a small JSON array of `(title, type, updated,
  key_claims, references, candidate_flags)` per article. Main agent
  collects summaries (NOT article content) and identifies cross-batch
  patterns (duplicates, contradictions, orphans).
- **Phase 2 (Adversary)** — spawn ONE `wiki-adversary` sub-agent.
  Pass it ONLY the proposals from Phase 1 (a few KB of structured
  text, not article content). Its job: challenge each proposal
  independently. Returns JSON array with `keep / modify / drop`
  verdict per proposal and reason. Fresh context is the point — it
  can't get talked into a bad merge by the Proposer's reasoning. If
  a proposal needs deeper context, the adversary reads articles
  itself with its restricted file tools.
- **Phase 3 (Judge)** — run in the main conversation. The main agent
  now holds proposals and challenges (both small structured payloads),
  reads any specific articles needed for final wording, and writes
  the draft.

### Fallback if sub-agents aren't available

If the harness doesn't expose Task tool / `spawn_agent` (older Claude
Desktop, or Codex without sub-agent support), process in chunks within
the main conversation: read 20 articles → summarize to a small
structured note → clear that context → read next 20. Slower and
rougher, but works.

### Skip for small wikis

For wikis under ~30 articles, sub-agents are overkill — run all three
phases in one cohesive pass in the main conversation.

---

## Phase 1 — Proposer

Read the wiki end to end (directly, or via reader sub-agents per above):

1. `wiki/index.md` — full catalog
2. `wiki/log.md` — recent operations and any flagged contradictions
3. `wiki/concepts/` — all atomic articles
4. `wiki/connections/` — all cross-cutting articles
5. `wiki/qa/` — filed Q&A entries (if present)
6. Recent `daily/` logs (last 30 days) — what the founder's been working on

Then propose:

- **Merge candidates** — pairs/triples covering overlapping ground
- **Edit candidates** — articles partially stale, contradicted, or missing context
- **Prune candidates** — articles no longer relevant (founder pivoted, tool deprecated)
- **Promote candidates** — recent daily-log captures that have proven durable
- **Cross-link candidates** — pairs that should reference each other but don't

For each, write a 2–3 sentence rationale.

Pick **5–10 highest-impact proposals**. Don't be exhaustive — a
consolidation pass is a sharp edit, not a churn.

## Phase 2 — Adversary

Play devil's advocate against your own proposals. For each:

- **What nuance does this lose?** Merging often flattens real distinctions.
- **What evidence supports the change?** Real contradiction, or two valid framings?
- **Is the founder's intent at stake?** Some "duplication" is intentional.
- **Is this contradiction or evolution?** Old vs new position is sometimes the point.

For each proposal: defend, withdraw, or modify. Be skeptical. The
default outcome should be "fewer changes than initially proposed."

## Phase 3 — Judge

For each surviving proposal, write the **exact change** as a draft:

- **Merges**: write the merged article in full, citing originals
- **Edits**: write the new version of the article in full
- **Prunes**: write path + short reason
- **Promotions**: write the new article in full
- **Cross-links**: list pairs and specific links to add

Output to `wiki/consolidation-{YYYY-MM-DD}.md`:

```markdown
# Consolidation Draft — YYYY-MM-DD

> Generated by `/consolidate`. **Not yet applied.** To apply: tell me
> which proposals to keep. To skip everything: delete this file.

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

---

## Proposal 2 — ...
```

Order proposals by **impact** — highest-leverage first.

## After writing the draft

Tell the founder:

> "I drafted [N] consolidation proposals at `wiki/consolidation-{date}.md`.
> Gist: [1-line summary]. Review when you have 10 minutes. To apply some
> or all, say which ones — or 'apply all' if it all looks right. To skip
> everything, delete the file."

**Do not apply anything yet.** Wait for the founder to approve.

## Applying approved changes

When the founder approves a subset (or all):

1. Make the file changes in `wiki/concepts/` or `wiki/connections/`
2. Update `wiki/index.md` with adds/removes/renames
3. Update `wiki/log.md` with a consolidation entry:

   ```markdown
   ## YYYY-MM-DD consolidation | Applied N proposals
   - Merged: [[A]] + [[B]] → [[A]]
   - Edited: [[C]] (resolved contradiction with daily/2026-04-15.md)
   - Pruned: [[D]] (no longer relevant after pivot)
   - Promoted: daily/2026-04-15.md insight → [[New Article]]
   - Linked: [[E]] ↔ [[F]]
   ```

4. Move the draft to `wiki/consolidation-archive/{date}.md` (create dir if needed)

## Constraints

- **Never auto-apply.** Always require approval, even for changes that look obviously right.
- **Preserve attribution.** When merging, note which originals contributed.
- **Preserve the founder's voice.** First-person prose stays exactly as written.
- **Don't consolidate `daily/`.** Daily logs are immutable raw sources.
- **Don't touch `imports/`.** External documents stay as-is.
- **One pass per session.** Consolidation is mentally heavy for the founder to review.

## When this goes wrong

If you find yourself proposing 20+ changes, stop. Cut to the top 5–10
and tell the founder the rest can wait for the next pass.

If the founder says "apply all" without reviewing: gently push back.
*"This is 12 proposals — would you like to skim the top 3 first?"*
