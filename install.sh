#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

# All symlink mappings: target (in ~/.claude/) -> source (in repo)
declare -A FILE_LINKS=(
  ["$CLAUDE_DIR/commands/chat.md"]="$REPO_DIR/commands/chat.md"
  ["$CLAUDE_DIR/commands/learn.md"]="$REPO_DIR/commands/learn.md"
  ["$CLAUDE_DIR/commands/auto-review.md"]="$REPO_DIR/commands/auto-review.md"
  ["$CLAUDE_DIR/commands/handle-pr-comments.md"]="$REPO_DIR/commands/handle-pr-comments.md"
  ["$CLAUDE_DIR/commands/techdebt-duplicate.md"]="$REPO_DIR/commands/techdebt-duplicate.md"
  ["$CLAUDE_DIR/commands/techdebt-standards.md"]="$REPO_DIR/commands/techdebt-standards.md"
  ["$CLAUDE_DIR/hooks/auto-review-reminder.sh"]="$REPO_DIR/hooks/auto-review-reminder.sh"
  ["$CLAUDE_DIR/CLAUDE.MD"]="$REPO_DIR/CLAUDE.md"
)

declare -A DIR_LINKS=(
  ["$CLAUDE_DIR/commands/pr-comment"]="$REPO_DIR/commands/pr-comment"
  ["$CLAUDE_DIR/skills"]="$REPO_DIR/skills"
)

uninstall() {
  echo "Removing symlinks..."
  for target in "${!FILE_LINKS[@]}"; do
    if [ -L "$target" ]; then
      rm "$target"
      echo "  Removed $target"
    fi
  done
  for target in "${!DIR_LINKS[@]}"; do
    if [ -L "$target" ]; then
      rm "$target"
      echo "  Removed $target"
    fi
  done
  echo "Done. Original files are not restored — re-copy from repo if needed."
}

install() {
  echo "Installing symlinks..."

  # Validate all sources exist
  for source in "${FILE_LINKS[@]}"; do
    if [ ! -f "$source" ]; then
      echo "ERROR: Source file missing: $source" >&2
      exit 1
    fi
  done
  for source in "${DIR_LINKS[@]}"; do
    if [ ! -d "$source" ]; then
      echo "ERROR: Source directory missing: $source" >&2
      exit 1
    fi
  done

  # Ensure parent directories exist
  mkdir -p "$CLAUDE_DIR/commands" "$CLAUDE_DIR/hooks"

  # Create file symlinks
  for target in "${!FILE_LINKS[@]}"; do
    source="${FILE_LINKS[$target]}"
    if [ -L "$target" ]; then
      rm "$target"
    elif [ -f "$target" ]; then
      echo "  WARNING: Removing existing file $target"
      rm "$target"
    fi
    ln -s "$source" "$target"
    echo "  $target -> $source"
  done

  # Create directory symlinks
  for target in "${!DIR_LINKS[@]}"; do
    source="${DIR_LINKS[$target]}"
    if [ -L "$target" ]; then
      rm "$target"
    elif [ -d "$target" ]; then
      echo "  ERROR: $target is an existing directory (not a symlink). Remove it manually first." >&2
      exit 1
    fi
    ln -s "$source" "$target"
    echo "  $target -> $source"
  done

  echo "Done."
}

case "${1:-}" in
  --uninstall)
    uninstall
    ;;
  *)
    install
    ;;
esac
