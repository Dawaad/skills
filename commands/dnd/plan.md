---
name: "dnd:plan"
description: "Session planning interview. Structured 7-stage conversation that loads campaign state, builds story arcs, pre-builds encounters, preps NPCs, generates loot, plants secrets, and plans pacing. Outputs a complete session plan file."
---

# /dnd:plan -- Session Planning Interview

A structured 7-stage interview that builds a complete session plan. Conversational, state-aware, and builds on established campaign context.

## Input

$ARGUMENTS -- campaign name (required). If omitted, list active campaigns and ask.

## Setup

1. Read the domain CLAUDE.md at `2. Areas/2.2 Dungeons & Dragons/CLAUDE.md`
2. Read entity schemas from `2. Areas/2.2 Dungeons & Dragons/_Config/Tag Taxonomy.md`

All paths below are relative to `~/docs/Documents/2. Areas/2.2 Dungeons & Dragons/`.

## Pre-Interview: Determine Session Number

1. Read `1. Campaigns/{campaign}/Campaign.md` -- get session-count
2. Glob `1. Campaigns/{campaign}/Sessions/Session Plan*.md` -- find highest plan number
3. New session plan number = max(session-count + 1, highest plan number + 1)

---

## Stage 1: Context Loading

### 1.1 Read Campaign State

Read ALL of the following before presenting anything:

- `1. Campaigns/{campaign}/Campaign.md` -- overview, party level, session count
- `1. Campaigns/{campaign}/State/World Clock.md` -- current day, time, scheduled events
- `1. Campaigns/{campaign}/State/` -- all quest files (`type: quest`)
- `1. Campaigns/{campaign}/State/` -- all plot-thread files (`type: plot-thread`)
- Most recent completed session file in `Sessions/`
- NPC files referenced in the most recent session (read their Memory sections)
- PC files in `Party/` -- levels, HP, spell slots, key items

### 1.2 Present State Summary

Present a concise "where we are" summary:

```markdown
## Campaign State -- {Campaign Name}

**Session:** Planning for Session {N}
**Game Day:** {current-day}, {current-time}
**Party Level:** {level}
**Location:** {where they are now}

### Last Session Recap
{2-3 sentence summary from most recent session log}

### Active Quests ({count})
- **{Quest 1}** ({priority}) -- {status/progress summary}. {Deadline: Day X / No deadline}
- **{Quest 2}** ...

### Active Plot Threads ({count})
- **{Thread 1}** ({urgency}) -- {current state}
- **{Thread 2}** ...

### Scheduled Events (Next 10 Days)
| Day | Event | Notes |
|-----|-------|-------|
{events where day <= current-day + 10 and triggered = false}

### NPC Tensions
{NPCs with relationship-score at extremes or unresolved interactions}
```

### 1.3 Ask Session Focus

"Here's where we left off. What's the focus of this session?"

Offer options:
- **Main plot** -- advance the central storyline
- **Side quest** -- focus on a specific side quest
- **Downtime** -- shopping, crafting, roleplaying, training
- **Player-driven** -- follow up on something specific a player wants
- **Specific scene** -- DM has a particular scene in mind

---

## Stage 2: Story Arc

### 2.1 Dramatic Question

Ask: "What's the dramatic question for this session? What should be resolved or at stake?"

A dramatic question is a yes/no tension: "Will the party save the village before the cult ritual?" "Can they earn the trust of the dragon?" "Will they discover the traitor?"

If the DM is unsure, suggest 2-3 based on active plot threads and quest states.

### 2.2 Target Ending

Ask: "How do you want this session to ideally end? What state should things be in?"

This gives directionality to the session plan.

### 2.3 Plot Thread Selection

Present active plot threads sorted by urgency. Suggest which are "ripe" for advancement:

- Threads at `climax` status need resolution soon
- Threads with `high` or `critical` urgency are pressing
- Threads connected to upcoming scheduled events are naturally ripe
- Threads the party has been actively engaging with have momentum

Ask: "Which threads should we advance? Any to introduce?"

### 2.4 Story Beats

Ask: "Any specific beats you want to hit?"

- Revelations (a secret is uncovered)
- Betrayals (an ally turns)
- Confrontations (face-to-face with an antagonist)
- Discoveries (new location, item, or lore)
- Consequences (past actions come home)

### 2.5 Build Scene Outline

Based on all input, draft an ordered scene outline:

```markdown
## Scene Outline

1. **{Scene Name}** ({type: combat/social/exploration/travel/downtime})
   - *Setting:* {where}
   - *Purpose:* {what this scene accomplishes}
   - *Transition to next:* {how we move to scene 2}

2. **{Scene Name}** ({type})
   ...
```

