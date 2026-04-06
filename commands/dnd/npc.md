---
name: "dnd:npc"
description: "NPC interaction and creation. Default mode reads an existing NPC and runs in-character dialogue with memory tracking. Use --create for new NPCs with personality, knowledge, and optional stat blocks."
---

# /dnd:npc -- NPC Interaction & Building

Two modes: create new NPCs with full personality generation, or interact with existing NPCs using memory-weighted dialogue.

## Input

$ARGUMENTS -- expects one of:
- `--create {name}` -- create a new NPC
- `{npc-name}` -- interact with an existing NPC (default)
- `{npc-name} --create` -- also triggers create mode

## Setup

1. Read the domain CLAUDE.md at `2. Areas/2.2 Dungeons & Dragons/CLAUDE.md`
2. Read entity schemas from `2. Areas/2.2 Dungeons & Dragons/_Config/Tag Taxonomy.md`

All paths below are relative to `~/docs/Documents/2. Areas/2.2 Dungeons & Dragons/`.

## Mode Detection

Parse `$ARGUMENTS`:
- Contains `--create` -> create mode
- Name provided that doesn't match any file in `2. World/NPCs/` -> offer create mode
- Name matches existing NPC file -> interact mode
- If ambiguous, search for the NPC name with Grep in `2. World/NPCs/`

---

## Create Mode

### 1. Gather NPC Details

Ask for (or extract from $ARGUMENTS):

- **Name** -- full NPC name
- **Race** -- any 5e race
- **Alignment** -- standard 5e alignment (e.g., Lawful Good, Chaotic Neutral)
- **Location** -- where they are currently found (wiki link, e.g., `[[Phandalin]]`)
- **Faction** -- optional, wiki link if applicable (e.g., `[[Zhentarim]]`)
- **Role in story** -- what purpose does this NPC serve? (quest giver, ally, antagonist, shopkeeper, informant, etc.)
- **Campaign** -- which campaign, or world-level if none

### 2. Generate Personality (5e System)

Generate a complete personality using the 5e system:

- **Personality trait** (1-2) -- observable behavior, quirk, or habit
- **Ideal** -- what drives this person (tied to alignment axis)
- **Bond** -- what they care about most, what they'd sacrifice for
- **Flaw** -- a weakness, vice, or blind spot that can be exploited

Use the role-in-story to weight these. A shopkeeper's flaw might be greed. An informant's bond might be to a destroyed homeland.

### 3. Generate Knowledge Items

Generate 3-5 knowledge items this NPC possesses:

- Secrets they know (about other NPCs, locations, factions)
- Rumors they've heard (may be true or false -- mark reliability)
- Quest hooks they can provide
- Lore about local area or history

Each item should be formatted as:
```
- **[Type: Secret/Rumor/Hook/Lore]** {content} (Reliability: high/medium/low)
```

### 4. Generate Voice & Speech Pattern

Write a 2-3 sentence description of how this NPC speaks:

- Speech cadence (slow and deliberate, rapid-fire, halting)
- Vocabulary level (educated, common, archaic, slang-heavy)
- Verbal tics or habits (always clears throat, uses a specific catchphrase, refers to self in third person)
- Accent or dialect notes (if applicable)

This is used by interact mode to maintain consistent dialogue voice.

### 5. Create Stat Block (If Combatant)

If the NPC has a combat role (guard, soldier, mage, assassin, etc.):

- Determine appropriate base creature from the API (commoner, guard, knight, mage, assassin, etc.)
- Spawn the `dnd-monster-manual` agent to fetch the base stat block
- Customize: rename, adjust stats if needed, add unique abilities tied to NPC personality
- Include the stat block in the NPC file's `## Stat Block` section

If non-combatant, omit the Stat Block section entirely.

### 6. Write NPC File

Write to `2. World/NPCs/{Name}.md` using the NPC schema:

```yaml
---
type: npc
name: "{name}"
campaign: "[[{campaign}]]"    # or omit if world-level
location: "[[{location}]]"
faction: "[[{faction}]]"       # omit if none
race: "{race}"
class:                         # omit if non-classed
alignment: "{alignment}"
cr:                            # omit if non-combatant
status: alive
disposition: neutral
relationship-score: 0
source: "homebrew"
tags:
  - "#dnd/npc"
---
```

Body:

```markdown
# {Name}

## Description

{Physical appearance -- 2-3 sentences. Age, build, distinguishing features, clothing/gear.}

## Personality

- **Trait:** {personality trait(s)}
- **Ideal:** {ideal}
- **Bond:** {bond}
- **Flaw:** {flaw}
- **Voice:** {speech pattern description}

## Knowledge

{Generated knowledge items}

## Memory

{Empty -- will be populated during interactions}

## Stat Block

{If combatant, full stat block. Otherwise omit this section.}

## Relationships

{Known relationships to other NPCs, factions, or PCs}
```

### 7. Update Location File

Read the location file referenced in `location:` frontmatter.

Find the `## NPCs Present` section and add:
```
- [[{NPC Name}]] -- {one-line role description}
```

