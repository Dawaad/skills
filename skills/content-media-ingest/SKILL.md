---
name: content-media-ingest
description: Ingest an Instagram Reel or carousel URL into the Content wiki as a fully-synthesized structure benchmark. Use whenever the user pastes an instagram.com/reel/ or instagram.com/p/ URL and wants it "added to the wiki", "broken down", "analyzed", "ingested", "turned into a page", or wants a scripting/shot/structure breakdown for later reference. Also use when the user shares a reel/carousel and says anything like "save this one", "make a benchmark out of this", "extract and wiki-fy", "pull this into Content", or asks for a beat map, slide-by-slide breakdown, hook analysis, or pattern extraction from an IG post — even if they do not say the word "wiki". Chains the reel-extractor or carousel-extractor, then writes a `sources/` pointer + a `pages/` synthesis in the exact house style (see reel-structure-a16z-systrom-upload.md, carousel-structure-foundr-boring-stuff.md). Branches synthesis by brand_type (business vs personal).
---

# Content Media Ingest

Pipeline that turns one Instagram URL into two wiki artifacts: a source pointer and a synthesized structure page. Reuses the existing reel/carousel extractor skills for the raw pull, then layers the Content wiki's house-style synthesis on top.

## Why this exists

The user is building a library of reference benchmarks for short-form content. Every ingested reel/carousel becomes a page future scripts get graded against. The synthesis — beat map, shot pacing, pattern rules, checklist — is what makes the page useful. Raw extraction alone is noise. This skill locks in the synthesis layers so every benchmark is directly comparable.

## Inputs

- **URL** (required) — an `instagram.com/reel/...` or `instagram.com/p/...` link.
- **brand_type** (required) — `business` (corporate account: a16z, Foundr, Stripe) or `personal` (individual creator/founder). If not stated, ask *once* before running anything. Don't guess from the handle alone — creator accounts often post business content and vice versa.
- **save_dir override** (optional) — user may specify where to save the raw extraction bundle. Default is `~/Documents/wiki/_Attachments/reels/` or `~/Documents/wiki/_Attachments/carousels/`.

Vault root is `/home/jared/Documents/`. The Content wiki lives at `/home/jared/Documents/wiki/Content/`.

## Pipeline

### Step 1 — Detect format

- URL contains `/reel/` → reel path. Uses the `instagram-reel-extractor` skill.
- URL contains `/p/` → ambiguous. Could be a single image, a reel-shared-as-post, or a carousel. Default to the **carousel extractor** — it handles single-item posts correctly and is the only reliable path for multi-slide sidecars. If the carousel extractor returns exactly one video slide with no image siblings, you may re-run via the reel extractor for better transcript/frame handling.

### Step 2 — Run the matching extractor

Invoke the appropriate extractor skill. Pass `--save-dir` so the bundle is self-contained and portable.

Reel:
```bash
/home/jared/.claude/skills/instagram-reel-extractor/.venv/bin/python3 \
  /home/jared/.claude/skills/instagram-reel-extractor/scripts/extract_reel.py \
  "<URL>" --save-dir ~/Documents/wiki/_Attachments/reels
```

Carousel:
```bash
python3 /home/jared/dev/util/carousel-extractor/scripts/extract_carousel.py \
  "<URL>" --save-dir ~/Documents/wiki/_Attachments/carousels
```

Common failures:
- **gallery-dl login wall** on carousel (IG `/p/` URLs): `HTTP redirect to login page`. Try `--cookies-from chrome` then `firefox`. If Chrome v11 cookies cannot decrypt (Linux keyring issue: `Unable to decrypt v11 cookies: no key found`), the carousel path is dead — fall through to the **reel extractor** on the same `/p/` URL. It handles single-video posts correctly. If the post is a genuine multi-slide carousel and gallery-dl can't auth, stop and ask the user to export cookies via a browser extension.
- **Missing deps**: stop and tell the user what to install — never fabricate extraction data.

Confirm the bundle landed where expected. Read the produced `extraction.md` (or equivalent) to get the structured summary and file paths.

### Step 2a — Persist the full extraction bundle into the vault (MANDATORY, reels only)

