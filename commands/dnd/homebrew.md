---
name: "dnd:homebrew"
description: "Homebrew content creation balanced against official 5e benchmarks. Create custom monsters, spells, magic items, and house rules with proper balance validation and registry tracking."
---

# /dnd:homebrew -- Homebrew Content Creation

Create balanced homebrew content: monsters, spells, items, and rules. Each creation is validated against official 5e benchmarks and tracked in the Homebrew Registry.

## Input

$ARGUMENTS -- expects one of:
- `--monster` -- create a custom monster
- `--spell` -- create a custom spell
- `--item` -- create a custom magic item
- `--rule` -- create or document a house rule
- Empty -- ask what type of content to create

## Setup

1. Read the domain CLAUDE.md at `2. Areas/2.2 Dungeons & Dragons/CLAUDE.md`
2. Read entity schemas from `2. Areas/2.2 Dungeons & Dragons/_Config/Tag Taxonomy.md`

All paths below are relative to `~/docs/Documents/2. Areas/2.2 Dungeons & Dragons/`.

---

## Monster Mode

### 1. Gather Monster Concept

Ask for:

- **Concept** -- what is this creature? (description, theme, narrative purpose)
- **Intended CR** -- target challenge rating
- **Creature type** -- aberration, beast, celestial, construct, dragon, elemental, fey, fiend, giant, humanoid, monstrosity, ooze, plant, undead
- **Size** -- Tiny, Small, Medium, Large, Huge, Gargantuan
- **Special abilities** -- any unique mechanics the DM wants (e.g., "phase through walls", "drain life on hit", "split when hit with slashing")
- **Campaign context** -- where and why this creature appears

### 2. Fetch Balance Reference

Spawn `dnd-monster-manual` agent to fetch 2-3 official monsters at the same CR for comparison.

DMG benchmark stats per CR (key reference):

| CR | Prof | AC | HP | Attack Bonus | DPR | Save DC |
|----|------|-----|-----|-------------|------|---------|
| 0 | +2 | 13 | 1-6 | +3 | 0-1 | 13 |
| 1/4 | +2 | 13 | 7-35 | +3 | 2-3 | 13 |
| 1/2 | +2 | 13 | 36-49 | +3 | 4-5 | 13 |
| 1 | +2 | 13 | 50-70 | +3 | 6-8 | 13 |
| 2 | +2 | 13 | 71-85 | +3 | 9-14 | 13 |
| 3 | +2 | 13 | 86-100 | +4 | 15-20 | 13 |
| 4 | +2 | 14 | 101-115 | +5 | 21-26 | 14 |
| 5 | +3 | 15 | 116-130 | +6 | 27-32 | 15 |
| 6 | +3 | 15 | 131-145 | +6 | 33-38 | 15 |
| 7 | +3 | 15 | 146-160 | +6 | 39-44 | 15 |
| 8 | +3 | 16 | 161-175 | +7 | 45-50 | 16 |
| 9 | +4 | 16 | 176-190 | +7 | 51-56 | 16 |
| 10 | +4 | 17 | 191-205 | +7 | 57-62 | 16 |
| 11 | +4 | 17 | 206-220 | +8 | 63-68 | 17 |
| 12 | +4 | 17 | 221-235 | +8 | 69-74 | 17 |
| 13 | +5 | 18 | 236-250 | +8 | 75-80 | 18 |
| 14 | +5 | 18 | 251-265 | +8 | 81-86 | 18 |
| 15 | +5 | 18 | 266-280 | +8 | 87-92 | 18 |
| 16 | +5 | 18 | 281-295 | +9 | 93-98 | 18 |
| 17 | +6 | 19 | 296-310 | +10 | 99-104 | 19 |
| 18 | +6 | 19 | 311-325 | +10 | 105-110 | 19 |
| 19 | +6 | 19 | 326-340 | +10 | 111-116 | 19 |
| 20 | +6 | 19 | 341-355 | +10 | 117-122 | 19 |

### 3. Generate Stat Block

Build the stat block following the monster schema:

1. **Set ability scores** -- distribute based on creature concept (a brute has high STR/CON, a spellcaster has high INT/CHA)
2. **Calculate HP** -- use appropriate hit dice for size (d4 Tiny, d6 Small, d8 Medium, d10 Large, d12 Huge, d20 Gargantuan) + CON modifier per die
3. **Set AC** -- match DMG benchmark for CR, justify with armor type (natural armor, armor, etc.)
4. **Design attacks** -- set attack bonus and damage per round to match DMG benchmark DPR
5. **Design special abilities** -- implement the DM's requested mechanics, balanced for the CR
6. **Set saves and skills** -- appropriate to creature concept
7. **Set resistances/immunities** -- note that these effectively increase survivability (adjust HP/CR accordingly)

