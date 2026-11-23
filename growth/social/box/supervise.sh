#!/bin/bash
# Persistent 15-minute loop for the SkillMaxx direct Bluesky poster.
# No LLM. Posts only items whose due_at has passed. Credentials stay in
# ~/.skillmaxx-secrets/bluesky.env (never printed). No cron/systemd on this box
# (PID 1 is tini), so this follows the skillmaxx-watch / skillmaxx-prep pattern.
set -u
export TZ="America/New_York"
DIR=/home/box/skillmaxx-bluesky
REPO=$DIR/repo
SCRIPT=$REPO/growth/social/bluesky_post.py
LOG=$DIR/bluesky-post.log
KEYFILE="${SKILLMAXX_BLUESKY_ENV:-$HOME/.skillmaxx-secrets/bluesky.env}"
INTERVAL=900

cd "$DIR" || exit 1
exec 8>"$DIR/supervise.lock"
if ! flock -n 8; then
  exit 0
fi
echo $$ > "$DIR/supervise.pid"

log() { echo "$(date '+%Y-%m-%d %H:%M:%S %Z')  $*" >>"$LOG"; }

refresh_repo() {
  if [ ! -d "$REPO/.git" ]; then
    git clone -q https://github.com/grandpajackai/skillmaxx.git "$REPO" || return 1
  fi
  # Dedicated scratch clone: never committed to or pushed from.
  git -C "$REPO" fetch -q origin master && git -C "$REPO" checkout -q -f -B master origin/master
}

run_once() {
  if ! refresh_repo; then
    log "git refresh failed; using existing clone"
  fi
  if [ ! -f "$SCRIPT" ]; then
    log "bluesky_post.py missing; skip"
    return 1
  fi
  if [ ! -f "$KEYFILE" ]; then
    log "keyfile missing; skip (safe no-op)"
    return 0
  fi
  # Hard cap so a hung AT Protocol call can never stall the loop.
  timeout -k 20 240 /usr/bin/python3 "$SCRIPT" >>"$LOG" 2>&1 8>&-
  return $?
}

log "supervisor start (pid $$)"
while true; do
  start=$(date +%s)
  run_once
  rc=$?
  printf '%s %s rc=%s\n' "$(date +%s)" "$(date '+%F %T %Z')" "$rc" > "$DIR/heartbeat.tmp" && mv -f "$DIR/heartbeat.tmp" "$DIR/heartbeat"
  pgrep -f "skillmaxx-bluesky/keeper.sh" >/dev/null 2>&1 || setsid nohup bash "$DIR/keeper.sh" >>"$LOG" 2>&1 < /dev/null 8>&- &
  if [ -f "$LOG" ] && [ "$(wc -c < "$LOG")" -gt 262144 ]; then
    mv "$LOG" "$LOG.1" 2>/dev/null || true
  fi
  now=$(date +%s)
  sleep_for=$((INTERVAL - (now - start)))
  if [ "$sleep_for" -lt 5 ]; then
    sleep_for=5
  fi
  sleep "$sleep_for" 8>&-
done
