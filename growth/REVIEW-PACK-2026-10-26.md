# SkillMaxx review pack — 2026-10-26

Everything here is a **draft for Brandon's approval**. Nothing was queued in Buffer, posted, emailed or sent. Approve, critique or kill each item; I'll apply edits and only then queue/post.

## What changed today
- **Fixed + merged (PR #24):** /sponsor/thanks/ asset form now only says "Assets received" when FormSubmit's AJAX endpoint confirms success (it used to show success on any 200, including the "please activate" page). File upload removed because the AJAX endpoint can't take files; sponsors give a logo URL or reply to their receipt with the file.
- **Draft PR #25 (NOT merged, needs review):** new guide /guides/flaky-vs-broken/, "Is this guide useful?" feedback box on both guides, footer links, DRAFT privacy + terms pages.
- **New docs:** growth/VOICE.md, growth/social/{SCHEDULE,PINNED,POST-BANK}.md, growth/newsletter/issue-002-beehiiv.md, growth/sponsors/{TARGETS-RANKED,BFCM}.md, outreach 01–06, growth/reddit/POSTS.md, growth/profiles/ (PROFILES.md + banner/cover/chart PNGs).

## Readiness check (read-only, nothing touched)
| Item | Status |
|---|---|
| Site | ✅ home, /reports/latest/, /reports/week/2026-44/, /advertise/, guides all 200 |
| Stripe Payment Links (8) + customer portal | ✅ all return 200; not modified |
| /sponsor/thanks/ false success | ✅ fixed (PR #24) |
| /advertise/ inquiry form | ✅ already AJAX-checked (PR #16) |
| FormSubmit activation | ⚠️ still unconfirmed — until the activation email is clicked, both forms show the honest error and inquiries are lost |
| Privacy / Terms | ❌ not live (404). Drafts in PR #25. Recommended before taking sponsor money at scale |
| Signup flow | ⚠️ Beehiiv subscribe page returns 403 to bots (normal). Double opt-in retest by Brandon still pending |
| Beehiiv Pro trial | ⚠️ ends ~Nov 2 — decide free vs paid |
| BFCM | ⚠️ only an idea existed → full draft offer in growth/sponsors/BFCM.md (no Stripe changes needed) |
| X avatar | ⚠️ Buffer shows X's default avatar → upload growth/profiles/avatar-400.png |
| Buffer queue | 0 posts on all 3 channels; schedules are Buffer's random defaults |

## Decisions needed (with my recommendation)
1. **Buffer schedules** → adopt the per-platform schedule in SCHEDULE.md (X 5/wk 9:30 AM, Bluesky 4/wk 12:30 PM, LinkedIn Tue+Thu). *Rec: yes.*
2. **Retire the old 35-post X bank** and use the 12-post v2 bank. *Rec: yes.*
3. **Pinned posts** (X, Bluesky, LinkedIn) — approve text; you post/pin X and LinkedIn, I can pin Bluesky via API. *Rec: approve.*
4. **Newsletter #2** — send Tue Nov 3? Was issue #1 ever emailed? If not, merge #1's best bits into #2 and make #2 the first send. *Rec: make #2 the first send.*
5. **Sponsor outreach** — start after #2 goes out and ≥25 subscribers, top 5 ranked targets, 2/week. *Rec: yes, wait for #2.*
6. **BFCM "Founding 12"** offer (12-month rate lock + free Dec newsletter line, Nov 27–30). *Rec: approve.*
7. **Reddit** — post from u/SkillMaxxHQ (low karma, may be filtered) or your personal account with disclosure? *Rec: SkillMaxxHQ, start with r/SideProject, comment for a few days first in r/mcp.*
8. **PR #25** — approve guide + privacy/terms text (I'll strip the DRAFT line and merge). *Rec: approve; legal text is a plain-English template, not lawyer-reviewed.*
9. **Bluesky profile** — let me set bio/banner via the API? *Rec: yes.*
10. **Beehiiv Pro** → drop to free before Nov 2. *Rec: free ($0 budget).*

---
<!-- source: growth/VOICE.md -->
## SkillMaxx brand voice

**One line:** a cheeky, helpful friend who happens to install every agent skill every night, run by a humble founder who's open about being early and keeps asking "is this useful?"

## The anchors (approved copy, don't drift from these)
- **X bio:** "We install agent skills & MCP servers in Claude Code, Codex, Grok, Cursor and Pi every night and post what works. Free daily report + weekly newsletter."
- **LinkedIn tagline:** "Find the skills, plugins and MCP servers that actually work with your AI agent."

## Three dials
| Dial | Where we sit | Sounds like | Never sounds like |
|---|---|---|---|
| Cheeky ↔ corporate | 70% cheeky | "Codex went 65 for 65. Show-off." | "We are excited to announce…" |
| Humble ↔ hype | 80% humble | "We're 2 weeks old, the numbers are small, tell us what's missing." | "The #1 / ultimate / definitive directory" |
| Receipts ↔ opinions | 90% receipts | "802/890 clean, 13 flaky we refused to count." | "Everyone knows X is better" |

## Rules
1. **Every claim has a receipt.** A number, a log, a link to /reports/latest/ or a skill page. Numbers come from scripts (`testing/weekly_scorecard.py`, `src/_data/reports.json`), never typed by hand.
2. **Be honest about limits.** Sandbox has no API keys; "pass" = installs and connects, not "does its job well". Flaky ≠ broken; say so.
3. **Ask, every time it's natural.** Close posts, emails and newsletters with a real question: "what should we test next?", "is this useful or noise?", "did we get your tool wrong? tell us, we'll rerun it."
4. **Founder in first person when it's a founder moment** ("I", Brandon) on LinkedIn, Reddit and the newsletter intro. **"We"** for the test bot and the site.
5. **Punch at problems, not people.** Joke about flaky installs, README promises and marketplace chaos. Never dunk on a tool author, an agent, or a competitor directory.
6. **Not salesy.** Sponsors get one line, clearly labeled. No urgency tricks, no fake scarcity; the "first 10 founding sponsors" cap is real.
7. **Plain words.** Short sentences, lowercase-friendly on X/Bluesky replies, proper case on LinkedIn, newsletter and site. One emoji max per post, zero is fine.
8. **Retired phrases:** "vibes directory", "no vibes, just logs" (reads as a dunk), "like animals", "Hi, we're the 1 person now", daily standout posts based on a single night (Qodo lesson: wait for 2 nights).

## Per-channel cheat sheet
| Channel | Register | Feedback ask |
|---|---|---|
| X | punchy, data-first, ≤280, one link | "what should we test next?" |
| Bluesky | same data, a bit warmer and nerdier, ≤300 | "reply with a repo and we'll run it" |
| LinkedIn page | proper case, founder lessons + data, 600–1,300 chars, link in post | "what would make this useful for your team?" |
| Reddit | founder, no marketing words, give value in the post itself, link last or in comments | "roast it / what's missing?" |
| Newsletter | friendly letter from Brandon, scorecard in the middle, one sponsor line | "hit reply: useful or noise?" |
| Site / blog | clear, AEO-friendly question headings, direct answers, honest limits box | "found a wrong result? tell us" |

## Before / after
- Before: "Unpopular opinion: a skill directory that hides its failures is just a vibes directory."
- After: "A directory that only shows green checks isn't helping you. Ours shows the red ✗ too, with the log. If we got yours wrong, tell us and we'll rerun it."

---
<!-- source: growth/social/SCHEDULE.md -->
## Buffer audit + recommended schedules (2026-10-26)

**Read-only audit. Nothing in Buffer was changed.**

## What Buffer has right now
| Channel | Buffer slots today (ET) | Queued posts | Notes |
|---|---|---|---|
| X @SkillMaxxAI | Mon 9:47, Tue 9:18, Wed 9:53, Thu 9:15, Fri 9:40 (none Sat/Sun) | 0 | Buffer shows the **default egg avatar**, so the X profile photo isn't uploaded yet (or Buffer hasn't refreshed). Goal 5/wk "at risk". |
| Bluesky @skillmaxx.bsky.social | Mon 18:24, Tue 21:13, Wed 21:48, Sat 17:55, Sun 20:48 (none Thu/Fri) | 0 | Buffer's random defaults; evening-heavy. |
| LinkedIn SkillMaxx AI page | Tue 22:54, Wed 17:08, Thu 15:41, Fri 14:59, Sat 8:40 | 0 | 10:54 PM Tue and 8:40 AM Sat are dead zones for a B2B page. |

Nothing is queued, sent or in error. The 35-post X bank (growth/x/posts.json) was never loaded. Ideas board only has Buffer's 2 sample cards.

## Flags on the existing 35-post X bank
- **Stale numbers everywhere:** 803/902 and per-agent numbers are from Oct 25; current is 802/890 judgeable (90.1%) and the honest-reports rules changed what counts as broken/fixed.
- **Retire:** day5-2 ("vibes directory"), day1-4 ("like animals"), day3-3 ("we're the 1 person now"), day2-5 & day5-5 ("Issue #1 is coming"/old issue tease), day1-5 (lists Qodo as an overachiever; Qodo is now flaky), day4-5 (PubMed flip-flop is now classed flaky, not a story), day6-2 (gdharness: fine to keep only as "confirmed broke 2 nights"), day4-4 & day7-1 (week-1 recap with old totals), day1-3 (the "295 rely on" claim needs a re-check).
- **Keep with fresh numbers:** install tips (day2-2, day6-1, day7-2), how we test (day4-3), agent picker (day4-1), reference servers (day4-2), submit ask (day3-5), "which skill first?" (day6-5).
- Replacement bank: growth/social/POST-BANK.md (12 posts, voice-checked).

## Recommended schedule
Daily report posts stay **off** unless a big event fires (popular tool ≥1k★ confirmed broken 2 nights, or an agent update breaks ≥3). Those go out manually, same day, after your OK.

| Channel | Posts/week | Slots (ET) | Mix |
|---|---|---|---|
| X | 5 | Mon–Fri 9:30 AM (+ Sun 6 PM weekly scorecard) | 2 install tips, 1 data post, 1 feedback ask, 1 weekly scorecard; replies daily via the sniper (manual, intent links) |
| Bluesky | 4 | Mon, Wed, Fri 12:30 PM + Sun 6:15 PM scorecard | Same posts as X, warmer wording, more "reply with a repo" asks |
| LinkedIn page | 2 | Tue 8:30 AM, Thu 12:00 PM | Tue: founder lesson + data; Thu: weekly scorecard/newsletter recap |

Change in Buffer when you approve (Settings → Posting schedule per channel). I won't touch it without a yes.

---
<!-- source: growth/social/PINNED.md -->
## Pinned posts (drafts, not posted)

## X (pin on @SkillMaxxAI)
```
We install agent skills & MCP servers in Claude Code, Codex, Grok, Cursor and Pi every night and post what actually installs.

Last night: 802 of 890 installs clean. The misses are listed too, with logs.

We're brand new. What should we test next? 👇
skillmaxx.gilventures.ai/reports/latest/
```
Image: weekly pass-rate chart (growth/profiles/pin-chart.png).

## Bluesky (pin on @skillmaxx.bsky.social)
```
hi bluesky 👋 we're SkillMaxx. every night we install agent skills, plugins & MCP servers in Claude Code, Codex, Grok Build, Cursor and Pi, in a sandbox with no API keys, and publish what works.

brand new, small, very open to feedback. reply with a repo and we'll run it through all 5.

skillmaxx.gilventures.ai
```

## LinkedIn (company page, pin as featured)
```
Why SkillMaxx exists

Every AI coding agent now has skills, plugins and MCP servers. Almost none of them tell you whether a given one installs in the agent you actually use. READMEs say "works with AI agents". That's a hope, not a test.

So every night we install them for real: 424 add-ons, 902 installs across Claude Code, Codex, Grok Build, Cursor and Pi, in fresh sandboxes with no API keys. Last night 802 of the 890 we could judge installed cleanly. The failures are published too, with logs, and we only call something broken after it fails two nights in a row.

Honest disclaimer: we launched this month and we're small. That's why I'm asking:
• What should we test next?
• Would a weekly install scorecard be useful for your team, or is it noise?

Free daily report: https://skillmaxx.gilventures.ai/reports/latest/
Weekly newsletter (Tuesdays): https://skillmaxx.gilventures.ai/newsletter/

— Brandon, founder
```

---
<!-- source: growth/social/POST-BANK.md -->
## Post bank v2 (voice-checked, numbers from 2026-10-26 run). Drafts, nothing queued.
X ≤280 / Bluesky ≤300. Same text works on both unless noted.

1. **Tip** — In Claude Code it's `/plugin install sentry@claude-plugins-official`. The @marketplace bit isn't decoration: same names now live in 2+ marketplaces and agents will ask "which one?". Pin it and move on.
2. **Tip** — Cursor MCP: add the server under mcpServers in ~/.cursor/mcp.json, then check it says "ready". Anything else means not ready. Cursor is very literal. (We grade on exactly that line.)
3. **Data** — Last night's installs by agent: Codex 65/65, Claude Code 94%, Grok Build 94%, Pi 66%, Cursor 61% (keyless). Not a ranking of agents, a ranking of how well the ecosystem ships for each one. skillmaxx.gilventures.ai/reports/latest/
4. **Honesty** — New rule: we only call an install "broken" after it fails two nights in a row. 13 add-ons flip-flopped this week. We used to shout about those. Now we label them flaky and shut up about it.
5. **Honesty** — 12 installs "failed" last night only because our sandbox has no API keys. That's not broken, that's shy. We list them separately now so nobody gets blamed for our missing keys.
6. **Feedback ask** — We're brand new and testing 424 agent add-ons a night. Real question: what's the one skill or MCP server you'd want checked before you install it? Reply and we'll run it through all 5 agents.
7. **How we test** — Fresh sandbox, real agent CLI, no credentials. "Pass" = the agent itself lists it as installed (or connected, for MCP). Every result links its log. If we got yours wrong, tell us, we'll rerun it. skillmaxx.gilventures.ai/how-we-test/
8. **Standout** — Superpowers installed clean in 4 agents with zero flakes this week. Stars don't prove installs. Two clean nights in a row do. skillmaxx.gilventures.ai/skills/superpowers/
9. **Tool authors** — Listed for one agent but quietly work in three? Most skills do. Submit yours and we'll show you the logs for Claude Code, Codex, Grok Build, Cursor and Pi, good or bad. skillmaxx.gilventures.ai/submit/
10. **Reference servers** — The official MCP reference servers (fetch, filesystem, git, memory, time) are still the backbone of most setups. Boring is a feature. They're tested every night too.
11. **Safe-today** — Before you install something into your agent: skillmaxx.gilventures.ai/reports/latest/ has an "is it safe to install today?" box. Type the tool, pick your agent. Tell us if it's useful or if we should kill it.
12. **Weekly scorecard (Sun)** — Week 44 install scorecard: 802/890 clean (90.1%). Confirmed broke: 1 add-on (2 installs). Really fixed: 0. Flaky noise we refused to count: 13. Most reliable: Codex. What should we add next week? skillmaxx.gilventures.ai/reports/week/2026-44/
   *(Regenerate numbers Sunday from weekly_scorecard.py.)*

---
<!-- source: growth/newsletter/issue-002-beehiiv.md -->
<!-- Beehiiv paste-ready DRAFT, not sent. Sends Tue Nov 3. Regenerate the scorecard block Monday night: python3 testing/weekly_scorecard.py -->
**Title:** SkillMaxx #2: we stopped crying wolf
**Subtitle:** A new two-night rule, a weekly scorecard, and a question for you.
**Preview text:** 13 add-ons flip-flopped this week. We refused to call any of them broken.

![SkillMaxx](https://raw.githubusercontent.com/grandpajackai/skillmaxx/master/growth/brand/beehiiv/skillmaxx-banner-1200x300.png)

## hey, Brandon here 👋

Quick confession. In week one we were calling things "broken" and "fixed" off a single night of tests. Then we noticed 13 of our 14 "fixed" items had just flip-flopped. That's not news, that's noise.

So we changed the rules:
- **Broken** now means it failed **two nights in a row**.
- **Flaky** means it flip-flopped. We label it and move on.
- **Needs your key** means it only failed because our sandbox has no API keys. Not the tool's fault.

Less drama, more truth. Here's the first scorecard under the new rules.

## 📊 Weekly install scorecard (2026-10-25 to 2026-10-26, 2 nightly runs)

**Pass rate trend** (installs we can judge without an API key): 10-25 795/890 (89.3%) → 10-26 802/890 (90.1%)
**Confirmed broke (failed 2 nights running):** [gdharness](https://skillmaxx.gilventures.ai/skills/gdharness/) (2 installs)
**Really fixed (passing after 2+ bad nights):** nothing (0 installs)
**Flaky, ignore the drama:** 13 add-ons flip-flopped (e.g. Airwallex Dev, @cyanheads/pubmed-mcp-server, Alloydb Omni, Claude Code Setup, Claude Security). We don't call these broken or fixed.
**Needs your API key:** 12 installs only failed because our sandbox has no keys. Not broken, just shy.
**Standout of the week:** [Superpowers](https://skillmaxx.gilventures.ai/skills/superpowers/), clean in 4 agents, zero flakes. Superpowers teaches Claude brainstorming, subagent driven development with built in code review, systematic debugging, and red/green TDD. Additionally, it teaches Claude how to author and test new ski
**Most reliable agents:** 1. Codex 100.0% · 2. Claude Code 93.9% · 3. Grok Build 93.5% · 4. Pi 65.5% · 5. Cursor 60.9%

Chart + full week: https://skillmaxx.gilventures.ai/reports/week/2026-44/ · Is your tool safe today? https://skillmaxx.gilventures.ai/reports/latest/

## 🔧 Install tip of the week

Pin the marketplace. Same plugin names now live in more than one marketplace, so agents ask "which one?". In Claude Code: `/plugin install sentry@claude-plugins-official`. In Grok Build: `grok plugin install auth0@<marketplace>`.

## 🆕 New on the site

- **Is it safe to install today?** Type a tool, pick your agent, get last night's answer: https://skillmaxx.gilventures.ai/reports/latest/
- **Weekly scorecard pages** with a chart: https://skillmaxx.gilventures.ai/reports/week/2026-44/

## 🙏 I need your help (seriously)

We're tiny and early, and I'd rather build what you'll use than guess. Hit reply with any of these:
1. **One tool you want tested** before you install it.
2. **Is this scorecard useful or noise?** One word is fine.
3. **Did we get your tool wrong?** Send the link, we'll rerun it and fix the page.

I read every reply.

---

**Sponsor:** This spot is open. Founding sponsors get one labeled line here for $19 an issue, and money never changes a test result. https://skillmaxx.gilventures.ai/advertise/

Built a skill? We'll run it through all five agents: https://skillmaxx.gilventures.ai/submit/

---
<!-- source: growth/sponsors/TARGETS-RANKED.md -->
## Sponsor targets, ranked (draft, 2026-10-26). No one has been contacted.

Score = Fit (is their tool in our directory and tested?) ×3 + Budget signal (they already buy dev sponsorships) ×2 + Ease (public contact / dev-rel) ×1. Max 30.

| # | Company | Score | Why | Best slot | First touch |
|---|---|---|---|---|---|
| 1 | Exa | 27 | Search MCP agents install first; sponsors dev newsletters | Category: Search $15/mo | Email (01-exa.md) |
| 2 | Firecrawl | 26 | Scraping MCP + plugins, active dev-rel, YC | Bundle $49 | Email (02-firecrawl.md) |
| 3 | Upstash / Context7 | 25 | Context7 docs MCP is everywhere | Featured $29 | Email (04-context7.md) |
| 4 | Tavily | 24 | Search API for agents, buys newsletter ads | Newsletter $19 | Email (05-tavily.md) |
| 5 | Composio | 23 | Integrations; awesome-claude-skills list owner | Category: Integrations | Email (03-composio.md) |
| 6 | Browser Use | 21 | Browser agents, OSS-heavy, loud on X | Featured | X DM after a reply thread |
| 7 | Neon | 20 | Postgres MCP, big DevRel budget | Category: Databases | Form |
| 8 | Supabase | 20 | Official plugin + MCP; partner program | Category: Databases | Partner form |
| 9 | CodeRabbit | 19 | Code-review plugin passes in 4+ agents | Featured | Form |
| 10 | Sentry | 18 | Official plugin in Claude/Codex marketplaces | Newsletter | Enterprise form (slow) |
| 11 | PostHog | 17 | Analytics MCP, fun brand, buys newsletter ads | Newsletter | Form |
| 12 | Skyvern | 15 | Browser automation, smaller | Category | Form |

**Sequence (when you approve):** wait until issue #2 is sent and there are ≥25 subscribers, then 2 emails a week, top of the list first, one follow-up after 7 days, then stop.

## What exists vs missing
| Item | Status |
|---|---|
| Sponsor menu / pricing page | ✅ Live: /advertise/ (founding prices, struck-through regular prices, Pay once + Subscribe & save, media kit, reliability ranking) |
| Stripe links + portal | ✅ 8 Payment Links + customer portal, all return 200 (checked today, nothing changed) |
| Thank-you / asset intake | ✅ /sponsor/thanks/ (false-success bug fixed today, PR #24) |
| Playbook + pipeline | ✅ growth/sponsors/PLAYBOOK.md, PIPELINE.md |
| Target list | ✅ 12 companies; **ranking was missing → added above** |
| Outreach drafts | ⚠️ 3 existed (Exa, Firecrawl, Composio) with stale numbers → revised; **Context7 + Tavily added** |
| Follow-up template | ❌ was missing → added (06-follow-up.md) |
| BF/CM offer | ⚠️ one paragraph idea in SPONSORS.md → full draft in growth/sponsors/BFCM.md |
| Monthly sponsor report template | ❌ still missing (not needed until first booking) |

---
<!-- source: growth/outreach/01-exa.md -->
## Cold intro: Exa (DRAFT v2, not sent)
**To:** via https://exa.ai/contact (partnerships) · **From:** skillmaxx@gilventures.ai
**Subject:** we install your MCP every night (it behaves)

Hi Exa team,

I'm Brandon, I run SkillMaxx. Every night it installs agent skills and MCP servers in fresh sandboxes across Claude Code, Codex, Grok Build, Cursor and Pi, then publishes what installed and what didn't, logs included: https://skillmaxx.gilventures.ai/reports/latest/

Search MCPs are what people install first, so I'd love Exa to be the founding sponsor of our Search category: $15/mo, rate locked for 6 months, labeled "Sponsored". Honest bit: we launched this month and the audience is small. That's why it's cheap, and you'd get a monthly report with real numbers even when they're tiny.

Paying gets a spot, never a better test result.

Even if it's a no, I'd value one thing: is there an Exa skill or config you'd like us to test that we're missing?

Brandon
SkillMaxx · https://skillmaxx.gilventures.ai

---
<!-- source: growth/outreach/02-firecrawl.md -->
## Cold intro: Firecrawl (DRAFT v2, not sent)
**To:** via https://www.firecrawl.dev/contact · **From:** skillmaxx@gilventures.ai
**Subject:** Firecrawl × 5 coding agents, tested nightly

Hey Firecrawl folks,

I'm Brandon from SkillMaxx. We answer the question devs ask right before installing something: "will this actually work in my agent?" Every night we install skills, plugins and MCP servers across Claude Code, Codex, Grok Build, Cursor and Pi in keyless sandboxes and publish the results. Last night 802 of 890 judgeable installs were clean; the rest are listed with logs.

Low-stakes ask: be a founding sponsor. The bundle is a featured spot, a category logo and a line in our weekly email for $49/mo (or $42/mo subscribed, cancel anytime), locked for 6 months.

Full honesty, we're new and small. You'd be backing it early and you'd get real monthly numbers. And if you'd rather just tell us which Firecrawl setup we should be testing, that helps too.

Brandon
https://skillmaxx.gilventures.ai

---
<!-- source: growth/outreach/03-composio.md -->
## Cold intro: Composio (DRAFT v2, not sent)
**To:** via https://composio.dev/contact · **From:** skillmaxx@gilventures.ai
**Subject:** your skills list + our nightly installs?

Hi Composio team,

Your awesome-claude-skills list is required reading. The part nobody has time for is checking which of those skills install in which agent, so that's what SkillMaxx does every night across Claude Code, Codex, Grok Build, Cursor and Pi, with logs.

Two ideas:
1. **Free, no strings:** send us any Composio skills and we'll run them through all five agents and share the logs.
2. **If it's useful:** founding sponsor of our Integrations category, $15/mo, locked six months, clearly labeled.

We're early and small, and I'd rather say that up front. Would either be useful?

Brandon
https://skillmaxx.gilventures.ai

---
<!-- source: growth/outreach/04-context7.md -->
## Cold intro: Upstash / Context7 (DRAFT, not sent)
**To:** via https://upstash.com/contact · **From:** skillmaxx@gilventures.ai
**Subject:** Context7 is in a lot of agent setups. We check it nightly

Hi Upstash team,

I'm Brandon from SkillMaxx. We install agent skills and MCP servers every night in Claude Code, Codex, Grok Build, Cursor and Pi and publish what installs, with logs. Context7 shows up in a lot of the setups people ask us about.

Would you be up for a founding Featured slot? It's the one labeled Sponsored card in our homepage Featured row plus top-of-category, $29/mo (or $25/mo subscribed), locked 6 months. We're new and small; you'd get a monthly report with honest numbers.

If it's not a fit, I'd still love to know: is there a Context7 config you'd want us testing that we aren't?

Brandon
https://skillmaxx.gilventures.ai

---
<!-- source: growth/outreach/05-tavily.md -->
## Cold intro: Tavily (DRAFT, not sent)
**To:** via https://www.tavily.com/contact · **From:** skillmaxx@gilventures.ai
**Subject:** a $19 test: one line in a weekly email for agent builders

Hi Tavily team,

I'm Brandon. SkillMaxx installs agent skills and MCP servers every night across five coding agents and sends a weekly install scorecard to developers who are deciding what to add to their agent.

Smallest possible experiment: one labeled sponsor line in an issue for $19. If it does nothing, you've lost a sandwich. If it works, the founding rate is locked for 6 months. We're new and the list is small, and you'll see the real numbers afterwards.

Want me to hold a Tuesday for you?

Brandon
https://skillmaxx.gilventures.ai/advertise/

---
<!-- source: growth/outreach/06-follow-up.md -->
## Follow-up (DRAFT, send once, 7 days after the first email, then stop)
**Subject:** Re: <original subject>

Hi again, one nudge and then I'll leave you alone. Since my last note we published this week's install scorecard: <link to /reports/week/YYYY-WW/>. If sponsoring isn't a fit, a one-line "not now" is genuinely helpful, and so is "test this instead".

Brandon

---
<!-- source: growth/sponsors/BFCM.md -->
## Black Friday / Cyber Monday sponsor promo (DRAFT, needs your OK; no Stripe changes made)

**Did one exist?** Only as a one-paragraph idea in SPONSORS.md ("lock founding pricing 12 months or a free extra issue"). Nothing built. Here's the full proposal.

## Offer: "Founding 12"
- **Window:** Fri Nov 27, 12:00 AM ET → Mon Nov 30, 11:59 PM ET.
- **What:** book any founding slot during the window and your founding rate is locked for **12 months instead of 6**, plus **one free newsletter line** in December.
- **Why this and not a discount:** prices are already founding-low; a longer lock costs $0 today, keeps the honest "first 10 sponsors" cap, and rewards early backers.
- **Cap:** still counts toward the first 10 founding sponsors.

## What it needs (no new Stripe prices)
1. Banner on /advertise/ during the window (small PR, scheduled to merge Nov 27, revert Dec 1).
2. Fulfil the 12-month lock manually: note it in PIPELINE.md and the thank-you email. Existing Payment Links and subscription prices stay as they are.
3. One line in the Nov 24 and Dec 1 newsletters.

## Draft copy
**Site banner:** "Black Friday, our way: book a founding slot by Cyber Monday and we lock your rate for 12 months, not 6. Plus a free newsletter line in December. Money still never changes a test result."

**X / Bluesky (Nov 27):** "Black Friday, sponsor edition: book a founding SkillMaxx slot by Monday night and your rate is locked for 12 months instead of 6, plus a free newsletter line. Only 10 founding spots, ever. skillmaxx.gilventures.ai/advertise/"

**Email line to warm leads (only those who already replied):** "Small heads-up: anything booked by Monday 11:59 PM ET gets the founding rate locked for 12 months."

---
<!-- source: growth/reddit/POSTS.md -->
## Reddit pack (account u/SkillMaxxHQ). DRAFTS, nothing posted.

Rules notes are from each sub's known rules; **re-read the sidebar right before posting**, they change. General: one sub per day max, reply to every comment for the first 2 hours, no cross-posting the same text, disclose "I built this".
New-account caution: u/SkillMaxxHQ has little karma. Several subs filter new accounts, so spend a few days commenting helpfully first, or post from your personal account with disclosure (your call).

---
## 1. r/mcp — flair: Showcase / Resource
**Rules to respect:** MCP-related only, self-promo allowed as showcase with disclosure, no spam/repeat posts.

**Title:** I install MCP servers in 5 agents every night with no API keys. Here's what actually connects (and I need feedback)

**Body:**
I built a little test rig (disclosure: it's my project, SkillMaxx). Every night it adds MCP servers to fresh sandboxes for Claude Code, Codex, Grok Build, Cursor and Pi, and counts a server as working only if the agent reports it connected and lists its tools.

Things I learned that might save you time:
- **Most "failures" are missing keys, not bugs.** 12 installs last night only failed because the sandbox has no credentials, so I now list those separately.
- **One bad night means nothing.** 13 servers/plugins flip-flopped this week. I only call something broken after two failing nights in a row.
- **Cursor is strict.** In ~/.cursor/mcp.json the server has to show "ready". 27 of 46 judgeable installs did.
- The official reference servers (fetch, filesystem, git, memory, time) are still the most boring and most reliable.

Results are public: https://skillmaxx.gilventures.ai/reports/latest/

Honest questions, because it's early:
1. Is "installs + connects with no keys" a useful signal for you, or do you need a deeper test (actually calling a tool)?
2. Which servers should I add?
3. If I got your server wrong, tell me and I'll rerun it.

---
## 2. r/ClaudeAI — flair: "Built with Claude" (or Productivity) 
**Rules to respect:** must be about Claude; self-promo only with clear disclosure and value in the post; no low-effort link drops.

**Title:** Tested 367 Claude Code plugin installs in clean sandboxes. Notes on what fails and why

**Body:**
Disclosure: I run SkillMaxx, a free directory that test-installs agent plugins every night. Sharing the Claude Code findings because they're useful on their own:

- 340 of 367 Claude Code installs passed last night. 6 of the misses only needed an API key.
- **Always pin the marketplace**: `/plugin install sentry@claude-plugins-official`. Plugin names now exist in multiple marketplaces.
- Grok Build auto-loads Claude Code plugins, so many plugins work in both without the author doing anything.
- Flip-flopping installs are common (network, rate limits), so I wait for 2 bad nights before calling anything broken.

Per-plugin results with logs: https://skillmaxx.gilventures.ai/reports/latest/

I'd really like feedback: what's the Claude Code plugin you'd most want checked before installing? And is this kind of report useful or overkill?

---
## 3. r/cursor — flair: Showcase / Resources
**Rules to respect:** Cursor-related, showcase flair for projects, no referral/affiliate links.

**Title:** Which MCP servers actually connect in Cursor? I test them every night (free list)

**Body:**
I made a list of every MCP server I could install in a real Cursor CLI sandbox (no accounts, no keys), counting it only if Cursor says ready and lists tools. Disclosure: it's my project.

Current numbers: 27 of 46 judgeable installs connected; 6 more only failed for lack of an API key. Full list with the exact mcp.json entry for each: https://skillmaxx.gilventures.ai/guides/best-mcp-servers-cursor/

Tip that fixed most of my own issues: if Cursor shows anything other than "ready", it's not running, and the log usually says it wants a key or an argument.

What MCP servers are you using in Cursor that I'm missing? I'll add them to the nightly run.

---
## 4. r/SideProject — flair: none needed
**Rules to respect:** self-promo is the point; be genuine, no fake engagement.

**Title:** I built a directory that installs every AI agent plugin every night and publishes what breaks. 10 days in, $0 spent, here's what I learned

**Body:**
SkillMaxx (https://skillmaxx.gilventures.ai) installs 424 agent skills/plugins/MCP servers across 5 coding agents every night and posts the results.

What I learned in 10 days:
- My first daily reports were mostly noise. 13 of 14 "fixed" items were flaky. Now I need 2 bad nights before I call anything broken.
- Being honest about limits (no API keys in the sandbox) made the data more trustworthy, not less.
- Static site + nightly script + GitHub Pages = $0 running cost.

I'd love blunt feedback: does the homepage make sense in 5 seconds? Would you subscribe to a weekly install scorecard, or is that a snooze?

---
<!-- source: growth/profiles/PROFILES.md -->
## Profile assets (X, Bluesky, LinkedIn). Drafts; Brandon uploads (we don't hold these logins).

Files are in this folder, raw links: `https://raw.githubusercontent.com/grandpajackai/skillmaxx/master/growth/profiles/<file>` once merged.

## X @SkillMaxxAI
- **Bio:** keep the live approved one: "We install agent skills & MCP servers in Claude Code, Codex, Grok, Cursor and Pi every night and post what works. Free daily report + weekly newsletter."
- **Location:** `in a sandbox, no API keys` · **Website:** https://skillmaxx.gilventures.ai/reports/latest/ (recommend pointing at the daily report the bio promises)
- **Avatar:** ⚠️ Buffer still shows X's default egg avatar → upload `avatar-400.png`. **Needs Brandon.**
- **Header:** `growth/x/header-1500x500.png` (existing, still accurate). **Needs Brandon** if not uploaded.
- **Pinned:** see growth/social/PINNED.md, attach `pin-chart.png`.

## Bluesky @skillmaxx.bsky.social
- **Display name:** SkillMaxx
- **Bio (≤256):** "We install agent skills, plugins & MCP servers in Claude Code, Codex, Grok Build, Cursor and Pi every night and post what works. Brand new, feedback welcome: reply with a repo and we'll test it. Free daily report + weekly newsletter ↓ skillmaxx.gilventures.ai"
- **Avatar:** `avatar-400.png` (Buffer shows a custom avatar already, so probably done; double-check it's the lime check-X).
- **Banner:** `bluesky-banner-3000x1000.png` (3:1).
- I can set these via the Bluesky API with the SkillMaxx app password if you say yes; otherwise **Brandon uploads**.
- Optional: custom domain handle `@skillmaxx.gilventures.ai` (one DNS TXT record, free) for trust.

## LinkedIn page (SkillMaxx AI)
- **Tagline:** "Find the skills, plugins and MCP servers that actually work with your AI agent." (approved)
- **Logo:** live logo looks right in Buffer.
- **Cover:** `linkedin-cover-1128x191.png` (text is right-aligned so the logo overlap bottom-left doesn't hide it). **Needs Brandon.**
- **Website button:** https://skillmaxx.gilventures.ai/reports/latest/ ("Visit website").
- **About (overview, 1,350 chars, under the 2,000 limit):**

SkillMaxx is a free directory of agent skills, plugins and MCP servers that we actually install. Every night we pull the official marketplaces and npm, then install each add-on in fresh sandboxes for Claude Code, Codex, Grok Build, Cursor and Pi, with no accounts or API keys. An add-on only counts as working if the agent itself lists it as installed, or for MCP servers, connected with its tools listed.

The results are public, failures included. Each skill page shows the exact install command for your agent, when it was last tested and the log. We only call something broken after it fails two nights in a row, we label flip-floppers as flaky, and we list installs that only failed for lack of an API key separately, so tool authors don't get blamed for our missing keys.

What you get:
• A free daily report with an "is it safe to install today?" lookup
• A weekly install scorecard by email every Tuesday
• Guides like "Which MCP servers work in Cursor?"

We're early and small, and we build in public. If a result looks wrong, or there's a tool you want tested, tell us and we'll rerun it.

Sponsorships are clearly labeled and never change a test result.

Website: https://skillmaxx.gilventures.ai
