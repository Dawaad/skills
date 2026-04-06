---
name: outbound:new
description: "Create a new outbound campaign and run the full prospect-to-ready pipeline. Interviews the user for ICP filters, searches Apollo for matching contacts, enriches with pain points and personalization, verifies emails via MillionVerifier, appends to the master CSV, and drafts A/B email variants. Use when the user says 'new campaign', 'start a campaign', 'outbound new', 'create outbound campaign', 'build a new list', 'new prospect batch', or wants to go from zero to send-ready for a specific segment."
---

# Create New Outbound Campaign

End-to-end pipeline: define campaign > search Apollo > enrich > verify > draft emails > ready to send.

## Paths

```
CAMPAIGNS_DIR=/home/jared/docs/Documents/2. Areas/2.1 Startup & Business/Riven/6. Customer Validation/Apollo Prospecting/campaigns
MASTER_CSV=/home/jared/docs/Documents/2. Areas/2.1 Startup & Business/Riven/6. Customer Validation/Apollo Prospecting/outreach_master.csv
VAULT_DIR=/home/jared/docs/Documents/2. Areas/2.1 Startup & Business/Riven/6. Customer Validation/Apollo Prospecting
```

## Phase 1: Campaign Definition

Interview the user to define the campaign. Be conversational — this shouldn't feel like a form.

**Gather:**
1. **Campaign name** — Short, descriptive. Will become the folder slug. (e.g., "DTC Cookware Q2", "B2C SaaS Apr Batch")
2. **Target segment** — Who are we going after? Vertical, company size, revenue range, geography, tech stack signals.
3. **Buyer persona** — Job titles, seniority levels, departments. Who feels the pain?
4. **Batch size** — How many prospects? Default 10-15 companies, 1-2 contacts each.
5. **Enrichment columns** — What do they want researched beyond the basics? Pain points, hiring signals, tech stack, recent news, personalized openers? Use defaults from the `/enrich` skill if they don't have strong preferences.
6. **Email approach** — Do they want A/B variants? How many? What angles? Reference the `/cold-email` skill for structure.
7. **Apollo credit budget** — Check current credit usage from the Batch Log. Confirm how many credits this campaign will consume.

After gathering, create the campaign folder and save config:

```
campaigns/[campaign-slug]/
├── campaign.json        # Campaign config and metadata
├── prospects.csv        # The working prospect list
├── emails/              # Drafted email variants
│   ├── variant_a.md
│   └── variant_b.md
└── tracking.json        # Send/response tracking state
```

**campaign.json structure:**
```json
{
  "name": "DTC Cookware Q2",
  "slug": "dtc-cookware-q2",
  "created": "2026-04-06",
  "status": "building",
  "segment": {
    "vertical": "DTC e-commerce",
    "company_size": "50-500",
    "revenue_range": "$1M-$20M",
    "tech_stack": ["shopify", "klaviyo"],
    "titles": ["Director of Marketing", "VP of Operations", "Head of Growth"],
    "seniorities": ["director", "vp", "manager"],
    "geography": "US, UK, AU"
  },
  "batch_size": 15,
  "enrichment_columns": ["Pain Points", "Recent News", "Tech Stack", "Hiring Signals", "Personalized Opener"],
  "email_variants": 2,
  "apollo_credits_used": 0,
  "stats": {
    "total_prospects": 0,
    "enriched": 0,
    "verified": 0,
    "ready": 0,
    "sent": 0,
    "replied": 0,
    "bounced": 0
  }
}
```

## Phase 2: Apollo Search

Search for matching prospects using `apollo_mixed_people_api_search`. Search by **person** with company filters — this is more efficient than company-first.

**Process:**
1. Build the Apollo search query from the campaign segment definition
2. Run the search (free, no credits) with `per_page: 50` to get a good pool
3. Deduplicate against:
   - The master CSV (by email)
   - Existing company files in the vault (by company name)
   - Other campaigns' prospect lists
