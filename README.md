<p align="center">
  <img src="arc-system.png" alt="ARC by Arcane Intelligence" width="700" />
</p>

# ARC

**By Arcane Intelligence — Built by Max Kelly**

ARC gives you an AI operating partner that actually knows your business, and gets
smarter every time you use it.

Open it in your AI tool, answer a few questions, and you get a workspace that has
learned how your business works. From then on you stop re-explaining yourself, and
every conversation adds to a knowledge base that compounds over time.

It works for both technical and non-technical founders, in Claude Code, Cursor,
Codex, and Claude Desktop.

---

## The idea in one minute

Most people use AI like a smart intern in a blank chat: they re-explain everything
every time, get generic answers, and never build any continuity.

ARC fixes that. Behind the scenes it keeps a **wiki**: a set of short, linked notes
about your business that the AI writes and maintains for you. It covers what you do
and how you make money, who you are and where you need help, the tools you use, your
current priorities, and how all of it connects.

You never edit the wiki by hand. The AI captures what matters from each session and
files it away automatically. You just talk to it, and it keeps getting more useful.

It is inspired by [Andrej Karpathy's LLM knowledge-base
pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).

---

## Two modes

ARC works in two modes. You start in personal mode and switch to company mode only
when you are ready to bring other people in.

### Personal brain (the default)

A single founder's operating partner. The wiki is yours, it lives on your machine
(and optionally in your own private GitHub repo as a backup), and it grows as you
work. This is where everyone starts.

### Company brain (a shared, multiplayer brain)

When you want teammates to share the brain, run **"upgrade to company"**. ARC turns
your personal workspace into a shared one that several people use at once:

- The brain lives in **one private GitHub repo** that the whole team uses. Each
  person signs in with **their own** GitHub account. No shared logins.
- Anything personal stays in a private folder on your own machine that is never
  shared. New notes are captured privately first, and you decide what to share with
  the team by saying **"promote this"**.
- Everyone works safely at the same time: each person has their own lane, changes
  come together through pull requests, and ARC merges overlapping edits for you
  instead of making you untangle them.
- A new teammate just clones the company repo and says **"join the company brain"**.
  ARC sets them up in a couple of minutes without re-interviewing the business.

The full team playbook lives in [`SHARING.md`](SHARING.md).

---

## Getting started

> **On Windows?** Install Git for Windows first (it includes Git Bash), then your AI
> tool. See [`guides/windows-setup.md`](guides/windows-setup.md) for the full path.

**1. Get the project.** Clone or download this repo. It creates a folder called
`arc-starter`.

**2. Open it in your AI tool and say "let's set up".**

- **VS Code or Cursor + Claude Code** (recommended): open the folder, open the Claude
  Code panel, say "let's set up".
- **Codex**: open the folder, say "let's set up" in plain language.
- **Claude Code in the terminal**: `cd` into the folder, run `claude`, say "let's set
  up".

> **Claude Desktop** works for conversation, but the automatic capture that grows the
> wiki needs Claude Code or Codex.

**3. That's it.** The agent will:

1. Install the automatic capture (about 30 seconds, once).
2. Ask which tool you're using and how technical to be.
3. Interview you about your business (about 15 to 30 minutes).
4. Build your starting wiki (roughly 15 to 25 linked notes).
5. Offer you a useful first win straight away.

You can pick **quick setup** (about 15 minutes) or **deep setup** (about 30).

**Have documents already?** Drop pitch decks, plans, or one-pagers into the
`imports/` folder before setup and ARC will read them first.

> **A note on permissions:** the first time you open the project, your AI tool may ask
> you to approve the project's hooks. Approve them. That's what lets ARC capture
> knowledge and stay current in the background.

---

## Using it day to day

Just talk to it. A few things you can ask for by name (or in plain language):

- **"Give me a quick win"** — it does one useful thing immediately.
- Ask questions about your business and get answers grounded in your wiki.
- **"Ingest this"** after dropping a document in `imports/`.
- **"What should I automate?"** to brainstorm leverage.
- **"Audit my tasks"** for a systematic inventory.
- **"Explore this idea"** to research and spec something.

The wiki grows on its own as you go. You don't maintain it.

---

## Commands

You can type `/command` where your tool supports it, or just say the plain-language
version. ARC understands both.

**Everyday**

