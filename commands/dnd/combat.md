---
name: "dnd:combat"
description: "Full combat encounter engine with automatic initiative, attack resolution, damage tracking, spell handling, death saves, and condition management. Runs the complete combat loop until resolution."
---

# /dnd:combat -- Combat Encounter Management

The most mechanically complex skill. Runs full auto combat -- rolls everything, resolves everything, tracks everything. DM narrates and makes story decisions; the engine handles all mechanics.

## Input

$ARGUMENTS -- expects one of:
- Monster list as `{name}:{count}` pairs (e.g., `goblin:3 bugbear:1`)
- `{encounter-file-name}` -- load a pre-built encounter
- Empty -- ask DM what they're fighting

## Setup

1. Read the domain CLAUDE.md at `2. Areas/2.2 Dungeons & Dragons/CLAUDE.md`
2. Read entity schemas from `2. Areas/2.2 Dungeons & Dragons/_Config/Tag Taxonomy.md`
3. **Read combat strategy from `2. Areas/2.2 Dungeons & Dragons/_Config/Combat Strategy.md`** — this controls enemy behavior, player difficulty scaling, environmental requirements, and anti-steamroll tactics. Apply it throughout this encounter.

All paths below are relative to `~/docs/Documents/2. Areas/2.2 Dungeons & Dragons/`.

---

## Starting Combat

### 1. Parse Combatants

**From $ARGUMENTS (monster list):**
- Parse `name:count` pairs
- Spawn `dnd-monster-manual` agent to fetch/cache stat blocks for each unique monster type
- Read all stat blocks and confirm they loaded

**From encounter file:**
- Search `Combat/` directory in the active campaign for the encounter file
- Read the encounter file, extract monsters from frontmatter `monsters:` array
- Spawn `dnd-monster-manual` agent for any stat blocks not yet cached

**If no arguments:**
- Ask DM: "What are you fighting? Give me monsters as `name:count` (e.g., `goblin:3 bugbear:1`)"

### 2. Load PC Stats

Identify the active campaign (from recent state or ask DM).

Glob `1. Campaigns/{campaign}/Party/*.md`. Read each PC file and extract:
- name, player, class, level
- hp-max (current HP = hp-max unless DM says otherwise)
- ac
- stats (all 6 ability scores -- calculate modifiers: floor((score - 10) / 2))
- proficiency-bonus
- Spell slots and known spells (if spellcaster)

Ask DM: "Any PCs not present for this fight?" Exclude them.

Ask DM: "Any PCs not at full HP?" Adjust starting HP.

### 3. Create Encounter File

If not loading from an existing encounter file, create one.

Read World Clock for current game day. Read current location.

Write to `1. Campaigns/{campaign}/Combat/{Encounter Name}.md`:

```yaml
---
type: encounter
name: "{descriptive name}"
campaign: "[[Campaign]]"
session: "[[Session {N}]]"
game-day: {current-day}
location: "[[{current-location}]]"
status: active
difficulty: "{calculated difficulty}"
encounter-type: combat
party-level: {average party level}
party-size: {number of PCs}
monsters:
  - name: "{monster}"
    count: {count}
    api-index: "{index}"
tags:
  - "#dnd/encounter"
  - "#dnd/combat"
---
```

**Difficulty calculation** (5e encounter building):
- Sum monster XP for all monsters
- Multiply by encounter multiplier (1 monster: x1, 2: x1.5, 3-6: x2, 7-10: x2.5, 11-14: x3, 15+: x4)
- Compare adjusted XP to party thresholds per DMG table
- Label as: trivial, easy, medium, hard, or deadly

### 4. Roll Initiative

For each combatant, roll initiative:
- **PCs:** d20 + DEX modifier
- **Monsters:** d20 + DEX modifier (roll once per monster group for identical monsters, or individually if DM prefers)
- **Ties:** Higher DEX modifier goes first. If still tied, PCs before monsters.

Announce each roll:
```
Initiative Rolls:
- Aelric the Brave: d20(14) + 2 = 16
- Goblin A: d20(11) + 2 = 13
- Goblin B: d20(7) + 2 = 9
- Goblin C: d20(18) + 2 = 20
- Thalia Moonwhisper: d20(9) + 3 = 12
```

