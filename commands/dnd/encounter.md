---
name: "dnd:encounter"
description: "Encounter generation -- random encounters from tables or designed encounters balanced for party level. Pre-builds combat-ready encounter files with stat blocks, terrain, and narrative hooks."
---

# /dnd:encounter -- Encounter Generation

Two modes: generate random encounters from environment-based tables, or design balanced encounters with full narrative and tactical setup.

## Input

$ARGUMENTS -- expects one of:
- `--random environment:{type} tier:{1-4}` -- random encounter generation
- `--designed` -- interactive encounter builder
- `--random` -- random with prompts for environment and tier
- Empty -- ask which mode

## Setup

1. Read the domain CLAUDE.md at `2. Areas/2.2 Dungeons & Dragons/CLAUDE.md`
2. Read entity schemas from `2. Areas/2.2 Dungeons & Dragons/_Config/Tag Taxonomy.md`
3. **Read combat strategy from `2. Areas/2.2 Dungeons & Dragons/_Config/Combat Strategy.md`** — use player threat profiles to calibrate difficulty, assign enemy archetypes, and generate environmental/interactable elements.

All paths below are relative to `~/docs/Documents/2. Areas/2.2 Dungeons & Dragons/`.

---

## Random Mode

### 1. Parse Parameters

Extract from $ARGUMENTS:

**Environment type** (if not provided, ask):
- arctic, coastal, desert, forest, grassland, hill, mountain, swamp, underdark, underwater, urban

**Tier** (if not provided, derive from party level):
- Tier 1: Levels 1-4 (CR 0-2)
- Tier 2: Levels 5-10 (CR 3-7)
- Tier 3: Levels 11-16 (CR 8-14)
- Tier 4: Levels 17-20 (CR 15+)

If tier not provided, read party level from Campaign.md or active PC files.

### 2. Find or Create Encounter Table

Search `3. Bestiary/Encounter Tables/` for a table matching the environment and tier.

**If table exists:**
- Read it
- Proceed to rolling

**If no table exists:**
- Generate one using dnd5eapi.co monster data
- Fetch monsters appropriate to the environment and CR range for the tier
- Build a d20 encounter table with weighted entries:

```markdown
---
type: config
environment: "{environment}"
tier: {tier}
cr-range: "{min}-{max}"
Created: {today}
tags:
  - "#dnd/encounter"
  - "#dnd/config"
---

# {Environment} Encounters -- Tier {N}

| d20 | Encounter | CR | Type |
|-----|-----------|-----|------|
| 1-2 | {peaceful/flavor encounter} | -- | exploration |
| 3-5 | {minor threat} x{count} | {total CR} | combat |
| 6-8 | {standard encounter} | {total CR} | combat |
| 9-10 | {social encounter with NPC} | -- | social |
| 11-13 | {moderate combat} | {total CR} | combat |
| 14-15 | {environmental hazard or puzzle} | -- | exploration |
| 16-17 | {harder combat} | {total CR} | combat |
| 18-19 | {discovery or treasure} | -- | exploration |
| 20 | {boss-level encounter for tier} | {total CR} | combat |
```

Write the table to `3. Bestiary/Encounter Tables/{Environment} Tier {N}.md`.

### 3. Roll on the Table

Roll a d20. Announce the roll and result:

```
Random Encounter Roll: d20({roll})
Result: {encounter description}
Type: {combat/social/exploration}
```

### 4. Present the Encounter

For **combat encounters:**
- List monsters with names and CRs
- Spawn `dnd-monster-manual` agent to fetch/verify stat blocks
- Suggest tactical setup (terrain, distance, surprise possibility)
- Show difficulty rating for the party

For **social encounters:**
- Describe the NPC or group encountered
- Suggest their disposition and motivation
- Note what they know or want

For **exploration encounters:**
- Describe the discovery, hazard, or environmental feature
- Note any skill checks involved and DCs
- Describe rewards or consequences

### 5. Offer to Run

Ask DM:
- "Run this encounter now?" -> If combat, hand off to `/dnd:combat`. If social, set up NPC interaction.
- "Reroll?" -> Roll again on the same table
- "Skip?" -> No encounter, continue with whatever was happening
- "Save for later?" -> Write as a planned encounter file

---

## Designed Mode

### 1. Gather Encounter Parameters

Ask for:

- **Name** -- descriptive encounter name (e.g., "Ambush at Cragmaw Bridge")
- **Location** -- where it takes place (wiki link)
- **Difficulty target** -- easy, medium, hard, deadly
- **Encounter type** -- combat, social, exploration, puzzle, trap
- **Narrative hook** -- why is this happening? What leads to it?
- **Campaign** -- which campaign

### 2. Read Party Data

Read all PC files for the campaign to determine:
- Party size
- Average party level
- Party composition (melee, ranged, spellcasters, healers)

### 3. Calculate XP Thresholds

Using DMG encounter building rules, calculate party XP thresholds:

| PC Level | Easy | Medium | Hard | Deadly |
|----------|------|--------|------|--------|
| Per DMG table per level |

Multiply per-PC threshold by party size for total party thresholds.

Target the requested difficulty bracket.

### 4. Build the Encounter

**For combat encounters:**

