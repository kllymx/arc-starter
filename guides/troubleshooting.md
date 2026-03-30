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

---

## ARC Doesn't Seem To Know My Business Yet

Check the files in `context/`.

- If they still contain placeholder text, setup has not been completed yet.
- Start by saying "let's set up" or "help me get started".
- If setup was interrupted, ARC should use `context/setup-status.md` to resume instead of starting over.

If needed, ask:

> "What do you already know about my business from the context files?"

That is a quick way to verify what the agent has actually loaded.

---

## I'm Using Codex

Codex should read `AGENTS.md`.

- Open the `arc-starter` folder in your editor
- Start a conversation naturally
- Do not assume ARC-specific slash commands are available

If ARC seems generic, point it back to the workspace:

> "Use the instructions in AGENTS.md and the files in context/."

---

## I'm Using Claude Desktop

Claude Desktop does not automatically read the whole repo the same way a coding environment does.

For best results:
- Create a Project
- Add `CLAUDE.md`
- Add the files in `context/`
- Add any relevant documents from `imports/` if you want them included

Then begin by saying:

> "Let's set up ARC in this project."

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

ARC should store that in `context/workspace.md` and `context/memory.md`.

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
