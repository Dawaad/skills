---
name: transcript-ingest
description: Pull the transcript from any long-form video or podcast URL (YouTube, Vimeo, podcast feeds — anything yt-dlp supports), then extract the discussion's atomic ideas and route them into the right domain wikis as proper pages. Use whenever the user shares a YouTube/Vimeo/podcast/talk/lecture URL and wants the *ideas* captured into their wiki — phrases like "ingest this video", "pull the transcript", "what are the takeaways from this talk", "summarize this podcast into my wiki", "extract topics from this", "add this lecture to my notes", "what's in this video", "wiki-fy this YouTube link", "/transcript-ingest", or any moment the user pastes a long-form video URL alongside intent like "save this", "what should I learn from this", "break this down", or "what's discussed in this". Also trigger when the user explicitly contrasts this against the Instagram benchmark flow ("not for the Content wiki, just the ideas") — that's the signal this is the right skill, not content-media-ingest. Do NOT use for Instagram Reels or short-form benchmark capture (that's content-media-ingest); do NOT use for arbitrary file/article ingest (that's the /wiki-ingest command).
---

# Transcript Ingest

Pipeline that turns one long-form video/podcast URL into atomic wiki pages across whichever domains the discussion actually touches. The transcript is just the raw material — the value is in the topic extraction and the multi-wiki routing.

## Why this exists (and what makes it different from siblings)

- `content-media-ingest` is for **short-form Instagram benchmarks**. The output is a single `flow`-kind page in `Content/` with a shot catalogue and a benchmark checklist. The unit is the *piece*.
- `transcript-ingest` (this skill) is for **long-form ideas**. The output is N atomic pages across whatever wikis the ideas belong in — `Dev/`, `Personal/`, `Meta/`, etc. The unit is the *idea*.
- `/wiki-ingest` is the generic ingest command. This skill specializes it for the case where the source is a video URL whose transcript must be extracted first, and where one source usually fans out into many pages.

If the user pastes an `instagram.com/reel/` or `instagram.com/p/` URL, hand off to `content-media-ingest`. Anything else long-form — YouTube, Vimeo, podcast MP3, Twitter/X video, lecture recording — is this skill's job.

## Inputs

- **URL** (required) — any URL `yt-dlp` can resolve. YouTube is the primary case; podcasts, talks, conference recordings, Twitter videos, and direct MP3/MP4 links all work.
- **target wikis hint** (optional) — if the user says "this is for Dev and Meta only", honor it; otherwise let topic extraction decide and propose fanout.
- **transcription mode** (optional) — default is captions-first with whisper fallback. Override to `--force-whisper` if the user wants a clean transcription even when captions exist (auto-captions on dense technical talks are often unusable).

Vault root: `/home/jared/Documents/`. Wikis live under `/home/jared/Documents/wiki/`.

## Pipeline

### Step 1 — Extract transcript + metadata

Run the extractor:

```bash
python3 /home/jared/.claude/skills/transcript-ingest/scripts/extract_transcript.py \
  "<URL>" \
  --save-dir ~/Documents/wiki/_Attachments/transcripts
```

Add `--force-whisper` if the user wants whisper even when captions exist.

The script writes a self-contained bundle to `~/Documents/wiki/_Attachments/transcripts/<slug>-<YYYY-MM-DD>/`:

```
<slug>-<date>/
├── transcript.md      ← timestamped lines, this is the primary working artifact
├── transcript.vtt     ← raw subtitles
├── metadata.json      ← full yt-dlp .info.json
├── chapters.json      ← extracted chapter list (may be empty array)
└── audio.m4a          ← only present if whisper was used
```

The script's final stdout lines tell you where everything landed, the line count, the chapter count, and which transcription path was used. Read those — they shape the next step.

Common failures and what they mean:

- `yt-dlp metadata failed` → URL is geo-blocked, private, or yt-dlp needs upgrading. Tell the user; don't fabricate.
- Caption attempt produced no `.en*.vtt` → the script will auto-fall through to whisper. That's fine, just slower (~real-time on CPU for the `base` model).
- whisper missing → install via `pip install --user openai-whisper` and ffmpeg. Surface the error rather than skipping.

### Step 2 — Read the transcript and the chapter map

Open `transcript.md` and `chapters.json`. Read the whole transcript end-to-end before doing anything else — topic extraction is much worse if you start carving pages while still mid-watch.

For very long sources (>1h), read chapter-by-chapter. The chapter list (when present) is your first-cut topic boundary. When `chapters.json` is empty, you'll do the topic-shift detection yourself.

### Step 3 — Extract atomic topics

Load `references/topic_extraction.md` and follow it. The short version:

1. Identify candidate atomic ideas in the transcript. One idea = one candidate.
2. Filter aggressively. Skip obvious-from-docs material, generic platitudes, anecdotes without transferable claims, and dupes of existing pages.
3. For each surviving candidate, pick exactly one `kind` (`decision` / `flow` / `feature` / `interaction` / `sop` / `insight` / `framework`).
4. Route each candidate to the right wiki — see `references/wiki_routing.md`. Multi-wiki fanout is expected and desirable for genuinely cross-domain content.

### Step 4 — Propose, then confirm

Before writing any pages, produce a proposal table and show it to the user:

```markdown
| # | Target wiki | Kind | Page slug | One-line summary |
|---|-------------|------|-----------|------------------|
| 1 | Dev | insight | <slug> | <one sentence> |
| 2 | Meta | framework | <slug> | <one sentence> |
| ... |
```

Also list anything you *skipped* and why — that's how the user catches mis-filters early. The user can approve, edit slugs, drop rows, request splits/merges, or change target wikis. Only proceed once they confirm.