| Command | Or just say... | What it does |
|---|---|---|
| `/setup` | "let's set up" | Interviews you and builds the wiki |
| `/first-win` | "give me a quick win" | Does the fastest useful thing |
| `/reflect` | "review what we learned" | Compiles recent work into the wiki |
| `/brainstorm` | "what should I automate?" | Suggests leverage from your wiki |
| `/audit` | "audit my tasks" | Finds what to automate first |
| `/explore` | "explore this idea" | Researches and specs an idea |
| `/ingest` | "ingest this" | Turns a document into wiki notes |

**Keeping the wiki healthy**

| Command | Or just say... | What it does |
|---|---|---|
| `/lint` | "check the wiki" | Finds gaps, contradictions, orphans |
| `/garden` | "tidy the wiki" | Light hygiene pass; drafts changes for review |
| `/link` | "add wikilinks" | Proposes verified links and maps of content |
| `/consolidate` | "clean up the wiki" | Heavier merge/prune pass; drafts for review |

**Sharing with a team (company mode)**

| Command | Or just say... | What it does |
|---|---|---|
| `/upgrade-to-company` | "make this a company brain" | Turns your personal brain into a shared one |
| `/join-company` | "join the company brain" | Sets up a teammate on an existing shared brain |
| `/promote` | "share this with the team" | Moves a private note into the shared wiki |
| `/sync` | "sync my changes" | Saves your work and opens/updates a pull request |
| `/reconcile` | "fix the conflicts" | Merges two people's overlapping edits |

There are a few more advanced commands (`/business-snapshot`, `/ai-leverage-brief`,
`/prototype-system`, `/skill-audit`). Ask ARC about them when you're ready.

---

## What stays private

ARC is careful about the line between your personal notes and the company's:

- A `private/` folder on your machine is **local only**. It is never shared, even in
  company mode. Personal finances, candid notes, half-formed ideas live here.
- In company mode, new captures land in your private folder first. Nothing reaches
  the team until you say **"promote this"**, which double-checks for sensitive content
  before sharing.
- Real secrets (API keys, passwords) never belong in the wiki at all. Use a `.env`
  file.

---

## How it works under the hood

You don't need this to use ARC, but if you're curious:

- **The wiki has three layers.** Raw sources (`imports/` and auto-captured session
  logs in `daily/`), the AI-maintained wiki (`wiki/`), and the instructions that tell
  the AI how to run it (`CLAUDE.md` / `AGENTS.md`).
- **Capture is automatic, via hooks.** At session start ARC loads a lean summary so
  the AI is oriented without bloat. During and at the end of a session it captures
  what was discussed, and compiles it into wiki notes. This works in Claude Code
  (fullest support) and Codex; Claude Desktop is conversation-only.
- **Everything ships in the repo.** Hooks, commands, and scripts are all included, so
  a fresh clone works out of the box after setup.

Want to check the workspace is healthy? Run `uv run python scripts/smoke_test.py`.

---

## Workspace structure

```
arc-starter/
├── CLAUDE.md / AGENTS.md   # How the AI runs the workspace (same content, two files)
├── README.md               # You are here
├── SHARING.md              # The team / company-mode playbook
├── context/                # Quick-scan snapshot the AI reads each session
├── wiki/                   # The compounding knowledge base (AI-maintained)
├── private/                # Your personal layer — local only, never shared
├── daily/                  # Auto-captured session logs
├── imports/                # Drop documents here to ingest
├── hooks/                  # Automatic capture + sync
├── scripts/                # Compile, retrieve, maintain, sync helpers
├── .claude/                # Claude Code settings, slash commands
├── .codex/                 # Codex config, skills
└── guides/                 # Plain-English reference material
```

---

## Guides

- **what-is-this.md** — Plain-English explanation of the workspace
- **session-roadmap.md** — How ARC grows from personal use to team infrastructure
- **privacy-and-imports.md** — Importing documents safely
- **skills-explained.md** / **mcps-explained.md** — Extending ARC
- **context-hygiene.md** / **wiki-retrieval.md** — Keeping it lean and finding things
- **troubleshooting.md** / **next-steps.md** — When you're stuck or ready for more

And [`SHARING.md`](SHARING.md) for everything about running ARC as a shared company
brain.

---

*ARC by Arcane Intelligence. Proprietary — provided to workshop participants only.*
