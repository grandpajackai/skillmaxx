# SkillMaxx Bluesky posting (direct, not Buffer)

Brandon chose to move Bluesky off the free Buffer plan (3 channels, all used) so a later channel could take that slot. Instagram `@skillmaxxai` was permanently disabled on 2026-11-23, so do not automatically fill the slot with Instagram. This path posts to `skillmaxx.bsky.social` with the public AT Protocol. No LLM, no Buffer API, $0.

**Live since 2026-11-23:** the always-on box supervisor at `/home/box/skillmaxx-bluesky/` is the runner. Do not also enable the Mac launchd job. The Buffer Bluesky channel is still connected (disconnect it in the browser after this is confirmed); scheduled Buffer copies of the queue were deleted on 2026-11-23 so nothing double-posts.

## How it works

1. Upcoming posts live in [`bluesky-queue.json`](bluesky-queue.json) (in the repo) plus an optional local overlay at `~/.local/share/skillmaxx/bluesky-queue.local.json` on the machine that runs the poster (the box).
2. The Sunday 10 PM ET Buffer top-up (`skillmaxx-buffer-daily-top-up`, prompt name **SkillMaxx Buffer daily top-up**) must enqueue Bluesky with `python3 growth/scripts/buffer_weekly.py --repo-queue` and open a small PR. It must **not** call Buffer `create_post` for channel `6adfbe402f1f5ed648def519`. X and LinkedIn stay on the Grok Buffer connector. A Mac-only local overlay is not enough: the box poster reads `origin/master` plus the box's own overlay, not the Mac's home directory.
3. `growth/social/bluesky_post.py` posts items whose `due_at` has passed, records AT URIs in `~/.local/share/skillmaxx/bluesky-state.json`, skips duplicates (queue id, text already in state, or the same text already on the account feed, treating `https://` and a bare host as the same), and caps at 3 posts per America/New_York day. `--dry-run` never contacts Bluesky.

```bash
python3 growth/social/bluesky_post.py --dry-run
python3 growth/social/bluesky_post.py --list
python3 growth/social/bluesky_post.py --self-test
# After Buffer has already published a migrated item, record it so the script will not also post it:
python3 growth/social/bluesky_post.py --mark-posted buf-6afbc1c1df36f4d8256372d8
```

## Credentials

