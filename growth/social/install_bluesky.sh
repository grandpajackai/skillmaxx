#!/bin/bash
# Print or install the Mac launchd job, or print the box supervisor notes.
# Does not post. Does not create credentials. `install` runs only on macOS
# and should stay off while the box supervisor is the live runner.
# Usage: growth/social/install_bluesky.sh {print-plist|install|uninstall|status|print-cron|print-box|dry-run}
set -uo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
LABEL=com.gilventures.skillmaxx.bluesky
PLIST="${HOME}/Library/LaunchAgents/${LABEL}.plist"
SCRIPT="$ROOT/growth/social/bluesky_post.py"
LOG_DIR="${HOME}/.local/share/skillmaxx/logs"
LOG="$LOG_DIR/bluesky-post.log"
KEYFILE="${SKILLMAXX_BLUESKY_ENV:-$HOME/.skillmaxx-secrets/bluesky.env}"

cmd_print_plist() {
  case "$ROOT" in
    *'&'*|*'<'*|*'>'*) echo "repo path has XML-special characters; refusing" >&2; return 2;;
  esac
  cat <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>$LABEL</string>
  <key>Comment</key>
  <string>Post due SkillMaxx Bluesky queue items every 30 minutes via the AT Protocol. No LLM. Skips when the app-password file is missing. Does not post to Buffer, Instagram, X, or LinkedIn.</string>
  <key>WorkingDirectory</key>
  <string>$ROOT</string>
  <key>ProgramArguments</key>
  <array>
    <string>/usr/bin/python3</string>
    <string>$SCRIPT</string>
  </array>
  <key>StartInterval</key>
  <integer>1800</integer>
  <key>RunAtLoad</key>
  <false/>
  <key>StandardOutPath</key>
  <string>$LOG</string>
  <key>StandardErrorPath</key>
  <string>$LOG</string>
</dict>
</plist>
EOF
}

cmd_print_cron() {
  cat <<EOF
# Legacy crontab line. The SkillMaxx box has no cron/systemd (PID 1 is tini),
# so the live runner is the supervised loop in growth/social/box/ (installed at
# /home/box/skillmaxx-bluesky/). Do not also enable Mac launchd while that loop
# is live. The poster is a no-op without ~/.skillmaxx-secrets/bluesky.env.
*/30 * * * * test -f $KEYFILE && /usr/bin/python3 $SCRIPT >> $LOG 2>&1
EOF
}

cmd_print_box() {
  cat <<EOF
# Live runner (the box is always on). No cron/systemd; same keep-alive pattern
# as /home/box/skillmaxx-watch and /home/box/skillmaxx-prep:
#   /home/box/skillmaxx-bluesky/supervise.sh   every 15 minutes
#   /home/box/skillmaxx-bluesky/keeper.sh      heartbeat watchdog
#   /home/box/skillmaxx-bluesky/ensure-running.sh  hooked from ~/.bashrc
# Canonical copies: growth/social/box/
# Logs: /home/box/skillmaxx-bluesky/bluesky-post.log
# Do not also run the Mac launchd job while this loop is live.
EOF
}

cmd_dry_run() {
  exec /usr/bin/python3 "$SCRIPT" --dry-run
}

cmd_install() {
  if [ "$(uname -s)" != "Darwin" ]; then
    echo "Not installed. install runs only on macOS. This machine is $(uname -s)."
    echo "On the box, use: $0 print-cron"
    return 2
  fi
  mkdir -p "$HOME/Library/LaunchAgents" "$LOG_DIR"
  cmd_print_plist > "$PLIST"
  launchctl bootout "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || true
  launchctl bootstrap "gui/$(id -u)" "$PLIST"
  echo "Installed $PLIST (every 30 minutes, RunAtLoad=false)."
  echo "Start it with: launchctl kickstart -k gui/$(id -u)/$LABEL"
  echo "Dry-run first: /usr/bin/python3 $SCRIPT --dry-run"
}

cmd_uninstall() {
  if [ "$(uname -s)" != "Darwin" ]; then
    echo "uninstall runs only on macOS. This machine is $(uname -s)."
    return 2
  fi
  launchctl bootout "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || true
  rm -f "$PLIST"
  echo "Removed $LABEL"
}

cmd_status() {
  echo "repo: $ROOT"
  echo "script: $SCRIPT"
  echo "keyfile path (existence only): $KEYFILE ($( [ -f "$KEYFILE" ] && echo present || echo missing ))"
  echo "plist: $PLIST ($( [ -f "$PLIST" ] && echo present || echo not installed ))"
  if [ "$(uname -s)" = "Darwin" ]; then
    launchctl print "gui/$(id -u)/$LABEL" 2>/dev/null | sed -n '1,20p' || echo "launchd job not loaded"
  fi
}

case "${1:-}" in
  print-plist) cmd_print_plist ;;
  print-cron) cmd_print_cron ;;
  print-box) cmd_print_box ;;
  dry-run) cmd_dry_run ;;
  install) cmd_install ;;
  uninstall) cmd_uninstall ;;
  status) cmd_status ;;
  *)
    echo "Usage: growth/social/install_bluesky.sh {print-plist|install|uninstall|status|print-cron|print-box|dry-run}" >&2
    exit 2
    ;;
esac
