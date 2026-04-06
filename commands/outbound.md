---
name: outbound
description: "Outbound campaign orchestrator — the single entry point for managing cold outreach campaigns end-to-end. Shows a dashboard of all active campaigns with prospect counts, pipeline stage breakdowns, and next actions. Use this skill whenever the user says 'outbound', 'show my campaigns', 'campaign status', 'outreach dashboard', 'what's the state of outbound', or wants an overview of their prospecting pipeline. Also trigger when the user mentions outbound in a general way without specifying a subcommand — this dashboard routes them to the right one."
---

# Outbound Campaign Dashboard

Show an overview of all campaigns and route the user to the right subcommand.

## Campaign Directory

All campaigns live in:
```
/home/jared/docs/Documents/2. Areas/2.1 Startup & Business/Riven/6. Customer Validation/Apollo Prospecting/campaigns/
```

The master outreach CSV (aggregates all campaigns) lives at:
```
/home/jared/docs/Documents/2. Areas/2.1 Startup & Business/Riven/6. Customer Validation/Apollo Prospecting/outreach_master.csv
```

## What to Show

1. **Read the campaigns directory.** Each subdirectory is a campaign. Inside each, read `campaign.json` for metadata.

2. **Read the master CSV** to get aggregate stats.

3. **Present the dashboard:**

```
Outbound Dashboard
==================

Active Campaigns:
  [campaign-name]  |  [X] prospects  |  [Y] sent  |  [Z] replied  |  Created [date]
  [campaign-name]  |  [X] prospects  |  [Y] sent  |  [Z] replied  |  Created [date]

Master Pipeline:
  Total prospects:  [X]
  Ready to send:    [X]
  Sent (awaiting):  [X]
  Replied:          [X]
  Bounced/Invalid:  [X]

Commands:
  /outbound:new       Create a new campaign
  /outbound:status    Detailed view of a specific campaign
  /outbound:enrich    Re-enrich a campaign with new columns
  /outbound:send      Draft and queue next email batch
  /outbound:followup  Draft follow-ups for non-responders
```

If no campaigns exist yet, show a welcome message and suggest `/outbound:new`.

If the user seems to want a specific action (e.g., "outbound — send the next batch"), route them to the appropriate subcommand rather than just showing the dashboard.
