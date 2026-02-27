Review the current implementation before finalizing. Work in batches, reporting findings and waiting for approval before making any changes.

## Scope

Determine what to review:
- If `$ARGUMENTS` specifies files or directories, review only those.
- If no arguments given, use `git diff --name-only` (staged + unstaged) to find recently changed files.
- If there are no git changes, ask the user what to review.

## Process

Work through the review in batches by category. For each batch:

### 1. Analyze

Examine the code for issues in this order (one batch per category):

**Batch 1 — Simpler approaches:** Could any part of the implementation be replaced with a simpler, clearer approach? Are there overly clever solutions where a straightforward one would do?

**Batch 2 — Redundant code:** Is there any code that does nothing useful, or conditions that can never be reached? Are there unnecessary abstractions, wrappers, or indirection?

**Batch 3 — Duplicate logic:** Was any logic introduced that duplicates something already in the codebase? Are there repeated patterns within the changed files themselves that should be consolidated?

**Batch 4 — Dead/unused code:** Were any functions, variables, imports, or exports left behind that are no longer referenced? Did refactoring leave orphaned code paths?

### 2. Report

For each batch, present findings as a numbered list. For each issue:
- **File and location** (file:line_number)
- **What the issue is** (1-2 sentences)
- **Proposed fix** (concrete description of the change)

If a batch has no issues, state that clearly and move to the next batch.

### 3. Wait for approval

After presenting each batch, ask the user to approve, reject, or modify the proposed fixes before proceeding. Use `AskUserQuestion` with options:
- "Apply all fixes in this batch"
- "Skip this batch"

Only apply approved fixes, then move to the next batch.

## Completion

After all batches are processed, provide a brief summary of what was reviewed and what was changed.
