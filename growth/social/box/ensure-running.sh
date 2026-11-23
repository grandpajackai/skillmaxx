#!/bin/bash
# Start the Bluesky poster supervisor if it is not already running. Fast and silent.
set -u
DIR=/home/box/skillmaxx-bluesky
LOG="$DIR/bluesky-post.log"
mkdir -p "$DIR"

already() {
  if [ -f "$DIR/supervise.pid" ]; then
    pid=$(cat "$DIR/supervise.pid" 2>/dev/null || true)
    if [ -n "${pid:-}" ] && kill -0 "$pid" 2>/dev/null; then
      if tr '\0' ' ' < /proc/"$pid"/cmdline 2>/dev/null | grep -q "skillmaxx-bluesky/supervise.sh"; then
        return 0
      fi
    fi
  fi
  if pgrep -f "/home/box/skillmaxx-bluesky/supervise.sh" >/dev/null 2>&1; then
    return 0
  fi
  return 1
}

if ! pgrep -f "skillmaxx-bluesky/keeper.sh" >/dev/null 2>&1; then
  setsid nohup bash "$DIR/keeper.sh" >>"$LOG" 2>&1 < /dev/null &
fi

if already; then
  exit 0
fi

setsid nohup bash "$DIR/supervise.sh" >>"$LOG" 2>&1 < /dev/null &
disown || true
exit 0
