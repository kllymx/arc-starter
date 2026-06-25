# Sharing your ARC brain with your team

This file governs how ARC works as a **company brain** shared across more than one
person. Solo? You don't need this yet — keep using ARC in personal mode and run
`/upgrade-to-company` when you're ready to bring teammates in.

## The model in one paragraph

The brain lives in **one shared git repo** that is the single source of truth.
Everyone clones it. The brain grows through a deliberate promotion step, not by
everyone's agent writing into the shared canon at once. Anything personal stays in a
local `private/` folder that is gitignored and never reaches the shared repo.

## The three things that make a brain "company" instead of "personal"

1. **Where it lives** — a private GitHub repo, not a local-only folder and not a
   cloud-synced shared folder. Dropbox/Drive corrupt concurrent markdown edits and
   lose history; git is the sync layer.
2. **Who writes the canon** — `main` is the source of truth. Captures land locally;
   approved knowledge is promoted into the shared `wiki/`. Designate a curator
   (usually the founder at first).
3. **What stays private** — the `private/` tier is gitignored from the shared repo, so
   personal context never leaves your machine through the company remote.

## How company mode actually behaves

When `context/workspace.md` is set to `- Mode: company`:

- New auto-captured knowledge compiles into **`private/wiki/`**, not the shared
  `wiki/`. The privacy default is fail-closed.
- Your local retrieval and session-start context still span **both** tiers, so your
  own connections keep surfacing. Teammates only ever see the shared `wiki/`.
- Knowledge reaches the shared wiki only via **`/promote`**, which re-checks for
  sensitive content and asks you to confirm before moving anything.

## What is shared vs private

| Shared (in the company repo)        | Private (local only, in `private/`)        |
|-------------------------------------|--------------------------------------------|
| `wiki/` company knowledge           | personal finance, comp, equity             |
| `context/` company snapshot         | health, family                             |
| team roster, roles, ways of working | candid opinions about named people         |
| product, customers, process docs    | career / exit thoughts                     |
|                                     | credentials, secrets (also use `.env`)     |

When in doubt, it goes private. You can always `/promote` later; you can't un-leak.

## Daily use

- **Work normally.** New captures compile into `private/wiki/` by default.
- **Promote** durable, shareable knowledge with `/promote` (re-checks for sensitive
  content, asks you to confirm, moves it into shared `wiki/`, fixes links).
- **Pull before you start, push when you finish.** `/sync` handles this and warns if
  the remote is ever public.
- **Curate.** `/garden` and `/link` draft changes for review and never auto-apply.

## Onboarding a teammate

1. Give them access to the private company repo.
2. They clone it and run `setup.sh` (installs the capture tooling).
3. They read this file. They do **not** get your `private/` folder; it isn't in the
   repo.
4. Optional: non-technical teammates can open the repo as an Obsidian vault to browse
   the wiki without touching git.

## Keep credentials out of the brain

Never put API keys, passwords, or true secrets in any article. Use `.env` (gitignored)
and keep secret values out of `imports/` too. The brain is context, not a vault.

## What this is not

This is the lightweight shared model. A full company rollout (role-based permissions,
scheduled agents, orchestration, server-enforced access) is a larger build and a
separate engagement. Start here; layer on sophistication when you actually need it.
