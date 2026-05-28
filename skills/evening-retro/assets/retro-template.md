---
type: retro-snapshot
date: {{DATE}}
weekday: {{WEEKDAY}}
created: {{TIMESTAMP}}
focus_character: {{STANDING_FOCUS_ONE_LINER}}
energy: {{ENERGY_1_TO_10}}
focus_rating: {{FOCUS_1_TO_10}}
mood: {{MOOD_SHORT}}
majors_completed: {{MAJORS_COMPLETED}}/3
minors_completed: {{MINORS_COMPLETED}}/3
criteria_met_rate: {{CRITERIA_MET_PCT}}
projects_touched: {{PROJECTS_TOUCHED_LIST}}
tags: {{TAGS}}
---

# Retro — {{WEEKDAY}}, {{DATE_HUMAN}}

> {{ONE_LINE_DAY_SUMMARY}}

## Plan grading

### Majors
{{MAJORS_GRADED_BLOCK}}

### Minors
{{MINORS_GRADED_BLOCK}}

## Projects touched
{{PROJECTS_TOUCHED_BLOCK}}

## Journal
{{JOURNAL_PROSE}}

## Workflow assessment

- **Today vs 7-day avg:** {{COMPARISON_BLOCK}}
- **Patterns surfaced:** {{PATTERNS_BLOCK_OR_NONE}}

## Adjustments

### Logged to planning-adjustments
{{ADJUSTMENTS_LOGGED_OR_NONE}}

### One-day experiment for tomorrow
{{TOMORROW_EXPERIMENT_OR_NONE}}

## Insight candidates
{{INSIGHT_CANDIDATES_OR_NONE}}

## Cross-links
- Daily note: [[../../Inbox/{{DATE}}]]
- Schedule: [[../schedule]]
{{PROJECT_CROSS_LINKS}}

---

## Placeholder reference

When this template is rendered, replace every `{{TOKEN}}` with the corresponding value. Drop optional blocks entirely (don't leave empty sections) when there's nothing to put.

| Token | Source |
|---|---|
| `{{DATE}}` | ISO date, e.g. `2026-05-14` |
| `{{DATE_HUMAN}}` | Human form, e.g. `May 14, 2026` |
| `{{WEEKDAY}}` | `Thursday` |
| `{{TIMESTAMP}}` | ISO 8601 datetime when the retro was written |
| `{{STANDING_FOCUS_ONE_LINER}}` | Phase 1 focus line (from the daily note or `schedule-today`) |
| `{{ENERGY_1_TO_10}}` / `{{FOCUS_1_TO_10}}` | Phase 4 self-ratings (drop the field entirely if user declined to rate) |
| `{{MOOD_SHORT}}` | One-word or short-phrase mood from Phase 4 (e.g. `frustrated-but-productive`) |
| `{{MAJORS_COMPLETED}}` / `{{MINORS_COMPLETED}}` | Phase 2 completion counts |
| `{{CRITERIA_MET_PCT}}` | Phase 2: of the completed tasks, what % met success criteria (e.g. `80%`) |
| `{{PROJECTS_TOUCHED_LIST}}` | YAML inline list of project slugs touched today, e.g. `[cranium-rework-migration, ig-change-series-v1]` |
| `{{TAGS}}` | YAML inline list of retro tags from Phase 4 (e.g. `[filming-day, focus-fragmented, win-shipped-pr]`) |
| `{{ONE_LINE_DAY_SUMMARY}}` | One-sentence overall read in the user's own voice if they gave one, else a neutral one-liner |
| `{{MAJORS_GRADED_BLOCK}}` | One bullet per major: `- <title> · <done\|partial\|skipped> · criteria <met\|not-met> · <one-line note>` |
| `{{MINORS_GRADED_BLOCK}}` | Same format for minors |
| `{{PROJECTS_TOUCHED_BLOCK}}` | One bullet per project: `- [[<slug>]] — <what moved today>` |
| `{{JOURNAL_PROSE}}` | Phase 4 interview captured as prose, preserving user's phrasing. Multi-paragraph OK. |
| `{{COMPARISON_BLOCK}}` | Today's numbers vs 7-day rolling avg, one short line. Use `n/a — first/early retros` if no baseline. |
| `{{PATTERNS_BLOCK_OR_NONE}}` | Bulleted patterns surfaced in Phase 5, or `_None worth surfacing yet._` |
| `{{ADJUSTMENTS_LOGGED_OR_NONE}}` | Bulleted list of adjustments appended to `planning-adjustments.md`, or `_None._` |
| `{{TOMORROW_EXPERIMENT_OR_NONE}}` | If user chose a one-day experiment, restate it here so they see it in the daily note flow. Else `_None._` |
| `{{INSIGHT_CANDIDATES_OR_NONE}}` | If Phase 7 produced an insight page, link `[[../pages/<slug>]]`. Else `_None this retro._` |
| `{{PROJECT_CROSS_LINKS}}` | One `- [[../projects/<slug>]]` line per project touched |

**Delete this reference section before writing the final snapshot** — it's here for template maintainers, not for the user.
