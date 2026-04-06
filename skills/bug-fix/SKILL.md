---
name: bug-fix
version: 1.0.0
description: |
  Disciplined bug-fix workflow: interview the user to understand the bug, write a
  failing test that proves it exists, then spawn a sub-agent to fix the source code
  while the test acts as the contract. Use when the user reports a bug, says "bug",
  "broken", "doesn't work", "regression", "fix this", "something's wrong with",
  "getting an error", "unexpected behavior", or invokes /bug-fix. Also trigger when
  the user describes symptoms like crashes, wrong output, 500 errors, or data loss —
  even if they don't use the word "bug". Do NOT trigger for feature requests, refactors,
  or performance improvements unless they stem from incorrect behavior.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
  - AskUserQuestion
---

# Bug Fix

You follow a strict reproduce-first, test-first workflow for fixing bugs. The goal is to never touch source code until you have a failing test that proves the bug exists — then the fix is just "make the test pass."

This matters because jumping straight to a fix without a reproduction test leads to incomplete fixes, regressions, and bugs that silently return. The test is the proof the bug existed and the guarantee it won't come back.

## Phase 1: Reproduce — Interview the User

Ask targeted questions **one at a time** using AskUserQuestion. Do not batch questions. Wait for each answer before asking the next.

1. **What's the bug?** — Symptoms, error messages, stack traces. Ask them to paste the exact error if they have one.
2. **Steps to reproduce** — What exact sequence of actions triggers it? Be specific: which page, which button, which input.
3. **Expected vs actual** — What should happen? What happens instead?
4. **When did it start?** — Recent change? Always been there? Did it work before a specific commit/deploy?
5. **Environment** — OS, browser, Node/Python version, config, feature flags — whatever is relevant to this project.
6. **Consistency** — Does it happen every time? Only with specific inputs? Intermittent?

**Adapt as you go.** Skip questions the user already answered. If the bug is obvious from their first message (e.g., they paste a stack trace with a clear cause), don't ask all six — get enough to write a test and move on. Follow up on anything vague.

### Investigate

Once you understand the bug, explore the codebase to locate the relevant code paths:

- Use Grep/Glob to find the files involved (error messages, function names, routes, components)
- Read the relevant source files to understand the current behavior
- Check git log for recent changes to those files if the user said "it used to work"
- Identify the specific function(s) or code path(s) where the bug lives

Present a brief summary to the user: "Here's what I think is happening: [explanation]. The relevant code is in [files]. Does that match what you're seeing?"

Wait for confirmation before proceeding to Phase 2.

## Phase 2: Test — Write a Failing Test

### Detect the test framework

Look for existing test infrastructure in the project:

- `package.json` → Jest, Vitest, Mocha, Playwright, etc.
- `pytest.ini` / `pyproject.toml` / `setup.cfg` → pytest
- `go.mod` → Go's built-in testing
- `Cargo.toml` → Rust's built-in testing
- Existing test files → follow their patterns (imports, structure, naming)

If the project has no tests at all, set up the minimal test infrastructure needed (ask the user which framework they prefer if it's ambiguous).

### Write the test

- Place the test next to existing tests for the same module, following the project's naming conventions
- The test should reproduce the exact bug described — not a broad test of the feature, but a precise assertion that fails because of this specific bug
- Name the test descriptively: `test_csv_export_preserves_unicode_characters`, not `test_bug_fix`
- Include a comment at the top of the test explaining what bug it reproduces

### Run it and confirm it fails

Run the test and verify it **fails** with output that matches the bug description. This is the proof the bug exists.

If the test passes (meaning you didn't reproduce the bug correctly), revisit your understanding — go back to the user if needed.

Show the user the test code and the failing output:

"Here's the test I wrote — it reproduces the bug. [test code]. When I run it, it fails with: [output]. Does this match the bug you're seeing? If so, I'll proceed to fix it."

Wait for the user to confirm before proceeding to Phase 3.

## Phase 3: Fix — Sub-Agent Fixes the Code

Spawn a sub-agent (using the Agent tool) with these instructions:

```
You are fixing a bug. A failing test has been written that reproduces the issue.

**Test file:** [path to the test file]
**What the test asserts:** [plain-English description of what it checks]
**Relevant source files:** [list of files identified during investigation]
**Bug summary:** [brief description of the root cause]

Your job:
1. Read the failing test to understand exactly what's expected
2. Read the relevant source files
3. Fix the source code so the test passes
4. NEVER modify the test file — it is the contract
5. Run the specific bug test to confirm it passes
6. Run the broader test suite to check for regressions:
   - If all tests pass, you're done
   - If other tests break, fix the regression without breaking the bug fix test
7. Summarize what you changed and why
```

### After the sub-agent returns

Report the fix to the user:

- **What changed:** Which files were modified and what the fix was (keep it concise)
- **Why it works:** Brief explanation of the root cause and how the fix addresses it
- **Test status:** Confirm the bug test passes and no regressions were introduced
- **The test stays:** Remind the user the test is now part of the suite, guarding against this bug returning

## Rules

- **Never fix without a test.** The test is written before any source code changes. No exceptions.
- **The test is the contract.** The sub-agent cannot modify it. If the test is wrong, come back to the user — don't silently change it.
- **One bug per invocation.** If the user describes multiple bugs, handle them one at a time. Suggest running `/bug-fix` again for the next one.
- **Interview depth scales with complexity.** A simple "this function returns null instead of an array" needs 2 questions. A complex intermittent race condition needs all 6 and maybe more. Use judgment.
- **Respect existing patterns.** Match the project's test style, file organization, and conventions. Don't introduce a new test framework or pattern.
