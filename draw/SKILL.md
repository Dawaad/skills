---
name: draw
description: Create Excalidraw diagram JSON files that make visual arguments. Use when the user wants to visualise workflows, architectures, or concepts.
---

# Excalidraw Diagram Creator

Generate `.excalidraw` JSON files that **argue visually**, not just display information.

**Setup:** If the user asks you to set up this skill (renderer, dependencies, etc.), see `README.md` for instructions.

## Customisation

**All colours and brand-specific styles live in one file:** `references/color-palette.md`. Read it before generating any diagram and use it as the single source of truth for all colour choices - shape fills, strokes, text colours, evidence artifact backgrounds, everything.

To make this skill produce diagrams in your own brand style, edit `color-palette.md`. Everything else in this file is universal design methodology and Excalidraw best practices.

---

## Core Philosophy

**Diagrams should ARGUE, not DISPLAY.**

A diagram isn't formatted text. It's a visual argument that shows relationships, causality, and flow that words alone can't express. The shape should BE the meaning.

**The Isomorphism Test**: If you removed all text, would the structure alone communicate the concept? If not, redesign.

**The Education Test**: Could someone learn something concrete from this diagram, or does it just label boxes? A good diagram teaches - it shows actual formats, real event names, concrete examples.

---

## Depth Assessment (Do This First)

Before designing, determine what level of detail this diagram needs:

### Simple/Conceptual Diagrams
Use abstract shapes when:
- Explaining a mental model or philosophy
- The audience doesn't need technical specifics
- The concept IS the abstraction (e.g., "separation of concerns")

### Comprehensive/Technical Diagrams
Use concrete examples when:
- Diagramming a real system, protocol, or architecture
- The diagram will be used to teach or explain (e.g., YouTube video)
- The audience needs to understand what things actually look like
- You're showing how multiple technologies integrate

**For technical diagrams, you MUST include evidence artifacts** (see below).

---

## Research Mandate (For Technical Diagrams)

**Before drawing anything technical, research the actual specifications.**

If you're diagramming a protocol, API, or framework:
1. Look up the actual JSON/data formats
2. Find the real event names, method names, or API endpoints
3. Understand how the pieces actually connect
4. Use real terminology, not generic placeholders

Bad: "Protocol" -> "Frontend"
Good: "AG-UI streams events (RUN_STARTED, STATE_DELTA, A2UI_UPDATE)" -> "CopilotKit renders via createA2UIMessageRenderer()"

**Research makes diagrams accurate AND educational.**

---

## Evidence Artifacts

Evidence artifacts are concrete examples that prove your diagram is accurate and help viewers learn. Include them in technical diagrams.

