# State Schema

All state persists in `.pr-review/` at repo root. Add `.pr-review/` to `.gitignore` if not already present.

## meta.json

Created during triage, read by all phases.

```json
{
  "pr_number": 142,
  "repo": "owner/repo",
  "branch": "feature/foo",
  "last_updated": "2025-01-15T10:30:00Z"
}
```

## triage.json

Phase 1 output. Array of triaged review comments.

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

### Severity definitions

- **critical**: Correctness bug, security vulnerability, data loss risk
- **important**: Logic error, missing edge case, API misuse, test gap
- **moderate**: Readability, naming, style violations, minor refactor
- **nitpick**: Subjective preference, cosmetic, optional improvement

### Status values

- `pending` — awaiting user decision
- `approved` — user confirmed to address
- `skipped` — user decided not to address
- `planned` — plan created (phase 2)
- `fixed` — implemented and comment resolved (phase 3)

## plans.json

Phase 2 output. Resolution plan for each approved comment.

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
