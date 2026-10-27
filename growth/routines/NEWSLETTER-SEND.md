# Newsletter send + site archive (every Tuesday)

**Rule:** every Beehiiv send also lands in the public archive at `/newsletter/issue-N/`, and on the index at `/newsletter/`. Issue #1 is archive-only (never emailed). Issue #2 is the **first email** (Tue Nov 3, 2026).

Source of truth for paste text: `growth/newsletter/issue-00N-beehiiv.md`.
Archive pages: `src/newsletter/issue-N.md` (collection tag `issues` → listed by `src/newsletter/index.njk`).

## Before send (Mon night / Tue morning)
1. Regenerate the scorecard: `python3 testing/weekly_scorecard.py` and paste fresh numbers into the Beehiiv draft.
2. Brandon reviews the Beehiiv copy.
3. Confirm `src/newsletter/issue-N.md` exists and matches the email body (or create it from the beehiiv file, same structure as issue-1 / issue-2).

## After Beehiiv marks the issue Sent
1. **Publish the archive page**
   - Remove `eleventyExcludeFromCollections: true` (if set).
   - Set `tags: [issues]` so `/newsletter/` lists it.
   - Remove or leave the client date-gate; once the send day has passed the gate is open anyway.
   - Sync body text to what actually went out (no silent edits after send).
2. Short branch → PR → CI green → squash-merge.
3. Verify live:
   - https://skillmaxx.gilventures.ai/newsletter/issue-N/ shows the issue
   - https://skillmaxx.gilventures.ai/newsletter/ lists it
4. Schedule the Buffer “newsletter is out” posts only after this confirm (see BUFFER-DAILY-TOPUP.md Nov 3 gate).
5. Log one line in STATUS.md.

## Date-gate pattern (pre-send)
Same idea as the BFCM banner: a client-side `Date.parse` gate can hide the body until send morning (see `src/newsletter/issue-2.md`, unlocks `2026-11-03T14:00:00Z` = 9:00 AM ET). Prefer also excluding from collections until after send so the archive index does not link early.

## Nightly refresh check
The 2:00 AM nightly (testing/nightly.sh) does not send email. After any Tuesday send, the next nightly (or the send PR) should confirm the latest emailed issue is on `/newsletter/` and that the archive body matches Beehiiv. If it does not, fix in a follow-up PR the same day.
