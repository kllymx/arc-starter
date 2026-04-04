# /reflect — Review and Promote Learnings

You are helping a founder make ARC more useful over time by reviewing what has happened recently and promoting the durable parts into the workspace.

The goal is not to rewrite everything. The goal is to keep the compiled context clean, current, and genuinely more helpful.

---

## Before You Start

Read the relevant context files:
- `context/workspace.md`
- `context/overview.md`
- `context/business.md`
- `context/founder.md`
- `context/stack.md`
- `context/priorities.md`
- `context/memory.md`
- `context/agent-learnings.md`

Then check for recent workspace artifacts that should influence your review:
- `audit-results.md` if it exists
- relevant files in `explorations/`
- relevant files in `imports/` that were added recently

If there is no meaningful context loaded yet, stop and suggest running setup first.

Use `context/workspace.md` to match the founder's environment and technical comfort.

---

## What Reflect Should Do

Look for:
- priorities that have changed
- facts that should be remembered later
- corrections the founder has made
- useful patterns that may deserve a future workflow
- exploration outputs that should update the current picture of the business
- stale context that should be revised or removed

Keep a strong distinction between:
- **core context** — durable business facts
- **memory** — lightweight preferences and facts
- **agent learnings** — mistakes and corrections
- **artifacts** — audits, explorations, imported docs, and other outputs

Do not dump artifact content into the context files. Promote only the durable signal.

---

## Output Format

Present a short review in three sections:

### What Changed
- [important change or clarification]

### What ARC Should Remember
- [small durable fact or preference]

### What May Be Worth Turning Into A Workflow Later
- [workflow candidate]

Then ask:

> "Want me to update the relevant context files with these changes?"

If they say yes, update only the files that need it:
- `context/overview.md`
- `context/priorities.md`
- `context/memory.md`
- `context/agent-learnings.md`

If there is no durable learning, say so plainly. Do not force an update just because the command was run.

---

## Good Judgment

- Prefer fewer, higher-signal updates.
- Keep memory concise.
- Keep corrections concrete.
- If a pattern looks workflow-worthy, mention it, but do not auto-create a command unless the founder asks.
- If a prior exploration is now obsolete, mention that it should be revised or replaced.
