---
description: Produce a one-page brief on a client, project, or topic using your context layer
argument-hint: <client, project, or topic>
---

# /brief

Produce a crisp one-page brief on the subject in the argument.
Argument: **$ARGUMENTS**

## What "brief" means

A founder-grade briefing you could read before a meeting, a cold reply,
or a strategic decision. Not a dump of notes. A synthesis.

## Inputs, in order

1. **Your context layer** (this arc-starter folder)
   - `context/` — any canonical note about the subject
   - `wiki/` — accumulated captures, patterns, learnings
   - Linked project or meeting notes if relevant
   - Read the whole relevant corpus. Skim nothing.

2. **Recent meetings** (Granola MCP, if connected)
   - Meetings in the last 30 days involving this subject
   - Summaries + action items only, not full transcripts, unless
     something specific warrants the detail

3. **Recent email threads** (Gmail MCP, if connected)
   - Top 5 most recent threads involving this subject
   - Skim for asks, commitments, open loops

## Output structure

Produce markdown, max 400 words, this shape:

  # Brief — $ARGUMENTS

  ## TL;DR
  One paragraph. What I actually need to know right now.

  ## Where we stand
  Current state of the relationship, project, or topic.
  Last meaningful interaction. Any commitments outstanding.

  ## Open questions
  What's undecided. What's waiting on me. What's waiting on them.

  ## Signal worth remembering
  2-3 bullets of things from the context layer that are
  non-obvious but load-bearing for how I should engage.

  ## Next move
  One recommended action. Not a menu — a pick.

## Tone

Direct. No corporate filler. Writing for myself, not for a report.

## Guardrails

- If the subject isn't in my context layer at all, STOP and tell me.
  Offer to create a stub note. Don't invent the briefing from thin air.
- If multiple entities could match (e.g. two clients named "Acme"),
  list them and ask which one.
- Cite which notes and meetings you used at the bottom, so I can
  verify and go deeper.
