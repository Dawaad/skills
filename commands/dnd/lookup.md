---
name: "dnd:lookup"
description: "Quick reference lookup for D&D 5e content. Checks local cache first, falls back to dnd5eapi.co, transforms to vault markdown, and presents a clean stat block."
---

# /dnd:lookup — Quick Reference Lookup

Fetch and display D&D 5e official content (monsters, spells, equipment, magic items). Caches results as vault markdown for future lookups.

## Input

$ARGUMENTS — expects `{type} {name}` (e.g., `monster adult red dragon`, `spell fireball`, `item longsword`, `magic-item cloak of protection`)

## Setup

1. Read the domain CLAUDE.md at `2. Areas/2.2 Dungeons & Dragons/CLAUDE.md`
2. Read entity schemas from `2. Areas/2.2 Dungeons & Dragons/_Config/Tag Taxonomy.md`

All paths below are relative to `~/docs/Documents/2. Areas/2.2 Dungeons & Dragons/`.

## Workflow

### 1. Parse Arguments

Extract type and name from `$ARGUMENTS`:

| Input Pattern | Type | API Endpoint |
|---------------|------|-------------|
| `monster {name}` | monster | `/api/2014/monsters/{index}` |
| `spell {name}` | spell | `/api/2014/spells/{index}` |
| `item {name}` or `equipment {name}` | equipment | `/api/2014/equipment/{index}` |
| `magic-item {name}` or `magic item {name}` | magic-item | `/api/2014/magic-items/{index}` |
| `condition {name}` | condition | `/api/2014/conditions/{index}` |

If type is ambiguous or missing, ask the user.

### 2. Build API Index

Convert name to API index format:
- Lowercase everything
- Replace spaces with hyphens
- Strip apostrophes and special characters
- Examples: `Adult Red Dragon` -> `adult-red-dragon`, `Mage's Sword` -> `mages-sword`

### 3. Check Local Cache

Search the appropriate cache directory for an existing file with matching `api-index:` in frontmatter:

| Type | Cache Directory |
|------|----------------|
| monster | `3. Bestiary/Official/` |
| spell | `4. Spellbook/Official/` |
| equipment | `5. Armory/Equipment/` |
| magic-item | `5. Armory/Magic Items/` |

Use Grep to search for `api-index: "{index}"` in the target directory.

If found, read and present it. Skip to step 6.

### 4. Fetch from API

If not cached, use WebFetch to GET `https://www.dnd5eapi.co/api/2014/{type}/{index}`.

If the API returns 404, try a search: `https://www.dnd5eapi.co/api/2014/{type}?name={url-encoded-name}`. Present matching results and ask the user to pick one.

### 5. Transform and Cache

Transform the JSON response to vault markdown using the schemas below, then write to the cache directory. Filename: `{Title Case Name}.md` (e.g., `Adult Red Dragon.md`).

#### Monster Transformation

Map API JSON fields to frontmatter:

```
API Field              -> Frontmatter Field
-----------------------------------------------
index                  -> api-index
name                   -> name
size                   -> size
type                   -> creature-type
alignment              -> alignment  (join array or use string directly)
challenge_rating       -> cr
xp                     -> xp
armor_class[0].value   -> ac
armor_class[0].type    -> ac-type
hit_points             -> hp
hit_points_roll        -> hit-dice
speed.walk             -> speed.walk
speed.fly              -> speed.fly       (omit if absent)
speed.swim             -> speed.swim      (omit if absent)
speed.burrow           -> speed.burrow    (omit if absent)
speed.climb            -> speed.climb     (omit if absent)
strength               -> stats.str
dexterity              -> stats.dex
constitution           -> stats.con
intelligence           -> stats.int
wisdom                 -> stats.wis
charisma               -> stats.cha
proficiencies[]        -> saving-throws[] and skills[] (separate by proficiency.index prefix: "saving-throw-" vs "skill-")
damage_resistances[]   -> damage-resistances
damage_immunities[]    -> damage-immunities
condition_immunities[] -> condition-immunities (use .name field)
senses                 -> senses (format as "darkvision 60 ft., passive Perception 14")
languages              -> languages
```

Always set:
- `type: monster`
- `source: official`
- `tags: ["#dnd/monster"]`

Body sections from API:

- **## Traits** — from `special_abilities[]`: format each as `### {name}\n{desc}`
- **## Actions** — from `actions[]`: format each as `### {name}\n{desc}`. For attacks, include to-hit and damage from `damage[]` array.
- **## Reactions** — from `reactions[]` if present
- **## Legendary Actions** — from `legendary_actions[]` if present. Include the preamble: "The {name} can take {count} legendary actions..."
- **## Lair Actions** — omit unless present in API response

