#!/bin/bash
# ARC Pre-Compact Wrapper (Claude Code + Codex)
#
# Same guard as session-end-wrapper.sh. Wired to the PreCompact event on
# both harnesses; pre-compact.py handles each harness's transcript format.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

if ! command -v uv &> /dev/null; then
  exit 0
fi

if [ ! -f "$PROJECT_ROOT/uv.lock" ] && [ ! -d "$PROJECT_ROOT/.venv" ]; then
  exit 0
fi

exec uv run python "$SCRIPT_DIR/pre-compact.py"
