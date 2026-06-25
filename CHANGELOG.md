# Changelog

Updates to the arc-starter framework. Your `context/`, `daily/`, `wiki/`,
and `imports/` folders are never touched by updates. See
`.claude/commands/update-starter.md` (or the equivalent Codex skill) for
the safe-update contract.

---

## [2026-06-25] — Company mode (personal → shared second brain)

Adds a `personal` vs `company` sharing mode so an ARC brain can grow from a single
founder's workspace into a shared team brain without leaking personal context. The
boundary is structural and fail-closed: a local-only `private/` tier, gitignored from
the shared remote, plus a default-deny upgrade ritual. Hooks and capture are unchanged;
only the compile target and retrieval scope become mode-aware.

### Added

- **`Mode` setting + `get_mode()` (`scripts/config.py`).** Resolves `personal`
  (default) or `company` from `ARC_MODE` env var or `- Mode:` in
  `context/workspace.md`. New `private/` tier path constants.
- **Mode-aware compilation (`scripts/compile.py`).** In company mode, new captures
  compile into the local-only `private/wiki/` and only reach the shared `wiki/` via
  `/promote`; personal mode is unchanged.
- **Whole-brain local retrieval (`scripts/wiki_query.py`, `scripts/context_select.py`).**
  In company mode, retrieval and SessionStart injection also span `private/wiki/` so
  the founder's connections keep surfacing locally. Teammates' clones have no
  `private/` tier (gitignored), so they see only the shared wiki.
- **`/upgrade-to-company` and `/promote`** commands (+ Codex skills). Default-deny
  upgrade with a privacy classification manifest, and the reviewed promote path.
- **`SHARING.md`** — founder-facing governance for the company-brain model.
- **`scripts/test_company_mode.py`** + a `test_company_mode_wiring` smoke check.
- **Multiplayer sync.** In company mode each person works on a personal branch
  `arc/<slug>` and merges via PRs; nobody pushes `main` directly. `get_user_branch()`
  (`scripts/config.py`) names the branch; the SessionEnd push hook refuses to push
  `main` and pushes the personal branch instead; the SessionStart pull hook only
  *fetches* `origin/main` (no silent rebase). `/sync` is now mode-aware: branch →
  commit → rebase `origin/main` → reconcile → push → open/update PR.
- **Agent-aware sync reminder (`scripts/sync_status.py`).** SessionStart (both the
  `.py` and bash hooks, so Claude + Codex) surfaces unsynced commits / open-PR /
  end-of-day prompts.
- **LLM-assisted conflict resolution.** `scripts/conflicts.py` exposes git merge
  stages (base/ours/theirs); new `/reconcile` command (+ Codex skill) unions additive
  wiki knowledge, flags genuine contradictions for the founder, and fails closed on
  `visibility: private`.
- **Private tier scaffold (`scripts/scaffold_private.py`).** Idempotent; run by
  `setup.sh` and `/setup`, so the gitignored `private/` tier exists from day one even
  in personal mode (a later upgrade is a move, not a retrofit). `/setup` now writes the
  `Mode: personal` knob into `context/workspace.md`.
- **GitHub access model documented.** `/upgrade-to-company` and `SHARING.md` are now
  explicit: the shared brain is one private repo accessed via a **GitHub Org** (or repo
  collaborators), with each person using their **own** GitHub account — never a shared
  login and never a teammate's personal repo.
- **Guided GitHub setup (`scripts/github_status.py`).** A preflight the agent runs to
  see what it can automate (gh installed/auth, scopes, existing orgs, origin/visibility).
  `/upgrade-to-company` now walks the org-vs-collaborators decision, recommends the org,
  and automates repo creation + invites + remote + push via `gh`. It's explicit that
  `gh` cannot create an org (browser step) but everything after is scriptable.
- **Teammate join flow (`/join-company` + Codex skill).** A teammate clones the *company
  repo* (not arc-starter) and runs `/join-company`, which sets them up — environment,
  their own local `private/` tier, personal branch — without re-running the business
  interview. The agent offers it automatically when a cloned company brain is detected.

### Multiplayer refinements

- **Conflict-free append files.** `.gitattributes` now sets git's `union` merge driver on
  `wiki/index.md`, `wiki/log.md`, `wiki/mocs/*.md`, and `daily/*.md`, so concurrent
  additions auto-merge instead of conflicting on nearly every sync.
- **Sync strategy.** `- Sync:` in `context/sharing.md` (read via `get_sync_strategy()`):
  `pr` (default, branches + PRs) or `direct` (small trusted teams work on `main`; `/sync`
  rebases + reconciles + pushes main, no PR). The session-end hook honors it (refuses
  `main` in `pr`, pushes `main` in `direct`).
- **Shared settings split out.** `Mode` and `Sync` now live in the committed, shared
  `context/sharing.md` instead of the per-person `workspace.md` (which is honored as a
  back-compat fallback), so changing a teammate's environment no longer touches a shared
  setting. Branch slug now handles GitHub noreply emails (`arc/<username>`).
