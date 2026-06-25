---
name: promote
description: Promote one or more private articles into the shared company wiki, with a re-check for sensitive content and founder confirmation. The reviewed path by which a company-mode brain grows. Trigger on "share this", "promote this to the team", "this should be company knowledge", or "/promote".
metadata:
  short-description: Move a private article into the shared wiki, gated by review
---

# promote

In **company mode**, new captures land in the local-only `private/wiki/` by default.
`promote` is the deliberate, reviewed step that moves an article into the shared
`wiki/` so the team can see it — how the company brain grows without leaking.

## Preconditions

- Mode is `company` (see `context/workspace.md`). If it is still `personal`, there is
  no private tier to promote from — tell the founder and stop.

## Flow

1. **Identify** the target in `private/wiki/`. If the founder gave a topic, run
   `uv run python scripts/wiki_query.py "<topic>"` to locate it and confirm.
2. **Re-check for sensitive content** (every time): personal finance / comp / equity,
   health, family, candid opinions about named people, credentials, legal, career or
   exit. If present, show the exact lines and ask redact-then-promote or keep private.
   Default to keeping private when unsure.
3. **Confirm** with the founder; show the title and what becomes company-visible.
4. **Move** (not copy) the approved article into the matching shared `wiki/` location;
   bump its `updated:` date.
5. **Fix links** — update `wiki/index.md`, repair `[[wikilinks]]` both ways, and remove
   or rewrite any link still pointing into `private/`.
6. **Log** the promotion in `wiki/log.md` and report back.

## Rules

- Always founder-confirmed; never auto-promote.
- Keep credentials and true secrets out of the wiki entirely (use `.env`).

## Trigger examples

- "share this with the team"
- "promote this to the company wiki"
- "/promote"
