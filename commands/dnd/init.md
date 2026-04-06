---
name: "dnd:init"
description: "Initialize a new D&D 5e campaign with full directory structure, state files, and optional party setup."
---

# /dnd:init — Initialize Campaign

Scaffolds a complete campaign directory with all state tracking files, ready for play.

## Input

$ARGUMENTS — optional campaign name. If omitted, will prompt.

## Setup

1. Read the domain CLAUDE.md at `2. Areas/2.2 Dungeons & Dragons/CLAUDE.md`
2. Read entity schemas from `2. Areas/2.2 Dungeons & Dragons/_Config/Tag Taxonomy.md`

All paths below are relative to `~/docs/Documents/2. Areas/2.2 Dungeons & Dragons/`.

## Workflow

### 1. Gather Campaign Info

If `$ARGUMENTS` provides a campaign name, use it. Otherwise, ask for:

- **Campaign name** — used as directory name and display name
- **Setting** — e.g., "Forgotten Realms", "Barovia", "homebrew"
- **Source** — "homebrew" or published adventure name (e.g., "Curse of Strahd", "Lost Mine of Phandelver")
- **Starting party level** — integer, default 1

### 2. Create Directory Tree

Create the full campaign structure under `1. Campaigns/{campaign-name}/`:

```
1. Campaigns/{campaign-name}/
├── Campaign.md
├── Sessions/
├── Adventures/
├── Party/
├── State/
│   ├── World Clock.md
│   ├── Active Quests.md
│   ├── Plot Threads.md
│   └── Snapshots/
└── Combat/
```

Create directories by writing placeholder or actual files. Empty directories need at least one file — the State/ files satisfy this for State/, but Sessions/, Adventures/, Party/, and Combat/ need their respective files created during play. Create them as empty dirs via mkdir if the tool supports it, or note they will be populated during play.

### 3. Create Campaign.md

Write `1. Campaigns/{campaign-name}/Campaign.md` using the campaign schema:

```yaml
---
type: campaign
name: "{campaign-name}"
Created: {today}
Updated: {today}
status: active
system: "D&D 5e"
setting: "{setting}"
party-level: {level}
session-count: 0
source: "{source}"
tags:
  - "#dnd/campaign"
  - "#dnd/campaign/{name-slug}"
---
```

Body sections:

```markdown
# {Campaign Name}

## Overview

{Brief description — if published adventure, a spoiler-free premise. If homebrew, ask user for a 1-2 sentence pitch.}

## House Rules

- None yet

## Party

```dataview
TABLE player, race, class, level
FROM "{relative-path-to-Party/}"
WHERE type = "pc"
SORT name ASC
```

## Session Log

```dataview
TABLE session-number AS "#", date-played AS "Date", game-day-start AS "Day Start", game-day-end AS "Day End"
FROM "{relative-path-to-Sessions/}"
WHERE type = "session"
SORT session-number DESC
```

## Quick Links

- [[World Clock]]
- [[Active Quests]]
- [[Plot Threads]]
```

### 4. Create World Clock

Write `1. Campaigns/{campaign-name}/State/World Clock.md`:

```yaml
---
type: world-clock
campaign: "[[Campaign]]"
current-day: 1
current-time: morning
calendar-date: ""
season: ""
weather: ""
---
```

Body:

```markdown
# World Clock

## Scheduled Events

| Day | Time | Event | Triggered |
|-----|------|-------|-----------|

## Time Log

- **Day 1, morning:** Campaign begins.
```

### 5. Create Active Quests Dashboard

Write `1. Campaigns/{campaign-name}/State/Active Quests.md`:

```yaml
---
type: config
campaign: "[[Campaign]]"
tags:
  - "#dnd/config"
---
```

Body:

