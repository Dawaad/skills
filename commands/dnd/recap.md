---
name: "dnd:recap"
description: "Session recap and continuity tool. Generates narrative recaps, session summaries, and between-session prep briefs."
---

# /dnd:recap — Session Recap & Continuity

Three modes for session continuity: recap previous session for players, summarize current session for the log, or prepare a brief for the next session.

## Input

$ARGUMENTS — expects one of:
- `--previous {campaign-name}` or just `{campaign-name}` — narrative recap of last session (default)
- `--summarize {campaign-name}` — generate session summary for the log
- `--prepare {campaign-name}` — between-session prep brief

## Setup

1. Read the domain CLAUDE.md at `2. Areas/2.2 Dungeons & Dragons/CLAUDE.md`
2. Read entity schemas from `2. Areas/2.2 Dungeons & Dragons/_Config/Tag Taxonomy.md`

All paths below are relative to `~/docs/Documents/2. Areas/2.2 Dungeons & Dragons/`.

## Mode Detection

Parse `$ARGUMENTS`:
- `--previous` or no flag -> previous mode (default)
- `--summarize` -> summarize mode
- `--prepare` -> prepare mode
- Extract campaign name from remaining text
- If no campaign name, list campaigns and ask

---

## Previous Mode (Narrative Recap)

For reading aloud to players at the start of a session.

### 1. Find Most Recent Session

Glob `1. Campaigns/{campaign-name}/Sessions/*.md`. Filter for files with `status: completed` in frontmatter. Sort by `session-number` descending. Take the first (most recent completed).

If no completed sessions exist, report "No completed sessions found. This appears to be the first session."

### 2. Read Session Content

Read the full session file. Extract:
- Session number and date played
- Game day range (start to end)
- All body sections: Recap, Events, Combat Encounters, NPC Interactions, State Changes, Loot Acquired

### 3. Read Supporting State

For richer context, also read:
- World Clock (current state for continuity)
- Any NPC files referenced in the session's NPC Interactions section (read their Memory sections for recent entries)
- Active quests that were mentioned or progressed

### 4. Generate Narrative Recap

Write a narrative recap in second person ("You...") or third person ("The party...") — match the DM's style if previous recaps exist.

Structure the recap as:

```markdown
## Session {N} Recap

*Last time, on {Campaign Name}...*

{Opening — set the scene, where were they, what were they doing}

{Key events in narrative order — weave together Events, Combat, and NPC interactions into a flowing story}

{Highlight key decisions the party made and their immediate consequences}

{End on the cliffhanger or hook — what's hanging, what's unresolved, where are they now}

---

**Where we left off:** Day {N}, {time} — {location}. {One-sentence situation summary}.
```

Guidelines:
- Keep it 2-4 paragraphs (2-3 minutes to read aloud)
- Mention each PC by name at least once
- Emphasize player agency — frame their decisions as driving the story
- End with forward momentum — what's next, what's unresolved
- Do NOT include mechanical details (HP, DCs, rolls) — this is narrative only

### 5. Present to User

Display the recap. Ask: "Want me to adjust the tone, length, or emphasis?"

---

## Summarize Mode (Session Log)

For capturing what happened during a session, run at the end of play.

### 1. Identify Current Session

Read `1. Campaigns/{campaign-name}/Campaign.md` for session-count.

Check if a session file already exists for the current session number:
- If `Sessions/Session {N}.md` exists with `status: in-progress`, use it
- If no in-progress session exists, create a new one with the next session number

### 2. Gather Session Data

Read all state changes made during the session. This means reading:

**World Clock changes:**
- Read `State/World Clock.md` — check Time Log for entries from today's play

