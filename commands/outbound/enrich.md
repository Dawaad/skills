---
name: outbound:enrich
description: "Re-run or extend enrichment on an existing outbound campaign. Use when the user wants to add new columns to a campaign's prospect list, re-enrich rows that had fallbacks, or run enrichment on newly added prospects. Triggers on 'outbound enrich', 're-enrich', 'add columns to campaign', 'enrich the campaign list', or when the user wants to improve the data quality of an existing campaign before sending."
---

# Re-Enrich Campaign

Run additional enrichment on an existing campaign's prospect list.

## Paths

```
CAMPAIGNS_DIR=/home/jared/docs/Documents/2. Areas/2.1 Startup & Business/Riven/6. Customer Validation/Apollo Prospecting/campaigns
```

## Identify the Campaign

If the user specifies a campaign name/slug, use it. If not, list campaigns and ask.

## Determine What Needs Enrichment

Read `campaigns/[slug]/prospects.csv` and `campaign.json`. Present what's already there and ask what the user wants:

1. **New columns** — User wants to add columns that don't exist yet (e.g., "add Hiring Signals and Tech Stack")
2. **Re-enrich fallbacks** — Rows where enrichment previously returned "Not Found" or fallback values
3. **Refresh stale data** — Re-research rows where the data might be outdated (e.g., "Recent News" from 3 months ago)
4. **Enrich new rows** — If new prospects were manually added to the CSV since the last enrichment run

## Run Enrichment

Follow the `/enrich` skill workflow, but scoped to the campaign's `prospects.csv`:

1. Skip the full interview if columns are already defined in `campaign.json` — just confirm the new columns or changes
2. Only research rows/columns that actually need work (don't re-research already-filled cells unless the user asks)
3. Run `/humanizer` on any new sentence-style outputs
4. Update the Resources column with any new sources
5. Write back to `prospects.csv`
6. Update `campaign.json` with revised enrichment stats

## Sync to Master CSV

After enrichment, update the corresponding rows in the master CSV with any new or changed data. Match on email address.

Report what changed: "Updated X rows in master CSV with new [column names]."
