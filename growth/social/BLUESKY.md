# SkillMaxx Bluesky posting (direct, not Buffer)

Brandon chose to move Bluesky off the free Buffer plan (3 channels, all used) so Instagram can take that slot for carousels. This path posts to `skillmaxx.bsky.social` with the public AT Protocol. No LLM, no Buffer API, $0.

## How it works

1. Upcoming posts live in [`bluesky-queue.json`](bluesky-queue.json) (in the repo) plus an optional local overlay at `~/.local/share/skillmaxx/bluesky-queue.local.json`.
2. `growth/scripts/buffer_weekly.py` writes the usual Mon/Wed/Fri 7:30 PM ET scorecard posts into that queue. It no longer creates Buffer posts for Bluesky. X and LinkedIn stay on the Grok Buffer connector.
3. `growth/social/bluesky_post.py` posts items whose `due_at` has passed, records AT URIs in `~/.local/share/skillmaxx/bluesky-state.json`, skips duplicates (queue id, exact text already in state, or the same text already on the account feed), and caps at 3 posts per America/New_York day. `--dry-run` never contacts Bluesky.

```bash
python3 growth/social/bluesky_post.py --dry-run
python3 growth/social/bluesky_post.py --list
python3 growth/social/bluesky_post.py --self-test
# After Buffer has already published a migrated item, record it so the script will not also post it:
python3 growth/social/bluesky_post.py --mark-posted buf-6afbc1c1df36f4d8256372d8
```

## Credentials

The box checkout of `/home/box/.skillmaxx-secrets/` has no Bluesky keyfile (names there: `accounts.env`, `intake.env`, `zoho_skillmaxx.json`). No Bluesky app-password env vars were set when this was added. The older community helper (`/workspace/bsky/bs.py`, not in the repo) expected the env alias `BLUESKY_SKILLMAXX_APP_PASSWORD` at runtime; that value is not in the secrets directory and is not in the current environment. Replies in the Bluesky community routine have been posted with that ad-hoc API client or by hand, not by a committed script.

Create a **Bluesky app password** (not the account password) while signed in as `skillmaxx.bsky.social`: [bsky.app Settings → App Passwords](https://bsky.app/settings/app-passwords) → “Add App Password”. Put it only on the Mac (and on the box only if you want the cron fallback) as:

`~/.skillmaxx-secrets/bluesky.env` (chmod 600)

```
BLUESKY_HANDLE=skillmaxx.bsky.social
BLUESKY_APP_PASSWORD=xxxxxxxx
```

Optional: `BLUESKY_PDS=https://bsky.social`. The script also accepts the older env alias `BLUESKY_SKILLMAXX_APP_PASSWORD`. Override the file path with `SKILLMAXX_BLUESKY_ENV`. Never commit this file, never paste it into chat, never print it.

Without that file the poster exits 0 and posts nothing, so cron/launchd is safe to load after the file exists.

## Mac launchd (primary)

Do not install this from Linux or from a remote agent. On the Mac checkout (usually `/Users/grandpajack/Projects/skillmaxx-local-trial-20261107`), after a dry-run looks right and the app-password file is in place:

```bash
# from the checkout, after git pull / the PR is on master
python3 growth/social/bluesky_post.py --dry-run
growth/social/install_bluesky.sh status
growth/social/install_bluesky.sh install
# RunAtLoad is false, so start it once you are ready (see overlap note below):
launchctl kickstart -k gui/$(id -u)/com.gilventures.skillmaxx.bluesky
```

The job label is `com.gilventures.skillmaxx.bluesky`, every 30 minutes. Logs: `~/.local/share/skillmaxx/logs/bluesky-post.log`. `install_bluesky.sh print-plist` writes the live plist with this checkout’s paths. The checked-in `com.gilventures.skillmaxx.bluesky.plist` is a template only; do not `launchctl load` that file as-is.

`testing/publish_nightly.sh` also runs `buffer_weekly.py` on Sundays after a successful publish, which enqueues the next week’s Bluesky posts into the local overlay (no Buffer API).

## Box cron (fallback only)

Only if `~/.skillmaxx-secrets/bluesky.env` exists on the box, and only if the Mac job is not already running. Print the line with `growth/social/install_bluesky.sh print-cron`. The poster is a no-op without the keyfile.

## Overlap with Buffer (do not double-post)

This change **does not** delete or disconnect the Buffer Bluesky channel. The migrated posts below are still scheduled in Buffer. Leave them there until the direct poster is confirmed live, then delete those Buffer posts (or wait until they have published and `--mark-posted` each id). Do not install launchd in live mode while Buffer still holds the same due items.

| Buffer post id | Time (ET) | Queue id |
|---|---|---|
| `6afbc1c1df36f4d8256372d8` | Sat Nov 21, 5:00 PM | `buf-6afbc1c1df36f4d8256372d8` |
| `6afbc1c2797935b975d8a168` | Sun Nov 22, 6:15 PM | `buf-6afbc1c2797935b975d8a168` |
| `6afbc1cbdf36f4d8256375b2` | Mon Nov 23, 7:30 PM | `buf-6afbc1cbdf36f4d8256375b2` |

Stale Buffer draft `6adfee163bff354cec696067` (planned Tue Nov 3 newsletter #2) was not migrated.

## After the script is confirmed live: disconnect Buffer Bluesky

Only after the remaining Buffer copies are deleted or have already published, free the slot:

1. Open [Buffer](https://publish.buffer.com/) signed in to the SkillMaxx org (`6adfb3f8d2cea8f4b234c15b`).
2. Click the profile avatar in the bottom left, then **Channels**.
3. On `skillmaxx.bsky.social`, click the three-dot menu on the right.
4. Click **Disconnect Channel**.
5. The dialog warns that existing posts, analytics, and data for this channel are removed and cannot be recovered. Type `disconnect` and click **Disconnect Channel** again.

Source: [Disconnecting a channel from Buffer](https://support.buffer.com/en-us/articles/disconnecting-a-channel-from-buffer-33vFDqJJjv).

Then connect the SkillMaxx Instagram account in the freed slot. See [`growth/carousels/INSTAGRAM-SETUP.md`](../carousels/INSTAGRAM-SETUP.md).

## Sunday / daily Buffer top-up

When scheduling the weekly scorecard posts, do **not** call Buffer `create_post` for channel `6adfbe402f1f5ed648def519`. Run `python3 growth/scripts/buffer_weekly.py --repo-queue` (and open a small PR) or let the Sunday Mac publish write the local overlay. X and LinkedIn stay on Buffer. Details: [`growth/routines/BUFFER-DAILY-TOPUP.md`](../routines/BUFFER-DAILY-TOPUP.md).