- **Quick wins.** `uv.lock` is committed (identical deps for everyone). Merged PRs are
  cleaned up with `--delete-branch`. README rewritten as a clean, non-technical guide to
  the framework and the two modes. `/join-company` gives a first win immediately and
  notes the one-time hook-trust prompt on a fresh clone.

### Changed

- `.gitignore` now excludes `private/` and `.firecrawl/`; the previously committed
  `.firecrawl/` research scrapes were untracked (kept on disk) so they stop shipping
  on every push.
- `CLAUDE.md` / `AGENTS.md` document the two new commands and the sharing modes.

---

## [2026-06-24] — Second-brain improvements (context hygiene, retrieval, maintenance)

Implemented from a research pass on PKM/second-brain patterns for AI coding agents.
Seven independent lanes; all new wiki-mutating tools write DRAFTS for founder review
and never auto-apply.

### Added

- **Leaner SessionStart injection (Lane A).** `hooks/session-start.{py,sh}` now inject
  a high-signal *navigation layer* (overview + memory caps, wiki index headings/
  summaries, last ~2 daily-log heads) under a ~7k-char budget instead of dumping the
  full index + 7 daily logs — directly targets "context rot". New
  `scripts/context_select.py` holds the tiered assembly; the JSON hook contract is
  unchanged. Full articles are now pull-on-demand.
- **Targeted wiki retrieval (Lane B).** `scripts/wiki_query.py` — deterministic,
  no-vector keyword retrieval that returns ranked article excerpts + paths so agents
  stop reading the whole index. Optional opt-in stdio MCP server
  `scripts/wiki_query_mcp.py` (+ `extensions/wiki-query-mcp.example.json`,
  `guides/wiki-retrieval.md`).
- **`/garden` daily maintenance (Lane C).** New command + Codex skill +
  `scripts/garden.py` — a lightweight hygiene pass (stale/orphan/promote candidates)
  that drafts `wiki/garden-{date}.md` for review. Lighter than `/consolidate`.
- **`/link` verified linking + MOCs (Lane D).** New command + Codex skill +
  `scripts/link_pass.py` — proposes `[[wikilinks]]` and Maps of Content as a draft,
  validating every link against articles that actually exist (no hallucinated links).
  Adds `wiki/mocs/` with a template.
- **Context-hygiene guide & templates (Lane F).** `guides/context-hygiene.md` plus
  scoped `guides/templates/{CLAUDE.md,memory.md,agents-fragment}.example` (<200 lines).

### Changed

- **Flush distillation + provenance (Lane E).** `scripts/flush.py` — sharper
  signal/noise rules, `[durable]`/`[ephemeral]` tagging, a Sources section, a
  `_provenance:` footer on daily entries, and a `--distill-only` mode. Positional
  invocation (`flush.py <context_file> <session_id>`) preserved for the hooks.
- **Lint staleness/provenance (Lane G).** `scripts/lint.py` — new
  `check_stale_articles`, `check_missing_provenance`, and best-effort
  `check_superseded` checks wired into the report.
- Registered `/garden` and `/link` and a "Wiki retrieval & context hygiene" note in
  `CLAUDE.md` / `AGENTS.md` / `README.md`; added smoke tests for command/skill parity
  and new-module import wiring.

---

## [2026-06-24] — Codex auto-capture via `PreCompact`

### Added — Codex auto-capture via `PreCompact`

- **Codex now auto-captures long sessions.** OpenAI shipped compaction
  hooks for Codex (openai/codex#17148 — `PreCompact`/`PostCompact`), so
  `.codex/hooks.json` now wires `PreCompact` to the same capture path as
  Claude Code (`hooks/pre-compact-wrapper.sh` → `pre-compact.py`). The
  Codex short-circuit in `pre-compact.py` was removed; its transcript
  parser already handled the Codex format. Long sessions now auto-capture
  on Codex as the context compacts, instead of relying solely on manual
  `/reflect`.
- **`Stop` deliberately still NOT used on Codex.** `Stop` fires per turn,
  so capturing via it would be wasted work — auto-capture rides
  `PreCompact` instead. `SessionEnd` is still unavailable on Codex
  (openai/codex#20603), so `/reflect` remains the way to flush the final
  post-compaction stretch of a session.

### Fixed

- **`.codex/config.toml` feature flag.** `codex_hooks = true` is a
  deprecated alias and hooks are enabled by default; switched to the
  canonical `hooks = true`.
- **Stale harness notes.** `CLAUDE.md` / `AGENTS.md` said "Codex only
  exposes `SessionStart` and `Stop`" — updated to reflect Codex's current
  hooks system. `scripts/smoke_test.py` updated to assert Codex has both
  `SessionStart` and `PreCompact`.

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
