# Page Templates

These are skeletons, not forms. The sections are required; the content inside each section is always specific to the piece.

## Reel page

Path: `wiki/Content/pages/reel-structure-<slug>.md`

```yaml
---
type: wiki-page
wiki: Content
kind: flow
brand_type: business | personal
sources:
  - <slug>-reel
Updated: YYYY-MM-DD
tags:
  - brand/business        # or brand/personal
  - scripting/structure
  - format/reel
  - platform/instagram
  - pattern/<one-or-two-extracted-pattern-names, e.g. analogy-transfer, offer-deconstruction>
---

# Reel Structure — <Creator> "<Topic>" (M:SS)

<One-sentence thesis. What is this reel doing worth copying. End with "Use this page to grade future ingests against a proven structure." or similar framing that signals benchmark-intent.>

## Script Skeleton (Beat Map)

| Beat | Time | Function | Line |
|------|------|----------|------|
| <beat name> | M:SS–M:SS | <what it accomplishes> | "<verbatim line fragment>" |
| ... |

## Pattern Rules Extracted

- **<Rule name — noun phrase>.** <One sentence of mechanism + why it works.>
- ...

## Shot-Mapping Principles

- <Head/b-roll alternation cadence and max shot length.>
- <How b-roll literalizes the spoken noun — give 2-3 concrete examples from the piece.>
- <Caption style, position, typeface.>
- <Chyron / lower-third treatment.>
- <Anything else specific to this piece's visual system.>

## <Brand-specific section — choose one>

### For business: Corporate Positioning Angle
<1-2 bullets on brand voice extension and production signal.>

### For personal: POV + Offer Placement
<1-2 bullets on authenticity markers, caption CTA placement, identity anchor.>

## Benchmark Checklist (apply to future ingests)

- [ ] <Checkable claim derived from Pattern Rules, not restated.>
- [ ] ...

## Transcript

*Language: <lang>. Source audio auto-transcribed (Whisper <model>).*

### Prose

<single-paragraph readable flow. No "improvements" — only line-break cleanup>

### Timestamped

- [MM:SS] <line>
- ...

## Shot Catalogue

*See `references/shot_catalogue_format.md` for full spec. Labels come from `references/shot_taxonomy.md` — do not invent ad-hoc labels.*

Every 2s frame classified along `distance · angle · motion · treatment`. Creative frames earn a 5th label + wikilink to their atomic `shot-<name>.md` page.

| Time | Frame | Classification | VO | Audio | Message | Creative |
|------|-------|----------------|----|-------|---------|----------|
| 00:00 | ![](../../../../__Attachments/reels/<slug>-<YYYY-MM-DD>/frames/frame_0000.jpg) | MS · eye-level · walk-and-talk · talking-head | "<VO fragment>" | ambient / <track name> / speech-only | <one sentence: what the shot communicates beyond its content> | [[shot-<name>]] or — |
| ... |

Condense runs of ≥3 identical frames (same classification AND same message) into a single row with a frame range (e.g., `00:08–00:14 (4 frames)`). If classification changes or a creative signature appears, do not condense — keep a separate row.

### Creative Shot Roll-up

3-column grid showing only the frames flagged `Creative` above, with wikilinks to the atomic shot pages. This is the reel's signature visual moves at a glance.

| ![](../../../../__Attachments/reels/<slug>-<YYYY-MM-DD>/frames/frame_NNNN.jpg) | ![](../../../../__Attachments/reels/<slug>-<YYYY-MM-DD>/frames/frame_MMMM.jpg) | ![](../../../../__Attachments/reels/<slug>-<YYYY-MM-DD>/frames/frame_KKKK.jpg) |
|---|---|---|
| **[[shot-<name>]]** at MM:SS | **[[shot-<name>]]** at MM:SS | **[[shot-<name>]]** at MM:SS |

If the reel has no creative frames, replace this section with one sentence naming why (e.g., "Deliberately conventional — script carries all variation. No creative shots to surface."). Absence is signal.
```

## Carousel page

Path: `wiki/Content/pages/carousel-structure-<slug>.md`

```yaml
---
type: wiki-page
wiki: Content
kind: flow
brand_type: business | personal
sources:
  - <slug>-carousel
Updated: YYYY-MM-DD
tags:
  - brand/business        # or brand/personal
  - scripting/structure
  - format/carousel
  - platform/instagram
  - pattern/<extracted-pattern-names>
---

# Carousel Structure — <Creator> "<Topic>" (<N> slides)

<One-sentence thesis. End with benchmark framing.>

## Slide Map

| # | Role | Content | Visual |
|---|------|---------|--------|
| 1 | Hook | "<on-slide text or dominant image>" | <layout: pure-type card / photo + overlay / meme / product shot> |
| 2 | <Role> | ... | ... |
| ... |

Roles vocabulary: Hook, Thesis, Restatement, Body, Proof, CTA, Sign-off, Bio. If a slide blends roles, pick the dominant one and note the blend in a sentence after the table.

## Pattern Rules Extracted

- **<Rule>.** <Mechanism + why.>
- ...

## Visual System

- **Aspect:** <W×H, ratio>
- **Template:** <reused layout across slides? describe the recurring slots: title / body / accent / footer>
- **Typography:** <font family, weight, sizing rhythm>
- **Color:** <palette + contrast pattern>
- **Background:** <solid / gradient / photo / mixed>

## Caption + CTA Interplay

<Describe the handoff between slide content, final slide CTA (if any), and caption CTA. Name the CTA mechanic explicitly: comment-gate, DM keyword, link-in-bio, swipe-to-subscribe, save-for-later, etc.>

## <Brand-specific section — choose one>

### For business: Funnel Role + Template-as-Asset
<1-2 bullets on where this post sits in the funnel and whether the template gets reused across the feed.>

### For personal: Voice Signal + Authenticity Tradeoff
<1-2 bullets on first-person tells, narrative vs advice split, polish-vs-raw positioning.>

## Benchmark Checklist

- [ ] ...

## Slide Grid

| 01 | 02 | 03 |
|---|---|---|
| ![slide 01](../../../../__Attachments/carousels/<slug>-<YYYY-MM-DD>/slides/slide_01.jpg) | ![slide 02](../../../../__Attachments/carousels/<slug>-<YYYY-MM-DD>/slides/slide_02.jpg) | ![slide 03](../../../../__Attachments/carousels/<slug>-<YYYY-MM-DD>/slides/slide_03.jpg) |
| **04** | **05** | **06** |
| ![slide 04](...) | ![slide 05](...) | ![slide 06](...) |
| ...

## Caption (verbatim)

> <full caption, line breaks preserved>

## Top Comments / Engagement Notes

- <Comment text — @author (N likes)> — <why it's signal, not noise>
- ...

Skip emoji-only comments. If nothing informative, write one line explaining why the comments were low-signal.
```

## Formatting pedantry that matters

- **Relative attachment paths** are exactly four `../` segments — `../../../../__Attachments/...` — because the page lives at `wiki/Content/pages/` (3 deep into the vault).
- **Frontmatter `Updated:`** uses capital U and no quotes: `Updated: 2026-04-23`.
- **Page title** uses an em dash, not a hyphen, between the format label and the creator: `# Reel Structure — a16z × Kevin Systrom ...`.
- **Duration format:** M:SS with no leading zero for minutes under 10 (e.g., `0:55`, `1:42`).
- **Benchmark checklist** uses `- [ ]` markdown checkboxes so Obsidian renders them toggle-able.
