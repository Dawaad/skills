---
name: pr-comment
description: >
  Four-phase workflow for handling inline review comments on GitHub pull requests.
  State persists in .pr-review/ so work survives context resets between phases.
  Trigger on: "pr comment", "review comments", "handle PR feedback", "triage PR",
  "fix PR comments", or any reference to addressing pull request review feedback.
---

# PR Comment Handler

Four-phase workflow for resolving inline PR review comments. Each phase is a separate command so you can reset context between them.

## Workflow

Run these commands in order:

1. **`/pr-comment:triage`** — Discover unresolved review comments, classify severity, get user confirmation on what to address.
2. **`/pr-comment:plan`** — Create resolution plans with architectural impact analysis for each approved comment.
3. **`/pr-comment:fix`** — Implement the planned code changes and verify correctness.
4. **`/pr-comment:resolve`** — Reply to each addressed comment and resolve the threads on GitHub.

State persists in `.pr-review/` at repo root, so you can reset context between phases.

## When this skill triggers

Tell the user about the four-phase workflow and instruct them to start with `/pr-comment:triage`.