Add `(SRD/API)` source citation at the bottom.

#### Spell Transformation

Map API JSON fields to frontmatter:

```
API Field              -> Frontmatter Field
-----------------------------------------------
index                  -> api-index
name                   -> name
level                  -> spell-level (0 for cantrips)
school.name            -> school
casting_time           -> casting-time
range                  -> range
duration               -> duration
concentration          -> concentration
ritual                 -> ritual
components[]           -> components (join as "V, S, M")
material               -> material (the material component description)
classes[].name         -> classes (array of class names)
```

Always set:
- `type: spell`
- `source: official`
- `tags: ["#dnd/spell"]`

Body sections:

- **## Description** — from `desc[]` (join paragraphs)
- **## At Higher Levels** — from `higher_level[]` if present

#### Equipment Transformation

Map API JSON fields to frontmatter:

```
API Field              -> Frontmatter Field
-----------------------------------------------
index                  -> api-index
name                   -> name
equipment_category.name -> item-type
cost.quantity + cost.unit -> cost (format as "25 gp")
weight                 -> weight
damage.damage_dice     -> damage (if weapon)
damage.damage_type.name -> damage-type (if weapon)
armor_class.base       -> ac-base (if armor)
properties[].name      -> properties (array)
```

Always set:
- `type: item`
- `source: official`
- `rarity: common`
- `attunement: false`
- `tags: ["#dnd/item"]`

Body: `## Description` from `desc[]`, `## Properties` listing weapon/armor properties.

#### Magic Item Transformation

Map API JSON fields to frontmatter:

```
API Field              -> Frontmatter Field
-----------------------------------------------
index                  -> api-index
name                   -> name
rarity.name            -> rarity (lowercase, spaces to hyphens)
equipment_category.name -> item-type
desc[]                 -> body description
```

Check `desc[]` text for "requires attunement" to set:
- `attunement: true`
- `attunement-requirement:` extract the parenthetical if present (e.g., "by a spellcaster")

Always set:
- `type: item`
- `source: official`
- `tags: ["#dnd/item"]`

Body: `## Description` from `desc[]` (join paragraphs). Parse out charges, properties, and effects into sub-sections if the description is long.

### 6. Update API Cache Index

After writing a new cached file, append a row to the appropriate table in `_Config/API Cache Index.md`:

| Type | Table | Row Format |
|------|-------|------------|
| monster | `## Monsters` | `\| {api-index} \| {name} \| {cr} \| {today's date} \|` |
| spell | `## Spells` | `\| {api-index} \| {name} \| {spell-level} \| {today's date} \|` |
| equipment | `## Equipment` | `\| {api-index} \| {name} \| {item-type} \| {today's date} \|` |
| magic-item | `## Magic Items` | `\| {api-index} \| {name} \| {rarity} \| {today's date} \|` |

### 7. Present Result

Display the entity to the user in a clean, readable stat-block format:

**For monsters:**
```
## {Name}
*{Size} {creature-type}, {alignment}*

**AC** {ac} ({ac-type}) | **HP** {hp} ({hit-dice}) | **Speed** {speeds}

| STR | DEX | CON | INT | WIS | CHA |
|-----|-----|-----|-----|-----|-----|
| {str} ({mod}) | {dex} ({mod}) | ... |

**Saving Throws** {list}
**Skills** {list}
**Senses** {senses}
**Languages** {languages}
**CR** {cr} ({xp} XP)

{traits, actions, reactions, legendary actions}
```

**For spells:**
```
## {Name}
*{level}-level {school}* (or *{school} cantrip*)

**Casting Time:** {casting-time}
**Range:** {range}
**Components:** {components} ({material})
**Duration:** {concentration prefix}{duration}
**Classes:** {classes}

{description}

**At Higher Levels.** {higher_level}
```

**For items/magic items:**
```
## {Name}
*{item-type}, {rarity}* {attunement note}

{description and properties}
```

## Edge Cases

- **Name not found:** Try the search endpoint, present options
- **Multiple matches:** List all and ask user to pick
- **API down:** Report the error, suggest checking dnd5eapi.co status
- **Already cached:** Skip fetch, present cached version, note "(from cache)"
- **Homebrew content:** This skill only handles official API content. For homebrew, direct user to create manually or use a different skill.
