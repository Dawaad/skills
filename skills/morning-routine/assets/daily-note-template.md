---
type: daily-note
date: {{DATE}}
weekday: {{WEEKDAY}}
created: {{TIMESTAMP}}
tags: [daily, inbox]
focus: {{STANDING_FOCUS_ONE_LINER}}
---

# {{WEEKDAY}}, {{DATE_HUMAN}}

> {{STANDING_FOCUS_ONE_LINER}}

## Briefing

### Slack
{{SLACK_SUMMARY}}

### Email
{{EMAIL_SUMMARY}}

### Calendar
{{CALENDAR_SUMMARY}}

### Standing focus (from weekly schedule)
{{SCHEDULE_TODAY_BLOCKS}}

### Active projects (from project catalog)
{{ACTIVE_PROJECTS_SUMMARY}}

## Today's plan — 3 majors / 3 minors

### Majors

#### 1. {{MAJOR_1_TITLE}}
- **Why:** {{MAJOR_1_WHY}}
- **Success criteria:** {{MAJOR_1_SUCCESS}}
- **Expected outcome:** {{MAJOR_1_OUTCOME}}
- **Time anchor:** {{MAJOR_1_TIME_OR_NA}}
- **Steps:**
{{MAJOR_1_BREAKDOWN}}

#### 2. {{MAJOR_2_TITLE}}
- **Why:** {{MAJOR_2_WHY}}
- **Success criteria:** {{MAJOR_2_SUCCESS}}
- **Expected outcome:** {{MAJOR_2_OUTCOME}}
- **Time anchor:** {{MAJOR_2_TIME_OR_NA}}
- **Steps:**
{{MAJOR_2_BREAKDOWN}}

#### 3. {{MAJOR_3_TITLE}}
- **Why:** {{MAJOR_3_WHY}}
- **Success criteria:** {{MAJOR_3_SUCCESS}}
- **Expected outcome:** {{MAJOR_3_OUTCOME}}
- **Time anchor:** {{MAJOR_3_TIME_OR_NA}}
- **Steps:**
{{MAJOR_3_BREAKDOWN}}

### Minors

#### 1. {{MINOR_1_TITLE}}
- **Why:** {{MINOR_1_WHY}}
- **Success criteria:** {{MINOR_1_SUCCESS}}

#### 2. {{MINOR_2_TITLE}}
- **Why:** {{MINOR_2_WHY}}
- **Success criteria:** {{MINOR_2_SUCCESS}}

#### 3. {{MINOR_3_TITLE}}
- **Why:** {{MINOR_3_WHY}}
- **Success criteria:** {{MINOR_3_SUCCESS}}

## Events today
{{EVENTS_TIMELINE}}

## Capture (add throughout the day)

### Tasks added mid-day
<!-- - [ ] new task that came up -->

### Notable info / decisions
<!-- - decision made, link, or fact worth remembering -->

### Followups
<!-- - person · what to circle back on -->

## End-of-day review

- **Majors completed:** /3
- **Minors completed:** /3
- **What worked:**
- **What didn't:**
- **Carry to tomorrow:**

---

## Placeholder reference

When this template is rendered, replace every `{{TOKEN}}` with the corresponding value:

| Token | Source |
|---|---|
| `{{DATE}}` | ISO date, e.g. `2026-05-14` |
| `{{DATE_HUMAN}}` | Human form, e.g. `May 14, 2026` |
| `{{WEEKDAY}}` | `Thursday` |
| `{{TIMESTAMP}}` | ISO 8601 datetime when the note was written |
| `{{STANDING_FOCUS_ONE_LINER}}` | Phase 4 focus line from `schedule-today` |
| `{{SLACK_SUMMARY}}` | Phase 1 compact summary (use `_Clear._` if quiet) |
| `{{EMAIL_SUMMARY}}` | Phase 2 compressed summary (drop noise rollups) |
| `{{CALENDAR_SUMMARY}}` | Phase 3 volume snapshot + conflicts + RSVPs |
| `{{SCHEDULE_TODAY_BLOCKS}}` | Phase 4 blocks + heads-up |
| `{{ACTIVE_PROJECTS_SUMMARY}}` | Phase 4b — compact list of active projects with each project's next action and any blockers (sourced from `project-tracker` in `morning-context` mode). Use `_None tracked._` if catalog is empty. |
| `{{MAJOR_n_*}}` | Phase 5 plan, majors 1–3 |
| `{{MINOR_n_*}}` | Phase 5 plan, minors 1–3 |
| `{{MAJOR_n_BREAKDOWN}}` | Bullet sub-steps if non-trivial, else `  - _trivial — single action_` |
| `{{MAJOR_n_TIME_OR_NA}}` | e.g. `09:30–11:00` or `—` |
| `{{EVENTS_TIMELINE}}` | Phase 3 chronological events, one per line |

**Delete this reference section before writing the final note** — it's here so future maintainers of the template know what each token means, not for the user to see.
