# Sponsor inventory, rotation and scaling (2026-10-26)

## What sponsorship looks like today
| Slot | Price (founding) | Where it shows | How many fit today |
|---|---|---|---|
| Newsletter sponsor | **$19 for 1 issue** · **$59/mo for 4 issues** (~$15 each, save $17) | One ~50-word block + 1 link, labeled "Sponsor", in SkillMaxx Weekly (Tuesdays) | **1 per issue** → 4–5 per month |
| Featured slot | **$29 for 1 month** · **$25/mo** sub | The one "Sponsored" card in the homepage Featured row (position 3) + top-of-category placement | **1 at a time** |
| Category sponsor | **$15 for 1 month** · **$13/mo** sub | Logo + link on one category page | **1 per category** (exclusive) |
| Founding bundle | **$49 for 1 month** (1 NL issue + Featured + Category, worth $63) · **$42/mo** same mix | All three for that month + "Founding Sponsor" credit on /advertise/ | consumes 1 featured + 1 category + 1 newsletter issue |

**Founding price, locked for 6 months** (first 10 sponsors). No struck-through regular prices on the site. (BFCM "Founding 12" is drafted, **not approved**; free Dec newsletter line **undecided**. See capacity forecast below.)
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

## Sponsor capacity forecast (2026-10-27, draft — no demand invented)

Honest baseline: **0 founding sponsors booked.** We have no traffic or sell-through history, so the scenarios below are **inventory math only**, not a sales forecast.

### Slots per month (current rules)
| Slot | Per month | Per 12 months | Notes |
|---|---|---|---|
| Newsletter | **~4** (1 per weekly issue) | ~48 issue-slots | The **$59/mo** product is “all 4 issues that month” → **one** such sub consumes **100%** of newsletter inventory every month it is active |
| Featured | **1** | 12 | Single homepage Featured Sponsored card (+ top-of-category). Hard scarce. |
| Category | **~30** (1 per category page; site has 30 categories today) | ~360 | Many categories are tiny (1–3 skills). Theoretical max ≠ sellable max; without traffic we cannot say how many are worth buying |
| Bundle | consumes 1 Featured + 1 Category + **1** newsletter issue that month | — | Does not buy the other ~3 newsletter issues |

One-time purchases fill a single month (or a single issue). **Monthly subscriptions** hold the slot until cancel; a rate **lock** (6 or 12 months) means we honour founding price for that term even if list prices rise later — and while the sub is active the slot stays taken.

### What a lock ties up (scenarios, not predictions)

Assume locks apply only while the subscription is active; one-time buys are not “12-month inventory holds.”

| Scenario | What is locked | Featured left for newcomers (of 1) | Newsletter left | Category left (of ~30) |
|---|---|---|---|---|
| A. No BFCM / no founding yet | nothing | 1 | ~4/mo | ~30 |
| B. One Featured Founding-12 monthly | Featured for up to 12 mo at founding $25/mo | **0** | ~4/mo | ~30 |
| C. One Newsletter $59/mo Founding-12 | All 4 issues/mo for up to 12 mo | 1 | **0** | ~30 |
| D. One Bundle $42/mo Founding-12 | Featured + 1 cat + 1 NL issue/mo for up to 12 mo | **0** | ~3/mo | ~29 |
| E. Fill all **10** founding seats with Category monthly only | up to 10 categories for 6 or 12 mo | 1 | ~4/mo | ≥20 |
| F. Worst mix for flexibility: 1× Featured-12 + 1× NL-4pack-12 + 8× Category-12 | Featured + all NL + 8 cats | **0** | **0** | ~22 |

**Read of the table:** Featured and the newsletter 4-pack are the foot-guns. Giving either a 12-month founding lock can zero that whole channel for a year at the lowest price. Categories have headroom even with a founding cap of 10.

Default **6-month** founding lock on all 10 seats is already a commitment; extending **every** product to 12 months multiplies the scarce-slot problem.

### Inventory left for new / later-rate sponsors
- After founding seats fill, newcomers pay whatever post-founding rates we set (not shown as fake “was” prices today).
- If Featured is on a 12-month founding sub, **there is no Featured inventory** for a higher rate until that sub ends or we raise the Featured cap (SCALING proposal: up to 3 cards — not built, needs yes).
- If newsletter 4-pack is locked 12 months, **there is no newsletter inventory** for issue-by-issue or a second pack buyer.
- Categories: even with 10 founding category locks, ~20 category pages remain — enough room if demand appears.

### Recommendation (draft for Brandon)
1. **Keep total founding cap = 10** (people/companies, not “10 of each slot”).
2. **12-month lock only for monthly subscriptions**, never for one-time checkouts.
3. **Eligible for Founding 12 (recommended):** Featured monthly ($25/mo) **cap 1**; Category monthly ($13/mo) **cap ≤5** of the 10 founding seats; Bundle monthly ($42/mo) **cap 1** (because it eats Featured).
4. **Not eligible for 12-month lock:** Newsletter $59/mo 4-pack (consumes all NL inventory); one-time $19/$29/$15/$49. Those stay at the normal **6-month** founding lock if they count as founding seats, or one-time with no lock length beyond the paid period.
5. **Free December newsletter line:** **undecided** — revisit after caps above are approved; do not put it on the banner yet.
6. **No BFCM social shoutouts** in the offer; shoutouts later only if paid or separately approved.
7. Until this forecast is approved, **do not finalize Founding 12** or merge PR #35.

### Open questions for Brandon
- Accept the eligibility caps in (3)–(4)?
- Raise Featured inventory later (2–3 cards) so a Founding-12 Featured buyer does not zero the channel?
- Free December line: yes / no / only for certain products?

