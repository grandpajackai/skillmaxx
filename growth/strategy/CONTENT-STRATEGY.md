# SkillMaxx social content strategy (v1, 2026-10-26)

Status: DRAFT for Brandon's review. Nothing is queued in Buffer and nothing is posted. Drafts: `DRAFTS-2026-10-27.md` (generated from `drafts.py`, which also checks lengths).

## Goal, in one line
Become the account devs check **before** they install an agent add-on. Growth (follows) → community (replies, test requests) → owned audience (newsletter subs) → revenue (sponsors once there are 25+ subs).

## Three key calls
1. **Daily on all three channels, 1 Buffer post per channel per day, refilled weekly.** Buffer Free caps the *queue* at 10 scheduled posts per channel (refills as posts publish; 3 channels max) - not a monthly cap. 7 posts/week/channel fits under 10, so a Sunday approve-and-refill session keeps every channel daily for $0. Bluesky moves from 3×/week to daily: it has a chronological feed, no link penalty and a dev crowd, so frequency costs nothing there; what it punishes is copy-paste and engagement bait.
2. **One daily theme, three native posts, full context everywhere.** Same idea and the same full story each day, formatted per platform: X = 2–4 post thread, link only in the last post; Bluesky = warmer, nerdier, lowercase, link inline (no penalty), alt text always; LinkedIn = founder voice, proper case, 600–1,300 chars, an image, link in post (company pages aren't penalized).
3. **Replies are the growth engine on X; posts are the receipts.** The sniper routine's 3–5 one-tap replies a day to relevant posts (manual, Brandon taps) do more for a new account than any scheduled post. Bluesky replies stay approval-gated until Brandon says go autonomous.

## Rule: full context on every platform (Brandon, 2026-10-26)
LinkedIn is the quality bar. X and Bluesky carry the same full story (who, what, when, what it means for the reader), never a vague, edgy summary. Post 1 always names the company or tool in plain words and stands alone. Say what things are (e.g. "a skill is a folder with a SKILL.md file"). X = 2–4 post thread (each ≤280); Bluesky = 1–3 posts (each ≤300), link inline, alt text on images. Single posts only when the full message truly fits. No clickbait that overpromises; every hook is backed by a receipt in the thread.

## The thread formula we apply
Modelled on the researched accounts (@cursor_ai one-line claim + proof, @thedelost / @quangdigiaz numbered repo lists, @levelsio timely first-person tips, Simon Willison's sourced "what happened" posts).
**X (2–4 posts)**
1. Hook post: a surprising number, a bold-but-true claim, or a named news event, with the full point in plain words. Ends with an open loop ("here's why", "the other 88 are the interesting part", 👇/🧵).
2. Context: what the thing is and who did what, when. One idea per post, short lines.
3. Receipt: our own numbers, a log or a screenshot.
4. Payoff: what it means for devs + one question or CTA, and the only link.
**Bluesky (1–3 posts)**: same arc compressed. Post 1 = hook + who/what/when; post 2 = what it means + receipt; last = question + link inline (no link penalty). Warmer, lowercase-friendly, no bait phrases, alt text always.
**LinkedIn (1 post)**: title-line hook → who/what/when → numbered "what it means for teams" → our receipt → one question → link → "Brandon".

## Buffer thread support (checked 2026-10-26)
Buffer schedules X and Bluesky threads (up to 25 posts, web composer; the Buffer MCP `create_post` takes `metadata.twitter.thread` / `metadata.bluesky.thread`). **But the Free plan allows only ONE scheduled thread per queue at a time**; unlimited threads can sit in Drafts (https://support.buffer.com/en-us/articles/using-xtwitter-with-buffer-nA84XnWtuU, https://support.buffer.com/en-us/articles/using-bluesky-with-buffer-7f6OcRnzIO). Operating model: Brandon approves the week on Sunday → all approved threads are saved as Buffer drafts → after each day's thread publishes, the next approved draft is moved into the queue (a daily step, no new approval needed). LinkedIn posts are single posts and queue normally. Alternative if that's too fiddly: Bluesky threads via the Bluesky API (needs Brandon's OK) or X Premium long posts.

## Buffer free limits (verified 2026-10-26)
| Limit | Value | Source |
|---|---|---|
| Channels | 3 (all used: X, Bluesky, LinkedIn page) | https://support.buffer.com/en-us/articles/buffer-pricing-and-features-6pJrOPuzIt |
| Scheduled posts | 10 per channel at any time, refills as posts publish | https://support.buffer.com/en-us/articles/how-many-posts-can-i-schedule-in-advance-Kmy2IEecqm |
| Ideas | 100 | https://buffer.com/pricing |
| First-comment scheduling | Paid only (Essentials) | https://buffer.com/resources/buffer-vs-meta-business-suite/ |
| API | Free (3,000 req/mo); can't change posting schedules | buffer.com/pricing, our own audit |
Design consequence: queue ≤7 per channel each Sunday (3 spare slots for news/big-event posts). X links go in thread post 2, not a scheduled first comment.

## Posting schedule (America/New_York) - replaces decision #1
| Channel | Mon–Fri | Sat | Sun | Why |
|---|---|---|---|---|
| X | 9:30 AM | 11:00 AM | 6:00 PM (scorecard) | Buffer 2026 study (8.7M posts): Tue–Thu 9–11 AM top; weekends weak, so lighter content there |
| Bluesky | 7:30 PM | 5:00 PM | 6:00 PM | Buffer (3M Bluesky posts): weekday late mornings are the *weakest*; weekday evenings and Sat 5 PM best |
| LinkedIn | 12:00 PM (Wed 4:00 PM) | 10:00 AM | 10:00 AM | Sprout: Tue–Thu 11 AM–5 PM; Buffer 2026: Wed 4 PM peak. Weekend posts are low-effort evergreen; drop them after 3 weeks if they underperform |
Launch exception: all three go out Tue Oct 27 at 9:30 AM and get pinned (Bluesky's evening slot starts Wed).

## Pillars and mix
| # | Pillar | X | Bluesky | LinkedIn |
|---|---|---|---|---|
| 1 | What we do / what results mean | 20% | 20% | 15% |
| 2 | Industry know-how (tips, myths, how-tos) | 20% | 25% | 20% |
| 3 | Free daily report + weekly newsletter CTAs | 15% | 10% | 15% |
| 4 | Sponsorships and benefits | 5% | 5% | 10% |
| 5 | Viral news commentary (value only) | 15% | 10% | 10% |
| 6 | Leaders and leading companies (education only) | 10% | 5% | 15% |
| 7 | Seasonal / business calendar | 5% | 5% | 5% |
| 8 | Community: test requests, polls, build-in-public | 10% | 20% | 10% |
Guardrails: never political (no election, policy or culture-war hooks, even on Nov 3), punch at problems not people, ≤2 CTA posts/week, ≤1 sponsor post per 2 weeks until 25 subs, every number from `reports.json`/`weekly_scorecard.py`.

## Weekly rhythm
| Day | Theme | Main pillar |
|---|---|---|
| Mon | Install tip / how-to | 2 |
| Tue | Results receipt or newsletter-out day | 1 / 3 |
| Wed | News take (what it means for installs) | 5 / 6 |
| Thu | Test-request call-out, or sponsor/tool-author post every other week | 8 / 4 |
| Fri | Myth vs. reality or how-we-test | 2 / 1 |
| Sat | Build in public / seasonal | 8 / 7 |
| Sun | Weekly scorecard + newsletter CTA | 3 |
Big-event posts (≥1k★ tool confirmed broken 2 nights, or agent update breaking ≥3 installs) jump the queue the same day after Brandon's OK, using a spare slot.

## Platform playbooks
**X @SkillMaxxAI.** Hook in line 1 (number, myth, lesson learned). ≤280 chars, one idea. Text-first for takes; image for scorecards/data. No hashtags (0–1 max). No link in the main post; CTA days use a 2-post thread with the link in post 2. 3–5 sniper replies/day. Pin the launch post.
**Bluesky @skillmaxx.bsky.social.** 200–300 chars, lowercase-friendly, peer-to-peer, no bait ("thoughts?"). Link inline; first URL makes the card. Alt text on every image. Natural keywords (claude code, mcp, cursor) route posts into dev custom feeds; 0–1 hashtag. Later: build a "MCP & agent-skills builders" starter pack (pillar 8).
**LinkedIn SkillMaxx AI page.** Founder first person, signed "Brandon" on founder posts. Short title line, numbered lists, one question at the end. Image posts by default (image beat link, text and document posts on company pages in a 2026 study); links in post are fine for company pages.

## Research: what similar accounts do (pulled 2026-10-26)
| Account | Example | What to copy |
|---|---|---|
| @cursor_ai (493k) | https://x.com/cursor_ai/status/2113661506634305834 (6.4k likes) "Cursor can now control your computer." + demo video | 1-line claim, then proof (video/screenshot). Nothing else |
| @cursor_ai | https://x.com/cursor_ai/status/2114793714531102901 (2.2k likes) Agent SDK launch | Concrete nouns: "prompts in Markdown, tools in TypeScript" |
| @levelsio (983k) | https://x.com/levelsio/status/2113587042185576853 (6.5k likes) VPS security tip | First-person, practical, timely tip tied to the news of the day |
| @thedelost (5k followers) | https://x.com/thedelost/status/2114016386896773177 (693 likes) "Anthropic turned Agent Skills into an open spec…" repo listicle | Small accounts go viral with timely lists of repos. We do the honest version: lists with receipts, no all-caps |
| @quangdigiaz | https://x.com/quangdigiaz/status/2110630770574348455 "7 GitHub repos that give Claude Code & Codex…" | Numbered repo lists with star counts; we add "installs clean in N agents" |
| @swyx (208k) | https://x.com/swyx/status/2113717251543367880 "*taps sign*" lesson + screenshot | Short lesson + screenshot, opinion as advice |
| simonwillison.net (Bluesky) | https://bsky.app/profile/simonwillison.net/post/3murtmdynq22s TIL with screenshot | Bluesky devs reward TIL-style "here's exactly what happened" with images |
| simonwillison.net | https://simonwillison.net/2026/Oct/22/donating-agent-skills/ | Fast, sourced take on news within hours |
| Formats research | https://buffer.com/resources/best-time-to-post-on-bluesky/ · https://ligosocial.com/research/linkedin-company-pages-2026 · https://gtmhacker.ai/guides/bluesky-post-guide/ | Timing, LinkedIn formats, Bluesky norms |

## Seasonal calendar (pillar 7)
| When | Hook | Use |
|---|---|---|
| Oct 31 | Halloween: "scariest install log" (flaky) | Sat post |
| Nov 1 | DST ends: "our run is on UTC" | Sun scorecard line |
| Nov 3 | Newsletter #2 (no election mentions) | Tue |
| Nov 9–20 | Q4 cleanup before code freeze | Mon tips |
| Nov 24 | Newsletter: Founding 12 heads-up | Newsletter line |
| Nov 26 | Thanksgiving: thank tool authors (name 3 clean tools) | All 3 |
| Nov 27–30 | Black Friday / Cyber Monday "Founding 12" (12-month rate lock) | 1 post/channel on Nov 27 + reminder Nov 30; no urgency tricks |
| Dec 1 | Advent of Code starts: agent-friendly setup tips | Dev hook |
| Dec | "Year in installs" recap, holiday code freeze, budget-reset note for sponsors | Weekly |
| Jan (Q1) | "Your agent setup for 2027": fresh-start checklist, new-year scorecard | Kickoff |
| Ongoing | Agent release days (Claude Code, Codex, Cursor, Grok, Pi): same-day "did anything break?" | News take |

## Existing drafts: keep / rework / retire
| Draft | Decision |
|---|---|
| PINNED.md X/Bluesky/LinkedIn | Kept, reworked into the Oct 27 posts (X now a 2-post thread so the link doesn't throttle the pin) |
| POST-BANK #1 marketplace tip, #8 standout, #7 how we test, #9 tool authors, #4 flaky rule, #12 scorecard | Reworked into the starter batch |
| POST-BANK #2 Cursor tip, #3 per-agent data, #5 needs-key, #6 feedback ask, #10 reference servers, #11 safe-today | Kept in the bank for weeks 3–4 (refresh numbers) |
| weekly/2026-44.md | Superseded by the Nov 1 scorecard drafts (same numbers, native per platform) |
| Daily report posts | Off; big-event criteria only (decision #11) |

## Weekly operating loop
1. Sun: refresh numbers, Brandon approves next week's 7×3 drafts, queue (≤7 per channel).
2. Daily: sniper replies (X), answer replies within a few hours, log test requests in `growth/x/sniper-log.md`.
3. Mon: 15-min look at Buffer insights → adjust one thing (hook type, time, format). After 3 weeks, re-cut pillar mix on data.
KPIs: followers per channel, replies per post, test requests received, newsletter subs (target 25 for sponsor outreach), /advertise/ inquiries.