Present and ask: "Does this flow work? Anything to add, remove, or reorder?"

---

## Stage 3: Scenes & Encounters

Iterate through each scene in the outline. For each:

### Combat Scenes
- Who are they fighting? (specific monsters or "appropriate threat")
- What's the CR target?
- What's the terrain? (open field, dungeon room, city street, forest clearing)
- Spawn `dnd-monster-manual` agent to select and pre-fetch stat blocks
- Pre-build the encounter file (write to `Combat/` via the encounter schema)
- Note: encounter file is ready for `/dnd:combat` to pick up during play

### Social Scenes
- Which NPCs are involved?
- Read those NPC files -- check disposition, memory, knowledge
- Flag any grudges or consequences from past interactions
- What do the NPCs want from the party?
- What does the party need from the NPCs?
- What are possible outcomes?

### Exploration Scenes
- What location? Read the location file or note that it needs to be created.
- If new area, spawn `dnd-world-builder` agent to draft it
- What can they discover?
- What skill checks are involved and at what DCs?

### Travel Scenes
- Origin and destination
- Estimated travel time
- Random encounter likelihood (danger level of route)
- Pre-roll encounters or leave to play mode?

### Downtime Scenes
- What activities? (shopping, crafting, research, training, socializing)
- Time cost? (advance World Clock planning)
- Available services at current location?

For each scene, ask: "What if the players go off-script here? What's the contingency?"

---

## Stage 4: NPCs & Dialogue Prep

### 4.1 NPC Roster

List all NPCs appearing in the planned scenes. For each, show:

```markdown
### NPC Prep

| NPC | Scene | Disposition | Last Interaction | Key Knowledge |
|-----|-------|-------------|-----------------|---------------|
| [[{Name}]] | {scene #} | {disposition} | Day {N}: {summary} | {what they know relevant to this session} |
```

### 4.2 New NPCs Needed

Ask: "Any new NPCs needed for this session?"

If yes, create them via the NPC creation workflow (ask details, generate personality/knowledge, write file).

### 4.3 Disposition & Knowledge Updates

Ask: "Before the session, should any NPC dispositions or knowledge change?"

- External events between sessions may shift NPC attitudes
- NPCs may have learned new information off-screen
- Faction politics may have changed relationships

Apply any changes immediately to NPC files.

### 4.4 Key Dialogue Moments

Ask: "Any specific dialogue moments you want to prepare?"

For each key dialogue moment:
- Which NPC
- What's the emotional beat
- What information is conveyed
- Draft a sample opening line in the NPC's voice (using their speech pattern from the Personality section)

---

## Stage 5: Loot & Rewards

### 5.1 Combat Loot

For each planned combat encounter:
- Suggest CR-appropriate treasure based on DMG guidelines
- Ask DM to confirm, modify, or skip

### 5.2 Quest Rewards

Review quests that might be completed this session:
- Check the quest file's `reward:` field
- Ask: "Is {quest} likely to be completed? Should we prep the reward?"
- If yes, detail the reward and any bonus rewards for exceptional play

### 5.3 Discovery Rewards

For exploration scenes:
- Suggest items, gold, or lore rewards for discoveries
- Offer to pre-generate magic items for important finds (spawn `dnd-gear-master`)

### 5.4 Pre-Generate If Requested

If DM wants loot pre-generated:
- Spawn `dnd-loot-dropper` for combat loot
- Spawn `dnd-gear-master` for specific items
- Include all loot details in the session plan

---

## Stage 6: Secrets & Clues

### 6.1 Information to Discover

Ask: "What information should the party discover this session?"

For each secret or clue:
- What is the information?
- Why does it matter? (advances which quest/thread?)
- Is it true, partially true, or a red herring?

### 6.2 Multiple Discovery Paths

For each piece of information, design at least 2 ways the party can find it:

```markdown
### Secret: {description}

**Path 1:** {NPC} reveals it during {scene} if disposition is {threshold} or better.
**Path 2:** Investigation check (DC {N}) at {location} reveals {clue pointing to it}.
**Path 3:** Found in {document/book/letter} at {location}.
```

This ensures information isn't gated behind a single skill check or NPC interaction.

### 6.3 Foreshadowing

Ask: "Any foreshadowing for future sessions?"

For each foreshadowing element:
- What's being foreshadowed?
- How is it presented? (NPC offhand comment, environmental detail, dream/vision)
- When does the payoff come?

---

## Stage 7: Pacing & Contingencies

### 7.1 Session Length

Ask: "How long is this session? (hours)"

Based on length, assess the scene outline:
- 2-3 hours: 3-4 scenes max, keep it focused
- 4 hours: 4-6 scenes, room for one detailed combat
- 5+ hours: Full session, multiple combats possible

