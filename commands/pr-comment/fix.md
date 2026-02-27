---
name: pr-comment:fix
description: >
  Phase 3 of PR comment handler. Implements planned fixes and verifies correctness.
  Does NOT reply to or resolve comments — run /pr-comment:resolve for that.
  Reads plans from .pr-review/ and updates state after each fix.
---

# PR Comment Fix (Phase 3 of 4)

Implement each planned fix and verify correctness. This phase only changes code — it does not interact with GitHub comments.

After this phase, reset context and run `/pr-comment:resolve`.

## Setup

1. Run `git branch --show-current` and `git remote get-url origin` to identify branch and repo.
   - If in a worktree, check for `.git` file in the topmost folder to find the repo root.
2. Load `.pr-review/meta.json`, `.pr-review/triage.json`, and `.pr-review/plans.json`. If any don't exist, stop and tell the user which prior phase to run.
3. Ensure `.pr-review/` is in `.gitignore`.

## Steps

1. Filter plans.json to entries with `status: "planned"`. If none, tell the user and stop.
2. For each plan, ordered by severity (critical first):
   a. Read the target file(s).
   b. Implement the changes described in the plan.
   c. Verify correctness:
      - If tests exist for the affected code, run them.
      - If the plan specifies a test strategy, follow it.
      - Read the changed code to confirm it addresses the review comment.
   d. Update `triage.json` status to `fixed` and `plans.json` status to `fixed`.
   e. **Write state after each fix** so progress is preserved if context resets.
3. After all fixes, present a summary:
   - Number of fixes applied
   - Files changed
   - Any plans that could not be fixed (with reasons — keep status as `planned`)
4. If all plans are now `fixed`, mark phase complete: update `meta.json` setting `phases.fix.completed_at` to the current ISO 8601 timestamp. Create the `phases` object if it doesn't exist.
5. Tell the user: "Fixes complete. Reset context and run `/pr-comment:resolve` to reply to and resolve the PR comments."

## Edge Cases

- **Context reset mid-fix**: State is written after each fix. On restart, read state and continue from the next `planned` entry.
- **Fix causes test failure**: Stop, report the failure to the user, and do not mark as fixed. Keep status as `planned` so it can be retried.
- **Overlapping file changes**: Apply fixes to the same file sequentially, re-reading the file before each change to pick up prior edits.
