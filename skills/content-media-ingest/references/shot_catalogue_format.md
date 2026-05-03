# Shot Catalogue Format

Two artifacts produced from shot classification:
1. **In-page Shot Catalogue** — a structured section on every reel page listing every 2s frame with its classification + message.
2. **Cross-reel shot library** — atomic `shot-<name>.md` pages in `wiki/Content/pages/`, indexed by `shot-library-creative.md` and `shot-library-framing.md`. Each atomic page collects example frames from any reel that uses that shot.

Labels come from `shot_taxonomy.md`. Do not invent ad-hoc labels — if a new category is needed, add it to the taxonomy first.

---

## 1. In-page Shot Catalogue section (reel pages)

Replace the old "Frame-by-Frame Shot Map" section on reel pages with this formal Shot Catalogue. Place it between "Shot-Mapping Principles" and "Transcript."

```markdown
## Shot Catalogue

Every 2s frame classified along `distance × angle × motion × treatment`. Creative frames earn a 5th label + cross-link to `shot-<name>.md` in the library. `vo` is the verbatim VO fragment at that timestamp; `message` is what the shot communicates beyond its content.

| Time | Frame | Classification | VO | Audio | Message | Creative |
|------|-------|----------------|----|----|---------|----------|
| 00:00 | ![](../../../../__Attachments/reels/<slug>-<YYYY-MM-DD>/frames/frame_0000.jpg) | MS · eye-level · walk-and-talk · talking-head | "Here's three years of scripting…" | ambient (footsteps) | Credential-flex lands harder outdoors — locked studio would read as training video | — |
| 00:06 | ![](../../../../__Attachments/reels/<slug>-<YYYY-MM-DD>/frames/frame_0003.jpg) | WS · eye-level · walk-and-talk · title-card | "I like to call it the arc formula" | ambient | Full-screen acronym card is a visual metronome — marks structural boundary | [[shot-visual-metronome-acronym]] |
| ... |

Rules:
- One row per 2s frame.
- **Classification column:** four labels joined by ` · ` (distance · angle · motion · treatment). Always all four — no omissions.
- **VO column:** paste the timestamped line verbatim from the transcript. If VO spans multiple frames, trim to the fragment audible at that stride.
- **Audio column:** the music cue at that moment (track title) OR `ambient` OR `speech-only` OR `silence`.
- **Message column:** one sentence. What does the shot *mean*? Not "what's in it." Skip the obvious ("talking head shows speaker talking"); write what the frame achieves.
- **Creative column:** if the frame deserves a cross-reel library entry, link to the `shot-<name>.md` page (create if new — see Section 2). If not, write `—`.

Rhythmic repetition of the same classification is expected (a locked walk-and-talk reel will have 20+ identical rows). Condense runs like this:

| 00:08–00:14 (4 frames) | — | MS · eye-level · walk-and-talk · talking-head | "A is attention…" | ambient | Motion-as-variety: the walking substitutes for editing cuts, preventing monotony despite identical classification | — |

— use a single row with frame range when a run of ≥3 frames shares classification AND message. Inspect each frame first; if creative signatures differ even slightly, don't condense.

## Creative Shot Roll-up

After the catalogue, summarise the creative shots into a small roll-up — a 3-column grid of just the frames marked creative + their library link. Fast skim surface for the reel's signature visual moves.

| ![](../../../../__Attachments/reels/<slug>-<YYYY-MM-DD>/frames/frame_NNNN.jpg) | ![](../../../../__Attachments/reels/<slug>-<YYYY-MM-DD>/frames/frame_MMMM.jpg) | ![](../../../../__Attachments/reels/<slug>-<YYYY-MM-DD>/frames/frame_KKKK.jpg) |
|---|---|---|
| **[[shot-visual-metronome-acronym]]** at 00:06 | **[[shot-demo-as-proof]]** at 00:16 | **[[shot-embossed-object-outro]]** at 00:50 |

If the reel has no creative frames, write one sentence explaining why (e.g., "Deliberately conventional — the script carries all variation. No creative shots to surface."). Absence is signal.
```

---

## 2. Cross-reel atomic shot page — `shot-<name>.md`

Atomic `shot-<name>.md` pages live in `wiki/Content/pages/` (flat, same directory as reel-structure pages). One shot type per page. Each page is `kind: insight` — it describes an observed pattern with evidence across multiple reels.

### Frontmatter

```yaml
---
type: wiki-page
wiki: Content
kind: insight
Updated: YYYY-MM-DD
tags:
  - shot/<category>       # creative | framing | motion — pick ONE, whichever this shot primarily teaches
  - pattern/<pattern>     # optional — only if the shot belongs to a named pattern family already in the wiki
sources: []               # empty unless the observation comes from a specific book/research
---
```

