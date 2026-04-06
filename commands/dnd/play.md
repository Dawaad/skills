---
name: "dnd:play"
description: "Live game execution engine. Runs the full play loop with automatic dice resolution, NPC dialogue, state persistence, scene management, and real-time world tracking. The core D&D gameplay skill."
---

# /dnd:play -- Live Game Execution Engine

The core gameplay skill. Runs the live game with full auto mechanics, persistent state, and scene management. DM narrates and makes story decisions; the engine handles all dice, mechanics, state tracking, and NPC voices.

## Input

$ARGUMENTS -- campaign name (required). If omitted, list active campaigns and ask.

## Setup

1. Read the domain CLAUDE.md at `2. Areas/2.2 Dungeons & Dragons/CLAUDE.md`
2. Read entity schemas from `2. Areas/2.2 Dungeons & Dragons/_Config/Tag Taxonomy.md`

All paths below are relative to `~/docs/Documents/2. Areas/2.2 Dungeons & Dragons/`.

---

## Starting Play Mode

### 1. Load Campaign State

Read ALL of the following:

- `1. Campaigns/{campaign}/Campaign.md` -- session count, party level, setting
- `1. Campaigns/{campaign}/State/World Clock.md` -- current day, time, weather, scheduled events
- `1. Campaigns/{campaign}/Party/*.md` -- all PC files (names, stats, HP, inventory, class features)
- `1. Campaigns/{campaign}/State/` -- active quest files, plot thread files
- Recent NPC interaction files (NPCs referenced in last session)

### 2. Check for Session Plan

Search `1. Campaigns/{campaign}/Sessions/` for a session plan with `status: planned` or `status: in-progress`.

**If session plan found:**
- Read the full plan
- Use it as the session roadmap
- Track scene progression through the plan
- Note: the plan is a guide, not a railroad. Adapt when players diverge.

**If no session plan:**
- That's fine -- run open/sandbox play
- Use quest states, plot threads, and scheduled events to drive the narrative

### 3. Check for Triggered Events

Read the World Clock Scheduled Events table. For each event where:
- `Day <= current-day` AND
- `Triggered = false`

Fire the event:
1. Mark `Triggered = true` in the World Clock
2. Narrate the event's effects
3. Apply state changes (NPC dispositions, location states, quest progress)
4. Write all changes immediately

If multiple events are due, process them in day order.

### 4. Set the Opening Scene

**With session plan:** Start with Scene 1 from the plan.

**Without session plan:** Based on current state:
- Where is the party? (last known location)
- What time of day is it?
- What's happening around them?
- Any NPCs present?

### 5. Present the Opening

```markdown
---
**{Campaign Name}** -- Session {N}
**Day {current-day}, {current-time}** | {weather if set} | [[{Location}]]
---

{Atmospheric scene description -- 3-5 sentences setting the scene}

{If events fired, weave their effects into the description}

{If NPCs are present, note them and their apparent activity}

**What do the players do?**
```

---

## The Play Loop

This is the core game loop. It runs continuously until the DM ends the session.

### Input Processing

When the DM provides input, process it through this pipeline:

```
DM Input
  ↓
Quick Command Check (see below)
  ↓
Read Relevant State Files
  ↓
Resolve Mechanics (dice, saves, checks)
  ↓
Generate Narrative Outcome
  ↓
Write ALL State Changes
  ↓
Check: Triggered Events? Scene Transition?
  ↓
Present Result + "What do the players do?"
```

### Resolving Actions

For every player action the DM describes:

**Ability Checks:**
1. Determine the appropriate ability and skill
2. Determine the DC (set by context, or ask DM if unclear)
3. Roll: d20 + ability modifier + proficiency (if proficient)
4. Announce: `{PC Name} -- {Skill} check: d20({roll}) + {mod} = {total} vs DC {DC} -- {Success/Failure}`
5. Narrate the outcome

**Saving Throws:**
1. Determine the save type and DC
2. Roll: d20 + save modifier
3. Announce roll and result
4. Apply effects based on success/failure

**Attack Rolls:**
- If a single attack during exploration/roleplay, resolve inline
- If combat breaks out, hand off to `/dnd:combat` (see Quick Commands)

**NPC Interactions:**
1. Read the NPC file (disposition, memory, personality, knowledge)
2. Generate in-character dialogue weighted by disposition and memory
3. If the player attempts persuasion/deception/intimidation, resolve the check
4. After the interaction, append to NPC memory
5. Update disposition if changed