**Critical gotcha:** the reel extractor's `--save-dir` flag writes **only the markdown summary** to the given directory. The actual media bundle (`audio.wav`, `reel.mp4`, `frames/`, `reel.info.json`) stays in `/tmp/reel_XXXXXX/` and gets wiped on reboot. The carousel extractor does persist its bundle — this step is reels-only.

The extractor's final line is `Saved to: <save-dir>/<creator>-reel-<YYYY-MM-DD>.md`. That's the **markdown only**. Grep the preceding output for the tmp bundle path (the script downloads to `/tmp/reel_<random>/`).

Restructure so the markdown and the media live together inside the vault under a single bundle folder named by slug:

```bash
# 1. make slug-named bundle folder inside vault
mkdir -p ~/Documents/wiki/_Attachments/reels/<slug>-<YYYY-MM-DD>/

# 2. copy the media + info from the tmp bundle
cp /tmp/reel_<hash>/audio.wav \
   /tmp/reel_<hash>/reel.mp4 \
   /tmp/reel_<hash>/reel.info.json \
   ~/Documents/wiki/_Attachments/reels/<slug>-<YYYY-MM-DD>/
cp -r /tmp/reel_<hash>/frames ~/Documents/wiki/_Attachments/reels/<slug>-<YYYY-MM-DD>/

# 3. move the markdown into the bundle folder AND rename it extraction.md
mv ~/Documents/wiki/_Attachments/reels/<creator>-reel-<YYYY-MM-DD>.md \
   ~/Documents/wiki/_Attachments/reels/<slug>-<YYYY-MM-DD>/extraction.md
```

Result — every reel bundle in `~/Documents/wiki/_Attachments/reels/<slug>-<YYYY-MM-DD>/` contains exactly these files: `extraction.md`, `audio.wav`, `reel.mp4`, `reel.info.json`, `frames/`. This is the shape the source pointer and the in-Obsidian media embeds both rely on.

For carousels, the extractor already writes `extraction.md + slides/` into `~/Documents/wiki/_Attachments/carousels/<bundle>/`. No restructure needed; just confirm the bundle folder exists under that path before moving on.

### Step 2b — Multi-window Shazam scan (reels only)

The reel extractor's default Shazam pass runs once on the full audio and surfaces a single track. Cinematic / essay / long-form reels frequently swap music 2–5 times, and each cue typically maps to a narrative beat (see [[score-as-beat-divider]]). Missing those cues flattens downstream synthesis.

Run the multi-window scan against the extracted audio to identify all beds:

```bash
/home/jared/.claude/skills/instagram-reel-extractor/.venv/bin/python3 \
  /home/jared/.claude/skills/content-media-ingest/scripts/multi_window_shazam.py \
  <bundle>/audio.wav
```

The script slides a 12-second fingerprint window across the runtime at 15-second stride, dedupes adjacent matches into single cue spans, and preserves gaps (speech-dominant regions are signal too — they tell you where the VO does the work alone).

Output example:
```
Multi-window scan identified 3 distinct cue(s):

- 0:00–0:15 — (no match — speech-dominant or no distinct bed)
- 0:15–0:27 — 보나마나 (BONAMANA) — G-DRAGON (K-Pop)
- 1:00–1:12 — Knives Out! (String Quartet in G Minor) — Nathan Johnson
- 1:15–2:10 — The Adults Are Talking — The Strokes
```

Use `--json` for programmatic consumption, `--stride`/`--window` to tune (e.g., 30/15 for faster scans of long reels; 10/8 for dense cue-swapping reels).

The full cue table belongs in the source file under a `Music (N cues, scored as beat-dividers):` section with each line noting `time-span — title — artist (genre) (narrative role)`. Narrative role is your synthesis — "melancholy intro", "uplift payoff", "K-pop reprise" — not just "track 2 of 4".

If the reel has only one cue across its runtime, skip the expanded music section and use the original single-track format. One-cue reels are the norm; multi-cue is the interesting case.

Carousels skip this step — per-slide video beds are already handled by the carousel extractor on a per-slide basis.

### Step 3 — Confirm bundle is page-renderable

After Step 2a, frames already live inside the bundle at `wiki/_Attachments/reels/<slug>-<YYYY-MM-DD>/frames/`. Carousel slides already live at `wiki/_Attachments/carousels/<slug>-<YYYY-MM-DD>/slides/`. There is no separate mirror copy — the bundle IS the attachment folder. Wiki pages embed those paths directly.

