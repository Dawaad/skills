---
name: morning-routine
description: Full morning briefing + day-planning ritual. Pulls Slack activity (via the claude.ai Slack connector), aggregates Gmail across all connected accounts (via gmail-multiaccount-summary), gathers today's calendar across all connected accounts (via calendar-today-multiaccount), reads today's standing focus from schedule-today, and then runs a propose-then-confirm planning interview that turns it all into a 3-major / 3-minor daily plan written into the Obsidian daily note at /home/jared/Documents/wiki/Inbox/YYYY-MM-DD.md. Each task gets success criteria, expected outcomes, and a complexity-aware breakdown. Use this skill whenever the user says "morning routine", "morning briefing", "good morning", "start my day", "plan my day", "kick off the day", "daily kickoff", "do the morning thing", "what's on today and what should I work on", or any variation of wanting one combined start-of-day flow that touches comms, calendar, and intentional planning. Also trigger when the user invokes /morning-routine, or when they describe a multi-source morning catch-up ("catch me up across slack, email, and calendar then help me plan").
---

# Morning Routine

A single ritual that takes the user from cold-start to a written daily plan in the Obsidian vault. Composes four existing skills + the Slack connector + an interview, in that order. The output is **today's daily note**, complete and committed to disk, plus a short chat summary.

## Why this exists

The user starts most days touching four inputs: Slack, Gmail, Google Calendar, and the standing weekly schedule. Doing this manually means four context-switches before any real planning starts, and the planning itself often gets skipped because the briefing phase ate the energy. This skill collapses the whole thing into one flow with a single decision point at the end — confirm or edit the plan — and persists the result so the daily note becomes the source of truth for the day.

Treat the user's time as the scarce resource. Be terse, lead with what changed, ask before assuming.

## Inputs

- **Date**: default = today, in the host timezone (use the date from environment context). Accept "tomorrow" or an explicit date.
- **Vault inbox**: `/home/jared/Documents/wiki/Inbox/`
- **Daily note path**: `/home/jared/Documents/wiki/Inbox/YYYY-MM-DD.md`
- **Daily note template**: `assets/daily-note-template.md` (bundled in this skill)

## Workflow

Run the five phases in order. Each phase produces a section of state you'll need in later phases — keep the outputs concise so they fit when assembling the final daily note. Show the user a short status line as each phase completes (e.g. "✓ Slack — 3 threads worth your attention") so the wait feels alive, not stalled.

### Phase 1 — Slack briefing

Use the claude.ai Slack connector tools (`mcp__claude_ai_Slack__*`). The user is in many channels; do not try to read them all. Triage with cheap calls first, open threads only when the metadata looks meaningful.

Recommended sequence:

1. `slack_search_public_and_private` for direct mentions of the user and DMs since the last working window (default: last 18h to cover overnight and early morning). Use the query syntax to filter on `from:` / `to:me` / `is:thread` as appropriate.
2. For each hit, glance at the channel + sender + first message. If it looks like signal (a question, a request, an @mention from a human, a thread the user is already in), call `slack_read_thread` to pull enough context to summarise. Skip bot posts, GitHub/CI/notification spam, and channels the user is clearly just lurking in.
3. Resolve user IDs to names via `slack_read_user_profile` only when the sender name isn't already in the search result.

What counts as "meaningful":
- direct messages
- @mentions of the user
- replies in threads the user started or already replied to
- decision-level messages in channels the user owns (you can infer ownership from prior activity)

What to drop: routine standups posted by bots, deploy notifications, marketing posts, link-share-only messages with no question attached.

Output for this phase (kept in working memory for Phase 5):

```
SLACK — <count> needs reply, <count> FYI, <N> noise skipped

Needs reply
- #channel · <sender>: <one-line gist> — <why it matters / what's being asked>
- DM · <sender>: <one-line gist>

FYI
- #channel: <one-line gist>
```

If nothing meaningful, say so plainly — `SLACK — clear`. Padding wastes the user's attention.

### Phase 2 — Gmail briefing

Invoke the `gmail-multiaccount-summary` skill. Don't reimplement its logic — read its output, keep the "Needs your attention" and "Worth knowing" blocks, drop the noise count rollups (we'll show a single noise line at the end). Hand back a compressed version for Phase 5 assembly.

### Phase 3 — Calendar briefing

Invoke the `calendar-today-multiaccount` skill. Keep:
- volume snapshot (count, booked, free)
- chronological events
- conflicts
- pending RSVPs
- notable gaps (these matter for planning in Phase 5)

### Phase 4 — Standing focus

