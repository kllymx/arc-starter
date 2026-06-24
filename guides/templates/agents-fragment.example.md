# AGENTS.md Fragment — TEMPLATE (merge into your `AGENTS.md`)

> **Portable fragment for cross-tool parity.** `AGENTS.md` is the emerging cross-tool
> standard (Cursor, Codex, Grok Build, and others). Claude Code reads `CLAUDE.md`;
> most other harnesses read `AGENTS.md`. Keep both in sync — or paste this block into
> an existing `AGENTS.md` under a `## Context Hygiene` heading.
>
> Source: cross-tool portability discussed widely in 2026 (e.g. @WenchangYue, Jun 2026).

---

## Context Hygiene (add to AGENTS.md)

Fight **context rot** — performance degradation as the session window fills (~50–60% full is a common pain point). Keep instruction files **under ~200 lines**.

### Layered memory

| Layer | Location | Purpose |
|---|---|---|
| Constitution | `CLAUDE.md` / `AGENTS.md` | How the agent behaves |
| Working preferences | `context/memory.md` | Tone, corrections — not business facts |
| Durable knowledge | `wiki/` | Business facts, filed syntheses |
| Raw capture | `daily/`, `imports/` | Immutable inputs — read only |

Prefer inspectable plain markdown over opaque built-in agent memory.

### Session habits

1. **Lean start** — rely on lean SessionStart injection (overview + memory + index navigation). Do not paste the whole wiki into the first message.
2. **On-demand retrieval** — query or read specific wiki articles when needed; avoid bulk-loading concepts into context.
3. **Sub-agent delegation** — spawn sub-agents for multi-file research, exploration, and consolidate phases. Pass paths, not contents. Summarize back to the main thread.
4. **Dump and clear** — when the thread is stale, write state to markdown, then clear/rewind and continue from the file.
5. **Edit the prompt** — rewrite the opening instruction instead of stacking corrections.
6. **Garden pass** — run `/garden` for light wiki hygiene between heavier `/consolidate` runs. Both produce drafts for founder approval — never auto-apply.

### Wiki discipline (summary)

- Atomic notes with `[[kebab-case]]` wikilinks
- File syntheses back (compounding rule): connections, qa, or concept updates
- Update `wiki/index.md` and `wiki/log.md` on every wiki change
- Infer durability tiers (permanent / active / ephemeral) — protect permanent during consolidation

### Memory vs wiki

- Founder preference or correction → `context/memory.md`
- Business fact or strategic insight → wiki article
- When unsure, check `wiki/index.md` before asking the founder to repeat

---

## Sync Reminder

If you edit `CLAUDE.md`, mirror substantive changes in `AGENTS.md` (and vice versa). For a full constitution template, see `guides/templates/CLAUDE.md.example`. For memory scope, see `guides/templates/memory.md.example`. For the founder-facing guide, see `guides/context-hygiene.md`.