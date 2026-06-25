#!/usr/bin/env bash
# ARC git auto-pull hook (session start)
#
# Quietly pulls main from origin if everything looks safe.
# Exits 0 silently in any failure case — never blocks the session.
#
# Skipped if:
#   - this isn't a git repo
#   - there's no origin remote
#   - the working tree is dirty (don't risk founder's WIP)
#   - any git command fails (auth, network, etc.)

set +e

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-${CODEX_PROJECT_DIR:-$PWD}}"
cd "$PROJECT_DIR" 2>/dev/null || exit 0

# Not a git repo? skip silently
git rev-parse --git-dir >/dev/null 2>&1 || exit 0

# No origin remote? skip silently (founder hasn't connected GitHub)
git remote get-url origin >/dev/null 2>&1 || exit 0

LOG_DIR="$PROJECT_DIR/.claude"
mkdir -p "$LOG_DIR" 2>/dev/null

# Company mode? Only FETCH the shared main — never auto-rebase here. A silent
# rebase that hits a conflict would leave the repo mid-rebase at session start.
# The SessionStart reminder tells the founder, and /sync does the integrate +
# LLM-assisted /reconcile under human supervision.
if grep -Eqi '^\s*-?\s*Mode:\s*company\b' "$PROJECT_DIR/context/sharing.md" "$PROJECT_DIR/context/workspace.md" 2>/dev/null; then
  git fetch origin main >>"$LOG_DIR/last-sync.log" 2>&1 || \
    git fetch origin master >>"$LOG_DIR/last-sync.log" 2>&1 || true
  exit 0
fi

# Personal mode: safe to fast-forward the current branch.
# Working tree dirty? skip — don't risk in-progress work.
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
  exit 0
fi

DEFAULT_BRANCH="$(git symbolic-ref --short HEAD 2>/dev/null || echo main)"

git pull --rebase --autostash origin "$DEFAULT_BRANCH" \
  >>"$LOG_DIR/last-sync.log" 2>&1 || true

exit 0
