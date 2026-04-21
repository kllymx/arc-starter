---
name: follow-up
description: Draft a meeting follow-up email for a named person or company, grounded in meeting notes, the arc-starter context layer, and recent email history. Trigger when the user asks to follow up on a meeting, draft a follow-up email, write a recap email, or uses phrases like "follow up with <name>", "draft a follow-up", or "/follow-up <name>".
metadata:
  short-description: Meeting follow-up email grounded in meeting notes + context layer + email history
---

# follow-up

Draft a meeting follow-up email for the person or company the user names.
The name appears as the argument after the trigger (e.g. "follow up with
Acme" → argument = "Acme").

## Inputs, pull in this order

1. **Meeting notes (Granola MCP, or whichever meeting tool is connected)**
   - Find the most recent meeting where the argument is in the title,
     attendee list, or transcript. If multiple match in the last 14 days,
     pick the most recent and tell me which one you picked.
   - Pull: title, date, attendees, full summary, transcript, action items.
   - If nothing matches in the last 14 days, STOP and tell me. Do not
     invent a meeting.

2. **The user's context layer (this arc-starter folder)**
   - Look in `context/` for any note about the person, company, or project
     named in the argument. Read the whole note.
   - Look in `wiki/` for recent captures relating to this entity.
   - Read linked project notes if the meeting touched an active project.
   - Read-only. Do not create or modify notes.

3. **Recent email history (Gmail MCP)**
   - Search last 90 days for threads involving this person or company.
   - Skim the last 2-3 threads. Match their tone. Note any open asks.

## Synthesize, decide, don't dump

Before drafting, internally answer:
- What is the ONE outcome this email needs to drive?
- What did we agree to in the meeting? Restate crisply.
- What am I owed vs what do I owe?
- What does the context layer say matters that wasn't said in the meeting?
  Signal, not trivia.

## Output, Gmail draft

Create a Gmail draft. Do not send. Structure:

- **To:** the right person, resolved from attendees + context note
- **Subject:** short, specific, no filler. Reference the actual thing.
- **Body:**
  - Opening: 1 line, human, not corporate.
  - Middle: what we agreed + what happens next.
  - Close: one clear ask.
  - Signature: standard sign-off.

Length: under 150 words unless the meeting needs more.

## Tone

Match the user's voice, as read from their context layer and recent email
history. Direct. Warm without being gushy. Peer, not client.

## Before you finish

Show the draft in chat AND save it as a Gmail draft. Then list:
- Which meeting you used (title + date)
- Which context notes you referenced
- One thing you chose NOT to include and why

## Guardrails

- Do not send. Draft only.
- If any input source is missing or ambiguous, stop and ask.
- If the most recent meeting is older than 7 days, flag it.

## Trigger examples

- "follow up with Acme"
- "draft a follow-up email for my meeting with Jake"
- "write a follow-up to Sarah Chen"
- "/follow-up Harvard Innovation Labs"
