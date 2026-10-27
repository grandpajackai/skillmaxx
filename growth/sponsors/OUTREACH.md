# Sponsor outreach templates + weekly cadence

**Status:** outreach started 2026-10-27 (Brandon approved start today; newsletter still first-sends Nov 3).  
**Gate (updated 2026-10-27):** Brandon OK'd outbound now. Ramp cold email ~10/day week 1 (verified public addresses only — never guess). Contact forms can go faster. Still log every send in PIPELINE.csv; follow-ups day 7 / day 14 then stop.  
**Audience honesty (say this every time):** SkillMaxx launched Oct 2026. Traffic and the list are tiny. Founding prices exist because of that. We share real numbers every month, even when they're small.  
**Source of prospects:** [PIPELINE.csv](PIPELINE.csv). Stages: Target → Contacted → Replied → Booked → Live → Renewed / Lost.

Approved model (2026-10-27): prices unchanged; founding price locked **6 months** for the first **10** sponsors; **Featured is month-to-month (no long lock)**; custom deals via contact us; BFCM Nov 27–30 (Cat/NL 12-mo lock; Featured $19 for December, 1 slot).

---

## 1. Cold email (LinkedIn-level context, plain)

**From:** skillmaxx@gilventures.ai  
**To:** their public form / published partnerships email only (never invent an address)  
**Length:** ≤150 words

**Subject options (pick one):**
- we install your {tool} every night (it {behaves|shows up a lot})
- a $19 test in front of people picking agent tools
- founding sponsor of our {category} page?

```
Hi {first_name or team},

I'm Brandon. I run SkillMaxx — a free directory that install-tests agent skills, plugins and MCP servers every night across Claude Code, Codex, Grok Build, Cursor and Pi, and publishes what installed (with logs): https://skillmaxx.gilventures.ai/reports/latest/

{One sentence why them: e.g. "Your {MCP/plugin} is already in the directory / is what people install first for {search|scraping|docs}."}

Honest ask: would you take a founding {slot} at ${price}/{unit}? Rate locked 6 months for the first 10 sponsors{; Featured is month-to-month}. Placements are always labeled Sponsored. Money never changes a test result.

We're brand new and the audience is still small — that's why it's cheap, and you'd get a monthly report with real numbers even when they're tiny.

Even a one-line "not now" or "test this config instead" helps.

Brandon
SkillMaxx · https://skillmaxx.gilventures.ai/advertise/
```

**Slot cheat sheet for the blank:**
| Slot | Price line |
|---|---|
| Newsletter | $19 for 1 issue (or $59/mo for 4) |
| Featured | $29 for 1 month / $25/mo (month-to-month, no long lock) |
| Category | $15 for 1 month / $13/mo |
| Bundle | $49 for 1 month = 1 NL issue + Featured + Category (worth $63) |

---

## 2. X / LinkedIn DM (after a real reply or useful comment — never cold spam)

```
Hey {name} — I run SkillMaxx (nightly install tests for agent skills/MCP across 5 coding agents). {One specific thing about their tool from our tests or their post}.

Tiny ask when you have a sec: we're opening founding sponsor slots ($15–$29/mo, labeled, honest numbers). Happy to send the one-pager: skillmaxx.gilventures.ai/advertise/

If sponsorship isn't useful, what's one setup of yours we should be testing that we aren't?
```

Rules: only after you've publicly engaged their content once; no pitch in the first reply ever; one DM, then stop unless they answer.

---

## 3. Follow-ups (2 steps, then stop)

### Follow-up 1 — 7 days later
**Subject:** Re: {original subject}

```
Hi again — one nudge, then I'll leave you alone.

Since my last note we published this week's install scorecard: {link to /reports/week/YYYY-WW/}.

If sponsoring isn't a fit, a one-line "not now" is genuinely helpful, and so is "test this instead".

Brandon
```

### Follow-up 2 — 14 days after first email (final)
**Subject:** Re: {original subject}

```
Last note from me on this.

Founding slots (first 10, 6-month rate lock) are still open; Featured stays month-to-month. Menu: https://skillmaxx.gilventures.ai/advertise/

If timing is wrong, I'll check back after we cross a real audience milestone rather than pinging again.

Thanks either way,
Brandon
```

After follow-up 2: set status **Lost** (or **Nurture** with next_touch = after 500 subs / BFCM week), no more outbound until a milestone.

---

## 4. Weekly cadence (autonomous; no daily work for Brandon)

**Routine intent:** every Monday ~9:00 AM America/New_York, run the sponsor pipeline check and message Brandon **only** when something needs a decision, a reply arrived, or a problem. Daily sends (email + forms) run autonomously under the ramp; still no invented addresses.