### 4. Balance Validation

Compare the generated stat block against the DMG benchmarks:

```markdown
## Balance Check

| Metric | Target (CR {N}) | Actual | Status |
|--------|----------------|--------|--------|
| AC | {benchmark} | {actual} | OK / HIGH / LOW |
| HP | {range} | {actual} | OK / HIGH / LOW |
| Attack Bonus | +{benchmark} | +{actual} | OK / HIGH / LOW |
| DPR | {range} | {actual} | OK / HIGH / LOW |
| Save DC | {benchmark} | {actual} | OK / HIGH / LOW |
```

If any metric is significantly off:
- Explain why (a glass cannon intentionally has low HP but high DPR)
- Note the effective CR may differ from intended CR
- Suggest adjustments if balance is concerning

### 5. Write Monster File

Write to `3. Bestiary/Homebrew/{Name}.md` using the monster schema:

Set `source: homebrew` in frontmatter. Include `## Design Notes` section with:
- Original concept and intended role
- Balance reference (which official monsters were compared)
- Effective CR analysis
- Suggested encounter use (solo, with minions, as part of a group)

### 6. Update Homebrew Registry

Read `_Config/Homebrew Registry.md` (create if it doesn't exist).

Append to the Monsters table:

```
| {name} | {cr} | {creature-type} | {campaign or "world"} | {today} |
```

---

## Spell Mode

### 1. Gather Spell Concept

Ask for:

- **Concept** -- what does this spell do?
- **Intended level** -- 0 (cantrip) through 9
- **School** -- abjuration, conjuration, divination, enchantment, evocation, illusion, necromancy, transmutation
- **Effect type** -- damage, healing, utility, control, buff, debuff
- **Flavor** -- thematic description, what it looks/sounds like
- **Which classes** should have access

### 2. Fetch Balance Reference

Spawn `dnd-spell-caster` agent to fetch 2-3 official spells at the same level and school for comparison.

Key balance benchmarks:

**Damage spells (single target):**
| Level | Damage (save for half) | Damage (attack roll) |
|-------|----------------------|---------------------|
| Cantrip | 1d10 (scales at 5/11/17) | 1d10 (scales) |
| 1st | 2d10 / 3d8 | 2d10 / 3d8 |
| 2nd | 3d10 / 4d8 | 3d10 |
| 3rd | 5d10 / 8d6 | 6d8 |
| 4th | 6d10 | 7d8 |
| 5th | 8d8 / 8d10 | 8d10 |

**Damage spells (AoE):** Reduce per-target damage by ~30% compared to single target.

**Healing spells:**
| Level | Healing |
|-------|---------|
| 1st | 1d8 + mod |
| 2nd | 2d8 + mod |
| 3rd | 3d8 + mod (or 6d8 mass) |

### 3. Design the Spell

Build the spell following the spell schema:

- **Casting time:** Action, bonus action, reaction, 1 minute, etc. (bonus action spells should be weaker)
- **Range:** Self, touch, 30/60/120/150 ft
- **Components:** V, S, M (costly material components for powerful spells)
- **Duration:** Instantaneous, 1 round, 1 minute, 10 minutes, 1 hour, concentration
- **Effect:** Full mechanical description
- **At higher levels:** Scaling when upcast (typically +1 die per level)

### 4. Balance Validation

Compare against official spells of the same level:

```markdown
## Balance Check

| Metric | Official Reference | This Spell | Notes |
|--------|-------------------|------------|-------|
| Damage/Healing | {reference spell: Xd8} | {this: YdZ} | {comparison} |
| Range | {reference} | {this} | |
| Duration | {reference} | {this} | |
| Conditions applied | {reference} | {this} | |
| Action economy | {reference} | {this} | |
| Concentration | {reference} | {this} | |
```

Flag if the spell is strictly better than an official spell at the same level.

### 5. Write Spell File

Write to `4. Spellbook/Homebrew/{Name}.md` using a spell frontmatter (adapt from the item/spell conventions):

```yaml
---
type: spell
name: "{name}"
source: homebrew
spell-level: {level}
school: "{school}"
casting-time: "{time}"
range: "{range}"
duration: "{duration}"
concentration: {true/false}
ritual: {true/false}
components: "{V, S, M}"
material: "{material description if applicable}"
classes:
  - "{class 1}"
  - "{class 2}"
tags:
  - "#dnd/spell"
  - "#dnd/homebrew"
---
```

Include `## Design Notes` with balance analysis and reference spells.

### 6. Update Homebrew Registry

Append to the Spells table:

```
| {name} | {level} | {school} | {classes} | {today} |
```

---

## Item Mode

### 1. Gather Item Concept

Ask for:

- **Concept** -- what is this item?
- **Rarity** -- common, uncommon, rare, very rare, legendary, artifact
- **Item type** -- weapon, armor, wondrous item, potion, scroll, ring, rod, staff, wand
- **Attunement** -- required? By whom? (spellcaster, specific class, specific alignment)
- **Effect** -- what does it do mechanically?
- **Flavor/history** -- the item's story

### 2. Fetch Balance Reference

Spawn `dnd-gear-master` agent to fetch 2-3 official items of the same rarity and type.

Rarity guidelines:

| Rarity | Typical Power Level |
|--------|-------------------|
| Common | Minor convenience, flavor, no combat advantage |
| Uncommon | +1 weapons/armor, minor abilities, limited use |
| Rare | +2 weapons/armor, significant abilities, 1-3 charges |
| Very Rare | +3 weapons/armor, powerful abilities, multiple charges |
| Legendary | Game-changing abilities, multiple powerful features |
| Artifact | Campaign-defining, world-altering power with drawbacks |

### 3. Design the Item

Build the item following the item schema:

- Mechanical effects (bonuses, charges, abilities)
- Activation (action, bonus action, passive)
- Charges and recharge (dawn, long rest, never)
- Curse/drawback (for powerful items)
- Destruction conditions (for artifacts)

### 4. Balance Validation

```markdown
## Balance Check

| Metric | Official Reference ({item}) | This Item | Notes |
|--------|---------------------------|-----------|-------|
| Combat bonus | {reference} | {this} | |
| Charges/uses | {reference} | {this} | |
| Action economy | {reference} | {this} | |
| Attunement | {reference} | {this} | |
| Drawbacks | {reference} | {this} | |
```

Flag if item is significantly stronger than official items of the same rarity.

### 5. Write Item File

Write to `5. Armory/Homebrew Items/{Name}.md` using the item schema:

Set `source: homebrew`. Include `## Design Notes` and `## Lore` sections.

### 6. Update Homebrew Registry

Append to the Items table:

```
| {name} | {rarity} | {item-type} | {attunement} | {today} |
```

---

## Rule Mode

### 1. Gather Rule Details

Ask for:

- **Rule name** -- short descriptive name
- **What it changes** -- which official rule is being modified or what new mechanic is added
- **Why** -- rationale for the change
- **Mechanical details** -- exact wording of the rule

### 2. Write Rule File

Write to `6. Rules/Homebrew Rules/{Name}.md`:

```yaml
---
type: config
name: "{rule name}"
Created: {today}
Updated: {today}
status: active                  # active | deprecated | testing
affects: "{what system it changes}"
tags:
  - "#dnd/rules"
  - "#dnd/homebrew"
---
```

Body:

```markdown
# {Rule Name}

## Summary

{One-sentence description of the rule change}

## Official Rule

{What the official rule says -- quote or paraphrase the relevant PHB/DMG text}

## Homebrew Modification

{Exact wording of the new rule}

## Rationale

{Why this change was made -- game balance, fun factor, narrative support, player preference}

## Examples

{1-2 concrete examples of the rule in action}

## Interactions

{How this rule interacts with other mechanics -- features, spells, abilities that are affected}
```

### 3. Update Homebrew Registry

Append to the Rules table:

```
| {name} | {affects} | {status} | {today} |
```

### 4. Update Campaign House Rules

If a specific campaign is active, read its `Campaign.md` and append to `## House Rules`:

```
- [[{Rule Name}]] -- {one-line summary}
```

---

## Homebrew Registry

The registry at `_Config/Homebrew Registry.md` tracks all homebrew content:

```markdown
---
type: config
Created: {today}
Updated: {today}
tags:
  - "#dnd/config"
  - "#dnd/homebrew"
---

# Homebrew Registry

## Monsters

| Name | CR | Type | Campaign | Created |
|------|----|------|----------|---------|

## Spells

| Name | Level | School | Classes | Created |
|------|-------|--------|---------|---------|

## Items

| Name | Rarity | Type | Attunement | Created |
|------|--------|------|------------|---------|

## Rules

| Name | Affects | Status | Created |
|------|---------|--------|---------|
```

If the registry doesn't exist when any homebrew content is created, create it first with the above structure, then add the entry.

## Edge Cases

- **Homebrew content that references other homebrew:** Link with wiki links, note dependencies in Design Notes.
- **Balancing for a specific party:** If the DM mentions their party composition, adjust balance advice accordingly (a party of 6 can handle stronger monsters than a party of 3).
- **Deliberately overpowered content:** If DM wants something intentionally unbalanced (e.g., for a narrative moment), note the imbalance clearly in Design Notes but create it anyway.
- **Content that already exists in a supplement:** Check if it's actually official content the DM doesn't own. Note the official version exists, create the homebrew version anyway.
- **Updating existing homebrew:** If the name matches an existing file, read it first and offer to revise rather than replace.