### Body

**Name the shot in the H1** — lowercase kebab-case slug + Title Case display. E.g., `# Shot — Demo As Proof`.

Follow the `insight` page structure from the master schema:

```markdown
# Shot — <Name>

## Claim
<One sentence — what this shot is + what it does to the viewer.>

## Mechanism
<Why it works. What the frame's composition + context creates that narration alone cannot. 2-4 sentences.>

## Evidence

- **[[reel-structure-X]] @ MM:SS** — `![MM:SS](../../../../__Attachments/reels/<slug>-<YYYY-MM-DD>/frames/frame_NNNN.jpg)`
  Brief context: what's the VO at that moment and how the shot reinforces it. 1-2 sentences.

- **[[reel-structure-Y]] @ MM:SS** — `![MM:SS](../../../../__Attachments/reels/<slug>-<YYYY-MM-DD>/frames/frame_NNNN.jpg)`
  ...

Grow this list on every new ingest that uses the shot.

## When to use
- <Concrete condition where this shot earns its place — tied to script function (hook / reveal / sign-off / etc).>
- ...

## When NOT to use
- <Condition where the shot would break the piece — tonal mismatch, production-cost mismatch, brand-type mismatch.>
- ...

## Cross-links
- [[shot-library-creative]] or [[shot-library-framing]]
- [[<related-shot-page>]]
- [[<related-framework-page>]]
```

### Rules

- **≤300 words** across all prose sections combined (Claim + Mechanism + When to use + When NOT to use). Evidence bullets are exempt — they grow over time and are the point.
- **Evidence bullets are append-only across ingests.** Every new reel that uses this shot appends an entry here. Never rewrite old evidence.
- **Screengrabs use the vault-relative 4-dotdot path** — `../../../../__Attachments/reels/<slug>-<YYYY-MM-DD>/frames/frame_NNNN.jpg` — because the shot page lives at the same depth as the reel pages (3 deep from vault root).
- **If two reels use the same shot but with subtly different effect,** do not fork the page. Document the variation inside the shot's Mechanism or evidence entry. Only fork when the shots are structurally different (e.g., `shot-reflection-framing` vs `shot-through-the-glass` — one uses a mirror, the other uses a transparent barrier).

### Naming

Slugs follow the taxonomy labels where possible:
- Distance-driven: `shot-extreme-close-up-emotion`, `shot-wide-scale-opener`
- Angle-driven: `shot-low-angle-authority`, `shot-overhead-flat-lay`
- Motion-driven: `shot-push-in-stakes-escalation`, `shot-whip-pan-transition`
- Treatment-driven: `shot-demo-in-medium`, `shot-title-card-metronome`
- Creative signature: verbatim label from taxonomy — `shot-rack-focus-reveal`, `shot-through-the-glass`, `shot-match-cut-metaphor`, `shot-embossed-object-outro`

Prefix is always `shot-`. This makes them trivially greppable (`ls wiki/Content/pages/shot-*`) and keeps them grouped in Obsidian's file pane.

---

## 3. Library index pages

Two library pages at `wiki/Content/pages/`:

- `shot-library-creative.md` — indexes creative-signature shots.
- `shot-library-framing.md` — indexes conventional shots that have strong message attribution (framing strategies, distance choices, angle philosophy).

Each is `kind: framework` (they provide a lens for selecting shots) and follows this body shape:

```markdown
## Lens
What this library gives you — a vocabulary of <creative/framing> shots with cross-reel evidence, usable as a reference when planning a new reel's visual language.

## Organization

### <Category 1>
- [[shot-<name>]] — <one-line what it does> — evidence in <N> reels
- [[shot-<name>]] — ...

### <Category 2>
...

## When to consult
- <Specific scripting / pre-production moments when this library beats starting from scratch.>

## When NOT to consult
- <When the reel's voice should NOT be borrowed from the library — e.g., a novel brand moment where reuse would look derivative.>

## Cross-links
- [[shot-library-<other>]]
- [[<related framework pages>]]
```

The libraries are *indexes*, not catalogs. They link to atomic pages. Organizing them keeps the corpus navigable once it grows past ~20 shots.

## Anti-patterns

- Ad-hoc label invention (use `shot_taxonomy.md` labels; propose additions, don't fork vocabulary).
- Duplicating evidence across shot pages (evidence lives on the *specific* shot's page; the reel page only wikilinks).
- Overloading "creative" — repeated walk-and-talk MS is not creative. Flag creative only when the frame earns it.
- Forking shot pages on tiny variation. Document variation in the single page's body.
- Populating library index pages with content instead of links. They index; they don't store.
