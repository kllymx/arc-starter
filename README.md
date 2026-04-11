<p align="center">
  <img src="arc-system.png" alt="ARC by Arcane Intelligence" width="700" />
</p>

# ARC

**By Arcane Intelligence — Built by Max Kelly**

A starter kit that gives founders an AI-powered operating partner with a compounding knowledge base.

Clone it, run the setup, and you get a workspace that learns your business deeply — and gets smarter every session.

This is not a generic chatbot prompt. It is a structured workspace with an LLM-maintained wiki that compounds knowledge over time, inspired by [Andrej Karpathy's LLM knowledge base architecture](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

---

## What This Is

ARC is a structured workspace that turns an AI agent into a persistent operating partner for your business. Instead of re-explaining your business every time you open a chat, ARC builds and maintains a **wiki of interlinked articles** about your business that the agent reads automatically.

After setup, your agent has a wiki covering:
- what your business does and how it makes money
- who you are, what you're good at, and where you need help
- what tools and platforms you use
- what your current priorities and pain points are
- how all of these connect together

The wiki grows every session. Questions you ask, documents you import, explorations you run — all of it feeds back into the knowledge base. The agent handles all the bookkeeping: creating articles, maintaining cross-references, flagging contradictions, and keeping everything current.

ARC is designed for both technical and non-technical founders, and works in Claude Code, Codex, Cursor, and Claude Desktop.

### What founders usually get wrong about AI

Most founders use AI like a very smart intern in a blank chat:
- they repeat context every time
- they get generic answers
- they do not build any continuity
- they never turn good outputs into reusable workflows

ARC fixes that. It gives the agent a compounding knowledge base, automated capture, and a repeatable operating model.

### What this is for

ARC is for founders who want to:
- get more leverage from AI without becoming deeply technical
- capture business context once and have it compound over time
- identify what work should stay human, what should be AI-assisted, and what could become a workflow
- start simple now and layer on more sophistication later

### What this is not

ARC is not:
- a SaaS product
- a no-code automation platform
- a promise that AI will run your company for you
- a giant prebuilt system you need to understand before it becomes useful

It is a practical starting point for building an AI operating layer around your actual business.

---

## Getting Started

### Step 1 — Clone or download this repo

### Step 2 — Open it in your environment

**VS Code + Claude Code extension** (recommended):
1. Open the `arc-starter` folder in VS Code
2. Open the Claude Code panel
3. Start a conversation — the agent reads CLAUDE.md and the wiki automatically

**Cursor + Claude Code extension**:
1. Open the `arc-starter` folder in Cursor
2. Open the Claude Code panel
3. Same as above

**Codex (VS Code extension)**:
1. Open the `arc-starter` folder in VS Code
2. Codex reads AGENTS.md for context
3. Start a conversation in natural language

**Claude Desktop**:
1. Create a new Project
2. Drag `CLAUDE.md` and `context/` files into the Project Knowledge
3. Start a conversation in natural language
4. Note: automated hooks are not available in Claude Desktop — use `/reflect` manually

**Terminal (Claude Code CLI)**:
1. `cd` into the `arc-starter` folder
2. Run `claude` to start a session
3. Claude Code reads CLAUDE.md and hooks fire automatically

### Step 3 — Start the conversation

Say **"help me get started"**, **"let's set up"**, or use `/setup`. The agent will interview you about your business and build an initial wiki with ~15-25 cross-referenced articles. There are two modes:

- **Quick setup** (~15 minutes) — captures the essentials
- **Deep setup** (~30 minutes) — comprehensive interview

**Have existing documents?** Drop pitch decks, one-pagers, business plans, or any relevant docs into the `imports/` folder before starting setup. The agent will analyze them first.

### Step 5 — Start using it

Once the wiki is built, you can:

- Ask it for a **quick win** so it does one useful thing immediately
- Ask questions about your business and get answers grounded in your wiki
- Drop documents in `imports/` and say **"ingest this"** to grow the wiki
- Ask it to **brainstorm** what to automate or improve
- Ask it to **audit** your tasks for a systematic inventory
- Ask it to **explore** a specific idea and spec it out
- Ask it to **reflect** to review recent work and compile insights
- Ask it to **lint** the wiki to check for gaps and contradictions

The wiki grows automatically — sessions are captured by hooks, insights are compiled into articles, and every interaction makes the agent smarter.

---

## Commands

| Command | Or just say... | What it does |
|---------|---------------|--------------|
| `/setup` | "let's set up" | Interviews you and builds the initial wiki |
| `/first-win` | "get me a quick win" | Recommends the fastest useful thing, then does it |
| `/reflect` | "review what we learned" | Reviews recent activity and compiles knowledge into wiki |
| `/brainstorm` | "what should I automate?" | Suggests automation opportunities from wiki knowledge |
| `/audit` | "audit my tasks" | Structured task audit to find what to automate first |
| `/explore` | "explore this idea" | Research and spec an idea into a buildable plan |
| `/ingest` | "ingest this document" | Process a document from imports/ into wiki articles |
| `/lint` | "check the wiki" | Wiki health check — contradictions, orphans, gaps |

---

## Workspace Structure

```
arc-starter/
├── CLAUDE.md              # Agent instructions (Claude Code / Cursor)
├── AGENTS.md              # Same content (Codex / Hermes / other agents)
├── README.md              # You are here
├── context/               # Quick-scan business snapshot
│   ├── workspace.md       # Environment, preferences, setup constraints
│   ├── setup-status.md    # Setup progress tracker
│   ├── overview.md        # One-page business summary (summary of the wiki)
│   └── memory.md          # Preferences and corrections
├── wiki/                  # LLM-maintained compounding knowledge base
│   ├── index.md           # Master catalog — agent reads this for all queries
│   ├── log.md             # Chronological record of wiki operations
│   ├── concepts/          # Atomic articles: one per business concept, entity, topic
│   └── connections/       # Cross-cutting insights linking 2+ concepts
├── daily/                 # Session logs (auto-captured by hooks)
├── imports/               # Drop zone for documents to ingest
├── explorations/          # Output from /explore — specs and plans
├── hooks/                 # Automation scripts (session capture, compilation)
├── scripts/               # Utility scripts (compile, flush, lint)
├── extensions/active/     # Optional overlays from later session packs
├── .claude/               # Claude Code settings and slash commands
│   ├── settings.json      # Hook configuration
│   └── commands/          # Workflow prompts
├── .codex/                # Codex configuration
│   ├── config.toml        # Feature flags (hooks enabled)
│   └── hooks.json         # Codex hook configuration
└── guides/                # Reference material for founders
```

---

## How the Wiki Works

The wiki is inspired by [Karpathy's LLM knowledge base pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). Three layers:

1. **Raw sources** (`imports/` + `daily/`) — Documents you drop in and automatic session logs. Immutable inputs.
2. **The wiki** (`wiki/`) — Cross-referenced markdown articles the AI creates and maintains. This is the compounding knowledge base.
3. **The schema** (`CLAUDE.md`) — Instructions that tell the AI how to manage the wiki.

Three core operations:
- **Ingest** — Process a new source into wiki articles, updating cross-references across 10-15 pages
- **Query** — Ask questions; good answers get filed back into the wiki
- **Lint** — Health-check for contradictions, orphan pages, and gaps

The wiki grows through use. The agent handles all the bookkeeping. You never maintain it manually.

---

## Automated Knowledge Capture

ARC uses hooks to automatically capture and compile knowledge. This is optional but recommended — the agent will offer to set it up during your first session.

**How it works:**
- **Session start** — Injects wiki index + business overview so the agent starts fully informed (works immediately, no setup needed)
- **Session end** — Captures conversation insights and appends to daily logs
- **Pre-compact** (Claude Code only) — Captures knowledge before context compression in long sessions
- **Nightly compilation** — Promotes daily log entries into structured wiki articles

**Setup:** The agent will offer to run `./setup.sh` during your first conversation. This installs the tools needed for automated capture. If you prefer to do it manually:

```bash
./setup.sh
```

This installs [uv](https://docs.astral.sh/uv/) (a Python package manager) and the project dependencies. It handles everything automatically.

**Without automated capture:** ARC still works. The wiki grows through commands like `/setup`, `/reflect`, `/ingest`, and `/explore`. Automated capture just means it also learns from every conversation passively.

**Claude Desktop users:** Hooks aren't available in Claude Desktop. Use `/reflect` manually after productive sessions.

---

## Guides

- **what-is-this.md** — Plain-English explanation of the workspace
- **skills-explained.md** — What skills are and how to create your own
- **mcps-explained.md** — What MCP integrations are and when to add them
- **privacy-and-imports.md** — How to think about importing documents safely
- **session-roadmap.md** — How ARC grows across Session 1, 2, and 3
- **troubleshooting.md** — What to do when things are confusing
- **next-steps.md** — Where to go after the basics

---

## The ARC Progression

**Layer 1 — Wiki Foundation** (start here)
Set up your workspace and build the initial wiki. This alone makes every AI conversation dramatically better — and it compounds from day one.

**Layer 2 — Workflows**
Build specific workflows that automate or augment tasks. Add tool integrations. Create custom commands. The wiki gives every workflow deep business context.

**Layer 3 — Systems**
Scale from personal use to team infrastructure. Add guardrails, permissions, scheduling, and orchestration.

Each layer builds on the previous one. Start with the wiki and let it grow.

---

*ARC by Arcane Intelligence. Proprietary — provided to workshop participants only.*
