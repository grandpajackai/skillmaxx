#!/bin/bash
# Heartbeat watchdog for the SkillMaxx Bluesky poster (no cron/systemd on this box).
# Every 60 s: if supervise.sh is gone, or its heartbeat is older than 20 min, kill the
# stale loop and start a fresh one. supervise.sh restarts this keeper in turn.
set -u
DIR=/home/box/skillmaxx-bluesky
exec 9>"$DIR/keeper.lock"
flock -n 9 || exit 0
echo $$ > "$DIR/keeper.pid"
log() { echo "$(TZ=America/New_York date '+%F %T %Z') keeper: $*" >> "$DIR/bluesky-post.log"; }
start_sup() { setsid nohup bash "$DIR/supervise.sh" >>"$DIR/bluesky-post.log" 2>&1 < /dev/null 9>&- & }
sleep 30 9>&-
while true; do
  now=$(date +%s)
  hb=$(cut -d' ' -f1 "$DIR/heartbeat" 2>/dev/null || echo 0)
  age=$((now - ${hb:-0}))
  if ! pgrep -f "skillmaxx-bluesky/supervise.sh" >/dev/null 2>&1; then
    log "supervise.sh not running; starting it"
    start_sup
  elif [ "$age" -gt 1200 ]; then
    log "heartbeat stale (${age}s); restarting supervise.sh"
    pkill -f "skillmaxx-bluesky/supervise.sh" 2>/dev/null
    pkill -f "skillmaxx-bluesky/repo/growth/social/bluesky_post.py" 2>/dev/null
    fuser -k "$DIR/supervise.lock" >/dev/null 2>&1
    sleep 2
    start_sup
    printf '%s restart\n' "$(date +%s)" > "$DIR/heartbeat"
  fi
  sleep 60 9>&-
done
