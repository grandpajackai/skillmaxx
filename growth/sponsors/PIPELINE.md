# Sponsor pipeline

**Machine-readable list:** [PIPELINE.csv](PIPELINE.csv) — 40 prospects, status column, public contact routes only (no guessed emails).  
**Templates + weekly cadence:** [OUTREACH.md](OUTREACH.md).  
**Pricing / caps:** [../SPONSORS.md](../SPONSORS.md) · [SCALING.md](SCALING.md).  
**Playbook:** [PLAYBOOK.md](PLAYBOOK.md).

Stages: **Target → Contacted → Replied → Booked → Live → Renewed / Lost**.

**Standing gate (updated 2026-10-27):** Brandon approved starting outreach today. Newsletter #2 still first-sends **Tue Nov 3**. Email ramp ~10/day week 1 (verified public addresses only). Contact forms can go faster. Day-1: **10 Contacted** by email. Day-2 (Oct 28): 9 email + 6 form.

Founding sponsors booked: **0 / 10**. Payment: 8 live Stripe Payment Links (`src/_data/sponsorLinks.json`). Live view: owner dashboard → Sponsors / Sales pipeline.

## Rate locks and promo commitments
Every booking gets a row here. Default founding lock = 6 months from first payment (Category / Newsletter / Bundle). **Featured = month-to-month, no long lock.**  
**Founding 12 (APPROVED 2026-10-27):** Nov 27–30 ET — **Category/Newsletter** → 12-month founding lock; **Featured** → $19 for December (normally $29), 1 slot FCFS (Stripe promo). Free Dec line not offered. No social shoutouts.

| Sponsor | Stripe customer | Slot | First paid | Rate | Locked until | Promo | Dec shoutout issue | Notes |
|---|---|---|---|---|---|---|---|---|
| _(none yet)_ | | | | | | | | |

## Lead log columns + routing (Brandon, 2026-10-27)

PIPELINE.csv columns: company, who_they_are, website, contact_route (email/form/call-only/linkedin/x), contact_detail, status, date_contacted, outreach_sent, data_points, notes, next_follow_up.

Routing: verified public email first (never guess) → contact form → if a site only offers call bookings, find a public email → if only a phone, log `call-only` with the number and tell Brandon → else `linkedin`/`x` with the URL and tell Brandon. Call-only and LinkedIn/X leads show in the dashboard "Needs Brandon" list.

## Snapshot (from PIPELINE.csv, 2026-10-28 11:50 AM ET)

| Stage | Count |
|---|---|
| Target | 4 (Vercel + Snyk blocked by form fields; Hugging Face + Cloudflare deferred to Oct 29) |
| Contacted | 34 (21 email, 13 form) |
| Call-only (needs Brandon) | 1 (ActiveCampaign, Sales +1 (800) 357-0402) |
| Replied | 0 (no human replies yet; Supabase auto-ack only) |
| Declined-warm | 1 (Upstash/Context7, check back 2027-01-26) |
| Booked | 0 |
| Live | 0 |
| Lost | 0 |

Oct 28 run: 9 emails (E2B sent 11:14 AM ET; 8 more spaced through the afternoon by the background sender, check growth/outreach/sent/2026-10-28-email-results.json) + 6 forms (Qodo, Together AI, Pinecone, PlanetScale, Figma, Notion). Rows marked Contacted for the 8 scheduled emails assume the sender finishes; if it stops on an SMTP error, flip the unsent ones back to Target. Follow-ups for the Oct 28 batch: 2026-11-04, then 2026-11-11 (final).

**Top 10 (warmest — most are already in our directory):** Exa, Firecrawl, Upstash/Context7, Tavily, Composio, Browser Use, Neon, Supabase, CodeRabbit, Sentry. Full ranking + contact routes in the CSV.

## Inbound leads
| Date | Company | Contact | Slot | Source | Stage | Notes |
|---|---|---|---|---|---|---|
| _(none yet)_ | | | | | | |