This step is not optional. Long-form sources can yield 5–15 candidate pages; writing them all without confirmation produces wiki bloat the user has to clean up later.

### Step 5 — Write source pointers (one per target wiki)

For each unique target wiki in the approved proposal, create:

```
Wiki/<Domain>/sources/videos/<slug>.md
```

Format per `references/source_template.md`. Critical points:

- The bundle lives in `wiki/_Attachments/transcripts/` and is shared across all source pointers — never duplicate.
- Each source pointer holds **only** the highlights relevant to that wiki's pages. Don't dump the full transcript into each pointer.
- The `## Highlights` section quotes the actual transcript lines (with their `[HH:MM:SS]` timecode) that drove each page. These are the receipts.
- If the video fans out to ≥2 wikis, cross-link the source pointers under each one's `## Companion sources` section.

### Step 6 — Write or update pages

For each approved row in the proposal:

1. Check `Wiki/<Domain>/index.md` for an existing page on the same topic.
2. **If exists:** read the page, integrate the new evidence, rewrite the body — don't append. Add the new source to `sources:`. If the wiki uses the L3 decay-tracker format (`Wiki/<Domain>/retrieval.yaml` exists), include `cited_region` and `content_hash` per the schema in `~/Documents/wiki/.claude/commands/wiki-ingest.md`.
3. **If new:** create `Wiki/<Domain>/pages/<slug>.md` per the master schema in `~/Documents/wiki/CLAUDE.md`. ≤300 words. Lead with the claim/rule/insight, not the setup. Use the kind-specific structure from the target wiki's `CLAUDE.md`.

Cross-link aggressively via `[[page-name]]` — wikilinks resolve across all wikis, so a `Dev/` insight page can cite a `Meta/` framework and a `Personal/` SOP in the same paragraph.

### Step 7 — Update each affected index

For each wiki you touched, add or update entries in `Wiki/<Domain>/index.md` under the matching section. One line per page: `- [[page-name]] — one-line summary`. Match the wiki's existing grouping style (by kind, by topic, etc.) — don't invent a new layout.

### Step 8 — Update source pointers with `pages_derived`

Go back to each source pointer you wrote in Step 5 and fill in the `pages_derived:` frontmatter array with the actual pages you produced for that wiki. This closes the loop — anyone reading the source can see exactly what came out of it.

### Step 9 — Append to each affected wiki's log

For each wiki you touched, append to `Wiki/<Domain>/log.md`:

```
## [YYYY-MM-DD] ingest | <video title> (<creator>, <duration>)
- [[page-slug-1]] (new) [insight] — <one-line>
- [[page-slug-2]] (updated) [framework] — <what changed>
- source: `sources/videos/<slug>.md` → bundle `wiki/_Attachments/transcripts/<slug>-<date>/`
- skipped: <candidate idea> — <reason>
- patterns surfaced (not yet promoted to pages): <optional — half-formed observations>
```

The `skipped:` line is non-negotiable. It's how the wiki stays lean — the model has to justify what it didn't include so future readers (and future-you) can see the editorial bar.

### Step 10 — Report

Final report to the user:

1. Bundle: `~/Documents/wiki/_Attachments/transcripts/<slug>-<date>/` — confirm `transcript.md`, `metadata.json`, `chapters.json` exist; confirm whether `audio.m4a` is present (whisper path) or absent (captions path).
2. Source pointers written: one path per wiki touched.
3. Pages created / updated: grouped by wiki, with kind.
4. Cross-links added between wikis.
5. Indexes + logs updated: list the files.
6. Skipped candidates: list each with reason — this is the lean-keeping artifact.

Then paste the **one-sentence thesis** of the video so the user can sanity-check that the synthesis caught the right core idea before walking away.

## What to avoid

- **Don't write pages before the user confirms the proposal table.** Step 4 is the trust mechanism. Skipping it produces wiki bloat that's hard to undo.
- **Don't dump the full transcript into the source pointer.** The transcript lives in the bundle. The source pointer holds the *highlights* with timecodes — the receipts for the pages it derived.
- **Don't single-wiki-bias to `Content/` just because the source is a video.** Routing is based on the *page's claim*, not the source's medium.
- **Don't fabricate timecodes, claims, or attributions.** If a candidate's evidence isn't in the transcript verbatim, don't write the page — re-watch or drop the candidate.
- **Don't ingest tutorials Claude can already derive from docs.** "Use `useState` to hold component state" is not a wiki page. The wiki is for non-obvious insight, observed truth, or earned procedure.
- **Don't skip the `skipped:` line in the log.** What you *didn't* ingest is half the editorial signal.
- **Don't conflate kinds.** If a candidate is both a procedure AND a framework, split it. Two narrow pages beat one blurry page.
- **Don't use this for Instagram Reels or short-form benchmarks.** Hand off to `content-media-ingest`.

## Reference files

- `scripts/extract_transcript.py` — the extractor itself (yt-dlp captions, whisper fallback). Read its docstring if you need to tune behavior.
- `references/source_template.md` — exact shape of the per-wiki source pointer, including the multi-wiki companion-source cross-link pattern.
- `references/topic_extraction.md` — the atomic-idea extraction procedure, the filter rules, the proposal-table format.
- `references/wiki_routing.md` — which wiki gets which kind of claim, plus the rules for cross-domain fanout vs single-wiki placement.
- The master wiki schema lives at `~/Documents/wiki/CLAUDE.md`. Always read it before writing pages so the page format, frontmatter, and kind-specific structure stay consistent with the rest of the vault.
