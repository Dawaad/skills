---
name: pr-comment:triage
description: >
  Phase 1 of PR comment handler. Discovers unresolved inline review comments,
  classifies severity, and gets user confirmation on what to address.
  Writes state to .pr-review/ for subsequent phases.
---

# PR Comment Triage (Phase 1 of 4)

Discover all unresolved inline review comments, classify severity, and get user confirmation on what to address.

After this phase, reset context and run `/pr-comment:plan`.

## State Schema

All state persists in `.pr-review/` at repo root.

### meta.json

```json
{
  "pr_number": 142,
  "repo": "owner/repo",
  "branch": "feature/foo",
  "last_updated": "2025-01-15T10:30:00Z",
  "phases": {
    "triage": { "completed_at": "2025-01-15T10:30:00Z" },
    "plan": { "completed_at": null },
    "fix": { "completed_at": null },
    "resolve": { "completed_at": null }
  }
}
```

### triage.json

Array of triaged review comments:

```json
[
  {
    "id": "thread-id-from-github",
    "status": "pending",
    "severity": "critical | important | moderate | nitpick",
    "summary": "Brief description of the issue raised",
    "reviewer": "github-username",
    "file": "src/auth/login.ts",
    "line_start": 42,
    "line_end": 45,
    "original_comment": "Full text of the review comment",
    "assessment": "Why this severity was assigned",
    "should_address": true,
    "user_decision": null
  }
]
```

**Status values:** `pending` → `approved` / `skipped` → `planned` → `fixed`

## Setup

1. Run `git branch --show-current` and `git remote get-url origin` to identify branch and repo.
   - If in a worktree, check for `.git` file in the topmost folder to find the repo root.
2. Load existing state from `.pr-review/meta.json` if it exists. If triage.json already exists with decisions, this is a re-triage — preserve existing `approved`/`skipped` decisions and only add new threads as `pending`.
3. Ensure `.pr-review/` is in `.gitignore`. Create the directory and gitignore entry if missing.

## Steps

1. Use GitHub MCP `list_pull_requests` to find the open PR for the current branch. If none found, stop. If multiple, ask the user.
2. Use GitHub MCP `pull_request_read` with method `get_review_comments` to retrieve all review comment threads. Page through all results.
3. Filter to **unresolved threads only** (where `isResolved` is false). Skip resolved and outdated threads.
4. For each unresolved thread:
   - Read the referenced file and line range for full context.
   - Classify severity:
     - **Critical** — correctness bug, security vulnerability, data loss risk
     - **Important** — logic error, missing edge case, API misuse, test gap
     - **Moderate** — readability, naming, style violation, minor refactor
     - **Nitpick** — subjective preference, cosmetic, optional improvement
   - Write a brief assessment of why this severity was assigned.
   - Determine if it should be addressed (`should_address: true/false`).
5. Write `meta.json` and `triage.json` to `.pr-review/`.
6. Present all comments to the user grouped by severity (critical first), showing:
   - Reviewer, file, line range
   - Summary of the comment
   - Assigned severity and reasoning
   - Recommendation: address or skip
7. For any comment where the right action is unclear, ask the user directly.
8. **Wait for user confirmation.** Do not proceed until the user approves which comments to address.
9. Update `triage.json` with user decisions (`user_decision` field, status to `approved` or `skipped`).
10. Mark phase complete: update `meta.json` setting `phases.triage.completed_at` to the current ISO 8601 timestamp. Create the `phases` object if it doesn't exist.
11. Tell the user: "Triage complete. Reset context and run `/pr-comment:plan` to create resolution plans."

## Edge Cases

- **New comments added after triage**: Re-running triage merges new comments. Existing decisions are preserved — only new threads are added as `pending`.
- **Comment references deleted code**: Flag to user, mark as needing manual review.
- **Multiple reviewers on same line**: Group related comments from the same thread together.
