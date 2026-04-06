---
name: "dnd:quest"
description: "Manage quest lifecycle — create, update, complete, fail, and list quests with full state tracking and consequence handling."
---

# /dnd:quest — Quest Lifecycle Management

Create, update, and track quests through their full lifecycle with proper state integration.

## Input

$ARGUMENTS — expects one of:
- `--create {campaign-name}` — create a new quest
- `{quest-name}` or `--update {quest-name}` — update an existing quest
- `--list {campaign-name}` — list all quests for a campaign
- `--complete {quest-name}` — mark quest completed and handle consequences
- `--fail {quest-name}` — mark quest failed and handle consequences

## Setup

1. Read the domain CLAUDE.md at `2. Areas/2.2 Dungeons & Dragons/CLAUDE.md`
2. Read entity schemas from `2. Areas/2.2 Dungeons & Dragons/_Config/Tag Taxonomy.md`

All paths below are relative to `~/docs/Documents/2. Areas/2.2 Dungeons & Dragons/`.

## Mode Detection

Parse `$ARGUMENTS`:
- `--create` -> create mode
- `--list` -> list mode
- `--complete` -> complete mode (shortcut for update with status change)
- `--fail` -> fail mode (shortcut for update with status change)
- `--update` or bare quest name -> update mode
- If ambiguous, search for existing quest by name. If found, update mode. If not found, offer to create.

Extract campaign name: check if provided, otherwise read active campaigns from `1. Campaigns/` and ask if multiple.

---

## Create Mode

### 1. Gather Quest Details

Ask for (or extract from $ARGUMENTS):

- **Quest name** — short, descriptive
- **Campaign** — which campaign this belongs to (confirm if not provided)
- **Quest giver** — NPC wiki link (e.g., `[[Gundren Rockseeker]]`)
- **Objective** — what must be accomplished
- **Priority** — main, side, or personal
- **Reward** — gold, items, favors, information, etc.
- **XP reward** — optional, numeric
- **Deadline** — game day number (optional, from World Clock reference)

### 2. Read World Clock

Read `1. Campaigns/{campaign-name}/State/World Clock.md` to get `current-day` for the `game-day-acquired` field.

### 3. Create Quest File

Write to `1. Campaigns/{campaign-name}/State/{Quest Name}.md`:

```yaml
---
type: quest
name: "{quest-name}"
campaign: "[[Campaign]]"
quest-giver: "[[{NPC Name}]]"
status: active
priority: {priority}
game-day-acquired: {current-day}
game-day-deadline: {deadline or omit}
reward: "{reward}"
xp-reward: {xp or omit}
tags:
  - "#dnd/quest"
  - "#dnd/campaign/{campaign-slug}"
---
```

Body:

```markdown
# {Quest Name}

## Objective

{Clear statement of what must be accomplished}

## Progress

- **Day {current-day}:** Quest acquired from [[{NPC}]]. {Any initial context.}

## Complications

{None yet}

## Related NPCs

- [[{Quest Giver}]] — quest giver

## Related Locations

{List any locations mentioned in the objective}

## Consequences

{To be written on completion or failure}
```

### 4. Link to NPC

If the quest-giver NPC file exists in `2. World/NPCs/`:
- Read the NPC file
- Append to their Memory section:
```
- **Day {current-day} | Session {N}:** Gave quest "[[{Quest Name}]]" to the party. Disposition: {current-disposition}.
```

### 5. Confirm Creation

Report: quest file path, linked NPC, deadline info (if set, how many game days from now).

---

## Update Mode

### 1. Find Quest File

Search `1. Campaigns/*/State/` for files where `type: quest` and name matches the provided quest name. Use Grep to find `name: "{quest-name}"` (case-insensitive).

If multiple matches, present options. If no match, offer to create.

### 2. Read Current State

Read the quest file. Display current status to user:
- Status, priority, quest giver
- Current progress entries
- Any complications
- Deadline vs current game day (read World Clock)

### 3. Ask What Changed

Prompt: "What changed with this quest?"

Common updates:
- **New progress** — what happened, which game day
- **New complication** — obstacle, twist, escalation
- **New information** — clue, revelation, lead
- **Priority change** — promoted to main, demoted to side
- **Status change** — offered -> active, active -> completed/failed

### 4. Apply Updates

**For progress/complications/info:**

Append to the appropriate section:
```markdown
## Progress

- **Day {current-day}:** {new progress entry}

## Complications

- **Day {current-day}:** {new complication}
```

**For priority change:**

Update frontmatter `priority:` field.

**For status change to completed or failed:**

Route to the Complete or Fail flow below.

### 5. Update Frontmatter

Update `Updated:` date if the field exists, or just modify the changed fields.

### 6. Confirm Update

Show the updated quest state. Note any deadline proximity warnings.

---

## Complete Mode

### 1. Find and Read Quest

