#!/usr/bin/env bash
# Safety net: blocks destructive operations in --dangerously-skip-permissions mode.
# Exit 0 = allow, exit 2 = block (requires user to re-run without skip-permissions).
#
# Reads $CLAUDE_TOOL_NAME and $CLAUDE_TOOL_INPUT from the environment.

TOOL="$CLAUDE_TOOL_NAME"
INPUT="$CLAUDE_TOOL_INPUT"

# Only inspect Bash commands — file tools (Edit/Write) are non-destructive by nature
if [[ "$TOOL" != "Bash" ]]; then
  exit 0
fi

# Extract the command string from the JSON input
CMD=$(echo "$INPUT" | jq -r '.command // empty' 2>/dev/null)
if [[ -z "$CMD" ]]; then
  # Fallback: treat the whole input as the command
  CMD="$INPUT"
fi

# --------------------------------------------------------------------------
# Pattern list: every destructive shell pattern we can think of.
# Grouped by category for readability. Uses extended regex (grep -Ei).
# --------------------------------------------------------------------------

PATTERNS=(
  # --- Filesystem deletion ---
  '\brm\b'
  '\brmdir\b'
  '\bunlink\b'
  '\bshred\b'
  '\bwipe\b'
  '\bsrm\b'
  '>\s*/dev/null.*>' # redirecting to overwrite via > (not >>)

  # --- Git destructive ---
  'git\s+clean'
  'git\s+reset\s+--hard'
  'git\s+checkout\s+--\s'
  'git\s+restore\s+--staged'
  'git\s+restore\s+--worktree'
  'git\s+branch\s+-[dD]'
  'git\s+push.*--force'
  'git\s+push.*-f\b'
  'git\s+stash\s+drop'
  'git\s+stash\s+clear'
  'git\s+tag\s+-d'
  'git\s+reflog\s+expire'
  'git\s+gc\s+--prune'
  'git\s+filter-branch'
  'git\s+rebase'

  # --- SQL destructive ---
  '\bDROP\s+(TABLE|DATABASE|SCHEMA|INDEX|VIEW|COLUMN|CONSTRAINT|TRIGGER|FUNCTION|PROCEDURE|SEQUENCE|TYPE|ROLE|USER)\b'
  '\bTRUNCATE\b'
  '\bDELETE\s+FROM\b'
  '\bALTER\s+TABLE\s+.*\bDROP\b'

  # --- Docker/container destructive ---
  'docker\s+rm\b'
  'docker\s+rmi\b'
  'docker\s+system\s+prune'
  'docker\s+volume\s+rm'
  'docker\s+volume\s+prune'
  'docker\s+container\s+prune'
  'docker\s+image\s+prune'
  'docker\s+network\s+rm'
  'docker\s+network\s+prune'
  'docker\s+compose\s+down\s+-v'
  'podman\s+rm\b'
  'podman\s+rmi\b'

  # --- Kubernetes destructive ---
  'kubectl\s+delete'
  'kubectl\s+drain'
  'kubectl\s+cordon'
  'helm\s+uninstall'
  'helm\s+delete'

  # --- Package manager destructive ---
  'npm\s+unpublish'
  'pip\s+uninstall'
  'cargo\s+uninstall'
  'pacman\s+-R'
  'apt\s+remove'
  'apt\s+purge'
  'apt-get\s+remove'
  'apt-get\s+purge'
  'yay\s+-R'
  'paru\s+-R'

  # --- Process/system destructive ---
  'kill\s+-9'
  'killall\b'
  'pkill\b'
  'systemctl\s+(stop|disable|mask)'
  'chmod\s+000'
  'chown\s+-R'
  'mkfs\b'
  'dd\s+if='
  'fdisk\b'
  'parted\b'

  # --- Cloud destructive ---
  'aws\s+s3\s+rm'
  'aws\s+s3\s+rb'
  'aws\s+.*delete'
  'gcloud\s+.*delete'
  'az\s+.*delete'
  'terraform\s+destroy'
  'pulumi\s+destroy'

  # --- Database tools ---
  'redis-cli\s+FLUSHALL'
  'redis-cli\s+FLUSHDB'
  'mongo.*--eval.*drop'
  'psql.*DROP'
  'mysql.*DROP'

  # --- Misc dangerous ---
  'curl.*\|\s*sh'
  'curl.*\|\s*bash'
  'wget.*\|\s*sh'
  'wget.*\|\s*bash'
  ':>\s'          # truncate file via :> file
  'mv\s+.*\s+/dev/null'
)

# Build a single regex from all patterns
COMBINED=$(IFS='|'; echo "${PATTERNS[*]}")

if echo "$CMD" | grep -qEi "$COMBINED"; then
  MATCHED=$(echo "$CMD" | grep -oEi "$COMBINED" | head -1)
  echo "" > /dev/tty
  echo "⚠  DESTRUCTIVE OPERATION DETECTED: '$MATCHED'" > /dev/tty
  echo "   Command: $CMD" > /dev/tty
  echo "" > /dev/tty
  read -p "   Allow this command? [y/N] " -t 30 REPLY < /dev/tty
  if [[ "$REPLY" =~ ^[Yy]$ ]]; then
    exit 0
  else
    echo "Blocked by safety hook." >&2
    exit 2
  fi
fi

exit 0
