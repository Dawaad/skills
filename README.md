# Claude Code Skills

Personal Claude Code skills, commands, and hooks.

## Structure

- `commands/` — Slash commands (`/chat`, `/learn`, `/auto-review`, etc.)
- `skills/` — Skills with `SKILL.md` per folder (`pr-comment`, `document`)
- `hooks/` — Hook scripts (`auto-review-reminder.sh`)
- `CLAUDE.md` — Global instructions

## Install

Symlinks content into `~/.claude/` for discovery by Claude Code:

```bash
./install.sh
```

To remove symlinks:

```bash
./install.sh --uninstall
```

## Usage

After install, skills and commands are available in any Claude Code session. Updates via `git pull` take effect immediately — no reinstall needed.