Same as Update step 1-2.

### 2. Confirm Completion

Ask: "Quest complete — what happened?" Gather:
- How was it resolved?
- Was the reward given? (confirm reward from frontmatter)
- Any additional rewards or consequences?

### 3. Update Quest File

Update frontmatter:
```yaml
status: completed
```

Append to Progress:
```
- **Day {current-day}:** Quest completed. {Resolution summary.}
```

Write Consequences section:
```markdown
## Consequences

### Rewards
- {Reward from frontmatter — confirmed given}
- {Any additional rewards}
- {XP: {xp-reward} XP awarded}

### World Impact
- {How the world changed as a result}
```

### 4. Handle Downstream State Changes

Ask the user about each consequence type and apply immediately (per persistence rules):

**NPC disposition changes:**
- If quest-giver should become more friendly, update their frontmatter
- Append to NPC Memory:
```
- **Day {current-day} | Session {N}:** Party completed quest "[[{Quest Name}]]". Disposition: {new}. Relationship: {new-score}.
```

**Location state changes:**
- If completing the quest changed a location's status, update it
- Append to Location State History:
```
- **Day {current-day}:** {What changed} due to completion of [[{Quest Name}]].
```

**New quests triggered:**
- If completion opens a new quest, offer to create it immediately

**Plot thread advancement:**
- If this quest is connected to a plot thread, ask if thread status should change

### 5. Log and Confirm

Report all state changes made. List files modified.

---

## Fail Mode

### 1. Find and Read Quest

Same as Update step 1-2.

### 2. Confirm Failure

Ask: "Quest failed — what happened?" Gather:
- Why did it fail? (deadline passed, objective became impossible, party chose to abandon)
- What are the consequences?

### 3. Update Quest File

Update frontmatter:
```yaml
status: failed    # or "abandoned" if party chose to drop it
```

Append to Progress:
```
- **Day {current-day}:** Quest failed. {Reason.}
```

Write Consequences section:
```markdown
## Consequences

### Failure Impact
- {What happened because the quest failed}
- {NPC reactions}
- {World state changes}
```

### 4. Handle Downstream State Changes

Same pattern as Complete mode, but for negative consequences:

**NPC disposition changes:**
- Quest-giver likely becomes less friendly
- Update disposition and relationship-score
- Append to Memory with failure context

**Location state changes:**
- If failure worsens a location (e.g., village overrun because party didn't help)
- Update location status and danger-level

**New threats:**
- If failure creates new problems, offer to create plot threads or scheduled events in World Clock

**Scheduled events:**
- If failure triggers a future consequence, add to World Clock Scheduled Events table:
```
| {future-day} | {time} | {consequence event} | false |
```

### 5. Log and Confirm

Report all state changes made. List files modified.

---

## List Mode

### 1. Find All Quests

Grep for `type: quest` in `1. Campaigns/{campaign-name}/State/` and any subdirectories.

### 2. Read World Clock

Read current game day for deadline calculations.

### 3. Present Quest Dashboard

Group by status, then by priority within each group:

```markdown
# Quests — {Campaign Name}

**Current Game Day:** {current-day}

## Active Quests

### Main Quests
| Quest | Quest Giver | Acquired | Deadline | Days Left | Reward |
|-------|------------|----------|----------|-----------|--------|
{rows}

### Side Quests
| Quest | Quest Giver | Acquired | Deadline | Days Left | Reward |
|-------|------------|----------|----------|-----------|--------|
{rows}

### Personal Quests
| Quest | Quest Giver | Acquired | Deadline | Days Left | Reward |
|-------|------------|----------|----------|-----------|--------|
{rows}

## Completed ({count})

| Quest | Priority | Reward |
|-------|----------|--------|
{rows}

## Failed / Abandoned ({count})

| Quest | Priority | Reason |
|-------|----------|--------|
{rows}
```

**Deadline highlighting:**
- "Days Left" column: calculate `game-day-deadline - current-day`
- If <= 0: mark as "OVERDUE"
- If <= 3: mark as "URGENT"
- If <= 7: mark as "approaching"
- If no deadline: show "---"

### 4. Offer Actions

After presenting the list:
- "Update a quest? Give me the name."
- "Create a new quest with `--create`."
- "Any quests to complete or fail?"

## Edge Cases

- **Quest name has special characters:** Sanitize for filename (replace special chars with spaces or hyphens)
- **Quest giver NPC doesn't have a file yet:** Warn user, still create quest with the wiki link (NPC file can be created later)
- **No quests exist yet:** Report empty, offer to create first quest
- **Campaign has no World Clock:** Error — campaign may not be properly initialized. Suggest running `/dnd:init`
- **Quest linked to destroyed/dead NPC:** Note in update, don't error. Quest may still be completable through other means.
- **Duplicate quest names:** Append a number or ask user for a unique name
