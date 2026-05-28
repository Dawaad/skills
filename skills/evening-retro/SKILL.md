---
name: evening-retro
description: End-of-day retrospective + journalling ritual. Reviews today's plan against actual delivery (majors/minors vs success criteria from the daily note), syncs project progress back into the project-tracker catalog, runs a short adaptive journalling interview to capture cognitive/emotional state, assesses workflow effectiveness against recent retro history, and proposes adjustments that morning-routine will consult on future plans. Writes a structured snapshot to /home/jared/Documents/wiki/Personal/retros/YYYY-MM-DD.md, updates the end-of-day section of today's daily note, and surfaces generalisable learnings as candidates for promotion into the Personal wiki as `kind: insight` pages. Use this skill whenever the user says "evening retro", "end of day", "wrap up the day", "day review", "evening review", "retro", "how did today go", "shut down", "close out the day", "did I get my majors done", "what worked today", "what didn't work today", "review my day", "log today", or any variation of closing the day's loop. Also trigger when the user describes wanting to journal, reflect, decompress, or capture how the day actually went vs how it was planned. Do NOT use for morning planning (that's morning-routine), schedule changes (schedule-manage), or one-off journal entries unrelated to today's plan.
---

# evening-retro

The end-of-day counterpart to `morning-routine`. Closes the loop: today's plan was the hypothesis, today's reality is the data, and this skill is where the user updates their model of what works.

The deliverable is a written **retro snapshot** + a updated daily note + project-catalog updates + (optionally) planning adjustments that future morning routines will respect. The chat surface is the interview itself; the artifacts are what persist.

## Why this exists

Morning planning without evening review is a one-way function — plans go in, outcomes evaporate. The user is trying to build a closed loop where today's experience compounds into better future days. Three things have to happen for that to work:

1. **The plan gets graded honestly.** Did the majors get done? Did they meet the success criteria the morning-self set, or did they get marked "done" because something happened that vaguely resembled the task? Without this, success criteria become decorative.
2. **Project state stays warm.** Every active project that got touched today should have its `current state` / `next action` / `log` updated before bed. Otherwise the catalog drifts within a week and the morning routine has to reconstruct context every day.
3. **Patterns become legible.** Energy, focus, friction, mood — these aren't noise. They're the signal that explains why some Tuesdays produce three majors and other Tuesdays produce one. The retro snapshot is the unit of trend data; the wiki insight pages are the synthesised takeaways.

Treat the user's evening attention as scarce — they are tired, this is the last thing before wind-down. Be terse, structured, and skip phases that are empty. A 20-minute retro is a failure; a 6-minute retro that closed the loop is a win.

## Inputs

- **Date**: default = today, host timezone. Accept "yesterday" if the user runs late.
- **Daily note**: `/home/jared/Documents/wiki/Inbox/YYYY-MM-DD.md` — the plan to grade against.
- **Project catalog**: `/home/jared/Documents/wiki/Personal/projects/` — via the `project-tracker` skill.
- **Retro history**: `/home/jared/Documents/wiki/Personal/retros/*.md` — for trend assessment in Phase 5.
- **Planning adjustments log**: `/home/jared/Documents/wiki/Personal/planning-adjustments.md` — append-only file that `morning-routine` will consult.
- **Standing schedule**: `/home/jared/Documents/wiki/Personal/schedule.md` — for "what kind of day was this".
- **Retro snapshot template**: `assets/retro-template.md` (bundled in this skill).

## Workflow

Six phases. Run them in order. Each phase produces state used by later phases. Show the user a short status line as each phase wraps so the conversation stays alive (`✓ activity reviewed — 2/3 majors`, etc.). If a phase has nothing to do (e.g. no daily note exists, no projects touched), say so plainly and skip — don't pad.

### Phase 1 — Load context

