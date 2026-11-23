# SkillMaxx Instagram setup (account disabled)

**Status (2026-11-23, America/New_York):** Meta permanently disabled the SkillMaxx Instagram account `@skillmaxxai` for a Community Standards violation. The in-app page said the account goes against Community Standards, nobody can see it anymore, and "You cannot request another review of this decision." The appeal is over. The account and its data are set to be deleted.

## What this means

- Do not check the appeal, reconnect Buffer, or queue posts to Instagram. There is no restore path.
- Carousels continue on LinkedIn and X via Buffer, as already scheduled and planned.
- Reuse the animated v3 MP4s (`animated/slide-0N.mp4` and `animated/preview.mp4`) as short video posts on the channels we still have. Do not leave them waiting for Instagram.
- A brand-new Instagram account is Brandon's call. Meta just banned this one, so a new account could get flagged too. Do not create, name, or connect a replacement unless Brandon asks.

Telegram request `req-003-instagram-skillmaxx` is cancelled. The Buffer Bluesky disconnect can still happen on its own schedule (see [`growth/social/BLUESKY.md`](../social/BLUESKY.md)); do not automatically connect Instagram in the freed slot.

The rest of this file is the original Buffer setup and posting plan, kept as a reference **only if** Brandon later approves a new Professional account. Treat every "create the account" / "once the account exists" step below as paused until that decision.

---

# Original setup notes (paused)

Brandon chose to move Bluesky posting off Buffer so an Instagram account could use the freed channel on the free plan (3 channels, 10 scheduled posts each). Carousels stay on Buffer; Bluesky is direct via the AT Protocol ([`growth/social/BLUESKY.md`](../social/BLUESKY.md)). CTA stays the newsletter until Brandon picks otherwise.

Nothing in the paused notes below should be posted or connected unless Brandon later approves a new SkillMaxx Instagram account and the Bluesky Buffer channel has been disconnected (after the direct poster is confirmed live).

## What Brandon needs to do

Only Brandon can create the account (Instagram asks for a phone). Use the SkillMaxx brand email, not a personal login.

1. **Create the account.** On a phone, sign up at Instagram with `skillmaxx@gilventures.ai`. Suggested handle: `skillmaxx.ai` or `skillmaxx` (take the closest available; tell the CEO agent the handle). Skip personal Facebook login if Instagram offers to “sign up with Facebook” — keep this a SkillMaxx-only account.
2. **Switch to a Professional account (Creator or Business).** In the Instagram app: Profile → Edit profile / Professional dashboard → **Switch to professional account**. Either **Creator** or **Business** works for Buffer automatic publishing. Creator is the usual fit for a media/education brand; Business is fine too. A Personal account can only use Buffer’s “notify me” flow and cannot auto-publish.
3. **Bio and link.**
   - Name: `SkillMaxx`
   - Bio (draft): `Which AI-agent skills, plugins and MCP servers actually install. Nightly tests in Claude Code, Codex, Grok Build, Cursor and Pi.`
   - Link: `https://skillmaxx.gilventures.ai/newsletter/` (newsletter CTA). Website field if Instagram shows one: the same URL, or `https://skillmaxx.gilventures.ai/` with the newsletter in the bio.
4. **No Facebook Page is required** for the setup we want. Buffer can auto-publish, show Insights, and manage comments when a Professional account is connected with an Instagram login. A linked Facebook Page is optional and is only needed later for locations, collaborators, liking mentions in Community, or music on Reels with automatic publishing.
5. **Tell the CEO agent in chat** when a new account (if Brandon approved one) is a Creator or Business profile and share the handle. Do not connect it to Buffer until Bluesky is off that slot (otherwise the free plan would lock a channel). Telegram request `req-003-instagram-skillmaxx` was cancelled on 2026-11-23 after Meta permanently disabled `@skillmaxxai`.

Full steps for connecting later are in the Buffer doc linked below. Use a desktop browser, log out of other Instagram accounts first, then in Buffer: profile avatar (bottom left) → **Channels** → **Connect Channel** → **Instagram** → under **Professional**, **Connect to Instagram**, and sign in as the SkillMaxx account. Select all permissions.

## Does Buffer’s free plan support Instagram carousels?

Yes, on all plans including Free, for Instagram Business or Creator accounts:

