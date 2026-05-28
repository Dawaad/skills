---
name: schedule-manage
description: Create and edit the user's canonical weekly work schedule at Wiki/Personal/schedule.md. The schedule allocates abstract work types (content research, filming, week planning, coding, deep work, admin, etc.) across days of the week to balance startup responsibilities. Use whenever the user wants to build, change, rebalance, or rebuild their work schedule. Trigger on "update my schedule", "change my schedule", "rebuild my schedule", "shift filming to Tuesday", "I want Mondays to be coding days", "rebalance my week", "my schedule isn't working", "swap X and Y day", "add a new work type", "drop X from the rotation", or any request that permanently adjusts the weekly cadence (not just today's plan). Also trigger when the user describes a life/energy change that should shift the schedule (e.g. "I have a recurring call every Wed morning now"). Do NOT use for retrieving today's focus — use schedule-today for that.
---

# schedule-manage

Owns the canonical weekly work schedule. One file: `Wiki/Personal/schedule.md`. Read it, edit it, or create it from scratch via interview.

## When to use

- File missing → bootstrap via interview.
- File exists + user wants change → load, propose edit, write back.
- User describes new constraint (recurring meeting, energy shift, new role) → fold into schedule.

If the user just wants today's focus, redirect to `schedule-today`. This skill is for permanent structural change.

## The schedule file

Path: `/home/jared/Documents/wiki/Personal/schedule.md`

Structure (keep simple, human-readable, machine-parseable):

```markdown
---
type: resource
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
tags: [schedule, work, personal-systems]
---

# Work Schedule

## Principles
- <1-line principles that shape the schedule, e.g. "filming batched mid-week to protect Monday momentum">
- <energy/biology constraints, e.g. "deep work mornings, admin afternoons">

## Work types
- **<Type name>**: <what counts as this type, e.g. "Content research: scrolling refs, watching reels, taking structure notes">
- **<Type name>**: <...>

## Weekly cadence

### Monday
- **Morning**: <work type> — <optional note>
- **Afternoon**: <work type>
- **Evening**: <work type or "off">

### Tuesday
- ...

(through Sunday)

## Fixed commitments
- <recurring meeting, gym, family time, etc. — anything that constrains a slot>

## Balance targets (weekly hours, approximate)
- Content research: ~Xh
- Filming: ~Xh
- Coding: ~Xh
- Week planning: ~Xh
- ...

## Notes
- <anything else the schedule-today skill should know to interpret blocks>
```

Three blocks per day (morning / afternoon / evening) is the default — enough granularity to be useful, not so fine it becomes a calendar. If the user wants different granularity (e.g. two blocks, or named slots like "9-12 / 13-17 / evening"), follow their preference.

## Workflow

### Bootstrap (no file exists)

Interview the user. Don't try to design their schedule for them — ask, then write what they say. Cover:

1. **Work types**: "What buckets of work are you balancing this season? Give me the abstract types — e.g. content research, filming, coding, week planning, admin, deep thinking. ~4–8 is typical."
2. **Energy / biology**: "When are you sharpest? When do you fade? Any non-negotiable rest blocks?"
3. **Fixed commitments**: "Anything recurring that locks a slot — gym, family, standing meetings?"
4. **Cadence preferences**: "Do you want batching (e.g. Mon/Tue = filming-heavy) or interleaving (a bit of everything each day)? Any day you protect for a specific thing?"
5. **Balance targets**: "Roughly how many hours per week should each type get? Ranges are fine — this is the rebalance check, not a contract."

Then draft the schedule, show it, ask for adjustments, write the file.

### Edit (file exists)

1. Read the current file.
2. Confirm the change: "You want to move filming from Wed to Tue afternoon, and Wed afternoon becomes coding — right?"
3. Apply edit with the Edit tool, preserving structure.
4. Update the `Updated:` frontmatter date to today.
5. **Balance check**: after the edit, recompute rough weekly hours per type. If a type is now starved or overweighted vs. its target, flag it. Don't auto-correct — flag it and ask.
6. If the change implies a deeper rebalance (e.g. user adds a new work type, or kills one), offer to do a full rebalance pass.

### Rebalance pass

Sometimes the right answer is "tear it up and redo". Trigger when:
- User adds/removes a work type.
- User says "this isn't working" without naming a specific change.
- Multiple types are off-target after a small edit.

In a rebalance: re-run the bootstrap interview but use the existing file as a starting draft instead of a blank slate.

## Principles for the editor (you)

- **The user owns the schedule. You ask, they decide.** Don't impose a "best-practice" cadence. Some people batch, some interleave. Some film at 6am, some at 9pm.
- **Write what they say in their language.** If they call it "shoot day" not "filming", use "shoot day". The schedule needs to feel like theirs.
- **Surface trade-offs, don't hide them.** "Moving filming to Tue takes deep coding from Tue morning. Want to push coding to Wed, or shrink the filming block?"
- **Keep the file lean.** No prose paragraphs. Bullets, slots, frontmatter. The other skill has to parse this.
- **Date discipline.** Always update `Updated:` to today (use the date from the environment context).

## Anti-patterns

- Writing the schedule before interviewing. Even if the user gives a partial spec, ask the gaps.
- Editing without reading the current file first.
- Silently rebalancing without showing the user.
- Adding planning theatre (Eisenhower matrices, deep-work scores, etc.) the user didn't ask for.
- Treating the schedule as a calendar of specific times — it's a *cadence*, not an itinerary. Today's specifics belong in `schedule-today` output, not here.