1. Compute today's date. Build path: `Inbox/YYYY-MM-DD.md`.
2. Read the daily note. Extract: majors (titles + success criteria), minors (titles + criteria), standing focus, schedule blocks.
3. If the daily note doesn't exist or has no morning plan, this is a degraded retro — tell the user there's nothing to grade against and ask whether they want to (a) just journal without a plan-review (skip Phase 2), or (b) abort and run morning-routine retroactively first. Default = journal-only mode.
4. Invoke `project-tracker` in `morning-context` mode to get current active-projects state. You'll need this for Phase 3 to identify which projects were touched.
5. Read the last 7 days of retro snapshots from `Personal/retros/` (newest first). Keep them in working memory for Phase 5 trend analysis. If `retros/` is empty, this is the first retro — note it; Phase 5 will produce a baseline rather than a comparison.

### Phase 2 — Activity review (objective)

Walk through the plan. For each major, then each minor:

1. Ask: **done / partial / skipped?** Keep it terse — one line per task. Example: `Major 1: PR opened for auth migration — done?`.
2. If done, ask: **did it meet success criteria?** Restate the criteria from the daily note so the user grades honestly rather than from memory. `Criteria: "PR opened and reviewer tagged" — met?`
3. If partial or skipped, ask: **what stopped it?** Keep the answer short — one sentence. This feeds Phase 4 (friction patterns).
4. Capture the verdicts in a small structured table for Phase 6 to write to the snapshot:

```
- Major 1: <title> · status=<done|partial|skipped> · criteria=<met|not-met|n/a> · note=<one line>
- Major 2: …
- Minor 1: …
```

Principles:
- **Grade by criteria, not vibes.** "I did some work on it" ≠ done if the criterion was "PR opened". Push back gently if the user marks done without the criterion being met — name the gap. The point is honest data.
- **One pass through the list.** Don't loop back. If the user wants to reconsider, they will.
- **Skip the criteria question for trivial minors with no defined criterion.** Just `done?` is enough.

### Phase 3 — Project sync

For every active project that got concrete work today (cross-reference Phase 2 tasks against the project catalog — most majors are project next-actions because morning-routine sources them that way):

1. Tell the user which project you're updating: `Updating cranium-rework-migration —`.
2. Ask the **smallest set of questions** needed to move the project forward:
   - If the next action got done: what's the new next action?
   - Did the current state change? Restate in one sentence.
   - Any new blockers? Any blockers cleared?
   - One-line log entry — what moved.
3. Invoke `project-tracker` `update` mode with the captured deltas. Trust that skill to handle the file + index mirror.
4. If a major was completed and the project itself is done, prompt: `That looks like the last step — mark <project> completed?`. If yes, route through `project-tracker` `status-change` for completion.
5. If a project had work today but its log entry from morning-routine never landed (the "pulled into daily plan" line), add it now alongside the retro update. The catalog should always be self-consistent by end of day.

Don't ask about projects that weren't touched. The point isn't a full sweep — that's a separate ritual (weekly review). Tonight is just "what moved".

### Phase 4 — Journalling interview

This is the part that builds the *trend layer* over time. Stay conversational, not clinical. The goal is to capture state that the user couldn't otherwise reconstruct in two weeks.

Ask 3–5 questions, adaptive based on what came up in Phase 2. Pick from this menu — don't ask all of them; pick the ones that fit today:

**Always ask one or two of these (energy / cognition):**
- "Energy through the day — 1 to 10? Peaks and troughs?"
- "Focus quality — could you hold attention, or were you fragmented?"
- "When did the day feel best? When did it feel worst?"

**Ask when Phase 2 showed surprises (positive or negative):**
- "<task> went better than expected — what made the difference?"
- "<task> got skipped — what actually happened? Be honest about the friction."
- "Anything land that wasn't on the plan? What pulled you toward it?"

**Ask when the day matched / didn't match its standing character:**
- "It was a <coding/filming/etc> day on the schedule — did it actually run as that, or did the day shape-shift?"
- "If you ran today's schedule again next week, what would you change about how it's allocated?"

**Ask one open-ended capture question:**
- "Anything on your mind worth getting out before bed — a worry, a half-formed idea, a thing to remember?"
- "If you could only carry one thing forward into tomorrow, what would it be?"

