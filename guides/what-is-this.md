# What Is This Workspace?

This is your ARC workspace — an AI-powered operating partner for your business.

Most founders spend the majority of their time on maintenance — answering the same questions, compiling the same reports, context-switching between tools. This workspace reclaims that time by giving you a partner that already knows your business and can help you move faster on everything from daily tasks to strategic decisions.

Unlike ChatGPT or a regular AI chat, this workspace has **persistent knowledge**. It knows your business because that knowledge is stored in files that the AI reads every time you start a conversation. You never need to re-explain who you are, what your business does, or what you're working on.

---

## How It Works

### The simple version

You have a folder on your computer with some files in it. Some of those files describe your business (the `context/` folder). One file tells the AI how to behave (`CLAUDE.md`). When you open this folder in your AI tool of choice and start a conversation, the AI reads those files and becomes an operating partner that deeply understands your business.

### The slightly longer version

There are four things that make this different from a regular AI chat:

1. **Context files** — Structured documents about your business, founder profile, tools, and priorities. The AI reads these automatically. When you update them, the AI's knowledge updates too.

2. **Slash commands** — Pre-written prompts that guide the AI through specific workflows. Type `/brainstorm` and the AI follows a structured process to identify automation opportunities. Type `/explore` and it helps you research and spec out an idea. You can also create your own.

3. **The workspace itself** — Everything the AI creates (documents, reports, explorations, audit results) lives in this folder. It builds up over time into a knowledge base about your business and the systems you've built.

4. **The instruction file (CLAUDE.md)** — This tells the AI what role to play, how to behave, and what commands are available. You can edit it to change how the AI works. Think of it as the AI's job description.

---

## What Can I Do With It?

Right now, after setup:

- **Ask questions about your business** and get answers grounded in your actual context — not generic advice
- **Brainstorm** what to automate or improve (`/brainstorm`)
- **Audit your tasks** to find where AI can save you the most time (`/audit`)
- **Explore ideas** and turn them into buildable plans (`/explore`)
- **Draft documents**, emails, reports, and analyses using your business context
- **Research** competitors, markets, tools, or strategies with your business as the lens

Over time, as you add more to the workspace:

- Connect external tools (email, calendar, CRM, spreadsheets) so the AI can access real data
- Build custom workflows that run automatically on a schedule
- Create specialized commands for tasks you do repeatedly
- Scale from personal use to team-wide infrastructure

---

## Key Concepts

### Context files vs chat history

In a regular AI chat, everything you've said is in the "chat history" — and it disappears when you start a new conversation. In this workspace, the important stuff lives in files. Start a new conversation and the AI still knows your business because it reads the files, not the old chat.

### Start new conversations often

This is different from ChatGPT where you might use one long conversation for days. With this workspace, **start a new conversation for each new topic or task.** Your context files reload automatically every time, so you lose nothing. Long conversations actually degrade quality — the AI gets less accurate the more it has to hold in one session. Keep conversations focused.

### CLAUDE.md

This is the most important file. It's the instruction set that shapes everything the AI does. You can read it, edit it, and customize it. If you want the AI to behave differently — change this file.

### Slash commands

These are pre-written prompts stored in `.claude/commands/`. When you type `/setup` or `/brainstorm`, the AI reads the corresponding file and follows the instructions in it. You can create your own by adding new markdown files to that folder.

### The imports folder

A drop zone. Put any documents here (pitch decks, business plans, reports, spreadsheets) and the `/setup` command will analyze them as part of building your context.

---

## What Comes Next?

See `next-steps.md` for where to go after you've got the basics working.

See `skills-explained.md` and `mcps-explained.md` to learn about more advanced capabilities you can add over time.
