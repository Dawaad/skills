---
name: pr-comment:resolve
description: >
  Phase 4 of PR comment handler. Replies to each fixed PR review comment with
  a summary of what changed, then resolves the thread. Reads state from .pr-review/
  to know which comments were fixed.
---

# PR Comment Resolve (Phase 4 of 4)

Reply to each fixed review comment thread and resolve it on GitHub.

## Setup

1. Run `git branch --show-current` and `git remote get-url origin` to identify branch and repo.
   - If in a worktree, check for `.git` file in the topmost folder to find the repo root.
2. Load `.pr-review/meta.json`, `.pr-review/triage.json`, and `.pr-review/plans.json`. If any don't exist, stop and tell the user which prior phase to run.
3. Ensure `.pr-review/` is in `.gitignore`.

## Steps

1. Filter triage.json to entries with `status: "fixed"` that have NOT yet been resolved (no `resolved: true` field). If none, tell the user and stop.
2. For each fixed comment, ordered by severity (critical first):
   a. Look up the corresponding plan in plans.json to understand what was changed.
   b. Read the changed file(s) to compose an accurate reply.
   c. Reply to the review comment thread via GitHub MCP with a brief description of what was changed (e.g., "Fixed: refactored the null check to handle the edge case at line 45. See latest push.").
   d. Resolve the comment thread via GitHub MCP.
   e. Mark the entry in triage.json with `"resolved": true`.
   f. **Write state after each resolution** so progress is preserved if context resets.
3. After all comments are addressed, present a summary:
   - Number of comments replied to and resolved
   - Any comments that could not be resolved (with reasons)
4. If all fixed entries are now resolved, mark phase complete: update `meta.json` setting `phases.resolve.completed_at` to the current ISO 8601 timestamp. Create the `phases` object if it doesn't exist.

## Replying and Resolving via GitHub MCP

1. **Reply**: Use `pull_request_review_write` with method `create` and event `COMMENT`, including the body text as the reply.
2. **Resolve**: The GitHub MCP does not have a direct "resolve thread" tool. After replying, inform the user which threads were addressed so they can resolve them on GitHub, or attempt using the GraphQL API via `gh api graphql` if available.

## Edge Cases

- **Context reset mid-resolve**: State is written after each resolution. On restart, read state and continue from the next unresolved `fixed` entry.
- **Comment was already resolved externally**: If the thread is already resolved on GitHub, mark it as `resolved: true` in triage.json and skip.
