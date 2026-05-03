# Source File Template

Path: `wiki/Content/sources/<reels|carousels>/<slug>-<reel|carousel>.md`

Purpose: pointer + in-vault playback surface. Captures what was extracted, where the media lives, and links to the synthesis page. The `## Music` and `## Media` blocks are mandatory — they turn the source file into a playable Obsidian note, not just a pointer.

## Reel source

```yaml
---
type: wiki-source
wiki: Content
brand_type: business | personal
Created: YYYY-MM-DD
tags:
  - brand/business        # or brand/personal
  - source/reel
  - platform/instagram
---

# Source — <Creator> <2-4 word topic anchor> Reel

- **URL:** <full permalink>
- **Creator:** <Display Name> (@handle)
- **Duration:** M:SS
- **Upload:** YYYY-MM-DD
- **Engagement (extract date):** <N> likes / <N> comments
- **Caption:** "<verbatim caption, hashtags included>"
- **Extracted bundle:** `reels/<slug>-<YYYY-MM-DD>/` (extraction.md + audio.wav + reel.mp4 + reel.info.json + frames/)
- **Frames:** `__Attachments/reels/<slug>-<YYYY-MM-DD>/frames/` (<N> frames @ <interval>s interval)
- **Feeds page:** [[reel-structure-<slug>]]

## Music

Break every identified audio cue out into structured fields. This subsection exists so song titles are greppable across the Content wiki. Never collapse it into a one-line bullet.

### Single-cue (most reels)

- **Song:** <Title>
- **Artist:** <Artist>
- **Genre:** <Genre as reported by Shazam>
- **Cue map:** single cue, full 0:00–M:SS runtime
- **Shazam:** <url>

### Multi-cue (cinematic essays, mixtape-style reels, long-form)

Use a per-cue block, one per identified track. Include narrative role as your synthesis ("melancholy intro", "uplift payoff") — not just "track 2 of 4".

- **Cue 1 — 0:00–0:15** — <Title> — <Artist> (<Genre>) — <narrative role>
  - Shazam: <url>
- **Cue 2 — 0:15–0:42** — <Title> — <Artist> (<Genre>) — <narrative role>
  - Shazam: <url>
- **Cue 3 — 0:42–1:12** — *(no match — speech-dominant or no distinct bed)*
- ...

### No music detected

- **Song:** *(no distinct track identified — speech-dominant / silent / non-music bed)*

## Media (embedded — playable in Obsidian preview)

Obsidian renders `![[...]]` wikilinks as inline players for `.mp4` and `.wav`. Use vault-relative paths, not `~/` or absolute paths.

### Video
![[reels/<slug>-<YYYY-MM-DD>/reel.mp4]]

### Audio
![[reels/<slug>-<YYYY-MM-DD>/audio.wav]]
```

## Carousel source

```yaml
---
type: wiki-source
wiki: Content
brand_type: business | personal
Created: YYYY-MM-DD
tags:
  - brand/business        # or brand/personal
  - source/carousel
  - platform/instagram
---

# Source — <Creator> <2-4 word topic anchor> Carousel

- **URL:** <full permalink>
- **Creator:** <Display Name> (@handle)
- **Format:** <N>-slide <image | mixed image+video> carousel (<dimensions>, <aspect ratio>)
- **Upload:** YYYY-MM-DD
- **Engagement (extract date):** <N> likes / <N> comments
- **Caption:** "<verbatim caption, line breaks preserved>"
- **Extracted bundle:** `carousels/<bundle-folder>/` (extraction.md + slides/ + any per-slide videos)
- **Slides:** `__Attachments/carousels/<slug>-<YYYY-MM-DD>/slides/slide_01.jpg` … `slide_NN.jpg`
- **Feeds page:** [[carousel-structure-<slug>]]

## Music

Carousels without video beds: write one line explaining there is none (e.g., `*(static image carousel — no audio)*`). If any slide has a video bed with music, break it out per-slide under ### Slide N.

### Slide <N> — <title/role>
- **Song:** <Title>
- **Artist:** <Artist>
- **Genre:** <Genre>
- **Shazam:** <url>

## Media (embedded — playable in Obsidian preview)

Carousels embed the full slide grid via the page's Slide Grid table. For any per-slide video beds, embed here:

### Slide <N> — video bed
![[carousels/<bundle-folder>/slides/slide_<NN>.mp4]]
```

## Rules

- The `Feeds page:` wikilink is mandatory — it's how the Obsidian graph connects the source to the synthesis.
- The `## Music` subsection is mandatory on every source file. If no music was detected, write it explicitly — silence is also signal. Never bury the song in a one-line bullet above the fold.
- The `## Media` embed block is mandatory on every source file. Obsidian `![[path/to/file.wav]]` must resolve from the vault root — paths start at `reels/...` or `carousels/...`, never `~/` or `/home/...`.
- Bundle paths use vault-relative form (`reels/<slug>-<YYYY-MM-DD>/`). The skill's Step 2a moves the bundle into the vault before you write this file, so these paths are always real.
- Omit fields where data is genuinely missing. Don't write "N/A"; drop the row entirely.
- For engagement, note extract date in the label so a stale number is obviously stale.
- Slug convention: `<creator-handle-or-shortname>-<2-to-4-word-topic>`. All lowercase, kebab-case. Reuse the same slug across source, page, bundle folder, and attachments folder.
