# Sponsor pipeline

**Machine-readable list:** [PIPELINE.csv](PIPELINE.csv) — 185 prospects (as of 2026-11-27), status column, public contact routes only (no guessed emails).  
**Templates + weekly cadence:** [OUTREACH.md](OUTREACH.md).  
**Pricing / caps:** [../SPONSORS.md](../SPONSORS.md) · [SCALING.md](SCALING.md).  
**Playbook:** [PLAYBOOK.md](PLAYBOOK.md).

Stages: **Target → Contacted → Replied → Booked → Live → Renewed / Lost**. Other statuses used in the sheet: `declined-warm`, `opted-out`, `Bounced`, and **`Warm - inbound`** (the prospect wrote to us — daily outreach must never email these rows).

**Standing gate (updated 2026-10-27):** Brandon approved starting outreach today. Newsletter #2 still first-sends **Tue Nov 3**. Email ramp ~10/day week 1 (verified public addresses only). Contact forms can go faster. Day-1: **10 Contacted** by email. Day-2 (Oct 28): 9 email + 6 form.

Founding sponsors booked: **0 / 10**. Payment: 8 live Stripe Payment Links (`src/_data/sponsorLinks.json`). Live view: owner dashboard → Sponsors / Sales pipeline.

## Rate locks and promo commitments
Every booking gets a row here. Default founding lock = 6 months from first payment (Category / Newsletter / Bundle). **Featured = month-to-month, no long lock.**  
**Founding 12 (APPROVED 2026-10-27):** Nov 27–30 ET — **Category/Newsletter** → 12-month founding lock; **Featured** → $19 for December (normally $29), 1 slot FCFS (Stripe promo). Free Dec line not offered. No social shoutouts.

| Sponsor | Stripe customer | Slot | First paid | Rate | Locked until | Promo | Dec shoutout issue | Notes |
|---|---|---|---|---|---|---|---|---|
| 2026-11-12 | PickAPlugin | Aaron, hello@pickaplugin.com | n/a (link swap, not a paid slot) | Inbound email | Replied (swap accepted 2026-11-13) | Confirmation email not yet sent; proposed /how-we-test/ Related directories link. They link /reports/latest/. | | |

## Lead log columns + routing (Brandon, 2026-10-27)

PIPELINE.csv columns: company, who_they_are, website, contact_route (email/form/call-only/linkedin/x/inbound-email), contact_detail, status, date_contacted, outreach_sent, data_points, notes, next_follow_up.

Routing: verified public email first (never guess) → contact form → if a site only offers call bookings, find a public email → if only a phone, log `call-only` with the number and tell Brandon → else `linkedin`/`x` with the URL and tell Brandon. Call-only and LinkedIn/X leads show in the dashboard "Needs Brandon" list. `inbound-email` is for threads where the prospect wrote to us first (e.g. Autonomous / Dee, dee@autonomous.ai, 2026-11-20). The weekday outreach routine must never email `inbound-email` or `Warm - inbound` rows; only a personal in-thread reply when there is a real reason.


## Snapshot (from PIPELINE.csv, 2026-11-22 ~11:57 PM ET, dashboard refresh)

