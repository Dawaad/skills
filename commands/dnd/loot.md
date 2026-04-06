---
name: "dnd:loot"
description: "Loot generation and shopping. Generate context-appropriate treasure drops after combat, run interactive shopping sessions with NPC shopkeepers, or roll on custom loot tables."
---

# /dnd:loot -- Loot Generation & Shopping

Three modes: generate loot drops from combat, run interactive shopping with NPC shopkeepers and haggling, or roll on custom loot tables.

## Input

$ARGUMENTS -- expects one of:
- `--drop {encounter-name}` or `--drop` -- generate loot from a combat encounter
- `--shop {location-name}` -- run an interactive shopping session
- `--roll {table-name}` -- roll on a specific loot table
- Empty -- ask DM what mode they want

## Setup

1. Read the domain CLAUDE.md at `2. Areas/2.2 Dungeons & Dragons/CLAUDE.md`
2. Read entity schemas from `2. Areas/2.2 Dungeons & Dragons/_Config/Tag Taxonomy.md`

All paths below are relative to `~/docs/Documents/2. Areas/2.2 Dungeons & Dragons/`.

## Mode Detection

Parse `$ARGUMENTS`:
- `--drop` -> drop mode
- `--shop` -> shop mode
- `--roll` -> roll mode
- If coming from `/dnd:combat` (post-combat context), default to drop mode
- Otherwise, ask

---

## Drop Mode

### 1. Load Encounter Context

If encounter name provided:
- Search `Combat/` in the active campaign for the encounter file
- Read it -- extract monsters, difficulty, location, outcome

If no encounter name:
- Check for the most recently resolved encounter file (`status: resolved`)
- If none found, ask DM: "What did you fight? Give me CR and monster types."

### 2. Read Location Context

Read the encounter's location file for thematic context:
- A forest bandit encounter yields different loot than a dragon's hoard
- A dungeon has different treasure than a roadside ambush
- Rich/poor areas affect coin amounts

### 3. Generate Loot

Spawn `dnd-loot-dropper` agent with context:
- Monster types and CRs
- Encounter difficulty
- Location type and theme
- Party level

The agent generates narrative-appropriate loot following DMG treasure tables as guidelines:

**Individual treasure** (per-monster, low-CR encounters):
- Coin amounts (CP, SP, GP, PP)
- Mundane items carried

**Hoard treasure** (significant encounters, boss fights):
- Coin piles
- Gems and art objects
- Magic items (rarity appropriate to CR)
- Unique/story items

### 4. Present Loot to DM

Display the generated loot:

```markdown
## Loot Drop -- {Encounter Name}

### Coins
- {X} GP, {Y} SP, {Z} CP

### Items
- {Item 1} -- {brief description, value}
- {Item 2} -- {brief description, value}

### Magic Items
- **{Magic Item Name}** ({rarity}) -- {brief description}

### Total Value: ~{X} GP
```

Ask DM: "Modify anything before distributing?"

### 5. Distribute to PCs

Ask DM how to split:
- **Even split:** Divide coins equally, assign items as DM directs
- **Specific distribution:** DM assigns each item to a PC
- **Party fund:** Coins go to shared pool (track in a party inventory note)

For each PC receiving items:
- Read the PC file
- Append items to `## Inventory` section
- Add coins to their gold total (if tracked in the file)

### 6. Update Encounter File

Append loot details to the encounter file's `## Loot` section.

---

## Shop Mode

### 1. Load Shop Context

Read the location file for the specified location. Find `## Shops & Services` section.

If no shops listed:
- Ask DM: "No shops listed at {location}. Want to add one? What type?"
- If yes, create the shop entry in the location file

### 2. Load Shopkeeper NPC

For the chosen shop, identify the shopkeeper NPC:
- If listed in the shop entry, read their NPC file
- If no shopkeeper exists, offer to create one via `/dnd:npc --create`

Key NPC data for shopping:
- `disposition` -- affects pricing and willingness to deal
- `relationship-score` -- affects pricing
- Personality traits -- affects negotiation style

### 3. Generate Shop Inventory

Spawn `dnd-gear-master` agent to generate inventory based on:
- Shop type (general store, blacksmith, magic shop, apothecary, etc.)
- Location size (village shops are sparse, city shops are well-stocked)
- Location wealth level
- Any specialties noted in the location file

