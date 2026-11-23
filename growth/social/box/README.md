# Box supervisor for the SkillMaxx Bluesky poster

Canonical copies of the always-on loop that lives at `/home/box/skillmaxx-bluesky/`
on the SkillMaxx box. The box has no cron/systemd (PID 1 is tini), so this
follows the `skillmaxx-watch` / `skillmaxx-prep` pattern:

- `supervise.sh` — every 15 minutes, refresh a dedicated `origin/master` clone
  and run `growth/social/bluesky_post.py` (240s timeout)
- `keeper.sh` — 60s watchdog; restarts supervise if it is gone or the heartbeat
  is older than 20 minutes
- `ensure-running.sh` — hooked from `~/.bashrc` so a new login shell brings it back

Do not also enable the Mac launchd job while this loop is live. One runner is
enough; the poster dedupes, but two clocks are still a risk.

These files are documentation and a restore path. Installing or restarting the
loop is done on the box, not by this folder existing in the repo.