**Outbound email status:** PAUSED since Nov 20 after `sales@xata.io` hard bounce (per PR #132 bounce-pause rule); 22+ follow-ups waiting until Brandon lifts the pause. Autonomous (`Warm - inbound`, Dee) has a separate scheduled Mon 10 AM ET routine reply with the issue #4 link.

| Stage | Count |
|---|---|
| Target | 26 |
| Contacted | 101 |
| Contacted (unconfirmed) | 1 (Nango) |
| Replied | 4 (WorkOS, Kinde, Liveblocks, PickAPlugin) |
| Warm - inbound | 1 (Autonomous / Dee) |
| dm-closed | 7 |
| call-only (needs Brandon) | 2 (ActiveCampaign, LogRocket) |
| blocked-form | 2 |
| x-only (needs Brandon) | 1 (Honeycomb) |
| declined-warm | 4 (Upstash/Context7, Railway, Better Stack, AssemblyAI) |
| Bounced | 4 (Rigour Labs, Braintrust, Doppler, Xata) |
| opted-out | 1 (FusionAuth) |
| Booked / Live / Lost | 0 / 0 / 0 |

Founding sponsors booked: **0 / 10**. Stripe checked Nov 22 ~11:57 PM ET (Gil Ventures LLC live): 0 charges, 0 Checkout sessions, 0 subscriptions. Beehiiv: 5 active subs, all test/Brandon addresses; issue #4 live on `/newsletter/issue-4/`, emails still held.

### Previous snapshot (from PIPELINE.csv, 2026-11-16 ~10:20 AM ET, weekly pipeline re-run)

This run did **not** send email, forms, or Bluesky notes. The 11 AM daily outreach routine is the only sender today.

| Stage | Count |
|---|---|
| Target | 37 (12 previously uncontacted + **25 new**, verified live 2026-11-16; Zed dropped) |
| Contacted | 95 (8 follow-ups already sent this morning by a running queue were logged, not sent by this run) |
| Contacted (unconfirmed) | 1 (Nango) |
| Replied | 3 (WorkOS; Liveblocks SDR onboarding, not a sponsorship answer; PickAPlugin link swap accepted, site link not added yet) |
| dm-closed | 7 |
| call-only (needs Brandon) | 2 |
| blocked-form | 2 |
| x-only (needs Brandon) | 1 |
| declined-warm | 3 |
| Bounced | 2 (Braintrust, Doppler) |
| Booked | 0 |
| Live | 0 |
| Lost | 0 |

Founding sponsors booked: **0 / 10**. Stripe last checked Sun Nov 15 ~6:15 PM ET (Gil Ventures LLC live): 0 charges, 0 Checkout sessions, 0 subscriptions. Beehiiv: 5 active subs, all test/Brandon addresses; no issues emailed yet. Due list: [../outreach/due-2026-11-16.md](../outreach/due-2026-11-16.md).

New Targets (public routes verified on the live page, 2026-11-16): Typesense, Cerebras, Dify, Flowise, Fern, Zuplo, Diffbot, Oxylabs, Scrapfly, Zenrows, Patronus AI, Cursor (customer-service inbox, low odds), Strapi, Lightning AI, Voyage AI, Cognee, Bruno, Apidog, Cerbos (partner-programme form; press email not used), Teleport, Namespace, Northflank, Dagger, BrowserStack, QA Wolf. Recommended slot for almost all is Newsletter $19 — the site has no Search or Scraping category.

#### Earlier snapshot (2026-11-02 ~9:15 AM ET, weekly pipeline run)

| Stage | Count |
|---|---|
| Target | 47 (Nimble + Carbone carried over; **45 new** added Nov 2: 38 email + 7 form, best fit first) |
| Contacted | 66 |
| Form-scheduled | 2 (Vercel + CockroachDB, 10:30 AM ET today) |
| Replied | 1 (WorkOS, nudge due 2026-11-05) |
| dm-closed (X DMs closed; LinkedIn-note route) | 7 |
| Call-only (needs Brandon) | 2 |
| X-only (needs Brandon) | 1 |
| Declined-warm | 1 (Upstash/Context7, check back 2027-01-26) |
| Booked | 0 |
| Live | 0 |
| Lost | 0 |

Before this run: 82 rows (Target 2). Stripe live (Gil Ventures LLC, read-only) since Oct 26: 0 charges, 0 Checkout sessions, 0 subscriptions → no bookings. Beehiiv: 5 active subs (outreach gate was 25); issue #2 still DRAFT for Tue Nov 3.
Next follow-ups: Oct 27 batch 2026-11-03 · Oct 28 batch 2026-11-04 · WorkOS nudge 2026-11-05 · X DMs 2026-11-08.

### Previous snapshot (2026-10-28 11:50 AM ET)
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
| 2026-11-12 | PickAPlugin | Aaron, hello@pickaplugin.com | n/a (link swap) | Inbound email | Replied | Swap accepted 2026-11-13; confirmation not yet sent; /how-we-test/ link not added yet. |
