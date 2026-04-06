---
name: "dnd:campaign"
description: "Campaign arc planning and status dashboard. Plan mode runs an interview to define the overarching story, BBEG, milestones, and factions. Status mode presents a comprehensive campaign dashboard from live state files."
---

# /dnd:campaign -- Campaign Arc Planning & Status

Two modes: plan the overarching campaign arc with milestones and story structure, or view a comprehensive status dashboard from live state.

## Input

$ARGUMENTS -- expects one of:
- `plan {campaign-name}` or `--plan {campaign-name}` -- campaign arc planning interview
- `status {campaign-name}` or `{campaign-name}` -- status dashboard (default)
- Empty -- list active campaigns and ask

## Setup

1. Read the domain CLAUDE.md at `2. Areas/2.2 Dungeons & Dragons/CLAUDE.md`
2. Read entity schemas from `2. Areas/2.2 Dungeons & Dragons/_Config/Tag Taxonomy.md`

All paths below are relative to `~/docs/Documents/2. Areas/2.2 Dungeons & Dragons/`.

## Mode Detection

Parse `$ARGUMENTS`:
- `plan` or `--plan` -> plan mode
- `status` or bare campaign name -> status mode
- If no arguments, list campaigns under `1. Campaigns/` and ask which + which mode

---

## Plan Mode -- Campaign Arc Interview

### 1. Load Existing State

Read `1. Campaigns/{campaign}/Campaign.md`. If it exists, read current arc details. The interview will update/extend what's already there.

If the campaign doesn't exist, offer to create it via `/dnd:init` first.

### 2. Overarching Story

Ask:

- "What's the central conflict of this campaign?" -- the core tension driving everything
- "What's the BBEG (Big Bad Evil Guy) or primary antagonist?" -- could be a person, faction, force of nature, or concept
- "What's the endgame?" -- how does this campaign reach its conclusion?

If published adventure:
- Ask which book/module
- Offer to outline the published arc structure (chapters, key beats)
- Ask what modifications the DM is making

If homebrew:
- Ask for a 2-3 sentence elevator pitch
- Ask about the setting's unique features

### 3. Story Structure -- Acts & Milestones

Ask: "How do you see this campaign structured? How many major acts or phases?"

Suggest a standard 3-5 act structure:

```markdown
### Act Structure

**Act 1: {Name}** (Levels {X}-{Y})
- Theme: {what this act is about}
- Key event: {the major beat}
- Ends when: {milestone that triggers Act 2}

**Act 2: {Name}** (Levels {X}-{Y})
- Theme: {escalation, complication}
- Key event: {major beat}
- Ends when: {milestone}

**Act 3: {Name}** (Levels {X}-{Y})
- Theme: {climax, resolution}
- Key event: {final confrontation}
- Ends when: {campaign conclusion}
```

For each act, ask:
- What's the major milestone or turning point?
- What changes for the party?
- What's the dramatic escalation from the previous act?

### 4. Major NPCs & Factions

Ask: "Who are the major players in this campaign?"

For each major NPC:
- Name and role (ally, antagonist, patron, mentor, rival)
- Relationship to the central conflict
- When do they appear?
- Offer to create NPC files immediately

