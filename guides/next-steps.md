# Next Steps — Where to Go From Here

You've got your ARC workspace set up and your context loaded. Here's how to get the most out of it, in roughly the order you should tackle things.

---

## Right Now (This Week)

### Get a first win immediately

Before you worry about workflows or integrations, ask ARC for a quick win. The goal is to have it do one useful thing for you right away so you can feel how this workspace is different from a generic chat.

Try:
- "Get me a quick win"
- "What can you do for me right now?"
- "Show me something useful"

The best first wins are usually things like:
- drafting an important email or memo with your business context baked in
- producing a summary, brief, or analysis you already need
- mapping one painful process clearly enough to improve it next
- creating the first version of a recurring update or briefing

### Use it conversationally

Just talk to it. Ask it questions about your business. Give it small tasks. The more you use it, the more you'll discover what it's good at and where it falls short.

Try things like:
- "What are our biggest risks right now?"
- "Draft a follow-up email to [client] about [topic]"
- "Help me think through our pricing strategy"
- "Summarize what we know about [competitor]"
- "What should I focus on this week based on my priorities?"

### Run /brainstorm

If you haven't already, run `/brainstorm` to get suggestions for what to automate or augment. This gives you a menu of ideas to work from.

### Run /audit

For a more systematic approach, run `/audit` to do a full task inventory. This shows you exactly where your time goes and which tasks have the highest automation potential.

### Keep the wiki growing

When priorities change, tell ARC — it will update the relevant wiki articles. When you add a new tool, mention it and the wiki gets updated. Drop new documents in `imports/` and say "ingest this" to process them into wiki knowledge. The workspace is only as good as the knowledge it has — and it grows automatically with every session.

### Run /reflect

After you've done a few useful tasks, ask ARC to reflect on what changed.

Try:
- "Review what we learned"
- "Reflect on recent work"
- "Update the workspace based on what changed"

This helps ARC compile durable learnings into wiki articles instead of letting good work disappear into old chats.

---

## Soon (Next 1-2 Weeks)

### Build your first workflow

Pick one thing from your brainstorm or audit results and run `/explore` to spec it out. Then build it — either with the agent's help or on your own.

Good first workflows:
- Automated meeting prep or follow-up
- A recurring research or competitor analysis
- Email drafting with your business context baked in
- A weekly report or briefing

### Create your first custom slash command

When you find yourself giving the AI the same kind of instruction repeatedly, turn it into a slash command. Create a new `.md` file in `.claude/commands/` with the instructions.

Example: if you keep asking "draft a client proposal for [company]", create a `/proposal` command that includes your proposal template, tone guidelines, and what information to include.

### Explore your first MCP

If one of your workflows would benefit from live data (email, calendar, spreadsheets), look into adding an MCP. See `mcps-explained.md` for guidance on which ones are most useful and how to set them up.

### If you're in the workshop series

Session 2 should build on this starter rather than replace it.

The pattern should be:
- keep your current workspace
- add a workflow-focused pack or extension layer
- preserve your existing context and outputs

See `session-roadmap.md` for the intended progression.

---

## Later (Weeks 3-4+)

### Build more complex workflows

Now that you have the pattern down (brainstorm → explore → build), start tackling the deeper builds from your brainstorm results. These might involve:
- Multiple tool integrations
- Scheduled automation (cron jobs)
- Multi-step workflows that chain together

### Create skills for recurring domains

If you have a whole area of your business that involves multiple related tasks (e.g., content creation, client onboarding, financial reporting), consider creating a skill. See `skills-explained.md` for how to do this.

### Think about team use

If other people in your business would benefit from this, start thinking about:
- What context they need vs what you have
- What guardrails or permissions should be in place
- Which workflows should be shared vs personal
- Who owns and maintains the workspace

### Set up a daily briefing

Once you have data integrations in place, a daily or weekly briefing is one of the highest-value automations you can build. It pulls together what happened across your business and surfaces what needs attention.

---

## The Progression

Remember: this is built in layers, not leaps.

**Layer 1 — Wiki Foundation** (where you are now)
Your workspace knows your business through a compounding wiki. You can ask questions, brainstorm, and explore ideas — and every interaction makes the wiki smarter.

**Layer 2 — Workflows**
You build specific automations and augmentations. You connect tools. You create custom commands. The workspace starts doing real work for you.

**Layer 3 — Systems**
Your workflows become reliable infrastructure. They run on schedules. They have guardrails. They can be used by your team. The workspace becomes an operating layer around your business.

Each layer builds on the previous one. Don't rush to Layer 3 — a solid Layer 1 is worth more than a shaky Layer 3.
