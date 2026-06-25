#!/bin/bash
# ARC — Install automated knowledge capture
#
# What this does:
#   1. Installs uv (fast Python package manager) if not present
#   2. Installs project dependencies (for session capture and compilation)
#
# Run once after cloning. The agent will typically run this for you.

set -e

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

# Step 1: Install uv if not present
if ! command -v uv &> /dev/null; then
  echo "Installing uv..."
  if command -v curl &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh 2>/dev/null
  elif command -v wget &> /dev/null; then
    wget -qO- https://astral.sh/uv/install.sh | sh 2>/dev/null
  else
    echo "ERROR: Neither curl nor wget found. Please install uv manually: https://docs.astral.sh/uv/"
    exit 1
  fi
  # Add to PATH for this session
  export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

  if ! command -v uv &> /dev/null; then
    echo "ERROR: uv installation failed. Please install manually: https://docs.astral.sh/uv/"
    exit 1
  fi
  echo "uv installed successfully."
fi

# Step 2: Create the local-only private tier (idempotent; gitignored).
# Done BEFORE dependency sync — it's stdlib-only (no deps needed), so the private
# tier is created even if `uv sync` later fails. Gives the founder a private layer
# from day one; makes a later personal→company upgrade a move, not a retrofit.
# Don't hard-fail bootstrap, but DO surface the failure — company mode needs it.
if python3 scripts/scaffold_private.py; then
  :
else
  echo "WARNING: could not create the private/ tier (scripts/scaffold_private.py failed)." >&2
  echo "         Company mode needs it. Run 'python3 scripts/scaffold_private.py' manually." >&2
fi

# Step 3: Install project dependencies
echo "Installing dependencies..."
uv sync --quiet 2>&1
echo "Automated knowledge capture is ready."
