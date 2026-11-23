# Buffer daily top-up (Grok Bot routine)

Routine id: `skillmaxx-buffer-daily-top-up`. Prompt name: **SkillMaxx Buffer daily top-up**.

**Updated 2026-11-23:** The box Bluesky poster is live. Do **not** `create_post` to Bluesky channel `6adfbe402f1f5ed648def519`. Enqueue those texts with `python3 growth/scripts/buffer_weekly.py --repo-queue` and open a small PR so the box clone of `origin/master` picks them up. Do not rely on the Mac Sunday-publish local overlay — the box cannot see the Mac home directory. The direct poster is `growth/social/bluesky_post.py` — see `growth/social/BLUESKY.md`. X and LinkedIn are unchanged (Buffer connector). Instagram `@skillmaxxai` was permanently disabled on 2026-11-23; do not connect or schedule Instagram. See `growth/carousels/INSTAGRAM-SETUP.md`. Scheduled Buffer Bluesky copies of the current queue were deleted on 2026-11-23; leave the stale Nov 3 draft (`6adfee163bff354cec696067`) alone, and do not disconnect the channel from this routine.

Goal: the 2-week calendar runs itself. Brandon approved the posts on 2026-10-26, so moving an approved draft into the queue needs **no new approval**. Bluesky *replies* still need approval (separate rule).

**When:** every day at 10:00 PM ET (the live routine time; this used to say 8:00 AM).
**Where:** Buffer org `6adfb3f8d2cea8f4b234c15b`. Channels still on Buffer: X `6adfb5c92f1f5ed648deaa83`, LinkedIn `6adfc4f12f1f5ed648df8e37`. Bluesky `6adfbe402f1f5ed648def519` stays connected only until it is disconnected in the browser (do not schedule new Bluesky posts here).
**Source of truth for text:** `growth/strategy/drafts.py` → `drafts-2026-10-27.json`.

## Free-plan limits
- At most 10 scheduled posts per channel. Slots free up as posts publish.
- At most 1 scheduled **thread** per channel. Drafts are unlimited.
- There's no first-comment scheduling, and the API can't set posting schedules. Every post uses `mode: customScheduled` with an explicit `dueAt`. Use `-04:00` before Nov 1 and `-05:00` from Nov 1 (EST).

## Draft label convention
Each draft not yet ready to schedule starts with one label line, followed by a blank line:
`[PLANNED <Day Mon D> <time> ET | <reason: REFRESH x / fill placeholders / newsletter gate / THREAD (n)> | remove this line ...]`
Buffer keeps the draft's `dueAt` at the planned time.

## Images
Buffer only takes images from public URLs. To add an image: put the PNG/JPG in `src/assets/social/`, then open a PR, wait for CI to pass and squash-merge. Check it's live (`curl -I https://skillmaxx.gilventures.ai/assets/social/<file>` should return 200 with an image/* type). Then attach it with `assets: [{image: {url, metadata: {altText}}}]`. Alt text is always required. When editing a post that already has an image, carry its assets forward. Live now: `pin-chart.png` (Oct 27 X + LinkedIn). Carousel decks live under `src/assets/social/carousels/<date-slug>/`.

## Carousels (1–3 per week)
Schedule **1–3 carousels a week** across X and LinkedIn only. Instagram `@skillmaxxai` was permanently disabled by Meta on 2026-11-23 (no further review). Do not schedule Instagram posts. Reuse animated v3 MP4s as short video posts. A new Instagram account is Brandon's call. Lead with value or practical tips, not failure stories (Brandon, 2026-11-23). One reader, one tool per carousel; rotate Claude Code, Cursor, and Codex across the week (plus Grok Build or Pi when relevant) and include at least one "works anywhere" tip post a week. Track coverage in `growth/carousels/CONTENT-PLAN.md`. Ground every deck in real SkillMaxx knowledge or committed nightly data; any number cited must come from the repo. Commit 1080×1080 (or 1080×1350) PNGs under `src/assets/social/carousels/<date-slug>/`, squash-merge, then `create_post` with public site URLs after deploy (or GitHub raw URLs on `master`). LinkedIn: all slides as a multi-image post, or one PDF document. X: a trimmed set of up to 4 images. Never schedule carousels on the Bluesky Buffer channel. Editorial templates: `growth/carousels/CONTENT-PLAN.md`. Instagram remains disabled unless Brandon later approves a new account: `growth/carousels/INSTAGRAM-SETUP.md`.

## Bluesky (not Buffer)
On every run, including Sunday: do **not** call `create_post`, `edit_post`, or otherwise schedule anything on Bluesky channel `6adfbe402f1f5ed648def519`. If the next week's Mon/Wed/Fri 7:30 PM ET scorecard posts are not already in `growth/social/bluesky-queue.json`, run `python3 growth/scripts/buffer_weekly.py --repo-queue` and open a PR. Skip Bluesky entirely when listing or topping up Buffer channels.

## Steps
1. `list_posts` for X and LinkedIn only (status scheduled and draft). Check for duplicates: if a scheduled post's text (with the label stripped) matches a draft's text, delete nothing and skip that draft. Log it.
2. Pick the drafts whose planned time is within the next 48 hours.
3. Gates. A draft is skipped and stays a draft if any of these is true:
   - **REFRESH:** re-read `data/reports.json` (latest night) and `scripts/weekly_scorecard.py` output, then update the numbers in the text. If the claim no longer holds (e.g. Superpowers isn't clean in 4 agents anymore, or the flaky count changed meaning), rewrite it from the same angle with true numbers, keeping the length limits (X ≤280 with URLs = 23, Bluesky ≤300, LinkedIn ≤1400). If no true version exists, skip it and note it in STATUS.md.
   - **Placeholders `[...]`:** fill them all from the weekly scorecard. Any left unfilled means skip.
   - **Newsletter gate (Nov 3):** schedule only after Beehiiv shows issue #2 as *sent*. If it's not sent, the Nov 3 posts stay drafts. Also edit the Nov 2 LinkedIn post ("issue #2 is out tomorrow") if the send moved.
   - **Thread limit:** a thread draft is scheduled only when no other thread is scheduled on that channel (e.g. Nov 4 X/Bluesky after the Oct 28 threads publish).
   - **Capacity:** the channel has fewer than 10 scheduled posts.
4. Strip the label line, write "SKILL file" (never "SKILL.md", which Buffer and the networks turn into a link), then `edit_post` the text (and every `metadata.<network>.thread` item, with item 1 equal to the outer text) and move it to the queue at its planned `dueAt`. If edit can't flip draft→scheduled, create a fresh post with the same text and `dueAt`, then delete the draft (it's our own draft, so that's fine).
5. Check: `list_posts` again. Confirm the status is scheduled, the time is right, and there are no duplicates.
6. Append one line to STATUS.md's Session log: what was scheduled, what was skipped and why. No daily report post unless something big happened.

## Calendar (as created 2026-10-26)
Scheduled: Oct 27, 28 (threads on X/Bluesky), 29, Nov 2, 5, 6, 7, 9 on all 3 channels (24 posts).
Drafts: Oct 30 (REFRESH Superpowers), Oct 31 (REFRESH flaky 13), Nov 1 (REFRESH wk-44 scorecard), Nov 3 (newsletter gate), Nov 4 (REFRESH Cursor 27/52; X/Bluesky threads), Nov 8 (wk-45 placeholders; X/Bluesky threads). That's 18 drafts.
