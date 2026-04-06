---
name: outbound:send
description: "Draft and prepare the next batch of outbound emails for a campaign. Picks unsent prospects, personalizes email variants using enrichment data, shows drafts for approval, and logs the send in the master CSV and campaign tracking. Use when the user says 'outbound send', 'send the next batch', 'draft emails', 'queue emails', 'send campaign', or wants to move prospects from ready to sent status."
---

# Send Campaign Batch

Draft personalized emails for the next batch of unsent prospects.

## Paths

```
CAMPAIGNS_DIR=/home/jared/docs/Documents/2. Areas/2.1 Startup & Business/Riven/6. Customer Validation/Apollo Prospecting/campaigns
MASTER_CSV=/home/jared/docs/Documents/2. Areas/2.1 Startup & Business/Riven/6. Customer Validation/Apollo Prospecting/outreach_master.csv
```

## Identify Campaign and Batch

1. If user specifies a campaign, use it. Otherwise list campaigns with `ready` or `active` status.
2. Read `prospects.csv` and filter to rows where `Outreach Status` = `ready` (not yet sent)
3. Ask how many to send this batch (default: all ready prospects, but user may want smaller batches)

## Draft Personalized Emails

For each prospect in the batch:

1. Read the email templates from `campaigns/[slug]/emails/variant_a.md` and `variant_b.md`
2. Assign the prospect to a variant (alternate A/B, or use the winning variant if enough data exists)
3. Personalize the template using the prospect's enrichment data:
   - Replace the opener with their `Personalized Opener` column
   - Reference their specific `Pain Points` or `Recent News`
   - Use their `First Name`, `Company`, `Title`
4. Run the personalized email through `/humanizer` to catch any AI patterns
5. Present the drafts to the user for review — show 2-3 examples before offering to generate the rest

## Draft Format

Present each email clearly:

```
To: [First Name] [Last Name] <[Email]>  ([Title] @ [Company])
Variant: [A/B]
Subject: [subject line]

[email body]

---
```

## After User Approval

Once the user approves the drafts:

1. **Save all drafted emails** to `campaigns/[slug]/emails/batch_[date]/` — one file per prospect
2. **Update prospects.csv:**
   - Set `Outreach Status` = `sent`
   - Set `Date First Sent` = today (if first touch)
   - Increment `Touch Count`
   - Set `Last Touch Date` = today
   - Record which variant was used
3. **Update master CSV** with the same status changes (match by email)
4. **Update campaign.json** stats
5. **Update tracking.json** with send details:
   ```json
   {
     "sends": [
       {
         "date": "2026-04-06",
         "batch_size": 10,
         "variant_split": {"A": 5, "B": 5},
         "touch_number": 1
       }
     ]
   }
   ```

## Report

```
Batch Sent: [campaign name]
=============================
Emails drafted: [X]
  Variant A: [Y]
  Variant B: [Z]
Touch #: [N]

Remaining unsent: [X] prospects
Next step: Wait 3-5 days, then /outbound:followup [campaign-slug]
```

## Important

- **The skill drafts emails, it does not actually send them.** The user copies/pastes or imports the drafts into their email tool. Make this clear.
- **Always show examples before batch-generating.** The user needs to approve the tone and personalization quality.
- **Track everything.** Every send gets logged in prospects.csv, master CSV, and tracking.json. This is what makes `/outbound:status` and `/outbound:followup` work.
