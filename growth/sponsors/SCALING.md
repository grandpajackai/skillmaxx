# Sponsor inventory, rotation and scaling (2026-10-26)

## What sponsorship looks like today
| Slot | Price (founding) | Where it shows | How many fit today |
|---|---|---|---|
| Newsletter sponsor | **$19 for 1 issue** · **$59/mo for 4 issues** (~$15 each, save $17) | One ~50-word block + 1 link, labeled "Sponsor", in SkillMaxx Weekly (Tuesdays) | **1 per issue** → 4–5 per month |
| Featured slot | **$29 for 1 month** · **$25/mo** sub | The one "Sponsored" card in the homepage Featured row (position 3) + top-of-category placement | **1 at a time** |
| Category sponsor | **$15 for 1 month** · **$13/mo** sub | Logo + link on one category page | **1 per category** (exclusive) |
| Founding bundle | **$49 for 1 month** (1 NL issue + Featured + Category, worth $63) · **$42/mo** same mix | All three for that month + "Founding Sponsor" credit on /advertise/ | consumes 1 featured + 1 category + 1 newsletter issue |

**Founding price, locked for 6 months** (first 10 sponsors). No struck-through regular prices on the site. (BFCM "Founding 12" drafted, **not approved** — see simplified model + capacity below. Free Dec line **undecided**.)
Rules that never change: always labeled "Sponsored", money never changes a test result or ranking.

**Gap found:** the homepage card is a static "Your skill here" placeholder, and category pages do not render a sponsor block yet. Before the first booking we need a `src/_data/sponsors.json` (who, slot, category, start/end, creative) that the homepage Featured card, category pages and /advertise/ credits read from. Fulfilment is manual until then (edit + PR within 24 h of payment).

So true capacity right now is about **1 featured + N categories + ~4 newsletter slots a month**. If 100 sponsors paid tomorrow, roughly 85+ would have nowhere to go.

## What others do
- **TLDR** (8M readers): max 3 sponsors per issue in fixed tiers (Primary top 100 words/logo, Secondary 50 words, Quick Links 30 words) plus a full-issue takeover. Scarcity is the product; you book dates in advance.
- **There's An AI For That**: 1 Main Sponsor per daily issue; directory sells "highlighted" listings that stay on the front page while paid, and a pay-per-click "Featured" section (bid-based, capped by budget).
- **Carbon Ads / EthicalAds** (dev sites): 1 ad per page view, rotated across many advertisers by impression share; pricing per 1,000 impressions; sold out → waitlist.
- **daily.dev, Product Hunt, Hacker Newsletter, Console.dev**: fixed weekly slots booked on a calendar, "sold out until <date>", waitlist form; category/keyword exclusivity is a premium.
Pattern: **fixed scarce inventory + calendar booking + waitlist**, with rotation only for low-tier, high-volume placements.

## Recommendation for SkillMaxx (fair at 10, 100 or more)
1. **Publish inventory and caps.** Newsletter: max 2 per issue (Primary + a 30-word Quick Link) once we pass 100 subscribers; 1 until then. Homepage Featured: up to 3 sponsored cards (1 per row), never more than 1 in 4 cards. Category: 1 exclusive sponsor per category. Show "X of Y left this month" on /advertise/.
2. **Calendar booking, first paid first served.** Slots are dated (week/month). A payment for a full slot goes to the next open date, told in the thank-you email. Stripe sub renewals keep their slot (renewal priority) as long as they stay active.
3. **Waitlist when sold out.** The Pay buttons turn into "Join waitlist" (same FormSubmit form, slot preselected). Waitlist is FIFO; next opening offered for 48 h.
4. **Rotation only for a cheap "Spotlight" tier.** If demand exceeds fixed slots, add a lower-priced Spotlight pool (e.g. $9/mo): a small labeled sponsor strip on report pages and skill pages that rotates evenly by impressions (client-side round-robin, logged), max 12 in the pool so each gets ≥ 1/12 share. Report impressions/clicks monthly.
5. **Category exclusivity is the premium.** One sponsor per category; competitors in the same category are not placed side by side in the same issue or row.
6. **Price tiers follow demand.** After the first 10 founding sponsors, set new rates for newcomers only (existing 6-month locks stay). When a slot sells out 2 months running, raise its price ~20% for new bookings. Do not show invented “was” prices on /advertise/.
7. **Fairness log.** Every placement (who, where, dates, impressions) in PIPELINE.md / sponsors.json so anyone can audit it.

## Next build steps (need Brandon's OK, $0)
- `sponsors.json` + rendering on homepage card, category pages, newsletter block, /advertise/ credits.
- Inventory counter + sold-out → waitlist switch on /advertise/.
- Spotlight tier + Stripe price only if fixed slots sell out.

## Simplified sponsor model (2026-10-27 draft — Brandon direction)

**Prices unchanged.** Live sheet on /advertise/ (founding price, locked for 6 months; no struck-through regulars).

| Rule | Detail |
|---|---|
| Founding | First **10** sponsors → founding price locked **6 months** |
| Featured | **Excluded from long locks.** Rotates monthly. Price rises as audience grows (newcomers only; existing months already paid stay). |
| BFCM Founding 12 | Nov 27–30 ET: **Category** and **Newsletter** only → founding rate locked **12 months** instead of 6 |
| Free Dec newsletter line | **Undecided** |
| Social shoutouts | Not in the BFCM offer |
| Premium / custom | “Contact us” partnership lane (draft on /advertise/ What you get) |

No per-plan seat math beyond: total founding cap **10**, Featured never gets the 12-month BFCM lock.

## Sponsor capacity forecast (simplified)

Honest baseline: **0** founding sponsors booked. No traffic history — scenarios are inventory only.

### Slots per month
| Slot | Per month | Lock behavior |
|---|---|---|
| Newsletter | ~4 issue-slots (1/issue) | One-time = one issue. $59/mo pack = all 4 that month. BFCM can lock founding rate **12 months** on Newsletter. |
| Featured | **1** | Monthly rotation. **No** 12-month BFCM lock. Price can step up for new months as audience grows. |
| Category | ~30 pages (1 each; many tiny) | BFCM can lock founding rate **12 months**. Room remains even if several founding seats are Category. |
| Bundle | Featured + Category + 1 NL issue | Featured piece follows Featured rules (no 12-mo BFCM lock on that piece). |

### Why Featured is special
One Featured card. A 12-month lock would freeze the only homepage Sponsored slot at founding price for a year and block raising the rate as traffic grows. Monthly rotation keeps inventory and pricing flexible.

### Scenarios (not demand forecasts)
| Scenario | Featured open next month? | Newsletter / Category |
|---|---|---|
| A. Nothing sold | Yes | Full |
| B. One Featured buyer this month | Next month yes (rotates); rate may be higher for the next buyer | Full |
| C. BFCM: 3 Category + 2 Newsletter 12-mo locks | Yes (Featured untouched) | Those products held at founding rate up to 12 mo; other categories / issue-slots still sellable |
| D. Fill 10 founding seats mostly Category | Yes | Many categories still free |

### Recommendation
1. Ship the simplified rules above; drop per-plan BFCM eligibility matrices.
2. Approve Featured = monthly, no long lock, rising price later.
3. Approve BFCM 12-mo lock = Category + Newsletter only.
4. Decide free December line separately.
5. Add Premium / custom “contact us” on /advertise/ (draft PR).
