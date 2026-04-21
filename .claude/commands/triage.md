---
description: Triage your inbox into reply-now / later / archive, grounded in your context layer
argument-hint: (optional) <time-window, e.g. "last 24h", default: last 24h>
---

# /triage

Triage my inbox into three buckets: **reply now**, **later**, **archive**.
Argument (optional, defaults to last 24h): **$ARGUMENTS**

## Inputs

1. **Gmail MCP** — unread threads in the window, plus starred unread older.
   Skip newsletters, receipts, marketing, automated notifications.

2. **Your context layer** (this arc-starter folder)
   - `context/` — client and project notes so priority is grounded in
     who actually matters to me right now, not generic importance
   - `Memory/workspace.md` if present — what I said I was focused on

3. **Recent meetings** (Granola MCP, if connected) — last 7 days, to
   spot follow-ups I owe people from conversations this week

## Bucketing logic

**Reply now**: someone's explicitly blocked on me, a time-sensitive
deadline, a client from my active context, or a follow-up I promised
in a recent meeting.

**Later today / this week**: meaningful but not blocking. Draft
mentally, batch later.

**Archive / ignore**: not worth reading in full. Don't delete, just
skip. Explain why briefly so I can correct the heuristic.

## Output

Markdown. Compact. One line per thread.

  # Inbox triage — <window>

  ## Reply now (<count>)
  - <sender> · <one-line ask> · <why it's in this bucket>

  ## Later (<count>)
  - <sender> · <one-line ask>

  ## Archive (<count>)
  - <sender> · <reason in 4 words>

  ## Anything I'd miss?
  One line. A thread that looks low-priority but the context layer
  says I should care about. Or "nothing flagged."

## Guardrails

- Read-only. Do not reply, do not archive, do not delete.
- If you're unsure which bucket, put it in "Later" and flag it for me.
- If the inbox is empty or sparse, say so and stop. Don't pad.
