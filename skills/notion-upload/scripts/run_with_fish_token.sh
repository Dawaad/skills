#!/usr/bin/env bash
# Reads NOTION_API_TOKEN from fish's universal variables (if not already in env)
# and execs the notion_upload script. Token never appears on the invoking
# command line.
set -euo pipefail

if [ -z "${NOTION_API_TOKEN:-}" ]; then
  fish_vars="$HOME/.config/fish/fish_variables"
  if [ -f "$fish_vars" ]; then
    token="$(grep -E '^SETUVAR --export NOTION_API_TOKEN:' "$fish_vars" | sed 's/.*NOTION_API_TOKEN://')"
    if [ -n "$token" ]; then
      export NOTION_API_TOKEN="$token"
    fi
  fi
fi

if [ -z "${NOTION_API_TOKEN:-}" ]; then
  echo "NOTION_API_TOKEN not set and not readable from fish universal vars" >&2
  exit 2
fi

exec uv run --script "$HOME/.claude/skills/notion-upload/scripts/notion_upload.py" "$@"
