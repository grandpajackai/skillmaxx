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

