# Session Roadmap

This guide explains how ARC grows across the workshop series.

---

## The Principle

ARC should stay simple at the surface and get more powerful in layers.

- Session 1 gives you the core workspace with a compounding wiki
- Session 2 adds workflow power and deeper integrations
- Session 3 adds systems, approvals, and remote interaction

---

## Session 1 — ARC Starter + Wiki Foundation

This is the base repo. What it does from day one:

- Interviews you and builds a cross-referenced wiki about your business
- Gives you a first win immediately after setup
- Helps you brainstorm, audit, and explore workflows
- Automatically captures session knowledge via hooks
- Compiles conversation insights into wiki articles overnight
- Gets smarter every session through the compounding loop

The wiki starts compounding from the moment you run setup. Every question, every exploration, every document you import makes it richer.

**Key operations available in Session 1:**
- `/setup` — Build the initial wiki through an interview
- `/first-win` — Get immediate value
- `/brainstorm` — Find automation opportunities
- `/audit` — Systematic task inventory
- `/explore` — Research and spec ideas
- `/ingest` — Process documents into wiki knowledge
- `/reflect` — Manual review and wiki update
- `/lint` — Wiki health check

---

## Session 2 — Workflow Pack

Session 2 builds on the starter, not replaces it.

Recommended additions:
- More structured workflow commands
- Curated MCP and skill patterns (email, calendar, CRM)
- Workflow templates for common founder tasks
- Stronger output reuse — turning first wins into repeatable commands
- External tool integrations connected to the wiki

Session 2 preserves the founder's existing:
- `wiki/` (all articles, index, log)
- `context/` (overview, memory, workspace)
- `explorations/`
- `imports/`
- `daily/` (session logs)

The wiki from Session 1 gives Session 2 workflows deep business context from day one.

---

## Session 3 — Systems Pack

Session 3 introduces the transition from personal to team/system use.

Recommended additions:
- Permissions and approval models
- Remote interaction (Slack, Telegram, email briefings)
- Read vs draft vs send boundaries
- Team-facing workflows
- Proactive summaries and briefings
- Scheduled tasks that query the wiki

The wiki becomes the team knowledge base — always current because the LLM handles maintenance.

---

## Recommended Install Model

To keep ARC compatible with both Claude Code and Codex:

1. Founder starts with `arc-starter` repo
2. In Session 2 or 3, the agent installs the relevant pack
3. Agent previews changes before applying
4. Additive files are copied in; founder's state is preserved

Packs add: new commands, guides, templates, scripts, extension instructions.
Packs preserve: wiki, context, explorations, imports, daily logs, founder-created commands.

---

## Extension Instructions

Session packs add capabilities via `extensions/active/*.md` — additive instructions layered on top of the starter. The base stays stable; packs extend it.

---

## What Not To Do

Avoid:
- Replacing the starter repo every session
- Locking ARC to one model provider
- Introducing broad automation before permissions are clear

The right pattern is:

**wiki foundation first → workflows second → systems third**
