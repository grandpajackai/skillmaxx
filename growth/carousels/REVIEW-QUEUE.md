# Carousel review queue — weeks 2026-W48 through 2026-W51

**Created:** 2026-11-20 (America/New_York)  
**Plan:** [`growth/carousels/CONTENT-PLAN.md`](CONTENT-PLAN.md) (box copy: `/workspace/carousels-samples/CONTENT-PLAN-2026-11-20.md`)  
**Nothing in this queue is posted, scheduled, or sent to Buffer / X / any social API.**

Four calendar weeks, core cadence from the plan (Tue news, Wed timely, Fri maxxing, Sun leaderboard). Monday `orgchart` is optional and included as a preview. Thursday/Saturday stay text-first unless a data event or the BFCM window (Fri Nov 27 start) justifies a deck later.

## How to read the folders

Future nights are not in `reports.json` yet. Every results/leaderboard/orgchart/maxxing deck in this queue is a **preview rendered from the 2026-11-20 nightly report** (and week `2026-47` for the leaderboard). Re-run the generator at publish time with that week's data. Do not treat preview numbers as that future week's scorecard.

Wednesday timely news cannot be known ahead of time. W48–W51 Wednesday decks are **template stubs**. A format preview using the 2026-11-20 HN/radar pull is in the v3 sample folders for review of layout and vendor-flag treatment only — it is not that Wednesday's news.

Radar snapshot used for the format preview: `/workspace/carousels-samples/queue-2026-W48..W51/radar-2026-11-20.json` (live `fetch_radar_hn.py` pull on 2026-11-20).

Each unique deck is rendered once (static PNG + animated MP4 at the existing 30fps H.264 settings) in both 1080×1350 and 1080×1920, then linked from every week that uses it, so we did not re-encode the same pixels four times.

Week subfolders `W48/`–`W51/` under this directory contain named symlinks (`tue-news-ig`, `wed-timely-stub-tiktok`, `fri-maxxing-ig`, `sun-leaderboard-ig`, optional `mon-orgchart-ig`, plus `.zip` links) pointing at those unique folders.

### Unique media (shared)

| Deck | Size | Folder | Zip | Best preview stills |
|---|---|---|---|---|
| Orgchart (Mon optional / v3 sample) | 1080×1350 | `/workspace/carousels-samples/v3-animated-orgchart-2026-11-20/` | `…/v3-animated-orgchart-2026-11-20.zip` | `slide-01.png` (hook + org chart), `slide-02.png` (5-agent payoff), `slide-09.png` (newsletter CTA) |
| Orgchart | 1080×1920 TikTok | `/workspace/carousels-samples/v3-animated-orgchart-tiktok-2026-11-20/` | `…/v3-animated-orgchart-tiktok-2026-11-20.zip` | Same slide numbers, taller canvas |
| Maxxing (Fri) | 1080×1350 | `/workspace/carousels-samples/v3-animated-maxxing-2026-11-20/` | `…/v3-animated-maxxing-2026-11-20.zip` | `slide-01.png` (cover), `slide-02.png` (what broke — payoff), `slide-08.png` (CTA) |
| Maxxing | 1080×1920 TikTok | `/workspace/carousels-samples/v3-animated-maxxing-tiktok-2026-11-20/` | `…/v3-animated-maxxing-tiktok-2026-11-20.zip` | Same slide numbers |
| Timely format preview (current radar, not a scheduled week) | 1080×1350 | `/workspace/carousels-samples/v3-animated-timely-2026-11-20/` | `…/v3-animated-timely-2026-11-20.zip` | `slide-01.png` (cover), `slide-03.png` (first story + vendor-source flag), `slide-09.png` (CTA) |
| Timely format preview | 1080×1920 TikTok | `/workspace/carousels-samples/v3-animated-timely-tiktok-2026-11-20/` | `…/v3-animated-timely-tiktok-2026-11-20.zip` | Same slide numbers |
| News (Tue preview) | 1080×1350 | `/workspace/carousels-samples/queue-2026-W48..W51/previews/animated-news-2026-11-20/` | `…/previews/animated-news-2026-11-20.zip` | `slide-01.png` (cover), `slide-02.png` or `slide-03.png` (payoff / broke-fixed), last slide (CTA) |
| News | 1080×1920 TikTok | `/workspace/carousels-samples/queue-2026-W48..W51/previews/animated-news-tiktok-2026-11-20/` | `…/previews/animated-news-tiktok-2026-11-20.zip` | Same |
| Leaderboard (Sun preview) | 1080×1350 | `/workspace/carousels-samples/queue-2026-W48..W51/previews/animated-leaderboard-2026-11-20/` | `…/previews/animated-leaderboard-2026-11-20.zip` | `slide-01.png`, ranking slide, last slide (CTA) |
| Leaderboard | 1080×1920 TikTok | `/workspace/carousels-samples/queue-2026-W48..W51/previews/animated-leaderboard-tiktok-2026-11-20/` | `…/previews/animated-leaderboard-tiktok-2026-11-20.zip` | Same |
| Timely stub (Wed, all four weeks) | 1080×1350 | `/workspace/carousels-samples/queue-2026-W48..W51/previews/v3-animated-timely-stub-2026-11-20/` | `…/previews/v3-animated-timely-stub-2026-11-20.zip` | `slide-01.png` (stub cover), `slide-02.png` (structure), `slide-03.png` (CTA) |
| Timely stub | 1080×1920 TikTok | `/workspace/carousels-samples/queue-2026-W48..W51/previews/v3-animated-timely-stub-tiktok-2026-11-20/` | `…/previews/v3-animated-timely-stub-tiktok-2026-11-20.zip` | Same |

