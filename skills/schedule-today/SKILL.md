---
name: schedule-today
description: Read the user's canonical weekly schedule at Wiki/Personal/schedule.md and output today's focus — which work types to run in which blocks, with the relevant fixed commitments and balance context surfaced. Use whenever the user wants to know what to focus on today or for an upcoming day. Trigger on "what should I focus on today", "today's schedule", "what's my focus", "what am I doing today", "plan my day", "daily focus", "what's on for tomorrow", "what's Tuesday looking like", "my day", or any request for the day's plan that should flow from the standing schedule. Do NOT use this skill to change the schedule — for permanent changes, use schedule-manage. If the schedule file is missing, tell the user and suggest running schedule-manage to bootstrap it.
---

# schedule-today

Reads the canonical schedule, returns today's (or another named day's) focus blocks. Read-only — never edits the file.

## Inputs

- **Day**: default = today (use the date from the environment context). Accept "tomorrow", "Tuesday", or an explicit date — resolve to a day of week.
- **Schedule file**: `/home/jared/Documents/wiki/Personal/schedule.md`.

## Workflow

1. Read the schedule file.
2. If missing → tell the user it doesn't exist, suggest `schedule-manage` to bootstrap. Stop.
3. Compute the target day of week (today by default).
4. Extract that day's blocks, plus any fixed commitments that hit that day, plus relevant principles/notes.
5. Output a compact daily plan (format below).

## Output format

Keep it short. The user is glancing at this to start their day, not reading a memo.

```
# <Day>, <YYYY-MM-DD>

Focus: <one-line summary of the day's character, e.g. "deep coding day, light admin">

Blocks
- Morning: <work type> — <1-line note from schedule, if any>
- Afternoon: <work type>
- Evening: <work type or "off">

Fixed
- <commitments hitting today, if any>

Heads-up
- <only if something is worth flagging: e.g. "this is your only filming block this week", "last coding block before week-planning Friday", or pull-through from a principle that applies today>
```

Omit empty sections. If there are no fixed commitments today, drop the "Fixed" block entirely. Same for "Heads-up".

## Principles

- **Surface, don't invent.** If the schedule says "Tue afternoon = filming", you say filming. Don't decide to "swap" because today feels different — that's a job for `schedule-manage`.
- **Lean output.** Bullets, not prose. The user is mid-flow; respect that.
- **Context > restating.** Don't echo the whole schedule. Only pull what's relevant to the asked day, plus the one or two principles that affect interpretation of today's blocks.
- **Date awareness.** Always include the resolved date in the header so the user can sanity-check "you thought today was Tuesday — it's Wednesday".
- **One-shot.** Default to a single output. No follow-up interview unless the user asks for it.

## When to bounce to schedule-manage

If the user, while asking about today, also says something like "filming doesn't make sense Tuesdays anymore" or "I want to shift this permanently" — that's a schedule change, not a daily query. Output today's plan, then add a line:

> Sounds like a schedule change — want me to update the standing schedule? (uses schedule-manage)

Don't silently jump skills. Surface it.

## Edge cases

- **"What's tomorrow / Tuesday / next Monday?"** Same flow, different day. Show the resolved date so the user can confirm.
- **Schedule file exists but the target day section is empty / missing.** Output what's there (frontmatter principles, fixed commitments hitting that day), say the day's blocks aren't set, suggest `schedule-manage`.
- **Today is a fixed-commitment-only day (e.g. travel, rest).** Honor that — output the rest/travel block as the answer instead of guessing work types.
