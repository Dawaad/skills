---
description: "Save knowledge from the current session to the Obsidian vault. Available globally — use from any Claude Code project."
---

# /save — Save to Obsidian Vault

Capture knowledge discovered or discussed in the current session and write it to the Obsidian vault at `~/docs/Documents/`.

This command is self-contained — it embeds all vault conventions since the vault's `CLAUDE.md` isn't loaded when running from outside projects.

## Input

$ARGUMENTS

## Workflow

### 1. Infer What to Save

If `$ARGUMENTS` is provided, use it as the topic.

If invoked mid-conversation without arguments, infer from session context and confirm:
> "Sounds like you want to save [X] — right?"

### 2. Classify with PARA Rules

| Signal | Category | Target |
|--------|----------|--------|
| Task with a finish line / deliverable | **Project** | `1. Projects/` |
| Ongoing responsibility / operational docs | **Area** | `2. Areas/` |
| Concept / technique / reference knowledge | **Resource** | `3. Resources/` |
| Genuinely unclear | **Inbox** | `0. Inbox/` |

**Subdirectory map:**

| Path | Purpose |
|------|---------|
| `0. Inbox/` | Quick captures, unsorted notes |
| `1. Projects/1.1 Startup Development/` | Startup product & engineering tasks |
| `1. Projects/1.2 Online Platform Growth/` | Content/social media growth tasks |
| `1. Projects/1.3 Home-Server/` | Home server build tasks |
| `1. Projects/1.4 Misc/` | One-off projects |
| `2. Areas/2.1 Startup & Business/` | Business ops, strategy, Riven |
| `2. Areas/2.2 Content & Platform Growth/` | Content standards, strategies |
| `2. Areas/2.3 Knowledge Management/` | PKM processes, vault maintenance |
| `2. Areas/2.4 Home Server + Linux/` | Server admin, Linux config |
| `3. Resources/3.1 Software Architecture/` | Design patterns, system design |
| `3. Resources/3.2 Startup Development/` | Startup-domain reference |
| `3. Resources/3.3 Platform Growth/` | Content strategy, algorithms |
| `3. Resources/3.4 Productivity & Systems/` | Productivity methods, workflows |
| `3. Resources/3.5 Linux Configuration/` | Linux setup, tooling, dotfiles |
| `3. Resources/3.6 Home Server Architecture/` | NAS, RAID, networking, self-hosting |
| `3. Resources/3.7 AI/` | AI concepts, prompting, agents |

### 3. Pick Target Subdirectory

Choose the most specific subdirectory that fits. If uncertain, state reasoning and ask.

### 4. Read Template

Select and read the matching template from `~/docs/Documents/__Templates/`:

| Template | Path | Use for |
|----------|------|---------|
| Resource | `__Templates/Resource.md` | Concept notes, research, reference |
| Project | `__Templates/Project.md` | Tasks with endpoints and success criteria |
| Task | `__Templates/Task.md` | Focused tasks with goal + outcomes |
| Document Entry | `__Templates/Document Entry.md` | Invoices, receipts, contracts |
| ADR | `__Templates/Software/Decisions/Architecture Decision Record.md` | Architecture decisions |
| Feature Design (Quick) | `__Templates/Software/Design/Feature Design - Quick.md` | Lightweight feature designs |
| Feature Design (Full) | `__Templates/Software/Design/Feature Design - Full.md` | Detailed feature designs |
| Architecture Flow | `__Templates/Software/Documentation/Architecture Flow.md` | System flow docs |
| Component Overview | `__Templates/Software/Documentation/Component Overview.md` | Component docs |
| Domain Overview | `__Templates/Software/Domain/Domain Overview.md` | Domain model docs |

### 5. Read Local Style

Read 1-2 existing documents in the target directory to match local conventions and voice.

### 6. Present Plan — WAIT FOR APPROVAL

**Do NOT write without approval.**

```
## Save Plan

- **Mode:** Create new
- **Title:** [Document title]
- **File path:** ~/docs/Documents/[full/path/Title.md]
- **Template:** [Template name]
- **Heading outline:**
  - ## Section 1
  - ## Section 2
- **Tags:** #tag1, #tag2
- **Wiki links:** [[Link 1]], [[Link 2]]

Proceed?
```

### 7. Write File

Use the Write tool to create the file at `~/docs/Documents/[path]`.

**Frontmatter conventions:**

Resource:
```yaml
---
type: resource
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
tags:
---
```

Project:
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
blocks: []
blocked by: []
tags:
---
```

Area:
```yaml
---
type: area
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
tags:
---
```

**Writing style:**
- Direct and practical — no filler
- Bullet-heavy — prefer bullets over paragraphs
- `[[Wiki links]]` — aggressively link to related vault docs
- Hierarchical `#tags` — `#topic/subtopic` format
- Follow template headings, omit empty sections

### 8. Report

- Full file path
- Brief summary of what was written
- Suggested `[[wiki links]]` to related docs

## Rules

- **Plan-then-write** — always wait for approval
- **No web research** — only captures from session context
- **No task creation workflow** — use `/task` in the vault for that
- **No domain-aware behavior** — uses PARA rules only (no domain CLAUDE.md reading)
- **Date format:** Always `YYYY-MM-DD`

## Index Files — NEVER Modify

- `1. Projects/1. Projects.md`
- `2. Areas/2. Areas.md`
- `3. Resources/3. Resources.md`
