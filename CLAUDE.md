## Communication Style

Be authentic and direct. Do not be sycophantic — skip the praise and get to the point.
Be self-confident in your recommendations. If you know the better approach, say so clearly.
Push back when my ideas seem infeasible, misguided, or suboptimal. Explain why and suggest alternatives.
Politely correct me when I use incorrect terminology or concepts, especially when the distinction matters for technical accuracy or practical outcomes.
Point out obvious mismatches, inconsistencies, or things that seem off. Use common sense.

## Problem Solving

- Ask clarifying questions before generating solutions when the prompt lacks sufficient context or is open-ended. Do not produce output until you have enough information to give a good answer.
- If a feature or design could be achieved in a simpler or more effective way, say so rather than implementing my exact (possibly worse) approach.
- When multiple valid approaches exist, briefly explain the tradeoffs rather than just picking one silently.
- Point out potential issues with error handling, edge cases, and performance
- Identify conflicts with existing patterns in the codebase
- Flag any security concerns or data validation gaps

## Git Commit Convention

- **Format**: `<type>(<scope>): <subject>`
- **Types**: feat, fix, docs, style, refactor, test, chore, perf
- **Subject Rules**:
  - Max 50 characters
  - Imperative mood ("add" not "added")
  - No period at the end
- **Commit Structure**:
  - Simple changes: One-line commit only
  - Complex changes: Add body (72-char lines) explaining what/why
  - Reference issues in footer
- **Best Practices**:
  - Keep commits atomic (one logical change)
  - Make them self-explanatory
  - Split different concerns into separate commits

## Code Style

Variable and function names should generally be complete words, and as concise as possible while maintaining specificity in the given context. They should be understandable by someone unfamiliar with the codebase.

Only add code comments in the following scenarios:

The purpose of a block of code is not obvious (possibly because it is long or the logic is convoluted).

We are deviating from the standard or obvious way to accomplish something.

If there are any caveats, gotchas, or foot-guns to be aware of, and only if they can't be eliminated. First try to eliminate the foot-gun or make it obvious either with code structure or the type system. For example, if we have a set of boolean flags and some combinations are invalid, consider replacing them with an enum.

Specifically, never add a comment that is a restatement of a function or variable name. ‘’’

## Auto Review

After completing a significant chunk of implementation work (new features, refactors, or bug fixes touching 3+ files), ask me whether I'd like to run `/auto-review` before moving on. Do not run it automatically — just offer it.

## Unit Testing

Test must be accurate, reflect real usage and be designed to reveal flaws. No useless tests! Design tests to be verbose so we can use them for debuging.
When developing new services, ensure that unit tests cover all potential use cases, including niche edge cases that may result in unexpected results
When developing new test suites for classes or services. Read 3-5 existing testing setups to understand and mimic the existing structure
