# Context Hygiene — Keeping Your Agent Sharp

## What Is Context Rot?

As a coding-agent session grows, the model's effective attention spreads thin. Practitioners call this **context rot**: performance drops well before you hit the hard token limit.

Rough thresholds people cite (Jun 2026):

- **~50–60% of the context window filled** — quality often starts slipping
- **~300–400k tokens** in very long sessions — "lost in the middle," distractor interference, and the feeling that the agent "got dumber" or "needs a rest"

**Symptoms you might notice:**

- The agent forgets decisions from earlier in the session
- It re-reads files you already discussed
- Corrections pile up but behavior doesn't improve
- Answers get generic instead of grounded in your wiki
- Tool calls multiply without progress

Context rot is not a bug in one harness — it's how large language models handle long windows. The fix is **context engineering**: keep the active window small and high-signal.

---

## The Fixes (What Practitioners Actually Do)

### 1. Keep instruction files short and scoped

Target **under ~200 lines** per `CLAUDE.md`, `AGENTS.md`, or project memory file. Split concerns across files instead of one giant constitution. Huge files go stale and load on every session whether you need them or not.

*Community consensus, Jun 2026 — e.g. @techNmak, @siddharthakat25.*

### 2. Delegate research to sub-agents

Spawn a sub-agent for exploration, file investigation, or wiki research. The sub-agent burns its own context window; the main session stays clean. Summarize findings back — don't paste raw sub-agent dumps into the main thread.

*@Suryanshti777 (Mar/Apr 2026); widely echoed in Jun 2026 hygiene posts.*

### 3. Dump to file, then clear

When a session is long or polluted, write the important state to a markdown file (decisions, open questions, next steps), then **clear or rewind** the conversation and continue from the file. ARC's `daily/` logs and wiki are built for this — capture durable output, start fresh.

*@JustAnotherPM, @cmd_alt_ecs, @svpino (Jun 2026).*

### 4. Edit the original prompt — don't stack corrections

Appending "no, I meant X" ten times forces the model to re-read a polluted history. **Rewrite the opening instruction** or start a new session with a clean, complete prompt. Fewer words, higher signal.

### 5. Pull knowledge on demand — don't dump everything upfront

Read `wiki/index.md` for navigation, then open **only the articles you need**. Atomic wiki notes (one concept per file) compound better than pasting whole vaults into context.

*Karpathy-style compile wiki pattern; @siddharthakat25 ContextOS (Jun 2026) for targeted retrieval.*

### 6. Separate instructions from facts

- **CLAUDE.md / AGENTS.md** — how the agent should behave (constitution)
- **context/memory.md** — lightweight preferences and corrections
- **wiki/** — business facts, strategy, entities (the durable knowledge store)

Opaque "agent memory" that you can't inspect or share is widely discouraged. Plain markdown in git wins.

*@mlafeldt (Jun 18, 2026); @WenchangYue on AGENTS.md portability (Jun 21, 2026).*

---

## How ARC Fights Rot

ARC is designed around lean context and compounding markdown — but you still need hygiene habits. Three framework features work together:

| Feature | What it does |
|---|---|
| **Lean SessionStart injection** | At session start, inject only a high-signal core: overview, memory, index *navigation* (descriptions, not full articles), and short recent-activity excerpts — not the whole wiki or every daily log. |
| **On-demand retrieval** | When you need depth, query the wiki for relevant slices (title, summary, excerpt) instead of reading dozens of files into context. Pull full articles only when necessary. |
| **Garden pass** | A lightweight `/garden` maintenance routine surfaces stale, orphaned, or low-signal wiki content as a **draft for your approval** — fighting slow rot between heavier `/consolidate` runs. |

Together: **start lean → retrieve on demand → garden periodically → file durable answers back to the wiki.**

---

## Practical Habits for Founders

**Start sessions clean.** Let SessionStart inject the snapshot; don't paste your entire wiki into the first message.

**Use sub-agents for research.** "Explore competitors in the EU market" is a good sub-agent task. "Update this one function" is not.

**End long sessions deliberately.** On Codex, run `/reflect` to flush the final stretch into your daily log. On Claude Code, SessionEnd capture handles most of this — but if the thread feels stale, dump state and start fresh.

**Keep memory.md short.** If a "fact" belongs in the business, promote it to a wiki article during `/reflect` or `/ingest`. Memory is for *how* the agent works with you, not *what* your business is.

**Review huge instruction files.** If `CLAUDE.md` or `AGENTS.md` grows past ~200 lines, split scoped fragments or trim stale sections. See the templates in `guides/templates/`.

---

## When to Start a Fresh Session

Good signals:

- You've been correcting the same mistake repeatedly
- The agent keeps re-reading the same files
- You're switching to a unrelated task (strategy → code → email drafts)
- The conversation is past an hour of heavy tool use

Before clearing: ensure hooks have captured what matters (`daily/` will have session slices if capture is set up). Write a one-paragraph handoff if something is mid-flight.

---

## Templates and Further Reading

Ready-to-use scoped examples live in `guides/templates/`:

- `CLAUDE.md.example` — a under-200-line constitution template with ARC patterns
- `memory.md.example` — preferences vs corrections vs wiki facts
- `agents-fragment.example.md` — portable `AGENTS.md` fragment for cross-tool parity

For the research behind these recommendations, see the ARC improvement research notes on context rot, short files, and stale memory (community sources collected Jun 2026).