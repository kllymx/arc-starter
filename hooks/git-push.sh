#!/usr/bin/env bash
# ARC git auto-commit + push hook (session end, Claude only)
#
# Quietly commits any changes and pushes to origin.
# Exits 0 silently in any failure case — never blocks the session.
#
# Claude only. Codex's Stop fires per-turn so auto-push there would
# commit after every message. Codex users invoke /sync manually.
#
# Skipped if not a git repo. If origin missing: commits locally only.
# If push auth fails: silently ignored (commit still succeeds).

set +e

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-$PWD}"
cd "$PROJECT_DIR" 2>/dev/null || exit 0

git rev-parse --git-dir >/dev/null 2>&1 || exit 0

# Read a `- <key>: <value>` setting from the shared sharing.md, falling back to
# the per-person workspace.md. Echoes the lowercased value (empty if unset).
arc_read_setting() {
  local key="$1" f v
  for f in "$PROJECT_DIR/context/sharing.md" "$PROJECT_DIR/context/workspace.md"; do
    [ -f "$f" ] || continue
    v="$(grep -iE "^[[:space:]]*-?[[:space:]]*${key}:[[:space:]]*[A-Za-z]" "$f" 2>/dev/null | head -1)"
    if [ -n "$v" ]; then
      printf '%s' "$v" | sed -E "s/.*:[[:space:]]*([A-Za-z][A-Za-z0-9_-]*).*/\1/" | tr '[:upper:]' '[:lower:]'
      return
    fi
  done
}

# Anything to commit?
if [ -z "$(git status --porcelain 2>/dev/null)" ]; then
  exit 0
fi

LOG_DIR="$PROJECT_DIR/.claude"
mkdir -p "$LOG_DIR" 2>/dev/null
LOG="$LOG_DIR/last-sync.log"

{
  echo "--- $(date -u +%Y-%m-%dT%H:%M:%SZ) git-push.sh ---"
} >>"$LOG" 2>&1

# Empty when detached HEAD — we must NOT fall back to "main" (that would push a
# detached commit as main). A detached HEAD skips the push entirely below.
CUR_BRANCH="$(git symbolic-ref --short HEAD 2>/dev/null)"

# Company mode + PR strategy: never push the shared main/master from a silent
# hook — work belongs on a personal branch (arc/<slug>) and PRs do the merging.
# Direct strategy (small trusted teams) works on main, so pushing it is allowed.
# Resolve mode/strategy via the Python config (single source of truth: honors
# ARC_MODE/ARC_SYNC_STRATEGY env + sharing.md/workspace.md precedence). Fall back
# to grepping the files only if python can't run.
MODE="$(python3 "$PROJECT_DIR/scripts/config_get.py" mode 2>/dev/null)"
[ -z "$MODE" ] && MODE="$(arc_read_setting Mode)"
STRATEGY="$(python3 "$PROJECT_DIR/scripts/config_get.py" sync 2>/dev/null)"
[ -z "$STRATEGY" ] && STRATEGY="$(arc_read_setting Sync)"
[ -z "$STRATEGY" ] && STRATEGY="pr"
COMPANY=0
[ "$MODE" = "company" ] && COMPANY=1

git add -A >>"$LOG" 2>&1
git commit -m "arc: $(date -u +%Y-%m-%d-%H%M)" >>"$LOG" 2>&1 || true

if [ "$COMPANY" -eq 1 ] && [ "$STRATEGY" = "pr" ] \
   && { [ "$CUR_BRANCH" = "main" ] || [ "$CUR_BRANCH" = "master" ]; }; then
  # Protect shared main: commit locally, do NOT push. The SessionStart
  # reminder + /sync move these commits onto the personal branch + open a PR.
  echo "[company-mode] On $CUR_BRANCH (pr strategy): committed locally, not pushed (protecting shared $CUR_BRANCH). Run /sync." >>"$LOG" 2>&1
  exit 0
fi

# Only attempt push if origin is configured. Pushes the CURRENT branch:
# personal arc/<slug> in company+pr, main in company+direct, or main in
# personal mode. We never block the session on a push, but we DON'T silently
# swallow a failure: it's logged clearly, and the committed-but-unpushed work
# is then surfaced at the next session start (the sync reminder reports commits
# ahead of origin/main and prompts /sync), so a failed push is recoverable.
if [ -z "$CUR_BRANCH" ]; then
  # Detached HEAD: don't guess a branch. Commit stays local; /sync sorts it out.
  echo "[arc] detached HEAD — committed locally, not pushing. Run /sync once on a branch." >>"$LOG" 2>&1
  exit 0
fi

if git remote get-url origin >/dev/null 2>&1; then
  if [ "$COMPANY" -eq 1 ]; then
    # Company mode: fail closed on the shared brain leaking — only auto-push when
    # origin is CONFIRMED private (gh pinned to origin's owner/repo so a public
    # upstream in a fork can't be mistaken for origin). If gh is missing or can't
    # determine visibility, stay safe: commits remain local and the next-session
    # sync reminder (commits ahead of origin/main) covers it.
    VIS=""
    if command -v gh >/dev/null 2>&1; then
      ORIGIN_REPO="$(git remote get-url origin 2>/dev/null | sed -E 's#^.*[:/]([^/:]+/[^/:]+?)(\.git)?/?$#\1#')"
      VIS="$(gh repo view "$ORIGIN_REPO" --json visibility -q .visibility 2>/dev/null)"
    fi

    if [ "$VIS" = "PRIVATE" ] || [ "$VIS" = "INTERNAL" ]; then
      if ! git push origin "$CUR_BRANCH" >>"$LOG" 2>&1; then
        echo "[arc] push of '$CUR_BRANCH' failed (see above). Commits are safe locally; run /sync to retry." >>"$LOG" 2>&1
      fi
    elif [ "$VIS" = "PUBLIC" ]; then
      echo "[arc] origin is PUBLIC — not auto-pushing (would leak the shared brain). Use a private remote." >>"$LOG" 2>&1
    else
      echo "[arc] could not confirm origin is private (gh missing or unavailable) — not auto-pushing to be safe. Run /sync, or install gh. Commits are safe locally." >>"$LOG" 2>&1
    fi
  else
    # Personal mode: the founder owns their own remote — push unconditionally
    # (unchanged from before company mode existed).
    if ! git push origin "$CUR_BRANCH" >>"$LOG" 2>&1; then
      echo "[arc] push of '$CUR_BRANCH' failed (see above). Commits are safe locally; run /sync to retry." >>"$LOG" 2>&1
    fi
  fi
fi

exit 0
