---
name: project-tracker
description: Manage and query the user's catalog of active projects — semi-complex undertakings that span multiple sessions like architectural migrations, feature builds, video productions, content series, or personal initiatives. Owns the project files at /home/jared/Documents/wiki/Personal/projects/ (one markdown file per project, an index.md catalog, and an archive/ for completed work). Use this skill whenever the user wants to see what they're working on across all responsibilities, add a new active project, log progress, change a project's status (active/paused/completed/cancelled), update the next action, record a blocker, or pull active-project context into other workflows. Trigger on "active projects", "what am I working on", "project status", "show my projects", "list projects", "add a project", "new project", "update [project name]", "log progress on", "what's next on [project]", "mark [project] done", "complete [project]", "pause [project]", "resume [project]", "drop [project]", "project tracker", "show me the project catalog", "what's stuck", "what's blocked", or any variation of querying or mutating the user's portfolio of active work. Also trigger when another skill (especially morning-routine) needs the current active-project list as planning context — surface a compact summary on request. Do NOT trigger for one-off tasks, daily to-dos, or items already living in today's daily note — those belong in the daily plan (morning-routine) or the inbox, not the project catalog.
---

# project-tracker

Owns the user's catalog of active projects. The project catalog lives at:

```
/home/jared/Documents/wiki/Personal/projects/
  index.md            # one-line-per-project catalog grouped by status
  <slug>.md           # one file per project, with frontmatter + structured body
  archive/            # completed and cancelled projects move here
    <slug>.md
```

A "project" here is a semi-complex undertaking that spans more than one work session — examples the user has named: architectural migrations, feature builds, whole video productions, content series, personal initiatives. **Not** small to-dos, not daily tasks, not items that fit comfortably inside a single morning plan.

## Why this exists

The user runs many strands of work in parallel — Cranium builds, content production, personal systems, infra. Without a catalog, the morning planning ritual has to be reconstructed from memory each day and active projects drift. This skill gives every multi-session effort a persistent home with: a stated goal, success criteria, the current state, and the next concrete action. That way, daily planning anchors on real momentum instead of whichever project happened to be top-of-mind.

The catalog is also the source of truth that `morning-routine` consults when building the day's plan. If a project isn't in the catalog, it shouldn't be quietly competing for attention.

## Project file format

Every project is a single markdown file. Keep them lean — this is a working catalog, not a journal. The log section is append-only and short.

```markdown
---
type: project
status: active           # active | paused | completed | cancelled
category: <one of: architecture | feature | video | content | infra | personal | other>
domain: <one of: cranium | content | personal | homelab | other>
priority: normal         # high | normal | low
created: YYYY-MM-DD
updated: YYYY-MM-DD
deadline: YYYY-MM-DD     # optional — drop the line if none
tags: []
---

# <Project Name>

## Goal
<1–3 sentences. What "done" looks like and why this matters. Concrete enough that someone re-reading next month can tell whether progress has been made.>

## Success criteria
- <objective signal #1 — bias toward measurable / verifiable>
- <objective signal #2>
- <…>

## Current state
<1–4 sentences. Where things actually stand right now. Updated every time meaningful progress (or non-progress) happens. This is the field most other skills will read — keep it accurate.>

## Next action
<The very next concrete step. One thing. If it's vague, decompose until it's a verb + an artifact ("draft the migration plan doc", "open PR on auth-rewrite branch", "shoot the B-roll for hook 3"). When the next action lands inside today's daily note, restate it here too so the catalog stays self-sufficient.>

## Blockers
<What's actually stopping the next action, or "none". Be specific — "waiting on X from Y" beats "waiting on review".>

## Log
- YYYY-MM-DD: <one-line progress note — what moved, what didn't>

## Cross-links
- [[wiki-page]]                 # any Personal/Cranium/Content/etc page that informs this
- /home/jared/path/to/code      # repo paths, design docs, anything pointer-worthy
```

Body rules:
- Total file ≤ ~150 lines. If a project's notes grow past that, the deep notes belong in a `[[…]]` wiki page or design doc and get linked from `Cross-links` — keep this file as the *spine*.
- Lead with goal + success criteria. The current-state / next-action pair is the pulse — those are what the morning routine will read.
- `updated:` frontmatter and `Log` entries should move together. Every meaningful edit touches both.
- Slug = lowercase, kebab-case, derived from the project name (e.g. "Cranium Auth Rewrite" → `cranium-auth-rewrite.md`).

## The index file

`projects/index.md` is the fast-glance catalog. Auto-maintained by this skill — every mutation to a project file should also update the index so the two never drift.

