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

CUR_BRANCH="$(git symbolic-ref --short HEAD 2>/dev/null || echo main)"

# Company mode: never push to the shared main/master from a silent hook.
# Work belongs on a personal branch (arc/<slug>); PRs do the merging.
COMPANY=0
if grep -Eqi '^\s*-?\s*Mode:\s*company\b' "$PROJECT_DIR/context/workspace.md" 2>/dev/null; then
  COMPANY=1
fi

git add -A >>"$LOG" 2>&1
git commit -m "arc: $(date -u +%Y-%m-%d-%H%M)" >>"$LOG" 2>&1 || true

if [ "$COMPANY" -eq 1 ] && { [ "$CUR_BRANCH" = "main" ] || [ "$CUR_BRANCH" = "master" ]; }; then
  # Protect shared main: commit locally, do NOT push. The SessionStart
  # reminder + /sync move these commits onto the personal branch + open a PR.
  echo "[company-mode] On $CUR_BRANCH: committed locally, not pushed (protecting shared $CUR_BRANCH). Run /sync." >>"$LOG" 2>&1
  exit 0
fi

# Only attempt push if origin is configured. Pushes the CURRENT branch:
# the personal arc/<slug> branch in company mode, or main in personal mode.
if git remote get-url origin >/dev/null 2>&1; then
  git push origin "$CUR_BRANCH" >>"$LOG" 2>&1 || true
fi

exit 0
