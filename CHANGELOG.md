# Changelog

Updates to the arc-starter framework. Your `context/`, `daily/`, `wiki/`,
and `imports/` folders are never touched by updates. See
`.claude/commands/update-starter.md` (or the equivalent Codex skill) for
the safe-update contract.

---

## [Session 3 capstone / 2026-04-28]

### Added

- **`/business-snapshot` command + Codex skill.** Generates a polished
  local HTML report from the founder's ARC context and wiki, separating
  founder/operator context from company-relevant signals. Supports
  sanitized demo context via `--demo <path>`.
- **`/ai-leverage-brief` command + Codex skill.** Classifies the next
  AI leverage path as personal, one-collaborator, shared knowledge,
  internal tool, or defer. Produces an internal champion brief without
  forcing company rollout from a personal ARC.
- **`/prototype-system` command + Codex skill.** Creates the first
  believable interaction or interface for the selected AI system:
  Slack/Teams/iMessage mockup, simple internal web app, dashboard, or
  product spec.
- **`/skill-audit` command + Codex skill.** Reviews ARC context, wiki,
  and recent daily logs for repeated workflows that should become
  reusable skills. Defaults to proposal mode and saves a skill backlog;
  when the founder approves a candidate, it builds the correct Claude
  command and/or Codex skill files in the workspace.

### Changed

- **Available command lists updated** in `CLAUDE.md`, `AGENTS.md`, and
  `README.md` so agents and founders can find the Session 3 capstone
  path naturally: snapshot -> leverage brief -> prototype, with
  skill-audit as the Session 2 bridge for repeated workflows.

### Session 3 themes

The revised Session 3 framework is "from personal leverage to AI
systems." ARC remains the personal lab and reference architecture. The
capstone commands help founders decide what should stay personal, what
could become shared knowledge, and what deserves to become an internal
tool.

---

## [Session 3 patch 4 / 2026-04-27]

### Fixed

- **`/consolidate` sub-agent spawn failure: dedicated named agents
  with restricted toolsets.** Generic Task / `spawn_agent` calls
  inherit the parent session's full MCP toolset as part of the
  sub-agent's system prompt, which can blow past the prompt budget at
  startup before the sub-agent's instructions even load. Symptom:
  sub-agents fail with "prompt is too long" in <3s and 0 tokens used.
  Caught on Max's arc-demo run, where the parent had Granola, Gmail,
  and other MCPs loaded.

  Fix: ship dedicated sub-agent definitions with `tools: Read, Glob,
  Grep` only. The system prompt is tiny — no MCP tool descriptions —
  so spawning is reliable regardless of parent session state.

  New files:
  - `.claude/agents/wiki-reader.md` — Phase 1 batch reader
  - `.claude/agents/wiki-adversary.md` — Phase 2 fresh-context reviewer
  - `.codex/agents/wiki-reader.toml`
  - `.codex/agents/wiki-adversary.toml`

  Both `/consolidate` files now invoke these by name (Claude:
  `subagent_type: "wiki-reader"` via Task; Codex: `agent_name:
  "wiki_reader"` via `spawn_agent` / `spawn_agents_on_csv`) instead of
  generic spawns.

### Changed

- **Safe-update OVERWRITE list extended** to include
  `.claude/agents/**` and `.codex/agents/**`. Required so future
  updates pick up new sub-agent definitions automatically. Updated in
  `guides/update-prompt.md`, `.claude/commands/update-starter.md`,
  and `.codex/skills/update-starter/SKILL.md`.

---

## [Session 3 patch 3 / 2026-04-27]

### Fixed

- **`/consolidate` sub-agent guidance: keep spawn prompts small.** The
  patch-2 sub-agent guidance worked architecturally but failed in
  practice — agents were embedding full article CONTENT in the spawn
  prompt and tripping "prompt is too long" errors. The fix: explicit
  instructions that the parent passes only file PATHS to sub-agents
  (not contents), and each sub-agent reads files inside its own
  context window using its own tools. Same applies to the Adversary
  phase — pass only the structured proposals, not article content.
  Both `.claude/commands/consolidate.md` and
  `.codex/skills/consolidate/SKILL.md` updated.

---

## [Session 3 patch 2 / 2026-04-27]

### Changed

- **`/consolidate` teaches the agent to use sub-agents on large wikis.**
  Both the Claude command and the Codex skill now instruct: spawn
  parallel reader sub-agents per ~10–15 article batch for the Proposer
  phase, spawn ONE adversary sub-agent with fresh context for the
  Adversary phase, run Judge in the main conversation. Falls back to
  in-conversation chunked reading if sub-agents aren't available.
  Skipped entirely for wikis under ~30 articles. Triggered by an
  arc-demo test run on a 99-article wiki — the original single-context
  run produced a thoughtful but light draft; sub-agents should let the
  pipeline read more thoroughly and let the adversary phase actually
  challenge proposals from a fresh perspective.

---

## [Session 3 patch / 2026-04-27]

### Fixed

- **Safe-update OVERWRITE list extended** to include
  `extensions/active/**` and `.claude/settings.json`. Without this fix,
  re-running `/update-starter` (or the canonical `update-prompt.md`)
  silently skipped the Session 3 overlay file and the new hook
  registrations on Claude. Both `.claude/commands/update-starter.md`,
  `.codex/skills/update-starter/SKILL.md`, and
  `guides/update-prompt.md` updated to match.

---

## [Session 3 / 2026-04-27]

### Added

- **`/consolidate` command + Codex skill.** Three-phase wiki
  consolidation pipeline (proposer → adversary → judge). Drafts
  proposed merges, edits, prunes, promotions, and cross-links to
  `wiki/consolidation-{date}.md` for founder review. Never auto-applies.
  Run periodically (every 2–4 weeks) once your wiki has 10+ articles.
- **`/sync` command + Codex skill.** Manual git pull / commit / push
  for the founder's ARC. The primary git-sync path for Codex users
  (since Codex's `Stop` event fires per-turn and isn't suitable for
  auto-push). Claude users have an auto-push hook on `SessionEnd` —
  `/sync` is still useful mid-session.
- **`hooks/git-pull.sh`.** Quietly pulls main from `origin` on session
  start. Skipped if not a git repo, no remote, or working tree dirty.
  Failure modes (auth, network) are logged to `.claude/last-sync.log`
  and silently ignored — never blocks the session.
- **`hooks/git-push.sh`.** Auto-commits + pushes on session end
  (Claude only — registered on `SessionEnd`). Same defensive failure
  handling as git-pull. Founders without GitHub are unaffected — the
  hook gracefully no-ops.
- **`extensions/active/03-consolidate.md`.** Behavior overlay covering
  tier-thinking (no folder changes — agent infers tier from metadata),
  capture-on-request from cloud sessions, sub-agent stance, Routines
  awareness, and the auto-pull/push trust model.

### Changed

- **`.claude/settings.json`** registers `git-pull.sh` on `SessionStart`
  alongside the existing wiki-context loader, and `git-push.sh` on
  `SessionEnd` alongside the existing capture wrapper.
- **`.codex/hooks.json`** registers `git-pull.sh` on `SessionStart`.
  Auto-push is intentionally not registered on Codex — its `Stop`
  event fires per-turn, which would commit after every message.

### Session 3 themes

The Session 3 framework is "always-on systems": cloud sessions,
Routines, mobile reach, and the trust gradient that separates draft
from autonomous. The new commands and hooks are the layer that makes
ARC keep working when the founder isn't actively at it.

The full Session 3 deck and module spec live in the workshop planning
folder. The capstone showcase is the next milestone.

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
