---
name: document
description: >
  Capture knowledge into the Obsidian vault at ~/docs/Documents/ using PARA methodology.
  Trigger on: "document this", "save to docs", "create a resource note", "research and document",
  "update my doc on", "add to my vault", "write up notes on", "/document", or any request to
  save, capture, or organize knowledge into Obsidian.
---

# Document — Obsidian Knowledge Capture

Route knowledge from any Claude Code session into the correct location in the user's PARA-structured Obsidian vault.

**Vault root:** `~/docs/Documents/`

---

## 1. PARA Directory Map

| Path | Purpose |
|------|---------|
| `0. Inbox/` | Quick captures, unsorted notes |
| `1. Projects/` | Goals with defined endpoints |
| `1. Projects/1.1 Startup Development/` | Startup product & engineering tasks |
| `1. Projects/1.2 Online Platform Growth/` | Content/social media growth tasks |
| `1. Projects/1.3 Home-Server/` | Home server build tasks |
| `1. Projects/1.4 Misc/` | One-off projects |
| `2. Areas/` | Ongoing responsibilities |
| `2. Areas/2.1 Startup & Business/` | Business ops, strategy, architecture |
| `2. Areas/2.2 Content & Platform Growth/` | Content standards, strategies, systems |
| `2. Areas/2.3 Knowledge Management/` | PKM processes, vault maintenance |
| `2. Areas/2.4 Home Server + Linux/` | Server administration, Linux config |
| `3. Resources/` | Reference knowledge (concepts, techniques) |
| `3. Resources/3.1 Software Architecture/` | Design patterns, system design, architecture docs |
| `3. Resources/3.2 Startup Development/` | Startup-domain reference material |
| `3. Resources/3.3 Platform Growth/` | Content strategy frameworks, hooks, algorithms |
| `3. Resources/3.4 Productivity & Systems/` | Productivity methods, workflow design |
| `3. Resources/3.5 Linux Configuration/` | Linux setup, tooling, dotfiles |
| `3. Resources/3.6 Home Server Architecture/` | NAS, RAID, networking, self-hosting |
| `3. Resources/3.7 AI/` | AI concepts, prompting, agents |
| `4. Archives/` | Retired/completed content |
| `4. Archives/4.1 Projects/` | Completed projects |
| `4. Archives/4.2 Areas/` | Retired areas |
| `4. Archives/4.3 Resources/` | Outdated resources |
| `__Templates/` | Document templates (never write here) |

### Index files — NEVER modify

- `1. Projects/1. Projects.md`
- `2. Areas/2. Areas.md`
- `3. Resources/3. Resources.md`

---

## 2. PARA Placement Rules

Use this decision framework to classify content:

| Signal | Category |
|--------|----------|
| "Manage / operate / maintain something ongoing" | **Area** |
| "Learn about a concept / technique / framework" | **Resource** |
| "Task with a finish line / deliverable" | **Project** |
| Genuinely unclear | **Inbox** (ask user first) |

**Projects vs Areas:** Projects end. Areas don't. "Set up NAS" is a project. "Home server administration" is an area.

**Resources vs Areas:** Resources are reference knowledge you might look up. Areas contain operational docs you work from. "What is RAID?" is a resource. "My RAID configuration" is an area doc.

If uncertain between two categories, state your reasoning and ask the user to confirm.

---

## 3. Templates

Select the template based on document type:

| Template | Path | Use for |
|----------|------|---------|
| Resource | `__Templates/Resource.md` | Concept notes, research, reference material |
| Project | `__Templates/Project.md` | Tasks with endpoints and success criteria |
| Document Entry | `__Templates/Document Entry.md` | Invoices, receipts, contracts |
| Video Content Piece | `__Templates/Content Creation/Video Content Piece.md` | Video scripts and planning |
| ADR | `__Templates/Software/Decisions/Architecture Decision Record.md` | Architecture decisions |
| Feature Design (Quick) | `__Templates/Software/Design/Feature Design - Quick.md` | Lightweight feature designs |
| Feature Design (Full) | `__Templates/Software/Design/Feature Design - Full.md` | Detailed feature designs |
| Architecture Flow | `__Templates/Software/Documentation/Architecture Flow.md` | System flow documentation |
| Component Overview | `__Templates/Software/Documentation/Component Overview.md` | Component docs |
| Domain Overview | `__Templates/Software/Domain/Domain Overview.md` | Domain model docs |

For general Area documents or notes that don't fit a template, use a minimal structure: frontmatter + `# Title` + relevant headings.

---

## 4. Workflow

Follow these seven steps in order. Do NOT skip the plan step.

