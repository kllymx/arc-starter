---
description: Prototype the first interaction for an AI system or internal tool
argument-hint: [slack|teams|imessage|web|dashboard|spec] [optional idea]
---

# /prototype-system

Prototype the front door for a proposed AI system.
Argument: **$ARGUMENTS**

## Purpose

Turn strategy into something the founder can show. This is not the full
system. It is the first believable interaction or internal tool mockup.

Use `reports/ai-leverage-brief.md` if it exists. If the founder names a
different idea, use that.

## Prototype Modes

Infer the best mode from the argument. If unclear, choose the mode that
best fits the recommended path:

- `slack` or `teams`: conversation mockup for a company assistant
- `imessage`: personal/always-available assistant mockup
- `web`: simple local HTML internal app mockup
- `dashboard`: local HTML report/dashboard mockup
- `spec`: one-page product/system spec only

For non-technical founders, default to a conversation mockup. For
technical/internal-tool opportunities, default to HTML.

## Inputs

Read:

1. `reports/ai-leverage-brief.md`
2. `reports/business-snapshot.md` if present
3. relevant `context/` and wiki articles
4. named workflow/routine if the argument includes one

## Output

Create a folder:

`prototypes/[kebab-case-system-name]/`

Inside it, create:

1. `README.md`
2. one prototype artifact:
   - `conversation-mockup.md` for Slack/Teams/iMessage style
   - `index.html` for web/dashboard style
   - `system-spec.md` for spec-only mode

## README Structure

```markdown
# [System Name] Prototype

## Job To Be Done

## Target User

## First Interaction

## Context Used

## Agent Permissions

## Human Approval Points

## Build Next
1. ...
2. ...
3. ...
```

## Conversation Mockup Requirements

Show:

- First message a teammate/founder would send
- Assistant response
- Follow-up actions/buttons as plain markdown bullets
- What context the assistant used
- What it would draft/update
- What it would ask a human to approve

## HTML Prototype Requirements

Create a single self-contained `index.html` with embedded CSS.

Visual style:

- Clean internal tool aesthetic
- Dark or neutral theme
- No external network assets
- Stable responsive layout
- Use cards, sidebars, status pills, simple charts, or panels where useful

The prototype should show the first useful screen, not a marketing page.

## Guardrails

- Do not build production auth, databases, or external integrations.
- Do not include sensitive private context in the prototype.
- Make it clear what is mocked vs real.
- Keep scope to one believable demo interaction.
