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
| Newsletter issues | [growth/newsletter/](growth/newsletter/) |
| **Social content strategy + 2-week drafts** | [growth/strategy/CONTENT-STRATEGY.md](growth/strategy/CONTENT-STRATEGY.md), [growth/strategy/DRAFTS-2026-10-27.md](growth/strategy/DRAFTS-2026-10-27.md) (edit `drafts.py`, rerun) |
| Social kits and post banks | [growth/x/](growth/x/), [growth/social/](growth/social/), [growth/profiles/](growth/profiles/), [growth/reddit/](growth/reddit/) |
| Daily X radar | [growth/x-radar/](growth/x-radar/) |
| Weekly scorecard drafts | [growth/weekly/](growth/weekly/) |
| Test pipeline | `testing/` (nightly.sh, run_tests.py, daily_report.py, weekly_scorecard.py) |
| Stripe payment links + clear unit labels | `src/_data/sponsorLinks.json` (amounts unchanged; units spelled out: $19 for 1 issue, $59/mo for 4 issues, bundle = 1 NL + Featured + Category) |
| Sponsor inventory, rotation, scaling | [growth/sponsors/SCALING.md](growth/sponsors/SCALING.md) |
| Sponsor rate locks + promo commitments | [growth/sponsors/PIPELINE.md](growth/sponsors/PIPELINE.md) (pricing + BFCM NOT approved yet) |
| Routine runbooks | [growth/routines/](growth/routines/) |
| Reddit profile pack + posts | [growth/reddit/](growth/reddit/) |
| Daily reports (site) | /reports/latest/, built by `testing/daily_report.py` |

## Routines (Grok Bot, times ET)
| Routine | Schedule | Status (Oct 27, 2:30 AM ET) |
|---|---|---|
| Nightly refresh (fetch, test, report, deploy) | daily 2:00 AM | enabled; last run Oct 27 2:02 AM, ok (806/900) |
| X radar (log: growth/x-radar/) | daily 10:00 AM | enabled |
| Buffer daily top-up ([growth/routines/BUFFER-DAILY-TOPUP.md](growth/routines/BUFFER-DAILY-TOPUP.md)) | daily 10:00 PM | enabled; last run Oct 26 10:06 PM, ok |
| Sunday recap | Sun 6:00 PM | enabled, never run yet |
| SkillMaxx reply sniper X/Bluesky/LinkedIn (log: growth/x/sniper-log.md) | — | **paused since Oct 26** at Brandon's request; picks saved, no replies sent |
| Brandon personal-brand reply sniper | — | paused, never run |
| BFCM banner on | Nov 27, 9:00 AM | enabled ⚠️ BFCM offer NOT approved: disable or get approval before Nov 27 ([growth/routines/BFCM-FOUNDING-12.md](growth/routines/BFCM-FOUNDING-12.md); PR #35 draft) |
| BFCM banner off | Dec 1, 9:00 AM | enabled (same caveat) |
| Sponsor-payment watcher | — | not built: Brandon uses the dashboard Sponsors section + Stripe's own emails |

## Accounts (no secrets here, ever; logins live in the vault)
| Service | Account / ID | Notes |
|---|---|---|
| GitHub | grandpajackai/skillmaxx | Pages deploy from master, branch protection on |
| Domain | skillmaxx.gilventures.ai | |
| Email | skillmaxx@gilventures.ai (Zoho) | on Brandon's phone; FormSubmit target |
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