**Types of evidence artifacts** (choose what's relevant to your diagram):

| Artifact Type | When to Use | How to Render |
|---------------|-------------|---------------|
| **Code snippets** | APIs, integrations, implementation details | Dark rectangle + syntax-coloured text (see colour palette for evidence artifact colours) |
| **Data/JSON examples** | Data formats, schemas, payloads | Dark rectangle + coloured text (see colour palette) |
| **Event/step sequences** | Protocols, workflows, lifecycles | Timeline pattern (line + dots + labels) |
| **UI mockups** | Showing actual output/results | Nested rectangles mimicking real UI |
| **Real input content** | Showing what goes IN to a system | Rectangle with sample content visible |
| **API/method names** | Real function calls, endpoints | Use actual names from docs, not placeholders |

**Example**: For a diagram about a streaming protocol, you might show:
- The actual event names from the spec (not just "Event 1", "Event 2")
- A code snippet showing how to connect
- What the streamed data actually looks like

**Example**: For a diagram about a data transformation pipeline:
- Show sample input data (actual format, not "Input")
- Show sample output data (actual format, not "Output")
- Show intermediate states if relevant

The key principle: **show what things actually look like**, not just what they're called.

---

## Multi-Zoom Architecture

Comprehensive diagrams operate at multiple zoom levels simultaneously. Think of it like a map that shows both the country borders AND the street names.

### Level 1: Summary Flow
A simplified overview showing the full pipeline or process at a glance. Often placed at the top or bottom of the diagram.

### Level 2: Section Boundaries
Labelled regions that group related components. These create visual "rooms" that help viewers understand what belongs together.

### Level 3: Detail Inside Sections
Evidence artifacts, code snippets, and concrete examples within each section. This is where the educational value lives.

**For comprehensive diagrams, aim to include all three levels.**

### Bad vs Good

| Bad (Displaying) | Good (Arguing) |
|------------------|----------------|
| 5 equal boxes with labels | Each concept has a shape that mirrors its behaviour |
| Card grid layout | Visual structure matches conceptual structure |
| Icons decorating text | Shapes that ARE the meaning |
| Same container for everything | Distinct visual vocabulary per concept |
| Everything in a box | Free-floating text with selective containers |

### Simple vs Comprehensive

| Simple Diagram | Comprehensive Diagram |
|----------------|----------------------|
| Generic labels: "Input" -> "Process" -> "Output" | Specific: shows what the input/output actually looks like |
| Named boxes: "API", "Database", "Client" | Named boxes + examples of actual requests/responses |
| "Events" or "Messages" label | Timeline with real event/message names from the spec |
| "UI" or "Dashboard" rectangle | Mockup showing actual UI elements and content |
| ~30 seconds to explain | ~2-3 minutes of teaching content |
| Viewer learns the structure | Viewer learns the structure AND the details |

---

## Container vs. Free-Floating Text

**Not every piece of text needs a shape around it.** Default to free-floating text. Add containers only when they serve a purpose.

| Use a Container When... | Use Free-Floating Text When... |
|------------------------|-------------------------------|
| It's the focal point of a section | It's a label or description |
| It needs visual grouping with other elements | It's supporting detail or metadata |
| Arrows need to connect to it | It describes something nearby |
| The shape itself carries meaning | It's a section title, subtitle, or annotation |
| It represents a distinct "thing" in the system | Typography alone creates sufficient hierarchy |

**Typography as hierarchy**: Use font size, weight, and colour to create visual hierarchy without boxes.

**The container test**: For each boxed element, ask "Would this work as free-floating text?" If yes, remove the container.

---

## Common Layout Mistakes

**Read `references/layout-gotchas.md` before generating JSON.** It documents 10 common issues found during render validation (fan-out label collisions, zone opacity, arrow-label overlap, column alignment, etc.) with proven fixes. These patterns were learned from real diagram builds and will save you render-fix cycles.

---

## Design Process (Do This BEFORE Generating JSON)

### Step 0: Assess Depth Required
Determine if this is a simple conceptual diagram or a comprehensive technical one. This drives every subsequent decision.

### Step 1: Understand Deeply
Read/research the subject. For technical diagrams, look up actual specs, formats, and terminology.

### Step 2: Map Concepts to Patterns

| If the concept... | Use this pattern |
|-------------------|------------------|
| Spawns multiple outputs | **Fan-out** |
| Combines inputs into one | **Convergence** |
| Has hierarchy/nesting | **Tree** |
| Is a sequence of steps | **Timeline** |
| Loops or improves continuously | **Spiral/Cycle** |
| Is an abstract state or context | **Cloud** |
| Transforms input to output | **Assembly line** |
| Compares two things | **Side-by-side** |
| Separates into phases | **Gap/Break** |

### Step 3: Ensure Variety
Don't use the same shape for everything. Each concept should have a visually distinct representation.

### Step 4: Sketch the Flow
Plan the spatial layout before writing JSON. Think about reading direction, visual weight, and whitespace.

### Step 5: Generate JSON
Build section by section (see Large Diagram Strategy below). Reference `element-templates.md` for correct JSON structure.

### Step 6: Render & Validate (MANDATORY)
Every diagram must be rendered and visually checked. See Render & Validate section below.

---

## Large / Comprehensive Diagram Strategy

**Build JSON one section at a time.** Do NOT attempt to generate the entire file in a single pass.

### The Section-by-Section Workflow

**Phase 1: Build each section**
1. Create the base file with JSON wrapper and first section
2. Add one section per edit
3. Use descriptive string IDs (e.g., "content-production-box", not "r1")
4. Namespace seeds by section (100xxx, 200xxx, etc.)
5. Update cross-section bindings as you go

**Phase 2: Review the whole**
Read the full JSON and check for overlapping coordinates, missing bindings, and consistent spacing.

**Phase 3: Render & validate**
Run the renderer and visually inspect. Fix issues and re-render.

---

## Visual Pattern Library

### Fan-Out
One source splits into multiple destinations. Use when a single input produces multiple outputs.

### Convergence
Multiple inputs combine into one output. The inverse of fan-out.

### Tree
Hierarchical parent-child relationships. Use for org charts, taxonomies, or component trees.

### Timeline
Sequential steps along a line. Use for processes, protocols, or event sequences.

### Spiral/Cycle
Continuous improvement or feedback loops. Use for iterative processes.

### Cloud
Overlapping ellipses creating a fuzzy boundary. Use for abstract states, contexts, or environments.

### Assembly Line
Linear transformation: input enters, processing happens, output exits. Use for data pipelines.

### Side-by-Side
Two parallel structures for comparison. Use for before/after, old/new, or option A vs B.

### Gap/Break
Visual separation between phases or domains. Use whitespace or a dashed line.

### Lines as Structure
Lines without arrowheads can create visual structure (timelines, brackets, underlines) without implying flow.

---

## Shape Meaning

| Concept Type | Shape | Why |
|--------------|-------|-----|
| Labels, descriptions | **none** (free-floating text) | Typography creates hierarchy |
| Section titles | **none** (free-floating text) | Font size/weight is enough |
| Markers on timeline | small `ellipse` (10-20px) | Visual anchor |
| Start, trigger | `ellipse` | Soft, origin-like |
| End, output | `ellipse` | Completion |
| Decision | `diamond` | Classic decision symbol |
| Process, action | `rectangle` | Contained action |
| Abstract state | overlapping `ellipse` | Fuzzy, cloud-like |
| Hierarchy node | lines + text | Structure through lines |

---

## Colour as Meaning

Assign colours semantically, not decoratively. See `references/color-palette.md` for the full palette.

- Use fill colour to indicate category or role
- Use stroke colour for borders and emphasis
- Use text colour for hierarchy (title > subtitle > body)
- Use evidence artifact colours for code/data blocks

---

## Modern Aesthetics

- `roughness: 0` for clean, professional diagrams
- `roundness: { "type": 3 }` for rounded rectangle corners
- `fontFamily: 3` (monospace) for all text
- Consistent spacing between elements (40-60px gaps)
- Generous whitespace. Let elements breathe.

---

## Layout Principles

1. **Reading direction**: Left-to-right or top-to-bottom for flow
2. **Visual weight**: Larger/darker elements draw attention first
3. **Proximity**: Related elements should be close together
4. **Alignment**: Align elements on invisible grid lines
5. **Whitespace**: Use it deliberately to separate sections

---

## Text Rules

- **Titles**: 20-24px, title colour from palette
- **Subtitles**: 16-18px, subtitle colour from palette
- **Body/labels**: 14-16px, body colour from palette
- **Inside shapes**: Use "on light fills" or "on dark fills" colour
- **Line height**: 1.25 for all text
- Keep text concise. If it needs a paragraph, it's not a diagram element.

---

## JSON Structure

Every `.excalidraw` file follows this wrapper:

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "mezcorp-claude-code",
  "elements": [ ... ],
  "appState": {
    "viewBackgroundColor": "#ffffff",
    "gridSize": null
  },
  "files": {}
}
```

See `references/json-schema.md` for element-level schema and `references/element-templates.md` for copy-paste templates.

---

## Render & Validate (MANDATORY)

### How to Render

```bash
cd .claude/skills/draw/references && uv run python render_excalidraw.py <path-to-file.excalidraw>
```

This produces a PNG next to the `.excalidraw` file. Read the PNG to visually inspect.

### The Loop

1. **Render & View**: Generate PNG, read it
2. **Audit against original vision**: Does the structure argue the concept?
3. **Check for visual defects**: Overlapping text? Misaligned arrows? Unbalanced spacing?
4. **Fix JSON**: Edit the `.excalidraw` file
5. **Re-render & re-view**: Generate new PNG, check fixes
6. **Repeat** (typically 2-4 iterations)

### First-Time Setup

```bash
cd .claude/skills/draw/references
uv sync
uv run playwright install chromium
```

---

## Quality Checklist

### Depth & Evidence
- [ ] Depth assessment done (simple vs comprehensive)
- [ ] Evidence artifacts included (for technical diagrams)
- [ ] Real terminology used (not generic placeholders)
- [ ] Multi-zoom levels present (for comprehensive diagrams)

### Conceptual Design
- [ ] Isomorphism test passes (structure communicates without text)
- [ ] Each concept has a distinct visual pattern
- [ ] Shapes match their meaning (not uniform boxes)
- [ ] Container test applied (no unnecessary boxes)

### Structural Integrity
- [ ] Consistent spacing throughout
- [ ] Clear reading direction
- [ ] Whitespace used deliberately
- [ ] No orphaned elements

### Technical Correctness
- [ ] All IDs unique and descriptive
- [ ] Arrow bindings reference correct element IDs
- [ ] Seeds unique per element
- [ ] Coordinates don't overlap
- [ ] `roughness: 0` for clean look

### Visual Validation
- [ ] Rendered to PNG
- [ ] No overlapping text
- [ ] No misaligned arrows
- [ ] Balanced visual weight
- [ ] Readable at expected zoom level
