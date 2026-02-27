---
name: pr-comment:status
description: >
  Shows current progress through the PR comment workflow.
  Reads state from .pr-review/ and reports which phases are complete,
  what triage/planning decisions were made, and what work remains.
---

# PR Comment Status

Report current progress through the PR comment handling workflow.

## Setup

1. Run `git branch --show-current` and `git remote get-url origin` to identify branch and repo.
   - If in a worktree, check for `.git` file in the topmost folder to find the repo root.
2. Check if `.pr-review/` directory exists. If not, tell the user no PR review session is in progress and suggest running `/pr-comment:triage` to start.
3. Load all available state files: `meta.json`, `triage.json`, `plans.json`.

## Report

Build a status report with these sections. Only include sections for which state exists.

### 1. Session Info (from meta.json)

- PR number and repo
- Branch name
- Last updated timestamp
- Which phases have completed (from `meta.json` → `phases` object)

### 2. Phase Progress

Determine overall progress by checking the `phases` field in `meta.json`:

```
Phase 1 — Triage:   ✓ completed | ○ not started
Phase 2 — Plan:     ✓ completed | ○ not started
Phase 3 — Fix:      ✓ completed | ◐ in progress | ○ not started
Phase 4 — Resolve:  ✓ completed | ◐ in progress | ○ not started
```

A phase is "in progress" if it has started producing state but `phases.<name>` has no `completed_at`. For example, if `plans.json` exists with some entries at `status: "planned"` but `phases.plan` is not complete, plan is in progress.

Use the presence of state files and entry statuses as fallback if `phases` field is missing (for backwards compatibility with sessions started before this field existed):
- Triage complete: `triage.json` exists with no `pending` entries remaining
- Plan complete: `plans.json` exists with no `planned`-status entries that aren't yet `fixed`
- Fix complete: all plan entries have `status: "fixed"`
- Resolve complete: all fixed triage entries have `resolved: true`

### 3. Triage Summary (from triage.json)

Show counts by status and severity:

```
Comments: X total
  ✓ Approved:  N  (critical: N, important: N, moderate: N, nitpick: N)
  ✗ Skipped:   N
  ? Pending:   N  (awaiting user decision)
```

If there are pending entries, note that triage is not yet finalized.

### 4. Plan Summary (from plans.json)

Show counts by status and architectural impact:

```
Plans: X total
  Planned:  N  (high-impact: N, low-impact: N, none: N)
  Fixed:    N
```

### 5. Fix Progress (derived from triage.json + plans.json)

```
Fixes: N/M applied
  Remaining: list files still to fix
  Failed:    any plans that couldn't be applied (if any)
```

### 6. Resolution Progress (from triage.json resolved field)

```
Resolved: N/M threads
  Remaining: list of unresolved fixed comments
```

### 7. Next Action

Based on current state, tell the user what to do next:

- If no state: "Run `/pr-comment:triage` to start."
- If triage has pending entries: "Triage is incomplete. Run `/pr-comment:triage` to finish decisions."
- If triage complete but no plans: "Run `/pr-comment:plan` to create resolution plans."
- If plans exist but fixes remain: "Run `/pr-comment:fix` to implement the planned changes."
- If all fixed but not resolved: "Run `/pr-comment:resolve` to reply to and close comment threads."
- If all resolved: "All done! All review comments have been addressed and resolved."

## Output Format

Present the report cleanly using markdown. Keep it scannable — use the structured formats above, not prose paragraphs.
