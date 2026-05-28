# Synthesis Layers

Every ingested piece must cover these layers. The layers are what make the page a reusable benchmark instead of a description. If a layer truly does not apply, write one sentence naming its absence — that gap is itself a pattern signal.

---

## Reels

### Common layers (both brand types)

1. **Thesis (1 sentence, lead the page)**
   *What is the piece doing that a future scriptwriter should copy?* Not "a reel about X" — name the move. "Analogy-transfer from Gmail prefetch → IG upload", "Offer-deconstruction via 3-component reveal", "Counter-intuitive credential flex → mechanism → reframe".

2. **Script Skeleton (Beat Map)**
   Time-stamped table: Beat | Time | Function | Line. Beats are functional units, not sentences. Typical reel beats: Hook, Setup, Mechanism, Reaction, Transfer, Payoff/Reframe. Deviations are the interesting part — note when a piece skips or collapses beats.

3. **Pattern Rules Extracted**
   The *portable* takeaways. Each rule should be copy-able into a fresh script. Format: bold lead + one sentence of reasoning + (optional) caveat.

4. **Shot-Mapping Principles**
   - Head-to-b-roll ratio and shot lengths (max shot duration, alternation cadence).
   - How b-roll literalizes spoken nouns.
   - Caption style (word-sync vs block, typeface, anchor position).
   - Chyron / presenter lower-third handling.
   - Overall visual philosophy of the piece in 2-3 sentences (principles, not the per-frame detail — that's Layer 5).

5. **Shot Catalogue + Creative Roll-up** *(mandatory on every reel page)*
   Every 2s frame classified along `distance × angle × motion × treatment` per `shot_taxonomy.md`. See `shot_catalogue_format.md` for table structure. Three required outputs:
   - **In-page Shot Catalogue table** — one row per 2s frame (or condensed run of ≥3 identical frames), with verbatim VO fragment + audio-bed attribution + a one-sentence *message* (what the shot communicates beyond its content).
   - **Creative frames flagged** with a 5th label from the taxonomy's creative-signature list + wikilink to the matching atomic `shot-<name>.md` page. If the shot type is new to the wiki, create the atomic page (see `shot_catalogue_format.md` §2) as part of this ingest.
   - **Creative Shot Roll-up** — 3-column visual index at the end of the section, showing just the creative frames + their library wikilinks. If the reel has no creative frames, write one sentence naming why (absence is signal).
   Do not skip the `message` column. The classification alone is a frame list; the message is what makes the catalogue a reusable shot vocabulary.

6. **Benchmark Checklist** (bulleted `- [ ]`)
   6–10 items a reviewer can tick against a new script to see if it's ripping off the pattern correctly. Derived from the Pattern Rules, not restated.

7. **Transcript**
   - Prose (paragraph) + Timestamped (line per ~2s beat).
   - Keep verbatim. Disfluencies and all.

### Business-brand layers (add on top)

- **Corporate positioning angle** — how does the reel extend the brand's public voice (thought-leadership / product-credibility / category-ownership)?
- **Production signal** — what tells you this is a vetted spend (multi-cam, on-brand chyron, set lighting, licensed music)?
- **Mechanism singularity** — business reels usually carry exactly one technical claim. Name it. If there's more than one, that's a red flag and worth noting.

### Personal-brand layers (add on top)

- **POV authenticity markers** — first-person framing, raw environment, selfie-cam, unpolished captions, native filming device (phone).
- **Offer/CTA placement** — personal brands usually run the CTA in the caption, not in-frame. Note where it lives and whether it's explicit or implied.
- **Identity anchor** — what part of the creator's claimed identity is being reinforced (longevity coach, founder-in-public, niche expert)? Single-topic discipline is a pattern worth surfacing.
- **Shot-length floor** — personal brand cuts are typically tighter (≤3s) because the talking-head is the entire production value. Measure and note.

---

## Carousels

### Common layers (both brand types)

1. **Thesis (1 sentence)** — same rule as reels. Name the move: "pure-type quote-card restatement", "photo-dump collage with buried CTA", "before/after with proof slide".

2. **Slide Map**
   Slide # | Role | Content | Visual. Roles: Hook, Thesis, Restatement, Body/Detail, Proof, CTA, Bio/Sign-off. One table row per slide. This is the carousel equivalent of the beat map.

3. **Pattern Rules Extracted** — same format as reels.

4. **Visual System**
   - Aspect ratio and crop.
   - Template reuse — same layout across slides? Or photo dump?
   - Typography: fonts, weight, stacking.
   - Color/contrast palette.
   - Background treatment (solid / gradient / photo).

5. **Caption + CTA interplay**
   Does the post rely on caption for CTA (DM keyword, comment-gate, link in bio)? Is the final slide a visual CTA, or just a sign-off card? Both mechanics create very different engagement profiles — call out which one.

6. **Benchmark Checklist** — 6–10 items.

7. **Slide Grid**
   3-column table, chronological. Each cell: slide number + `![](../../_Attachments/<folder>/slide_NN.jpg)`.

8. **Full Caption (verbatim)** — blockquoted.

9. **Top Comments / Engagement notes** — brief. Skip emoji-only noise. Note anything that reveals how the audience read the post (did they do the asked CTA, argue, thank, tag).

### Business-brand layers

- **Funnel role** — where does this sit in the brand's funnel? (awareness hook, nurture proof-asset, conversion comment-gate to DM funnel). Business carousels almost always have a retrievable funnel position — name it.
- **Template-as-asset** — is the visual template reused across posts? If yes, note the template's recurring slots. Template reuse is a distribution moat.

### Personal-brand layers

- **Voice signal** — first-person pronoun density, idioms, tells that mark the author as an individual not a brand.
- **Authenticity vs production tradeoff** — polished template undercuts personal-brand trust; photo-dump rawness boosts it but costs scannability. Name which side this piece lands on.
- **Narrative vs advice split** — personal carousels are either "lesson I learned" (narrative) or "here's how you do X" (advice). Note which and why the creator chose it.

---

## Cross-format: when brand_type is ambiguous

Some creators run hybrid accounts (founder posting both personal POV and company announcements). Pick based on *this specific piece*, not the feed. Cues:
- Logo/chyron with company name → business
- First-person singular + raw selfie-cam → personal
- Licensed music + multi-cam → business
- One take, phone camera, unbranded → personal

If genuinely hybrid, tag both in the tags field but pick the dominant one for `brand_type`. Note the hybridity in the Thesis.
