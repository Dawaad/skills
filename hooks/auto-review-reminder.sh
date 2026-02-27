#!/usr/bin/env bash
# Counts recent Edit/Write tool calls in the session.
# After a threshold of file modifications, nudges the agent to offer /auto-review.

COUNTER_FILE="/tmp/claude-edit-counter-$$"

# Initialize or read counter
if [ -f "$COUNTER_FILE" ]; then
  count=$(cat "$COUNTER_FILE")
else
  count=0
fi

count=$((count + 1))
echo "$count" > "$COUNTER_FILE"

# After 10 file modifications, emit a reminder and reset
if [ "$count" -ge 10 ]; then
  echo "You've made $count file modifications this session. Consider asking the user if they'd like to run /auto-review."
  echo "0" > "$COUNTER_FILE"
fi
