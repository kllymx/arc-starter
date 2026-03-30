# /brainstorm — Automation & Augmentation Opportunities

You are helping a founder identify what to automate or augment in their business using AI.

---

## Before You Start

Read the relevant context files:
- `context/workspace.md`
- `context/overview.md`
- `context/business.md`
- `context/founder.md`
- `context/stack.md`
- `context/priorities.md`

If any are empty or contain only placeholders, stop and tell the founder to run `/setup` first. You cannot brainstorm effectively without business context.

---

## How to Brainstorm

Analyze the founder's business context and generate concrete, actionable suggestions for things that could be automated or heavily augmented with AI.

### What to look for

- **Repetitive tasks** the founder mentioned doing regularly
- **Pain points** and bottlenecks from priorities.md
- **Tool integrations** that could be connected (from stack.md)
- **Information flows** that are currently manual (copying data between tools, compiling reports, etc.)
- **Communication tasks** (emails, follow-ups, briefings, updates)
- **Research and analysis** tasks that could be accelerated
- **Reporting and dashboards** that are currently manual
- **Content creation** if relevant to the business

### What NOT to suggest

- Anything that requires replacing the founder's core judgment or domain expertise
- Complex multi-system integrations that would take weeks to set up
- Suggestions that don't connect to their actual tools or workflow
- Generic "use AI for marketing" type suggestions — be specific

---

## Output Format

Present suggestions in two tiers:

### Quick Wins (can be done in a single session)

For each suggestion:
- **What**: One-line description
- **Why**: How it connects to their specific pain points or priorities
- **How**: Brief description of what it would look like in practice
- **Impact**: Time saved or quality improved

Aim for 3-5 quick wins.

### Deeper Builds (require more setup or integration)

For each suggestion:
- **What**: One-line description
- **Why**: How it connects to their business
- **What's needed**: Tools, integrations, or setup required
- **Impact**: What changes when this is working

Aim for 3-5 deeper builds.

---

## After Presenting

Ask the founder:

> "Any of these jump out? If something interests you, I can run `/explore` to research the best way to build it and spec it out."

If they pick one, suggest running `/explore` with that specific idea.

If they seem to want immediate value rather than a bigger build, say:

> "If you want, I can also pick the fastest useful thing to do right now and just do it. Ask me for a quick win."

If nothing resonates, ask:

> "What did I miss? Is there something you do every day or every week that feels like it shouldn't take as long as it does?"

Use their answer to generate more targeted suggestions.