Interview principles:
- **Listen for emotional shape, not just facts.** "Frustrated about the auth PR review delay" is more useful future signal than "auth PR is pending review". Capture the affect.
- **Don't interrogate.** If the user gives a one-word answer, that itself is a data point — log it and move on. Don't extract.
- **Free-form > forms.** This is the one phase where prose beats structure. The user's actual words, in their voice, are what makes trend-recognition work later when patterns emerge.
- **Tag for retrieval.** As the user answers, mentally tag the response: `#energy`, `#focus`, `#friction-<source>`, `#win`, `#filming-day`, `#decision`, etc. Phase 6 will write these as frontmatter tags on the snapshot so future queries (`"show me all #focus #fragmented days"`) work.

Capture the interview as a prose block (not structured Q&A) — Phase 6 will fold it into the snapshot under `## Journal`. Keep the user's own phrasing wherever possible.

### Phase 5 — Workflow assessment + adjustment proposals

This is the closed-loop phase. Use Phase 2 data + Phase 4 journal + the last 7 retro snapshots to surface signal.

1. **Today's completion rate.** Compute: `majors completed/3`, `minors completed/3`, `criteria-met rate` (of the completed tasks, how many actually met their criteria).
2. **Compare to the 7-day rolling baseline.** From the retro history, average the same three numbers. Tell the user: `Completion today: majors 2/3 (vs 1.7/3 7-day avg), criteria-met 100% (vs 67% avg) — strong day.` Keep it factual; don't moralise.
3. **Surface patterns** when they're real, not when they'd be neat. Examples of real patterns worth surfacing:
   - "This is the 3rd filming day in a row where minor #3 got skipped — that slot might be optimistic on filming days."
   - "When the morning plan had ≥2 majors anchored to active projects, your criteria-met rate is 90%; otherwise it's 50%. The project-anchoring rule is paying off."
   - "Energy dropped consistently in the 12-3 block this week. Walk timing or food timing might be worth experimenting with."
   Only surface a pattern if it's stable across ≥3 data points or a single very strong signal. Avoid trend-narrating from one bad day.
4. **Propose adjustments**, max 2 at a time. Adjustments are concrete experiments, not vague intentions. Bad: "be more focused". Good: "tomorrow's morning routine: cap minors at 2 on filming days". For each proposed adjustment, ask the user one of three things:
   - `Try this tomorrow only? (one-day experiment)`
   - `Add to the planning-adjustments log? (morning-routine will consult)`
   - `Drop it? (not the right call)`
5. For any adjustment the user wants persistent, append to `planning-adjustments.md` with structured shape (see file format below). For one-day experiments, hold it in Phase 6's snapshot under `## Tomorrow's experiment` and trust the user to read their own daily note tomorrow morning.

If there's no recent data (first or second retro), skip the comparison and just state today's numbers. Adjustments still work — the user knows their own friction without needing 7 days of data.

### Phase 6 — Persist artifacts

Three writes, in this order. Don't ask permission — the user already committed by going through the interview. Just confirm afterwards.

**6a. Retro snapshot file.**

Path: `/home/jared/Documents/wiki/Personal/retros/YYYY-MM-DD.md`.

If the file already exists (rare — usually means the user ran the retro twice today), append a second `## Retro (added <HH:MM>)` section instead of overwriting. Never lose journal content.

Read `assets/retro-template.md`, substitute placeholders, write. The snapshot is the canonical unit of historical retro data — keep its structure stable so future trend queries don't break.

**6b. Daily note end-of-day section.**

Open the daily note. Find the `## End-of-day review` section (the morning-routine template already provides it as a stub). Replace the stub with the filled version:

```markdown
## End-of-day review

- **Majors completed:** 2/3
- **Minors completed:** 3/3
- **Criteria-met rate:** 80%
- **Energy / focus:** 7 / 6
- **What worked:** <one or two lines from Phase 4>
- **What didn't:** <one or two lines>
- **Carry to tomorrow:** <if any>

Full retro: [[retros/YYYY-MM-DD]]
```