Invoke the `schedule-today` skill to pull today's work-type allocation from `Wiki/Personal/schedule.md`. Keep the focus line, blocks, and any heads-up. This is the **frame** Phase 5 plans against — the 3-major / 3-minor plan should respect the day's standing character (e.g. don't propose three coding tasks on a filming day unless the user explicitly overrides).

If `schedule-today` reports the schedule file is missing, surface that to the user once at the end of the briefing — don't block the routine. Suggest they run `schedule-manage` later.

### Phase 4b — Active projects

Invoke the `project-tracker` skill in `morning-context` mode to load the user's current portfolio of semi-complex work (architectural migrations, feature builds, video productions, content series, etc.). The output is a structured list with each project's current state, next action, and blockers.

This phase is the **substance** Phase 5 plans against. The standing focus from Phase 4 says *what kind of work* today is for; the project list says *which specific next actions are eligible*. The Phase 5 majors should mostly be next-actions pulled from this list, filtered by:
- Today's standing focus (don't pull a filming next-action on a coding day unless explicit override).
- Priority (high before normal before low).
- Deadlines hitting in ≤14 days (surface inline; they raise priority implicitly).
- Blockers — if a project's blocker is "waiting on X", don't propose its next action unless X arrived.

If `project-tracker` reports an empty catalog, continue without it and note once at the end of the briefing: "no active projects tracked — consider running `project-tracker` to set some up". Don't block.

### Phase 4c — Planning adjustments

Read `/home/jared/Documents/wiki/Personal/planning-adjustments.md` and load the **Active** section into context. Each entry is a deliberate adjustment the user has persisted from a past evening retro — a constraint, a rule, an experiment they chose to keep. The file may not exist yet (no retros have run) — in that case, skip silently.

For each active adjustment, decide whether its **trigger** applies to today:
- Day-of-week or day-character triggers (e.g. "on filming days") → check against today's standing focus from Phase 4.
- Project-state triggers (e.g. "when cranium-rework is blocked") → check against Phase 4b's project context.
- Energy / load triggers (e.g. "when calendar density > 5 events") → check against Phase 3 calendar.
- Universal adjustments (no trigger) → always apply.

Keep matched adjustments in working memory for Phase 5 to honor. Don't lecture the user about which ones matched — just respect them in the plan. If something matches and you're going to override it (rare), name the override explicitly in the proposal so the user sees the trade-off.

If the active list has more than ~5 entries, surface that once at the end of the briefing: "planning-adjustments list is getting long — worth pruning via `evening-retro` later?". Adjustment-creep ossifies the system.

### Phase 5 — Propose-then-confirm plan

Now synthesise. Build the **3 major / 3 minor** plan from the four briefings above, anchored to the standing focus from Phase 4 and the time-shape from Phase 3.

**Framework recap (3+3):**

- **3 majors** — the things that, if done, make today a win. High-impact, anchored to the week's character. By default, **at least two majors should be concrete next-actions on active projects** (from Phase 4b), with the third reserved for Slack/email/calendar pressure or a deliberate non-project priority. The whole point of the project catalog is that the day's biggest bets compound on multi-session work rather than dissolve into reactive tasks. Override this default only when the day's reality genuinely demands it (fire drill, hard deadline elsewhere) — and name the override out loud.
- **3 minors** — smaller wins, admin, follow-ups, quick replies, errands. Cheap-to-finish items the user can use to ride momentum between majors.

