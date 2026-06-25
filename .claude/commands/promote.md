---
description: Promote one or more private articles into the shared company wiki, with a re-check for sensitive content. The reviewed path by which a company brain grows.
---

# /promote

In **company mode**, new captures land in the local-only `private/wiki/` by default.
`/promote` is the deliberate, reviewed step that moves an article into the shared
`wiki/` so the team can see it. This is how the company brain grows without leaking.

## When to use

- The founder says "share this", "promote this to the team", "this should be company
  knowledge", or names a private article to publish.
- After `/upgrade-to-company`, as the everyday path for growing the shared wiki.

## Preconditions

- Mode is `company` (see `context/workspace.md`). If the workspace is still
  `personal`, there is no private tier to promote from — tell the founder and stop.

## Flow

1. **Identify** the target article(s) in `private/wiki/`. If the founder described a
   topic rather than a path, run `uv run python scripts/wiki_query.py "<topic>"` to
   locate candidates and confirm which one(s) they mean.
2. **Re-check for sensitive content** (the gate, every time). Scan each article for:
   personal finance / comp / equity, health, family, candid opinions about named
   people, credentials or secrets, legal, career or exit thoughts. If any is present,
   show the founder the exact lines and ask whether to redact-then-promote or keep it
   private. Default to keeping private when unsure.
3. **Confirm** with the founder before moving anything. Show the article title and a
   one-line summary of what becomes company-visible.
4. **Move** (do not copy) the approved article from `private/wiki/...` to the matching
   shared `wiki/...` location. Update its `updated:` date.
5. **Fix links** so nothing dangles: update `wiki/index.md`, add the article to the
   shared index, repair `[[wikilinks]]` in both directions, and reuse `/link`'s
   verified-link logic. Remove or rewrite any link that still points back into
   `private/`.
6. **Log** the promotion in `wiki/log.md` and note it back to the founder.

## Rules

- Promotion is always founder-confirmed. Never auto-promote.
- Never the reverse direction silently: if a shared article needs to become private,
  that is a deliberate move too — surface it, don't just edit.
- Keep credentials and true secrets out of the wiki entirely; they belong in `.env`,
  not in either tier.