### 7.2 Must-Hit Scene

Ask: "Which scene absolutely must happen this session?"

Mark it in the plan. Ensure it's positioned so it happens even if earlier scenes run long.

### 7.3 Cut-If-Needed Scene

Ask: "Which scene can be cut or deferred if we run long?"

Mark it in the plan as optional/deferrable.

### 7.4 Off-Rails Contingency

Ask: "What if the players go completely off the plan?"

Design a flexible redirect hook:
- A way to bring the dramatic question back into play regardless of player choices
- An NPC who can deliver critical information in any location
- A scheduled event that fires regardless of player position

### 7.5 Time Targets

Assign rough time estimates to each scene:

```markdown
| Scene | Estimated Time | Priority |
|-------|---------------|----------|
| Scene 1: Opening | 20 min | Must-hit |
| Scene 2: Investigation | 30 min | Flexible |
| Scene 3: Boss Fight | 45 min | Must-hit |
| Scene 4: Aftermath | 15 min | Cut-if-needed |
```

---

## Output: Write Session Plan File

After all 7 stages are complete, write the session plan.

Write to `1. Campaigns/{campaign}/Sessions/Session Plan {NNN}.md`:

```yaml
---
type: session-plan
campaign: "[[Campaign]]"
session-number: {NNN}
planned-date: {today or DM-specified date}
game-day-start: {current World Clock day}
dramatic-question: "{dramatic question}"
target-ending: "{target ending state}"
estimated-scenes: {count}
status: planned
tags:
  - "#dnd/session"
---
```

Body includes ALL sections from the interview:

```markdown
# Session Plan {NNN} -- {Campaign Name}

## Story Arc

### Dramatic Question
{The dramatic question}

### Target Ending
{Ideal end state}

### Plot Threads in Play
- {Thread 1} -- {how it advances}
- {Thread 2} -- {how it advances}

## Scene Outline

{Full scene outline with details from Stage 3}

### Scene 1: {Name}
**Type:** {type} | **Location:** [[{location}]] | **Est. Time:** {minutes} min | **Priority:** {must-hit/flexible/cut-if-needed}

{Full scene details: setup, NPCs, encounters, skill checks, possible outcomes}

### Scene 2: {Name}
...

## Pre-built Encounters

{List all encounter files created during planning, with links}
- [[{Encounter 1}]] -- {brief description}, {difficulty}

## NPC Prep

{NPC roster table from Stage 4}

### Key Dialogue
{Any prepared dialogue beats}

## Loot & Rewards

### Combat Loot
{Per-encounter loot details}

### Quest Rewards
{Expected quest completions and their rewards}

### Discovery Rewards
{Items/gold/lore from exploration}

## Secrets & Clues

{For each secret: the info, why it matters, discovery paths}

### Foreshadowing
{Elements planted for future sessions}

## Pacing Notes

- **Session length:** {hours}
- **Must-hit scene:** {scene name}
- **Cut-if-needed:** {scene name}
- **Time targets:** {table from Stage 7}

## Contingencies

### Off-Rails Plan
{What to do if players diverge}

### Redirect Hook
{How to bring the story back}

### Scene-Specific Contingencies
{Per-scene "what if" plans from Stage 3}
```

---

## Post-Output

After writing the plan, present:
- Session plan file path
- Quick summary: "{N} scenes planned, {M} encounters pre-built, {K} NPCs prepped"
- "Ready for `/dnd:play` when the session starts."
- Offer to adjust any section

## Interview Navigation

The interview is conversational. The DM can:
- Skip a stage: "Skip loot" -> move to next stage
- Revisit a stage: "Go back to scenes" -> return to that stage
- Ask for suggestions at any point: "What do you think?" -> offer recommendations based on state
- End early: "That's enough" -> write the plan with what we have, mark incomplete sections

Track which stages are complete and which are pending. Present stage navigation at any time:

```
Stages: [1. Context] [2. Story Arc] [3. Scenes] [4. NPCs] [5. Loot] [6. Secrets] [7. Pacing]
         DONE         DONE           IN PROGRESS  pending   pending   pending     pending
```

## Edge Cases

- **No previous sessions:** First session -- skip recap, focus on opening scene and character introductions.
- **No active quests or threads:** New campaign or fresh start. Focus on world introduction and hook planting.
- **DM has no plan:** Guide more heavily. Suggest dramatic questions, offer scene ideas based on state.
- **DM already has everything planned:** Act as scribe. Take their input, organize it into the session plan format.
- **Session plan already exists for this number:** Warn and ask to overwrite or increment.
- **Campaign not found:** List available campaigns, offer to create one with `/dnd:init`.