4. Group results by company, pick 1-2 best contacts per company based on:
   - Title/seniority fit for the buyer persona
   - `has_email: true`
   - Stack depth (more ICP tools = stronger signal)
5. Present the shortlist to the user for approval before spending credits
6. Enrich approved companies via `apollo_organizations_bulk_enrich` (10 at a time, 1 credit each)
7. Enrich approved contacts via `apollo_people_match` (1 credit each)
8. Export enriched data to `campaigns/[slug]/prospects.csv`
9. Update `campaign.json` stats and `apollo_credits_used`
10. Append to the vault Batch Log with credit usage

## Phase 3: Enrichment

Run the `/enrich` skill workflow on `prospects.csv`:

1. The enrichment columns were already defined in Phase 1 — skip the interview, go straight to the enrichment plan confirmation
2. Use the waterfall research strategy from `/enrich` (existing data > Apollo > web search > company websites)
3. Run web research in parallel across the prospect batch
4. Run `/humanizer` on all sentence-style outputs (pain points, openers)
5. Add the Resources column with source attribution
6. Write enriched data back to `prospects.csv`
7. Update `campaign.json` stats

## Phase 4: Email Verification

Run the MillionVerifier verification script:

```bash
python /home/jared/.claude/commands/enrich/scripts/verify_emails.py campaigns/[slug]/prospects.csv --email-column "Email"
```

If `MILLIONVERIFIER_API_KEY` is not set, tell the user and offer to proceed without verification (flag all emails as `unverified` instead).

After verification:
1. Report results (ok/catch_all/unknown/invalid breakdown)
2. Flag invalid/disposable rows — suggest removing them
3. Update `campaign.json` stats with verified counts

## Phase 5: Master CSV Append

Append verified, enriched prospects to the master outreach CSV:

1. Read the master CSV (create it with headers if it doesn't exist)
2. Deduplicate by email — skip any already in master
3. Set auto fields:
   - `Date Added` = today
   - `Batch ID` = campaign slug
   - `Outreach Status` = `ready` (if ok/catch_all), `hold` (if unknown), `invalid` (if invalid/disposable)
   - `Touch Count` = 0
4. Append rows
5. Report: "Added X to master CSV. Y skipped (duplicates). Master total: Z."

## Phase 6: Email Drafting

Draft A/B email variants using the `/cold-email` skill's approach:

1. Read the campaign's enrichment data — particularly Pain Points, Recent News, and Personalized Opener
2. Draft email variants based on the user's requested approach:
   - **Variant A**: Lead with a specific company observation (from Recent News + Pain Points)
   - **Variant B**: Lead with a question about their operational challenge
3. Each email should:
   - Use the Personalized Opener as the first line (already humanized)
   - Be 4-6 sentences total
   - End with a low-friction CTA (quick question, not "book a call")
   - Run through `/humanizer` before saving
4. Save to `campaigns/[slug]/emails/variant_a.md` and `variant_b.md`
5. Show the user both variants for approval
6. Assign prospects to variants (A/B split — alternate or random)

## Phase 7: Ready

Update `campaign.json` status to `ready`. Present the final summary:

```
Campaign Ready: [name]
========================
Prospects:    [X] total ([Y] ready, [Z] on hold)
Email Status: [X] verified, [Y] catch-all, [Z] unknown
Variants:     [A] and [B] drafted
Credits used: [X] Apollo

Next step: /outbound:send [campaign-slug]
```

## Important Notes

- **Always confirm credit spend before enriching.** Present the shortlist and credit estimate first.
- **Never skip MillionVerifier.** Even Apollo "verified" emails bounce. The verification step protects sender reputation.
- **The master CSV is the source of truth** for cross-campaign deduplication. Always check it before adding new prospects.
- **Each campaign is self-contained** in its folder but contributes to the master CSV. This lets you run multiple campaigns in parallel without conflicts.
