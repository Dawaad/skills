---
name: "dnd:map"
description: "Generate ASCII top-down tactical maps of the current environment, encounter, or location for whiteboard drawing. Shows terrain, objects, doors, elevation, and interactable elements with a legend."
---

# /dnd:map -- ASCII Tactical Map Generator

Generates top-down ASCII maps designed to be drawn on a whiteboard for players. Maps include terrain features, objects, doors, elevation markers, and interactive elements with a clear legend.

## Input

$ARGUMENTS -- expects one of:
- `{location-name}` -- generate map from an existing location file
- `{encounter-name}` -- generate map from a pre-built encounter file
- `--live` -- generate map from the current scene in an active play session
- `--custom` -- freeform map creation from DM description
- Empty -- detect context (active combat? current location?) or ask

## Setup

1. Read the domain CLAUDE.md at `2. Areas/2.2 Dungeons & Dragons/CLAUDE.md`
2. Read entity schemas from `2. Areas/2.2 Dungeons & Dragons/_Config/Tag Taxonomy.md`

All paths below are relative to `~/docs/Documents/2. Areas/2.2 Dungeons & Dragons/`.

---

## Mode Detection

Parse `$ARGUMENTS`:
- If a location name is given, search `2. World/Locations/` for the file
- If an encounter name is given, search active campaign `Combat/` directory
- If `--live`, read the current scene context from the active session/combat
- If `--custom`, interview the DM for layout details
- If empty, check for active combat (read recent encounter files with `status: active`) or current location from World Clock

---

## Map Generation

### 1. Gather Spatial Information

**From a location file:**
- Read the location file, extract Key Features, Description, NPCs Present
- If location-type is `dungeon`, extract room layout from the room-by-room key
- For towns/cities, focus on the specific area the party is in (ask DM: "Which part? The tavern interior? The market square? The whole town overview?")

**From an encounter file:**
- Read the encounter file, extract Terrain, Starting Positions, monsters
- Read the location file linked in the encounter's `location:` field
- Extract environmental hazards and tactical features

**From active combat (`--live`):**
- Read the active encounter file
- Read the current initiative table for combatant positions
- Infer positions from the round log if not explicitly tracked

**From DM description (`--custom`):**
- Interview the DM:
  - "What kind of space? (room, cave, clearing, street, building interior, etc.)"
  - "Rough dimensions? (small ~30ft, medium ~60ft, large ~100ft, huge ~200ft)"
  - "Key features? (pillars, tables, pit, water, elevation changes, doors)"
  - "Entry/exit points?"
  - "Any hazards or interactable elements?"

### 2. Determine Scale

Choose grid scale based on the space:
- **Small (interior room, 20-40ft):** 1 char = 5ft (standard combat grid)
- **Medium (large hall, courtyard, 40-80ft):** 1 char = 5ft
- **Large (outdoor area, building complex, 80-200ft):** 1 char = 10ft
- **Huge (town overview, wilderness, 200ft+):** 1 char = 20ft or more

Announce the scale clearly in the legend.

### 3. Build the ASCII Map

Use this symbol set consistently:

**Structural:**
```
#   Wall / solid boundary
.   Open floor / ground
~   Water (shallow or deep -- note in legend)
,   Grass / soft ground
^   Trees / dense vegetation
=   Bridge / wooden platform
_   Road / path
|   Vertical wall or barrier
-   Horizontal wall or barrier
+   Wall intersection / corner
```

**Doors & Passages:**
```
D   Door (standard)
Ð   Door (locked -- use D* if terminal doesn't support)
O   Open doorway / archway
▽   Stairs down (use v if no unicode)
△   Stairs up (use ^ if no unicode -- disambiguate from trees in legend)
/   Slope / ramp
```

**Elevation:**
```
1   Elevation level 1 (ground)
2   Elevation level 2 (+10ft)
3   Elevation level 3 (+20ft)
░   Pit / lower elevation (use _ if no unicode)
```

**Objects & Features:**
```
T   Table / furniture
P   Pillar / column
C   Chest / container
A   Altar / pedestal
F   Fire / brazier / torch
B   Barrel / crate
S   Statue
W   Well / fountain
```

**Interactable Elements (mark with ! prefix in legend):**
```
!   Interactable element (always mark these prominently)
X   Trap location (DM only -- don't show to players)
*   Hazard zone boundary
@   Interactable object (chandelier, lever, rope, etc.)
```

**Combatants (for encounter maps):**
```
J   Jasper (or first letter of PC name)
E   Esmeralda
A   Aurelia
C   Clemenza
R   Renesmea
O   Opal
g   Goblin (lowercase for enemies)
b   Bugbear
s   Skeleton
(number enemies if multiples: g1 g2 g3)
```

### 4. Map Layout Rules

**Grid structure:**
- Use a clear border of `#` for enclosed spaces
- Number the Y-axis (rows) on the left edge
- Letter the X-axis (columns) across the top
- Use consistent spacing -- each cell is exactly 1 character wide
- Add compass rose: `N↑` or `N` arrow indicator

**Dimensions:**
- Target 20-40 characters wide and 15-30 characters tall
- This maps well to a whiteboard at ~5ft per square
- For larger areas, indicate that the map continues or use reduced scale

