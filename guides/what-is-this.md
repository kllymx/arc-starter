# What Is This Workspace?

This is your ARC workspace — an AI-powered operating partner for your business with a compounding knowledge base.

Most founders spend the majority of their time on maintenance — answering the same questions, compiling the same reports, context-switching between tools. This workspace reclaims that time by giving you a partner that already knows your business and gets smarter every session.

Unlike ChatGPT or a regular AI chat, this workspace has **persistent, growing knowledge**. It maintains a wiki about your business — interlinked articles covering your model, customers, tools, priorities, and everything the agent learns over time. Start a new conversation and the agent already knows your business deeply because it reads the wiki, not old chat history.

---

## How It Works

### The simple version

You have a folder on your computer. Inside is a wiki of markdown files about your business that the AI maintains for you. One file tells the AI how to behave (`CLAUDE.md`). When you open this folder in your AI tool and start a conversation, the AI reads the wiki and becomes an operating partner that deeply understands your business — and gets smarter with every interaction.

### The slightly longer version

There are four things that make this different from a regular AI chat:

1. **A compounding wiki** — The AI builds and maintains a knowledge base about your business. It creates articles about your business model, customers, tools, priorities, and strategy. These articles are cross-referenced with links so the AI can navigate between connected concepts. Every conversation, every document you import, every question you ask can make the wiki smarter.

2. **Slash commands** — Pre-written prompts that guide the AI through specific workflows. Type `/brainstorm` and the AI follows a structured process to identify automation opportunities. Type `/explore` and it helps you research and spec out an idea. Type `/ingest` and it processes a document into wiki knowledge. You can also create your own.

3. **Automated capture** — Hooks run automatically at the start and end of every session. They inject your wiki context so the agent starts smart, and they capture what you discussed so knowledge doesn't disappear when the session ends. Over time, this captured knowledge gets compiled into new wiki articles.

4. **The instruction file (CLAUDE.md)** — This tells the AI what role to play, how the wiki works, and what commands are available. You can edit it to change how the AI works. Think of it as the AI's job description.

---

## The Three Layers

Your workspace has three layers of information:

### Raw Sources (`imports/` + `daily/`)
Documents you drop in and automatic session logs. These are the unprocessed inputs — the AI reads them but never changes them.

### The Wiki (`wiki/`)
Cross-referenced markdown articles the AI creates and maintains. This is the AI's knowledge base — it grows every time you use the workspace. The AI owns this layer entirely.

### Context Snapshot (`context/`)
Quick-scan files the AI reads at the start of every session for fast orientation. Think of these as the executive summary of the wiki.

---

## What Can I Do With It?

Right now, after setup:

- **Ask questions about your business** and get answers grounded in your actual wiki — not generic advice
- **Get a quick first win** and have ARC do one immediately useful thing
- **Ingest documents** — drop files in `imports/` and tell ARC to process them into wiki knowledge (`/ingest`)
- **Reflect on what worked** so the wiki grows with new insights (`/reflect`)
- **Brainstorm** what to automate or improve (`/brainstorm`)
- **Audit your tasks** to find where AI can save you the most time (`/audit`)
- **Explore ideas** and turn them into buildable plans (`/explore`)
- **Check wiki health** to find gaps, contradictions, and stale content (`/lint`)
- **Draft documents**, emails, reports, and analyses using your wiki knowledge
- **Research** competitors, markets, tools, or strategies — and the results get filed back into the wiki

Over time, as you add more to the workspace:

- Connect external tools (email, calendar, CRM, spreadsheets) so the AI can access real data
- Build custom workflows that run automatically on a schedule
- Create specialized commands for tasks you do repeatedly
- Scale from personal use to team-wide infrastructure

---

## Key Concepts

### The wiki vs chat history

In a regular AI chat, everything you've said is in the "chat history" — and it disappears when you start a new conversation. In this workspace, the important stuff lives in wiki articles. Start a new conversation and the AI still knows your business because it reads the wiki, not the old chat.

### Knowledge compounds automatically

You don't need to manually organize your knowledge base. The AI creates articles, maintains cross-references, and files useful answers back into the wiki. Hooks automatically capture session knowledge. The wiki just keeps getting smarter.

### Start new conversations often

This is different from ChatGPT where you might use one long conversation for days. With this workspace, **start a new conversation for each new topic or task.** Your wiki reloads automatically every time, so you lose nothing. Long conversations degrade quality — keep them focused.

### CLAUDE.md

This is the most important file. It's the instruction set that shapes everything the AI does. You can read it, edit it, and customize it. If you want the AI to behave differently — change this file.

### Slash commands

Pre-written prompts stored in `.claude/commands/`. When you type `/setup` or `/brainstorm`, the AI reads the corresponding file and follows the instructions. You can create your own by adding new markdown files.

### The imports folder

A drop zone. Put any documents here and tell the agent to `/ingest` them. The AI reads the document, creates wiki articles, updates existing ones, and cross-links everything.

### Obsidian (optional but recommended)

Obsidian is a free markdown editor with a graph view that shows how your wiki articles are connected. Point it at your ARC workspace folder and you can browse the wiki visually — see which concepts link to which, find orphan pages, and watch the knowledge graph grow over time.

### Extension layers

This starter is the base layer. Later sessions can extend it with optional overlays in `extensions/active/` without replacing the workspace.

---

## What Comes Next?

See `next-steps.md` for where to go after you've got the basics working.

See `session-roadmap.md` for how ARC grows across Session 1, Session 2, and Session 3.

See `skills-explained.md` and `mcps-explained.md` for advanced capabilities.