```markdown
---
type: project-index
Updated: YYYY-MM-DD
---

# Active Projects

## Active
- [[cranium-auth-rewrite]] — auth middleware migration; PR open, waiting on review · next: address review comments · updated 2026-05-12
- [[ig-change-series-v1]] — 6-part change series for personal IG · next: film hook 3 · updated 2026-05-13

## Paused
- [[homelab-nas-rebuild]] — paused 2026-04-30, resume when drives arrive

## Completed (last 14 days)
- [[outbound-prospect-pipeline]] — completed 2026-05-10
```

Index conventions:
- One line per project. Format: `[[slug]] — <one-liner from goal/state> · next: <next action> · updated <date>` (drop fields that aren't relevant — paused projects don't need "next:").
- Group by status. Active first, paused second, recently completed (last 14 days) third. Older completed work just lives in `archive/` and doesn't clutter the index.
- If active list grows past ~7 projects, surface that to the user — too many concurrent projects is a planning failure, not a feature.

## Operations

This skill is multi-modal. Figure out which operation the user is asking for, then run it. If the intent is ambiguous, default to **list** — showing the catalog usually tells the user what they wanted to know.

### list — show active projects

Default behavior when the request is vague ("what am I working on", "show projects", "project status").

1. Read `index.md`. If missing, generate it from the project files (read frontmatter from each `*.md`, build the index, write it). If the directory itself is empty, tell the user there are no projects yet and offer to add one.
2. Output a compact view:

```
Active projects (<N>)
1. <name> — <one-liner> · next: <next action> · updated <relative date e.g. "2d ago">
2. …

Paused (<N>)
- <name> — <reason / when to resume>

Stuck / blockers worth noting
- <name>: <blocker>
```

- Use relative dates ("today", "2d ago", "last week") in chat. Absolute dates only in files.
- Surface any project where `updated` is >14 days old with a `⏳ stale` tag. Not a problem per se, just visibility.
- If the user asked about a specific status ("what's paused?", "what did I finish this month?"), filter accordingly.

### query — show one project in detail

Triggered by "what's the status on [project]", "show [project]", "where am I on [project]".

1. Resolve the project name to a slug (fuzzy match — the user will rarely say the exact slug). If multiple match, list candidates and ask.
2. Read the project file. Output:

```
<Name> · <status> · updated <relative date>

Goal: <one-paragraph>
Current state: <as-is>
Next action: <as-is>
Blockers: <as-is, or "none">

Recent log
- <last 3–5 entries>
```

- Don't dump the whole file. The user is asking for orientation, not an archive.

### add — create a new project

Triggered by "new project", "add a project", "start tracking [thing]".