Create a **Bluesky app password** (not the account password) while signed in as `skillmaxx.bsky.social`: [bsky.app Settings → App Passwords](https://bsky.app/settings/app-passwords) → “Add App Password”. On the box (the live runner):

`~/.skillmaxx-secrets/bluesky.env` (chmod 600)

```
BLUESKY_HANDLE=skillmaxx.bsky.social
BLUESKY_APP_PASSWORD=xxxxxxxx
```

Optional: `BLUESKY_PDS=https://bsky.social`. The script also accepts the older env alias `BLUESKY_SKILLMAXX_APP_PASSWORD`. Override the file path with `SKILLMAXX_BLUESKY_ENV`. Never commit this file, never paste it into chat, never print it.

Without that file the poster exits 0 and posts nothing.

## Box supervisor (live runner)

The SkillMaxx box has no cron/systemd (PID 1 is tini). The poster is kept alive the same way as `/home/box/skillmaxx-watch` and `/home/box/skillmaxx-prep`:

- `/home/box/skillmaxx-bluesky/supervise.sh` — every 15 minutes, refresh a dedicated `origin/master` clone, run `bluesky_post.py` (240s timeout)
- `/home/box/skillmaxx-bluesky/keeper.sh` — 60s heartbeat watchdog
- `/home/box/skillmaxx-bluesky/ensure-running.sh` — hooked from `~/.bashrc` so a new login shell brings it back

Canonical copies of those scripts: [`box/`](box/). Logs: `/home/box/skillmaxx-bluesky/bluesky-post.log`. Print a reminder with `growth/social/install_bluesky.sh print-box`.

## Mac launchd (do not enable while the box is live)

`install` in `install_bluesky.sh` runs only on macOS and is **off on purpose** while the box loop is the runner. One poster is enough. The job label would be `com.gilventures.skillmaxx.bluesky`, every 30 minutes. `install_bluesky.sh print-plist` writes a plist with that checkout’s paths. The checked-in `com.gilventures.skillmaxx.bluesky.plist` is a template only; do not `launchctl load` that file as-is.

`testing/publish_nightly.sh` still runs `buffer_weekly.py` on Sundays after a successful publish, which writes the Mac local overlay (no Buffer API). That overlay is a backup only; the live box poster will not see it until the same items land in the repo queue via `--repo-queue` and a merged PR.

## Overlap with Buffer (do not double-post)

Scheduled Buffer copies of the current queue were deleted on 2026-11-23 after `--mark-posted` of the two items Buffer had already published:

| Buffer post id | Time (ET) | Queue id | Disposition (2026-11-23) |
|---|---|---|---|
| `6afbc1c1df36f4d8256372d8` | Sat Nov 21, 5:00 PM | `buf-6afbc1c1df36f4d8256372d8` | Already published; marked in box state |
| `6afbc1c2797935b975d8a168` | Sun Nov 22, 6:15 PM | `buf-6afbc1c2797935b975d8a168` | Already published; marked in box state |
| `6afbc1cbdf36f4d8256375b2` | Mon Nov 23, 7:30 PM | `buf-6afbc1cbdf36f4d8256375b2` | Buffer copy deleted; due on the box poster |
| `6b03aefdd5eabfb8ccfee23d` | Tue Nov 24, 7:30 PM | `buf-6b03aefdd5eabfb8ccfee23d` | Buffer copy deleted; remains in the repo queue |
| `6b03af04c72676f5e97ffe1b` | Wed Nov 25, 7:30 PM | `buf-6b03af04c72676f5e97ffe1b` | Buffer copy deleted; remains in the repo queue |
| `6b03af0bc72676f5e98000a1` | Thu Nov 26, 7:30 PM | `buf-6b03af0bc72676f5e98000a1` | Buffer copy deleted; remains in the repo queue |
| `6b03af12a6de38de9eb4c23e` | Fri Nov 27, 7:30 PM | `buf-6b03af12a6de38de9eb4c23e` | Buffer copy deleted; remains in the repo queue |
| `6b03af1a846b0ee907dbd421` | Sat Nov 28, 5:00 PM | `buf-6b03af1a846b0ee907dbd421` | Buffer copy deleted; remains in the repo queue |
| `6b03af22d864a01105185400` | Sun Nov 29, 6:15 PM | `buf-6b03af22d864a01105185400` | Buffer copy deleted; remains in the repo queue |

Stale Buffer draft `6adfee163bff354cec696067` (planned Tue Nov 3 newsletter #2) was not migrated and was left as a draft. Do not schedule it.

## Community actions (replies, likes, follows)

Scheduled posts stay on `bluesky_post.py`. For replies, likes, follows, unfollows, and notification checks, use [`../bluesky/bsky_api.py`](../bluesky/bsky_api.py) with the same `bluesky.env` app password. Do not use the box browser for these (a signed-out bsky.app session is not required). Never print the app password or a session token.

```bash
python3 growth/bluesky/bsky_api.py login
python3 growth/bluesky/bsky_api.py reply URL TEXT
python3 growth/bluesky/bsky_api.py like URL
python3 growth/bluesky/bsky_api.py follow HANDLE
python3 growth/bluesky/bsky_api.py unfollow HANDLE
python3 growth/bluesky/bsky_api.py notifications --since 2026-11-19T00:00:00-05:00 --reasons reply,mention,quote
```

## After the script is confirmed live: disconnect Buffer Bluesky

The channel is still connected. Free the slot in the browser (do not do this from an API/tooling pass that only takes posting live):

1. Open [Buffer](https://publish.buffer.com/) signed in to the SkillMaxx org (`6adfb3f8d2cea8f4b234c15b`).
2. Click the profile avatar in the bottom left, then **Channels**.
3. On `skillmaxx.bsky.social`, click the three-dot menu on the right.
4. Click **Disconnect Channel**.
5. The dialog warns that existing posts, analytics, and data for this channel are removed and cannot be recovered. Type `disconnect` and click **Disconnect Channel** again.

Source: [Disconnecting a channel from Buffer](https://support.buffer.com/en-us/articles/disconnecting-a-channel-from-buffer-33vFDqJJjv).

Do **not** automatically connect Instagram in the freed slot. `@skillmaxxai` was permanently disabled by Meta on 2026-11-23 (no further review). A new Instagram account is Brandon's call. See [`growth/carousels/INSTAGRAM-SETUP.md`](../carousels/INSTAGRAM-SETUP.md).

## Sunday / daily Buffer top-up

When scheduling the weekly scorecard posts, do **not** call Buffer `create_post` for channel `6adfbe402f1f5ed648def519`. Run `python3 growth/scripts/buffer_weekly.py --repo-queue` (and open a small PR). X and LinkedIn stay on Buffer. Details: [`growth/routines/BUFFER-DAILY-TOPUP.md`](../routines/BUFFER-DAILY-TOPUP.md).