**NPC interactions:**
- Search `2. World/NPCs/` for files where Memory section has entries from the current session (matching session number or today's date)

**Quest updates:**
- Search for quest files modified today or with progress entries from this session

**Combat encounters:**
- Search `Combat/` for encounter files from this session

**Location changes:**
- Search `2. World/Locations/` for State History entries from this session

**Plot thread updates:**
- Search `State/` for plot-thread files modified during this session

### 3. Generate Session Summary

Write/update the session file at `1. Campaigns/{campaign-name}/Sessions/Session {N}.md`:

```yaml
---
type: session
campaign: "[[Campaign]]"
session-number: {N}
date-played: {today}
game-day-start: {start-day}
game-day-end: {end-day}
party-level: {current-level}
status: completed
tags:
  - "#dnd/session"
---
```

Body:

```markdown
# Session {N}

## Recap

{2-3 sentence narrative summary of the session}

## Events

{Chronological list of significant events}
- **Day {N}, {time}:** {event description}

## Combat Encounters

{List each combat with outcome}
- **{Encounter name}** ({location}) — {brief outcome, casualties, resources spent}

## NPC Interactions

{List significant NPC interactions}
- **[[{NPC Name}]]** — {what happened, disposition change if any}

## State Changes

{List all mechanical state changes}
- World Clock: Day {start} -> Day {end}
- {NPC} disposition: {old} -> {new}
- {Location} status: {old} -> {new}
- {Quest} status: {old} -> {new}

## Loot Acquired

{List items, gold, and other rewards}
- {item/gold amount} (from {source})

## Notes

{DM notes, things to remember, follow-up items}
```

### 4. Update Campaign File

Update `Campaign.md` frontmatter:
- Increment `session-count`
- Update `party-level` if it changed
- Update `Updated` date

### 5. Confirm

Present session summary to user. Ask: "Anything to add or correct before finalizing?"

---

## Prepare Mode (Next Session Brief)

Between-session prep — what's hanging, what's coming, what to plan for.

### 1. Read Current State

Read all of:
- `State/World Clock.md` — current day, time, upcoming scheduled events
- `State/Active Quests.md` context — then read actual quest files for active quests
- `State/Plot Threads.md` context — then read actual thread files for active threads
- All NPC files for this campaign — focus on relationship-score extremes and unresolved tensions
- Most recent session log — for immediate continuity

### 2. Analyze Scheduled Events

From World Clock's Scheduled Events table, identify:
- Events where Day is within 3 game-days of current-day and `triggered: false`
- Flag these as "imminent"
- Events further out but still scheduled — note as "upcoming"

### 3. Analyze Quest Deadlines

For each active quest:
- Compare `game-day-deadline` to World Clock's `current-day`
- Flag quests within 5 game-days as "urgent"
- Flag overdue quests as "critical"
- Note quests with no deadline as "open-ended"

### 4. Analyze Plot Threads

For each active or climax thread:
- Check urgency field
- Cross-reference connected quests and NPCs
- Identify which threads are "ripe" — they have active connections, escalating urgency, or player engagement

### 5. Analyze NPC Tensions

For NPCs with this campaign:
- Identify relationship-score at extremes (-3 or below, +3 or above)
- Check for recent Memory entries indicating unresolved situations
- Flag NPCs with disposition changes that haven't been addressed

### 6. Generate Prep Brief

Present to user:

```markdown
# Next Session Prep — {Campaign Name}

**Current State:** Day {N}, {time} | {location/situation}

## Imminent Events (next 1-3 game days)

{List scheduled events about to fire, with what they mean for the story}

## Urgent Quests

{Quests approaching deadline, sorted by urgency}
| Quest | Deadline | Days Left | Status |
|-------|----------|-----------|--------|

## Ripe Plot Threads

{Threads ready for advancement}
- **{Thread name}** ({urgency}) — {why it's ripe, what could happen next}

## NPC Tensions

{Unresolved NPC situations}
- **[[{NPC}]]** (disposition: {X}, score: {Y}) — {what's unresolved}

## Simmering (Not Urgent)

{Things in the background that could escalate}
- {thread/quest/event} — {current state, escalation trigger}

## Suggested Session Focus

Based on urgency and player engagement:
1. {Primary focus — what demands immediate attention}
2. {Secondary focus — what could naturally come up}
3. {Optional — side content if pacing needs it}
```

### 7. Offer Next Steps

After presenting the brief:
- "Want me to create a session plan with `/dnd:plan`?"
- "Want to drill into any of these threads?"
- "Need to look up any NPCs, monsters, or locations?"

## Edge Cases

- **No sessions yet (previous mode):** Report this is session 1, offer to run prepare mode instead
- **No state changes found (summarize mode):** Ask if the session happened or if state wasn't tracked during play
- **No active quests/threads (prepare mode):** Note the campaign may need new hooks, suggest creating some
- **Multiple campaigns active:** Always confirm which campaign before proceeding