Present the inventory as a browsable list:

```markdown
## {Shop Name} -- {Shopkeeper Name}
*{Shop type} in [[{Location}]]*

### Weapons
| Item | Price | Properties |
|------|-------|------------|
| Longsword | 15 gp | Versatile (1d10) |

### Armor
| Item | Price | AC | Properties |
|------|-------|----|------------|

### Adventuring Gear
| Item | Price | Notes |
|------|-------|-------|

### Special Items
| Item | Price | Notes |
|------|-------|-------|
```

**Pricing modifiers based on disposition:**

| Disposition | Price Modifier |
|-------------|---------------|
| Hostile | Won't sell (or 200% markup) |
| Unfriendly | 150% markup |
| Neutral | Standard price |
| Friendly | 10% discount |
| Allied | 20% discount |

### 4. Interactive Shopping Loop

Run the shopping interaction:

1. DM/player says what they want to buy or browse
2. Check if item is in stock
3. Quote price (with disposition modifier)
4. If player accepts, process purchase
5. If player haggles, go to haggling

Repeat until DM says they're done shopping.

**Selling items:**
- Shops buy at 50% of item value (standard)
- Disposition modifiers apply in reverse (friendly shops buy at 60%, hostile won't buy)
- Magic items: shops may not have enough gold. Ask DM.

### 5. Haggling Mechanic

When a player wants to haggle:

1. Determine the base DC based on how much discount they're asking for:
   - 5-10% off: DC 10
   - 11-20% off: DC 15
   - 21-30% off: DC 20
   - 31%+ off: DC 25
2. Modify DC by NPC disposition:
   - Hostile: +5
   - Unfriendly: +3
   - Neutral: +0
   - Friendly: -2
   - Allied: -5
3. Ask DM for PC's Charisma (Persuasion) check result
4. **Success:** NPC agrees to the reduced price. Generate in-character acceptance dialogue.
5. **Failure:** NPC refuses. Generate in-character refusal. NPC's disposition may drop by 1 if the attempt was insulting (roll < DC by 5+).
6. **Nat 20:** Exceptional deal -- NPC offers even better than asked. "You know what, take it for {lowest reasonable price}."
7. **Nat 1:** NPC is offended. Prices go up 10% for the rest of this visit.

### 6. Update PC Inventory

For each purchase/sale:
- Read the PC file
- Update `## Equipment` or `## Inventory` section
- Deduct/add gold

### 7. Update NPC Memory

After the shopping session, update the shopkeeper's Memory:

```
- **Day {current-day} | Session {N}:** Party visited shop. {Summary of transactions -- items bought/sold, haggling attempts, total gold spent}. Disposition: {current}.
```

Update disposition if it changed during the interaction.

---

## Roll Mode

### 1. Find Loot Table

Search `5. Armory/Loot Tables/` for the specified table name.

If not found:
- List available tables
- Ask DM to pick one, or offer to create a new table

### 2. Read Table

Read the table file. Expected format:

```markdown
| d{N} | Result |
|------|--------|
| 1 | {item/result} |
| 2-3 | {item/result} |
| 4-6 | {item/result} |
```

### 3. Roll and Present

Roll the appropriate die for the table.

Announce: `d{N}: {roll} -- {result}`

If the result references another table (e.g., "Roll on Magic Item Table A"), follow the chain.

### 4. Offer Next Steps

After presenting the result:
- "Add this to a PC's inventory?"
- "Roll again?"
- "Switch to a different table?"

## Edge Cases

- **Monster has no listed treasure:** Generate minimal mundane items (worn equipment, a few coins) based on what the monster would logically carry.
- **Shop inventory doesn't include requested item:** Shopkeeper doesn't have it. Offer alternatives or suggest where to find it.
- **PC can't afford item:** Report the shortfall. Suggest alternatives: cheaper version, haggling, trade, or quest for the shopkeeper.
- **Magic item shop in a small village:** Unrealistic unless DM has established one. Flag this to DM.
- **Multiple PCs shopping simultaneously:** Handle one at a time or track parallel transactions as DM directs.
- **Shopkeeper is hostile:** They refuse to deal. Party must improve disposition first (quest, gift, persuasion) or find another shop.
- **Custom loot table doesn't exist:** Offer to create one based on DM specifications (terrain, level range, theme).
