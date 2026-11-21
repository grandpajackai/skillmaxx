#!/bin/bash
# Install or print the Mac launchd job and the box cron fallback for Bluesky posting.
# Does not post. Does not create credentials. install runs only on macOS.
# Usage: growth/social/install_bluesky.sh {print-plist|install|uninstall|status|print-cron|dry-run}
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
# Box fallback only. Do not also run this if the Mac launchd job is live (the
# poster dedupes against state + the account feed, but one runner is enough).
# Install by appending to crontab only after ~/.skillmaxx-secrets/bluesky.env exists
# (chmod 600). The poster is a no-op without that file.
*/30 * * * * test -f $KEYFILE && /usr/bin/python3 $SCRIPT >> $LOG 2>&1
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
  dry-run) cmd_dry_run ;;
  install) cmd_install ;;
  uninstall) cmd_uninstall ;;
  status) cmd_status ;;
  *)
    echo "Usage: growth/social/install_bluesky.sh {print-plist|install|uninstall|status|print-cron|dry-run}" >&2
    exit 2
    ;;
esac