**Environmental Interactions:**
1. Read the location file
2. Determine what happens (DC for finding things, trap triggers, etc.)
3. Resolve any checks
4. Update location state history if something changes

**Spell Casting (out of combat):**
1. Spawn `dnd-spell-caster` agent for resolution
2. Deduct spell slot
3. Apply effects
4. Update PC file

### State Persistence

**CRITICAL: Write state changes IMMEDIATELY after every action that changes state.** Do not batch. Do not defer.

After each resolved action, check for and write:

- **NPC memory entries** -- any interaction, no matter how brief
- **NPC disposition changes** -- any shift in attitude
- **Location state history** -- any change to a location
- **Quest progress** -- any advancement or setback
- **Plot thread updates** -- any thread advancement
- **World Clock changes** -- any time advancement
- **PC file updates** -- HP, spell slots, inventory, XP
- **Scheduled events** -- any new future consequences

### World Clock Management

Advance the World Clock for time-passing activities:

| Activity | Time Cost |
|----------|----------|
| Short rest | 1 hour (advance current-time) |
| Long rest | 8 hours (advance to next morning) |
| Travel (see `/dnd:world`) | Per distance |
| Shopping | 1-2 hours |
| Investigation/research | 1-4 hours |
| Crafting | Per DM/rules |
| Downtime activity | Per activity |

After any time advancement:
1. Update World Clock frontmatter (current-day, current-time)
2. Append to Time Log
3. Check for scheduled events that should now fire
4. Fire any due events

### Scene Management

**With session plan:** Track which scene we're in. When the scene's purpose is fulfilled or the players move on:

```markdown
---
**Scene {N+1}: {Name}** ({type})
[[{Location}]] | Day {current-day}, {current-time}
---

{Scene transition narration}
```

**Without session plan:** Transition scenes based on:
- Player actions (they decide to go somewhere new)
- Time passage (night falls, morning comes)
- Events firing (scheduled event changes the situation)
- Natural story beats (the conversation ends, the mystery deepens)

**When players deviate from the plan:**

Flag it to the DM:
```
[NOTE: Players went off-plan -- the plan expected {planned scene}, but they're doing {actual action}. Improvising based on {relevant context}. Want to redirect, or roll with it?]
```

If DM says roll with it, adapt. If DM wants to redirect, use the session plan's contingency/redirect hook.

---

## Quick Commands

Detect these keywords or phrases in DM input and trigger the appropriate response:

### Combat Triggers
**Keywords:** "combat", "roll initiative", "fight", "attack", "they attack", "ambush"

**Action:** Trigger `/dnd:combat` via the Skill tool. Pass monster information from the DM's input. Combat skill handles the full combat loop. When combat ends, resume play mode.

### Loot Trigger
**Keywords:** "loot", "search the bodies", "check for treasure", "what do they find"

**Action:** Trigger `/dnd:loot --drop`. The loot skill generates and distributes loot. Resume play mode.

### Save Trigger
**Keywords:** "save", "save game", "snapshot"

**Action:** Trigger `/dnd:save {campaign}`. The save skill creates a snapshot. Resume play mode.

### Show Mechanics
**Keywords:** "show hood", "show mechanics", "what were the numbers", "show rolls"

**Action:** Reveal the underlying mechanics for the last resolved action:
- Dice rolled, natural values, modifiers
- DC and how it was determined
- Monster stats used
- Any advantage/disadvantage calculations
- Condition effects applied

### Pause
**Keywords:** "pause", "break", "hold on"

**Action:**
1. Save current state (ensure all pending writes are done)
2. Present a brief summary: current scene, HP status, active conditions
3. "Game paused. Say 'resume' to continue."

### Advance Time
**Keywords:** "advance time", "skip ahead", "X hours later", "next morning", "long rest", "short rest"

**Action:**
1. Parse the time duration
2. Advance World Clock
3. Check for scheduled events in the elapsed time
4. Fire any triggered events
5. Describe the passage of time and new state
6. For rests: restore HP/spell slots per 5e rest rules

### New NPC
**Keywords:** "new npc", "create npc", "make an npc"

