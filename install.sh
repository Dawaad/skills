#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
GSD_DIR="$HOME/.gsd"

# Directory symlinks: ~/.claude/{commands,hooks,skills,CLAUDE.MD} -> repo
LINKS=(
  "$CLAUDE_DIR/commands:$REPO_DIR/commands"
  "$CLAUDE_DIR/hooks:$REPO_DIR/hooks"
  "$CLAUDE_DIR/skills:$REPO_DIR/skills"
  "$CLAUDE_DIR/CLAUDE.MD:$REPO_DIR/CLAUDE.md"
)

# GSD symlinks inside repo (local, gitignored)
GSD_LINKS=(
  "$REPO_DIR/commands/gsd:$GSD_DIR/commands"
  "$REPO_DIR/hooks/gsd-check-update.js:$GSD_DIR/hooks/gsd-check-update.js"
  "$REPO_DIR/hooks/gsd-statusline.js:$GSD_DIR/hooks/gsd-statusline.js"
)

link() {
  local target="$1" source="$2"
  if [ -L "$target" ]; then
    rm "$target"
  elif [ -e "$target" ]; then
    echo "  SKIP: $target exists and is not a symlink. Remove it manually." >&2
    return 1
  fi
  ln -s "$source" "$target"
  echo "  $target -> $source"
}

uninstall() {
  echo "Removing symlinks..."
  for entry in "${LINKS[@]}" "${GSD_LINKS[@]}"; do
    target="${entry%%:*}"
    [ -L "$target" ] && rm "$target" && echo "  Removed $target"
  done
  echo "Done."
}

install() {
  echo "Installing..."

  # Main directory symlinks
  for entry in "${LINKS[@]}"; do
    target="${entry%%:*}"
    source="${entry#*:}"
    link "$target" "$source"
  done

  # GSD symlinks (only if ~/.gsd exists)
  if [ -d "$GSD_DIR" ]; then
    echo "Linking GSD from $GSD_DIR..."
    for entry in "${GSD_LINKS[@]}"; do
      target="${entry%%:*}"
      source="${entry#*:}"
      link "$target" "$source"
    done
  else
    echo "  Skipping GSD (no $GSD_DIR found)"
  fi

  echo "Done."
}

case "${1:-}" in
  --uninstall) uninstall ;;
  *)           install ;;
esac