For each task, propose:
- **Title** (short, verb-led)
- **Why** (one line — what makes this matter today)
- **Success criteria** (objective signal it's done — e.g. "PR opened and reviewer tagged", "30 min on bike with HR > 130", "draft sent to Sarah")
- **Expected outcome** (what becomes true once it's done — what unblocks, what the user moves toward)
- **Breakdown** — only when the task is non-trivial. Use this rule of thumb:
  - Trivial (<30 min, one obvious action) → no breakdown
  - Moderate (30 min–2h, a few steps) → 3–5 bullet sub-steps
  - Complex (half-day+, ambiguous) → name the first concrete action, the rough next milestone, and an explicit "stop and reassess" checkpoint
- **Time anchor** (optional but encouraged) — which calendar gap from Phase 3 this fits into

**Propose-then-confirm flow:**

1. Draft the full 6-item plan in one shot, presented in chat with the briefing summary on top.
2. End the proposal with three explicit asks:
   - "Swap any out?"
   - "Reorder?"
   - "Anything I've missed from your own head?"
3. Iterate on edits until the user signals approval ("looks good", "ship it", "save it", a thumbs-up emoji, etc.). One round of edits is normal; more than two probably means you over-proposed — strip back.
4. **Only after approval**, write the daily note.
5. **Mirror project pulls back into the catalog.** For every major (and any minor) that was sourced from an active project, call `project-tracker` to append a one-line log entry on that project — `- <today>: pulled into daily plan as "<task title>"`. This keeps the project catalog accurate as the source-of-truth on what's actually getting worked on, and means the user can later trace which projects got attention on which days. If a major was *not* from the project catalog but feels like multi-session work, surface that to the user once before writing the note: "this looks like a project rather than a one-off — want me to add it to the catalog?".

Do not pre-write the note and ask for approval after — the user explicitly chose propose-then-confirm because draft-then-confirm is the slow path here. Write once, write right.

### Phase 6 — Write the daily note

1. Compute the path: `/home/jared/Documents/wiki/Inbox/<YYYY-MM-DD>.md`.
2. **If the file already exists**, do NOT overwrite. Read it, decide whether the user has already added meaningful content (anything beyond the template skeleton), and:
   - If yes → append today's plan under a `## Morning Plan (added <HH:MM>)` heading at the bottom and tell the user you appended rather than replaced.
   - If no (just an empty template) → replace.
3. Read `assets/daily-note-template.md`, substitute the placeholders (see template for the full list), and write the result. Preserve the frontmatter exactly; only mutate the body sections.
4. Confirm in chat: `Wrote /home/jared/Documents/wiki/Inbox/<date>.md — 3 majors, 3 minors, briefing baked in.`

## Output to chat

After Phase 6, send one final compact message:

```
Morning briefing — <Day>, <date>

Slack: <one-line>
Email: <one-line>
Calendar: <one-line>
Focus: <one-line from schedule-today>

Today's plan
Majors
1. <title> — <why>
2. <title> — <why>
3. <title> — <why>

Minors
- <title>
- <title>
- <title>

Saved to wiki/Inbox/<date>.md
```

That's it. Don't restate the success criteria and breakdowns in chat — they live in the note. The chat message is a glance; the note is the working document.

## Principles

- **One ritual, one artifact.** The daily note is the deliverable. Everything else (briefings, summaries) is in service of it. If you find yourself outputting more chat text than what's in the note, you're inverted.
- **Compose, don't duplicate.** `gmail-multiaccount-summary`, `calendar-today-multiaccount`, and `schedule-today` already exist and do their jobs well. This skill is glue, not a replacement. Invoke them; trust their output.
- **Surface, don't invent.** If Slack is quiet, say it's quiet. If the calendar is empty, say so. Don't manufacture action items to fill a section — the absence of pressure is itself information the user can use.
- **Anchor planning to the standing focus.** The weekly schedule represents the user's pre-committed bet about what each day should be. Propose plans that respect that bet. If today's reality genuinely overrides the standing focus (e.g. a fire drill), name the override out loud so the user sees the trade-off.
- **Success criteria over verbs.** "Work on dashboard" is not a task; "Dashboard PR opened with charts rendering live data" is. Push the user toward verifiable outcomes — that's the whole point of the success-criteria field.
- **Cheap reads first.** When pulling Slack or email, always start with metadata (search results, labels, headers). Only open threads / message bodies when the metadata says they're worth it. The user is trying to start their day, not waste 30 seconds on a CI bot post.
- **Idempotent + safe.** Running this skill twice in one morning shouldn't destroy the user's work. The "already exists with content" branch in Phase 6 is the contract: never silently overwrite a daily note that has user-added content.

## Edge cases

- **Vault path doesn't exist.** `mkdir -p /home/jared/Documents/wiki/Inbox/` before writing. Don't ask the user to create it — they shouldn't have to.
- **Slack connector unavailable.** Skip Phase 1, note "Slack — connector unavailable" in the briefing, continue. Don't abort the whole ritual; the rest of the value still lands.
- **Both Google accounts un-auth'd.** Gmail and calendar skills will report this. Surface it once, suggest the user re-auth via `gog`, continue with whatever briefings did work.
- **User invokes mid-day.** Still works — the daily note is for "today" regardless of when the routine fires. If it's already 3pm, weight the proposed plan toward what's still achievable in the remaining hours (and call that out: "you've got 4 working hours left — proposing a lighter set").
- **User asks for tomorrow's routine.** Treat as a planning-ahead variant: same flow, but for tomorrow's date. Skip Slack/Gmail (they're current-state), use calendar-today-multiaccount with `--tomorrow`, use schedule-today for tomorrow, and write to tomorrow's daily-note path.
- **Schedule file missing.** Continue without Phase 4 framing. Tell the user at the end of the briefing, suggest `schedule-manage` later. Don't block on it.

## Bundled assets

- `assets/daily-note-template.md` — the Obsidian daily note skeleton. Read it, substitute placeholders, write the result. The template is the single source of truth for the note's shape — if you want to change the structure, change the template, not this SKILL.md.