For each major faction:
- Name and alignment
- Goals (that intersect with the party's story)
- Leader
- How the party encounters them
- Offer to create faction files

### 5. Level Range & Progression

Ask:
- "What level does the campaign start at?" (read from Campaign.md if set)
- "What level should it end at?"
- "Any key levels where important features unlock?" (e.g., "Level 5 is when they get extra attack and the combat shifts")

Map levels to acts:
```
Act 1: Levels 1-5 (Tier 1 -- local heroes)
Act 2: Levels 5-10 (Tier 2 -- regional heroes)
Act 3: Levels 10-15 (Tier 3 -- masters of the realm)
```

### 6. Key Locations

Ask: "What are the major locations in this campaign?"

For each:
- Name and type (city, dungeon, wilderness, plane)
- Which act(s) it features in
- Why it matters to the story
- Offer to create location files

### 7. Themes & Tone

Ask:
- "What themes do you want to explore?" (power, corruption, redemption, friendship, loss, duty, freedom)
- "What's the tone?" (dark/gritty, heroic/epic, lighthearted/comedic, horror, political intrigue)
- "Any content limits or safety tools?"

### 8. Write/Update Campaign.md

Update `1. Campaigns/{campaign}/Campaign.md` with the arc details.

Add or update these sections:

```markdown
## Campaign Arc

### Central Conflict
{The overarching conflict}

### BBEG / Primary Antagonist
{Who/what they are, their goals, their methods}

### Endgame
{How the campaign concludes}

### Act Structure

{Full act structure from Step 3}

### Major NPCs
{List with wiki links and roles}

### Major Factions
{List with wiki links and allegiances}

### Level Progression
{Level range mapped to acts}

### Key Locations
{List with wiki links and act associations}

### Themes & Tone
- **Themes:** {list}
- **Tone:** {description}
- **Content limits:** {any safety tools or avoided content}
```

### 9. Create Supporting Files

Offer to create any files discussed during the interview:
- NPC files for major NPCs
- Faction files for major factions
- Location files for key locations
- Plot thread files for the main storylines

### 10. Confirm

Present a summary of the campaign arc:

```
Campaign Arc: {Campaign Name}
- {N} acts, levels {X} to {Y}
- Central conflict: {one-line}
- BBEG: {name}
- {N} major NPCs, {N} factions, {N} key locations
- Tone: {tone}
```

"Ready to plan your first session with `/dnd:plan`."

---

## Status Mode -- Campaign Dashboard

### 1. Read All State Files

Read comprehensively:

- `1. Campaigns/{campaign}/Campaign.md` -- overview, arc, session count, party level
- `1. Campaigns/{campaign}/State/World Clock.md` -- current day, time, scheduled events
- `1. Campaigns/{campaign}/Party/*.md` -- all PCs
- `1. Campaigns/{campaign}/State/` -- all quest files
- `1. Campaigns/{campaign}/State/` -- all plot-thread files
- `1. Campaigns/{campaign}/Sessions/` -- most recent session (for latest activity)
- `2. World/NPCs/` -- NPCs linked to this campaign (check `campaign:` frontmatter)
- `2. World/Factions/` -- factions linked to this campaign
- `2. World/Locations/` -- locations linked to this campaign

### 2. Present Campaign Dashboard

```markdown
# {Campaign Name} -- Status Dashboard

**System:** D&D 5e | **Setting:** {setting} | **Source:** {source}
**Sessions Played:** {session-count} | **Party Level:** {party-level}
**Current Game Day:** {current-day}, {current-time}
**Last Played:** {most recent session date}

---

## Party

| PC | Player | Race | Class | Level | HP | AC | Status |
|----|--------|------|-------|-------|-----|-----|--------|
{row per PC from Party/ files}

## World Clock

- **Day:** {current-day}
- **Time:** {current-time}
- **Season:** {season}
- **Weather:** {weather}

### Upcoming Events (Next 10 Days)
| Day | Time | Event |
|-----|------|-------|
{events where day <= current-day + 10 and triggered = false}

### Overdue Events
{events where day <= current-day and triggered = false -- these should have fired!}

## Active Quests ({count})

### Main Quests
| Quest | Giver | Day Acquired | Deadline | Days Left | Status |
|-------|-------|-------------|----------|-----------|--------|
{rows for priority = main, status = active}

### Side Quests
| Quest | Giver | Day Acquired | Deadline | Days Left | Status |
|-------|-------|-------------|----------|-----------|--------|
{rows for priority = side, status = active}

## Plot Threads ({count active})

| Thread | Type | Urgency | Status | Introduced |
|--------|------|---------|--------|------------|
{rows sorted by urgency desc}

## NPC Relationships ({count})

### Allied / Friendly
| NPC | Disposition | Score | Location | Last Interaction |
|-----|------------|-------|----------|-----------------|
{rows where disposition in [allied, friendly], sorted by score desc}

### Neutral
| NPC | Disposition | Score | Location | Last Interaction |
|-----|------------|-------|----------|-----------------|
{rows where disposition = neutral}

### Unfriendly / Hostile
| NPC | Disposition | Score | Location | Last Interaction |
|-----|------------|-------|----------|-----------------|
{rows where disposition in [unfriendly, hostile], sorted by score asc}

## Faction Standing

| Faction | Reputation | Score | Leader | Status |
|---------|-----------|-------|--------|--------|
{rows from faction files}

## Campaign Arc Progress

{If arc is defined in Campaign.md, show current act and progress toward next milestone}

**Current Act:** {act name}
**Next Milestone:** {what triggers the next act}
**Progress:** {assessment based on quest/thread states}

## Session History (Last 5)

| # | Date | Days | Key Event |
|---|------|------|-----------|
{last 5 sessions with brief recap}

---

## Suggested Next Session Focus

Based on the current state:
1. **{Primary suggestion}** -- {why: urgency, momentum, scheduled events}
2. **{Secondary suggestion}** -- {why}
3. **{Optional}** -- {lower priority thread or quest}
```

### 3. Offer Next Steps

After the dashboard:
- "Plan next session? `/dnd:plan {campaign}`"
- "Jump into play? `/dnd:play {campaign}`"
- "Update the campaign arc? `/dnd:campaign plan {campaign}`"
- "Prep between sessions? `/dnd:recap --prepare {campaign}`"
- "Drill into a specific NPC, quest, or location?"

## Edge Cases

- **Campaign not found:** List available campaigns. Offer to create one with `/dnd:init`.
- **No sessions played yet:** Show the initial state dashboard. Suggest running Session 1.
- **No arc defined:** In status mode, note "Campaign arc not yet planned" and suggest plan mode.
- **Stale data (overdue events):** Flag overdue scheduled events prominently. They may indicate a missed session or state tracking gap.
- **Campaign marked as completed/paused:** Show status but note the campaign status. Ask if DM wants to reactivate.
- **Multiple active campaigns:** Each has its own state. Never mix state between campaigns.
