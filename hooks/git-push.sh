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

CUR_BRANCH="$(git symbolic-ref --short HEAD 2>/dev/null || echo main)"

# Company mode + PR strategy: never push the shared main/master from a silent
# hook — work belongs on a personal branch (arc/<slug>) and PRs do the merging.
# Direct strategy (small trusted teams) works on main, so pushing it is allowed.
COMPANY=0
[ "$(arc_read_setting Mode)" = "company" ] && COMPANY=1
STRATEGY="$(arc_read_setting Sync)"
[ -z "$STRATEGY" ] && STRATEGY="pr"

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
# personal mode. A rejected push (e.g. direct mode, main moved) is swallowed;
# /sync rebases and reconciles.
if git remote get-url origin >/dev/null 2>&1; then
  git push origin "$CUR_BRANCH" >>"$LOG" 2>&1 || true
fi

exit 0
