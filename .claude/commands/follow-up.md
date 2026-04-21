---
description: Draft a meeting follow-up email grounded in your meeting notes + your context layer
argument-hint: <person or company name>
---

# /follow-up

Draft a meeting follow-up email for the person or company in the argument.
Argument: **$ARGUMENTS**

## Inputs, pull in this order

1. **Meeting notes (Granola MCP, or whatever meeting tool you use)**
   - Find the most recent meeting where "$ARGUMENTS" is in the title,
     attendee list, or transcript. If multiple match in the last 14 days,
     pick the most recent and tell me which one you picked.
   - Pull: title, date, attendees, full summary, transcript, action items.
   - If nothing matches in the last 14 days, STOP and tell me. Do not
     invent a meeting.

2. **Your context layer (this arc-starter folder)**
   - Look in `context/` for any note about the person, company, or project
     named in $ARGUMENTS. Read the whole note, not just the first paragraph.
   - Look in `wiki/` for any recent captures relating to this entity.
   - Read any linked project notes. Prior context matters.
   - Read-only. Do not create or modify notes.

3. **Recent email history (Gmail MCP)**
   - Search last 90 days for threads involving this person or company.
   - Skim the last 2 to 3 threads. Match my tone. Note any open asks I
     owe them or they owe me.

## Synthesize, decide, don't dump

Before drafting, internally answer:
- What is the ONE outcome this email needs to drive? Reply, decision,
  intro, scheduling, or nothing-just-warmth.
- What did we agree to in the meeting? Restate crisply.
- What am I owed vs what do I owe? Separate the two.
- What does my context layer tell me matters to this person that wasn't
  said in the meeting? Use sparingly. Signal, not trivia.

## Output, Gmail draft

Create a Gmail draft. Do not send. Structure:

- **To:** the right person, resolved from meeting attendees + context note
- **Subject:** short, specific, no "quick follow-up" filler. Reference the
  actual thing we discussed.
- **Body:**
  - Opening: 1 line, human, not corporate. No "I hope this finds you well."
  - Middle: what we agreed + what happens next. Bullets if 3 or more items,
    otherwise prose.
  - Close: the single clear ask. One thing.
  - Signature: your standard sign-off.

Length: under 150 words unless the meeting genuinely needs more.

## Tone

Your voice, read from your arc-starter context and recent email history.
Direct. Warm without being gushy. Peer, not client.

## Before you finish

Show me the draft in chat AND save it as a Gmail draft. Then list:
- Which meeting you used (title + date)
- Which context notes you referenced
- One thing you chose NOT to include and why

## Guardrails

- Do not send. Draft only.
- If any input source is missing or ambiguous, stop and ask. Do not invent
  attendees, action items, or context.
- If the most recent meeting is older than 7 days, flag it. Stale
  follow-ups need a different opening.
