---
description: Find repeated ARC workflows and optionally turn one into a reusable command/skill
argument-hint: [optional: build <candidate-name>|claude-only|codex-only]
---

# /skill-audit

Assess the founder's ARC workspace for repeated work that should become a
reusable command or skill.

Argument: **$ARGUMENTS**

## Purpose

Session 2 introduced the progression from prompts to commands to skills.
This command turns that idea into a practical review:

1. Find repeated questions, outputs, routines, decisions, and workflows.
2. Propose the best candidates for reusable skills.
3. If the founder approves one, build it in the right place for Claude
   and/or Codex to use.

Default mode is **audit only**. Do not create command or skill files unless
the founder explicitly asks to build a specific candidate.

## Modes

### Audit Mode

Use when:

- no argument is provided
- the argument asks what should become a skill
- the founder asks for suggestions, opportunities, repeated work, or a
  skill backlog

### Approved Build Mode

Use when the founder says something like:

- "build candidate 1"
- "turn the follow-up workflow into a skill"
- "yes, build this"
- `/skill-audit build investor-update`

Only build a specific candidate. If the target is ambiguous, ask one
clarifying question before writing files.

## Inputs

Read:

1. `context/`
2. `wiki/index.md` and relevant wiki articles
3. recent `daily/` logs
4. existing commands in `.claude/commands/`
5. existing Codex skills in `.codex/skills/`
6. `reports/skill-audit.md` if it exists
7. any workflow/routine named in the argument

## Audit Signals

Look for work that has:

- repeated inputs
- repeated output shape
- recurring stakeholders or entities
- repeated decision criteria
- repeated tool usage
- repeated "can you draft / summarize / compare / prepare / follow up"
  style requests
- enough context in ARC to make the workflow grounded
- clear safety boundaries

Do **not** recommend a skill just because something sounds useful once.
The strongest candidates are repeated, structured, and easy to describe.

## Candidate Scoring

Score each candidate from 1-5:

- **Repeatability** — how often this likely happens
- **Leverage** — time saved or decision quality improved
- **Clarity** — whether inputs and outputs are well-defined
- **Context readiness** — whether ARC already contains enough grounding
- **Safety** — whether it can run without risky external side effects

## Audit Output

Save to:

`reports/skill-audit.md`

Use this structure:

```markdown
# Skill Audit

## Recommendation
Short summary of what should become reusable next.

## Top Candidates

### 1. [Candidate Name]
- Type: Claude command, Codex skill, or both
- Trigger phrases:
- What it does:
- Why it repeats:
- Inputs:
- Output:
- Tools needed:
- Safety boundary:
- Scores:
  - Repeatability:
  - Leverage:
  - Clarity:
  - Context readiness:
  - Safety:
- Suggested file names:
  - Claude: `.claude/commands/[kebab-name].md`
  - Codex: `.codex/skills/[kebab-name]/SKILL.md`

## Build Recommendation
If you want to build one now, say: "build candidate [number]".

## Sources Used
- ...
```

Also create or update:

`context/skill-backlog.md`

Keep it short and scannable. Use this structure:

```markdown
# Skill Backlog

## Ready To Build
- [Candidate] — one-line reason

## Watch List
- [Candidate] — needs more examples/context first

## Built
- [Skill] — path(s), date, source candidate
```

## Approved Build Output

When the founder approves a candidate, create the appropriate files:

1. Claude command:

   `.claude/commands/[kebab-name].md`

2. Codex skill:

   `.codex/skills/[kebab-name]/SKILL.md`

Default to **both** unless:

- the candidate is only useful in one harness
- `context/workspace.md` clearly says the founder only uses one harness
- the founder asks for `claude-only` or `codex-only`

If either target path already exists, do not overwrite it silently. Read the
existing file and either update it carefully or ask before replacing it.

## Claude Command Template

Use this structure:

````markdown
---
description: [one-line description]
argument-hint: [expected argument]
---

# /[kebab-name]

[One-sentence purpose.]

Argument: **$ARGUMENTS**

## Purpose

## Inputs

Read:
1. ...

## Workflow

1. ...
2. ...
3. ...

## Output

Save to:

`[path]`

Use this structure:

```markdown
# [Output Title]

## ...
```

## Guardrails

- ...
````

## Codex Skill Template

Use this structure:

```markdown
---
name: [kebab-name]
description: [Trigger description for Codex. Include natural-language triggers and /[kebab-name].]
metadata:
  short-description: [short description]
---

# [kebab-name]

Follow the same workflow as `.claude/commands/[kebab-name].md`.

Read that command file first, then execute it.

[Any Codex-specific notes, if needed.]
```

## Build Quality Rules

- Use the founder's actual repeated workflow as the source, not a generic
  automation idea.
- Make the command concrete enough that a future agent can run it.
- Include trigger phrases so natural language can invoke it.
- Include exact input files/directories to read.
- Include exact output path and format.
- Include guardrails for sensitive data, external actions, and approvals.
- Prefer draft/review outputs over automatic external actions.
- Add the new command to the command table in `README.md`, `AGENTS.md`, and
  `CLAUDE.md` only if the founder wants it to become part of the durable
  workspace.

## After Building

Update `context/skill-backlog.md`:

- Move the candidate into `## Built`
- Record created file paths
- Record the date
- Record any open follow-ups

Briefly tell the founder:

- what was created
- how to invoke it naturally
- where the files live
