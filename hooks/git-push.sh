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

git add -A >>"$LOG" 2>&1
git commit -m "arc: $(date -u +%Y-%m-%d-%H%M)" >>"$LOG" 2>&1 || true

# Only attempt push if origin is configured
if git remote get-url origin >/dev/null 2>&1; then
  DEFAULT_BRANCH="$(git symbolic-ref --short HEAD 2>/dev/null || echo main)"
  git push origin "$DEFAULT_BRANCH" >>"$LOG" 2>&1 || true
fi

exit 0
