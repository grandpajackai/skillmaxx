# One-off routine: BFCM "Founding 12" banner (routine-ready)

Approved by Brandon 2026-10-26. Final banner copy goes to Brandon for OK ~Nov 23; do not merge without that OK.

## Run 1 — Fri Nov 27, 2026, 12:05 AM ET (banner up)
1. Confirm Brandon approved the final copy (STATUS.md / DECISIONS.md). If not: stop, ping him, do nothing.
2. Rebase the banner PR (branch `grokbot/bfcm-founding-12-banner`) on master, apply the approved copy, wait for CI green, squash-merge.
3. Check https://skillmaxx.gilventures.ai/advertise/ shows the banner (cache-bust with ?v=).
4. Log in STATUS.md. Social posts only if Brandon approved them in Buffer.

## Run 2 — Tue Dec 1, 2026, 12:05 AM ET (banner down)
1. New branch from master, set `bfcm.active` to `false` in `src/_data/site.js` (or revert the banner commit), PR, CI green, squash-merge.
2. Check /advertise/ no longer shows it.
3. In growth/sponsors/PIPELINE.md, confirm every Nov 27–30 booking has "Founding 12", a 12-month lock date, and a December shoutout issue assigned. Report the list to Brandon.

No Stripe changes in either run.
