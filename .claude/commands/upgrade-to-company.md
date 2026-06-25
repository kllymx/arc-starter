---
description: Convert a personal ARC second brain into a shared company brain. A deliberate, reviewed ritual that crosses a trust boundary — never a one-click switch.
---

# /upgrade-to-company

Turn this personal ARC workspace into a **company** (shared) second brain: a single
git-backed source of truth the team clones, with a local-only `private/` tier that
never leaves the founder's machine.

This is a **trust-boundary crossing**, not a storage move. A personal brain
accumulates candid content (comp, equity, health, opinions about named people,
career thoughts) that is safe for one reader and a leak the moment the company can
read it. So the boundary is **structural and fail-closed**: nothing becomes
company-visible until the founder explicitly approves it.

## When to use

Recognize slash command and natural language: "make this a company brain", "share
this with my team", "upgrade to company", "set up the team version".

## Hard rules

- **Default-deny.** Nothing in the personal brain becomes shared until the founder
  approves it in the manifest. When unsure, an item stays private.
- **Never push to a public remote.** Run `gh repo view --json visibility` and abort
  if `PUBLIC` (same guardrail as `/sync`).
- **Structure is the boundary.** Privacy is enforced by the `private/` folder +
  `.gitignore`, not by trusting frontmatter or prose.
- **You propose, the founder decides.** The classification pass is a draft manifest
  for human review. You will miss things; the sign-off is the real gate.

## Flow

### Step 0 — Preconditions

1. Confirm `/setup` has run (a populated `wiki/` exists). If not, stop and run setup.
2. Confirm the target: recommend a **fresh private company repo** so the personal
   git history never ships. Alternatively designate this repo as the shared one.
3. Verify the company remote. `gh repo view --json visibility`; abort if PUBLIC.

### Step 1 — Create the private tier (if absent)

1. Create `private/`, `private/wiki/{concepts,connections,qa}/`, `private/context/`,
   and `private/wiki/index.md` + `private/wiki/log.md` (mirror the shared layout).
2. Confirm `.gitignore` excludes `private/` (it ships excluded by default).

### Step 2 — Classify (the privacy gate)

1. Walk every article in `wiki/` and every file in `context/`.
2. Classify each as **shared**, **private**, or **ambiguous**. Reuse the
   `/ai-leverage-brief` taxonomy and `business-snapshot` keep-personal labels.
   Flag as **private-by-default** anything touching: personal finance / comp /
   equity, health, family, candid opinions about named people, credentials or
   secrets, legal, career or exit thoughts.
3. Write `private/upgrade-manifest-{date}.md`: a table of
   `path | proposed visibility | reason | excerpt`. **Ambiguous defaults to private.**

### Step 3 — Human review

1. Present the manifest. The founder approves, downgrades, or overrides per row.
2. **Move** (do not copy) everything marked private into `private/wiki/` or
   `private/context/`, preserving wikilinks. Reuse `/link`'s verified-link logic so
   nothing dangles.
3. Run `/lint` and surface any link from a shared article into a now-private one — a
   shared article referencing a private one is a leak vector; fix or sever it.

### Step 4 — Company scaffolding

1. Set `- Mode: company` in `context/workspace.md` (this flips compile to write new
   captures into `private/wiki/` by default; see `scripts/config.py:get_mode`).
2. Interview the founder briefly and create team context articles:
   `wiki/concepts/team-roster.md`, `roles.md`, `access-tiers.md`, `ways-of-working.md`.
3. Update `context/overview.md` to read as a company brain (audience = the team).

### Step 5 — Establish the shared remote

1. Point the company remote at the fresh private repo.
2. Push only the shareable tree (everything except `private/` and gitignored paths).
3. Print teammate onboarding: clone, run `setup.sh`, read `SHARING.md`.

### Step 6 — Govern and close out

1. Write or refresh `SHARING.md` at the repo root.
2. Summarize what is now shared, what stayed private, the capture-defaults-to-private
   rule, and how to promote (`/promote`) and rotate (`/sync`).
3. Remind the founder: deeper company rollout (permissions, scheduling, orchestration)
   is a separate engagement, not part of this command.

## Out of scope (say plainly if asked)

Multi-user RBAC, encryption at rest, multi-remote selective sync, server-enforced
access. Those belong to a hosted product, not this starter kit.