### 5. Display Initiative Order

Build and display the initiative table:

```markdown
## Initiative Order

| # | Name | Init | AC | HP | Conditions |
|---|------|------|-----|-----|------------|
| 1 | Goblin C | 20 | 15 | 7/7 | -- |
| 2 | Aelric the Brave | 16 | 18 | 45/45 | -- |
| 3 | Goblin A | 13 | 15 | 7/7 | -- |
| 4 | Thalia Moonwhisper | 12 | 14 | 32/32 | -- |
| 5 | Goblin B | 9 | 15 | 7/7 | -- |
```

---

## The Combat Loop

Run automatically until combat ends. For each round:

### Round Header

```
=== ROUND {N} ===
```

### For Each Combatant in Initiative Order:

#### Skip Conditions Check
- If dead/destroyed: skip entirely
- If unconscious (PC at 0 HP): go to death saves
- If incapacitated, stunned, paralyzed: skip action (note why)
- If conditions have start-of-turn effects (e.g., ongoing damage), resolve them first

#### Condition Expiry
- Check all conditions on this creature
- Remove any that expire "at the start of your turn"
- Announce removals: "{Name} shakes off the {condition} effect."

#### Monster Turn (Automatic)

**Step 1: Check Combat Strategy.** Read the enemy's assigned archetype from the encounter file or Combat Strategy config. If no archetype assigned, infer from creature type and INT.

**Step 2: Check Player Threat Profiles.** Before choosing a target, consult `_Config/Combat Strategy.md` player profiles. Apply per-player difficulty modifiers:
- **Apex-threat PCs:** Apply anti-steamroll tactics from the config (2-3 per encounter, not all at once). Target their exploitable weaknesses.
- **Learning players:** Don't hard-focus them unless they're the only viable target. Create dramatic moments, not frustration.

**Step 3: Apply archetype + INT behavior:**

**Low INT (1-7) -- Bestial/simple:**
- Attack nearest creature
- Use breath weapons/area abilities on cooldown whenever possible
- Flee at <25% HP if WIS > 7
- No tactical awareness
- *Archetype override:* Low INT creatures always use Berserker archetype regardless of assignment

**Medium INT (8-12) -- Tactical basics:**
- Focus on wounded targets (low HP)
- Use ranged attacks if available and at distance
- Protect spellcaster allies
- Retreat to allies when injured
- Use abilities strategically (not just on cooldown)
- *Archetype behavior:* Follow assigned archetype from Combat Strategy (Skirmisher, Tactician, etc.)
- *Anti-steamroll:* If targeting an apex-threat PC, apply relevant counters from Combat Strategy (e.g., kiting, swarm grapples, targeting weak saves)

**High INT (13+) -- Strategic:**
- Focus fire on the biggest threat (healer, spellcaster)
- Use terrain and cover
- Coordinate with allies (flank, set up combos)
- Target weak saves with spells/abilities
- Use legendary actions optimally
- Surrender or flee if fight is clearly lost
- *Archetype behavior:* Follow assigned archetype with full tactical intelligence
- *Anti-steamroll:* Actively exploit apex-threat PC weaknesses from Combat Strategy. Use counter-rage timing, terrain denial, and damage types that bypass resistance.
- *Environmental awareness:* High INT enemies may use interactable elements against PCs (topple pillars, ignite oil, trigger hazards)

**Step 4: Check "Everyone Shines" principle.** If combat has lasted 3+ rounds and a PC hasn't had a meaningful moment, create an opening for them on the next monster turn (e.g., position near a glaring interaction, leave a flank open for the rogue, cluster for the wizard's AoE).

For the chosen action:
1. Announce the action: "{Monster} attacks {target} with {weapon/ability}."
2. Roll to hit or force save (see resolution below)
3. Resolve damage/effects
4. Announce result

#### PC Turn (DM Directed)

Prompt the DM:
```
**{PC Name}'s turn.** HP: {current}/{max} | AC: {ac} | Conditions: {list or "none"}
Available: Action, Bonus Action, Movement, Reaction (if not used)
What does {PC Name} do?
```

