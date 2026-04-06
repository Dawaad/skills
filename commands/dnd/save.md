---
name: "dnd:save"
description: "Save or restore full campaign game state as a snapshot. Captures World Clock, party, quests, NPCs, locations, and plot threads."
---

# /dnd:save — Save/Restore Game State

Creates point-in-time snapshots of all campaign state, or restores from a previous snapshot.

## Input

$ARGUMENTS — expects one of:
- `save {campaign-name}` or just `{campaign-name}` — save current state
- `restore {campaign-name}` — restore from a snapshot
- Empty — ask for campaign name and default to save mode

## Setup

1. Read the domain CLAUDE.md at `2. Areas/2.2 Dungeons & Dragons/CLAUDE.md`
2. Read entity schemas from `2. Areas/2.2 Dungeons & Dragons/_Config/Tag Taxonomy.md`

All paths below are relative to `~/docs/Documents/2. Areas/2.2 Dungeons & Dragons/`.

## Mode Detection

Parse `$ARGUMENTS`:
- Contains "restore" -> restore mode
- Contains "save" or no mode keyword -> save mode
- Extract campaign name from remaining text

If no campaign name, list directories under `1. Campaigns/` and ask user to pick.

---

## Save Mode

### 1. Validate Campaign

Read `1. Campaigns/{campaign-name}/Campaign.md` to confirm it exists and is active.

### 2. Determine Snapshot Number

List files in `1. Campaigns/{campaign-name}/State/Snapshots/`. Find the highest `snapshot-session-{NNN}.md` number. New snapshot = highest + 1. If no snapshots exist, start at 1.

Also check `session-count` from Campaign.md frontmatter to use as the snapshot number if it makes more sense (align with session numbers when possible).

### 3. Read All State Files

Read each of the following, collecting frontmatter data:

**World Clock:**
- Read `State/World Clock.md`
- Extract: current-day, current-time, calendar-date, season, weather, scheduled events table

**Party (all PCs):**
- Glob `Party/*.md`
- For each PC, extract: name, player, level, hp-max, ac, class, status
- Also read Equipment and Inventory sections for key items

**Active Quests:**
- Grep for `type: quest` files in the campaign directory tree
- For each quest, extract: name, status, priority, quest-giver, game-day-deadline, reward

**NPCs:**
- Search `2. World/NPCs/` for files where `campaign:` matches this campaign
- For each NPC, extract: name, disposition, relationship-score, status, location

**Locations:**
- Search `2. World/Locations/` for files where `campaign:` matches this campaign
- For each location, extract: name, status, danger-level, controlling-faction

**Plot Threads:**
- Grep for `type: plot-thread` files in the campaign State/ directory
- For each thread, extract: name, status, urgency, thread-type

### 4. Write Snapshot File

Write to `1. Campaigns/{campaign-name}/State/Snapshots/snapshot-session-{NNN}.md`:

```yaml
---
type: snapshot
campaign: "[[Campaign]]"
snapshot-number: {NNN}
Created: {today}
game-day: {current-day}
game-time: "{current-time}"
calendar-date: "{calendar-date}"
season: "{season}"
weather: "{weather}"
tags:
  - "#dnd/config"
---
```

Body:

```markdown
# Snapshot — Session {NNN}

Captured: {today} | Game Day: {current-day}, {current-time}

## World Clock State

- **Day:** {current-day}
- **Time:** {current-time}
- **Calendar:** {calendar-date}
- **Season:** {season}
- **Weather:** {weather}

### Scheduled Events

{Copy the full scheduled events table from World Clock}

## Party State

| Name | Player | Class | Level | HP Max | AC | Status | Key Items |
|------|--------|-------|-------|--------|-----|--------|-----------|
{row per PC}

## Quest State

| Quest | Status | Priority | Quest Giver | Deadline | Reward |
|-------|--------|----------|-------------|----------|--------|
{row per quest}

## NPC Dispositions

| NPC | Disposition | Relationship | Status | Location |
|-----|------------|--------------|--------|----------|
{row per NPC}

## Location States

| Location | Status | Danger Level | Controlling Faction |
|----------|--------|-------------|-------------------|
{row per location}

## Plot Threads

| Thread | Type | Status | Urgency |
|--------|------|--------|---------|
{row per plot thread}
```

### 5. Confirm Save

Report to user:
- Snapshot file path
- Number of entities captured (PCs, quests, NPCs, locations, threads)
- Current game day and time
- "Restore with `/dnd:save restore {campaign-name}`"

---

## Restore Mode

### 1. List Available Snapshots

Glob `1. Campaigns/{campaign-name}/State/Snapshots/snapshot-session-*.md`. Present list:

```
Available snapshots for {campaign-name}:
1. snapshot-session-001.md — Day 1, morning (2026-03-21)
2. snapshot-session-005.md — Day 12, evening (2026-03-28)
```

Ask user which to restore.

### 2. Destructive Action Warning

This is a destructive operation. Display warning and require explicit confirmation:

```
WARNING: Restoring will overwrite current state for:
- World Clock (day, time, weather)
- All PC stats referenced in the snapshot
- All quest statuses
- All NPC dispositions and relationship scores
- All location states
- All plot thread statuses

Current state will NOT be automatically backed up.

Type "confirm restore" to proceed, or "save first" to create a snapshot before restoring.
```

If user says "save first", run save mode first, then proceed with restore.

### 3. Read Snapshot

Read the selected snapshot file. Parse all tables to extract entity states.

### 4. Restore World Clock

Read current `State/World Clock.md`. Update frontmatter fields:
- current-day
- current-time
- calendar-date
- season
- weather

Replace the Scheduled Events table with the snapshot's version.

Append to Time Log:
```
- **Day {current-day}, {current-time}:** RESTORED from snapshot-session-{NNN}. State rolled back to Day {snapshot-day}, {snapshot-time}.
```

### 5. Restore PC State

For each PC in the snapshot's Party State table:
- Find the PC file in `Party/`
- Update frontmatter: level, hp-max, ac, status
- Do NOT overwrite Equipment/Inventory sections (snapshot only captures key items for reference)

### 6. Restore Quest State

For each quest in the snapshot:
- Find the quest file (grep for matching name in State/ directory)
- Update frontmatter: status, priority, game-day-deadline

### 7. Restore NPC Dispositions

For each NPC in the snapshot:
- Find the NPC file in `2. World/NPCs/`
- Update frontmatter: disposition, relationship-score, status

Append to Memory:
```
- **Day {restore-day} | Restore:** State restored from snapshot-session-{NNN}. Disposition: {disposition}.
```

### 8. Restore Location States

For each location in the snapshot:
- Find the location file in `2. World/Locations/`
- Update frontmatter: status, danger-level

Append to State History:
```
- **Day {restore-day}:** RESTORED from snapshot-session-{NNN}. Status: {status}, Danger: {danger-level}.
```

### 9. Restore Plot Threads

For each thread in the snapshot:
- Find the thread file in State/ directory
- Update frontmatter: status, urgency

### 10. Confirm Restoration

Report:
- Which snapshot was restored
- Number of entities updated
- Current game state (day, time)
- Any entities in snapshot that couldn't be found (warn user)

## Edge Cases

- **Entity in snapshot no longer exists:** Warn user, skip that entity, list in report
- **Entity exists now but not in snapshot:** Leave untouched (it was created after the snapshot)
- **No snapshots available:** Inform user, suggest running save first
- **Snapshot file corrupted/unparseable:** Report error, do not partially restore
- **Campaign not found:** List available campaigns and ask user to pick
