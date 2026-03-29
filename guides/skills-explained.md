# Skills — What They Are and How to Create Them

## What Is a Skill?

A skill is a reusable, agent-invoked solution to a recurring problem. Think of it like an SOP (Standard Operating Procedure) that the AI knows how to follow.

Skills are different from slash commands:

| | Slash Command | Skill |
|---|---|---|
| **Triggered by** | You type it manually (e.g., `/brainstorm`) | The agent invokes it automatically when relevant |
| **Scope** | One specific task or workflow | A whole problem domain with multiple operations |
| **Complexity** | Simple — a single prompt | Can include multiple files, sub-commands, and resources |
| **When to create** | You find yourself writing the same prompt repeatedly | You have a recurring multi-step problem that the agent should handle without being asked |

**The rule of thumb**: Start with a slash command. Only upgrade to a skill when you have multiple related operations that form a cohesive domain.

---

## Anatomy of a Skill

A skill lives in the `.claude/skills/` folder and typically has this structure:

```
.claude/skills/
└── my-skill/
    ├── skill.md          # Instructions for the agent
    └── (optional files)  # Templates, examples, reference data
```

### skill.md

This is the core file. It tells the agent:
- What the skill does
- When to use it
- How to execute it
- What inputs it needs
- What output it should produce

### Example: A "weekly report" skill

```markdown
# Weekly Report Skill

Generate a weekly business report based on current data and priorities.

## When to use

When the founder asks for a weekly report, weekly summary, or status update.

## How to execute

1. Read context/priorities.md for current focus areas
2. Review any recent documents or notes created this week
3. Generate a structured report covering:
   - Progress against priorities
   - Key decisions made
   - Blockers or risks
   - Recommended actions for next week
4. Save as reports/weekly-[date].md
```

---

## How to Create a Skill

### Step 1 — Notice a pattern

You've been doing the same kind of task multiple times. Maybe you keep asking the AI to "analyze this competitor" or "draft a client proposal" in a similar way.

### Step 2 — Write it down

Create a folder in `.claude/skills/` and write a `skill.md` that describes:
- What the skill does
- When the agent should use it
- Step-by-step instructions for how to do it
- What the output should look like

### Step 3 — Test it

Ask the agent to do the task. It should automatically find and follow the skill. If it doesn't, refine the "when to use" section.

### Step 4 — Iterate

Skills get better over time. When the output isn't quite right, update the skill.md with more specific instructions or examples.

---

## When NOT to Create a Skill

- If you've only done the task once — it's not a pattern yet
- If a simple slash command works fine — don't over-engineer
- If the task is different every time — skills work best for consistent processes
- If you're in the first few days of using the workspace — learn the basics first

---

## Skills vs Slash Commands vs MCPs

| Tool | Purpose | Example |
|---|---|---|
| **Slash command** | Manual, one-off reusable prompt | `/brainstorm`, `/audit` |
| **Skill** | Automatic, agent-invoked workflow | Weekly report generation |
| **MCP** | External tool integration | Gmail access, calendar sync |

These compose together: a skill might use an MCP to pull data, and a slash command might trigger a skill. Start simple, add complexity only when you need it.