Wait for DM input, then resolve the described action.

---

### Attack Resolution

For every attack (melee, ranged, spell attack):

1. **Roll to hit:** d20 + attack modifier
   - Announce: `d20({natural roll}) + {modifier} = {total} vs AC {target AC}`
2. **Natural 20:** Critical hit -- proceed to damage with doubled dice
3. **Natural 1:** Automatic miss -- announce and move on
4. **Hit (total >= AC):** Roll damage
5. **Miss (total < AC):** Announce miss

### Damage Resolution

1. **Roll damage dice:** Roll the specified dice + modifier
   - Announce: `{dice}({rolled values}) + {modifier} = {total} {damage type} damage`
2. **Critical hit:** Double the number of damage dice (NOT the modifier)
   - Announce: `CRITICAL! {doubled dice}({rolled values}) + {modifier} = {total} {damage type} damage`
3. **Apply resistances/immunities:**
   - Resistant: halve damage (round down)
   - Immune: 0 damage
   - Vulnerable: double damage
   - Announce modifications: "{Target} is resistant to {type} -- {total} reduced to {reduced}."
4. **Apply to target HP:** Subtract from current HP
5. **At 0 HP:**
   - **Monster/NPC:** Dead (or unconscious if DM says non-lethal)
   - **PC:** Falls unconscious, begin death saves on their next turn

### Saving Throws

When a spell or ability requires a save:

1. **Announce:** "{Target} must make a {ability} saving throw (DC {DC})."
2. **Roll:** d20 + save modifier (include proficiency if proficient)
3. **Announce:** `d20({natural roll}) + {modifier} = {total} vs DC {DC}`
4. **Success/Failure:** Apply effects as described by the spell/ability
   - Many spells do half damage on success
   - Some effects are all-or-nothing

### Spell Resolution

When a PC or monster casts a spell:

1. Spawn `dnd-spell-caster` agent for full spell resolution
2. Track spell slot expenditure
3. **Concentration:** If the caster is already concentrating on a spell, the old spell ends
4. **Concentration saves:** When a concentrating creature takes damage, they must make a CON save (DC = max(10, damage/2)). On failure, concentration breaks.
5. Apply all spell effects (damage, conditions, zones, summons)

### Condition Tracking

Track all active conditions with their source and duration:

| Condition | Source | Duration | Applied |
|-----------|--------|----------|---------|
| Frightened | Dragon Fear | 1 minute (10 rounds) | Round 2 |
| Prone | Shove | Until stand (costs half movement) | Round 3 |
| Concentrating | Bless | Up to 1 minute | Round 1 |

Standard 5e conditions and their effects:
- **Blinded:** Disadvantage on attacks, attacks against have advantage
- **Charmed:** Can't attack charmer, charmer has advantage on social checks
- **Deafened:** Can't hear, auto-fail hearing checks
- **Frightened:** Disadvantage on checks/attacks while source visible, can't willingly move closer
- **Grappled:** Speed 0
- **Incapacitated:** No actions or reactions
- **Invisible:** Heavily obscured, advantage on attacks, attacks against have disadvantage
- **Paralyzed:** Incapacitated, auto-fail STR/DEX saves, attacks have advantage, melee crits within 5ft
- **Petrified:** Incapacitated, resistant to all damage, immune to poison/disease
- **Poisoned:** Disadvantage on attacks and ability checks
- **Prone:** Disadvantage on attacks, melee attacks against have advantage, ranged attacks against have disadvantage
- **Restrained:** Speed 0, disadvantage on attacks, DEX saves; attacks against have advantage
- **Stunned:** Incapacitated, auto-fail STR/DEX saves, attacks against have advantage
- **Unconscious:** Incapacitated, drops items, prone, auto-fail STR/DEX saves, attacks have advantage, melee crits within 5ft

Apply advantage/disadvantage from conditions automatically when resolving rolls.

### Death Saves (PCs at 0 HP)

At the start of an unconscious PC's turn:

