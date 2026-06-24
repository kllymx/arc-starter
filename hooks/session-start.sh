#!/bin/bash
# ARC Session Start Hook (bash fallback)
#
# Injects lean session context: overview + memory + index navigation +
# recent daily heads. Pure bash — no Python dependency beyond JSON escape.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Lane-local caps (aligned with scripts/context_select.py)
OVERVIEW_MAX=2000
MEMORY_MAX=2000
INDEX_NAV_MAX=2500
DAILY_LOOKBACK=2
DAILY_EXCERPT_MAX=800
DAILY_ACTIVITY_MAX=1500
INJECT_BUDGET=7000
TRUNCATION_MARKER=$'\n\n[...truncated]'

parts=""

truncate_text() {
  local content="$1"
  local max_chars="$2"
  if [ "${#content}" -le "$max_chars" ]; then
    printf '%s' "$content"
    return
  fi
  printf '%s' "${content:0:$max_chars}"
  printf '\n[...truncated]'
}

is_placeholder_context() {
  local content="$1"
  local kind="$2"

  if [ -z "$(printf '%s' "$content" | tr -d '[:space:]')" ]; then
    return 0
  fi

  if [ "$kind" = "overview" ]; then
    if printf '%s' "$content" | grep -Fqi "Fast one-page summary of the business" \
      && printf '%s' "$content" | grep -Fqi "This file is created during /setup"; then
      return 0
    fi
  fi

  if [ "$kind" = "memory" ]; then
    if printf '%s' "$content" | grep -Fqi "Lightweight preferences, corrections, and facts learned during conversations." \
      && printf '%s' "$content" | grep -Fqi "This file stores two types of information:"; then
      return 0
    fi
  fi

  return 1
}

index_navigation() {
  local index_file="$1"
  local nav=""
  local in_footer=0

  if [ ! -f "$index_file" ]; then
    return
  fi

  if grep -q "No articles yet" "$index_file"; then
    return
  fi

  while IFS= read -r line || [ -n "$line" ]; do
    if printf '%s' "$line" | grep -q '^> \*\*Last updated'; then
      in_footer=1
    fi
    if [ "$in_footer" -eq 1 ]; then
      continue
    fi
    if printf '%s' "$line" | grep -q '^# Wiki Index'; then
      continue
    fi
    if printf '%s' "$line" | grep -q '^>'; then
      continue
    fi
    if printf '%s' "$line" | grep -q '^---'; then
      continue
    fi
    if printf '%s' "$line" | grep -q '^## How to Read'; then
      continue
    fi
    if printf '%s' "$line" | grep -qi '_No articles yet'; then
      continue
    fi
    if printf '%s' "$line" | grep -q '^## \|^\[\[' || printf '%s' "$line" | grep -q '\[\['; then
      nav="${nav}${line}"$'\n'
    fi
  done < "$index_file"

  nav="$(truncate_text "$(printf '%s' "$nav" | sed '/^$/d')" "$INDEX_NAV_MAX")"
  if [ -n "$nav" ]; then
    if [ -f "$PROJECT_ROOT/scripts/wiki_query.py" ]; then
      nav="${nav}"$'\n\n'"Use \`uv run python scripts/wiki_query.py\` to search the wiki and retrieve relevant article excerpts on demand."
    else
      nav="${nav}"$'\n\n'"Read full wiki articles from \`wiki/\` on demand when a topic needs depth — this injection is navigation only."
    fi
    printf '%s' "$nav"
  fi
}

daily_head_excerpt() {
  local file="$1"
  local excerpt=""
  local line
  local started=0

  while IFS= read -r line || [ -n "$line" ]; do
    if [ "$started" -eq 1 ] && printf '%s' "$line" | grep -q '^## '; then
      break
    fi
    if [ -n "$line" ]; then
      started=1
    fi
    excerpt="${excerpt}${line}"$'\n'
    if [ "${#excerpt}" -ge "$DAILY_EXCERPT_MAX" ]; then
      break
    fi
  done < "$file"

  truncate_text "$(printf '%s' "$excerpt" | sed '/^$/d')" "$DAILY_EXCERPT_MAX"
}

recent_activity() {
  local daily_dir="$1"
  local activity=""
  local total=0
  local count=0

  if [ ! -d "$daily_dir" ]; then
    return
  fi

  while IFS= read -r file; do
    [ -n "$file" ] || continue
    count=$((count + 1))
    if [ "$count" -gt "$DAILY_LOOKBACK" ]; then
      break
    fi
    basename="$(basename "$file" .md)"
    excerpt="$(daily_head_excerpt "$file")"
    block="--- ${basename} ---"$'\n'"${excerpt}"
    block_len="${#block}"
    if [ $((total + block_len)) -gt "$DAILY_ACTIVITY_MAX" ]; then
      break
    fi
    if [ -n "$activity" ]; then
      activity="${activity}"$'\n\n'
    fi
    activity="${activity}${block}"
    total=$((total + block_len + 2))
  done < <(ls -1r "$daily_dir"/*.md 2>/dev/null)

  printf '%s' "$activity"
}

apply_total_budget() {
  local content="$1"
  local budget="$2"
  if [ "${#content}" -le "$budget" ]; then
    printf '%s' "$content"
    return
  fi
  local marker_len=${#TRUNCATION_MARKER}
  local cut_at=$((budget - marker_len))
  if [ "$cut_at" -lt 0 ]; then
    cut_at=0
  fi
  printf '%s' "${content:0:$cut_at}"
  printf '%s' "$TRUNCATION_MARKER"
}

# 1. Overview
overview_file="$PROJECT_ROOT/context/overview.md"
if [ -f "$overview_file" ]; then
  content="$(cat "$overview_file")"
  if ! is_placeholder_context "$content" "overview"; then
    content="$(truncate_text "$content" "$OVERVIEW_MAX")"
    parts="${parts}## Business Overview\n\n${content}\n\n---\n\n"
  fi
fi

# 2. Memory
memory_file="$PROJECT_ROOT/context/memory.md"
if [ -f "$memory_file" ]; then
  content="$(cat "$memory_file")"
  if ! is_placeholder_context "$content" "memory"; then
    content="$(truncate_text "$content" "$MEMORY_MAX")"
    parts="${parts}## Memory\n\n${content}\n\n---\n\n"
  fi
fi

# 3. Wiki index navigation
index_file="$PROJECT_ROOT/wiki/index.md"
nav="$(index_navigation "$index_file")"
if [ -n "$nav" ]; then
  parts="${parts}## Wiki Index\n\n${nav}\n\n---\n\n"
fi

# 4. Recent daily heads
daily_dir="$PROJECT_ROOT/daily"
activity="$(recent_activity "$daily_dir")"
if [ -n "$activity" ]; then
  parts="${parts}## Recent Session Logs\n\n${activity}"
fi

# Output as JSON if we have anything to inject
if [ -n "$parts" ]; then
  parts="$(apply_total_budget "$parts" "$INJECT_BUDGET")"
  escaped=$(printf '%s' "$parts" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))' 2>/dev/null || printf '%s' "$parts" | sed 's/\\/\\\\/g; s/"/\\"/g; s/\t/\\t/g' | tr '\n' ' ')
  echo "{\"hookSpecificOutput\": {\"hookEventName\": \"SessionStart\", \"additionalContext\": ${escaped}}}"
fi