The link back to the snapshot is important — daily notes are the entry point users will rediscover; the snapshot is where the depth lives.

**6c. Planning adjustments (if any new adjustments from Phase 5).**

Append-only. Path: `/home/jared/Documents/wiki/Personal/planning-adjustments.md`. Schema:

```markdown
---
type: planning-adjustments-log
Updated: YYYY-MM-DD
---

# Planning Adjustments

Append-only log of experiments and tuning the user has chosen to persist from evening retros. `morning-routine` reads this file in Phase 4b/5 and applies the still-active adjustments when relevant. Each entry has a status — adjustments are not forever; the user can mark them retired.

## Active

### 2026-05-14 — Cap minors at 2 on filming days
- Source retro: [[retros/2026-05-14]]
- Trigger: today's schedule = filming
- Adjustment: when proposing the 3+3 plan, downgrade to 3+2 — filming days have less slack than coding days.
- Review on: 2026-06-14 (1 month)

## Retired
<!-- adjustments the user decided weren't working -->
```

When appending, also bump the `Updated:` frontmatter field.

### Phase 7 — Promote insights (optional, low-friction)

If anything from Phase 4's journal sounded like a *generalisable* observation rather than a today-only feeling — e.g. "I notice I shut down when I have to context-switch from coding to meetings" — surface it once:

> Heard you say: "<paraphrase>". That sounds more durable than a one-day feeling. Want me to draft it as a `kind: insight` page under `Personal/pages/` so it joins the trend layer?

If yes, write a wiki insight page following the Personal wiki's Insight template (Pattern / Evidence / Implication / Source / Cross-links). Use the retro snapshot as the `Source`. Otherwise drop it. Don't push more than once per retro — promoting insight pages is the user's decision, not a habit.

This is the bridge from operational retro data to durable wiki knowledge. Most evenings will produce zero insight pages; that's fine. The point is to catch the rare durable observation when it does land.

## Output to chat (after Phase 6)

Send one compact closing message:

```
Retro saved — <Day>, <date>

Majors: 2/3 · Minors: 3/3 · Criteria-met: 80%
Energy 7 · Focus 6
Trend: completion rate stable, criteria-met up from 7d avg
1 adjustment logged · 1 insight drafted

Saved to wiki/Personal/retros/<date>.md
Daily note end-of-day section updated.
```

If the retro produced no adjustments or insights, drop those lines. Don't pad.

That's the deliverable. Don't restate the full journal — it lives in the file. The chat closes the day; the file is the working document tomorrow.

## Bundled assets

- `assets/retro-template.md` — the retro snapshot skeleton. Read it, substitute placeholders, write the result. Single source of truth for retro shape — change the template, not this SKILL.md, if you want to evolve the format.

## Integration with other skills

- **`morning-routine`** — Symmetric partner. Morning produces the plan; evening grades it and updates the project catalog. Morning-routine in Phase 4b reads `planning-adjustments.md` (the active section) and applies relevant adjustments when proposing the day's plan. Don't duplicate logic across the two — the daily note + adjustments file are the shared state.
- **`project-tracker`** — Called in Phase 3 to update each touched project. This is the *primary* update path for projects — most days, the morning's `pulled into plan` log lines and the evening's `progress update` log lines together form the project's audit trail. Don't ask the user to update projects manually outside of this skill (unless they explicitly want to mid-day).
- **`schedule-today`** — Used in Phase 1 to know what kind of day today *was supposed to be*. Phase 4 may ask the user whether the day actually ran as that character. If multiple recent retros show the day-character mismatch, that's a Phase 5 pattern worth surfacing (and possibly a hint that `schedule-manage` should be run to re-allocate).
- **wiki pages** — Phase 7 promotes durable observations into `kind: insight` pages under `Personal/pages/`. The retro snapshot itself is *not* a wiki page — it's operational, not knowledge. Insight pages are the curated layer.
- **`changelog`** / **weekly retro** — When the user later runs a weekly retro, this skill's snapshots are the obvious source material. Make sure the snapshot frontmatter (`energy`, `focus`, `majors_completed`, `minors_completed`, `criteria_met_rate`, tags) is structured enough that future skills can aggregate without re-parsing prose.

