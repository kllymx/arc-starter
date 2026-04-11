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

# Step 2: Install project dependencies
echo "Installing dependencies..."
uv sync --quiet 2>&1
echo "Automated knowledge capture is ready."
