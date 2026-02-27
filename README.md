# Claude Code Skills

Personal Claude Code skills, commands, and hooks.

## Structure

- `commands/` — Slash commands (`/chat`, `/learn`, `/auto-review`, `/gsd:*`, etc.)
- `skills/` — Skills with `SKILL.md` per folder (`pr-comment`, `document`)
- `hooks/` — Hook scripts (`auto-review-reminder.sh`, GSD hooks)
- `CLAUDE.md` — Global instructions

## Install

Create directory symlinks from `~/.claude/` to this repo:

```bash
ln -s ~/dev/util/skills/commands ~/.claude/commands
ln -s ~/dev/util/skills/hooks    ~/.claude/hooks
ln -s ~/dev/util/skills/skills   ~/.claude/skills
ln -s ~/dev/util/skills/CLAUDE.md ~/.claude/CLAUDE.MD
```

Remove any existing directories/files at those paths first.

## Adding new content

Push files to `commands/`, `skills/`, or `hooks/`. `git pull` is all that's needed — no reinstall.

## GSD

GSD commands and hooks live directly in this repo. The GSD updater (`/gsd:update`) writes to `~/.claude/commands/gsd/` which resolves into the repo via the directory symlink, so updates overwrite in place.
