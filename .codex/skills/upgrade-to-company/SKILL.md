---
name: upgrade-to-company
description: Convert a personal ARC second brain into a shared company brain. A deliberate, reviewed ritual that crosses a trust boundary — default-deny, founder-approved, never a one-click switch. Trigger on "make this a company brain", "share this with my team", "upgrade to company", "set up the team version", or "/upgrade-to-company".
metadata:
  short-description: Personal → company brain, with a fail-closed privacy gate
---

# upgrade-to-company

Turn this personal ARC workspace into a **company** (shared) second brain: one
git-backed source of truth the team clones, plus a local-only `private/` tier that
never leaves the founder's machine.

This is a **trust-boundary crossing**, not a storage move. A personal brain holds
candid content (comp, equity, health, opinions about named people, career thoughts)
that is safe for one reader and a leak the moment the company can read it. The
boundary is therefore **structural and fail-closed**.

## Hard rules

- **Default-deny.** Nothing becomes company-visible until the founder approves it in
  the manifest. When unsure, an item stays private.
- **Never push to a public remote.** `gh repo view --json visibility`; abort if PUBLIC.
- **Structure is the boundary** — the `private/` folder + `.gitignore`, not frontmatter.
- **You propose, the founder decides.** The classification is a draft for review.

## Flow

1. **Preconditions** — `/setup` has run. Decide where the shared brain lives: a fresh
   **private** repo under a **GitHub Organization** (best — each teammate joins with
   their own account), or a private repo with the other person added as a collaborator
   (fine for two). NEVER a shared GitHub login, and never a teammate's existing personal
   repo. Verify the remote is private (`gh repo view --json visibility`).
2. **Create the private tier** if absent: `uv run python scripts/scaffold_private.py`
   (idempotent). Confirm `.gitignore` excludes `private/`.
3. **Classify** every `wiki/` article and `context/` file as shared / private /
   ambiguous, reusing the `ai-leverage-brief` taxonomy and `business-snapshot`
   keep-personal labels. Private-by-default: personal finance / comp / equity, health,
   family, candid opinions about named people, credentials, legal, career or exit.
   Write `private/upgrade-manifest-{date}.md` (path | visibility | reason | excerpt);
   ambiguous defaults to private.
4. **Human review** — founder approves per row. **Move** (not copy) private items into
   `private/`, preserving wikilinks. Run `lint` and fix any shared→private link leak.
5. **Company scaffolding** — set `- Mode: company` in `context/workspace.md` (flips
   compile to write new captures into `private/wiki/` by default; see
   `scripts/config.py:get_mode`). Add `team-roster.md`, `roles.md`, `access-tiers.md`,
   `ways-of-working.md`. Reframe `context/overview.md` for a team audience.
6. **Shared remote** — point `origin` at the org/private repo; push only the shareable
   tree (except `private/` and gitignored paths). Teammate onboarding, each with THEIR
   OWN account: founder adds them as org member/collaborator → they `gh auth login` as
   themselves → `git clone` → run `setup.sh` (creates their own local `private/`) → read
   `SHARING.md` → work on `arc/<their-slug>` and `/sync`. No shared credentials.
7. **Govern** — write/refresh `SHARING.md`; summarize what is shared vs private and how
   to `promote`/`sync`; note that deeper rollout is a separate engagement.

## Out of scope

Multi-user RBAC, encryption at rest, multi-remote selective sync, server-enforced
access — those belong to a hosted product, not this starter kit.

## Trigger examples

- "make this a company brain"
- "share this brain with my team"
- "upgrade to company"
- "/upgrade-to-company"
