> ## Documentation Index
>
> Fetch the complete documentation index at: [/docs/llms.txt](https://code.claude.com/docs/llms.txt)
>
> Use this file to discover all available pages before exploring further.

[Skip to main content](https://code.claude.com/docs/en/whats-new#content-area)

[Claude Code Docs home page![light logo](https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/logo/light.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=78fd01ff4f4340295a4f66e2ea54903c)![dark logo](https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/logo/dark.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=1298a0c3b3a1da603b190d0de0e31712)](https://code.claude.com/docs/en/overview)

English

Search...

Ctrl KAsk Assistant

- [Claude Developer Platform](https://platform.claude.com/)
- [Claude Code on the Web](https://claude.ai/code)
- [Claude Code on the Web](https://claude.ai/code)

Search...

Navigation

What's New

What's new

[Getting started](https://code.claude.com/docs/en/overview) [Build with Claude Code](https://code.claude.com/docs/en/agents) [Administration](https://code.claude.com/docs/en/admin-setup) [Configuration](https://code.claude.com/docs/en/settings) [Reference](https://code.claude.com/docs/en/cli-reference) [Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview) [What's New](https://code.claude.com/docs/en/whats-new) [Resources](https://code.claude.com/docs/en/legal-and-compliance)

### What's New

- [What's new](https://code.claude.com/docs/en/whats-new)
- [Week 24 · June 8–12](https://code.claude.com/docs/en/whats-new/2026-w24)
- [Week 23 · June 1–5](https://code.claude.com/docs/en/whats-new/2026-w23)
- [Week 22 · May 25–29](https://code.claude.com/docs/en/whats-new/2026-w22)
- [Week 21 · May 18–22](https://code.claude.com/docs/en/whats-new/2026-w21)
- [Week 20 · May 11–15](https://code.claude.com/docs/en/whats-new/2026-w20)
- [Week 19 · May 4–8](https://code.claude.com/docs/en/whats-new/2026-w19)
- [Week 18 · Apr 27 – May 1](https://code.claude.com/docs/en/whats-new/2026-w18)
- [Week 17 · Apr 20–24](https://code.claude.com/docs/en/whats-new/2026-w17)
- [Week 16 · Apr 13–17](https://code.claude.com/docs/en/whats-new/2026-w16)
- [Week 15 · Apr 6–10](https://code.claude.com/docs/en/whats-new/2026-w15)
- [Week 14 · Mar 30 – Apr 3](https://code.claude.com/docs/en/whats-new/2026-w14)
- [Week 13 · Mar 23–27](https://code.claude.com/docs/en/whats-new/2026-w13)

What's New

# What's new

Copy page

A weekly digest of notable Claude Code features, with code snippets, demos, and context on why they matter.

Copy page

The weekly dev digest highlights the features most likely to change how you work. Each entry includes runnable code, a short demo, and a link to the full docs. For every bug fix and minor improvement, see the [changelog](https://code.claude.com/docs/en/changelog).

[​](https://code.claude.com/docs/en/whats-new#week-24)

Week 24

v2.1.166–v2.1.176

June 8–12, 2026

**`/cd`**: move the current session to a new working directory mid-conversation without rebuilding the prompt cache.Also this week: **sub-agents can spawn their own sub-agents** (background chains are capped at five levels deep); **`--safe-mode`** starts Claude Code with all customizations disabled for troubleshooting; and **`fallbackModel`** configures up to three fallback models tried in order.[Read the Week 24 digest →](https://code.claude.com/docs/en/whats-new/2026-w24)

[​](https://code.claude.com/docs/en/whats-new#week-23)

Week 23

v2.1.158–v2.1.165

June 1–5, 2026

**Auto mode on Bedrock, Vertex, and Foundry**: auto mode is now available on third-party providers for Opus 4.7 and Opus 4.8, replacing permission prompts with background safety checks.Also this week: **safer automatic edits** prompt before writing files that can run code in `acceptEdits` mode; **`/plugin list`** prints your installed plugins inline; and **version requirements** let managed deployments require an approved Claude Code version range.[Read the Week 23 digest →](https://code.claude.com/docs/en/whats-new/2026-w23)

[​](https://code.claude.com/docs/en/whats-new#week-22)

Week 22

v2.1.150–v2.1.157

May 25–29, 2026

**Claude Opus 4.8**: the new default model for Max, Team Premium, Enterprise pay-as-you-go, and Anthropic API accounts, with high effort by default and `/effort xhigh` for the hardest tasks.Also this week: **dynamic workflows** orchestrate dozens to hundreds of subagents from a script Claude writes; the **security-guidance plugin** reviews Claude’s changes for vulnerabilities as it works; and **fast mode** runs on Opus 4.8 at $10/$50 per MTok.[Read the Week 22 digest →](https://code.claude.com/docs/en/whats-new/2026-w22)

[​](https://code.claude.com/docs/en/whats-new#week-21)

Week 21

v2.1.143–v2.1.149

May 18–22, 2026

**Auto mode on the Pro plan**: auto mode now runs on Pro accounts and supports Sonnet 4.6 alongside Opus, replacing permission prompts with background safety checks.Also this week: **`/usage`** breaks down what drives your plan limits by skill, subagent, plugin, and MCP server; the new **`/code-review`** command reports correctness bugs; and **background sessions** appear in `/resume` and stay alive when pinned.[Read the Week 21 digest →](https://code.claude.com/docs/en/whats-new/2026-w21)

[​](https://code.claude.com/docs/en/whats-new#week-20)

Week 20

v2.1.139–v2.1.142

May 11–15, 2026

**Agent view**: `claude agents` opens one screen for every Claude Code session, showing what’s running, what’s blocked on you, and what’s done.Also this week: **`/goal`** keeps Claude working across turns until a completion condition holds; **fast mode** now runs on Opus 4.7 by default; and the **Rewind menu** can compress earlier context with “Summarize up to here”.[Read the Week 20 digest →](https://code.claude.com/docs/en/whats-new/2026-w20)

[​](https://code.claude.com/docs/en/whats-new#week-19)

Week 19

v2.1.128–v2.1.136

May 4–8, 2026

**Plugins load from `.zip` archives and URLs**: `--plugin-dir` now accepts `.zip` files, and `--plugin-url` fetches a plugin archive for the current session.Also this week: **`worktree.baseRef`** chooses whether new worktrees branch from the remote default or local `HEAD`; **auto mode hard deny rules** block actions unconditionally regardless of allow exceptions; and **hooks see the active effort level** via `effort.level` and `$CLAUDE_EFFORT`.[Read the Week 19 digest →](https://code.claude.com/docs/en/whats-new/2026-w19)

[​](https://code.claude.com/docs/en/whats-new#week-18)

Week 18

v2.1.120–v2.1.126

April 27 – May 1, 2026

**Windows without Git Bash**: Git for Windows is no longer required, and Claude Code uses PowerShell as the shell tool when Bash is absent.Also this week: **`claude ultrareview`** brings cloud code review to CI and scripts; **`claude project purge`** cleans up local state for a project; and pasting a **PR URL into `/resume`** finds the session that created it.[Read the Week 18 digest →](https://code.claude.com/docs/en/whats-new/2026-w18)

[​](https://code.claude.com/docs/en/whats-new#week-17)

Week 17

v2.1.114–v2.1.119

April 20–24, 2026

**`/ultrareview`** opens as a public research preview: a fleet of bug-hunting agents runs in the cloud and findings land back in your CLI or Desktop automatically.Also this week: **session recap** shows you what happened while a terminal was unfocused; **custom themes** let you build and ship color palettes from `/theme` or a plugin; and **Claude Code on the web** gets a redesign with a new sessions sidebar and drag-and-drop layout.[Read the Week 17 digest →](https://code.claude.com/docs/en/whats-new/2026-w17)

[​](https://code.claude.com/docs/en/whats-new#week-16)

Week 16

v2.1.105–v2.1.113

April 13–17, 2026

**Claude Opus 4.7** lands as the new default on Max and Team Premium, with a new `xhigh` effort level that’s the recommended setting for most coding work and an interactive `/effort` slider to dial it in.Also this week: **Routines** on Claude Code on the web fire templated cloud agents from a schedule, GitHub event, or API call; **mobile push notifications** ping your phone when a long task finishes or Claude needs you; `/usage` shows what’s driving your limits; and the CLI moves to native binaries.[Read the Week 16 digest →](https://code.claude.com/docs/en/whats-new/2026-w16)

[​](https://code.claude.com/docs/en/whats-new#week-15)

Week 15

v2.1.92–v2.1.101

April 6–10, 2026

**Ultraplan** enters early preview: draft a plan in the cloud from your CLI, review and comment on it in a web editor, then run it remotely or pull it back local. The first run now auto-creates a cloud environment for you.Also this week: the **Monitor** tool streams background events into the conversation so Claude can tail logs and react live, `/loop` self-paces when you omit the interval, `/team-onboarding` packages your setup into a replayable guide, and `/autofix-pr` turns on PR auto-fix from your terminal.[Read the Week 15 digest →](https://code.claude.com/docs/en/whats-new/2026-w15)

[​](https://code.claude.com/docs/en/whats-new#week-14)

Week 14

v2.1.86–v2.1.91

March 30 – April 3, 2026

**Computer use** comes to the CLI in research preview: Claude can open native apps, click through UI, and verify changes from your terminal. Best for closing the loop on things only a GUI can verify.Also this week: `/powerup` interactive lessons, flicker-free alt-screen rendering, a per-tool MCP result-size override up to 500K, and plugin executables on the Bash tool’s `PATH`.[Read the Week 14 digest →](https://code.claude.com/docs/en/whats-new/2026-w14)

[​](https://code.claude.com/docs/en/whats-new#week-13)

Week 13

v2.1.83–v2.1.85

March 23–27, 2026

**Auto mode** lands in research preview: a classifier handles your permission prompts so safe actions run without interruption and risky ones get blocked. The middle ground between approving everything and `--dangerously-skip-permissions`.Also this week: computer use in the Desktop app, PR auto-fix on Web, transcript search with `/`, a native PowerShell tool for Windows, and conditional `if` hooks.[Read the Week 13 digest →](https://code.claude.com/docs/en/whats-new/2026-w13)

Was this page helpful?

YesNo

[Week 24 · June 8–12](https://code.claude.com/docs/en/whats-new/2026-w24)

Ctrl+I

[Claude Code Docs home page![light logo](https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/logo/light.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=78fd01ff4f4340295a4f66e2ea54903c)![dark logo](https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/logo/dark.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=1298a0c3b3a1da603b190d0de0e31712)](https://code.claude.com/docs/en/overview)

[x](https://x.com/AnthropicAI) [linkedin](https://www.linkedin.com/company/anthropicresearch)

Company

[Anthropic](https://www.anthropic.com/company) [Careers](https://www.anthropic.com/careers) [Economic Futures](https://www.anthropic.com/economic-futures) [Research](https://www.anthropic.com/research) [News](https://www.anthropic.com/news) [Trust center](https://trust.anthropic.com/) [Transparency](https://www.anthropic.com/transparency)

Help and security

[Availability](https://www.anthropic.com/supported-countries) [Status](https://status.anthropic.com/) [Support center](https://support.claude.com/)

Learn

[Courses](https://www.anthropic.com/learn) [MCP connectors](https://claude.com/partners/mcp) [Customer stories](https://www.claude.com/customers) [Engineering blog](https://www.anthropic.com/engineering) [Events](https://www.anthropic.com/events) [Powered by Claude](https://claude.com/partners/powered-by-claude) [Service partners](https://claude.com/partners/services) [Startups program](https://claude.com/programs/startups)

Terms and policies

[Privacy choices](https://www.anthropic.com/legal/privacy) [Privacy policy](https://www.anthropic.com/legal/privacy) [Disclosure policy](https://www.anthropic.com/responsible-disclosure-policy) [Usage policy](https://www.anthropic.com/legal/aup) [Commercial terms](https://www.anthropic.com/legal/commercial-terms) [Consumer terms](https://www.anthropic.com/legal/consumer-terms)

Assistant

Responses are generated using AI and may contain mistakes.