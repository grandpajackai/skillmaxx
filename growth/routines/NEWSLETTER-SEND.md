# Newsletter send + site archive (every Tuesday)

**Rule:** every Beehiiv send also lands in the public archive at `/newsletter/issue-N/`, and on the index at `/newsletter/`. Issue #1 is archive-only (never emailed). Issue #2 is the **first email** (Tue Nov 3, 2026).

Source of truth for paste text: `growth/newsletter/issue-00N-beehiiv.md`.
Archive pages: `src/newsletter/issue-N.md` (collection tag `issues` → listed by `src/newsletter/index.njk`).

## Before send (Mon night / Tue morning)
1. Regenerate the scorecard: `python3 testing/weekly_scorecard.py` and paste fresh numbers into the Beehiiv draft.
2. Brandon reviews the Beehiiv copy.
3. **Do not add `src/newsletter/issue-N.md` until after send.** Keep the draft only under `growth/newsletter/` so `/newsletter/issue-N/` stays 404 (no client-side gate, no premature 200).

## After Beehiiv marks the issue Sent
1. **Publish the archive page**
   - Create `src/newsletter/issue-N.md` from the beehiiv file (same front matter pattern as `issue-1.md`: `permalink: /newsletter/issue-N/`, `tags: [issues]`, `issueDate`, Article JSON-LD).
   - Body must match what was emailed (no silent edits after send).
2. Short branch → PR → CI green → squash-merge.
3. Verify live:
   - https://skillmaxx.gilventures.ai/newsletter/issue-N/ shows the issue (was 404 before this PR)
   - https://skillmaxx.gilventures.ai/newsletter/ lists it
4. Schedule the Buffer “newsletter is out” posts only after this confirm (see BUFFER-DAILY-TOPUP.md Nov 3 gate).
5. Log one line in STATUS.md.

## Why no pre-send page
Client-side date gates still return HTTP 200 and leak draft HTML. Unpublished issues stay out of `src/newsletter/` entirely until the send PR.

## Nightly refresh check
The 2:00 AM nightly (testing/nightly.sh) does not send email. After any Tuesday send, the next nightly (or the send PR) should confirm the latest emailed issue is on `/newsletter/` and that the archive body matches Beehiiv. If it does not, fix in a follow-up PR the same day.
