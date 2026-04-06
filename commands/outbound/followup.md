---
name: outbound:followup
description: "Draft follow-up emails for prospects who haven't replied to a campaign. Identifies non-responders past a configurable wait period, drafts follow-up sequences with different angles, and tracks touchpoints in the master CSV. Use when the user says 'outbound followup', 'follow up', 'draft follow-ups', 'who hasn't replied', 'send reminders', 'second touch', or wants to re-engage prospects from a previous send batch."
---

# Campaign Follow-Up

Draft follow-up emails for non-responders.

## Paths

```
CAMPAIGNS_DIR=/home/jared/docs/Documents/2. Areas/2.1 Startup & Business/Riven/6. Customer Validation/Apollo Prospecting/campaigns
MASTER_CSV=/home/jared/docs/Documents/2. Areas/2.1 Startup & Business/Riven/6. Customer Validation/Apollo Prospecting/outreach_master.csv
```

## Identify Non-Responders

1. Read `prospects.csv` for the specified campaign
2. Filter to prospects where:
   - `Outreach Status` = `sent` (not replied, not bounced, not opted out)
   - `Last Touch Date` is at least 3 days ago (configurable — ask the user)
3. Report: "Found X non-responders from [last send date]. Y are past the [N]-day wait period."

## Determine Follow-Up Approach

Ask the user (or use defaults if they've set preferences):

1. **Touch number** — Is this the 2nd, 3rd, or 4th touch? Each should be progressively shorter and more direct.
2. **Angle shift** — The follow-up should NOT repeat the first email. Options:
   - **Value-add**: Share a relevant insight, article, or data point related to their pain
   - **Social proof**: Mention a similar company or result
   - **Direct question**: Short, one-question email that's easy to reply to
   - **Breakup**: Last touch — acknowledge you're not going to keep emailing, give a final reason to reply
3. **Max touches** — Default 3 total. After 3 unanswered touches, mark as `exhausted` and stop.

## Follow-Up Templates by Touch

**Touch 2 (3-5 days after initial):**
Short, reference the first email without repeating it. Add a new angle — ideally something specific that happened since the first email (new company news, industry trend).

**Touch 3 (5-7 days after touch 2):**
Very short. One question. Make it the easiest possible email to reply to. "Figured this might have gotten buried — is [pain point] something you're actively working on, or not a priority right now?"

**Touch 4 / Breakup (7+ days after touch 3):**
Acknowledge the silence. Give them an easy out. "Totally understand if the timing's off. If [pain point] becomes a priority later, happy to pick this back up."

## Draft Follow-Ups

For each non-responder:
1. Read their original enrichment data (Pain Points, Recent News, Company)
2. Check which variant they received initially
3. Draft the follow-up using the chosen angle
4. Run through `/humanizer`
5. Present 2-3 examples for approval

## After Approval

Same logging as `/outbound:send`:
1. Save drafts to `campaigns/[slug]/emails/followup_[touch_N]_[date]/`
2. Update `prospects.csv` — increment `Touch Count`, update `Last Touch Date`
3. Update master CSV
4. Update `tracking.json`
5. If touch count reaches max, set `Outreach Status` = `exhausted`

## Report

```
Follow-Up Batch: [campaign name] — Touch #[N]
===============================================
Drafted: [X] follow-ups
Angle: [value-add / social proof / direct question / breakup]

Still in sequence: [X] prospects
Exhausted (max touches): [Y] prospects
Already replied: [Z] prospects

Next: Wait [N] days, then /outbound:followup or /outbound:status to review
```

## Logging Replies

When the user tells you someone replied ("Sarah from Bloom & Wild replied", "got a response from Jake"), update:
1. `Outreach Status` = `replied` in both prospects.csv and master CSV
2. `Response` = brief note about the reply content
3. Update `campaign.json` stats

Don't wait for `/outbound:followup` to log replies — handle them whenever the user mentions them, in any `/outbound` subcommand.
