> ## Documentation Index
>
> Fetch the complete documentation index at: [/docs/llms.txt](https://code.claude.com/docs/llms.txt)
>
> Use this file to discover all available pages before exploring further.

[Skip to main content](https://code.claude.com/docs/en/whats-new/2026-w19#content-area)

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

Week 19 · May 4–8, 2026

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

# Week 19 · May 4–8, 2026

Copy page

Load plugins from .zip archives and URLs, search command history across every project with Ctrl+R, branch new worktrees from local HEAD or the remote default, and block actions unconditionally with auto mode hard deny rules.

Copy page

Releases [v2.1.128 → v2.1.136](https://code.claude.com/docs/en/changelog#2-1-128)2 features · May 4–8

Plugins from .zip archives and URLs

`--plugin-dir` now accepts a `.zip` plugin archive in addition to a directory, and the new `--plugin-url` flag fetches a plugin archive from a URL for the current session. Useful for trying a plugin before adding it to a marketplace, or for shipping internal plugins from an artifact store.

Load a plugin straight from a URL:

terminal

```
claude --plugin-url https://example.com/my-plugin.zip
```

[Plugins guide](https://code.claude.com/docs/en/plugins)

History search across all your projectsv2.1.129

`Ctrl+R` reverse-search now defaults to all prompts across every project, restoring the behavior from before v2.1.124. Press `Ctrl+S` while searching to narrow back to the current project or session. Handy when you remember a command you ran in another repo last week and don’t want to go digging for it.

[Interactive mode: command history](https://code.claude.com/docs/en/interactive-mode#command-history)

Other wins

New `worktree.baseRef` setting (`fresh` \| `head`) controls whether `—worktree`, the `EnterWorktree` tool, and agent-isolation worktrees branch from the remote default branch or local `HEAD`; the default `fresh` keeps unpushed commits out of new worktrees

New `settings.autoMode.hard_deny` rules block matching actions unconditionally in auto mode, regardless of allow exceptions, for actions that should never run automatically even when broader allow rules apply

Hooks now receive the active effort level via the `effort.level` JSON input field and the `$CLAUDE_EFFORT` environment variable, and Bash tool commands can read `$CLAUDE_EFFORT`

`CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` opts out of the fullscreen alternate-screen renderer and keeps the conversation in the terminal’s native scrollback

`CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE` lets Homebrew or WinGet installations run the upgrade in the background and prompt to restart

`CLAUDE_CODE_SESSION_ID` is now in the Bash tool subprocess environment, matching the `session_id` passed to hooks

`/mcp` now shows the tool count for connected servers and flags servers that connected with 0 tools

`—channels` now works with console (API key) authentication

Subprocesses such as Bash, hooks, MCP, and LSP no longer inherit `OTEL_*` environment variables, so OTEL-instrumented apps run via the Bash tool no longer pick up the CLI’s own OTLP endpoint

Sub-agent progress summaries now hit the prompt cache, cutting `cache_creation` token cost by roughly 3x

Several OAuth and credential reliability fixes: parallel sessions no longer dead-end at 401 after a refresh-token race, MCP OAuth refresh tokens are no longer lost when multiple servers refresh concurrently, and a rare login loop from a concurrent credential write is fixed

New `parentSettingsBehavior` admin key lets admins opt SDK `managedSettings` into the policy merge

[Full changelog for v2.1.128–v2.1.136 →](https://code.claude.com/docs/en/changelog#2-1-128)

Was this page helpful?

YesNo

[Week 20 · May 11–15](https://code.claude.com/docs/en/whats-new/2026-w20) [Week 18 · Apr 27 – May 1](https://code.claude.com/docs/en/whats-new/2026-w18)

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