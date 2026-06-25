# Workspace Context

> This file is populated early so the agent knows how the founder is using ARC and which environment they're in.
>
> Once populated, this file contains: which environment the founder is using (Claude Code, Codex, Cursor, etc.), whether slash commands are available, how technical the agent should be, and any setup constraints.
>
> The hooks and automation scripts also read this file to determine which LLM SDK to use for background processing (Claude Agent SDK for Claude Code, OpenAI SDK for Codex).

## Sharing

- Mode: personal

<!-- Mode is `personal` (a single founder's brain) or `company` (a shared/team
brain). In company mode, new auto-captured knowledge compiles into the local-only
private/ tier first and only reaches the shared wiki via /promote. Run
/upgrade-to-company to switch; do not flip this by hand. -->

