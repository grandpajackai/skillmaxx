# Decisions log

## 2026-10-26 — Brandon approved all 10 review-pack recommendations
1. **Buffer schedules:** X Mon–Fri 9:30 AM; Bluesky Mon/Wed/Fri 12:30 PM + Sun 6:15 PM; LinkedIn Tue 8:30 AM + Thu 12:00 PM (America/New_York). Buffer's API has no posting-schedule mutation, so Brandon sets these in Buffer → channel → Settings → Posting schedule.
2. **Post bank:** growth/x/posts.json retired; growth/social/POST-BANK.md is active.
3. **Pinned posts:** approved as drafts only. Nothing posted or pinned until Brandon signs off the final text in the dashboard.
4. **Newsletter:** issue #2 (growth/newsletter/issue-002-beehiiv.md) is the FIRST send, scheduled Tue Nov 3, 2026. Draft, not sent, pending Brandon's text review; regenerate the scorecard Monday night.
5. **Sponsor outreach:** on hold until the newsletter has 25+ subscribers. Then top 5 ranked targets, 2 emails/week, one follow-up.
6. **Founding 12 (BF/CM) offer:** approved as a plan (Nov 27–30). No Stripe changes made. Needed when it runs:
   - Site: dismissible banner on /advertise/ (and optionally home) Nov 27 → revert Dec 1; one line on /sponsor/thanks/ during the window confirming the 12-month lock.
   - Stripe (none required): existing Payment Links stay. Optional later: add a custom-field/metadata note "Founding 12" to the links, or duplicate links with "12-month founding lock" in the description; for subscriptions, ensure no price change for 12 months (no action needed, prices are fixed).
   - Ops: tag bookings in PIPELINE.md, add the lock to the thank-you email, schedule the free December newsletter line.
   - Content: X/Bluesky/LinkedIn post Nov 27 + newsletter lines Nov 24 and Dec 1 (Brandon reviews).
7. **Reddit:** posts go from u/SkillMaxxHQ; warm up with helpful r/mcp comments for a few days first, then r/SideProject first post.
8. **PR #25** (flaky-vs-broken guide, guide feedback boxes, privacy + terms): approved, DRAFT label removed, merged.
9. **Bluesky profile:** bio + banner set via API on 2026-10-26 (avatar and display name "SkillMaxx AI" kept).
10. **Beehiiv:** drop from the Pro trial to the free plan before Nov 2, 2026 (reminder; nothing changed yet).

## 2026-10-26 (evening)
11. **Daily report posts:** drafted only for big events (≥1k-star tool confirmed broken, or agent update breaking ≥3 installs) plus a weekly scorecard post. No daily emails.
12. **Advertise/submit autoresponses:** text approved as written; forms use standard POST + reCAPTCHA.
13. **First post / pinned post:** Tue Oct 27 ~9:30 AM ET, after Brandon reviews the social assets.
14. **Content strategy:** daily posting within Buffer's free limits on every channel, platform-specific formats, built on pillars (results, industry knowledge, report/newsletter CTAs, sponsorships, viral-news commentary, industry leaders, seasonal/Q4–Q1/BFCM), modelled on what similar popular accounts do. Never political.
15. **Knowledge base:** everything is documented in the repo (HANDBOOK.md is the index) so any collaborator or agent can catch up.

## 2026-10-26 (night) — content strategy v1 (PROPOSED, pending Brandon's review)
16. **Cadence:** daily on X, Bluesky and LinkedIn, 1 Buffer post per channel per day, refilled each Sunday (Buffer Free = 10 queued per channel, refillable). Replaces the 3×/week Bluesky and 2×/week LinkedIn plan once approved.
17. **Times (ET):** X weekdays 9:30 AM, Sat 11 AM, Sun 6 PM; Bluesky weekdays 7:30 PM, Sat 5 PM, Sun 6 PM; LinkedIn weekdays 12 PM (Wed 4 PM), weekends 10 AM. Launch posts all at 9:30 AM Tue Oct 27, then pinned.
18. **Format:** one daily theme, three native posts; X keeps links out of the main post (thread post 2 on CTA days); 8 pillars with per-platform mix in CONTENT-STRATEGY.md.

