---
name: pr-comment:plan
description: >
  Phase 2 of PR comment handler. Creates resolution plans with architectural
  impact analysis for each approved comment from triage. Reads state from
  .pr-review/ and writes plans back.
---

# PR Comment Plan (Phase 2 of 4)

Create a resolution plan for each approved comment from triage.

After this phase, reset context and run `/pr-comment:fix`.

After fix, run `/pr-comment:resolve` to reply to and resolve the comment threads.

## State Schema

### plans.json

Phase 2 output. Resolution plan for each approved comment:

```json
[
  {
    "triage_id": "thread-id-from-github",
    "severity": "critical",
    "summary": "Brief description from triage",
    "file": "src/auth/login.ts",
    "changes": [
      {
        "file": "src/auth/login.ts",
        "description": "What to change and why",
        "lines": "42-45"
      }
    ],
    "architectural_impact": "none | low | high",
    "impact_notes": "Only populated when architectural_impact is not 'none'",
    "test_strategy": "How to verify the fix",
    "status": "planned"
  }
]
```

## Setup

1. Run `git branch --show-current` and `git remote get-url origin` to identify branch and repo.
   - If in a worktree, check for `.git` file in the topmost folder to find the repo root.
2. Load `.pr-review/meta.json` and `.pr-review/triage.json`. If they don't exist, stop and tell the user to run `/pr-comment:triage` first.
3. Ensure `.pr-review/` is in `.gitignore`.

## Steps

1. Filter triage.json to comments with `status: "approved"`. If none, tell the user and stop.
2. For each approved comment, ordered by severity (critical first):
   - Read the relevant file(s) and surrounding code to understand context.
   - Determine what changes are needed and in which files.
   - Assess architectural impact:
     - **none** — localized change, no ripple effects
     - **low** — touches related code but no structural changes
     - **high** — changes interfaces, data flow, or patterns used elsewhere
   - Define a test strategy (how to verify the fix is correct).
3. Write all plans to `.pr-review/plans.json`.
4. Update corresponding entries in `triage.json` to `status: "planned"`.
5. Present plans to the user, grouped by severity. For any plan with `architectural_impact: "high"`, explicitly discuss the proposed changes and get user approval before proceeding.
6. **Wait for user confirmation** on all plans.
7. Mark phase complete: update `meta.json` setting `phases.plan.completed_at` to the current ISO 8601 timestamp. Create the `phases` object if it doesn't exist.
8. Tell the user: "Plans complete. Reset context and run `/pr-comment:fix` to implement the fixes."

## Edge Cases

- **Comment references deleted code**: Flag to user, mark as needing manual review rather than creating a plan.
- **Overlapping changes**: If multiple comments affect the same file/region, note the overlap in the plan so fixes can be applied in the right order.
