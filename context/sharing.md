# Sharing settings

> Shared, committed settings for how this ARC workspace is shared. Unlike
> `workspace.md` (which is per-person — your environment and preferences), this
> file is the same for the whole team. Don't edit it by hand; the sharing
> commands manage it.

- Mode: personal
- Sync: pr

<!--
Mode:
  personal — a single founder's brain (default). New knowledge compiles straight
             into the shared wiki/.
  company  — a shared/team brain. New auto-captured knowledge compiles into the
             local-only private/ tier first and reaches the shared wiki via /promote.
  Change only via /upgrade-to-company.

Sync (company mode only):
  pr     — each person works on a personal branch arc/<slug> and merges via pull
           requests. Safe default; nobody pushes shared main directly.
  direct — small trusted teams work on main; /sync rebases onto origin/main,
           reconciles, and pushes main directly (no branches/PRs).
-->