## 2026-10-26 (late night)
19. **Stripe labels:** best-practice fix approved: separate product for the $59/mo 4-issue newsletter plan; clearer names/descriptions on all sponsor products.
20. **No payment watcher:** Brandon uses the dashboard Sponsors section + Stripe emails.
21. **BFCM Founding 12:** approved (12-month founding lock + free December newsletter shoutout for bookings Nov 27–30), tracked in PIPELINE.md, no Stripe changes; final banner copy to Brandon before Nov 27.
22. **Beehiiv:** keep Pro trial features for now; Brandon re-opts/downgrades himself on the date (supersedes #10's "before Nov 2" action for Grok Bot).
19. **Full context on every platform (Brandon):** LinkedIn is the bar; X and Bluesky carry the same who/what/when/what-it-means as threads (X 2–4 posts ≤280 each, Bluesky 1–3 posts ≤300 each), story-driven hook → open loop → receipt → payoff question/CTA, no overpromising. All 14 days rewritten. Buffer Free allows one scheduled thread per queue, so approved threads wait in Buffer Drafts and are queued one day at a time.

## 2026-10-26 (late night, Buffer)
20. **Singles by default + autonomous Buffer:** Brandon approved the drafts. X/Bluesky are single full-context posts, with threads at most ~2 per channel per week (Oct 28, Nov 4; Nov 8 scorecard). 24 posts scheduled with explicit times, 18 labeled drafts, daily top-up routine (growth/routines/BUFFER-DAILY-TOPUP.md) with no new approval needed for approved posts.

## 2026-10-26/27 — recorded by the Oct 27 nightly
23. **Sponsor pricing NOT approved.** Brandon finds the draft pricing iffy (the bundle can cost more than buying items separately). He wants one clear price sheet with consistent, matching prices everywhere (site, Stripe, docs, newsletter). Nothing new on pricing or promos goes live until he approves it.
24. **BFCM / Founding 12 NOT approved** (supersedes #6 and #21). PR #35 stays draft. Open item: the BFCM banner on (Nov 27 9 AM) / off (Dec 1 9 AM) routines are still enabled; disable or get approval before Nov 27.
25. **Beehiiv:** keep Pro features for now; Brandon downgrades himself around Nov 2 or lets it lapse (confirms #22).
26. **Stripe:** Brandon prefers the dashboard Sponsors view + Stripe's own emails over a payment-watcher routine (confirms #20).
27. **Social runs autonomously:** no daily manual work for Brandon; a weekly plan is queued in Buffer ahead of time so he can see everything there.
28. **Full context everywhere, mostly singles:** every post on every platform carries LinkedIn-level context (hook, who/what/when, what it means for the reader); no vague one-liners, no cheesy self-deprecation, never overpromise. Single posts by default; threads only when the story needs one, story-driven with an ending question/CTA.
29. **Reply sniper paused** (Oct 26) until Brandon turns it back on; picks stay in growth/x/sniper-log.md for a planned initiative.
30. **Reddit names claimed (Oct 26):** r/SkillMaxxAI (mod u/SkillMaxxHQ) and backup u/SkillMaxxAI to block impersonators; u/SkillMaxxHQ stays the main posting account.

## 2026-10-27 — newsletter archive
26. **Every emailed newsletter issue is also published to the site archive** at `/newsletter/issue-N/` and linked from `/newsletter/`. Issue #1 stays archive-only (never emailed). Issue #2 is the first Beehiiv send (Tue Nov 3). Archive pages are **not built** until after send (no `src/newsletter/issue-N.md` → live 404); client-side gates alone are not enough. Runbook: growth/routines/NEWSLETTER-SEND.md.

## 2026-10-27 — pricing display
27. **No struck-through “regular” prices.** Show only founding prices with the line “Founding price, locked for 6 months”. Amounts unchanged.

## 2026-10-27 — Founding 12 capacity
28. **Founding 12 still NOT approved.** Capacity forecast in growth/sponsors/SCALING.md. Recommend: 12-month lock only on selected monthly subs (Featured cap 1, Category ≤5, Bundle cap 1); newsletter 4-pack and one-times not eligible. Free Dec newsletter line undecided. No BFCM social shoutouts. Banner must not say “money still never changes a test result.”

## 2026-10-27 — simplified sponsor model (draft)
29. **Draft only (not live):** Founding = first 10, 6-month lock. Featured excluded from long locks (monthly rotation, price rises with audience). BFCM Nov 27–30: 12-month lock on Category + Newsletter only. Free Dec line undecided. Premium/custom = contact us. No per-plan BFCM cap matrix.

## 2026-10-27 — Brandon approved simplified sponsor model
30. **Approved:** founding = first 10, 6-month lock; Featured month-to-month (no long lock, price may rise); BFCM Nov 27–30: Category+Newsletter 12-month lock; Featured $19 for December (normally $29), one slot FCFS; Premium = contact us; free December newsletter line undecided and **not offered**. Banner without “money still never changes a test result.”


## 2026-10-27 — sponsor outreach, lead routing, social, advertise (recorded by the Oct 28 nightly)
31. **Sponsor outreach starts now** (supersedes #5): Brandon approved outreach and sponsor replies from Oct 27, before newsletter #2 (Nov 3) and with no subscriber minimum. Grok Bot runs it and the follow-ups from skillmaxx@gilventures.ai, using growth/sponsors/PIPELINE.csv and OUTREACH.md, and updates Brandon as it goes.
32. **Outreach volume and channel:** 15–30 contacts a day max. Direct email only to a real public address listed by the company; email ramps from ~10/day up to 30/day to protect the domain. Companies without a public email get the contact form, as many as possible each day. Email addresses are never guessed (bounces hurt domain health).
33. **Lead routing:** booking-only company → find a public email and use that; phone only → log "call only" with the number and tell Brandon so he can call; no email or phone → log its LinkedIn or X and tell Brandon. Every lead is logged in PIPELINE.csv with who they are, contact route, outreach done, data points, notes and next follow-up date.
34. **Bluesky community building:** genuine, no-pitch messages to builders on Bluesky are approved (separate from sponsor outreach).
35. **Trend posts:** standing permission for Grok Bot to create and publish SkillMaxx trend posts on its own, in real time, through Buffer, in the agreed style (full context, no overpromising). Other new posts still follow the weekly-plan approval.
36. **/advertise/ changes approved** (shipped in PR #54): honest audience line, sponsor logo strip (hidden until the first live booking), open-slot counter.
37. **Newsletter:** issue #1 lives only on the site; issue #2 (Tue Nov 3, 2026) is the first emailed issue (confirms #4 and the archive rule).

## 2026-10-28 — content, outreach and LinkedIn (recorded by the Oct 29 nightly)
38. **Blog posts publish without approval** (Brandon, Oct 28) once checked for voice, tone, accuracy and SEO, and aimed at traffic. Blogs/guides are pillar content: social posts give a short take and link back to the full post on the site.
39. **Outreach updates:** a one-line chat update to Brandon for every sponsor outreach email, contact form or reply sent (company, contact route, what was sent), plus a quick tally at the end of each outreach run.
40. **Email pacing (refines #32):** outreach emails are spread naturally through the business day (about 8:30/9 AM–7 PM ET), not one every few minutes, and stay capped by the 10 → 20 → 30/day ramp to protect the 2-week-old domain. Contact-form outreach stays unlimited. (Oct 29 note: background senders must check the full window before every send; see STATUS open issues.)
41. **Every sponsor reply gets a quick, very personal answer**, including "not interested". Decliners get a warm, no-pitch note inviting them to follow SkillMaxx on X (@SkillMaxxAI) and Bluesky (skillmaxx.bsky.social), SkillMaxx follows them back, and a friendly re-approach once SkillMaxx has a bigger following.
42. **LinkedIn comment picks** are posted as the **SkillMaxx AI company page**, not Brandon's personal profile. Every pick reminds him to choose the page in the "Commenting as" picker in the LinkedIn app, or switch to the page first from the profile photo menu.

## 2026-10-29 — unreachable leads (recorded by the Oct 30 nightly)
43. **"Brandon to reach out" list:** every SkillMaxx lead that can't be emailed or reached by form (call-only, social-only, press-only, blocked/unanswerable forms) goes on a running list for Brandon with its route and blocker. It lives in growth/sponsors/PIPELINE.csv (contact_route call-only / x / linkedin, or a blocker in notes) and the owner dashboard Sales pipeline. These leads never stall outreach: Grok Bot keeps sourcing new leads to hit the daily email and form quotas without waiting on Brandon.
44. **Outreach wrap-up routine (Oct 29)** was a one-off; it ran 5:35–5:45 PM ET and is now paused/done.


## 2026-10-30 — Brandon's calls (recorded by the Oct 31 nightly)
45. **Newsletters no longer need Brandon's review.** He approved issues #1 and #2 and trusts Grok Bot to finalize future issues, as long as each adds real developer value with fresh stats. X and Reddit post drafts still need his approval before anything is queued in Buffer; trend posts (#35) and blogs (#38) keep their standing approvals.
46. **Reddit, Hacker News and Product Hunt are Brandon's.** He posts and comments himself from drafts Grok Bot writes, starting with useful comments in subreddits like r/ClaudeAI and r/LocalLLaMA before sharing any links.
47. **Tag the companies and tools we test** in Bluesky and Buffer posts wherever possible.
48. **Bluesky runs fully autonomously:** answer replies (jokes answered wittily, like a person, never mentioning AI), like and reply to relevant builders' posts, follow likely follow-backs and unfollow non-followers after a while, and tag companies we mention. Daily routine "SkillMaxx Bluesky community", 1 PM ET.
49. **Vendor onboarding / "what are you building" emails** that land in the SkillMaxx inbox (e.g. Tavily, WorkOS) get an autonomous reply: a short SkillMaxx intro plus a soft sponsor mention.
50. **"Brandon's queue"** goes at the top of the owner dashboard, refreshed daily, with everything for his human time block: X reply links, LinkedIn picks, Reddit comment drafts, reach-out DMs, weekly video scripts and pending reviews. He plans the cadence with the COO bot.
51. **Real /blog** with in-depth, SEO-friendly posts that carry weight with developers, separate from guides and daily reports (shipped Oct 30, PR #70).
52. **No Google My Business.** SkillMaxx has no physical address or LLC of its own; it operates under Gil Ventures (registered in Florida; use FL in form state fields).
53. **Leads:** skip CockroachDB's support-labeled info@ address; reach Cloudflare and Hugging Face by X DM after Brandon engages a post (drafts in BRANDON-OUTREACH.md), not press@.
54. **Free December newsletter line approved** for the BFCM offer (updates #30). Brandon pinned the X launch post, downgrades Beehiiv himself, and blocks time for human-only tasks (reply sniper links, reach-out list).

## 2026-10-31 — operating notes (recorded by the Nov 1 nightly)
No new owner decisions came in on Oct 31. Operating rules adopted after that day's incidents:
55. **Disk cleanups never touch test deps:** any box cleanup must exclude /workspace/agents (agent CLIs, Node 22, Cursor install) and /workspace/skillmaxx/node_modules + ~/.cache/ms-playwright; the Oct 31 wipe broke every install test and the build.
56. **A pass must mean the check passed:** if an agent's own health check and a follow-up check disagree (e.g. Cursor says `ready` but `list-tools` fails), don't count it as a pass. Fix tracked in STATUS open issues (Cursor MCP pass check); until it ships, site numbers keep the documented `ready` criterion.


## 2026-11-01 — Brandon's daily hand-posting + outreach rules (recorded by the Nov 2 nightly)
57. **Daily hand posting:** Brandon committed to posting by hand every day. Grok Bot builds a daily queue for ~8 AM ET (routine "Brandon's daily SkillMaxx queue") with that day's X replies, Reddit comments and posts, LinkedIn picks and DMs. He's building a matching Gil Growth system with his COO bot, modeled on this one.
58. **Reddit comments are spaced out** across the day: the new u/SkillMaxxHQ account hits Reddit's "try again in 5 minutes" rate limit when comments go out close together.
59. **Reply drafts only after reading the full original post and thread** (X, Reddit, LinkedIn, etc.), never from a screenshot or the latest comment alone.
60. **LinkedIn connection-request notes are short, organic smart questions with no links.** SkillMaxx links (site, X @SkillMaxxAI, Bluesky) go in later messages. LinkedIn outreach from his personal account is relationship-first: open with a question that carries value, mention SkillMaxx briefly, no hard sponsorship pitch in the first message.
61. **Every outreach message asks a sharp question drawn from our own observations** (their README/docs, our test results, gaps we noticed). Never ask what their docs already answer, and never offer to test something we can just test ourselves. Check README/docs before drafting (OUTREACH.md §0b).
62. **Named contacts are verified as currently at the company** from current sources such as the person's own profile, not search snippets or directory sites, before they reach Brandon (OUTREACH.md §0).
63. **Every hand-handled item gets a direct link or the exact in-app search text**, so Brandon goes straight to the spot and pastes.
64. **X DMs only to brands with open inboxes** (closed ones need verification or an X Number). Prefer leads with open DMs, flag unknowns, and give a backup route: Bluesky DM or a LinkedIn message to a named partnerships/marketing person. **No sponsor pitches in public replies.** Grok Bot may send SkillMaxx sponsor DMs on Bluesky itself.
65. **LinkedIn Sales Navigator** (free trial on Brandon's personal account) is an ongoing SkillMaxx lead-gen tool: saved searches, lead lists, alerts; get the most out of the trial (growth/sponsors/SALES-NAV-PLAYBOOK.md, SALES-NAV-LEADS.csv).
66. **Lead routing update (replaces the phone step of #33):** booking-only → find a public email and send there; phone only (usually a general sales line) → find a named partnerships/marketing contact on LinkedIn for Brandon to message instead of calling; neither → log the company's LinkedIn or X for Brandon. Every lead stays logged where he can see it.
67. **X follows ≤15/hour:** Brandon's X got follow-restricted after mass-following. No follow needed before a DM.
68. **CockroachDB + Vercel sales forms approved** for Mon Nov 2 business hours (CockroachDB with Brandon's phone as given in chat, never stored in the repo; Vercel with state FL). One-off routine Nov 2 10:30 AM ET.

## 2026-11-02 — Brandon's calls (recorded by the Nov 3 nightly)
69. **GitHub stays on grandpajackai, anonymously.** grandpajackai is Brandon's personal pseudonymous account and must stay anonymous; the SkillMaxx repo, builds and nightly routines stay there with no migration. A separate free GitHub account for SkillMaxx (signed up with the SkillMaxx business email) is planned for public activity such as opening issues and starring repos.
70. **Grok Bot does the GitHub-side outreach itself** (starring repos, opening issues on projects we tested); Brandon only approves. Non-GitHub platforms still get paste-ready replies for him.
71. **X replies in Brandon's queue are the original post link plus the reply text in a copy block**, never an intent link alone (intent links open as new posts in his X app).
72. **CockroachDB: skip the contact-sales form** (no honest Use Case option); reach them only through X and LinkedIn. Updates #68.

## 2026-11-03 — Brandon's calls (recorded by the Nov 7 nightly)
73. **Grok Bot fully runs Beehiiv**: edits, schedules and publishes newsletters when ready, no approval from Brandon needed (extends #26 and the Oct 30 newsletter trust).
74. **Grok Bot manages both GitHub accounts**: grandpajackai (repo, builds, routines; stays anonymous per #69) and a new free **SkillMaxx GitHub account** (business email; links and description set, no logo avatar yet) used for public activity like opening issues and starring repos. Steps Grok Bot can't do itself go to Brandon as instructions. His first grandpajackai issue comment was blanked to "." and gets redone from the SkillMaxx account.
75. **Bluesky display name is "SkillMaxx AI"** to match X (confirms #9).
76. **Brandon's goal: no pending setup on his side, focus on content.** Grok Bot alerts him whenever sponsor email outreach or another initiative needs his reply.

