#!/bin/bash
# ARC Setup — Installs dependencies for automated knowledge capture
#
# Run this once after cloning:
#   ./setup.sh
#
# What it does:
#   1. Installs uv (Python package manager) if not present
#   2. Installs Python 3.12+ via uv if not present
#   3. Installs project dependencies (Claude Agent SDK, OpenAI SDK)
#
# After this, the hooks will automatically capture session knowledge.
# If you skip this step, ARC still works — you just won't get
# automated knowledge capture between sessions. Use /reflect manually instead.

set -e

echo ""
echo "  ARC — Setting up automated knowledge capture"
echo "  ─────────────────────────────────────────────"
echo ""

# Step 1: Install uv if not present
if ! command -v uv &> /dev/null; then
  echo "  Installing uv (Python package manager)..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # Add to PATH for this session
  export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
  echo "  ✓ uv installed"
else
  echo "  ✓ uv already installed"
fi

# Step 2: Install dependencies
echo "  Installing dependencies..."
uv sync 2>&1 | sed 's/^/    /'
echo "  ✓ Dependencies installed"

echo ""
echo "  Done! Automated knowledge capture is now active."
echo "  Open this folder in Claude Code or Codex and say \"let's set up\""
echo ""