Spawn `dnd-monster-manual` agent to select CR-appropriate monsters:
- Choose monsters that fit the location theme
- Mix monster types for interesting tactics (one bruiser + ranged support, spellcaster + melee screen)
- Verify the adjusted XP falls within the target difficulty bracket
- Fetch and cache all stat blocks

Design terrain and tactical setup:
- Starting positions and distances
- Cover and obstacles
- Environmental hazards (unstable ground, fire, water, elevation)
- Lighting conditions
- Special terrain features that affect movement or combat

**Assign enemy archetypes** from Combat Strategy config:
- Each enemy group gets an archetype (Berserker, Skirmisher, Controller, Assassin, Tactician, Artillery, Protector)
- Mix archetypes within a single encounter for depth
- Choose archetypes that create interesting challenges for the party composition (consult player threat profiles)

**Generate environmental elements** (MANDATORY — minimum 2 per combat encounter):
- At least 1 destructible object or hazard zone
- At least 1 glaring interaction (obvious, high-reward, low-barrier action)
- At least 1 element should favor ranged/magic users
- At least 1 element should be usable by anyone (no skill check required)
- Follow the templates in Combat Strategy config for element design
- Describe interactables with vivid, unmissable visual cues

**For social encounters:**
- Identify NPCs involved (link existing or note new ones needed)
- Define NPC goals and knowledge
- Outline possible outcomes and consequences
- Set DCs for relevant social checks

**For exploration encounters:**
- Describe the challenge or discovery
- Define skill checks and DCs needed
- Describe success and failure outcomes
- Note time cost and resource expenditure

**For puzzle encounters:**
- Describe the puzzle setup
- Define the solution (or multiple valid solutions)
- Set hint structure (what investigation/arcana/etc. checks reveal)
- Define consequences of failure and rewards for success

**For trap encounters:**
- Detection DC (Investigation or Perception)
- Trigger mechanism
- Effect (damage type and amount, conditions applied, area)
- Disarm DC (Thieves' tools, Arcana, etc.)
- What happens on a failed disarm attempt

### 5. Write Encounter File

Write to `1. Campaigns/{campaign}/Combat/{Encounter Name}.md`:

```yaml
---
type: encounter
name: "{name}"
campaign: "[[Campaign]]"
session:                        # to be filled during play
game-day:                       # to be filled during play
location: "[[{location}]]"
status: planned
difficulty: "{difficulty}"
encounter-type: "{type}"
party-level: {average level}
party-size: {party size}
monsters:                       # for combat encounters
  - name: "{monster}"
    count: {count}
    api-index: "{index}"
tags:
  - "#dnd/encounter"
---
```

Body:

```markdown
# {Encounter Name}

## Setup

### Narrative Hook
{Why this encounter happens, what leads to it}

### Terrain
{Description of the environment, tactical features, lighting, hazards}

### Starting Positions
{Where combatants/NPCs begin, distances, sight lines}

## Enemy Archetypes

{For combat encounters -- assign each enemy group an archetype from Combat Strategy}

| Enemy | Archetype | Behavior Summary |
|-------|-----------|-----------------|
| {enemy group} | {archetype} | {1-line behavior description} |

## Environmental Elements

{MANDATORY for combat encounters -- minimum 2 elements}

### {Element 1 Name} ({map position})
- **Visual Cue:** {What makes this obviously interactive}
- **Interaction:** {Action type, skill check, DC}
- **Effect:** {Damage, condition, terrain change}
- **One-time or Repeatable:** {usage}

### {Element 2 Name} ({map position})
- **Visual Cue:** {Unmissable description}
- **Interaction:** {Action type, skill check, DC}
- **Effect:** {Damage, condition, terrain change}
- **One-time or Repeatable:** {usage}

## {Type-specific sections}

{For combat: monster tactics, phase transitions, morale/retreat conditions}
{For social: NPC motivations, conversation flow, DC table}
{For exploration: challenge description, skill checks, outcomes}
{For puzzle: puzzle description, solution, hints}
{For trap: detection, trigger, effect, disarm}

## Possible Outcomes

- **Success:** {what happens if party succeeds}
- **Partial:** {what happens with mixed results}
- **Failure:** {what happens if party fails}

## Consequences

{How this encounter connects to the larger story -- quest advancement, NPC reactions, world state changes}

## Loot

{Pre-determined loot or "Roll after combat"}
```

### 6. Confirm and Offer Next Steps

Present the encounter summary:
- Name, type, difficulty
- Monsters (if combat) with CR breakdown
- Key tactical features
- Narrative hook

Ask:
- "Run this now?" -> hand off to appropriate skill
- "Modify?" -> adjust specific elements
- "Save for session plan?" -> it's already written, reference in planning

## Edge Cases

- **No monsters fit the environment/CR:** Adjust slightly outside the exact bracket, or reskin a close match (a wolf can become a winter wolf pup in arctic terrain).
- **Party composition makes standard difficulty misleading:** Warn DM (e.g., "Your party has no healers -- 'hard' may feel 'deadly'").
- **Encounter table already full (d20):** Offer to expand to d100 or create a variant table for the same environment.
- **Mixed encounter types:** An encounter can be combat + social (enemies who can be talked down). Build both paths.
- **Encounter for travel:** If called from `/dnd:world --travel-to`, use the travel route terrain instead of destination terrain.
