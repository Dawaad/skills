---
name: "dnd:world"
description: "World building and location management. Create locations with atmospheric descriptions, run travel sequences with random encounters and time tracking, or describe existing locations adapted to current state."
---

# /dnd:world -- World Building & Location Management

Three modes: create new locations, travel between locations with time and encounter mechanics, or describe existing locations with state-aware atmosphere.

## Input

$ARGUMENTS -- expects one of:
- `--create` -- create a new location
- `--travel-to {destination}` -- travel from current location to destination
- `--describe {location-name}` or just `{location-name}` -- describe an existing location (default)

## Setup

1. Read the domain CLAUDE.md at `2. Areas/2.2 Dungeons & Dragons/CLAUDE.md`
2. Read entity schemas from `2. Areas/2.2 Dungeons & Dragons/_Config/Tag Taxonomy.md`

All paths below are relative to `~/docs/Documents/2. Areas/2.2 Dungeons & Dragons/`.

## Mode Detection

Parse `$ARGUMENTS`:
- `--create` -> create mode
- `--travel-to` or `--travel` -> travel mode (extract destination name)
- `--describe` or bare location name -> describe mode
- If no arguments, ask what the user wants to do

---

## Create Mode

### 1. Gather Location Details

Ask for (or extract from $ARGUMENTS):

- **Name** -- location name
- **Region** -- parent location as wiki link (e.g., `[[Sword Coast]]`, `[[Barovia]]`)
- **Location type** -- continent, region, city, town, village, dungeon, building, wilderness, plane
- **Description** -- brief description of the place (2-3 sentences)
- **Key features** -- 3-5 notable features (landmarks, resources, hazards)
- **Danger level** -- safe, low, moderate, high, deadly
- **Controlling faction** -- wiki link if applicable
- **Campaign** -- which campaign, or omit for world-level
- **Population** -- approximate, if applicable

### 2. Generate Read-Aloud Text

Generate atmospheric, sensory read-aloud text for when the party first arrives. Guidelines:

- 3-5 sentences, designed to be read aloud at the table
- Hit at least 3 senses (sight, sound, smell, touch, taste)
- Set the mood appropriate to danger level and location type
- Include one specific detail that makes this location memorable
- Do NOT include mechanical information in the read-aloud

Format as a blockquote:
```markdown
> {Read-aloud text in italicized narrative voice}
```

### 3. Generate NPCs Present

Based on the location type and description:

- List 2-4 NPCs who would logically be present
- For each, check if they already exist in `2. World/NPCs/`
- If they exist, link them: `[[{NPC Name}]] -- {role at this location}`
- If they don't exist, list them with a note: `{NPC Name} -- {role} (not yet created)`
- Offer to create missing NPCs via `/dnd:npc --create`

### 4. Generate Connections

Generate connections to other locations:

- 2-4 connected locations with travel details
- For each connection:
  - Destination (wiki link if exists, plain name if not)
  - Distance (miles)
  - Travel time by foot (24 mi/day), horse (30 mi/day)
  - Route description (road, trail, wilderness, river)
  - Danger level of the route

Format as:
```markdown
| Destination | Distance | By Foot | By Horse | Route | Danger |
|-------------|----------|---------|----------|-------|--------|
```

### 5. Dungeon Type Check

If `location-type` is `dungeon`:

- Spawn the `dnd-dungeon-architect` agent to generate:
  - Room map / layout description
  - Room-by-room key with encounters, traps, and treasure
  - Boss encounter
  - Environmental hazards
- Incorporate the dungeon content into the location file's body

### 6. Write Location File

Determine the file path based on region:
- If region has an existing directory under `2. World/Locations/`, use it
- Otherwise create the region directory: `2. World/Locations/{region}/`

Write to `2. World/Locations/{region}/{Name}.md`:

```yaml
---
type: location
name: "{name}"
campaign: "[[{campaign}]]"      # omit if world-level
region: "[[{region}]]"
location-type: "{type}"
population: {population}         # omit if N/A
controlling-faction: "[[{faction}]]"  # omit if none
status: "{appropriate status}"
danger-level: "{danger-level}"
source: "homebrew"
tags:
  - "#dnd/location"
---
```

Body:

```markdown
# {Name}

## Description

> {Read-aloud text}

{Additional DM-only description -- history, hidden details, what's really going on}

## Key Features

- **{Feature 1}** -- {description}
- **{Feature 2}** -- {description}
- **{Feature 3}** -- {description}

## NPCs Present

{Generated NPC list with wiki links}

## State History

- **Day {current-day}:** Location created/discovered.

## Connections

{Generated connections table}

## Random Encounter Table

{If danger-level is not "safe", generate a simple d6 or d8 encounter table appropriate to the terrain and danger level. Otherwise omit.}

## Shops & Services

{If location-type is city/town/village, generate 2-3 shops/services. Otherwise omit.}
```

### 7. Confirm Creation

Report: file path, key features, NPCs present, connections, danger level.

---

## Travel Mode

### 1. Identify Origin and Destination

**Origin:** Read World Clock or recent session state to determine current party location. If unclear, ask the DM.

**Destination:** Parse from $ARGUMENTS. Search `2. World/Locations/` for a matching file.

