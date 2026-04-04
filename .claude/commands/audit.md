# /audit — Structured Task Audit

You are helping a founder do a systematic inventory of everything they do in their business, then identify what to automate or augment first.

---

## Before You Start

Read the relevant context files:
- `context/workspace.md`
- `context/overview.md`
- `context/business.md`
- `context/founder.md`
- `context/stack.md`
- `context/priorities.md`

If any are empty or contain only placeholders, stop and tell the founder to run `/setup` first.

Then check for supporting artifacts:
- relevant files in `explorations/`
- recent or relevant files in `imports/`

Use them to understand what work may already be structured, documented, or partially solved.

---

## Phase 1 — Task Inventory

Walk through each area of the business systematically. For each area, ask the founder to list the tasks they (or their team) do regularly.

### Areas to cover

Guide the conversation through these areas, but adapt based on the business model from context:

1. **Operations / delivery** — What does fulfilling your product or service actually involve?
2. **Sales / acquisition** — How do you find and close customers?
3. **Marketing / content** — How do you generate awareness and leads?
4. **Finance / admin** — Invoicing, reporting, bookkeeping, compliance
5. **Communication** — Internal (team), external (clients, partners)
6. **Strategy / planning** — How do you decide what to work on?
7. **Hiring / team** — Recruiting, onboarding, management (if applicable)

For each task they mention, capture:
- **Task name** — what is it
- **Frequency** — daily, weekly, monthly, ad hoc
- **Time cost** — how long does it take each time
- **Who does it** — founder, team member, outsourced
- **Current tools** — what tools are used

Don't make this feel like a form. Have a conversation. Ask follow-up questions. If they say "I do a lot of admin" — dig into what that actually means.

**Save progress as you go.** After completing each business area, append the tasks to `audit-results.md` immediately. Don't wait until the end — long conversations degrade quality and progress could be lost. If the conversation is getting very long, suggest continuing in a new session: "We've covered 4 areas. Want to save progress and pick up the rest in a fresh conversation?"

---

## Phase 2 — Score and Prioritize

Once you have a comprehensive task list, score each task on automation potential:

### Scoring criteria

- **Repeatability** (1-5): How consistent is the process? Does it follow the same steps each time?
- **Data availability** (1-5): Is the input data digital and accessible? Or is it locked in someone's head?
- **Risk tolerance** (1-5): How bad is it if the AI gets it 80% right? (5 = totally fine, 1 = catastrophic)
- **Time impact** (1-5): How much time would be freed up?

**Automation score** = average of the four scores.

### Classification

For each task, classify it as one of:
- **Automate** — AI can handle this end-to-end with minimal oversight
- **Augment** — AI can do 60-80% of the work; founder reviews or completes
- **Keep manual** — Requires human judgment, relationships, or creativity that AI can't replace
- **Eliminate** — On reflection, this task might not need to be done at all

---

## Phase 3 — Output

Create a clear, structured audit document. Save it as `audit-results.md` in the workspace root.

### Format

```markdown
# Task Audit — [Business Name]

> Completed: [date]
> Total tasks identified: [number]

## Summary

- Tasks to automate: [number]
- Tasks to augment: [number]
- Tasks to keep manual: [number]
- Tasks to eliminate: [number]
- Estimated time recoverable per week: [hours]

## Priority Actions (Top 5)

[The 5 highest-scoring tasks that should be tackled first, with brief notes on approach]

## Full Task Inventory

### [Business Area]

| Task | Frequency | Time | Score | Classification | Notes |
|------|-----------|------|-------|----------------|-------|
| ...  | ...       | ...  | ...   | ...            | ...   |

[Repeat for each business area]
```

---

## After the Audit

Present the summary and priority actions. Then ask:

> "These are your highest-impact automation targets. Want to pick one and run `/explore` to figure out how to build it?"

If they're not sure which to pick, recommend based on: highest score + quickest to implement = best first win.
