---
name: "dnd"
description: "D&D 5e game engine -- main entry point. Routes to subcommands or shows campaign status. Use for any D&D related request."
---

# /dnd -- D&D 5e Game Engine

Main entry point for all D&D operations. Routes to subcommands or displays active campaign status.

## Input

$ARGUMENTS -- subcommand and its arguments, or empty for status dashboard.

## Setup

1. Read the domain CLAUDE.md at `2. Areas/2.2 Dungeons & Dragons/CLAUDE.md`

All paths below are relative to `~/docs/Documents/2. Areas/2.2 Dungeons & Dragons/`.

## Routing

### 1. Check for Subcommand

Parse the first word of `$ARGUMENTS` against the subcommand table:

| Subcommand | Skill | Purpose |
|------------|-------|---------|
| `play` | `/dnd:play` | Live game execution engine |
| `plan` | `/dnd:plan` | Session planning interview |
| `campaign` | `/dnd:campaign` | Campaign arc planning and status |
| `combat` | `/dnd:combat` | Combat encounter management |
| `npc` | `/dnd:npc` | NPC interaction and creation |
| `world` | `/dnd:world` | World building and location management |
| `quest` | `/dnd:quest` | Quest lifecycle management |
| `loot` | `/dnd:loot` | Loot generation and shopping |
| `encounter` | `/dnd:encounter` | Encounter generation |
| `homebrew` | `/dnd:homebrew` | Homebrew content creation |
| `save` | `/dnd:save` | Save/restore game state |
| `recap` | `/dnd:recap` | Session recap and continuity |
| `lookup` | `/dnd:lookup` | Quick reference lookup (API) |
| `init` | `/dnd:init` | Initialize a new campaign |
| `map` | `/dnd:map` | ASCII tactical map for whiteboard |

If a subcommand is matched:
- Strip the subcommand from `$ARGUMENTS`
- Route to the matching skill with the remaining arguments via the Skill tool

### 2. No Subcommand -- Show Status Dashboard

If `$ARGUMENTS` is empty or doesn't match a subcommand, display the active campaign status.

#### Find Active Campaigns

Glob `1. Campaigns/*/Campaign.md`. Read each and filter for `status: active`.

#### Single Active Campaign

If exactly one active campaign, show its dashboard:

```markdown
# D&D Engine -- {Campaign Name}

**System:** D&D 5e | **Setting:** {setting} | **Source:** {source}
**Sessions:** {session-count} | **Level:** {party-level} | **Day:** {current-day}, {current-time}

## Party

| PC | Class | Level | HP | Status |
|----|-------|-------|-----|--------|
{rows from Party/ files}

## Active Quests ({count})

- **{Quest 1}** ({priority}) -- {brief status}
- **{Quest 2}** ({priority}) -- {brief status}

## Recent Activity

- **Last session:** {date} -- {one-line recap}
- **Next scheduled event:** Day {N} -- {event description}

## Subcommands

| Command | Description |
|---------|-------------|
| `/dnd play` | Start or resume a live game session |
| `/dnd plan` | Plan the next session (structured interview) |
| `/dnd campaign` | View full dashboard or plan campaign arc |
| `/dnd combat` | Start a combat encounter |
| `/dnd npc {name}` | Interact with or create an NPC |
| `/dnd world {location}` | Describe, create, or travel to a location |
| `/dnd quest` | Create, update, or list quests |
| `/dnd loot` | Generate loot, shop, or roll on tables |
| `/dnd encounter` | Generate random or designed encounters |
| `/dnd homebrew` | Create custom monsters, spells, items, rules |
| `/dnd save` | Save or restore game state |
| `/dnd recap` | Session recaps and prep briefs |
| `/dnd lookup {type} {name}` | Look up official 5e content |
| `/dnd init` | Initialize a new campaign |
```

#### Multiple Active Campaigns

If multiple active campaigns:

```markdown
# D&D Engine -- Active Campaigns

| Campaign | Setting | Sessions | Level | Last Played |
|----------|---------|----------|-------|-------------|
{row per active campaign}

Select a campaign by name, or use a subcommand:
- `/dnd play {campaign}` -- start playing
- `/dnd campaign {campaign}` -- view full dashboard
- `/dnd plan {campaign}` -- plan next session
```

#### No Active Campaigns

If no active campaigns found:

```markdown
# D&D Engine

No active campaigns found.

**Get started:**
- `/dnd init` -- Initialize a new campaign
- `/dnd lookup {type} {name}` -- Look up 5e content (works without a campaign)
- `/dnd homebrew` -- Create homebrew content (works without a campaign)
```

### 3. Ambiguous Input

If `$ARGUMENTS` doesn't clearly match a subcommand but looks like it could be a campaign name:
- Search `1. Campaigns/` for a matching directory
- If found, show that campaign's dashboard
- If not found, show the subcommand list and ask what the user meant

## Edge Cases

- **Subcommand with no further arguments:** Route to the skill with empty arguments (each skill handles its own missing-argument prompting).
- **Typos in subcommand:** Fuzzy match -- if input is close to a subcommand (e.g., "combay" -> "combat"), suggest the match.
- **User says just a campaign name:** Show that campaign's status dashboard (same as `/dnd campaign status {name}`).
- **D&D domain directory doesn't exist:** Warn that the D&D vault structure needs to be created. Offer to set it up.