### Step 1: Understand

Ask the user what to document. Aim for a single clarifying question, but ask multiple if:
- The topic is ambiguous or too broad
- The scope is unclear (full write-up vs quick note)
- You can't determine the target audience or depth

If the user invoked `/document` mid-conversation, infer context from the session and confirm: *"It sounds like you want to document [X] — is that right?"*

### Step 2: Determine Mode

- **Create new** — default when no existing doc matches
- **Edit existing** — when the user says "update my doc on..." or a relevant doc already exists

For edits, search the vault:
```
Glob: ~/docs/Documents/**/*.md  (filter by keywords)
Grep: search for topic keywords across the vault
```
Show the user what you found and confirm which file to edit.

### Step 3: Classify & Locate

1. Apply the PARA placement rules (Section 2) to pick a category
2. Pick the subdirectory using the directory map (Section 1)
3. State your choice: *"This belongs in `3. Resources/3.1 Software Architecture/` as a reference note."*
4. If uncertain, present options and let the user choose
5. Check for existing sub-folders in the target directory before defaulting to the parent

### Step 4: Gather Structure

1. Read the matching template from `__Templates/` (Section 3)
2. Read 1–2 existing documents in the target directory to match local style and conventions
3. If the target directory is empty, read docs from a sibling directory instead

### Step 5: Research (Optional)

**Only if the user explicitly asked for research** (e.g., "research and document", "look up X and save it").

- Use `WebSearch` to gather 3–5 key insights
- Collect reference URLs for the References section
- Summarize findings before proceeding

If the user did NOT ask for research, extract content from:
- The current session context (conversation, code, errors, decisions)
- Information the user provides directly

### Step 6: Present Plan

**This step is mandatory. Do NOT write the file without user approval.**

Present a structured plan:

```
## Document Plan

- **Mode:** Create new / Edit existing
- **Title:** [Document title]
- **File path:** ~/docs/Documents/[full/path/Title.md]
- **Template:** [Template name] or "Custom structure"
- **Heading outline:**
  - ## Section 1
  - ## Section 2
  - ...
- **Content summary:**
  - Key point 1
  - Key point 2
  - ...
- **Tags:** #tag1, #tag2
- **Wikilinks:** [[Link 1]], [[Link 2]]

Proceed?
```

Wait for the user to approve, modify, or reject the plan.

### Step 7: Write & Confirm

1. Create or edit the file using the Write or Edit tool
2. Report back with:
   - Full file path
   - Brief summary of what was written
   - Suggested related documents to link (`[[wikilinks]]`)

---

## 5. Frontmatter Conventions

### Resource documents
```yaml
---
type: resource
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
tags:
  - topic/subtopic
---
```

### Project documents
```yaml
---
type: Project
date: "YYYY-MM-DD"
active: true
status: Not Started
priority:
effort:
due:
energy:
blocks:
blocked by:
tags:
  - topic/subtopic
---
```

### Area documents
```yaml
---
type: area
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
tags:
  - area/subtopic
---
```

### Software templates (ADR, flows, designs)
Follow the tag conventions defined in each template's frontmatter. Keep the tag options from the template as-is and select the appropriate one.

**Date format:** Always `YYYY-MM-DD`.

---

## 6. Writing Style

- **Direct and practical** — no filler, no preamble
- **Bullet-heavy** — prefer bullets over paragraphs for scannable content
- **Use the user's terminology** — match the language they used in the conversation
- **`[[Wikilinks]]`** — link to related docs in the vault wherever relevant
- **Hierarchical `#tags`** — use `topic/subtopic` format (e.g., `#software/architecture`, `#server/nas`)
- **Headings from the template** — follow the template's heading structure; only add extra headings if necessary
- **No fluff sections** — if a template section isn't relevant, omit it rather than writing "N/A"

---

## 7. Edge Cases

| Situation | Action |
|-----------|--------|
| File exists but is 0 bytes or only whitespace | Treat as **create new** — the file is a placeholder |
| Target directory has nested sub-folders | Check for existing sub-folders before placing at the parent level |
| Content could go in multiple categories | State the trade-off, recommend one, ask user to confirm |
| User wants to document a software decision | Use the ADR template in `__Templates/Software/Decisions/` |
| User wants to document a system flow | Use Architecture Flow template in `__Templates/Software/Documentation/` |
| Placement is genuinely unclear after discussion | Use `0. Inbox/` as a temporary home |
| User says "just save this quickly" | Minimal frontmatter + content in Inbox, skip deep classification |
| Edit would change the document's PARA category | Flag this — suggest moving the file to the new location |