**Each Monday run does:**
1. Read `growth/sponsors/PIPELINE.csv` + Stripe (paid checkouts / active subs).
2. Count stages: Target / Contacted / Replied / Booked / Live / Lost.
3. Check Beehiiv subscriber count vs the 25-sub gate; note whether issue #2 has been sent.
4. Advance follow-ups that are due (draft only — never send). Mark Contacted rows that hit day 7 / day 14.
5. Advance the next Target rows: send verified-email cold notes (ramp) and queue contact-form submissions; archive copies under `growth/outreach/sent/`.
6. If any Stripe payment arrived: log in PIPELINE.md bookings table, start PLAYBOOK fulfillment, ping Brandon.
7. Refresh the Sales pipeline section on the owner dashboard Page.
8. **Delivery:** Brandon in this chat. If nothing moved and no batch is ready: one short "pipeline quiet" line, or silence if the standing rule prefers no noise.

**BFCM overlay (Nov 24–Dec 1):** Monday runs in that window also remind Brandon which BFCM slots remain (Cat/NL 12-mo; Featured Dec $19 one slot) and whether any warm Replied leads should get the BFCM heads-up (only people who already replied — never cold BFCM blasts).

**Brandon's only recurring job:** reply yes/no to the weekly batch card when one appears. No daily tasks.

Runbook file for the routine: [../routines/SPONSOR-PIPELINE-WEEKLY.md](../routines/SPONSOR-PIPELINE-WEEKLY.md).

---

## 5. Inbound improvements on /advertise/ (PROPOSED — not shipped)

Do not build until Brandon says yes. Keep $0 and honest.

1. **Audience stats line (honest):** under the media kit / What you get, one line pulled from build-time data only, e.g. "Directory: {N} add-ons · last night {pass}/{judgeable} installs clean · newsletter: just starting (we'll publish the subscriber count here once it's not embarrassing)." Never invent traffic.
2. **"Sponsors from" proof slot:** empty state until first Live booking — then logos of founding sponsors with link to their site. Same component later powers the Founding Sponsor credit.
3. **Inventory counter:** "Featured: 1 of 1 open this month · Newsletter: next open Tuesday · Category: {open} of ~30 pages." Sold-out → "Join waitlist" (FormSubmit, slot preselected) — already sketched in SCALING.md.
4. **Public booking calendar (later):** dated week/month slots once demand exists; not needed at 0 bookings.
5. **BFCM note:** already date-gated on the page (#50). No extra promo chrome.

---

## 6. First outreach batch (SENT 2026-10-27 — day-1 email)

Propose when gate opens. Top of PIPELINE.csv:

| # | Company | Slot | Route |
|---|---|---|---|
| 1 | Exa | Category: Search $15/mo | https://exa.ai/partners |
| 2 | Firecrawl | Bundle $49 | affiliates / partner program |
| 3 | Upstash / Context7 | Featured $29/mo | https://context7.com/contact |
| 4 | Tavily | Newsletter $19 | https://www.tavily.com/partnerships |
| 5 | Composio | Category: Integrations | https://composio.dev/partnerships |
| 6 | Browser Use | Featured | sales page or X @browser_use after engagement |
| 7 | Neon | Category: Databases | https://neon.com/contact-sales |
| 8 | CodeRabbit | Featured | https://www.coderabbit.ai/contact-us |

Personalized drafts already exist for 1–5 in `growth/outreach/01`–`05` (refresh numbers from latest `/reports/` before send; Featured copy must say **month-to-month**, not 6-month lock).


### Day-1 email sent (2026-10-27 ET)
From `skillmaxx@gilventures.ai` via Zoho SMTP. SPF + DKIM `zmail._domainkey` verified before send. Plain text, no tracking. Archive: [sent/2026-10-27-batch1.json](../outreach/sent/2026-10-27-batch1.json).

| Company | To | Source |
|---|---|---|
| Exa | partnerships@exa.ai | https://exa.ai/partners |
| Firecrawl | partnerships@firecrawl.dev | https://www.firecrawl.dev/firecrawl-for-platforms/partner-program |
| Upstash / Context7 | context7@upstash.com | https://context7.com/contact |
| Composio | partnerships@composio.dev | https://composio.dev/partnerships |
| Browser Use | sales@browser-use.com | https://browser-use.com/enterprise |
| CodeRabbit | hello@coderabbit.ai | CodeRabbit KB (Marketing & Partnerships) |
| Apify | partners@apify.com | https://apify.com/partners/join |
| Axiom | partners@axiom.co | https://axiom.co/partner-program |
| Semgrep | partnerships@semgrep.com | https://docs.semgrep.dev/licensing |
| Parallel AI | partnerships@parallel.ai | https://docs.parallel.ai/resources/faqs |

Form queue (not submitted in this PR): [sent/2026-10-27-form-targets.md](../outreach/sent/2026-10-27-form-targets.md).
