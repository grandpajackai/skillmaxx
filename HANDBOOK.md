# SkillMaxx Handbook (start here)

One page to catch up. Site: https://skillmaxx.gilventures.ai · Repo: grandpajackai/skillmaxx · Owner: Brandon Gil · Operator: Grok Bot ("Side Hustle CEO").

## Where things live
| What | File |
|---|---|
| Current state, session log, pending items | [STATUS.md](STATUS.md) |
| Every approved decision | [growth/DECISIONS.md](growth/DECISIONS.md) |
| How to collaborate (branch, PR, CI, squash-merge) | [COLLABORATING.md](COLLABORATING.md) |
| Roadmap | [PLAN.md](PLAN.md) |
| Brand voice | [growth/VOICE.md](growth/VOICE.md) |
| Review pack (Oct 26) | [growth/REVIEW-PACK-2026-10-26.md](growth/REVIEW-PACK-2026-10-26.md) |
| Channels ranked | [growth/CHANNELS.md](growth/CHANNELS.md) |
| Sponsors: pricing, playbook, pipeline, BFCM | [growth/SPONSORS.md](growth/SPONSORS.md), [growth/sponsors/](growth/sponsors/) |
| Newsletter drafts (Beehiiv paste) | [growth/newsletter/](growth/newsletter/) |
| Newsletter **site archive** | `src/newsletter/` → /newsletter/ and /newsletter/issue-N/ (publish after every Beehiiv send: [growth/routines/NEWSLETTER-SEND.md](growth/routines/NEWSLETTER-SEND.md)) |
| **Social content strategy + 2-week drafts** | [growth/strategy/CONTENT-STRATEGY.md](growth/strategy/CONTENT-STRATEGY.md), [growth/strategy/DRAFTS-2026-10-27.md](growth/strategy/DRAFTS-2026-10-27.md) (edit `drafts.py`, rerun) |
| Social kits and post banks | [growth/x/](growth/x/), [growth/social/](growth/social/), [growth/profiles/](growth/profiles/), [growth/reddit/](growth/reddit/) |
| Daily X radar | [growth/x-radar/](growth/x-radar/) |
| Weekly scorecard drafts | [growth/weekly/](growth/weekly/) |
| Test pipeline | `testing/` (nightly.sh, mac_nightly.sh, run_tests.py, daily_report.py, weekly_scorecard.py, freshness.py) |
| Stripe payment links + clear unit labels | `src/_data/sponsorLinks.json` (founding price, locked for 6 months; units spelled out; no struck-through regulars) |
| Sponsor inventory, rotation, scaling | [growth/sponsors/SCALING.md](growth/sponsors/SCALING.md) |
| Sponsor leads log (who, route, outreach, follow-up) | [growth/sponsors/PIPELINE.csv](growth/sponsors/PIPELINE.csv), templates [growth/sponsors/OUTREACH.md](growth/sponsors/OUTREACH.md), sent logs `growth/outreach/sent/` |
| Sponsor rate locks + promo commitments | [growth/sponsors/PIPELINE.md](growth/sponsors/PIPELINE.md) (BFCM Founding 12 approved 2026-10-27; see growth/sponsors/BFCM.md) |
| Routine runbooks | [growth/routines/](growth/routines/) |
| Reddit profile pack + posts | [growth/reddit/](growth/reddit/) |
| Daily reports (site) | /reports/latest/, built by `testing/daily_report.py` |
| "Brandon to reach out" list (call/social/press-only, blocked forms) | [growth/sponsors/PIPELINE.csv](growth/sponsors/PIPELINE.csv) (non-email/form routes + blocker in notes) and the owner dashboard Sales pipeline (DECISIONS #43) |
| npm packages dropped as deprecated | `data/npm_excluded.json` (read by `build_data.py`) |
| Daily X radar notes + newsletter idea log | [growth/x-radar/](growth/x-radar/) (incl. `*-brandons-queue.md` fallback when the dashboard canvas can't be edited), [growth/newsletter/issue-002-notes.md](growth/newsletter/issue-002-notes.md), [growth/newsletter/issue-003-notes.md](growth/newsletter/issue-003-notes.md) |
| Brandon's reach-out list (X DMs, calls, blocked forms) | [growth/sponsors/BRANDON-OUTREACH.md](growth/sponsors/BRANDON-OUTREACH.md) |
| Bluesky community log (pending replies, follows) | [growth/bluesky/](growth/bluesky/) |
| Show HN / Product Hunt launch drafts (Brandon posts) | [growth/launch/LAUNCH-DRAFTS.md](growth/launch/LAUNCH-DRAFTS.md) |
| Blog (in-depth posts) | `src/blog/` → /blog/ |
| LinkedIn connection notes + Sales Navigator lead-gen (Brandon's trial) | [growth/sponsors/LINKEDIN-NOTES-2026-11-01.md](growth/sponsors/LINKEDIN-NOTES-2026-11-01.md), [growth/sponsors/SALES-NAV-PLAYBOOK.md](growth/sponsors/SALES-NAV-PLAYBOOK.md), [growth/sponsors/SALES-NAV-LEADS.csv](growth/sponsors/SALES-NAV-LEADS.csv) |
| Outreach rules (verify named contacts, smart questions, DM-open column) | [growth/sponsors/OUTREACH.md](growth/sponsors/OUTREACH.md) §0/§0b, DECISIONS #57–68 |
| Newsletter subscribe CTA rule | [growth/NEWSLETTER-CTA-RULE.md](growth/NEWSLETTER-CTA-RULE.md) |

## Routines (Grok Bot, times ET)
| Routine | Schedule | Status (Nov 11, ~4:15 AM ET) |
|---|---|---|
| Nightly refresh (Mac runs tests 2 AM; Grok Bot validates Mac outputs, refreshes catalog, QA, publishes) | daily ~4:00 AM ET | enabled; Nov 9–11: Mac runs (727, 790, 790 /1,070) rejected (Grok Build marketplace-scan failures + agent versions differ from published series), not published, retest needed; latest public report Nov 8 |
| **Brandon's daily SkillMaxx queue** (X replies as post link + copy block, Reddit comments/posts, LinkedIn picks, DMs due that day; direct link or exact search text per item; DECISIONS #57–63, #71) | Mon/Wed/Fri 8:00 AM | enabled; last run Nov 9 ok (queue in growth/x-radar/2026-11-09-brandons-queue.md) |
| X radar (log: growth/x-radar/) | daily 10:00 AM | enabled; Nov 10: ok (5 reply opportunities, no trend post) |
| Post check (Buffer sent / errors) | daily 10:30 AM | **paused** (last run Nov 4 failed) |
| Daily sponsor outreach (PIPELINE.csv, OUTREACH.md; DECISIONS #31–33, #39–41, #43, #61–66) | weekdays 11:00 AM | enabled; Nov 10: unattended run sent 0 (box SMTP blocked); Brandon then approved the 23 prepared emails for attended Zoho webmail sends (Sourcegraph, 42Crunch, Dash0 day-7 follow-ups sent 1:10–1:13 PM ET). Every follow-up is checked for replies (incl. Spam), duplicates and sequence position first (DECISIONS #79) |
| SkillMaxx Vercel + CockroachDB forms (DECISIONS #68, #72) | Mon Nov 2, 10:30 AM | done, paused (Vercel submitted; CockroachDB form skipped, X/LinkedIn only) |
| Sponsor pipeline weekly ([growth/routines/SPONSOR-PIPELINE-WEEKLY.md](growth/routines/SPONSOR-PIPELINE-WEEKLY.md)) | Mon 9:00 AM | enabled; last run Nov 9 (due list + status; no sends possible) |
| Newsletter #2 finalize + schedule (refresh scorecard, swap "(refresh)" parts, schedule in Beehiiv) | Tue Nov 3, ~2:45 AM | one-off, ran, now paused; issue #2 still a Beehiiv draft (post_d4f7cc7e), body needs editor paste (see STATUS open issues) |
| Newsletter send + archive ([growth/routines/NEWSLETTER-SEND.md](growth/routines/NEWSLETTER-SEND.md)) | Tue after Beehiiv send | runbook ready; first email = issue #2 (not yet sent; issue #1 is site-only) |
| SkillMaxx Reddit post reminders (Nov 4 r/SideProject, Nov 5 r/mcp, Nov 6 r/cursor, Nov 9 r/ClaudeAI) | Nov 4/5/6/9, 9:00 AM | enabled; all four dates ran (Nov 6 failed on usage), schedule finished. Brandon posts (DECISIONS #46) |
| SkillMaxx HN + Product Hunt launch reminder ([growth/launch/LAUNCH-DRAFTS.md](growth/launch/LAUNCH-DRAFTS.md)) | Tue Nov 10, 9:00 AM | ran Nov 10, now paused: judged not ready; proposed HN Wed Nov 18 ~9 AM ET and PH Tue Dec 1 12:01 AM PT if fixes land by Nov 16 (proposal, not yet approved) |
| Buffer daily top-up ([growth/routines/BUFFER-DAILY-TOPUP.md](growth/routines/BUFFER-DAILY-TOPUP.md)) | daily 10:00 PM | enabled; Nov 10: ok (Nov 12 guide promos scheduled); approved posts run out after Nov 12, next week needs drafts + Brandon review |
| Bluesky community (replies, likes, follows, tagging; DECISIONS #48) | Mon + Thu 1:00 PM | enabled; Nov 9: ok (12 followers / 27 following); follows logged in growth/bluesky/FOLLOWS.md |
| Sunday recap | Sun 6:00 PM | enabled; last run Nov 8 ok |
| Outreach wrap-up | Oct 29, 5:45 PM; Oct 30, ~5 PM | paused (one-off, done) |
| SkillMaxx reply sniper X/Bluesky/LinkedIn (log: growth/x/sniper-log.md) | — | **paused** at Brandon's request (his daily queue covers replies now); LinkedIn picks go out as the SkillMaxx AI page (DECISIONS #42) |
| Brandon personal-brand reply sniper | — | paused |
| BFCM banner on | Nov 27, 9:00 AM | enabled; offer approved Oct 27 (DECISIONS #30) ([growth/routines/BFCM-FOUNDING-12.md](growth/routines/BFCM-FOUNDING-12.md)) |
| BFCM banner off | Dec 1, 9:00 AM | enabled |
| Trend posts (Buffer) | as news breaks | standing permission (DECISIONS #35) |
| Blog/guide posts | as written | publish without approval after voice/tone/accuracy/SEO check; socials give a short take and link back (DECISIONS #38) |
| Sponsor-payment watcher | — | not built: Brandon uses the dashboard Sponsors section + Stripe's own emails |

## Accounts (no secrets here, ever; logins live in the vault)
| Service | Account / ID | Notes |
|---|---|---|
| GitHub | grandpajackai/skillmaxx | Brandon's pseudonymous personal account, keep anonymous (DECISIONS #69); Pages deploy from master, branch protection on. Separate SkillMaxx GitHub account (business email) planned for public issues/stars |
| GitHub (SkillMaxx) | free SkillMaxx account, business email | public activity (issues, stars); links + description set, no logo avatar yet (DECISIONS #74) |
| Domain | skillmaxx.gilventures.ai | |
| Email | skillmaxx@gilventures.ai (Zoho) | on Brandon's phone; mailto target for /submit/ and /advertise/; sponsor outreach sender via SMTP (SPF + DKIM verified Oct 27; SMTP currently unreachable from the box); inbox read through box-browser webmail (IMAP/POP blocked from box) |
| FormSubmit | (removed from site) | activated Oct 26; dropped 2026-11-07 (PR #88) after the Cloudflare 522 outage. /submit/ and /advertise/ now use a prefilled mailto to skillmaxx@gilventures.ai + copy details (and a GitHub issue on /submit/). formsubmit.co returned 200 on Nov 8; we did not switch back |
| Stripe | Gil Ventures LLC (live, acct …HnNCwlg7U0) | connector still on the wrong account ("Linkedin") as of Nov 11, needs re-auth to Gil Ventures LLC; 8 payment links, portal bpc_1UUuTKHnNCwlg7U0D15J5OZG; no payouts/refunds/settings without Brandon |
| Beehiiv | SkillMaxx Weekly | Grok Bot runs it fully (DECISIONS #73); issue #2 still a draft (post_d4f7cc7e), body needs editor paste; 5 active subs (Nov 6) |
| Buffer | org 6adfb3f8d2cea8f4b234c15b | X 6adfb5c92f1f5ed648deaa83, Bluesky 6adfbe402f1f5ed648def519, LinkedIn page 6adfc4f12f1f5ed648df8e37; posts use explicit times, 2-week plan queued, daily top-up |
| X | SkillMaxx account (@SkillMaxxAI) | posts via Buffer; replies + DMs by Brandon from his daily queue; DMs only to open inboxes; ≤15 follows/hour (DECISIONS #64, #67) |
| Bluesky | SkillMaxx AI | API; replies need Brandon's OK |
| LinkedIn | company page "SkillMaxx AI" | via Buffer |
| LinkedIn (Brandon personal) + Sales Navigator free trial | Brandon's own profile | connection notes/messages sent by Brandon only; Sales Nav used for SkillMaxx lead lists (DECISIONS #60, #65) |
| Reddit | u/SkillMaxxHQ (main posting account); r/SkillMaxxAI (created Oct 26, mod SkillMaxxHQ); u/SkillMaxxAI (backup, anti-impersonation) | logins in Brandon's vault; profile pack drafts in growth/reddit/; new account is rate-limited, so comments are spaced out (DECISIONS #58) |
| Owner dashboard | Grok Bot canvas d70f3b85-34d9-4642-b1a1-ff1f64a40b22 | Sponsors section (Stripe snapshot at refresh), review queue, sales pipeline |

## Standing rules
- **Newsletter CTA (X radar, Bluesky community, Buffer top-up):** roughly 1 in 3 new trend/Bluesky posts end with the newsletter link https://skillmaxxs-newsletter.beehiiv.com/subscribe. New posts only; never edit approved X copy; never in replies. Full rule: growth/NEWSLETTER-CTA-RULE.md.
$0 budget · no secrets in chat or repo · Brandon approves posts once (weekly plan), then routines queue approved posts in Buffer without daily asks · nothing on pricing/promos goes live without Brandon's approval · only SkillMaxx accounts · log every session in STATUS.md.

**Outreach sender lesson (Oct 30):** the background email sender died silently mid-batch (after 8 of 10, log ended on "next in 28m20s", no process left), and its per-send PIPELINE.csv writes were lost from the working copy. So: (1) check the sender is still alive mid-afternoon (`pgrep -f send_MMDD.py` + tail the log) and again before 5 PM ET; if it's dead, don't re-run it (it refuses once results have 'sent' entries anyway), roll the unsent to the next weekday batch; (2) commit PIPELINE.csv + the results JSON the same day, and treat `growth/outreach/sent/*-email-results.json` as the source of truth for what went out.

