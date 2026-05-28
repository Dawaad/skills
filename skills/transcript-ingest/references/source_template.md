# Transcript Source File Template

Each ingested video produces one source file per target wiki under `Wiki/<Domain>/sources/videos/<slug>.md`. The same transcript bundle is referenced from each — never copied.

## Required frontmatter

```yaml
---
type: wiki-source
wiki: Dev | Riven | Content | Personal | Homelab | Meta | Marketing
source_type: videos
location: <youtube/vimeo/podcast URL>
ingested: YYYY-MM-DD
pages_derived: []
---
```

## Required body sections

```markdown
# <Video title>

- creator: <channel / speaker name>
- duration: <H:MM:SS>
- uploaded: <YYYY-MM-DD>
- bundle: `~/Documents/wiki/_Attachments/transcripts/<slug>-<date>/`
- transcript: `wiki/_Attachments/transcripts/<slug>-<date>/transcript.md`
- source: captions | whisper-base | whisper-medium

## Why this video

One or two sentences: what made this worth ingesting? Name the specific claim,
framework, or technique that pulled you in. If you can't say, you probably
shouldn't be ingesting it.

## Chapter map

If yt-dlp returned chapters, list them verbatim with timecodes. If not, list the
LLM-detected topic shifts the ingest produced — these are your atomic-page
boundaries.

- [HH:MM:SS] — chapter title
- [HH:MM:SS] — chapter title

## Highlights

Verbatim transcript excerpts — the actual sentences that drove a page. Each
excerpt is wrapped with its timecode and attributed:

> `[12:34]` "The thing nobody tells you about Postgres logical replication
> is that the slot survives the subscriber going away…"
> — derived `[[postgres-logical-replication-slot-cleanup]]`

Multiple highlights per source are normal. They are not the page — they are
the receipts.

## Notes

Your raw reactions, not yet synthesized. Anything that surfaced while watching
that didn't make it onto a page yet. Future ingests can mine this.
```

## Multi-wiki fanout

When a video spans multiple domains (common for long-form podcasts, talks,
lectures), write one source pointer **per target wiki**. Each pointer:

- Holds only the highlights relevant to that wiki's pages
- References the same shared bundle in `wiki/_Attachments/transcripts/`
- Lists `pages_derived:` scoped to that wiki's pages only

Cross-link the source files to each other under a `## Companion sources`
section near the bottom:

```markdown
## Companion sources

- [[Wiki/Dev/sources/videos/<slug>]] — Dev-side extraction (Postgres, replication mechanics)
- [[Wiki/Meta/sources/videos/<slug>]] — Meta-side extraction (the "queues vs streams" mental model)
```

This keeps each domain's source file focused while letting a reader trace
the full multi-wiki ingest.
