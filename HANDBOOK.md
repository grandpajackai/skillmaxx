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
| Test pipeline | `testing/` (nightly.sh, run_tests.py, daily_report.py, weekly_scorecard.py) |
| Stripe payment links + clear unit labels | `src/_data/sponsorLinks.json` (founding price, locked for 6 months; units spelled out; no struck-through regulars) |
| Sponsor inventory, rotation, scaling | [growth/sponsors/SCALING.md](growth/sponsors/SCALING.md) |
| Sponsor leads log (who, route, outreach, follow-up) | [growth/sponsors/PIPELINE.csv](growth/sponsors/PIPELINE.csv), templates [growth/sponsors/OUTREACH.md](growth/sponsors/OUTREACH.md), sent logs `growth/outreach/sent/` |
| Sponsor rate locks + promo commitments | [growth/sponsors/PIPELINE.md](growth/sponsors/PIPELINE.md) (BFCM Founding 12 approved 2026-10-27; see growth/sponsors/BFCM.md) |
| Routine runbooks | [growth/routines/](growth/routines/) |
| Reddit profile pack + posts | [growth/reddit/](growth/reddit/) |
| Daily reports (site) | /reports/latest/, built by `testing/daily_report.py` |

## Routines (Grok Bot, times ET)
| Routine | Schedule | Status (Oct 28, 2:45 AM ET) |
|---|---|---|
| Nightly refresh (fetch, test, report, deploy) | daily 2:00 AM | enabled; last run Oct 28 ok (792/900). After a Tuesday send, confirm /newsletter/ archive matches the emailed issue (see NEWSLETTER-SEND.md) |
| X radar (log: growth/x-radar/) | daily 10:00 AM | enabled |
| Post check (Buffer sent / errors) | daily 10:30 AM | enabled; last run Oct 27 10:37 AM, ok |
| Daily sponsor outreach (PIPELINE.csv, OUTREACH.md; DECISIONS #31–33) | weekdays 11:00 AM | enabled; 15–30/day max, email ramp ~10→30/day, forms at full pace, never guess emails |
| Sponsor pipeline weekly ([growth/routines/SPONSOR-PIPELINE-WEEKLY.md](growth/routines/SPONSOR-PIPELINE-WEEKLY.md)) | Mon 9:00 AM | enabled |
| Buffer daily top-up ([growth/routines/BUFFER-DAILY-TOPUP.md](growth/routines/BUFFER-DAILY-TOPUP.md)) | daily 10:00 PM | enabled; last run Oct 27 10:10 PM, ok |
| Newsletter send + archive ([growth/routines/NEWSLETTER-SEND.md](growth/routines/NEWSLETTER-SEND.md)) | Tue after Beehiiv send | runbook ready; first email = issue #2 on Nov 3 |
| Sunday recap | Sun 6:00 PM | enabled, never run yet |
| SkillMaxx reply sniper X/Bluesky/LinkedIn (log: growth/x/sniper-log.md) | — | **paused since Oct 26** at Brandon's request; picks saved, no replies sent |
| Brandon personal-brand reply sniper | — | paused, never run |
| BFCM banner on | Nov 27, 9:00 AM | enabled; offer approved Oct 27 (DECISIONS #30) ([growth/routines/BFCM-FOUNDING-12.md](growth/routines/BFCM-FOUNDING-12.md)) |
| BFCM banner off | Dec 1, 9:00 AM | enabled |
| Trend posts (Buffer) | as news breaks | standing permission (DECISIONS #35) |
| Sponsor-payment watcher | — | not built: Brandon uses the dashboard Sponsors section + Stripe's own emails |

## Accounts (no secrets here, ever; logins live in the vault)
| Service | Account / ID | Notes |
|---|---|---|
| GitHub | grandpajackai/skillmaxx | Pages deploy from master, branch protection on |
| Domain | skillmaxx.gilventures.ai | |
| Email | skillmaxx@gilventures.ai (Zoho) | on Brandon's phone; FormSubmit target; sponsor outreach sender (SPF + DKIM verified Oct 27) |
| FormSubmit | skillmaxx@gilventures.ai | activated Oct 26; autoresponse on /advertise/, /submit/ |
| Stripe | Gil Ventures LLC (live, acct …HnNCwlg7U0) | 8 payment links, portal bpc_1UUuTKHnNCwlg7U0D15J5OZG; no payouts/refunds/settings without Brandon |
| Beehiiv | SkillMaxx Weekly | Pro features kept; Brandon downgrades himself ~Nov 2 |
| Buffer | org 6adfb3f8d2cea8f4b234c15b | X 6adfb5c92f1f5ed648deaa83, Bluesky 6adfbe402f1f5ed648def519, LinkedIn page 6adfc4f12f1f5ed648df8e37; posts use explicit times, 2-week plan queued, daily top-up |
| X | SkillMaxx account | posts via Buffer, replies via one-tap links |
| Bluesky | SkillMaxx AI | API; replies need Brandon's OK |
| LinkedIn | company page "SkillMaxx AI" | via Buffer |
| Reddit | u/SkillMaxxHQ (main posting account); r/SkillMaxxAI (created Oct 26, mod SkillMaxxHQ); u/SkillMaxxAI (backup, anti-impersonation) | logins in Brandon's vault; profile pack drafts in growth/reddit/ |
| Owner dashboard | Grok Bot canvas d70f3b85-34d9-4642-b1a1-ff1f64a40b22 | has a Sponsors section (Stripe snapshot at refresh) |

## Standing rules
$0 budget · no secrets in chat or repo · Brandon approves posts once (weekly plan), then routines queue approved posts in Buffer without daily asks · nothing on pricing/promos goes live without Brandon's approval · only SkillMaxx accounts · log every session in STATUS.md.
