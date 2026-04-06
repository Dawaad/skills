---
name: outbound:status
description: "Detailed status view for a specific outbound campaign. Shows prospect breakdown, email verification results, send progress, response rates, A/B variant performance, and recommended next actions. Use when the user says 'outbound status', 'campaign status', 'how is the campaign doing', 'show me [campaign name]', or wants detailed metrics on a specific campaign's progress."
---

# Campaign Status

Show detailed stats for a specific campaign.

## Paths

```
CAMPAIGNS_DIR=/home/jared/docs/Documents/2. Areas/2.1 Startup & Business/Riven/6. Customer Validation/Apollo Prospecting/campaigns
MASTER_CSV=/home/jared/docs/Documents/2. Areas/2.1 Startup & Business/Riven/6. Customer Validation/Apollo Prospecting/outreach_master.csv
```

## Identify the Campaign

If the user specifies a campaign name/slug, use it. If not, list available campaigns and ask which one.

## Read Campaign State

1. Read `campaign.json` from the campaign folder
2. Read `prospects.csv` to get current row-level data
3. Read `tracking.json` if it exists for send/response history
4. Cross-reference with the master CSV for the latest outreach status

## Present Status

```
Campaign: [name]
Created: [date]    Status: [building/ready/active/complete]
Segment: [vertical], [company size], [titles]

Pipeline
========
  Prospected:     [X]
  Enriched:       [X] / [total]
  Email Verified: [X] ok, [Y] catch-all, [Z] invalid
  Ready to Send:  [X]
  Sent:           [X]
  Replied:        [X] ([reply rate]%)
  Bounced:        [X]
  Opted Out:      [X]

A/B Performance (if sends have happened)
========================================
  Variant A: [X] sent, [Y] opened, [Z] replied ([rate]%)
  Variant B: [X] sent, [Y] opened, [Z] replied ([rate]%)
  Winner:    [A or B] by [metric]

Touchpoints
===========
  Touch 1: [X] sent, [Y] replied
  Touch 2: [X] sent, [Y] replied
  Touch 3: [X] sent, [Y] replied

Apollo Credits: [X] used this campaign

Next Action: [recommendation based on current state]
```

## Next Action Recommendations

Based on the campaign state, suggest the logical next step:

- If `building`: "Run `/outbound:enrich` to complete enrichment"
- If `ready` with 0 sent: "Run `/outbound:send` to send the first batch"
- If sent but low reply rate and touch count < 3: "Run `/outbound:followup` to draft follow-ups"
- If one A/B variant is clearly winning: "Consider sending remaining prospects with Variant [X]"
- If all prospects exhausted: "Run `/outbound:new` to add more prospects to this segment, or start a new campaign"
