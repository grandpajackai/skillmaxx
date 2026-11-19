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

**Newsletter (since Nov 18, evening):** the Mac Sunday data PR now publishes the real issue itself:
`growth/scripts/newsletter_auto.py` writes `src/newsletter/issue-N.md` (permalink `/newsletter/issue-N/`, `tags: issues`,
same format as issues 1-3, clean copy with no placeholders, one issue per Mon-Sun week, never overwrites). When that
issue exists, `recap` writes **no** draft and its brief says "issue #N already published" (optional Grok polish =
edit that file). Only if the auto issue is missing does `recap` still write the fallback `newsletter-draft.md`
(box) / `src/newsletter/issue-N.draft.md` (Mac PR; never built: `*.draft.md` is ignored by eleventy). The recap
brief also says whether the Sunday post `/blog/week-YYYY-WW/` exists: the Grok recap links it and never writes a
second Sunday post. The email send stays held (growth/routines/NEWSLETTER-SEND.md).

Local check: `python3 testing/test_prep.py` (offline, no Zoho, no network).
