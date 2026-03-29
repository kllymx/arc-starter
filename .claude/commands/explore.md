# /explore — Research and Spec an Idea

You are helping a founder take a specific idea — whether it's an automation, a workflow, a tool integration, or a process improvement — and turn it into a clear, buildable plan.

---

## Before You Start

Read all four context files:
- `context/business.md`
- `context/founder.md`
- `context/stack.md`
- `context/priorities.md`

If any are empty or contain only placeholders, stop and tell the founder to run `/setup` first.

---

## Phase 1 — Define

If the founder hasn't clearly stated what they want to explore, ask:

> "What's the idea? It can be rough — even just 'I wish I could...' or 'It would be cool if...' is enough to start."

Then clarify until you have:

1. **What** they want to achieve (the outcome, not the implementation)
2. **Why** it matters (connect to their priorities or pain points)
3. **What triggers it** (when does this need to happen?)
4. **What inputs it needs** (where does the information come from?)
5. **What output it should produce** (what does "done" look like?)
6. **Who benefits** (founder, team, customer?)

Don't ask all six as a list. Have a conversation and naturally cover these.

---

## Phase 2 — Analyze

Look at:

1. **Current workspace** — What's already set up that could support this? Any existing context, tools, or workflows that are relevant?
2. **Tech stack** — From stack.md, what tools are involved? Are there APIs available? Are there existing integrations?
3. **Feasibility** — Is this something that can be done with the current setup, or does it need new tools/integrations?

Search the web if needed to:
- Check if APIs exist for the tools involved
- Find best practices for this type of automation
- Identify existing solutions or approaches
- Understand technical constraints

---

## Phase 3 — Spec

Produce a clear exploration document. This is not code — it's a plan that anyone could follow to build the thing.

### Format

```markdown
# Exploration: [Name of the idea]

> Explored: [date]
> Status: Ready to build / Needs more research / Blocked by [X]

## What

[One paragraph: what this does and why it matters]

## How It Works

[Step-by-step description of the workflow, in plain language]

1. [Trigger] — what kicks it off
2. [Input] — where data comes from
3. [Process] — what happens in the middle
4. [Output] — what gets produced
5. [Delivery] — where the result goes

## What's Needed

- **Tools/integrations**: [list any APIs, MCPs, or connections needed]
- **Data sources**: [where information comes from]
- **New files/commands**: [any new workspace additions needed]

## Complexity

- **Effort**: [Quick win / Half-day build / Multi-session project]
- **Risk**: [What could go wrong? What needs human oversight?]
- **Dependencies**: [What needs to be set up first?]

## Recommended Approach

[Your specific recommendation for how to build this, given the founder's context and tech stack. Be concrete — don't just say "use an API," say which API and roughly how.]

## Next Steps

[Exactly what the founder should do next to start building this]
```

Save this document as `explorations/[short-name].md`.

**Save progress incrementally.** If the research or analysis is extensive, write findings to the exploration file as you go rather than building everything in the conversation. Long conversations degrade quality. Use this structure for in-progress saves:

```
## Progress
- **Goal**: [what we're trying to achieve]
- **Done**: [completed steps]
- **In Progress**: [current step]
- **Blocked**: [anything waiting on the founder]
- **Next Steps**: [what comes after]
```

---

## After the Exploration

Present the spec to the founder. Then:

> "This is the plan. Want to start building it now, or save it for later?
>
> If you want to build it now, I can walk you through it step by step."

If they want to build:
- Walk them through each step
- Write any code, commands, or configurations needed
- Test as you go
- Confirm before taking any actions that affect external systems

If they want to save it for later:
- The exploration document is saved — they can come back to it anytime
- Suggest they review it before the next session
