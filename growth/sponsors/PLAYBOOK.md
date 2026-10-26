# Sponsor playbook

How a SkillMaxx sponsorship goes from "Book now" to live and reported. Pricing and rules: [../SPONSORS.md](../SPONSORS.md). Pipeline: [PIPELINE.md](PIPELINE.md).

## 1. Intake
- **Now (no Stripe yet):** every "Book now" button on /advertise/ scrolls to the inquiry form with the slot preselected. Inquiries arrive at skillmaxx@gilventures.ai via formsubmit ("New Advertiser Inquiry - SkillMaxx").
  - Reply within 1 business day: confirm the slot is open, propose a start date, and (until Stripe is live) say payment link follows.
- **After Stripe:** create one Stripe Payment Link per slot, set its success URL to `https://skillmaxx.gilventures.ai/sponsor/thanks/?slot=<key>` (keys: newsletter, featured, category, bundle), and paste each URL into `src/_data/sponsorLinks.json` → `url`. The buttons then go straight to checkout. No template changes needed.
- After paying, the sponsor lands on **/sponsor/thanks/** and sends assets (name, email, company, slot, start date, link, logo file or URL, ad copy, category). They arrive as "Sponsor assets - SkillMaxx".
- Log every lead and booking in [PIPELINE.md](PIPELINE.md) and on the owner dashboard.

## 2. Scheduling
| Slot | Capacity | Unit | Starts |
|---|---|---|---|
| Newsletter sponsor | 1 per issue | weekly issue | next issue with ≥3 days lead time |
| Featured slot | 1 at a time | 30 days | any day after assets approved |
| Category sponsor | 1 per category | 30 days | any day after assets approved |
| Founding bundle | counts against all three | 30 days | same day for all parts |

- Founding pricing: first 10 sponsors, rate locked for 6 months. Count them here: **0 / 10**.
- If a slot is taken, offer the next open date or a different category.

## 3. Ad formats and specs
| Format | Copy | Image | Link |
|---|---|---|---|
| Newsletter blurb | ≤ 50 words, plain text, 1 bold product name | optional logo, square SVG/PNG ≥ 256 px | 1 URL (UTM: `?utm_source=skillmaxx&utm_medium=newsletter`) |
| Featured card | name + 1-line pitch ≤ 90 chars | square SVG/PNG ≥ 256 px | 1 URL (`utm_medium=featured`) |
| Category sponsor | name | logo, SVG preferred, ≤ 60 KB | 1 URL (`utm_medium=category`) |

- Always labeled **"Sponsored"** / **"Sponsor"**. Never changes a test result, status or sort order.
- We can edit copy for length and tone; we send a preview before going live.
- Reject: anything misleading, claims we can't verify about our tests, adult/gambling/crypto-pump, competitors' trademarks.

## 4. Fulfillment checklist
- [ ] Payment received (Stripe email) or invoice agreed
- [ ] Assets received via /sponsor/thanks/ (or email); logo meets spec
- [ ] Copy edited to spec; UTM link added and tested
- [ ] Preview sent to sponsor, approved
- [ ] Placement shipped on a `grokbot/sponsor-<name>` branch → PR → build passes → squash-merge (site) **or** placed in the Beehiiv issue (newsletter)
- [ ] Live check on desktop + 390 px mobile; "Sponsored" label visible
- [ ] Confirmation email sent (template below); row updated in PIPELINE.md and dashboard
- [ ] Calendar note for end date; renewal email 5 days before end
- [ ] Monthly report: pageviews, clicks to their link, newsletter subscribers (real numbers only)
- [ ] Remove placement on end date unless renewed

## 5. Thank-you / receipt email template
> Stripe sends the payment receipt itself. This email confirms the booking.

**Subject:** You're booked on SkillMaxx: {slot} starting {start_date}

Hey {first_name},

Thanks for backing SkillMaxx as a founding sponsor. You locked in {slot} at ${price}/{unit} for 6 months.

Here's the plan:
- **Goes live:** {start_date}{, in issue #{n}}
- **Runs until:** {end_date}
- **Link:** {link_with_utm}

If you haven't sent your logo and copy yet, drop them here: https://skillmaxx.gilventures.ai/sponsor/thanks/?slot={key}. I'll send a preview before anything goes live.

You'll get a short report with real numbers (views, clicks, subscribers) at the end of the month, even when they're small.

Cheers,
SkillMaxx · skillmaxx@gilventures.ai
