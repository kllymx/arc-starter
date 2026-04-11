# Troubleshooting

If ARC is not behaving the way you expect, use this guide to get unstuck quickly.

---

## Slash Commands Don't Work

That is normal in some environments.

- In Claude Code environments, slash commands like `/setup` may work as shortcuts.
- In Codex, Claude Desktop, or other environments, they may not.
- You do not need slash commands to use ARC.

Instead, just say things naturally:
- "Let's set up"
- "Get me a quick win"
- "Brainstorm what I should automate"
- "Audit my tasks"
- "Explore this idea"
- "Ingest this document"

---

## ARC Doesn't Seem To Know My Business Yet

Check the wiki. If `wiki/index.md` still says "No articles yet", setup has not been completed.

- Start by saying "let's set up" or "help me get started".
- If setup was interrupted, ARC should use `context/setup-status.md` to resume instead of starting over.

If the wiki has articles but ARC gives generic answers, ask:

> "Check the wiki index and tell me what you know about my business."

That verifies the agent is actually reading the wiki.

---

## Automated Knowledge Capture Isn't Working

ARC should install automated capture during first setup. If it didn't work:

1. **Check if `.venv` exists** in the project root. If not, dependencies weren't installed.
2. **Run `./setup.sh`** from the terminal. This installs everything needed.
3. **If `./setup.sh` fails**, it will tell you what went wrong — usually a missing tool like `curl`.

You can test if hooks are working by starting a new session — you should see your wiki context loaded automatically.

If automated capture can't be installed on your machine, the wiki still works through commands like `/reflect` and `/ingest` — but you'll need to use them manually.

---

## I'm Using Codex

Codex should read `AGENTS.md`.

- Open the `arc-starter` folder in your editor
- Start a conversation naturally
- Do not assume ARC-specific slash commands are available

If ARC seems generic, point it back to the workspace:

> "Use the instructions in AGENTS.md and the wiki in wiki/index.md."

---

## I'm Using Claude Desktop

Claude Desktop does not support hooks, which means automated knowledge capture won't run between sessions. For the full ARC experience with automated knowledge capture, use **Claude Code** or **Codex** instead.

If you still want to use Claude Desktop:
- Create a Project
- Add `CLAUDE.md`
- Add the files in `context/`
- Add `wiki/index.md`
- Begin by saying "Let's set up ARC"

Note that the wiki will only grow through direct commands in this environment, not automatically.

---

## Setup Was Interrupted

That is fine. ARC should resume rather than restart.

Ask:

> "Check setup-status and resume setup from where we left off."

If needed, you can also ask:

> "What parts of setup are already complete and what is still missing?"

---

## I Want Less Technical Explanations

Tell ARC directly. It should remember.

Try:
- "Keep this non-technical."
- "Explain it simply."
- "I want the practical version, not the technical version."

ARC stores that in `context/workspace.md` and `context/memory.md`.

---

## I Want ARC To Feel More Useful

Don't ask it broad questions first. Ask for a concrete outcome.

Good prompts:
- "Get me a quick win."
- "Draft the email I need to send about X."
- "Summarize what matters about this competitor."
- "Help me think through this decision."
- "Turn this recurring task into a repeatable workflow."

ARC gets more impressive when it is asked to produce something specific, not just discuss possibilities.

---

## I Want to Add More Knowledge

Drop documents into the `imports/` folder and tell ARC to ingest them:

> "Ingest the new documents in imports"

This reads each document, creates wiki articles, updates cross-references, and grows the knowledge base. Meeting notes, articles, competitor research, pitch decks — anything relevant.

---

## I Installed A Later Session Pack But Nothing Changed

If you extend ARC in a later session, the new files should land in `extensions/active/` plus any new commands or guides.

Check:
- that the pack was added into this workspace, not a separate folder
- that `extensions/active/` contains the new overlay files
- that you started a fresh conversation after installation

If needed, tell ARC:

> "Re-read CLAUDE.md or AGENTS.md and any files in extensions/active/ before continuing."
