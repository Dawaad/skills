---
name: changelog
version: 1.0.0
description: |
  Create changelog/devlog entries from recent git activity. Discovers what was
  built, interviews for narrative context, and produces a vault document with
  platform-ready drafts (LinkedIn, X, landing page). Use when the user says
  "changelog", "devlog", "build log", "what's new entry", or invokes /changelog.
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - AskUserQuestion
---

# Changelog / Devlog Entry Creator

You create changelog and devlog entries that capture what was built, why it matters, and produce platform-ready content drafts — all in one document.

## Workflow

### Phase 1: Discover

Inspect the current working directory for git context. Run these commands:

```bash
git log --oneline -20
git diff --stat HEAD~5
```

Also scan for recently modified files in relevant documentation directories:
- Feature designs, ADRs, flows
- Any docs modified in the last week

Present a concise summary of what was built recently.

### Phase 2: Interview

Ask targeted questions **one at a time** using AskUserQuestion. Do not batch questions. Wait for each answer before asking the next.

1. "Which of these changes represents something worth highlighting? What's the single change to focus on?"
2. "What's the outcome for the user? What can they do now that they couldn't before?"
3. "What was the problem before this change? What friction existed?"
4. "Any specific numbers — load times, limits, counts, before/after metrics?"
5. "What's the story behind this? What prompted it, what was hard, what did you learn?"
6. "Do you have a screenshot or recording? If so, what's the file path? If not, we'll skip the visual."

Skip questions where the answer is already obvious from the discovery phase. Adapt follow-ups based on previous answers.

### Phase 3: Draft

Generate the changelog document using the template at `__Templates/Content Creation/Changelog Entry.md`.

**File location:** `2. Areas/2.1 Startup & Business/Riven/5. Changelog/YYYY-MM-DD - <title>.md`

**Title:** Short, outcome-first description of the change (e.g., "Real-time entity sync", "Workspace navigation overhaul")

Fill all sections:

- **What Changed** — One sentence, outcome-first. Lead with what the user gets.
- **Why It Matters** — The problem this solves or friction it removes.
- **Details** — Specific, credible details. Numbers, before/after, technical specifics.
- **Visual** — Embed the visual if provided, otherwise omit this section.
- **The Story** — Human voice devlog angle. What prompted this, what was hard, what you learned.
- **Related** — Wiki links to relevant feature designs, ADRs, domains, or other changelog entries.

**Platform Drafts — follow these adaptation guidelines strictly:**

#### LinkedIn
- **Format:** Thought piece / personal narrative (600-1500 words)
- **Tone:** Conversational, personal, slightly vulnerable
- **Structure:** Hook → story → insight → takeaway
- **Approach:** Longest form, most personal anecdotes, narrative arc matters
- Build-in-public angle: share the journey, the decision-making, the lessons

#### X
- **Format:** Single post or thread (3-6 posts)
- **Tone:** Punchy, quotable, contrarian when possible
- **Structure:** Provocative hook → compressed points → one-line closer
- **Approach:** Maximum compression, build-in-public cadence, revenue transparency when relevant

#### Landing Page
- **Format:** Scannable entry for a "What's New" section
- **Structure:** Title + one-paragraph summary + visual reference
- **Tone:** User-facing, benefit-oriented, concise

**Frontmatter:**
- Set `phase` to `devlog` (pre-MVP) or `changelog` (post-launch)
- Set `category` based on the change type: `feature`, `improvement`, `fix`, `performance`, or `integration`
- Set platform statuses to `drafted`
- Set `visual` to the attachment path if provided

### Phase 4: Review

Present the full draft to the user. Ask:

"Here's the draft. What would you change? Or should I finalize it?"

Iterate based on feedback. Make targeted edits rather than rewriting the whole document.

### Phase 5: Finalize

- Write the final file
- Update `status` in frontmatter to `ready`
- Confirm the file path and suggest next steps (post to platforms, add visual, etc.)

## Rules

- **One change per entry.** If multiple changes are worth highlighting, suggest creating separate entries.
- **Outcome-first language.** Always lead with what the user/customer gets, not what was built internally.
- **No AI slop.** Platform drafts must sound human. No "In today's fast-paced world", no "game-changer", no "revolutionize". Write like a founder talking to peers.
- **Skip empty sections.** If there's no visual, omit the Visual section entirely. Don't write "N/A".
- **Preserve the devlog voice.** The Story section is where personality lives. Don't sanitize it.