1. **Roll d20** (no modifiers unless features apply)
2. **Announce:** `Death Save: d20({roll})`
3. **Results:**
   - **10+:** Success. Track it. (need 3 successes to stabilize)
   - **9 or below:** Failure. Track it. (3 failures = death)
   - **Natural 20:** PC regains 1 HP and is conscious. Clear all death saves.
   - **Natural 1:** Counts as TWO failures.
4. **Taking damage at 0 HP:** Automatic death save failure. If damage >= hp-max, instant death.
5. **Stabilized (3 successes):** No longer makes death saves. Remains unconscious at 0 HP. Regains 1 HP after 1d4 hours.
6. **Dead (3 failures):** Character is dead. Mark status in PC file.

Display death save tracker:
```
{PC Name}: Successes [X][X][ ] | Failures [X][ ][ ]
```

### Environmental Interaction (PC Turns)

When a PC is near an interactable element (marked with `@` on the map or described in the encounter file), remind the DM:
```
💡 {PC Name} is adjacent to {interactable element}. {Brief description of what it does}.
```

When a PC uses an interactable element:
1. Resolve the interaction per the element's defined effect (from encounter file or Combat Strategy config)
2. Narrate dramatically — these moments should feel awesome
3. Mark one-time elements as used in the encounter log
4. If the interaction changes terrain (creates difficult terrain, opens a hole, blocks a path), update the tactical situation

### End of Round

After all combatants have acted:

1. Resolve end-of-round effects (ongoing damage, zone effects)
2. Resolve environmental effects (spreading fire, rising water, crumbling floor)
3. Display updated initiative table with current HP and conditions
4. Check combat end conditions
5. If phase transition threshold reached (see Combat Strategy), trigger the phase change and narrate it

---

## End of Round Display

After each round, show the updated state:

```markdown
--- End of Round {N} ---

| # | Name | Init | AC | HP | Conditions |
|---|------|------|-----|-----|------------|
| 1 | Goblin C | 20 | 15 | DEAD | -- |
| 2 | Aelric the Brave | 16 | 18 | 38/45 | -- |
| 3 | Goblin A | 13 | 15 | 3/7 | Frightened |
| 4 | Thalia Moonwhisper | 12 | 14 | 32/32 | Concentrating (Bless) |
| 5 | Goblin B | 9 | 15 | 7/7 | -- |
```

---

## Combat End Conditions

Check after each round:
- **All enemies dead or fled:** Victory
- **All PCs unconscious or dead:** TPK (Total Party Kill)
- **Enemies surrender:** DM calls it
- **Party flees:** DM calls it
- **DM ends combat:** Manual override

---

## Ending Combat

### 1. Announce Outcome

```
=== COMBAT OVER ===
Result: {Victory / Defeat / Surrender / Retreat}
Duration: {N} rounds
```

### 2. Write Encounter Log

Update the encounter file with the full round log:

```markdown
## Round Log

### Round 1
- **Goblin C** attacks Aelric with shortbow: d20(14)+4=18 vs AC 18 -- Hit! d6(4)+2 = 6 piercing damage.
- **Aelric** uses Great Weapon Master on Goblin C: d20(12)+5=17 vs AC 15 -- Hit! 2d6(4,5)+3+10 = 22 slashing damage. Goblin C is DEAD.
{... full log ...}

## Outcome

- **Result:** Victory
- **Rounds:** 3
- **PC Casualties:** None
- **PC Resources Spent:** 1 spell slot (Bless, 1st level)
- **Enemy Casualties:** 3 goblins killed
```

### 3. Calculate XP

Sum the XP values from all defeated monsters:
```
XP Earned:
- 3x Goblin (50 XP each) = 150 XP
- 1x Bugbear (200 XP) = 200 XP
Total: 350 XP / {party size} PCs = {per-PC XP} XP each
```

Ask DM: "Award XP now?" If yes, note it for PC sheet updates.

### 4. Generate Loot

Ask DM: "Roll for loot?"

If yes:
- Spawn `dnd-loot-dropper` agent for context-appropriate loot based on CR, monster types, and location
- Present loot to DM
- Ask for distribution among PCs

If DM provides specific loot, use that instead.

### 5. Update PC Sheets

For each PC, update their file:
- **HP:** Set to current HP after combat (not max unless they heal)
- **Spell slots:** Deduct used slots
- **Inventory:** Add any looted items
- **XP:** Add earned XP (if DM uses XP tracking)