- Free plan includes Instagram business accounts and Instagram creator accounts, with automatic publishing and notification publishing. Up to 3 channels and 10 scheduled posts per channel. Source: [Buffer pricing](https://buffer.com/pricing).
- Automatic publishing works on all plans when the account is Professional (Business or Creator) and the media meets Instagram’s rules. The recommended Free-plan connection is **Professional via Instagram login** (no Facebook Page). A Personal account cannot auto-publish. Source: [Connecting your Instagram account to Buffer](https://support.buffer.com/en-us/articles/connecting-your-instagram-account-to-buffer-n9Ad6veXsu).
- Feed posts can be a carousel of up to 20 images and videos. Each image must be between **3:4 and 1.91:1**. If the ratio is outside that range, Buffer falls back to notification publishing. Source: [Scheduling Instagram posts, reels, stories, and notifications](https://support.buffer.com/en-us/articles/scheduling-instagram-posts-reels-stories-and-notifications-3XA98S9Q5p) and [Instagram’s accepted aspect ratio ranges](https://support.buffer.com/en-us/articles/instagrams-accepted-aspect-ratio-ranges-Frc2Xqewbd).
- SkillMaxx IG carousels are already rendered at **1080×1350** (4:5 = 0.80), which sits inside 3:4 (0.75) and 1.91:1, so they should auto-publish. Use the IG-sized stills, not the 1080×1920 TikTok set, for this channel.

## Posting plan (3 carousels / week)

The content plan in [`CONTENT-PLAN.md`](CONTENT-PLAN.md) has a core cadence of four decks a week (Tue news, Wed timely, Fri maxxing, Sun leaderboard). On Buffer Free we start at **3 carousels a week** so the 10-slot queue has headroom (about one week scheduled at a time, plus a slip day):

| Day (ET) | Deck | Notes |
|---|---|---|
| Tuesday, 11:00 AM | `news` — last night’s install report | Re-render that morning from `reports.json`. Preview media: `/workspace/carousels-samples/queue-2026-W48..W51/previews/animated-news-2026-11-20/` |
| Friday, 11:00 AM | `maxxing` — honest fails + 5/5 elite | Re-render from that night’s data. Preview: `/workspace/carousels-samples/v3-animated-maxxing-2026-11-20/` |
| Sunday, 4:00 PM | `leaderboard` — weekly scorecard | Re-render from that week’s `weeks.json`. Preview: `/workspace/carousels-samples/queue-2026-W48..W51/previews/animated-leaderboard-2026-11-20/` |

Wednesday `timely` and the optional Monday `orgchart` stay in the review queue ([`REVIEW-QUEUE.md`](REVIEW-QUEUE.md)) for later, or as a swap when a week has a strong news hook (drop Friday or Tuesday that week so we still ship 3). Do not schedule more than 10 posts on the channel.

First weeks to fill: 2026-W48 (Tue Nov 24, Fri Nov 27, Sun Nov 29) through W51, after each deck is re-rendered at publish time. Preview numbers from the 2026-11-20 report must not be posted as that future week’s scorecard. Wednesday timely stubs are layout only.

**Captions.** One caption per carousel, written at schedule time from the same nightly figures that went on the slides. Pattern:

- Line 1: the hook (same claim as slide 1, with the live numbers).
- 1–3 short lines of context (what we tested, or one takeaway). Not a paste of every slide.
- CTA, always the newsletter until Brandon picks another path: `Free Sunday newsletter: https://skillmaxx.gilventures.ai/newsletter/`
- Optional: 3–5 topical hashtags, not a dump. No comment-keyword CTA until a fulfillment path is staffed (`generate.py --cta keyword|hybrid` is a placeholder only).

Example shape (replace the figures at publish time):

```
Last night: 862 of 1,085 add-ons installed cleanly in our keyless sandbox.

That's Claude Code, Codex, Grok Build, Cursor and Pi — not a ranking of the agents, a record of how completely each add-on ships.

Free Sunday newsletter: https://skillmaxx.gilventures.ai/newsletter/
```

**Images.** Use the 1080×1350 `slide-NN.png` stills, in order, one asset per slide (usually 8–10). Do not attach the stitched `preview.mp4` or per-slide MP4s to an Instagram feed post; those are for TikTok / review. Alt text is required on every image (a short description of that slide’s claim, including the live numbers).

## How images get into Buffer (`create_post` assets)

Buffer’s connector does **not** accept a local file path. Every image must be a publicly downloadable `https://` URL that stays up until the post publishes (not a share page, not a temporary host). Same rule as the existing X/LinkedIn image path in [`growth/routines/BUFFER-DAILY-TOPUP.md`](../routines/BUFFER-DAILY-TOPUP.md).

1. Re-render the deck: `python3 growth/carousels/generate.py --format news --date YYYY-MM-DD --size ig` (or `maxxing` / `leaderboard`). CTA remains the newsletter default.
2. Copy the IG `slide-NN.png` files into the repo, e.g. `src/assets/social/carousels/YYYY-MM-DD-news/slide-01.png` … `slide-0N.png`.
3. Open a PR, wait for CI, squash-merge, then confirm each file is live:

   `curl -I https://skillmaxx.gilventures.ai/assets/social/carousels/YYYY-MM-DD-news/slide-01.png`

   Expect HTTP 200 and an `image/png` type.

4. Schedule with the SkillMaxx Buffer connector (`user-Buffer--skillmaxx`), organization `6adfb3f8d2cea8f4b234c15b`, on the new Instagram channel id from `list_channels`. Do not post until that channel exists.

   `create_post` fields:

   - `channelId`: the Instagram channel (from `list_channels` after it is connected).
   - `schedulingType`: `"automatic"` (Professional account, 1080×1350 stills).
   - `mode`: `"customScheduled"` with an explicit `dueAt` in America/New_York (`-05:00` in EST, `-04:00` in EDT).
   - `text`: the caption, including the newsletter CTA.
   - `assets`: one entry per slide, in order:

     `{ "image": { "url": "https://skillmaxx.gilventures.ai/assets/social/carousels/…/slide-01.png", "metadata": { "altText": "…" } } }`

   - `metadata`: `{ "instagram": { "type": "post" } }` — a feed post; multiple image assets become the carousel. (A single video must be `reel`; we are not using that for these carousels.)

5. Confirm with `list_posts` that the post is `scheduled`, the time is right, and there are no duplicate captions. Stay at or under 10 scheduled posts on the channel.

Never `shareNow` a carousel in this workflow. Never attach images from a personal Drive link or a box path.

## Related

- Content plan, hooks, and CTA rule: [`CONTENT-PLAN.md`](CONTENT-PLAN.md)
- Four-week review queue and preview paths: [`REVIEW-QUEUE.md`](REVIEW-QUEUE.md)
- Generator: [`generate.py`](generate.py)
- Bluesky move and Buffer disconnect steps: [`growth/social/BLUESKY.md`](../social/BLUESKY.md)
