# One-off routine: BFCM "Founding 12" banner (routine-ready — offer NOT approved)

**Do nothing until Brandon approves (1) capacity / which plans get the 12-month lock, (2) the offer shape, (3) final banner copy.** Free December newsletter line is **undecided**. No BFCM social shoutouts in this offer.

Final banner copy OK ~Nov 23; do not merge PR #35 without that OK. Banner text must **not** include "money still never changes a test result."

## Run 1 — Fri Nov 27, 2026, 9:00 AM ET (banner up; runbook gate also allows 12:05 AM ET)
1. Confirm Brandon approved capacity + offer + final copy (STATUS.md / DECISIONS.md). If not: stop, ping him, do nothing.
2. Rebase the banner PR (PR #35, branch `grokbot/bfcm-founding-12-banner`) on master, apply the approved copy (no money/test-result line; no Dec line unless decided), wait for CI green, squash-merge.
3. Check https://skillmaxx.gilventures.ai/advertise/ shows the banner (cache-bust with ?v=).
4. Log in STATUS.md. **No** BFCM X/Bluesky/LinkedIn/Buffer shoutout posts unless separately approved later.

## Run 2 — Mon Dec 1, 2026, 9:00 AM ET (banner down)
1. Client date gate hides the banner at Dec 1 12:00 AM ET. Clean up: PR removing the `#bfcm` block from src/advertise.njk, CI green, squash-merge.
2. Check /advertise/ no longer shows it.
3. In growth/sponsors/PIPELINE.md, confirm every Nov 27–30 booking has lock length (6 vs 12), product eligibility, and — only if approved — a December shoutout issue. Report the list to Brandon.

No Stripe changes in either run.