If the section doesn't exist, create it.

### 8. Update Faction File (If Applicable)

If a faction was specified:

- Read the faction file from `2. World/Factions/{faction}.md`
- Find `## Members` section and add:
```
- [[{NPC Name}]] -- {role within faction}
```

### 9. Confirm Creation

Report:
- NPC file path
- Key personality summary (trait + flaw in one line)
- Knowledge count
- Files updated (location, faction)
- "Interact with `/dnd:npc {name}`"

---

## Interact Mode

### 1. Load NPC State

**CRITICAL: Read these files BEFORE generating ANY dialogue.**

1. **Read NPC file** -- full file, paying special attention to:
   - `disposition` and `relationship-score` from frontmatter
   - `## Personality` -- trait, ideal, bond, flaw, voice
   - `## Knowledge` -- what they know and can share
   - `## Memory` -- every past interaction (read ALL entries)
   - `## Relationships` -- connections to other entities

2. **Read current location file** -- for scene context (where is this conversation happening?)

3. **Read World Clock** -- for current game day (needed for memory entries)

4. **Read Campaign.md** -- for session count (needed for memory entries)

### 2. Assess Interaction Context

Before generating dialogue, assess:

- **Disposition weight:** hostile NPCs are terse, evasive, threatening. Friendly NPCs are open, helpful, generous with info. Neutral NPCs are transactional.
- **Memory continuity:** If the party has prior history with this NPC, the NPC remembers. Reference past events naturally in dialogue.
- **Knowledge gating:** The NPC only shares knowledge appropriate to their disposition. Hostile NPCs share nothing. Neutral NPCs trade info for something. Friendly NPCs volunteer information.
- **Scene context:** Time of day, location, what's happening around them affects the interaction.

### 3. Generate In-Character Dialogue

Present the NPC's dialogue in character, weighted by all the above factors.

Guidelines:
- Use the voice/speech pattern from the Personality section
- Stay true to the trait, ideal, bond, and flaw
- Reference specific Memory entries when relevant ("Last time you came through here, you left my shop in shambles...")
- Gate knowledge sharing by disposition level
- React to what the DM/player says in character
- Include brief action/gesture descriptions in italics (*adjusts spectacles nervously*, *slams fist on table*)

Format dialogue as:
```
**{NPC Name}:** *{action/gesture}* "{dialogue text}"
```

### 4. Run the Interaction Loop

Continue the conversation as long as the DM/player engages. For each exchange:

1. Read player/DM input
2. Determine NPC response based on personality + disposition + memory
3. If player attempts persuasion/deception/intimidation, note the request and ask DM for the roll result, then adjust response accordingly
4. If NPC shares knowledge, note which items were revealed
5. If interaction is going well, disposition may warm. If going poorly, it may cool.

### 5. Update Memory After Interaction

When the interaction concludes (DM moves on or says done):

Append a new entry to the `## Memory` section of the NPC file:

```
- **Day {current-day} | Session {session-count}:** {concise summary of what happened} -> {outcome}. Disposition: {current-disposition}.
```

Examples:
```
- **Day 3 | Session 2:** Party asked about the missing shipment. Shared rumor about bandits on the road. Accepted 5gp for information. -> Cooperative exchange. Disposition: neutral.
- **Day 7 | Session 4:** Caught party member stealing from the shop. Threatened to call the guard. -> Hostile confrontation, party fled. Disposition: hostile.
```

### 6. Update Disposition (If Changed)

If the interaction meaningfully shifted the NPC's feelings:

- Update `disposition:` in frontmatter (hostile / unfriendly / neutral / friendly / allied)
- Update `relationship-score:` in frontmatter (-5 to +5, shift by 1 per significant interaction)

Disposition change triggers:
- **Positive:** Helped the NPC, fulfilled a request, shared valuable info, completed their quest, saved their life
- **Negative:** Threatened, stole from, lied to (caught), harmed allies, failed their quest
- **Major shifts (2+ points):** Only for dramatic events (saved their child, burned their home)

### 7. Schedule Future Consequences (If Applicable)

If the interaction has future consequences:

- Read `State/World Clock.md`
- Append to the Scheduled Events table:

```
| {future-day} | {time} | {consequence event description} | false |
```

Examples:
- NPC threatens to report the party -> scheduled guard patrol in 2 days
- NPC promises to gather information -> scheduled info delivery in 3 days
- NPC sends word to faction about the party -> faction response in 5 days

## Edge Cases

- **NPC is dead:** Read status field. If dead, inform user. Offer to create a ghost/undead version or a different NPC.
- **NPC not found:** Search broadly with Grep. If still not found, offer to create.
- **Multiple NPCs with similar names:** Present options, ask user to pick.
- **NPC has no Memory entries:** First interaction -- NPC has no prior context with the party. Use default disposition.
- **NPC from a different campaign:** Warn user about cross-campaign NPC usage. Proceed if confirmed.
- **Player attempts to use a skill check during dialogue:** Prompt for the roll, then adjust NPC response based on success/failure. Note the check result in the memory entry.
