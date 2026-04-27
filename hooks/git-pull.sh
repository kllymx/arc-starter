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

# Working tree dirty? skip — don't risk in-progress work
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
  exit 0
fi

DEFAULT_BRANCH="$(git symbolic-ref --short HEAD 2>/dev/null || echo main)"

LOG_DIR="$PROJECT_DIR/.claude"
mkdir -p "$LOG_DIR" 2>/dev/null
git pull --rebase --autostash origin "$DEFAULT_BRANCH" \
  >>"$LOG_DIR/last-sync.log" 2>&1 || true

exit 0
