#!/bin/bash
# ARC Session End Wrapper
#
# Checks if uv and Python deps are available before running session-end.py.
# If not, silently skips — the workspace still functions without automated capture.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Check if uv is available
if ! command -v uv &> /dev/null; then
  exit 0
fi

# Check if deps are installed (quick check for the lock file)
if [ ! -f "$PROJECT_ROOT/uv.lock" ] && [ ! -d "$PROJECT_ROOT/.venv" ]; then
  exit 0
fi

# Forward stdin to the Python script
exec uv run python "$SCRIPT_DIR/session-end.py"
