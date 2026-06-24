[Skip to main content](https://cursor.com/docs/cli/overview#main-content)

[Cursor Logo](https://cursor.com/docs) [Docs](https://cursor.com/docs) [API](https://cursor.com/docs/api) [Learn](https://cursor.com/learn) [Help](https://cursor.com/help)

Search docs...⌘K

Ask AI⌘I

[Sign in](https://cursor.com/dashboard) [Download](https://cursor.com/downloads)

## Command Palette

Search for a command to run...

## Get Started

[Welcome](https://cursor.com/docs) [Quickstart](https://cursor.com/docs/get-started/quickstart)
Models & Pricing
[Changelog](https://cursor.com/changelog)

## Agent

[Overview](https://cursor.com/docs/agent/overview) [Agents Window](https://cursor.com/docs/agent/agents-window) [Agent Review](https://cursor.com/docs/agent/agent-review) [Planning](https://cursor.com/docs/agent/plan-mode) [Prompting](https://cursor.com/docs/agent/prompting) [Debugging](https://cursor.com/docs/agent/debug-mode) [Design Mode](https://cursor.com/docs/agent/design-mode)
Tools

Security

## Customize

[Overview](https://cursor.com/docs/customize-cursor) [Plugins](https://cursor.com/docs/plugins) [Rules](https://cursor.com/docs/rules) [Skills](https://cursor.com/docs/skills) [Subagents](https://cursor.com/docs/subagents) [Hooks](https://cursor.com/docs/hooks) [MCP](https://cursor.com/docs/mcp)

## Cloud Agents

[Overview](https://cursor.com/docs/cloud-agent) [Setup](https://cursor.com/docs/cloud-agent/setup) [Capabilities](https://cursor.com/docs/cloud-agent/capabilities) [Choose Runtime](https://cursor.com/docs/cloud-agent/choose-runtime) [My Machines](https://cursor.com/docs/cloud-agent/my-machines) [Self-Hosted Pool](https://cursor.com/docs/cloud-agent/self-hosted-pool) [Google Cloud Run](https://cursor.com/docs/cloud-agent/self-hosted-cloud-run) [Bugbot](https://cursor.com/docs/bugbot) [Automations](https://cursor.com/docs/cloud-agent/automations) [Best Practices](https://cursor.com/docs/cloud-agent/best-practices) [Security Agents](https://cursor.com/docs/security-agents) [Approval Agents](https://cursor.com/docs/approval-agents) [Security & Network](https://cursor.com/docs/cloud-agent/security-network) [Settings](https://cursor.com/docs/cloud-agent/settings) [API](https://cursor.com/docs/cloud-agent/api/endpoints)

## Integrations

[Slack](https://cursor.com/docs/integrations/slack) [Microsoft Teams](https://cursor.com/docs/integrations/microsoft-teams) [Jira](https://cursor.com/docs/integrations/jira) [Linear](https://cursor.com/docs/integrations/linear) [GitHub](https://cursor.com/docs/integrations/github) [GitLab](https://cursor.com/docs/integrations/gitlab) [Azure DevOps](https://cursor.com/docs/integrations/azure-devops) [Bitbucket](https://cursor.com/docs/integrations/bitbucket) [JetBrains](https://cursor.com/docs/integrations/jetbrains) [Xcode](https://cursor.com/docs/integrations/xcode) [Deeplinks](https://cursor.com/docs/reference/deeplinks)

## SDK

[TypeScript](https://cursor.com/docs/sdk/typescript) [Python](https://cursor.com/docs/sdk/python)

## CLI

[Overview](https://cursor.com/docs/cli/overview) [Installation](https://cursor.com/docs/cli/installation) [Capabilities](https://cursor.com/docs/cli/using) [Changelog](https://cursor.com/docs/cli/changelog) [Shell Mode](https://cursor.com/docs/cli/shell-mode) [ACP](https://cursor.com/docs/cli/acp) [Headless / CI](https://cursor.com/docs/cli/headless)
Reference

## Teams & Enterprise

Teams

Enterprise

CLI

# Cursor CLI

Cursor CLI lets you interact with AI agents directly from your terminal to write, review, and modify code. Whether you prefer an interactive terminal interface or print automation for scripts and CI pipelines, the CLI provides powerful coding assistance right where you work.

## [Getting started](https://cursor.com/docs/cli/overview\#getting-started)

```
# Install (macOS, Linux, WSL)
curl https://cursor.com/install -fsS | bash

# Install (Windows PowerShell)
irm 'https://cursor.com/install?win32=true' | iex

# Run interactive session
agent
```

## [Interactive mode](https://cursor.com/docs/cli/overview\#interactive-mode)

Start a conversational session with the agent to describe your goals, review proposed changes, and approve commands:

```
# Start interactive session
agent

# Start with initial prompt
agent "refactor the auth module to use JWT tokens"
```

## [Modes](https://cursor.com/docs/cli/overview\#modes)

The CLI supports the same modes as the editor. Switch between modes using slash commands, keyboard shortcuts, or the `--mode` flag.

| Mode | Description | Shortcut |
| --- | --- | --- |
| **Agent** | Full access to all tools for complex coding tasks | Default (no `--mode` value needed) |
| **Plan** | Design your approach before coding with clarifying questions | `Shift+Tab`, `/plan`, `--plan`, `--mode=plan` |
| **Ask** | Read-only exploration without making changes | `/ask`, `--mode=ask` |

## [Non-interactive mode](https://cursor.com/docs/cli/overview\#non-interactive-mode)

Use print mode for non-interactive scenarios like scripts, CI pipelines, or automation:

```
# Run with specific prompt and model
agent -p "find and fix performance issues" --model "gpt-5"

# Use with git changes included for review
agent -p "review these changes for security issues" --output-format text
```

## [Cloud Agent handoff](https://cursor.com/docs/cli/overview\#cloud-agent-handoff)

Push your conversation to a [Cloud Agent](https://cursor.com/docs/cloud-agent) to continue running while you're away. Prepend `&` to any message:

```
# Send a task to Cloud Agent mid-conversation
& refactor the auth module and add comprehensive tests
```

Pick up your Cloud Agent tasks on web or mobile at [cursor.com/agents](https://cursor.com/agents).

## [Sessions](https://cursor.com/docs/cli/overview\#sessions)

Resume previous conversations to maintain context across multiple interactions:

```
# Open previous chats and resume one
agent ls

# Resume latest conversation
agent resume

# Continue the previous session
agent --continue

# Resume specific conversation
agent --resume="chat-id-here"
```

## [Sandbox controls](https://cursor.com/docs/cli/overview\#sandbox-controls)

Configure command execution settings with `/sandbox` or the `--sandbox <mode>` flag (`enabled` or `disabled`). Toggle sandbox mode on or off and control network access through an interactive menu. Settings persist across sessions.

## [Max mode](https://cursor.com/docs/cli/overview\#max-mode)

Toggle [Max Mode](https://cursor.com/help/ai-features/max-mode) on models that support it using `/max-mode`.

## [Sudo password prompting](https://cursor.com/docs/cli/overview\#sudo-password-prompting)

Run commands requiring elevated privileges without leaving the CLI. When a command needs `sudo`, Cursor displays a secure, masked password prompt. Your password flows directly to `sudo` via a secure IPC channel; the AI model never sees it.

English

- English
- 简体中文
- 日本語
- 繁體中文
- Español
- Français
- Português
- 한국어
- Русский
- Türkçe
- Bahasa Indonesia
- Deutsch
- हिन्दी

- [Getting started](https://cursor.com/docs/cli/overview#getting-started)
- [Interactive mode](https://cursor.com/docs/cli/overview#interactive-mode)
- [Modes](https://cursor.com/docs/cli/overview#modes)
- [Non-interactive mode](https://cursor.com/docs/cli/overview#non-interactive-mode)
- [Cloud Agent handoff](https://cursor.com/docs/cli/overview#cloud-agent-handoff)
- [Sessions](https://cursor.com/docs/cli/overview#sessions)
- [Sandbox controls](https://cursor.com/docs/cli/overview#sandbox-controls)
- [Max mode](https://cursor.com/docs/cli/overview#max-mode)
- [Sudo password prompting](https://cursor.com/docs/cli/overview#sudo-password-prompting)

Copy page

Share feedback

Explain more

Agent

Tokenizer OffContext: 0/200k (0%)

Open chat