> ## Documentation Index
>
> Fetch the complete documentation index at: [/docs/llms.txt](https://code.claude.com/docs/llms.txt)
>
> Use this file to discover all available pages before exploring further.

[Skip to main content](https://code.claude.com/docs/en/whats-new/2026-w13#content-area)

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

Week 13 · March 23–27, 2026

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

# Week 13 · March 23–27, 2026

Copy page

Auto mode for hands-off permissions, computer use built in, PR auto-fix in the cloud, transcript search, and a PowerShell tool for Windows.

Copy page

Releases [v2.1.83 → v2.1.85](https://code.claude.com/docs/en/changelog#2-1-83)6 features · March 23–27

Auto moderesearch preview

Auto mode hands your permission prompts to a classifier. Safe edits and commands run without interrupting you; anything destructive or suspicious gets blocked and surfaced. It’s the middle ground between approving every file write and running with `—dangerously-skip-permissions`.

![Claude Code prompt footer showing 'auto mode on (shift+tab to cycle)' indicator in yellow](https://mintcdn.com/claude-code/CfffsX01JHFnIKvD/images/whats-new/auto-mode.png?fit=max&auto=format&n=CfffsX01JHFnIKvD&q=85&s=367c9e9d4ba5bc57ec4b935154bf1fbb)

Cycle to auto with Shift+Tab, or set it as your default:

~/.claude/settings.json

```
{
  "permissions": {
    "defaultMode": "auto"
  }
}
```

[Permission modes guide](https://code.claude.com/docs/en/permission-modes)

Computer useDesktop

Claude can now control your actual desktop from the Claude Code Desktop app: open native apps, click through the iOS simulator, drive hardware control panels, and verify changes on screen. It’s off by default and asks before each action. Best for the things nothing else can reach: apps without an API, proprietary tools, anything that only exists as a GUI.

![Claude Desktop settings with the Computer use toggle enabled, showing the option to let Claude take screenshots and control your keyboard and mouse in apps you allow](https://mintcdn.com/claude-code/CfffsX01JHFnIKvD/images/whats-new/computer-use.png?fit=max&auto=format&n=CfffsX01JHFnIKvD&q=85&s=d631de2017edafff463505f8ddbc0f51)

Enable it in Settings, grant the OS permissions, then ask Claude to verify a change end to end:

Claude Code

```
> Open the iOS simulator, tap through the onboarding flow, and screenshot each step
```

[Computer use guide](https://code.claude.com/docs/en/desktop#let-claude-use-your-computer)

PR auto-fixWeb

Flip a switch when you open a PR and walk away. Claude watches CI, fixes the failures, handles the nits, and pushes until it’s green. No more babysitting a PR through six rounds of lint errors.

![Claude Code web CI panel showing the Auto fix toggle enabled, with description 'Proactively fix CI failures and review comments'](https://mintcdn.com/claude-code/CfffsX01JHFnIKvD/images/whats-new/auto-fix.png?fit=max&auto=format&n=CfffsX01JHFnIKvD&q=85&s=c62b181c6c5d96929f0b43525f9f3584)

After creating a PR on Claude Code web, toggle Auto fix in the CI panel.

[Auto-fix pull requests](https://code.claude.com/docs/en/claude-code-on-the-web#auto-fix-pull-requests)

Transcript searchv2.1.83

Press `/` in transcript mode to search your conversation. `n` and `N` step through matches. Finally a way to find that one Bash command Claude ran 400 messages ago.

Open transcript mode and search:

Claude Code

```
Ctrl+O    # open transcript
/migrate  # search for "migrate"
n         # next match
N         # previous match
```

[Fullscreen guide](https://code.claude.com/docs/en/fullscreen#search-and-review-the-conversation)

PowerShell toolpreviewv2.1.84

Windows gets a native PowerShell tool alongside Bash. Claude can run cmdlets, pipe objects, and work with Windows-native paths without translating everything through Git Bash.

Opt in from settings:

.claude/settings.json

```
{
  "env": {
    "CLAUDE_CODE_USE_POWERSHELL_TOOL": "1"
  }
}
```

[PowerShell tool docs](https://code.claude.com/docs/en/tools-reference#powershell-tool)

Conditional hooksv2.1.85

Hooks can now declare an `if` field using permission rule syntax. Your pre-commit check only spawns for `Bash(git commit *)` instead of every bash call, cutting the process overhead on busy sessions.

Scope a hook to git commits only:

.claude/settings.json

```
{
  "hooks": {
    "PreToolUse": [{\
      "hooks": [{\
        "if": "Bash(git commit *)",\
        "type": "command",\
        "command": ".claude/hooks/lint-staged.sh"\
      }]\
    }]
  }
}
```

[Hooks reference](https://code.claude.com/docs/en/hooks)

Other wins

Plugin `userConfig` now public: prompt for settings at enable time, keychain-backed secrets

Pasted images insert `[Image #N]` chips you can reference positionally

`managed-settings.d/` drop-in directory for layered policy fragments

`CwdChanged` and `FileChanged` hook events for direnv-style setups

Agents can declare `initialPrompt` in frontmatter to auto-submit a first turn

`Ctrl+X Ctrl+E` opens your external editor, matching readline

Interrupting before any response restores your input automatically

`/status` now works while Claude is responding

Deep links open in your preferred terminal, not first-detected

Idle-return nudge to `/clear` after 75+ minutes away

VS Code: rate limit banner, Esc-twice rewind picker

[Full changelog for v2.1.83–v2.1.85 →](https://code.claude.com/docs/en/changelog#2-1-83)

Was this page helpful?

YesNo

[Week 14 · Mar 30 – Apr 3](https://code.claude.com/docs/en/whats-new/2026-w14)

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

![Claude Code prompt footer showing 'auto mode on (shift+tab to cycle)' indicator in yellow](https://mintcdn.com/claude-code/CfffsX01JHFnIKvD/images/whats-new/auto-mode.png?w=1100&fit=max&auto=format&n=CfffsX01JHFnIKvD&q=85&s=83cea86510e05a3f8a7216c6e104cbc5)

![Claude Desktop settings with the Computer use toggle enabled, showing the option to let Claude take screenshots and control your keyboard and mouse in apps you allow](https://mintcdn.com/claude-code/CfffsX01JHFnIKvD/images/whats-new/computer-use.png?w=1100&fit=max&auto=format&n=CfffsX01JHFnIKvD&q=85&s=d2b9f8b4ca801bde2be15a0b7b261bd5)

![Claude Code web CI panel showing the Auto fix toggle enabled, with description 'Proactively fix CI failures and review comments'](https://mintcdn.com/claude-code/CfffsX01JHFnIKvD/images/whats-new/auto-fix.png?w=1100&fit=max&auto=format&n=CfffsX01JHFnIKvD&q=85&s=dccd0dd2f159f29c0dce450e298c0922)