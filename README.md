# ARC

**By Arcane Intelligence — Built by Max Kelly**

A starter kit that gives founders an AI-powered operating partner for their business. Clone it, run the setup, and get a workspace that knows your business deeply enough to help you move faster on everything from daily tasks to strategic decisions.

---

## What This Is

ARC is a structured workspace that turns an AI agent into a persistent operating partner for your business. Instead of re-explaining your business every time you open a chat, ARC stores your business context in structured files that the agent reads automatically.

After setup, your agent knows:
- what your business does and how it makes money
- who you are, what you're good at, and where you need help
- what tools and platforms you use
- what your current priorities and pain points are

It can then help you brainstorm what to automate, audit your tasks, explore new ideas, and execute faster than working alone.

---

## Getting Started

### Step 1 — Clone or download this repo

### Step 2 — Open it in your environment

**VS Code + Claude Code extension** (recommended):
1. Open the `arc-starter` folder in VS Code
2. Open the Claude Code panel
3. Start a conversation — the agent will read CLAUDE.md automatically

**Cursor + Claude Code extension**:
1. Open the `arc-starter` folder in Cursor
2. Open the Claude Code panel
3. Same as above — CLAUDE.md is read automatically

**Codex (VS Code extension)**:
1. Open the `arc-starter` folder in VS Code
2. Codex reads AGENTS.md for context (included alongside CLAUDE.md with identical content)
3. Start a conversation

**Claude Desktop**:
1. Create a new Project
2. Drag the files from `context/` and `CLAUDE.md` into the Project Knowledge
3. Start a conversation

**Terminal (Claude Code CLI)**:
1. `cd` into the `arc-starter` folder
2. Run `claude` to start a session
3. Claude Code reads CLAUDE.md automatically

### Step 3 — Run /setup

Type `/setup` in your first conversation. The agent will interview you about your business and populate the context files. There are two modes:

- **Quick setup** (~15 minutes) — captures the essentials, enough to be useful immediately
- **Deep setup** (~30 minutes) — comprehensive interview that fills in all the details

You can do the quick setup now and run the deep setup later when you have more time.

**Have existing documents?** Drop pitch decks, one-pagers, business plans, or any relevant docs into the `imports/` folder before running /setup. The agent will analyze them first and only ask about what's missing.

### Step 4 — Start using it

Once context is loaded, you can:

- Ask questions about your business and get answers grounded in your actual context
- Run `/brainstorm` to get suggestions for what to automate or improve
- Run `/audit` to do a structured inventory of tasks across your business
- Run `/explore` to take a specific idea and research/spec it out
- Just talk to it — ask for help with emails, reports, analysis, strategy, whatever you need

---

## Commands

You can trigger these by typing the `/command` name, or just say it naturally — the agent understands both.

| Command | Or just say... | What it does |
|---------|---------------|--------------|
| `/setup` | "let's set up" | Interviews you and populates your business context files |
| `/brainstorm` | "what should I automate?" | Suggests automation and augmentation opportunities based on your context |
| `/audit` | "audit my tasks" | Structured task audit — inventory what you do and identify what to automate first |
| `/explore` | "explore this idea" | Takes an idea and researches the best way to build it |

---

## Workspace Structure

```
arc-starter/
├── CLAUDE.md              # Agent instructions (Claude Code / Cursor)
├── AGENTS.md              # Same content (Codex / Hermes / other agents)
├── README.md              # You are here
├── context/               # Your business context (populated by /setup)
│   ├── business.md        # Business model, market, customers, strategy
│   ├── founder.md         # Your background, role, preferences
│   ├── stack.md           # Tools, platforms, integrations
│   ├── priorities.md      # Current priorities and pain points
│   ├── memory.md          # Lightweight preferences learned over time
│   └── agent-learnings.md # Corrections — so mistakes aren't repeated
├── .claude/commands/      # Slash commands
│   ├── setup.md
│   ├── brainstorm.md
│   ├── audit.md
│   └── explore.md
├── imports/               # Drop documents here before running /setup
├── explorations/          # Output from /explore — plans accumulate here
└── guides/                # Reference material
    ├── what-is-this.md    # Plain-English explanation of the workspace
    ├── skills-explained.md # What skills are and how to create them
    ├── mcps-explained.md  # What MCPs are and when to add them
    └── next-steps.md      # Where to go after the basics
```

---

## Guides

New to this? Start with the guides in the `guides/` folder:

- **what-is-this.md** — Plain-English explanation of how this workspace works
- **skills-explained.md** — What skills are, how they work, and how to create your own
- **mcps-explained.md** — What MCP integrations are and when to add them
- **next-steps.md** — Where to go after you've got the basics set up

---

## The ARC Progression

ARC is designed to grow with you in layers:

**Layer 1 — Context** (start here)
Set up your workspace and load your business context. This alone makes every AI conversation dramatically better.

**Layer 2 — Workflows**
Build specific workflows that automate or augment tasks in your business. Add tool integrations. Create custom commands for your recurring work.

**Layer 3 — Systems**
Scale from personal use to team infrastructure. Add guardrails, permissions, scheduling, and orchestration for more complex workflows.

Each layer builds on the previous one. You don't need to jump to Layer 3 on day one — start with context and let it grow.

---

*ARC by Arcane Intelligence. Proprietary — provided to workshop participants only.*