```markdown
# Active Quests

## Active

```dataview
TABLE quest-giver AS "Giver", priority AS "Priority", game-day-deadline AS "Deadline", reward AS "Reward"
FROM "{relative-path-to-State/}"
WHERE type = "quest" AND status = "active"
SORT priority ASC
```

## Completed

```dataview
TABLE quest-giver AS "Giver", priority AS "Priority", reward AS "Reward"
FROM "{relative-path-to-State/}"
WHERE type = "quest" AND status = "completed"
SORT file.name ASC
```

## Failed / Abandoned

```dataview
TABLE quest-giver AS "Giver", status AS "Status"
FROM "{relative-path-to-State/}"
WHERE type = "quest" AND (status = "failed" OR status = "abandoned")
SORT file.name ASC
```
```

### 6. Create Plot Threads Dashboard

Write `1. Campaigns/{campaign-name}/State/Plot Threads.md`:

```yaml
---
type: config
campaign: "[[Campaign]]"
tags:
  - "#dnd/config"
---
```

Body:

```markdown
# Plot Threads

## Active Threads

```dataview
TABLE thread-type AS "Type", urgency AS "Urgency", status AS "Status"
FROM "{relative-path-to-State/}"
WHERE type = "plot-thread" AND (status = "seed" OR status = "active" OR status = "climax")
SORT urgency DESC
```

## Resolved Threads

```dataview
TABLE thread-type AS "Type", introduced-session AS "Introduced"
FROM "{relative-path-to-State/}"
WHERE type = "plot-thread" AND status = "resolved"
SORT file.name ASC
```
```

### 7. Published Adventure Setup (Conditional)

If source is not "homebrew":

- Ask which adventure book (confirm the name)
- Create `1. Campaigns/{campaign-name}/Adventures/{book-name}.md`:

```yaml
---
type: resource
Created: {today}
Updated: {today}
campaign: "[[Campaign]]"
tags:
  - "#dnd/campaign"
  - "#dnd/lore"
---
```

Body:

```markdown
# {Book Name}

## Overview

{Ask user for or look up the adventure premise — keep spoiler-free for player-facing notes}

## Chapters

{List chapter names if known, or leave as placeholder}

## Key NPCs

{To be populated during play}

## Key Locations

{To be populated during play}

## Modifications

{Track any DM changes to the published adventure here}
```

### 8. Party Setup (Interactive)

Ask: "Want to set up PCs now?"

If yes, for each PC ask:
- Player name (real person)
- Character name
- Race
- Class
- Subclass (if applicable at starting level)
- Level (default to campaign party-level)
- Stats (array of 6, or roll/point-buy later)
- HP max
- AC

Create each PC file at `1. Campaigns/{campaign-name}/Party/{Character Name}.md` using the PC schema:

```yaml
---
type: pc
name: "{character-name}"
player: "{player-name}"
campaign: "[[Campaign]]"
race: "{race}"
class: "{class}"
subclass: "{subclass}"
level: {level}
hp-max: {hp}
ac: {ac}
stats:
  str: {str}
  dex: {dex}
  con: {con}
  int: {int}
  wis: {wis}
  cha: {cha}
proficiency-bonus: {bonus}
status: active
tags:
  - "#dnd/pc"
---
```

Body:

```markdown
# {Character Name}

## Features & Traits

{List racial and class features for their level}

## Spells Known

{If spellcaster, list known/prepared spells}

## Equipment

{Starting equipment from class + background}

## Inventory

{Other items}

## Backstory

{Ask player or leave placeholder}

## Relationships

{To be populated during play}

## Notes
```

Repeat for each PC. When done, confirm party roster.

### 9. Completion Report

Present:
- Campaign directory path
- Files created (list all)
- Quick links to Campaign.md, World Clock, Active Quests
- Next steps: "Run `/dnd:plan` to plan your first session, or `/dnd:play` to jump straight in."

## Edge Cases

- **Campaign name already exists:** Warn and ask to pick a different name or confirm overwrite
- **No source provided:** Default to "homebrew"
- **User skips party setup:** That's fine, PCs can be added later
- **Published adventure not recognized:** Create the adventure file anyway with placeholder content