## Principles

- **Grade against criteria, not memory.** The success-criteria field exists for this moment. Use it. Push back when the user marks done without the criterion being met — that's the discipline that makes morning planning valuable.
- **The interview is the deliverable.** The user gets value during Phase 4, not just from the file. If the conversation is mechanical or feels like a form, you've lost the point. Stay curious, stay specific.
- **Capture the affect.** Future-you needs to know whether yesterday was "fine, 2/3 majors" or "miserable, 2/3 majors". Those are different days that will not produce the same patterns. Tag emotional state.
- **Stable structure, free-form prose.** Snapshot frontmatter and headings stay stable across files (so trend queries work). The body under `## Journal` is whatever shape today wants. Don't impose structure on the journal.
- **Closed loop > closed day.** The retro is only useful if tomorrow's planning is informed by today's learning. The planning-adjustments file is how that informs forward. Use it sparingly — every adjustment is a constraint the morning routine has to apply; over-adjustment ossifies the system.
- **Idempotent + safe.** Running the retro twice in one evening shouldn't blow away the first run's journal. Same contract as morning-routine: read, append rather than overwrite if content already exists.

## Edge cases

- **No daily note for today.** Either the user skipped morning-routine or it's been a wild day. Offer journal-only mode (skip Phase 2, run Phase 4 + 6 only). Don't make the user run morning-routine retroactively unless they want to.
- **Daily note exists but plan was never executed (e.g. user was sick).** Don't grade harshly. Phase 2 takes ~30 seconds — mark everything skipped, note "sick day" in the journal, and skip Phase 5's adjustments (one-off days aren't pattern data).
- **Retros directory doesn't exist.** Create it. First retro will be the only file; Phase 5 baseline becomes "n/a — first retro".
- **User runs retro late at night and is exhausted.** Detect signs of tired one-word answers in Phase 4. Cut the interview short — 2 questions instead of 5 is fine. Don't sacrifice the next morning by extracting tonight.
- **User runs retro for "yesterday".** Same flow, dated to yesterday. Useful when morning was hectic and tonight is the catch-up. Just resolve the date carefully.
- **Project mentioned wasn't in the catalog.** If the user worked on something not tracked, prompt once: `That doesn't appear to be in the project catalog — was it a one-off, or should I add it via project-tracker?`. Don't force; some work is genuinely one-off.
- **Planning-adjustments.md doesn't exist.** Create it with the schema shown above, then append the first entry.

## Failure modes to avoid

- **Form-filling.** If Phase 4 feels like answering a survey, you've lost the user. Stay conversational. Skip questions that don't fit today.
- **Over-grading.** A 2/3 majors day is not a failure. The point is data, not judgement. Don't moralise about completion rates.
- **Pattern-narrating from noise.** One bad day is not a trend. Three bad days in a row with the same shape is. Be patient with the data.
- **Adjustment-creep.** Don't accumulate planning adjustments faster than the user can internalise them. If the active section in `planning-adjustments.md` has more than ~5 entries, prompt: `the planning-adjustments list is getting long — want to retire any?`. The morning routine can only respect so many overrides before the standing schedule and project priorities stop mattering.
- **Promoting insights too aggressively.** Insight pages are precious. One per week tops, mostly less. If you're suggesting one every retro, lower the bar — most retro observations are operational state, not durable knowledge.
- **Letting the journal lose the user's voice.** When writing the snapshot, preserve phrasing. "Felt like swimming through molasses on the auth review" is better than "user reported low energy on review tasks". The trend layer is built on language as much as on numbers.

## Bootstrap

If any of these don't exist yet, create them:
- `Wiki/Personal/retros/` — directory for snapshot files.
- `Wiki/Personal/planning-adjustments.md` — empty log with the schema shown above.

Do this silently on first run. Don't make the user manage the scaffolding.
