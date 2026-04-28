---
description: Classify the next AI leverage path and create a founder-ready adoption brief
argument-hint: [optional workflow, routine, or business area]
---

# /ai-leverage-brief

Create an AI Leverage Pathway Brief from the founder's ARC context.
Argument: **$ARGUMENTS**

## Purpose

Session 3 is not about forcing personal ARC into the company. This command
decides what should happen next:

1. keep compounding personal leverage
2. package something for one collaborator
3. build a shared knowledge layer
4. prototype an internal tool
5. defer until more context exists

The founder should leave with language they can use internally, grounded
in their own business.

## Inputs

Read:

1. `context/`
2. `wiki/index.md` and relevant wiki articles
3. `audit-results.md` if present
4. recent `explorations/`
5. `reports/business-snapshot.md` if present
6. any routine/workflow named in the argument

If the argument names a specific workflow, assess that workflow first.
Otherwise infer the strongest opportunity from the whole context.

## Classification Model

Assess these signals:

- Is the context mostly founder/operator private context?
- Is there a clear second user or teammate?
- Is the workflow repeated by more than one person?
- Is company knowledge scattered or stale?
- Would a shared knowledge base reduce repeated questions or onboarding
  load?
- Does the opportunity need structured records, state, permissions,
  dashboards, or approvals?
- Is the data sensitive, regulated, customer-specific, HR/finance, or IP-heavy?
- Is there enough evidence to recommend a company-facing wedge?

Choose exactly one primary path:

### Personal Leverage Path

Use when the best next move is another private workflow, routine, memory
improvement, or founder/operator system.

### One-Collaborator Path

Use when one teammate, cofounder, contractor, EA, or operator could reuse
a narrow workflow safely.

### Shared Knowledge Path

Use when the best first company wedge is an AI-readable knowledge layer:
wiki, decision log, SOPs, onboarding, meeting decisions, customer learnings,
technical/project context.

### Internal Tool Path

Use when the opportunity needs a focused custom internal app or agentic
workflow around structured data, state, permissions, dashboards, approvals,
or routing.

### Defer

Use when context is too thin, the opportunity is too sensitive, or the
business needs more personal experimentation first.

## Output

Save to:

`reports/ai-leverage-brief.md`

Use this structure:

```markdown
# AI Leverage Pathway Brief

## Recommendation
Primary path: [Personal / One-Collaborator / Shared Knowledge / Internal Tool / Defer]

One-paragraph rationale.

## Why This Path
- Evidence from ARC context
- What makes this higher-leverage than alternatives
- What should not be shared or scaled yet

## The Wedge
- Business bottleneck
- Who benefits
- What changes if it works

## Knowledge And Data
- What context it needs
- Where that context lives today
- Recommended substrate: docs/wiki, markdown/GitHub, database/custom app, or hybrid

## System Shape
- Interface: chat, Slack/Teams, iMessage, web app, dashboard, existing tool
- Agent permissions: read, draft, update, send/trigger
- Human approval points
- Owner / steward
- Failure mode and fallback

## One-Week Build Plan
1. ...
2. ...
3. ...

## 60-Second Internal Pitch
Plain-English pitch the founder can use with a teammate, executive, or
advisor. Outcome-first, not tool-first.

## What To Avoid
Specific risks, overreach, or premature company rollout traps.

## Sources Used
List files/articles read.
```

## Tone

Strategic but practical. Founder/operator language. Do not sound like an
enterprise AI consulting deck.

## Guardrails

- Do not recommend company rollout just because a workflow is useful.
- Do not suggest sharing the founder's whole personal ARC.
- Treat ARC as a reference architecture: context, memory, workflows,
  skills, tools, integrations, review, routines.
- Be explicit that markdown is one implementation, not the required
  company storage format.
