# /audit — Structured Task Audit

You are helping a founder do a systematic inventory of everything they do in their business, then identify what to automate or augment first.

---

## Before You Start

Read context files:
- `context/workspace.md`
- `context/overview.md`

Read the wiki:
- `wiki/index.md`
- Drill into relevant articles: business model, founder profile, tech stack, priorities

If the wiki has no articles, stop and tell the founder to set up ARC first.

Check for prior work:
- wiki articles with `type: exploration` for prior research
- recent files in `imports/`

---

## Phase 1 — Task Inventory

Walk through each area of the business systematically. For each area, ask the founder to list the tasks they (or their team) do regularly.

### Areas to cover

Adapt based on the business model from the wiki:

1. **Operations / delivery** — What does fulfilling your product or service actually involve?
2. **Sales / acquisition** — How do you find and close customers?
3. **Marketing / content** — How do you generate awareness and leads?
4. **Finance / admin** — Invoicing, reporting, bookkeeping, compliance
5. **Communication** — Internal (team), external (clients, partners)
6. **Strategy / planning** — How do you decide what to work on?
7. **Hiring / team** — Recruiting, onboarding, management (if applicable)

For each task, capture:
- **Task name**
- **Frequency** — daily, weekly, monthly, ad hoc
- **Time cost** — how long each time
- **Who does it** — founder, team member, outsourced
- **Current tools** — what tools are used

Don't make this feel like a form. Have a conversation. Dig into vague answers.

**Save progress as you go.** After completing each business area, append to `audit-results.md`. Don't wait until the end. Suggest continuing in a new session if the conversation gets long.

---

## Phase 2 — Score and Prioritize

### Scoring criteria

- **Repeatability** (1-5): How consistent is the process?
- **Data availability** (1-5): Is the input data digital and accessible?
- **Risk tolerance** (1-5): How bad is 80% accuracy? (5 = fine, 1 = catastrophic)
- **Time impact** (1-5): How much time freed up?

**Automation score** = average of the four scores.

### Classification

- **Automate** — AI handles end-to-end with minimal oversight
- **Augment** — AI does 60-80%; founder reviews
- **Keep manual** — Requires human judgment
- **Eliminate** — Might not need to be done at all

---

## Phase 3 — Output

Save as `audit-results.md`:

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

[The 5 highest-scoring tasks with brief notes on approach]

## Full Task Inventory

### [Business Area]

| Task | Frequency | Time | Score | Classification | Notes |
|------|-----------|------|-------|----------------|-------|
| ...  | ...       | ...  | ...   | ...            | ...   |
```

---

## After the Audit

> "These are your highest-impact automation targets. Want to pick one and explore how to build it?"

### Update the wiki

The audit produces valuable business knowledge. After completing it:
- Update `wiki/concepts/priorities.md` with the top automation targets
- Create articles for any new processes or workflows discovered (e.g., `wiki/concepts/sales-process.md`)
- Create a `wiki/connections/automation-opportunities.md` summarizing the highest-impact findings
- Update `wiki/index.md` and `wiki/log.md`