### 6. Update NPC Files

If any named NPCs were involved:
- If killed, update `status: dead` in their frontmatter
- If injured, note in their State History or Memory
- Append combat participation to their Memory:
```
- **Day {current-day} | Session {N}:** {Combat description and outcome}. Disposition: {current}.
```

### 7. Update Encounter File Status

Set encounter file frontmatter `status: resolved`.

### 8. Return to Play

Report combat summary and return control to the DM/play mode.

---

## Special Mechanics

### Opportunity Attacks
When a creature moves out of another creature's reach without Disengaging:
- The threatened creature can use its reaction for one melee attack
- Resolve as normal attack
- Only one opportunity attack per reaction

### Bonus Actions
Track bonus action usage separately from actions. Common bonus actions:
- Two-weapon fighting (off-hand attack)
- Cunning Action (Rogue)
- Spiritual Weapon, Healing Word, Misty Step
- Rage (Barbarian)

### Reactions
Track reaction availability (refreshes at start of creature's turn):
- Opportunity attacks
- Shield spell
- Counterspell
- Uncanny Dodge (Rogue)
- Sentinel feat attacks

### Legendary Actions
For legendary creatures:
- Track legendary action points (typically 3, refresh at start of creature's turn)
- Can use at the end of another creature's turn
- Announce usage and resolve immediately

### Lair Actions
On initiative count 20 (losing ties):
- Resolve lair action effects
- Describe environmental changes

## Edge Cases

- **Surprise round:** If one side is surprised, surprised creatures can't act on their first turn and can't use reactions until their first turn ends. Roll initiative normally.
- **Reinforcements mid-combat:** Add to initiative order with a new roll. Add to encounter file monsters list.
- **Terrain/cover:** Half cover (+2 AC/DEX saves), three-quarters cover (+5 AC/DEX saves), full cover (can't be targeted)
- **Darkness/obscurement:** Apply blinded condition effects as appropriate
- **Grappling:** Athletics check vs Athletics/Acrobatics. On success, target is grappled.
- **Shoving:** Athletics check vs Athletics/Acrobatics. On success, target is prone or pushed 5ft.
- **Two-weapon fighting:** Bonus action attack with off-hand weapon, don't add ability modifier to damage (unless feature allows it)
- **Ready action:** Creature specifies trigger and action. When trigger occurs, use reaction to take the readied action.
- **Concentration lost mid-combat:** End the spell immediately, remove all its effects from tracking

## Environmental & Interactable Elements

**Every encounter MUST have at least 2 interactable elements.** These are defined in the encounter file or generated on the fly from the Combat Strategy config.

### If Encounter File Has Interactables
Read them from the encounter file's `## Environmental Elements` section and incorporate into combat.

### If No Interactables Defined
Generate 2 appropriate elements based on the location:

1. **One destructible or hazard** — something that deals damage or changes terrain (chandelier, barrel, pillar, steam vent)
2. **One glaring interaction** — an obvious, high-reward action any player can spot (cargo net, oil barrel behind enemies, collapsing ceiling)

Describe these in the opening combat narration so players know they exist. Mark them on the map with `@` if using `/dnd:map`.

### Glaring Interaction Narration
When describing the scene at combat start, emphasize glaring interactions with vivid, unmissable language:
- BAD: "There are some barrels nearby."
- GOOD: "Behind the goblin line, several tar-stained barrels leak dark, pungent liquid — the reek of lamp oil fills the air."

The goal is for players to think "I should DO something with that" without being told explicitly.

## Phase Transitions (Hard/Deadly Encounters)

For encounters rated hard or deadly, include at least one phase transition:

- **HP threshold:** At 50% HP, the boss changes behavior (new archetype, new abilities, terrain change)
- **Reinforcement wave:** After round 3, new enemies arrive from a specific direction
- **Environmental shift:** Terrain changes mid-fight (bridge collapses, fire spreads, water rises)
- **Objective reveal:** A secondary objective appears mid-combat (hostage about to die, portal opening)

Announce phase transitions with dramatic narration and update the initiative table if new combatants join.
