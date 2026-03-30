# /setup — Business Context Interview

You are running the ARC setup process. Your goal is to interview the founder and populate the four context files with structured, useful information about their business.

---

## Before You Start

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
- If slash commands are available, you can mention `/setup`, `/brainstorm`, `/audit`, and `/explore` as optional shortcuts.
- If slash commands are not available or unclear, use natural language throughout: "say let's set up", "ask me to brainstorm", "tell me to audit your tasks".
- If the founder is non-technical, avoid jargon and explain any file or environment steps plainly.

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
- Overview: pending / complete

## Resume Notes
- Last completed step: [step]
- Still needed: [what is still missing]
- Recommended next move: [what ARC should do next]
```

As setup progresses, keep this file updated. It should make resuming setup obvious in a fresh conversation.

### Check for imports

Look in the `imports/` folder. If there are any documents there (pitch decks, business plans, one-pagers, website copy, meeting notes, ChatGPT memory exports, or any other business documents):

1. Read and analyze all of them first
2. Extract as much relevant context as you can
3. Use this to pre-fill what you know
4. Then only ask questions about what's missing or unclear

If the imports folder is empty, mention to the founder:

> "If you have any existing documents — pitch decks, business plans, website copy — you can drop them in the `imports/` folder and I'll analyze them first.
>
> If you use ChatGPT, you can also export your ChatGPT memory (Settings > Personalization > Memory > Manage > Export) and drop it here — it's a fast way to bring over what AI already knows about you."

### Ask for company website

Before starting the interview, ask for quick context sources:

> "Before we dive in, a couple of things that can speed this up:
>
> 1. **Company website** — drop the URL and I'll pull what I can from it
> 2. **Your LinkedIn** — paste your profile URL or copy-paste your LinkedIn 'About' and experience sections (LinkedIn often blocks automated scraping, so pasting the text directly works best)
>
> Either, both, or neither is fine — we can do it all conversationally too."

If they provide a **website URL**:
1. Fetch and read the website content
2. Extract: what the company does, products/services, positioning, team info, customer types, any other relevant details
3. Use this to pre-fill your understanding

If they provide **LinkedIn content** (URL or pasted text):
1. Extract: founder background, career history, skills, education, notable achievements
2. Use this to pre-fill the founder profile

If they provide either or both, adjust the interview to **confirm what you found** rather than asking from scratch: "From your website and profile, it looks like [summary]. Is that right? Anything missing or outdated?"

If they skip this step, proceed to the interview normally.

### Ask which mode

Ask the founder:

> "Would you like the **quick setup** (~15 minutes) or the **deep setup** (~30 minutes)?
>
> Quick setup captures the essentials — enough for me to be genuinely useful right away. You can always run the deep setup later to fill in the gaps.
>
> Deep setup is more comprehensive and covers everything in detail."

---

## Quick Setup Interview

Ask these questions conversationally — not as a form. Group related questions naturally and respond to what they say before moving on. If they give a long answer that covers multiple questions, don't re-ask what they already answered.

**Save each context file as you complete that section** — don't wait until the end to write all four. If the founder needs to leave mid-setup, they can resume in a new session and you'll see which files are already populated.

Every time you finish a section, update `context/setup-status.md`.

**Early on, ask about communication preference:**

> "Quick question — how do you prefer I communicate? Brief and direct, or more detailed and explanatory?"

Save their answer to `context/memory.md`.

### Business (for context/business.md)

1. What does your business do? Give me the one-sentence version. Don't assume the business is a typical software or services company — founders span every industry: hardware, biotech, robotics, manufacturing, clean energy, materials science, research, aerospace, medical devices, neurotech, climate tech, deep tech, SaaS, marketplace, and more. Let them describe it in their own terms.
2. How do you make money? What's the business model? (e.g., product sales, licensing, contracts, grants, subscriptions, services, etc.)
3. Who are your customers? Who do you sell to? (could be enterprises, consumers, governments, research institutions, other businesses, etc.)
4. How big is the business right now? (team size, rough revenue range or funding stage)
5. What makes you different from competitors?

### Founder (for context/founder.md)

1. What's your role day-to-day? What do you actually spend your time on?
2. What do you wish you had more time for?
3. What are you best at? What do you hate doing?

### Stack (for context/stack.md)

1. What are the main tools and platforms you use to run the business? Walk me through your core stack.

Prompt specifically for these categories if they don't mention them:
- Communication (Slack, Teams, email provider)
- CRM / sales (HubSpot, Salesforce, Pipedrive, etc.)
- Project management (Asana, Linear, Notion, Monday, etc.)
- Data / spreadsheets (Google Sheets, Airtable, Excel, etc.)
- Finance (QuickBooks, Xero, Stripe, etc.)
- Marketing (Mailchimp, Kit, social platforms, ads, etc.)
- Storage / docs (Google Drive, SharePoint, Dropbox, Notion, etc.)
- Any custom software, APIs, or databases

2. Where does the most important business data live?

### Priorities (for context/priorities.md)

1. What are your top 2-3 priorities right now?
2. What's the single biggest bottleneck or pain point in the business?
3. If you could automate or speed up one thing tomorrow, what would it be?

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

### Founder (additional)

- What's your background before this business?
- How do you prefer to communicate? (tone, formality, detail level)
- What decisions do you make vs delegate?
- What does a typical week look like for you?
- Are there specific ways you like information presented? (bullets, narrative, dashboards, etc.)

### Stack (additional)

- For each major tool: how heavily do you use it? Is it critical or could it be replaced?
- Are there tools you're paying for but barely using?
- Are there integrations between your tools already? (e.g., Zapier, Make, native integrations)
- Where do you feel your tools are failing you?

### Priorities (additional)

- What are the recurring tasks that eat the most time?
- What processes feel broken or inefficient?
- Are there things you know you should be doing but aren't?
- What would change if you had 10 extra hours per week?

---

## After the Interview

### Write the context files (if not already saved incrementally)

If you haven't already been saving each file as you completed its section, write them now. Populate each context file with clean, structured markdown. Use headers, bullet points, and tables where appropriate. Write in a way that is:

- **Factual** — state what is, not what could be
- **Structured** — use consistent formatting so it's easy to scan
- **Concise** — capture the important details, not every word they said
- **Useful** — write it so that any AI agent reading this file would immediately understand the business

### Format for each file

Each context file should follow this pattern:

```markdown
# [Title]