**Action:** Quick inline NPC generation:
1. Ask for minimal details (name, race, role)
2. Generate personality and voice quickly
3. Write the NPC file
4. Resume play with the new NPC ready for interaction

### Recap
**Keywords:** "recap", "what happened", "where are we"

**Action:** Trigger `/dnd:recap --previous {campaign}`. Present the recap. Resume play.

---

## Narrative Voice

During play, maintain two voices:

**Narrative voice** (scene descriptions, action outcomes):
- Atmospheric, sensory, evocative
- Second person for player actions: "You push open the heavy oak door..."
- Third person for NPC/world actions: "The guard steps forward, hand on sword..."
- Vary sentence length for pacing (short for tension, longer for atmosphere)

**Mechanical voice** (dice, stats, rules):
- Clear, precise, bracketed
- Always show the math: `d20(14) + 5 = 19 vs AC 16 -- Hit`
- Separate from narrative with formatting

Blend both:
```
Aelric swings his greatsword in a wide arc at the ogre's knee.
[Attack: d20(17) + 7 = 24 vs AC 11 -- Hit! Damage: 2d6(4,5) + 4 = 13 slashing]
The blade bites deep into flesh and the ogre howls, staggering sideways and clutching its leg.
```

---

## Session End

When the DM says "wrap up", "end session", "that's a wrap", or similar:

### 1. Write Session Log

Create/update the session file at `1. Campaigns/{campaign}/Sessions/Session {N}.md`:

```yaml
---
type: session
campaign: "[[Campaign]]"
session-number: {N}
date-played: {today}
game-day-start: {day at session start}
game-day-end: {current day}
party-level: {current level}
status: completed
tags:
  - "#dnd/session"
---
```

Body with all events, combat encounters, NPC interactions, state changes, and loot acquired from this session.

### 2. Verify Entity File Integrity

Quick audit -- check that all state changes during the session were persisted:

- NPC memory entries written for all interactions
- Location state history updated for all changes
- Quest files updated for all progress
- PC files reflect current HP, spell slots, inventory
- World Clock reflects final time state

If anything was missed, write it now.

### 3. Auto-Save Snapshot

Trigger `/dnd:save {campaign}` to create a post-session snapshot.

### 4. Update Campaign File

Update `Campaign.md`:
- Increment `session-count`
- Update `party-level` if it changed
- Update `Updated` date

### 5. Present Session Summary

```markdown
---
**Session {N} Complete**
**Duration:** Day {start} to Day {end} | {time-of-day start} to {time-of-day end}
---

### Key Events
- {Event 1}
- {Event 2}
- {Event 3}

### Combat Summary
- {Encounter 1}: {outcome}

### NPC Interactions
- [[{NPC}]]: {summary}

### Quests Updated
- {Quest}: {status change}

### Loot Acquired
- {Items/gold}

### XP Earned
- {Total XP per PC}

---

### Next Session Hooks
- {Hanging thread 1}
- {Unresolved tension}
- {Upcoming scheduled event}
- {Player-expressed interest in X}
```

### 6. Mark Session Plan (If Used)

If a session plan was followed, update its frontmatter to `status: played`.

---

## Agent Delegation

The play skill manages the loop and state persistence. It spawns the `dnd-gm` agent as the primary orchestrator for:

- Narrative generation (scene descriptions, NPC dialogue, action outcomes)
- Mechanical rulings (edge cases, rule interpretations)
- Improvisation (player actions not covered by plan or pre-built content)

The skill retains control of:
- State file reads and writes
- World Clock management
- Quick command routing
- Session start/end protocols
- Encounter/skill delegation

## Edge Cases

- **No PC files exist:** Can't run play without PCs. Direct to `/dnd:init` or ask DM to create PCs.
- **World Clock missing:** Campaign not properly initialized. Create a default World Clock or direct to `/dnd:init`.
- **Session plan references NPCs/locations that don't exist:** Create them on the fly with minimal details, or ask DM.
- **Players want to do something not covered by any system:** Make a ruling, announce it, resolve with an appropriate ability check, and move on. Note the ruling for consistency.
- **Multiple sessions in one day:** Track game time within the day using current-time advancement.
- **DM wants to retcon something:** Apply the retcon to state files, note it in the session log: "RETCON: {what changed and why}".
- **Technical interruption (connection lost, etc.):** State is persisted after every action, so resuming picks up from the last written state. Run a quick integrity check on resume.