**Readability for whiteboard:**
- Keep it simple -- a DM needs to reproduce this with a marker
- Use straight lines, avoid diagonal walls where possible
- Group furniture/objects logically
- Leave space for combatant tokens

### 5. Generate the Map

Output the map in a fenced code block with the grid:

```
Example -- Tavern Common Room (1 char = 5ft, 40x30ft)

        N
        ↑
    A B C D E F G H
   ┌────────────────┐
 1 │##D#############│
 2 │#..............#│
 3 │#.TT....TT....#│
 4 │#.TT....TT..P.#│
 5 │#..............#│
 6 │#....FF........#│
 7 │#.BB..........O│  ← Kitchen
 8 │#.BB...TT.....#│
 9 │#......TT..S..#│
10 │####D####D#####│
        ↓
      Entrance
```

### 6. Generate the Legend

Always include a complete legend below the map:

```markdown
## Legend

**Scale:** 1 square = 5ft
**Dimensions:** 40ft × 50ft

### Symbols
- `#` — Stone wall
- `.` — Wooden floor
- `D` — Door (unlocked)
- `O` — Open archway (to kitchen)
- `T` — Table (4-person, wooden)
- `F` — Fireplace (lit, provides warmth and light)
- `B` — Barrel (ale storage)
- `P` — Support pillar (provides half cover)
- `S` — Mounted stag head (decorative)

### Interactable Elements
- `F` (Row 6, C-D) — **Fireplace** → Can be kicked to scatter embers (DEX save DC 12, 1d6 fire in 10ft cone). Can light weapons/arrows.
- `B` (Row 7-8, B-C) — **Ale barrels** → Can be tipped to create difficult terrain (10ft area). Flammable — if ignited, 2d6 fire damage in area.
- `P` (Row 4, G) — **Stone pillar** → Provides half cover (+2 AC). Can be toppled with STR DC 18 — 3d6 bludgeoning in 10ft line.

### Elevation
- Entire room is ground level. Fireplace hearth is slightly raised (no mechanical effect).

### Notes for Whiteboard
- Draw walls as thick lines
- Mark doors with a gap and small arc
- Use X marks for table positions
- Circle the interactable elements
```

### 7. DM-Only vs Player Version

Generate TWO versions when traps or secrets are present:

**Player version:** Omit trap markers (`X`), secret doors, and hidden elements. Show only what's visible.

**DM version:** Full map with all traps, secret doors, hidden passages, and tactical notes.

Label each clearly:
```
## Player Map (safe to show)
{map without secrets}

## DM Map (your eyes only)
{full map with everything}
```

If no secrets exist, generate a single map.

### 8. Encounter Positioning

When generating a map for an active or planned encounter:

- Place combatants using their initial letters
- Show starting distances
- Mark engagement zones (where melee can reach)
- Highlight interactable elements that could change the fight
- Note cover positions

```
Encounter Setup -- Goblin Ambush at Cragmaw Bridge

    A B C D E F G H I J K L
   ┌────────────────────────┐
 1 │^^^^....~~~~....~~~~^^^^│
 2 │^^^.....~~~~....~~~~.^^^│
 3 │^^..g1..====....====..^^│
 4 │^........====@===.....^│  ← @=rope anchor
 5 │...J.E.A............g2.│
 6 │...O.C.R.....BB........│
 7 │^^..............g3...^^│
 8 │^^^.....~~~~....~~~~.^^^│
 9 │^^^^....~~~~....~~~~^^^^│
   └────────────────────────┘

Scale: 1 char = 5ft | Bridge spans rows 3-4
```

---

## Output Format

Present the final output as:

1. **Map title** with location name and context
2. **ASCII map** in a code block
3. **Legend** with all symbols explained
4. **Interactable elements** with DCs and effects (highlighted)
5. **Whiteboard tips** — specific advice for drawing this on a whiteboard (simplifications, what to emphasize, where to place minis/tokens)

---

## Iteration

After presenting the map, ask:
- "Adjust anything? (add features, change scale, move elements)"
- "Generate a player-safe version?" (if DM version was shown)
- "Add encounter positions?" (if no combatants placed yet)
- "Map an adjacent area?" (for dungeon exploration)

Apply changes and regenerate. Maps are iterative -- expect 1-3 rounds of refinement before the DM is happy.

## Edge Cases

- **Very large areas (towns, wilderness):** Use abstract overview maps with labeled points of interest rather than detailed grids. Not every building needs interior detail.
- **Multi-level locations:** Generate separate maps per level, clearly labeled "Level 1", "Level 2". Mark stair connections.
- **Irregular cave shapes:** Use `.` for open space and `#` for walls. Caves don't need to be rectangular -- use jagged wall lines.
- **Moving encounter (chase, vehicle):** Generate a scrolling strip map showing the chase path with obstacles and branch points.
- **Outdoor combat with no walls:** Use terrain features (trees, rocks, streams, elevation) as the structural elements instead of walls. Border with `~` for the edge of the mapped area.
- **Location file has no spatial details:** Infer from the description and type. A tavern has a common room, a bar, stairs. A cave has an entrance, chambers, passages. Ask the DM to confirm your interpretation.
