# Session 3 Overlay — Always-On Systems & Consolidation

This file extends the base CLAUDE.md / AGENTS.md instructions with
behaviors introduced in Session 3 of the ARC workshop. It's read at
the start of every session as part of the `extensions/active/` overlay
system.

---

## The Three-Layer Frame, Updated

Sessions 1 and 2 built the first two layers: **context** (you know the
business) and **workflows** (you do real work for the founder). Session
3 adds the third: **always-on**.

That means:

- The wiki should grow even when the founder isn't actively prompting you
- Periodic maintenance (`/consolidate`) keeps the wiki sharp instead of bloated
- The founder may now run you in cloud sessions, Routines, or via
  Channels — same skills, different surfaces

Always-on **does not** mean always-autonomous. The trust gradient still
applies. Default to draft-only for anything outbound; autonomy is
earned over time.

---

## Tier-Thinking (Without Folder Changes)

Wiki articles have an effective tier based on durability, even though
the folder structure doesn't enforce it:

- **Permanent** — durable principles, foundational facts about the
  business, things unlikely to change
- **Active** — current strategy, current tools, current priorities;
  likely correct now, may shift in 6+ months
- **Ephemeral** — short-lived captures from recent conversations,
  candidates for promotion or pruning

You infer tier from:

- The article's `updated:` date relative to today
- How often other articles link to it (incoming references)
- The article type (`type:` frontmatter field)
- The founder's `context/memory.md` (if they explicitly marked
  something as permanent)

**You don't mark tiers explicitly.** Inference is enough. Tier is a
lens for `/consolidate`, not a folder structure.

When `/consolidate` runs, it weights proposals by inferred tier:

- Permanent articles get protected — propose merges only with strong evidence
- Active articles get reviewed for stale claims and cross-links
- Ephemeral articles get aggressive pruning if they haven't accumulated
  references

---

## When to Suggest /consolidate

Proactively suggest the founder run `/consolidate` when:

- The wiki has 30+ articles and hasn't been consolidated in 4+ weeks
- During `/reflect`, you notice 3+ flagged contradictions in `wiki/log.md`
- Multiple recent articles cover ground that an existing article
  already covered
- The founder asks "is my wiki getting bloated?"

Don't run `/consolidate` automatically. Always suggest, always wait for
the founder to invoke.

---

## Capture-On-Request in Cloud Sessions

In cloud sessions (`claude.ai/code`, Codex cloud) and Routines, the
founder may ask you to save something to the wiki mid-conversation.
Recognize these triggers:

- *"Save this to my wiki"*
- *"Add this to my context"*
- *"Remember this"*
- *"Update [file] with this"*

When triggered:

1. Pull the latest main branch (`git pull --rebase --autostash`)
2. Write the new content to the appropriate wiki location (or update
   an existing article)
3. Update `wiki/index.md`
4. Append to `wiki/log.md`
5. Commit and push (via `/sync` or directly)
6. Confirm: *"Saved. You'll see it on your laptop next session."*

This is the only path that lets cloud sessions modify the wiki.
Without an explicit trigger phrase, cloud sessions stay read-only on
the wiki.

---

## Sub-Agents (When Available)

In Claude Code (with sub-agents) and Codex (with custom agents in
`.codex/agents/`), spawning a sub-agent is appropriate when:

- The task requires extensive codebase exploration that would bloat
  the main context
- Multiple independent research questions can run in parallel
- A specialized agent (defined per harness) is a better fit than the
  general assistant
- The founder explicitly asks for one

Sub-agents consume more tokens than equivalent single-agent runs. Use
deliberately. Don't spawn one for tasks the main agent can handle in
2–3 turns.

If you spawn sub-agents, summarize their findings yourself before
reporting back. Don't dump raw sub-agent output on the founder —
synthesize.

---

## Routines Awareness (Claude)

If the founder mentions Claude Routines:

- Routines are scheduled cloud sessions (Claude-only — Codex's
  Automations run locally instead)
- They run on Anthropic infrastructure, not the founder's laptop
- They have access to account-level Connectors (which interactive
  cloud sessions do **not**)
- They run unattended; the founder can't intervene mid-run
- Permissions are configured per routine; default to read-only
  connector access unless the founder grants writes explicitly

When suggesting a Routine for a workflow:

- Confirm it's been run successfully at least 3 times manually first
- Recommend draft-only outputs for the first 2–4 weeks
- Pick connectors deliberately — only what the routine actually needs
- Schedule to match actual cadence (daily briefs at a reasonable hour,
  weekly reports on Mondays, etc.)

---

## Auto-Pull / Auto-Push Hooks

The session-start hook runs `git-pull.sh` quietly. The session-end
hook (Claude only) runs `git-push.sh`. Both gracefully no-op if:

- Not a git repo
- No `origin` remote configured
- Working tree dirty (pull only)
- Auth fails (silent failure, log to `.claude/last-sync.log`)

Founders without GitHub keep working locally — the hooks just do
nothing. The `/sync` command is the manual path for Codex users (whose
`Stop` event fires per-turn and isn't suitable for auto-push).

If a founder asks why something isn't pushing, check:

1. `git remote -v` — is origin configured?
2. `git status` — is there anything to push?
3. `.claude/last-sync.log` — what was the last error?
4. `gh repo view --json visibility,permissions` — do they have push
   access? If origin points to the upstream `kllymx/arc-starter`, they
   don't.

---

## Failure-Recovery Stance

Things will go wrong. The Session 3 mindset:

- **Stale context** → suggest `/consolidate` or `/reflect`
- **Wrong recipient drafted** → keep agent in draft-only mode for
  outbound; never auto-send
- **Hallucinated commitment** → human-in-loop on anything that touches
  a customer or partner
- **Connector outage** → Routines retry; alert if persistent
- **Cloud session can't reach Gmail** → expected; cloud interactive
  sessions are bounded by repo. Suggest the Routine path or local

When you encounter a failure that suggests a process change (e.g.,
"we keep CCing the wrong person on briefs"), proactively suggest a
workflow refinement to prevent recurrence.
