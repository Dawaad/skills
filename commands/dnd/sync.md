# /dnd:sync — Sync D&D Beyond Characters

Scrapes public D&D Beyond character sheets and syncs them to campaign PC files in the vault.

## Input

 — optional. If "add <URL>" is provided, adds the character to the sync config. Otherwise syncs all registered characters.

## Setup

1. Read sync config: `2. Areas/2.2 Dungeons & Dragons/_Config/DDB Sync.md`
2. Read domain CLAUDE.md: `2. Areas/2.2 Dungeons & Dragons/CLAUDE.md`
3. Read PC schema from: `2. Areas/2.2 Dungeons & Dragons/_Config/Tag Taxonomy.md`

All paths are relative to `~/docs/Documents/2. Areas/2.2 Dungeons & Dragons/`.

## Workflow

### 1. Load Character Registry

Read `_Config/DDB Sync.md` and extract the character table. Each row has:
- Character ID
- D&D Beyond URL
- Campaign name

### 2. Spawn Sub-Agents

For each character in the registry, spawn a sub-agent (using the Agent tool) to scrape and sync that character. Run all agents **in parallel**.

Each sub-agent receives this prompt:

---

**Task:** Scrape D&D Beyond character and write vault PC file.

**Character URL:** `https://www.dndbeyond.com/characters/{CHARACTER_ID}`
**Campaign:** `{CAMPAIGN_NAME}`
**Output path:** `~/docs/Documents/2. Areas/2.2 Dungeons & Dragons/1. Campaigns/{CAMPAIGN_NAME}/Party/{CHARACTER_NAME}.md`

**Steps:**

1. **Navigate** to the character URL using the headless browser:
   ```bash
   B=~/.claude/skills/gstack/browse/dist/browse
   $B goto "https://www.dndbeyond.com/characters/{CHARACTER_ID}"
   ```

2. **Wait for content** — the page is a JavaScript SPA. Wait for it to load:
   ```bash
   $B wait --load
   ```

3. **Extract text dump:**
   ```bash
   $B text
   ```

4. **Parse the text dump.** The D&D Beyond character page text follows this structure:
   - **Header:** `{Name}{Gender}{Race}{Class} {Level}Level {Level}Campaign:{CampaignName}`
   - **Stats:** `Ability ScoresStrengthstr{mod}{value}Dexteritydex{mod}{value}Constitutioncon{mod}{value}Intelligenceint{mod}{value}Wisdomwis{mod}{value}Charismacha{mod}{value}`
   - **Proficiency:** `Proficiency{bonus}Bonus`
   - **Speed:** `Walking{speed}ft.`
   - **HP:** `Current{current}/MaxMax hit points{max}`
   - **AC:** `Armor{ac}Class`
   - **Saving Throws:** `{ability} Saving Throw{abbr}{bonus}` repeated for each
   - **Skills:** `{ABILITY}{SkillName}{bonus}` repeated (proficient skills marked with `Proficiency` prefix)
   - **Spells:** Listed after `Spells` section header with format `{SpellName}({level}),`
   - **Actions/Weapons:** Listed after `Actions` with format `{Name}{Type}{Range}{hit}{damage}{properties}`
   - **Features:** Listed throughout with descriptions

5. **Extract the following fields** from the parsed text:
   - `name` — character name (first word(s) before gender)
   - `player` — leave as "Unknown" (DDB doesn't show player name)
   - `race` — e.g., "High Elf", "Human"
   - `class` — e.g., "Ranger", "Fighter"
   - `subclass` — look for subclass name in features section
   - `level` — integer
   - `hp-max` — from "Max hit points{N}"
   - `ac` — from "Armor{N}Class"
   - Stats: `str`, `dex`, `con`, `int`, `wis`, `cha` — the raw score values (not modifiers)
   - `proficiency-bonus` — from "Proficiency{N}Bonus"
   - Speed
   - Saving throw proficiencies
   - Skill proficiencies and bonuses
   - Spells known/prepared
   - Equipment (weapons from actions section)
   - Features and traits
   - Defenses and conditions (resistances, immunities)
   - Languages and proficiencies

6. **Also try to get Inventory and Features tabs** by clicking those sections:
   ```bash
   $B snapshot -i 2>&1 | grep -i "invent\|feature"
   ```
   If you find inventory/features tab refs, click them and extract the text.

7. **Check for existing PC file.** If a file already exists at the output path, read it first to preserve any manually-added content in `## Backstory`, `## Relationships`, and `## Notes` sections.

8. **Write the PC file** using this format:

```yaml
---
type: pc
name: "{name}"
player: "Unknown"
campaign: "[[Campaign]]"
ddb-id: "{CHARACTER_ID}"
ddb-url: "https://www.dndbeyond.com/characters/{CHARACTER_ID}"
race: "{race}"
class: "{class}"
subclass: "{subclass}"
level: {level}
hp-max: {hp}
ac: {ac}
speed: "{speed}"
stats:
  str: {str}
  dex: {dex}
  con: {con}
  int: {int}
  wis: {wis}
  cha: {cha}
proficiency-bonus: {prof}
status: active
last-synced: "{today's date YYYY-MM-DD}"
tags:
  - "#dnd/pc"
---
```

Body sections:

```markdown
# {Character Name}

## Saving Throws

{List saving throw proficiencies with bonuses}

## Skills

{List ALL skills with bonuses, mark proficient/expert ones}

## Features & Traits

{List all racial and class features}

## Spells Known

{If spellcaster — list cantrips and spells by level}

## Actions

{List all actions with attack bonuses, damage, ranges, properties}

## Equipment

{Equipped weapons and armor}

## Inventory

{Other carried items — if available from inventory tab}

## Defenses

{Resistances, immunities, condition immunities}

## Proficiencies & Languages

{Armor, weapon, tool proficiencies and languages}

## Backstory

{Preserve from existing file, or leave placeholder}

## Relationships

{Preserve from existing file, or "To be populated during play"}

## Notes

{Preserve from existing file, or empty}
```

9. **Return a summary** of what was synced: character name, class, level, and the output file path.

**IMPORTANT:** If the page shows "Private" or "Permission denied", report that the character is private and cannot be synced.

---

### 3. Collect Results

After all sub-agents complete, collect the results and present a summary table:

| Character | Class | Level | Status |
|-----------|-------|-------|--------|

### 4. Update Sync Log

Append a row to `_Config/DDB Sync.md` Sync Log table:

```
| {today} | {count} | Synced: {character names} |
```

### 5. Update Campaign Level

If all characters are synced, check if the party level in `Campaign.md` needs updating (use the average or minimum level).

## Add Mode

If  starts with "add":
1. Extract the URL/ID from the argument
2. Ask which campaign it belongs to
3. Add a row to the Characters table in `_Config/DDB Sync.md`
4. Run the sync for just that character

## Edge Cases

- **Character is private:** Report and skip, don't fail the whole sync
- **Character name changed:** The filename is based on character name — if it changed, the old file will remain. Report this.
- **Browse binary not available:** Run the setup script at `~/.claude/skills/gstack/browse/setup`
- **Page doesn't load:** Retry once after 5 seconds, then report failure
