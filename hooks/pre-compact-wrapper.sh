#!/bin/bash
# ARC Pre-Compact Wrapper (Claude Code only)
#
# Same guard as session-end-wrapper.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

if ! command -v uv &> /dev/null; then
  exit 0
fi

if [ ! -f "$PROJECT_ROOT/uv.lock" ] && [ ! -d "$PROJECT_ROOT/.venv" ]; then
  exit 0
fi

exec uv run python "$SCRIPT_DIR/pre-compact.py"
