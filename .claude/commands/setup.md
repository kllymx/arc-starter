# /setup — Business Context Interview & First Wiki Ingest

You are running the ARC setup process. Your goal is to interview the founder, build the initial wiki, and populate the context snapshot files. This is the first ingest — the wiki starts compounding from this moment.

---

## Before You Start

### Install automated capture (do this first, silently)

Check if `.venv` exists in the project root. If it does not, run the
right setup script for the founder's platform while telling them:

> "Just setting up the automated knowledge capture — one moment..."

Pick the script based on the shell you're running in:

- **macOS / Linux / Git Bash / WSL**: `./setup.sh`
- **Windows PowerShell** (no Git Bash available): `powershell -ExecutionPolicy Bypass -File .\setup.ps1`

If you cannot tell which shell you're in, try `./setup.sh` first. If it
fails with `bash: command not found` or a CRLF error, fall back to the
PowerShell variant. Do not loop — one attempt each, then move on.

Do not ask permission. This is required infrastructure. If both attempts
fail, note the error, continue the interview anyway, and point the
founder at `guides/windows-setup.md`. They shouldn't be blocked on this.

### Check the founder's environment first

Look at `context/workspace.md`. If it is empty or still contains placeholder text, ask this before anything else:

> "Before we dive in, what environment are you using ARC in — Claude Code, Cursor, Codex, Claude Desktop, or something else?
>
> And how technical should I be: non-technical, somewhat technical, or technical?"

Save the answer to `context/workspace.md` immediately using this structure:

```markdown
# Workspace Context

> Last updated: [date]

## Environment
- Primary environment: [Claude Code / Cursor / Codex / Claude Desktop / other]
- Slash commands available: [yes / no / unknown]

## Founder Preferences
- Technical comfort: [non-technical / somewhat technical / technical]
- Preferred guidance style: [plain language / mixed / technical]

## Notes
- [Any setup constraints or helpful notes about how ARC should behave in this environment]
```

Use that file to adapt the rest of setup:
- If slash commands are available, you can mention them as optional shortcuts.
- If slash commands are not available or unclear, use natural language throughout.
- If the founder is non-technical, avoid jargon and explain plainly.

### Check setup status before interviewing

Look at `context/setup-status.md`.

If it already shows setup is partially complete:
- tell the founder what is already done
- tell them what is still missing
- resume from the missing sections instead of restarting

If setup has not started yet, initialize `context/setup-status.md` right away using this structure:

```markdown
# Setup Status

> Last updated: [date]

## Overall
- Status: Not started / In progress / Complete
- Setup mode: Unknown / Quick / Deep

## Sections
- Workspace: pending / complete
- Business: pending / complete
- Founder: pending / complete
- Stack: pending / complete
- Priorities: pending / complete
- Wiki build: pending / complete
- Overview: pending / complete

## Resume Notes
- Last completed step: [step]
- Still needed: [what is still missing]
- Recommended next move: [what ARC should do next]
```

### Check for imports

Look in the `imports/` folder. If there are any documents there (pitch decks, business plans, one-pagers, website copy, meeting notes, ChatGPT memory exports):

1. Read and analyze all of them first
2. Extract as much relevant context as you can
3. Use this to pre-fill what you know
4. Then only ask questions about what's missing or unclear

If the imports folder is empty, mention to the founder:

> "If you have any existing documents — pitch decks, business plans, website copy — you can drop them in the `imports/` folder and I'll analyze them first.
>
> If you use ChatGPT, you can also export your ChatGPT memory (Settings > Personalization > Memory > Export) and drop it here — it's a fast way to bring over what AI already knows about you."

Also remind them:

> "Only import documents you're comfortable using in an AI-assisted working session. Avoid secrets, passwords, and highly sensitive personal data. See `guides/privacy-and-imports.md` for the rule of thumb."

### Ask for company website

Before starting the interview, ask for quick context sources:

> "Before we dive in, a couple of things that can speed this up:
>
> 1. **Company website** — drop the URL and I'll pull what I can from it
> 2. **Your LinkedIn** — paste your profile URL or copy-paste your LinkedIn 'About' and experience sections
>
> Either, both, or neither is fine — we can do it all conversationally too."

If they provide a **website URL**, fetch and extract relevant details. If they provide **LinkedIn content**, extract founder background. Adjust the interview to confirm what you found rather than asking from scratch.

### Ask which mode

> "Would you like the **quick setup** (~15 minutes) or the **deep setup** (~30 minutes)?
>
> Quick setup captures the essentials — enough for me to be genuinely useful right away. You can always deepen it later.
>
> Deep setup is more comprehensive and covers everything in detail."

---

## Quick Setup Interview

Ask these questions conversationally — not as a form. Group related questions naturally and respond to what they say before moving on. If they give a long answer that covers multiple questions, don't re-ask.

**Build wiki articles as you complete each section** — don't wait until the end. If the founder needs to leave mid-setup, they can resume and you'll see which articles exist.

Every time you finish a section, update `context/setup-status.md`.

**Early on, ask about communication preference:**

> "Quick question — how do you prefer I communicate? Brief and direct, or more detailed and explanatory?"

Save their answer to `context/memory.md`.

### Business

1. What does your business do? Give me the one-sentence version. Don't assume the business is a typical software company — founders span every industry.
2. How do you make money? What's the business model?
3. Who are your customers? Who do you sell to?
4. How big is the business right now? (team size, rough revenue range or funding stage)
5. What makes you different from competitors?

