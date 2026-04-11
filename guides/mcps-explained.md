# MCPs — Connecting Your AI to External Tools

## What Is an MCP?

MCP stands for **Model Context Protocol**. It's a standard way to connect your AI agent to external tools and services — like Gmail, Google Calendar, Slack, spreadsheets, CRMs, and more.

Think of MCPs as plugins. Without them, your AI agent can read files and write documents, but it can't reach outside the workspace. With MCPs, it can:

- Read and draft emails
- Check your calendar
- Query your CRM
- Pull data from spreadsheets
- Search the web
- Access databases
- And much more

---

## How MCPs Work

An MCP server runs alongside your AI agent and provides it with specific capabilities. When you ask your agent something like "check my calendar for tomorrow," the agent calls the calendar MCP, which connects to Google Calendar and returns the results.

You don't need to understand the technical details. The key points:

1. **MCPs give the agent tools** — specific actions it can take in external systems
2. **You install them once** — then the agent can use them whenever relevant
3. **They need authentication** — you'll need to grant access to your accounts (like signing into Gmail)
4. **They run locally** — your data doesn't go through third-party servers (in most cases)

---

## Common MCPs for Founders

| MCP | What it does | Good for |
|---|---|---|
| **Gmail** | Read, search, and draft emails | Email triage, follow-ups, client comms |
| **Google Calendar** | View and create events, find free time | Scheduling, meeting prep, daily briefings |
| **Google Sheets** | Read and write spreadsheet data | Reports, data analysis, dashboards |
| **Slack** | Read messages and channels | Team awareness, daily briefs |
| **Notion** | Access pages and databases | Knowledge management, project tracking |
| **Web Search** | Search the internet | Research, competitor analysis, market intel |
| **File System** | Read/write files beyond the workspace | Accessing documents stored elsewhere |

---

## When to Add MCPs

**Not in your first session.** Get comfortable with the workspace and let the wiki build up first. MCPs add power but also complexity — and they're much more effective when the agent already has deep wiki knowledge of your business.

**Good time to add them:**
- When you find yourself manually copying data from a tool into the workspace
- When a workflow you're building needs live data from an external system
- When you want to automate something that involves multiple tools
- When you're ready for your daily briefing or automated reports

**Signs you don't need one yet:**
- You're still figuring out what workflows to build
- You haven't run `/brainstorm` or `/audit` yet
- Adding it feels like it's for fun rather than solving a real problem

---

## How to Add an MCP

The exact process depends on your environment, but the general steps are:

### In Claude Code (VS Code / Cursor / Terminal)

1. MCP servers are configured in your Claude Code settings
2. Some can be installed with a single command
3. Others require downloading and configuring a server
4. Once configured, the agent automatically discovers and can use the tools

### In Claude Desktop

1. Go to Settings > Developer > MCP Servers
2. Add the server configuration
3. Restart Claude Desktop
4. The tools appear in your conversation

### Authentication

Most MCPs need you to authenticate once — like signing into your Google account. After that, the agent can access the tools without you re-authenticating each time.

---

## A Note on Security

MCPs give your AI agent real access to real systems. A few things to keep in mind:

- **Start with read-only access** where possible — let the agent read your email before you let it send emails
- **Review what the agent does** — especially early on, check that it's using the tools correctly
- **Don't connect sensitive systems** until you trust the setup — start with low-risk integrations
- **Your CLAUDE.md includes a guardrail**: the agent is instructed to confirm before taking actions that affect external systems

---

## MCPs vs Skills vs Slash Commands

| | What it is | Example |
|---|---|---|
| **MCP** | A connection to an external tool | Gmail integration |
| **Skill** | A reusable workflow the agent follows | Weekly report process |
| **Slash command** | A manual prompt template | `/brainstorm` |

MCPs provide the *capabilities*. Skills and commands define *how to use them*. The wiki provides the *business knowledge*. You might have a Gmail MCP that lets the agent access email, a skill that tells it how to do your weekly email triage, and wiki knowledge that tells it who your key clients are and what tone to use.