- If destination file exists, read it
- If destination file doesn't exist, ask if the user wants to create it first (spawn create mode), or describe it on the fly

### 2. Read Both Location Files

Read origin and destination location files to get:
- Distance and route info from the Connections table (check both files)
- Danger levels for the route
- Any relevant NPCs or state

If no connection exists between the two locations, ask the DM for distance and route type.

### 3. Calculate Travel Time

Determine travel mode (ask DM if not obvious):

| Mode | Speed | Notes |
|------|-------|-------|
| On foot | 24 miles/day | Standard pace |
| On horseback | 30 miles/day | Assumes riding horses |
| Forced march | 30 miles/day on foot | CON save DC 10 + hours beyond 8; failure = 1 level exhaustion per failed save |
| Cart/wagon | 16 miles/day | Slow but can carry cargo |
| Sailing | 48 miles/day | If water route available |

Travel days = ceil(distance / speed per day)

If forced march, note exhaustion risk and resolve saves if the DM chooses this option.

### 4. Advance World Clock

Read `State/World Clock.md`. Advance:
- `current-day` by the number of travel days
- `current-time` to the appropriate time of arrival (if 1 day, arrive evening; if partial day, calculate)

Append to Time Log:
```
- **Day {start-day} to Day {end-day}:** Traveled from [[{Origin}]] to [[{Destination}]] ({distance} miles, {mode}).
```

Write the updated World Clock immediately.

### 5. Check for Random Encounters

For each day of travel, roll for random encounters.

Determine the encounter threshold based on the route's danger level:

| Danger Level | Encounter on d20 roll of... |
|--------------|---------------------------|
| Safe | 18+ (15% chance) |
| Low | 15+ (30% chance) |
| Moderate | 12+ (45% chance) |
| High | 8+ (65% chance) |
| Deadly | 5+ (80% chance) |

For each travel day:
- Roll a d20
- Announce the roll and whether an encounter occurs
- If encounter triggered:
  - Determine time of day (roll d4: 1=morning, 2=midday, 3=evening, 4=night)
  - Select appropriate encounter based on terrain type and party level
  - Spawn `dnd-monster-manual` agent for monster stat blocks if combat encounter
  - Narrate the encounter setup
  - Ask DM how to proceed (fight, flee, negotiate, etc.)
  - If combat, hand off to `/dnd:combat`
  - After resolution, continue travel

### 6. Describe Arrival

When the party arrives at the destination:

- Read the destination location file (re-read for fresh state)
- Read World Clock for time of day, weather, season
- Generate arrival description adapted to:
  - Time of day (morning light, torchlit evening, etc.)
  - Weather and season
  - Party's condition (any exhaustion from forced march, injuries from encounters)
  - Location's current state (status field -- thriving, declining, ruined, etc.)

Present the read-aloud text from the location file, adapted for the arrival context.

### 7. Update State

- Update party's current location in any active tracking
- Append to destination location's State History:
```
- **Day {arrival-day}:** Party arrived from [[{Origin}]].
```

Report: travel time, encounters (if any), current state, what they see.

---

## Describe Mode

### 1. Find and Read Location

Search `2. World/Locations/` for the location name. Read the full file.

If not found, offer to create it.

### 2. Read Supporting Context

- Read World Clock for current time of day, weather, season
- Read NPC files for NPCs listed in `## NPCs Present` (check their current status -- are they alive? Still here?)
- Read the location's State History for recent changes

### 3. Generate State-Aware Description

Generate a description that adapts to the current world state:

- **Time of day:** Dawn has different light than midnight. Markets are active at midday, closed at night.
- **Weather/season:** Rain, snow, heat all affect the atmosphere.
- **State history:** If the location was recently attacked, show the damage. If recently liberated, show the rebuilding.
- **NPC presence:** Mention visible NPCs and what they're doing.
- **Status field:** A "declining" city looks different from a "thriving" one.

Present as atmospheric narrative, NOT as a data dump. The description should feel like a scene being set at the table.

### 4. List Available Actions

After the description, present what the party can do here:

- **NPCs to interact with:** List present NPCs with brief context
- **Shops/services:** If available, list what they can buy/sell/repair
- **Connections:** Where they can travel from here
- **Points of interest:** Key features that can be investigated
- **Quests available:** Any NPCs with quest hooks in their Knowledge section

Format as:
```markdown
### What You Can Do Here

- **Talk to** [[{NPC}]] -- {what they might want/know}
- **Visit** {shop/service} -- {what's available}
- **Travel to** [[{destination}]] -- {distance, travel time}
- **Investigate** {feature} -- {what it might reveal}
```

## Edge Cases

- **Location not found:** Broad search with Grep. If still not found, offer create mode.
- **Travel with no established route:** Ask DM for distance and terrain type, then proceed normally.
- **Travel through multiple zones of different danger:** Roll separately for each zone with appropriate thresholds.
- **Party splits during travel:** Track each group separately, ask DM who goes where.
- **Destination is a dungeon:** After arrival description, note that exploring the dungeon should use the dungeon's room-by-room key.
- **Location has been destroyed:** State History should reflect this. Describe the ruins, not the original state.
- **NPCs listed as present are actually dead:** Check NPC status field. Remove dead NPCs from the present list and note the discrepancy in the description.
