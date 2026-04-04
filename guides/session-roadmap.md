# Session Roadmap

This guide explains how ARC is meant to grow across the workshop series without turning the starter into a giant all-in-one system.

---

## The Principle

ARC should stay simple at the surface and get more powerful in layers.

That means:
- Session 1 gives you the core workspace
- Session 2 adds workflow power
- Session 3 adds systems, approvals, and remote interaction

The goal is not to install everything on day one.

---

## Session 1 — ARC Starter

This is the base repo.

What it should do:
- load business context
- give you a first win
- help you brainstorm and explore workflows
- create a clean local operating layer

This repo should remain:
- easy to understand
- usable in Claude Code or Codex
- mostly file-based
- light on infrastructure

---

## Session 2 — Workflow Pack

Session 2 should build on the starter, not replace it.

The best structure is probably a separate repo or pack that overlays new files onto the Session 1 workspace.

Recommended additions in Session 2:
- more structured workflow commands
- reflection and promotion workflows
- curated MCP and skill patterns
- workflow templates
- stronger output reuse

This should still preserve the founder's existing:
- `context/`
- `explorations/`
- imports
- prior outputs

In other words, Session 2 should extend the workspace they already built.

---

## Session 3 — Systems Pack

Session 3 should introduce the transition from personal workflow use to team/system use.

Recommended additions in Session 3:
- permissions and approval models
- remote interaction
- read vs draft vs send boundaries
- team-facing workflows
- simple proactive summaries or briefings

This is the right point to introduce remote interfaces like:
- Slack
- Telegram
- email briefings

Default recommendation:
- Slack first for teams and operators
- Telegram optional for solo/mobile use

---

## Recommended Install Model

To keep ARC compatible with both Claude Code and Codex, the install model should stay file-based and agent-friendly.

Recommended pattern:

1. Founder starts with the base `arc-starter` repo
2. In Session 2 or 3, the founder tells the agent to install the relevant pack
3. The agent clones or fetches the pack into a temporary folder
4. The agent previews what will be added or changed
5. The agent copies in additive files while preserving the founder's local state

The agent should preserve:
- `context/*`
- `explorations/*`
- founder-created commands
- any founder-specific outputs

The packs should mostly add:
- new commands
- new guides
- templates
- scripts
- extension instructions

This keeps the founder's workspace continuous across sessions.

---

## Extension Instructions

The cleanest way to support packs is to let ARC read optional instructions from `extensions/active/*.md`.

That means:
- the base starter stays stable
- Session 2 and Session 3 packs can add capabilities without replacing the starter instructions
- both Claude Code and Codex can keep using the same workspace model

This is better than replacing `CLAUDE.md` or `AGENTS.md` every session.

---

## Provider and Runtime Flexibility

The workspace itself should remain provider-agnostic as much as possible.

That means the long-term ARC architecture should separate:
- the **workspace** and memory files
- the **commands and workflow logic**
- the **remote bridge/runtime**

That makes it possible later to support:
- Claude Code
- Codex
- a custom remote bridge
- a different authenticated runtime or provider layer

The workspace should be the durable asset. The runtime should be swappable.

---

## What Not To Do

Avoid:
- turning Session 1 into a giant second-brain system
- replacing the starter repo every session
- locking ARC to one model provider
- introducing broad automation before permissions are clear

The right pattern is:

starter first  
workflow pack second  
systems pack third
