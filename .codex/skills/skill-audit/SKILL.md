---
name: skill-audit
description: Find repeated ARC workflows that should become reusable commands or skills, and build an approved one. Trigger when the user asks what should become a skill, asks to audit repeated work, asks to create a reusable command/skill from a workflow, or uses /skill-audit.
metadata:
  short-description: Find and build reusable ARC skills
---

# skill-audit

Follow the same workflow as `.claude/commands/skill-audit.md`.

Read that command file first, then execute it.

Default to audit mode:

- create `reports/skill-audit.md`
- create or update `context/skill-backlog.md`
- do not create command/skill files until the founder approves a specific
  candidate

If the founder approves a candidate, build it using the command's Approved
Build Mode:

- Claude command: `.claude/commands/<kebab-name>.md`
- Codex skill: `.codex/skills/<kebab-name>/SKILL.md`

Default to building both harness files unless the founder asks for one
harness only or the workflow clearly belongs to one harness.
