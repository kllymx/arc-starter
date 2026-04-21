---
name: triage
description: Triage the user's inbox into reply-now, later, and archive buckets, grounded in their arc-starter context layer so priority reflects who actually matters to them. Trigger when the user asks to "triage my inbox", "sort my emails", "what should I reply to first", or uses "/triage".
metadata:
  short-description: Inbox triage into reply-now / later / archive, context-aware
---

# triage

Triage the user's inbox into three buckets: reply now, later, archive.

Default window is the last 24 hours. If the user provides a different
window as an argument (e.g. "last 3 days"), use that.

## Inputs

1. **Gmail MCP** — unread threads in the window, plus starred unread
   older threads. Skip newsletters, receipts, marketing, automated
   notifications.

2. **The user's context layer** (this arc-starter folder)
   - `context/` — client and project notes, so priority is grounded in
     who actually matters to them right now
   - `Memory/workspace.md` if present — stated focus for this week

3. **Recent meetings** (Granola MCP, if connected) — last 7 days, to
   spot follow-ups they owe people from this week's conversations

## Bucketing logic

**Reply now**: someone's explicitly blocked on them, time-sensitive
deadline, a client in their active context, or a follow-up promised
in a recent meeting.

**Later today / this week**: meaningful but not blocking.

**Archive / ignore**: not worth reading in full. Explain why briefly.

## Output

Markdown, compact. One line per thread.

  # Inbox triage — <window>

  ## Reply now (<count>)
  - <sender> · <one-line ask> · <why>

  ## Later (<count>)
  - <sender> · <one-line ask>

  ## Archive (<count>)
  - <sender> · <reason in 4 words>

  ## Anything I'd miss?
  One line. Low-priority thread the context layer says matters.
  Or "nothing flagged."

## Guardrails

- Read-only. Do not reply, archive, or delete.
- If unsure about a bucket, put in "Later" and flag.
- If the inbox is empty or sparse, say so and stop. Don't pad.

## Trigger examples

- "triage my inbox"
- "sort my emails from today"
- "what should I reply to first"
- "/triage"
- "/triage last 3 days"
