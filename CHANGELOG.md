# Changelog

Updates to the arc-starter framework. Your `context/`, `daily/`, `wiki/`,
and `imports/` folders are never touched by updates. See
`.claude/commands/update-starter.md` (or the equivalent Codex skill) for
the safe-update contract.

---

## [Session 2 / 2026-04-25]

### Added

- **`/follow-up <name>` command + skill.** Drafts a meeting follow-up
  email grounded in your meeting notes, your arc-starter context layer,
  and recent Gmail threads. Uses Granola MCP + Gmail MCP. The flagship
  example workflow for Session 2.
- **`/brief <subject>` command + skill.** Produces a one-page founder
  brief on a client, project, or topic, synthesised from your context
  layer, recent meetings, and email threads.
- **`/triage` command + skill.** Triages your inbox into reply-now,
  later, and archive buckets. Priority is grounded in your context
  layer, so "important" reflects who actually matters to you.
- **`/update-starter` command + skill.** Pulls the latest framework
  updates from the arc-starter repo while preserving all of your
  context work. Safe-update contract baked in.
- **`.codex/skills/` directory** with project-scoped Codex skills for
  each of the above. Codex deprecated custom prompts in favour of
  skills, and skills support project-level scoping where prompts
  don't. Your Codex agent will now auto-trigger these on natural
  language (e.g. "follow up with Sarah") in addition to the explicit
  `$follow-up` syntax.

### Added (Windows support)

- **`setup.ps1`**. PowerShell equivalent of `setup.sh` for Windows
  attendees. Installs `uv` via the native PowerShell installer, runs
  `uv sync`, and prints a reminder to verify Git Bash is on PATH.
- **`.gitattributes`**. Forces LF line endings on `.sh` and `.py` files
  so a fresh clone on Windows doesn't get CRLF-converted shell scripts
  (which silently break hooks with `/bin/bash^M: bad interpreter`).
  This was almost certainly the root cause of the Claude startup
  errors Windows attendees hit last week.
- **`guides/windows-setup.md`**. Walks through Windows prerequisites
  (Git for Windows, native Claude Code install, Codex native vs WSL2)
  and the common "my hooks aren't firing" symptoms with fixes.
- **README note** at the top of Getting Started pointing Windows users
  to the new guide.

### Changed

- **`/setup` is now Windows-aware.** It tries `./setup.sh` first and
  falls back to `setup.ps1` if bash isn't available. No more silent
  stalls on Windows PowerShell sessions where `bash: command not found`
  halted the flow with no recovery path.
- Other existing commands (`/ingest`, `/reflect`, `/brainstorm`,
  `/explore`, `/first-win`, `/lint`, `/audit`) are unchanged.

### Fixed — hooks now fire correctly per harness

- **Claude Code: `Stop` → `SessionEnd`.** End-of-session capture now
  wires to `SessionEnd` (fires once at session terminate) instead of
  `Stop` (fires per turn). Long sessions are still captured by the
  existing `PreCompact` hook. Net result: one clean capture per session
  instead of one per turn, and no more per-turn status flicker.

- **Codex: `Stop` hook removed.** It was firing per turn and doing no
  work (`session-end.py` short-circuits when `CODEX_CLI` is set). Codex
  users capture manually via `/reflect`. When OpenAI ships `SessionEnd`
  or `PreCompact` for Codex (openai/codex#17148), we'll wire it up.
  Rationale and the Codex-specific workflow are documented in
  `AGENTS.md` / `CLAUDE.md` under the "Harness Notes" section.

- **Hook timeouts fixed (1000× too long).** All hook timeouts in
  `.claude/settings.json` and `.codex/hooks.json` were specified in
  milliseconds, but Claude Code and Codex both take seconds. Values
  like `15000` meant 15,000 seconds (over 4 hours) of potential hang
  if a hook got stuck. Corrected to 15s / 10s / 10s to match the
  actual intent and prevent long hangs on pathological failures.

### Added — update tooling

- **`guides/update-prompt.md`**. The canonical instruction file that
  `/update-starter` and the Session 2 bootstrap prompt both point at.
  Keeps the rules in one versioned place rather than duplicated across
  slides, command files, and memory.

- **Two-tier update allowlist.** The update protocol now distinguishes
  between OVERWRITE paths (scripts, hooks, skills, commands, package
  code — safe to replace outright) and MERGE CAREFULLY paths
  (`AGENTS.md`, `CLAUDE.md`, `README.md` — founders' agents may have
  added preference sections over the week, which must be preserved on
  update). The update agent reads both local + upstream, keeps
  local-only sections, adds upstream-only sections, and stops to ask
  when the same section differs in ways that look like founder
  customization rather than upstream rewording. The pre-flight check
  respects this split: dirty MERGE-CAREFULLY files proceed without a
  prompt (they're expected), dirty OVERWRITE files still stop and ask.

### Notes

- Commands (Claude) and skills (Codex) are two packaging models for the
  same underlying workflow. Commands are explicit — you type `/name`.
  Skills are contextual — the agent decides when to fire them based on
  the skill's description. Each harness uses its native idiom.
- The morning-brief Codex automation (weekdays 7:45am) and Claude
  routine are cloud-scheduled agents, configured in the respective
  Desktop apps. They don't live in this repo.
