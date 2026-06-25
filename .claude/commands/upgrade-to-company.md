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

Confirm `/setup` has run (a populated `wiki/` exists). If not, stop and run setup.

### Step 0b — Set up the shared GitHub home (guided)

This is where the brain will live for the whole team. Walk the founder through it;
don't just dump commands. **Run the preflight first** so you know what you can automate:

```bash
uv run python scripts/github_status.py
```

That reports whether `gh` is installed/authenticated, the login, whether they can
create repos / invite org members, and any orgs they already belong to.

**Explain the options in plain language and recommend the org:**

- **GitHub Organization (recommended).** The org owns a fresh **private** repo. Each
  teammate joins with their **own** account — no shared logins, real access control,
  survives anyone leaving. Best for a company brain.
- **Collaborators on a private repo (fine for two people).** Quicker, but ownership is
  tied to one individual; migrate to an org later.
- **Never:** a shared "company account", or using a teammate's existing personal repo.

**Important capability note:** `gh` **cannot create an organization** (there is no
`gh org create`, and org creation isn't in the API for normal accounts). Org creation
is a ~30-second browser step. Everything after it you CAN automate.

**Org path:**
1. If the preflight lists an existing org they want to use, use it. Otherwise tell them:
   "Creating the org is the one step I can't do from here — open
   <https://github.com/account/organizations/new>, pick the Free plan, name it (e.g.
   `acme-brains`), and tell me the org name when it's done." Wait for confirmation.
2. Create the private repo under the org and wire it as origin (the initial push
   happens in Step 5, after the personal branch is set up):
   ```bash
   gh repo create <org>/<repo> --private --source=. --remote=origin
   ```
3. Invite teammates (each keeps their own account):
   - If the preflight shows `admin:org`: `gh api -X PUT orgs/<org>/memberships/<user> -f role=member`
   - Else add them to the repo: `gh api -X PUT repos/<org>/<repo>/collaborators/<user> -f permission=push`
   - Else (no scope / gh limits): point them to the org's People → Invite, or
     `gh auth refresh -s admin:org` then retry.

**Collaborator path (no org):**
```bash
gh repo create <user>/<repo> --private --source=. --remote=origin
gh api -X PUT repos/<user>/<repo>/collaborators/<teammate> -f permission=push
```

**If `gh` is missing or unauthenticated:** walk them through install
(<https://cli.github.com>) and `gh auth login`, or fall back to creating the repo in the
browser and `git remote add origin <url>`.

**Always** confirm the result is private (`gh repo view --json visibility`) and **abort
if PUBLIC**.

### Step 1 — Create the private tier (if absent)

1. Run the idempotent scaffold helper (creates `private/wiki/{concepts,connections,qa}/`,
   `private/context/`, `private/wiki/index.md` + `log.md`, and `private/README.md`):
   ```bash
   uv run python scripts/scaffold_private.py
   ```
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

1. Write the shared settings to `context/sharing.md` (committed; the same for the whole
   team, unlike per-person `workspace.md`):
   - `- Mode: company` (flips compile to write new captures into `private/wiki/` by
     default; see `scripts/config.py:get_mode`).
   - `- Sync: pr` by default. Ask the founder: for a small, trusted team that wants to
     move fast without pull requests, offer `- Sync: direct` (everyone works on `main`;
     `/sync` rebases + reconciles + pushes main). PR is the safe default; recommend it
     unless they ask for direct.
2. Interview the founder briefly and create team context articles:
   `wiki/concepts/team-roster.md`, `roles.md`, `access-tiers.md`, `ways-of-working.md`.
3. Update `context/overview.md` to read as a company brain (audience = the team).

### Step 5 — Push the shared base and onboard the team

`origin` is already wired (Step 0b). Now publish and set the founder up for ongoing work:

1. Push the shareable tree to `main` (private/ and gitignored paths are excluded
   automatically): `git push -u origin main`.
2. Put the founder on their own personal branch for future sessions:
   `git switch -c arc/<slug>` (matches `scripts/config.py:get_user_branch()`).
3. **Onboard teammates — they do NOT clone arc-starter; they clone THIS repo.** Tell the
   founder to send each teammate:
   - "You've been added to the `<org>/<repo>` brain. Run `gh auth login` as yourself,
     `git clone` it, open it in your agent, and say **join the company brain** (`/join-company`)."
   - Each person uses their **own** GitHub account; no shared credentials, ever.
   The `/join-company` flow sets up that person (their environment, private tier, personal
   branch) without re-running the business interview.

### Step 6 — Govern and close out

1. Write or refresh `SHARING.md` at the repo root.
2. Summarize what is now shared, what stayed private, the capture-defaults-to-private
   rule, and how to promote (`/promote`) and rotate (`/sync`).
3. Remind the founder: deeper company rollout (permissions, scheduling, orchestration)
   is a separate engagement, not part of this command.

## Out of scope (say plainly if asked)

Multi-user RBAC, encryption at rest, multi-remote selective sync, server-enforced
access. Those belong to a hosted product, not this starter kit.