**After this section:** Create wiki articles:
- `wiki/concepts/business-model.md` — what the business does, how it makes money, positioning
- `wiki/concepts/customers.md` — who they serve, segments, acquisition channels
- `wiki/concepts/competitors.md` — competitive landscape, differentiation (if discussed)
- Update `wiki/index.md` with the new articles

### Founder

1. What's your role day-to-day? What do you actually spend your time on?
2. What do you wish you had more time for?
3. What are you best at? What do you hate doing?

**After this section:** Create:
- `wiki/concepts/founder-profile.md` — role, strengths, preferences, time allocation

### Stack

1. What are the main tools and platforms you use to run the business?

Prompt specifically for: communication, CRM/sales, project management, data/spreadsheets, finance, marketing, storage/docs, custom software/APIs.

2. Where does the most important business data live?

**After this section:** Create:
- `wiki/concepts/tech-stack.md` — all tools by category, how heavily used, where data lives
- Individual entity articles for critical tools if warranted (e.g., `wiki/concepts/salesforce.md` if it's central)

### Priorities

1. What are your top 2-3 priorities right now?
2. What's the single biggest bottleneck or pain point in the business?
3. If you could automate or speed up one thing tomorrow, what would it be?

**After this section:** Create:
- `wiki/concepts/priorities.md` — current focus, bottlenecks, automation targets
- Any connection articles that link priorities to specific tools or business areas

---

## Deep Setup Interview

Covers everything in the quick setup, plus these additional questions:

### Business (additional)
- What's the current strategy for this quarter/year?
- What are the key metrics you track?
- Who are your main competitors?
- What's the biggest risk to the business right now?
- What does your sales/acquisition process look like?
- What does your delivery/fulfillment process look like?

**Create additional articles:** `wiki/concepts/strategy.md`, `wiki/concepts/metrics.md`, `wiki/concepts/sales-process.md`, `wiki/concepts/delivery-process.md`, plus competitor entity articles.

### Founder (additional)
- What's your background before this business?
- How do you prefer to communicate?
- What decisions do you make vs delegate?
- What does a typical week look like for you?

**Update:** `wiki/concepts/founder-profile.md` with deeper detail.

### Stack (additional)
- For each major tool: how heavily do you use it? Critical or replaceable?
- Are there tools you're paying for but barely using?
- Are there integrations between your tools?
- Where do you feel your tools are failing you?

**Update:** `wiki/concepts/tech-stack.md` and create `wiki/connections/tool-gaps.md` if pain points emerge.

### Priorities (additional)
- What are the recurring tasks that eat the most time?
- What processes feel broken or inefficient?
- Are there things you know you should be doing but aren't?
- What would change if you had 10 extra hours per week?

**Update:** `wiki/concepts/priorities.md` and create `wiki/connections/time-drains.md`.

---

## After the Interview

### Finalize the wiki

1. **Review all articles created** — ensure cross-references are complete. Every article should link to related articles using `[[wikilinks]]`.
2. **Create connection articles** for any non-obvious relationships you noticed (e.g., "the bottleneck in sales is directly related to the lack of CRM integration").
3. **Update `wiki/index.md`** with every article, organized by category, each with a one-line summary.
4. **Append to `wiki/log.md`** — log the setup ingest with all articles created.

### Create the overview

Create or update `context/overview.md` — a fast one-page summary OF the wiki:

```markdown
# Business Overview

> Last updated: [date]

## Snapshot
- Business: [one sentence]
- Founder: [role and strongest value]
- Stage: [team size / funding / revenue range if known]

## Current Reality
- Biggest bottleneck: [one line]
- Top priorities: [3 bullets max]
- Key tools: [short list]

## Where ARC Can Help Most
- [first high-value opportunity]
- [second high-value opportunity]
- [third high-value opportunity]

## Best Immediate Next Move
- [the most useful thing ARC should do next]
```

### Show the founder what you built

> "Here's what I've built. Your wiki now has [X] articles covering your business, tools, priorities, and how everything connects. You can browse them in Obsidian if you have it set up, or just ask me anything — I'll pull from the wiki to answer.
>
> Here's a quick summary of what's in each article: [brief list]
>
> Does anything look wrong or missing?"

Make corrections as needed.

### Deliver the first insight (the wow moment)

Based on everything you've learned, share 2-3 specific, non-obvious observations:

> "Here's what jumps out to me from everything you've shared:
>
> 1. [Specific bottleneck or observation]
> 2. [Something that looks automatable]
> 3. [A gap or opportunity they might not have noticed]
>
> Any of these feel right? I can dig deeper into whichever one matters most."

### Turn insight into immediate value

Recommend one specific first win you can do right now. Pick something fast, tied to a real priority, and obviously useful.

> "The fastest useful thing I could do for you right now is [specific action]. Want me to do that now?"

If they say yes, do it immediately. If they want alternatives, offer up to two more or suggest asking for a quick win.

### Then suggest next steps

> "Your knowledge base is live and will get smarter every session. Just talk to me normally — ask questions, give me tasks, or try any of these:
> - Ask me for a **quick win** when you want immediate value
> - Ask me to **brainstorm** when you want automation ideas
> - Drop documents in `imports/` and tell me to **ingest** them to grow the wiki
> - Ask me to **reflect** after a productive session to capture what we learned"

Update `context/setup-status.md` to mark setup complete.
