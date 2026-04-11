# /explore — Research and Spec an Idea

You are helping a founder take a specific idea — whether it's an automation, a workflow, a tool integration, or a process improvement — and turn it into a clear, buildable plan.

---

## Before You Start

Read context files:
- `context/workspace.md`
- `context/overview.md`

Read the wiki:
- `wiki/index.md`
- Drill into relevant articles based on the idea being explored

If the wiki has no articles, stop and tell the founder to run setup first.

Check for prior work:
- relevant prior files in `explorations/`
- recent files in `imports/`

If a similar idea has already been explored, build from that work unless the founder wants a fresh take.

---

## Phase 1 — Define

If the founder hasn't clearly stated what they want to explore, ask:

> "What's the idea? It can be rough — even just 'I wish I could...' or 'It would be cool if...' is enough to start."

Clarify until you have:
1. **What** they want to achieve
2. **Why** it matters (connect to wiki articles — priorities, bottlenecks)
3. **What triggers it**
4. **What inputs it needs**
5. **What output it should produce**
6. **Who benefits**

Don't ask all six as a list. Have a conversation.

---

## Phase 2 — Analyze

Look at:
1. **Wiki knowledge** — What do you already know from the wiki that's relevant?
2. **Tech stack** — What tools are involved? APIs available?
3. **Feasibility** — Can this be done with the current setup?

Search the web if needed for APIs, best practices, existing solutions.

---

## Phase 3 — Spec

Save as `explorations/[short-name].md`:

```markdown
# Exploration: [Name of the idea]

> Explored: [date]
> Status: Ready to build / Needs more research / Blocked by [X]

## What

[One paragraph: what this does and why it matters]

## How It Works

1. [Trigger] — what kicks it off
2. [Input] — where data comes from
3. [Process] — what happens
4. [Output] — what gets produced
5. [Delivery] — where the result goes

## What's Needed

- **Tools/integrations**: [list any APIs, MCPs, or connections]
- **Data sources**: [where information comes from]
- **New files/commands**: [any workspace additions]

## Complexity

- **Effort**: [Quick win / Half-day build / Multi-session project]
- **Risk**: [What could go wrong?]
- **Dependencies**: [What needs to be set up first?]

## Recommended Approach

[Concrete recommendation given the founder's context and stack]

## Next Steps

[Exactly what to do next]
```

**Save progress incrementally** if the research is extensive.

---

## After the Exploration

> "This is the plan. Want to start building it now, or save it for later?"

If they want to build, walk them through step by step.

### Update the wiki

Every exploration produces knowledge worth keeping:
- **New concepts** discovered during research → create `wiki/concepts/` articles
- **New tools or APIs** identified → create entity articles
- **Connections** between the exploration and existing wiki content → create `wiki/connections/` articles
- **Update `wiki/index.md`** with new articles
- **Append to `wiki/log.md`** with what was explored and what was learned

The exploration file stays in `explorations/` as the spec. The knowledge it produced enters the wiki for future use.
