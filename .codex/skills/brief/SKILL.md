---
name: brief
description: Produce a one-page founder-grade brief on a client, project, or topic, synthesised from the user's arc-starter context layer, recent meetings, and recent email threads. Trigger when the user asks to "brief me on <X>", "write a brief on <X>", "summarise what we know about <X>", or uses "/brief <X>".
metadata:
  short-description: One-page founder brief on a client, project, or topic
---

# brief

Produce a crisp one-page brief on the subject the user names. Argument
appears after the trigger.

## What "brief" means

A founder-grade briefing readable before a meeting, a cold reply, or a
strategic decision. A synthesis, not a dump.

## Inputs, in order

1. **The user's context layer** (this arc-starter folder)
   - `context/` — canonical notes on the subject
   - `wiki/` — accumulated captures and patterns
   - Linked project or meeting notes
   - Read the whole relevant corpus.

2. **Recent meetings** (Granola MCP, if connected)
   - Last 30 days involving this subject
   - Summaries + action items, not full transcripts unless warranted

3. **Recent email threads** (Gmail MCP, if connected)
   - Top 5 most recent threads involving the subject
   - Look for asks, commitments, open loops

## Output structure

Markdown, max 400 words:

  # Brief — <argument>

  ## TL;DR
  One paragraph. What the user needs to know right now.

  ## Where we stand
  Current state. Last meaningful interaction. Outstanding commitments.

  ## Open questions
  What's undecided. What's waiting on whom.

  ## Signal worth remembering
  2-3 bullets of non-obvious, load-bearing context.

  ## Next move
  One recommended action. A pick, not a menu.

## Tone

Direct. No corporate filler.

## Guardrails

- If the subject isn't in the context layer, STOP. Offer to create a
  stub note. Don't invent the briefing.
- If multiple entities could match, list and ask.
- Cite which notes and meetings you used.

## Trigger examples

- "brief me on Acme Corp"
- "write a brief on the MGA project"
- "summarise what we know about Harvard Innovation Labs"
- "/brief Sarah Chen"
