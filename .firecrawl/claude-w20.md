> ## Documentation Index
>
> Fetch the complete documentation index at: [/docs/llms.txt](https://code.claude.com/docs/llms.txt)
>
> Use this file to discover all available pages before exploring further.

[Skip to main content](https://code.claude.com/docs/en/whats-new/2026-w20#content-area)

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

Week 20 · May 11–15, 2026

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

# Week 20 · May 11–15, 2026

Copy page

Manage every Claude Code session from one screen with agent view, keep Claude working toward a goal until a condition holds, and run fast mode on Opus 4.7 by default.

Copy page

Releases [v2.1.139 → v2.1.142](https://code.claude.com/docs/en/changelog#2-1-139)3 features · May 11–15

Agent viewresearch preview

`claude agents` opens one screen for every Claude Code session: what’s running, what’s blocked on your input, and what’s done. Dispatch a bug fix, a pull request review, and a flaky-test investigation as three rows, keep working in another window, and step in only when a row needs you. Attach to any row to drop into its full conversation, then press `←` to return to the list. Each background session keeps running without a terminal attached.

Open the dashboard from your shell:

terminal

```
claude agents
```

[Agent view](https://code.claude.com/docs/en/agent-view)

/goalv2.1.139

Set a completion condition and Claude keeps working toward it across turns without you prompting each step. After every turn, a fast model checks whether the condition holds; if not, Claude starts another turn instead of handing control back. Useful for substantial work with a verifiable end state, like migrating a module until every call site compiles and tests pass. The goal clears once the condition is met, and works in interactive, `-p`, and Remote Control.

Set a goal and let Claude run until it holds:

Claude Code

```
> /goal all tests in test/auth pass and the lint step is clean
```

[Goals](https://code.claude.com/docs/en/goal)

Fast mode on Opus 4.7research preview

`/fast` now runs on Opus 4.7 by default instead of Opus 4.6. Fast mode is a high-speed Opus configuration: the same model quality at about 2.5x the speed for a higher per-token cost, useful for rapid iteration and live debugging. Pricing is unchanged at $30/$150 per MTok, the same as Opus 4.6 fast mode. To pin fast mode to Opus 4.6, set `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE=1`.

![The Claude Code model picker showing Opus 4.7 Fast 1M as the default with the Fast toggle on](https://mintcdn.com/claude-code/ITvjicPxe1SM3GX7/images/whats-new/fast-mode-opus-47.png?fit=max&auto=format&n=ITvjicPxe1SM3GX7&q=85&s=6b6d92f7748ce5328a1ee9a269fb1a87)

Toggle fast mode, now running on Opus 4.7:

Claude Code

```
> /fast
```

[Fast mode on Opus 4.7](https://code.claude.com/docs/en/fast-mode#understand-the-cost-tradeoff)

Other wins

`claude agents` gained dispatch flags (`—add-dir`, `—settings`, `—mcp-config`, `—plugin-dir`, `—permission-mode`, `—model`, `—effort`, `—dangerously-skip-permissions`) to configure background sessions, and `claude agents —cwd <path>` scopes the session list to a directory

New hook `args: string[]` exec form spawns the command directly without a shell, so path placeholders never need quoting

New `continueOnBlock` config option for `PostToolUse` hooks feeds the hook’s rejection reason back to Claude and continues the turn instead of ending it

New `terminalSequence` field in hook JSON output lets hooks emit desktop notifications, window titles, and bells without a controlling terminal

The Rewind menu added “Summarize up to here” to compress earlier context while keeping recent turns intact

Remote Control, `/schedule`, Claude.ai MCP connectors, and notification preferences are now disabled when `ANTHROPIC_API_KEY`, `apiKeyHelper`, or `ANTHROPIC_AUTH_TOKEN` is set, even alongside a Claude.ai login; unset the API key to use these features

MCP stdio servers now receive `CLAUDE_PROJECT_DIR` in their environment, matching hooks, and plugin configs can reference `${CLAUDE_PROJECT_DIR}` in commands

`claude plugin details <name>` shows a plugin’s component inventory and projected per-session token cost, and the `/plugin` details pane now also lists the LSP servers a plugin provides

Plugins with a root-level `SKILL.md` and no `skills/` subdirectory are now surfaced as a skill

`/feedback` can now include recent sessions from the last 24 hours or 7 days for issues spanning more than the current session

Agent tool `subagent_type` now matches case- and separator-insensitively, so `“Code Reviewer”` resolves to `code-reviewer`

[Full changelog for v2.1.139–v2.1.142 →](https://code.claude.com/docs/en/changelog#2-1-139)

Was this page helpful?

YesNo

[Week 21 · May 18–22](https://code.claude.com/docs/en/whats-new/2026-w21) [Week 19 · May 4–8](https://code.claude.com/docs/en/whats-new/2026-w19)

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

![The Claude Code model picker showing Opus 4.7 Fast 1M as the default with the Fast toggle on](https://mintcdn.com/claude-code/ITvjicPxe1SM3GX7/images/whats-new/fast-mode-opus-47.png?w=1100&fit=max&auto=format&n=ITvjicPxe1SM3GX7&q=85&s=73cd67b861da8a43d9c75dcad3bedd89)