1. Run a short interview to fill the template. Ask for:
   - **Name** (then derive slug — confirm if the slug isn't obvious).
   - **Goal** — what done looks like. Push back if it's too vague to grade later.
   - **Success criteria** — at least one objective signal. If the user can't name one, suggest 1–2 based on the goal and confirm.
   - **Category** + **domain** (offer the enum, accept first matching word).
   - **Next action** — one concrete step. If they say "figure out where to start", help them turn that into a real next action (e.g. "30-min scoping session: list components touched and write it as a checklist").
   - **Deadline** — optional. Skip if not relevant.
2. Write the project file. Update `updated:` and `created:` to today.
3. Add a line to `index.md` under `## Active`.
4. Confirm in chat: `Tracked: <name> (<slug>) — next: <next action>.`

Interview principles:
- Don't ask everything in one wall-of-text. Two or three questions at a time. The user is starting a project, not filing a form.
- If the user has already given the info in the conversation (e.g. they were just discussing it), pre-fill and confirm rather than re-asking. The point is friction reduction.

### update — record progress / change next action / log a note

Triggered by "update [project]", "log progress on [project]", "[project] — done with X", "next on [project] is Y".

1. Resolve project → file. Fuzzy match; ask if ambiguous.
2. Decide what fields the user is updating:
   - **Current state** → rewrite the section.
   - **Next action** → replace.
   - **Blockers** → set or clear.
   - **Log entry** → prepend (newest first) a `- <today>: <note>` to the Log section. Always also bump `updated:` to today.
3. Most updates touch at least the log + `updated:`. The log is the audit trail — keep entries one line each, factual.
4. Mirror any change that affects the one-liner (state, next action, status) into `index.md`.
5. Confirm in chat with a one-line summary of what changed.

If the user gave free-form context ("I finished the auth review, now starting on the migration script"), parse it into the structured fields rather than dumping it raw into Current state. The whole point of the structure is that it stays queryable.

### status change — pause / resume / complete / cancel

Triggered by "pause [project]", "resume [project]", "[project] is done", "mark [project] complete", "drop [project]", "cancel [project]".

1. Resolve project → file.
2. Update `status:` in frontmatter and `updated:` to today.
3. Append a log entry recording the transition (e.g. `- 2026-05-14: paused — waiting on drives`).
4. For **completed** or **cancelled**:
   - Move the file to `archive/`.
   - Remove from `## Active` in `index.md` and (for completed) add under `## Completed (last 14 days)`. Drop completed entries older than 14 days from the index — the file stays in `archive/`.
   - For completed projects, prompt the user once: "Anything worth lifting into the wiki as a `kind: insight` or `kind: framework`?" — don't push, but don't lose the chance to capture learning.
5. For **paused**, keep the file in `projects/` (not archive) but move the index entry under `## Paused` with a note on what resume looks like.
6. For **cancelled**, also offer to write a short post-mortem entry under the project's Log before archiving — "what stopped this" is high-value future context.

### morning-context — emit a compact summary for other skills

Triggered by `morning-routine` (or any other skill) needing active-project context for planning. This is a non-interactive operation — output is structured, no chat affordances.

1. Read all active (and optionally paused) project files.
2. Output:

```
ACTIVE PROJECTS — <N>

- <name> [<domain>/<category>] · <priority>
  state: <one-line current state>
  next: <next action>
  blockers: <or "none">
  updated: <date>
```

- Sort by priority (high → low), then by `updated:` desc.
- Optionally include `deadline:` if within 14 days — surface it inline as `⏰ due <date>`.
- This is the contract `morning-routine` reads. Keep it stable.

## Integration with other skills

- **`morning-routine`** — Before Phase 5 (the propose-then-confirm plan), call this skill in `morning-context` mode to get the active-project list. Use it as a primary source of "majors": at least one of the three majors should usually be a deliberate next-action on an active project, unless the day's standing focus (filming, content research, etc.) overrides. After the user approves the plan, if any major was a project's next action, mirror that back: update the project's Log and `updated:` field with a one-liner like `pulled into <date> daily plan` so the catalog stays in sync.
- **`schedule-today`** / **`schedule-manage`** — These own *time allocation*. project-tracker owns *what's competing for the time*. They're complementary, not overlapping. Don't put projects in the schedule and don't put time-blocks in projects.
- **`changelog`** — When the user runs a changelog/devlog ritual, completed projects from `archive/` are obvious source material. Make sure completed projects have a useful final log entry so the changelog has something to draw from.
- **wiki pages** (`Personal`, `Cranium`, etc.) — A project file is a *spine*. Deep design work, decisions, insights, retros belong in proper wiki pages with the right `kind:` and get linked from `Cross-links`. Don't bloat the project file with knowledge that wants to outlive the project.

## Principles

- **One project = one outcome.** If a "project" has two unrelated goals, it's two projects. Split it during the add interview.
- **Structured > prose.** Free-form narrative belongs in the log. The state / next / blockers / criteria fields exist because they're queryable and skim-able.
- **Updates touch the index.** A mutation that doesn't update `index.md` creates drift. Always mirror.
- **Stale is signal, not failure.** If a project hasn't been touched in 30+ days, that's worth surfacing — it usually means the project is silently dead, the next action is too vague to start, or the priority has changed. Don't auto-archive; tell the user and let them decide.
- **Don't over-track.** Two-hour tasks aren't projects. If a request looks like a to-do, route it to the daily note instead — say so plainly: "this fits today's plan rather than the project catalog."
- **Be terse in chat, structured in files.** The chat surface is a glance; the files are the working document. Mirror what schedule-today and morning-routine already establish.

## Failure modes to avoid

- Asking the user to refill the whole template every update. The catalog should feel like a low-friction tool.
- Letting `index.md` drift from project files. Always re-derive it from frontmatter if there's any doubt.
- Auto-archiving paused projects after some time-based rule. Pausing is a deliberate state; only the user moves it.
- Treating "completed" as success. A cancelled project that the user learned from is more valuable than a completed one that was the wrong thing — capture the learning either way.
- Inventing categories or statuses. Stick to the enum unless the user proposes an extension; if they do, update this skill's documentation.

## Bootstrap

If `Wiki/Personal/projects/` doesn't exist yet, create it (with an empty `archive/` subdir) and write a stub `index.md`. Tell the user the catalog is initialised and offer to add their first project — but only if they were actually asking to use the skill, not if some other flow just probed it for `morning-context`.