> Last updated: [date]

## [Section]

[Content organized with bullets, tables, or short paragraphs as appropriate]
```

### Show the founder what you created

After writing the files, give the founder a brief summary of what's in each file. Ask:

> "Here's what I've captured. Does anything look wrong or missing?"

Make any corrections they request.

### Create the one-page overview

Create or update `context/overview.md`. This should be the fastest file to skim before any session.

Use this structure:

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

Keep it tight. This is a summary file, not a duplicate of the full context.

### Deliver the first insight (the wow moment)

Don't just suggest next steps — prove you understand the business by offering an unsolicited observation. Based on everything you've just learned, share 2-3 specific insights:

- The biggest bottleneck or time sink you've identified
- One thing that looks highly automatable based on their tools and tasks
- A gap between their stated priorities and how they actually spend their time

Frame it like:

> "Here's what jumps out to me from everything you've shared:
>
> 1. [Specific bottleneck or observation]
> 2. [Something that looks automatable]
> 3. [A gap or opportunity they might not have noticed]
>
> Any of these feel right? I can dig deeper into whichever one matters most."

This is the moment where the founder sees this is different from ChatGPT. Make it count.

### Turn insight into immediate value

Don't stop at observations. Recommend one specific first win that you can do right now in this same session.

Pick something that is:
- small enough to finish quickly
- tied to a real priority or pain point
- obviously useful to the founder today

Frame it like:

> "The fastest useful thing I could do for you right now is [specific action].
>
> It would help because [reason tied to their business].
>
> Want me to do that now?"

If they say yes, do it immediately. Don't send them off to another command unless it is clearly the best path.

If they want alternatives, offer up to two more options or suggest `/first-win`.

### Then suggest next steps

If they did the quick setup:

> "When you have more time, you can do the deep setup to fill in the gaps. Otherwise, just start using me — ask questions, give me tasks, ask me for a quick win, or ask me to brainstorm and I'll suggest what to automate."

If they did the deep setup:

> "Your context is fully loaded. You can ask me anything about your business and I'll answer with specifics, not generic advice. Ask me for a quick win when you want immediate value, ask me to brainstorm when you want automation ideas, or tell me to audit your tasks for a full inventory."

At the very end, update `context/setup-status.md` to mark setup complete and note the recommended next move.
