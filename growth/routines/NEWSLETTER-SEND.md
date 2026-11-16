# Newsletter send + site archive (every Tuesday)

**Rule (since Nov 13, 2026, Brandon):** every issue goes on the public archive at `/newsletter/issue-N/` (and the `/newsletter/` index) as soon as it is final, **even before or without a Beehiiv email**. The archive is the record of what we're doing; the email is extra reach. Issue #1 and #2 are archive-only (#2 was written for Nov 3 but never emailed: the free Beehiiv plan blocks connector edits). Issue #3 (Nov 13) is the first one with paste-ready HTML for a manual Beehiiv send.

**Quick path:** write `growth/newsletter/issue-00N-beehiiv.md` from published numbers only, then
`python3 growth/newsletter/to_site.py N YYYY-MM-DD "desc" "optional archive note"` (makes `src/newsletter/issue-N.md`) and
`python3 growth/newsletter/to_html.py growth/newsletter/issue-00N-beehiiv.md` (makes the paste-ready `.html`). PR, squash-merge, verify the page is 200.

**Brandon's manual Beehiiv send (free plan):** app.beehiiv.com → Posts → open the draft (or New post) → set Title / Subtitle / Preview text from the top of the `.html` file → in the editor, delete the old body, then paste the HTML (open the `.html` in a browser, select all, copy, paste into the editor; or use an HTML snippet block) → Preview → Publish → "Email and web" → Send now (or schedule Tue 9 AM ET). After it sends, tell Grok Bot so the Buffer "newsletter is out" posts get scheduled.

_Older rule, superseded below where it conflicts:_ archive pages were added only after the Beehiiv send.

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
