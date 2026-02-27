# Claude Code Skills

Personal Claude Code skills, commands, and hooks.

## Structure

- `commands/` — Slash commands (`/chat`, `/learn`, `/auto-review`, etc.)
- `skills/` — Skills with `SKILL.md` per folder (`pr-comment`, `document`)
- `hooks/` — Hook scripts (`auto-review-reminder.sh`)
- `CLAUDE.md` — Global instructions

## Install

Creates directory symlinks from `~/.claude/` to this repo:

```
~/.claude/commands → repo/commands
~/.claude/hooks    → repo/hooks
~/.claude/skills   → repo/skills
~/.claude/CLAUDE.MD → repo/CLAUDE.md
```

If GSD is installed at `~/.gsd/`, it also links GSD commands/hooks into the repo dirs (gitignored).

```bash
./install.sh
```

To remove symlinks:

```bash
./install.sh --uninstall
```

## Adding new content

New files added to `commands/`, `skills/`, or `hooks/` are discovered immediately — `git pull` is all you need. No reinstall required.

## GSD

GSD lives separately in `~/.gsd/` and is wired in via local symlinks (gitignored). The GSD updater (`/gsd:update`) should be pointed at `~/.gsd/` if you need to update it.
