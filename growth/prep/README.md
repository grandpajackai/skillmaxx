# Grok-free routine prep (`growth/prep/prep.py`)

Brandon, Nov 18: "anything that doesn't need Grok's judgment should run on his Mac; Grok keeps only judgment work."
`prep.py` does the mechanical half of six Grok routines (fetch, list, count, format) and writes a Markdown brief
plus JSON. The Grok routine reads the brief and does only the judgment step (pick, write, decide, send under its
existing approval rules). No LLM, stdlib only, keyless reads, **never posts, follows, likes, sends or replies**.

| Job | Routine it feeds | Where it runs | When (ET) | Output |
|---|---|---|---|---|
| `queue` | brandon-s-daily-skillmaxx-queue (Mon/Wed/Fri 8:00) | box loop | 7:40 Mon/Wed/Fri | `/home/box/skillmaxx-prep/out/DATE/queue.md` |
| `pipeline` | skillmaxx-sponsor-pipeline-weekly (Mon 9:00) | Mac (in the Monday data PR) + box loop | Mac ~3 AM Mon · box 8:40 Mon | `growth/sponsors/briefs/pipeline-DATE.md` · `/home/box/skillmaxx-prep/out/DATE/pipeline.md` |
| `xradar` | skillmaxx-x-radar (daily 10:00) | box loop | 9:40 daily | `/home/box/skillmaxx-prep/out/DATE/xradar.md` |
| `outreach` | skillmaxx-daily-sponsor-outreach (weekdays 11:00) | box loop (`--zoho`, read-only) | 10:40 Mon–Fri | `/home/box/skillmaxx-prep/out/DATE/outreach.md` |
| `bluesky` | skillmaxx-bluesky-community (Mon/Thu 1:00 PM) | box loop | 12:40 Mon/Thu | `/home/box/skillmaxx-prep/out/DATE/bluesky.md` |
| `recap` | skillmaxx-sunday-recap (Sun 6:00 PM) | Mac (in the Sunday data PR) + box loop | Mac ~3 AM Sun · box 17:40 Sun | `growth/weekly/recap-prep-DATE.md` · `/home/box/skillmaxx-prep/out/DATE/recap.md` |

`/home/box/skillmaxx-prep/out/latest/` always holds the newest copy of each brief. Each brief's second line is
`<!-- prep {"date": ...} -->`; routines treat a brief whose date is not today as stale and fall back.

**Why the daily jobs run on the box, not the Mac:** the Grok routines can only read box files or the repo; Zoho
credentials live on the box; and committing daily scratch fetches (and private mail-scan results) to this public
repo would be noise and a privacy leak. The weekly briefs (repo data only) ride in the Mac's existing data PR.

**What cannot move:** reading X (no free API; scraping X behind a login is off-limits), Reddit (403 from box and
Mac), Stripe and Beehiiv (connectors only), and every pick/draft/send/post decision.

Box loop: `/home/box/skillmaxx-prep/supervise.sh` (not in this repo; no cron/systemd on the box), started by
`ensure-running.sh` from `~/.bashrc` and desktop autostart. It uses its own scratch clone in
`/home/box/skillmaxx-prep/repo` (fetch + reset to origin/master; never committed to or pushed from).
Manual run: `/home/box/skillmaxx-prep/run-now.sh outreach --zoho`.

**Newsletter draft (since Nov 18):** `recap` also writes `newsletter-draft.md`, a no-LLM draft of the next
SkillMaxx Weekly issue in the `src/newsletter/issue-N.md` format (front matter, crumbs, Brandon intro, numbers,
by-agent table, fixed/broke/flaky, links, blog, radar candidates, tip, Tell us, sponsor footer). Real numbers
only; the parts that need writing are `<!-- DRAFT: ... -->` comments. Box: `/home/box/skillmaxx-prep/out/DATE/newsletter-draft.md`.
Mac Sunday data PR: `src/newsletter/issue-N.draft.md`, which eleventy ignores (`*.draft.md` in eleventy.config.js,
plus `permalink: false`), so it is never built, listed or sent. The Sunday recap routine polishes it, renames it to
`issue-N.md` to publish, and saves an unsent Beehiiv draft.

Local check: `python3 testing/test_prep.py` (offline, no Zoho, no network).
