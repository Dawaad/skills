# Topic Extraction from Long-Form Transcripts

The transcript is raw material. The pages are the product. This file is the bridge.

## Goal

Identify the **atomic ideas** in the transcript — each one a candidate page.
"Atomic" means: one concept, one claim, one procedure, one mental model. If a
candidate cannot be summarized in a single sentence, it is two candidates.

## Procedure

### 1. Read the transcript holistically first

Do not start extracting on a per-paragraph basis. Read the whole transcript
end-to-end (or skim chapter-by-chapter for very long videos). You are looking
for the *shape* of the talk before you start carving pages out of it.

### 2. Use chapters as the first-cut boundary

If `chapters.json` is non-empty, every chapter is a candidate topic region.
Within each chapter there may be 0–3 atomic pages. A chapter is not
automatically a page — many chapters are setup, framing, or filler.

If `chapters.json` is empty, do the topic-shift detection manually: look for
phrases like "okay, switching gears", "the second thing", "let me give you an
example", or hard subject changes 30+ seconds apart.

### 3. Filter aggressively

Skip the candidate if any of the following is true:

- It restates content easily derivable from a tutorial, README, or the
  official docs of the named tool/lib (e.g. "you use `useState` to hold
  component state"). The wiki is for non-obvious insight.
- It is a generic platitude ("be consistent", "ship fast"). No specifics =
  no page.
- It is purely anecdotal with no transferable claim ("we had a bug last
  Tuesday and it was annoying"). If the anecdote leads to a transferable
  rule, the page is the rule, not the anecdote.
- It duplicates an existing page in the target wiki without adding new
  evidence. In that case, *update* the existing page — append the new
  evidence under `## Evidence` or merge into the prose.

### 4. Classify each surviving candidate

Pick exactly ONE `kind` per page (per `Wiki/CLAUDE.md`):

| The candidate explains… | kind |
|-------------------------|------|
| Why a path was chosen over another, with criteria + tradeoffs | `decision` |
| The end-to-end mechanics of an event/request through a system | `flow` |
| How a sub-feature orchestrates its components | `feature` |
| How component A talks to component B | `interaction` |
| A repeatable procedure ("do it this way") | `sop` |
| An observed truth about the world ("X is true / happens") | `insight` |
| A reusable lens for thinking about a class of problems | `framework` |

If the candidate blurs two kinds, split it into two pages. Splitting is
almost always the right call.

### 5. Route each candidate to a wiki

See `wiki_routing.md`. A candidate may legitimately fan out to 2–3 wikis
(e.g., a podcast on developer career strategy → `Personal` for the energy/
focus piece, `Dev` for the technical patterns, `Meta` for the underlying
career framework). But every fanout should be justified by genuinely
different insight, not the same insight stamped on multiple pages.

### 6. Produce a proposal table

Before writing any pages, produce a proposal for user confirmation:

```markdown
| # | Target wiki | Kind | Page slug | One-line summary |
|---|-------------|------|-----------|------------------|
| 1 | Dev | insight | postgres-logical-replication-slot-survives-restart | Logical replication slots persist on the publisher across subscriber restarts and require manual cleanup. |
| 2 | Meta | framework | streams-vs-queues-substitution-mental-model | Treat "queue" and "stream" as substitutable only when consumer semantics match (at-least-once vs at-most-once). |
| 3 | Personal | sop | review-foundational-papers-before-shipping-novel-design | Before designing a system in a category you haven't built before, read the seminal paper plus one production post-mortem. |
```

Then ask the user to approve, edit, or drop rows. Only after confirmation
do you write pages.

## Anti-patterns

- **Chapter ≡ page.** Many chapters produce zero pages (intro, sponsor read,
  outro) or three pages (dense technical segment). Don't force 1:1.
- **Transcript-quoting page bodies.** The page is the synthesized claim,
  not a long quote. Verbatim excerpts live in the source file's
  `## Highlights` section, not the page body.
- **Single-wiki bias.** Don't dump every page into `Content/` just because
  the source was a video. The target wiki is determined by the *content*
  of the page, not the medium of the source.
- **Skipping the proposal step.** Writing pages before the user confirms
  the proposal table burns trust and produces wiki bloat.
