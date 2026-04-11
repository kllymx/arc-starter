#!/bin/bash
# ARC Session Start Hook (bash fallback)
#
# Injects wiki index + overview + memory into the session.
# Pure bash — no Python dependency. Works even if uv/Python aren't installed.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

parts=""

# 1. Overview
overview_file="$PROJECT_ROOT/context/overview.md"
if [ -f "$overview_file" ]; then
  content=$(cat "$overview_file")
  if ! echo "$content" | grep -qi "populated\|placeholder"; then
    parts="${parts}## Business Overview\n\n${content}\n\n---\n\n"
  fi
fi

# 2. Memory
memory_file="$PROJECT_ROOT/context/memory.md"
if [ -f "$memory_file" ]; then
  content=$(cat "$memory_file")
  if ! echo "$content" | grep -qi "populated\|placeholder"; then
    parts="${parts}## Memory\n\n${content}\n\n---\n\n"
  fi
fi

# 3. Wiki index
index_file="$PROJECT_ROOT/wiki/index.md"
if [ -f "$index_file" ]; then
  content=$(cat "$index_file")
  if ! echo "$content" | grep -q "No articles yet"; then
    parts="${parts}## Wiki Index\n\n${content}\n\n---\n\n"
  fi
fi

# 4. Recent daily logs (last 3 days)
daily_dir="$PROJECT_ROOT/daily"
if [ -d "$daily_dir" ]; then
  recent=$(ls -1r "$daily_dir"/*.md 2>/dev/null | head -3)
  if [ -n "$recent" ]; then
    log_content=""
    for f in $recent; do
      basename=$(basename "$f" .md)
      log_content="${log_content}--- ${basename} ---\n$(cat "$f")\n\n"
    done
    if [ -n "$log_content" ]; then
      parts="${parts}## Recent Session Logs\n\n${log_content}"
    fi
  fi
fi

# Output as JSON if we have anything to inject
if [ -n "$parts" ]; then
  # Escape for JSON
  escaped=$(printf '%s' "$parts" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))' 2>/dev/null || printf '%s' "$parts" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g' | tr '\n' ' ')
  echo "{\"message\": ${escaped}}"
fi