- Reel frames → `wiki/_Attachments/reels/<slug>-<YYYY-MM-DD>/frames/frame_NNNN.jpg`
- Carousel slides → `wiki/_Attachments/carousels/<slug>-<YYYY-MM-DD>/slides/slide_NN.jpg`

The `<slug>` is a lowercase-kebab identifier combining creator + topic (e.g., `a16z-systrom-upload`, `foundr-boring-stuff`, `mason-personal-brand-offer`). Pick something someone skimming the index can read at a glance — creator first, then the 2-3 word topic anchor.

Verify the `frames/` (or `slides/`) directory exists inside the bundle and contains the expected count before moving on. If empty, Step 2a was incomplete — go back and finish it.

### Step 4 — Write the source pointer

Path: `wiki/Content/sources/reels/<slug>-reel.md` or `wiki/Content/sources/carousels/<slug>-carousel.md`.

Template: see `references/source_template.md`.

Always include: URL, creator + handle, duration/slide-count, upload date, engagement counts as of extract date, path to local bundle, path to attachments folder, wikilink to the forthcoming feeds page.

**Two subsections are mandatory on every source file (not negotiable):**

1. **`## Music`** — dedicated subsection with every identified track broken out as structured fields. Never bury the song in a one-line bullet. For single-cue reels: Song / Artist / Genre / Cue map (`single cue, full runtime`) / Shazam link. For multi-cue reels: one entry per cue with `time-span — title — artist (genre) (narrative role)`. Carousels: capture per-slide audio if present; otherwise write one line explaining there is none. If Shazam returned no match, state that explicitly ("No distinct track identified — speech-dominant / silent / non-music bed"). The goal: the song titles are trivially greppable from the source file without opening the extraction bundle.

2. **`## Media`** — dedicated subsection with Obsidian `![[...]]` embeds for playable media. Reels embed both `reel.mp4` and `audio.wav`. Carousels embed the slides grid in the page and embed any per-slide video beds in the source. The embed path is the vault-relative path — `![[wiki/_Attachments/reels/<slug>-<YYYY-MM-DD>/reel.mp4]]` — so Obsidian renders an inline player in preview mode. Without this block the user has to `cd` into the bundle folder to play the audio; we owe them a one-click play.

See `references/source_template.md` for exact layout.

### Step 5 — Synthesize the structure page

Path: `wiki/Content/pages/reel-structure-<slug>.md` or `wiki/Content/pages/carousel-structure-<slug>.md`.

Frontmatter kind is **always `flow`** (it answers "how does this piece orchestrate end-to-end"). Frontmatter `brand_type` is what the user specified. Both `brand_type: <x>` in frontmatter AND `#brand/<x>` tag — the domain CLAUDE.md requires both.

Load `references/synthesis_layers.md` and walk through every section listed for the matching format (reel vs carousel) and brand_type. Do not skip layers silently — if a layer doesn't apply, write one sentence saying why (e.g., "No b-roll — single talking-head take throughout"). Gaps are information.