Each folder contains per-slide `slide-NN.png` + `slide-NN.mp4`, plus a stitched `preview.mp4`. Default CTA on every deck is the newsletter (`https://skillmaxx.gilventures.ai/newsletter/`).

## Week calendar

Pillars follow `growth/strategy/CONTENT-STRATEGY.md`. Hook formulas are templates; preview wording uses the 2026-11-20 report and must be regenerated.

### 2026-W48 — Mon Nov 23 – Sun Nov 29

BFCM / Founding 12 window starts Fri Nov 27 (DECISIONS #6). Optional Saturday seasonal deck is not rendered here.

| Day | Date | Pillar | Deck | Hook (template, preview data) | Paths |
|---|---|---|---|---|---|
| Mon (optional) | Nov 23 | 2 Know-how | orgchart | “{cc_pass} skills that actually install in Claude Code” — preview: 340 | IG + TikTok orgchart zips above |
| Tue | Nov 24 | 1 Results, 3 Report | news | “{pass} clean installs out of {tested} judged last night” — preview: 906 / 1,050 | news zips in `previews/` |
| Wed | Nov 25 | 5 News, 6 Leaders | timely **stub** | Render at publish from a fresh HN pull | timely-stub zips in `previews/` |
| Fri | Nov 27 | 2 Know-how, 1 Results | maxxing | “Stop installing the {broken} add-ons that already failed tonight’s sandbox” — preview: 140 | maxxing zips above |
| Sun | Nov 29 | 3 Report/newsletter | leaderboard | Week scorecard from that week’s `weeks.json` (preview still shows 2026-47) | leaderboard zips in `previews/` |

### 2026-W49 — Mon Nov 30 – Sun Dec 6

Same deck types, same shared preview media, same stub for Wednesday. Re-render with W49 nightly data at publish.

| Day | Date | Pillar | Deck | Paths |
|---|---|---|---|---|
| Mon (optional) | Nov 30 | 2 | orgchart preview | shared orgchart zips |
| Tue | Dec 1 | 1, 3 | news preview | shared news zips |
| Wed | Dec 2 | 5, 6 | timely **stub** | shared timely-stub zips |
| Fri | Dec 4 | 2, 1 | maxxing preview | shared maxxing zips |
| Sun | Dec 6 | 3 | leaderboard preview | shared leaderboard zips |

### 2026-W50 — Mon Dec 7 – Sun Dec 13

| Day | Date | Pillar | Deck | Paths |
|---|---|---|---|---|
| Mon (optional) | Dec 7 | 2 | orgchart preview | shared orgchart zips |
| Tue | Dec 8 | 1, 3 | news preview | shared news zips |
| Wed | Dec 9 | 5, 6 | timely **stub** | shared timely-stub zips |
| Fri | Dec 11 | 2, 1 | maxxing preview | shared maxxing zips |
| Sun | Dec 13 | 3 | leaderboard preview | shared leaderboard zips |

### 2026-W51 — Mon Dec 14 – Sun Dec 20

Subscriber baseline is due around Dec 18 (STATUS / DECISIONS). That is a measurement milestone, not a reason to invent a number for a slide.

| Day | Date | Pillar | Deck | Paths |
|---|---|---|---|---|
| Mon (optional) | Dec 14 | 2 | orgchart preview | shared orgchart zips |
| Tue | Dec 15 | 1, 3 | news preview | shared news zips |
| Wed | Dec 16 | 5, 6 | timely **stub** | shared timely-stub zips |
| Fri | Dec 18 | 2, 1 | maxxing preview | shared maxxing zips |
| Sun | Dec 20 | 3 | leaderboard preview | shared leaderboard zips |

## Re-render at publish time

From the SkillMaxx repo:

```bash
python3 growth/carousels/generate.py --format news --date YYYY-MM-DD --size both --animate --zip --out /workspace/carousels-samples/queue-2026-W48..W51/Wxx
python3 growth/carousels/generate.py --format timely --size both --animate --zip --out /workspace/carousels-samples/queue-2026-W48..W51/Wxx
python3 growth/carousels/generate.py --format maxxing --v3 --date YYYY-MM-DD --size both --animate --zip --out /workspace/carousels-samples/queue-2026-W48..W51/Wxx
python3 growth/carousels/generate.py --format leaderboard --date YYYY-MM-DD --size both --animate --zip --out /workspace/carousels-samples/queue-2026-W48..W51/Wxx
```

`--date` is the nightly report to use (Tue/Fri: that morning's night; Sun: the week's last run). Timely has no `--date` dependency for stories; it always pulls HN live unless `--radar-json` is passed. Do not pass an old radar file when publishing.

CTA remains the newsletter until Brandon chooses otherwise (`--cta keyword|hybrid` is a placeholder only).