The page is a reference benchmark. Someone will grade future scripts against it. That means:
- Lead with the one-sentence thesis of the piece (what does this reel *do* that's worth copying).
- Name specific patterns, not generic advice. "Analogy-transfer" beats "tells a story". "4-word credential hook" beats "strong opening".
- Include the checklist at the end — that's what makes the page a tool, not just a description.

### Step 5.5 — Classify every frame (Shot Catalogue) — reels only

**Mandatory for every reel page.** The Shot Catalogue is Layer 5 of `references/synthesis_layers.md` and the single largest upgrade over the old Frame-by-Frame Shot Map. Two reference files drive this step:

- `references/shot_taxonomy.md` — the canonical vocabulary for distance · angle · motion · treatment labels, plus the list of recognised `creative_signature` tags. **Read it before classifying.** Do not invent labels.
- `references/shot_catalogue_format.md` — the table shape for the in-page catalogue, the Creative Roll-up, and the atomic `shot-<name>.md` library pages.

Walk the frame set chronologically at 2s stride. For each frame:

1. Read the frame image.
2. Assign four labels: `distance · angle · motion · treatment`. Use taxonomy vocabulary verbatim.
3. Copy the VO fragment at that timecode from the timestamped transcript.
4. Note the audio bed at that timecode (music cue title / `ambient` / `speech-only` / `silence`) — pull from the source file's `## Music` section.
5. Write the **message** — one sentence on what the shot communicates *beyond* its content. Skip the tautological ("talking head shows speaker talking"). If you can't name what it's doing, the frame is a filler and the message line should say so plainly.
6. Decide: creative or not? The bar is high — see `shot_taxonomy.md` §"What counts as creative."
   - If yes: add a 5th label from the creative-signature list, and either (a) wikilink an existing `shot-<name>.md` page or (b) **create a new one** per `shot_catalogue_format.md` §2.
   - If no: leave creative column as `—`.
7. Condense runs. When ≥3 consecutive frames share classification AND message AND creative state, collapse to one row with a frame range. Don't condense across classification or creative changes.

Write the Shot Catalogue table into the reel page between Shot-Mapping Principles and Benchmark Checklist. Append the Creative Shot Roll-up (3-column image grid) immediately after the table.

**Atomic shot pages — growth rules:**

- Before creating a new `shot-<name>.md` page, grep `wiki/Content/pages/shot-*.md` for an existing match. Evidence bullets are append-only — do not duplicate a page to add an evidence row.
- When appending to an existing shot page, add an evidence bullet with the new reel's wikilink + timecode + frame embed + 1-2 sentence context. Keep older evidence in place.
- When creating a new shot page, use the frontmatter + body structure in `shot_catalogue_format.md` §2. ≤300 words across prose sections; evidence bullets are exempt.
- Update `shot-library-creative.md` or `shot-library-framing.md` (whichever applies — creative-signature shots go to creative; distance/angle/motion/treatment default choices with strong message signal go to framing) by adding a one-line link pointer under the right category heading.

**Degenerate cases handled honestly:**

- Locked talking-head reel with zero variation → catalogue will collapse to 1-2 rows total. That is correct output. The reel's visual philosophy is "the script carries everything" and the catalogue should say so via the Creative Roll-up's absence-note.
- Multi-cut cinematic reel → catalogue may have 20+ distinct rows and several creative entries. That is also correct. A multi-cut reel earns the full catalogue weight.

**Skip for carousels.** Carousels already get slide-by-slide treatment in their Slide Map. The Shot Catalogue concept is reel-specific. Do not retrofit the catalogue onto carousel pages.

### Step 6 — Update index

Open `wiki/Content/index.md`. Find `## Formats → ### Scripting Structure`. Add a new bullet under the correct brand group (`**Business-branded**` or `**Personal brand**`), format:

```
- [[<page-slug>]] — <creator>, <duration or slide count> <one-line structure signature>
```

Keep bullets sorted newest-first within each brand block. If the Scripting Structure section doesn't yet split Reels vs Carousels and the list is getting long, group by format under each brand header.

### Step 7 — Append the log

`wiki/Content/log.md`. Match the existing entry style exactly:

```
## [YYYY-MM-DD] ingest | <Creator> <topic> <format> (<platform>, <duration or slide count>)
- [[<page>]] (new) [flow] — <one-line synthesis signature>
- source: `sources/<type>/<source-file>.md`
- frames cached: `wiki/_Attachments/reels/<slug>-<YYYY-MM-DD>/frames/` or `wiki/_Attachments/carousels/<slug>-<YYYY-MM-DD>/slides/` (<count> @ <interval>)
- shot catalogue: <N frames classified, M creative frames flagged>
- shot library additions: `[[shot-<name>]] (new)` OR `[[shot-<name>]] (evidence append)` — one bullet per atomic shot page created or extended
- skipped: <anything intentionally dropped and why>
- patterns surfaced (not yet promoted to framework pages): <optional>
```

The `skipped:` line matters. It's how the wiki stays lean — the model has to justify what it didn't include so the signal stays high.

## Output contract

When done, tell the user:
1. Page created: `wiki/Content/pages/<page>.md`
2. Source: `wiki/Content/sources/<type>/<source>.md` — confirm it has **both** the `## Music` subsection and the `## Media` embed block
3. Bundle: `~/Documents/wiki/_Attachments/reels/<slug>-<YYYY-MM-DD>/` or `~/Documents/wiki/_Attachments/carousels/<slug>-<YYYY-MM-DD>/` — the bundle IS the attachment folder. Confirm it contains `extraction.md`, `audio.wav`, `reel.mp4` (reels) or `slides/` + per-slide videos (carousels), `frames/`, and `reel.info.json` where applicable. If any of these are missing, name what's missing and why.
4. Wiki page embeds reference paths inside that bundle (e.g., `wiki/_Attachments/reels/<slug>-<YYYY-MM-DD>/frames/frame_NNNN.jpg`).
5. Index + log updated
6. **Shot Catalogue** (reels only): N frames classified, M creative frames flagged. List any new `shot-<name>.md` pages created and any existing pages that received new evidence.

Then paste the one-sentence thesis of the piece so the user sees whether the synthesis caught the right core idea.

## What to avoid

- **Don't rewrite the transcript.** Clean line breaks only. Any "improvement" corrupts the benchmark.
- **Don't invent engagement numbers or dates.** If the extractor didn't surface them, leave the field blank or write "not captured".
- **Don't copy the example pages literally.** They are *templates in spirit*, not forms to fill. The beat count, the pattern names, the checklist items are all particular to the piece. Copying the a16z 6-beat structure onto a carousel is wrong — carousels get slide-mapping, not beat-mapping.
- **Don't create subfolders inside `pages/`.** Flat by design — kind + brand_type live in frontmatter.
- **Don't promote derivative frameworks to their own pages yet.** If you notice a pattern that deserves its own `kind: framework` page (e.g., "analogy-transfer hook"), log it under `patterns surfaced (not yet promoted)` in the log entry — the user decides when to spin it out so the wiki doesn't bloat with half-baked abstractions.
- **Don't leave the extraction bundle in `/tmp/`.** The reel extractor's `--save-dir` only writes the markdown summary; the media stays in `/tmp/reel_XXXXXX/` and dies on reboot. Step 2a is mandatory — the audio, mp4, frames, and info.json must all live inside the vault under `~/Documents/wiki/_Attachments/reels/<slug>-<YYYY-MM-DD>/` before you move on.
- **Don't bury the song metadata in a one-line bullet.** Every source file gets a dedicated `## Music` subsection with Song / Artist / Genre / Cue map / Shazam fields (or per-cue rows for multi-cue reels). This is what makes song titles greppable across the Content wiki — a bullet in a mixed field list is not good enough.
- **Don't skip the `## Media` embed block.** The source file is where audio/video playback happens inside Obsidian. Missing `![[...]]` embeds = user has to leave Obsidian to hear the reel = the wiki failed at its job.
- **Don't invent shot labels.** The Shot Catalogue vocabulary lives in `references/shot_taxonomy.md`. If a frame doesn't fit an existing label, propose a new one via edit to the taxonomy in the same ingest — do not just write an ad-hoc label into the catalogue. Consistency across ingests is the whole value.
- **Don't flag every frame creative.** The bar is high (see `shot_taxonomy.md` §"What counts as creative"). Repeated identical walk-and-talk MS is not creative. Over-tagging dilutes the cross-reel library — a library where everything is creative catalogues nothing.
- **Don't fork atomic shot pages on tiny variation.** If a shot type already has a page and this reel uses a slightly different spin, append an evidence bullet + a sentence on the variation. Fork only when structurally distinct (e.g., reflection-through-glass is not the same as mirror-reflection).
- **Don't duplicate evidence across shot pages.** Each reel's use of a shot is recorded once, on the shot's atomic page. The reel page's Shot Catalogue wikilinks to it; the atomic page holds the evidence bullet.

## Reference files

- `references/synthesis_layers.md` — the mandatory layers each page must cover, split by format (reel/carousel) and brand_type (business/personal). Read this before writing Step 5.
- `references/source_template.md` — canonical source-file shape.
- `references/page_templates.md` — reel and carousel page skeletons that match the existing benchmarks.
- `references/shot_taxonomy.md` — canonical vocabulary for shot classification (distance · angle · motion · treatment + creative-signature list). Read this before Step 5.5.
- `references/shot_catalogue_format.md` — Shot Catalogue table shape, Creative Roll-up layout, and atomic `shot-<name>.md` page template. Read this alongside shot_taxonomy.md.
