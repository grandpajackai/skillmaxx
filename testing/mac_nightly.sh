#!/bin/bash
# Mac/local entry for the existing mechanical nightly. Does not install a schedule
# unless you run "install" on macOS with the two confirmation variables set.
# Does not disable the Grok Bot routine. Does not send mail, posts, or newsletters.
# Usage: testing/mac_nightly.sh {steps|preflight|dry-run|test|run|print-plist|install|uninstall|status}
set -uo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
LABEL=com.gilventures.skillmaxx.nightly
PLIST="${HOME}/Library/LaunchAgents/${LABEL}.plist"
ENV_FILE=${SKILLMAXX_ENV_FILE:-$ROOT/testing/local.env}

load_env() {
  if [ -f "$ENV_FILE" ]; then
    set -a
    # shellcheck disable=SC1090
    . "$ENV_FILE"
    set +a
  fi
  export SKILLMAXX_AGENTS="${SKILLMAXX_AGENTS:-/workspace/agents}"
}

apply_push_gate() {
  # Only the Mac entry uses this gate. Direct testing/nightly.sh is unchanged.
  if [ "${SKILLMAXX_ALLOW_PUSH:-}" != "yes" ]; then
    if [ "${1:-apply}" = "apply" ]; then
      export NOPUSH=1
      echo "NOPUSH=1 because SKILLMAXX_ALLOW_PUSH is not yes. nightly.sh will still commit data; it will not git push."
    else
      echo "Would set NOPUSH=1 because SKILLMAXX_ALLOW_PUSH is not yes."
    fi
  else
    echo "SKILLMAXX_ALLOW_PUSH=yes, so this entry does not force NOPUSH."
  fi
}

say_dependencies() {
  cat <<'EOF'
Mechanical steps inside testing/nightly.sh (same behavior as the Grok routine's script):
  1. git fetch, checkout master, fast-forward pull. Needs the git credentials this machine already has. This script does not create or change credentials.
  2. Update the local Codex marketplace mirror when SKILLMAXX_AGENTS/codex-mirror exists, then rename it to openai-plugins-mirror.
  3. Sandboxed install tests (testing/run_tests.py via testing/sbx.sh). Every case still runs. On Linux, bubblewrap. On a Mac, the same cases run inside local image skillmaxx-sandbox:local (Docker, not privileged, not the Mac binaries). If neither sandbox is ready, sbx.sh exits and does not run the case on the host. This script does not start Docker, pull images, or install CLIs.
  4. fetch_meta.py. Public HTTP only (no token). Requires Pillow (PIL) and the codex mirror for Codex paths.
  5. testing/daily_report.py. Writes report JSON and, only for a big event, a local draft file. It does not send or queue posts.
  6. testing/weekly_scorecard.py --write. Local weekly pages data.
  7. Eleventy build (npx @11ty/eleventy). Needs Node and a local npm ci.
  8. Data-only git commit. git push only when NOPUSH is empty. A push to master starts the existing GitHub Pages workflow. That is the current publish path, not a new one.

Still done by the Grok routine and not run by nightly.sh. This pass does not automate them:
  - Marketplace re-fetch, build_data.py, and the hand restore of community MCP entries (build_data.py drops them).
  - Browser QA, the health audit, Stripe checks, and FormSubmit checks.
  - STATUS.md, HANDBOOK.md, and DECISIONS.md narrative.
  - Buffer, Beehiiv, email, and social sends.

The per-machine lock is /tmp/skillmaxx-nightly.lockdir (override with SKILLMAXX_LOCKDIR). It stops two runs on this computer. It does not stop the Grok box.
EOF
}

cmd_steps() {
  cat <<EOF
SkillMaxx mechanical nightly on a Mac
Repo: $ROOT

This file is the operator artifact. Run it from the existing checkout. Nothing here merges, pushes, or loads a schedule unless you pass install on the Mac itself.

Cutover (do this before install). This script cannot see or disable the Grok routine.
  1. Pause the Grok Bot routine named "SkillMaxx nightly refresh" (about 2:00 AM ET). Confirm the next fire is off and no run is in progress.
  2. Leave it paused. Do not assume this repository change paused it.
  3. One-time Linux sandbox, only after you start Docker yourself (the 2026-11-07 10:25 ET check found the CLI but the daemon was down; this repo does not start it):
     docker build -t skillmaxx-sandbox:local -f testing/sandbox/Dockerfile testing/sandbox
     Copy testing/local.env.example to testing/local.env and set SKILLMAXX_AGENTS to a directory under your home, for example $HOME/skillmaxx-agents.
     SKILLMAXX_AGENTS must be under /Users so Docker Desktop can mount it.
     bash testing/setup_agents.sh
     That clones the codex mirror and writes templates. It does not npm-install Mac copies of the CLIs.
  4. bash testing/mac_nightly.sh preflight
  5. Trial with no push: bash testing/mac_nightly.sh run
     That sets NOPUSH=1 until testing/local.env contains SKILLMAXX_ALLOW_PUSH=yes.
     Do this before any launchd install. The trial is the no-Grok check.
  6. Read testing/logs/nightly-<date>.log and run: python3 testing/freshness.py
  7. Only after that trial reaches done, and only while the Grok routine is still paused, set SKILLMAXX_ALLOW_PUSH=yes if you want the existing git push, then install.

Install (macOS only, does not run from this cloud VM):
  SKILLMAXX_INSTALL_SCHEDULE=yes SKILLMAXX_GROK_ROUTINE_PAUSED=yes bash testing/mac_nightly.sh install
  SKILLMAXX_GROK_ROUTINE_PAUSED=yes means you attest you paused it. The script does not check Grok and does not disable it.
  The job is launchd $LABEL at 02:00 in the Mac's local timezone. Set the Mac to America/New_York if you want 2:00 AM ET. If the Mac is asleep at 2:00, launchd runs it after wake. The job does not use RunAtLoad, so install does not start a nightly immediately.

Verify the morning after the first scheduled run:
  - One testing/logs/nightly-<date>.log, with a done line or a NIGHTLY FAILED line.
  - python3 testing/freshness.py --check-public
  - The Grok routine did not also write a run (still paused).
  - If push was allowed: published_at comes from GitHub Pages, not from the local build.

Rollback on the Mac:
  bash testing/mac_nightly.sh uninstall
  Uninstall removes the launchd job only. It does not re-enable or disable the Grok routine. Turn that routine back on yourself if you still want it.

Non-secret config: testing/local.env (see testing/local.env.example).
  SKILLMAXX_AGENTS   directory of agent CLIs and templates. Default /workspace/agents.
  SKILLMAXX_ALLOW_PUSH=yes   lets the Mac entry git push. Without it, NOPUSH=1.

EOF
  say_dependencies
}

check() {
  # check <ok:0|1> <label> <detail>
  if [ "$1" -eq 0 ]; then
    echo "ok   $2 — $3"
    return 0
  fi
  echo "blocked   $2 — $3"
  return 1
}

cmd_preflight() {
  load_env
  blocked=0
  echo "Preflight for $ROOT on $(uname -s) ($(uname -m)). Agents dir: $SKILLMAXX_AGENTS"
  command -v python3 >/dev/null 2>&1
  check $? "python3" "required" || blocked=1
  command -v git >/dev/null 2>&1
  check $? "git" "uses existing credentials; this script does not change them" || blocked=1
  command -v node >/dev/null 2>&1
  check $? "node" "required for the Eleventy build" || blocked=1
  [ -d "$ROOT/node_modules/@11ty/eleventy" ]
  check $? "eleventy" "run npm ci in the repo yourself; this script does not" || blocked=1
  python3 -c 'import PIL' >/dev/null 2>&1
  check $? "Pillow" "fetch_meta.py imports PIL. This script does not pip install" || blocked=1
  [ -d "$SKILLMAXX_AGENTS/templates/claude" ]
  check $? "agent templates" "$SKILLMAXX_AGENTS/templates/claude (testing/setup_agents.sh installs CLIs; this handoff does not run it)" || blocked=1
  if [ -d "$SKILLMAXX_AGENTS/codex-mirror" ]; then
    check 0 "codex mirror" "$SKILLMAXX_AGENTS/codex-mirror"
  else
    check 0 "codex mirror" "missing; nightly.sh already continues without it and says so"
  fi
  img=${SKILLMAXX_SANDBOX_IMAGE:-skillmaxx-sandbox:local}
  if command -v bwrap >/dev/null 2>&1; then
    check 0 "sandbox" "bubblewrap is on PATH. Install tests use bwrap."
  elif ! command -v docker >/dev/null 2>&1; then
    check 1 "sandbox" "no bubblewrap and no docker CLI. sbx.sh will refuse an unsandboxed run." || blocked=1
  elif ! docker info >/dev/null 2>&1; then
    check 1 "sandbox" "docker CLI is present but the daemon is not running. This script does not start it. bubblewrap is absent." || blocked=1
  elif ! docker image inspect "$img" >/dev/null 2>&1; then
    check 1 "sandbox" "Docker is up but local image $img is missing. Build: docker build -t $img -f testing/sandbox/Dockerfile testing/sandbox" || blocked=1
  else
    check 0 "sandbox" "local image $img. Tests run in that Linux container as your uid, without --privileged."
  fi
  [ -f "$ROOT/data/skills.json" ]
  check $? "skills.json" "catalog the tests read" || blocked=1
  mkdir -p "$ROOT/testing/logs"
  check $? "log dir" "$ROOT/testing/logs (gitignored)" || blocked=1
  echo
  say_dependencies
  echo
  if [ "$blocked" -eq 0 ]; then
    echo "preflight: ready for a full mechanical nightly"
    return 0
  fi
  echo "preflight: blocked. testing/mac_nightly.sh run will not start nightly.sh."
  return 1
}

cmd_dry_run() {
  echo "Dry run. No git commands, no tests, no build, no push, no launchd."
  cmd_preflight || true
  echo
  echo "Would execute, only if preflight is ready: bash $ROOT/testing/nightly.sh"
  apply_push_gate dry
  echo "Dry run finished. Nothing was executed."
}

cmd_run() {
  load_env
  apply_push_gate
  if [ "${SKILLMAXX_SKIP_PREFLIGHT:-}" != "1" ]; then
    if ! cmd_preflight; then
      mkdir -p "$ROOT/testing/logs"
      echo "$(date '+%F %T %Z') refused: preflight blocked, nightly.sh not started" >> "$ROOT/testing/logs/mac-nightly-refused.log"
      echo "Refused. nightly.sh was not started, so there was no pull, test, build, commit, or push."
      return 1
    fi
  fi
  nightly=${SKILLMAXX_NIGHTLY:-$ROOT/testing/nightly.sh}
  echo "Starting $nightly"
  exec bash "$nightly"
}

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
  <string>SkillMaxx mechanical nightly at 02:00 in this Mac local timezone. Does not disable the Grok Bot routine. Operator must pause that routine first. Push stays off unless testing/local.env sets SKILLMAXX_ALLOW_PUSH=yes.</string>
  <key>WorkingDirectory</key>
  <string>$ROOT</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>$ROOT/testing/mac_nightly.sh</string>
    <string>run</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key>
    <integer>2</integer>
    <key>Minute</key>
    <integer>0</integer>
  </dict>
  <key>StandardOutPath</key>
  <string>$ROOT/testing/logs/launchd-nightly.log</string>
  <key>StandardErrorPath</key>
  <string>$ROOT/testing/logs/launchd-nightly.log</string>
</dict>
</plist>
EOF
}

cmd_install() {
  if [ "$(uname -s)" != "Darwin" ]; then
    echo "Not installed. install runs only on macOS. This machine is $(uname -s)."
    echo "The Grok Bot routine was not changed."
    return 2
  fi
  if [ "${SKILLMAXX_INSTALL_SCHEDULE:-}" != "yes" ]; then
    echo "Not installed. Set SKILLMAXX_INSTALL_SCHEDULE=yes to load the launchd job."
    return 2
  fi
  if [ "${SKILLMAXX_GROK_ROUTINE_PAUSED:-}" != "yes" ]; then
    echo "Not installed. Pause the Grok Bot routine \"SkillMaxx nightly refresh\" yourself, then set SKILLMAXX_GROK_ROUTINE_PAUSED=yes."
    echo "This script cannot disable that routine and does not claim it is off."
    return 2
  fi
  if ! cmd_preflight; then
    echo "Not installed. Preflight is blocked, so a 2:00 job would fail."
    return 1
  fi
  mkdir -p "${HOME}/Library/LaunchAgents" "$ROOT/testing/logs"
  cmd_print_plist > "$PLIST"
  uid=$(id -u)
  launchctl bootout "gui/${uid}/${LABEL}" 2>/dev/null || true
  launchctl bootstrap "gui/${uid}" "$PLIST"
  echo "Installed $PLIST at 02:00 local time. The Grok routine was not disabled by this command."
}

cmd_uninstall() {
  if [ "$(uname -s)" != "Darwin" ]; then
    echo "Not uninstalled. uninstall runs only on macOS. This machine is $(uname -s)."
    echo "The Grok Bot routine was not changed."
    return 2
  fi
  uid=$(id -u)
  launchctl bootout "gui/${uid}/${LABEL}" 2>/dev/null || launchctl unload -w "$PLIST" 2>/dev/null || true
  rm -f "$PLIST"
  echo "Removed $LABEL if it was loaded. The Grok routine was not changed. Turn it back on yourself if you still want it."
}

cmd_status() {
  echo "Machine: $(uname -s). Label: $LABEL"
  if [ "$(uname -s)" != "Darwin" ]; then
    echo "No launchd job is managed here. Install was not run."
    return 0
  fi
  if [ -f "$PLIST" ]; then
    echo "Plist present: $PLIST"
  else
    echo "Plist absent: $PLIST"
  fi
  uid=$(id -u)
  launchctl print "gui/${uid}/${LABEL}" >/dev/null 2>&1 && echo "launchd: loaded" || echo "launchd: not loaded"
}

cmd_test() {
  tmp=$(mktemp -d)
  trap 'rm -rf "$tmp"' EXIT
  export SKILLMAXX_LOCKDIR="$tmp/lock"
  # Fixture: two locks in this temp dir. Not the live /tmp/skillmaxx-nightly.lockdir.
  ( . "$ROOT/testing/lock.sh"; skillmaxx_lock >/dev/null; sleep 30 ) &
  holder=$!
  i=0
  while [ "$i" -lt 30 ]; do
    if [ -f "$tmp/lock/pid" ] && kill -0 "$(cat "$tmp/lock/pid")" 2>/dev/null; then
      break
    fi
    i=$((i + 1))
    sleep 0.1
  done
  set +e
  ( . "$ROOT/testing/lock.sh"; skillmaxx_lock >/dev/null )
  rc=$?
  kill "$holder" 2>/dev/null
  wait "$holder" 2>/dev/null
  if [ "$rc" != 3 ]; then
    echo "fixture lock self-test failed (rc=$rc)"
    return 1
  fi
  echo "fixture: second lock refused while the first was held"
  echo "live preflight for this machine:"
  cmd_preflight
  prc=$?
  echo "preflight_exit=$prc"
  echo "live dry-run:"
  cmd_dry_run >/dev/null
  echo "dry-run completed without executing nightly.sh"
  return 0
}

usage() {
  echo "Usage: testing/mac_nightly.sh {steps|preflight|dry-run|test|run|print-plist|install|uninstall|status}" >&2
  return 2
}

cmd=${1:-steps}
case "$cmd" in
  steps) cmd_steps ;;
  preflight) cmd_preflight ;;
  dry-run) cmd_dry_run ;;
  test) cmd_test ;;
  run) cmd_run ;;
  print-plist) cmd_print_plist ;;
  install) cmd_install ;;
  uninstall) cmd_uninstall ;;
  status) cmd_status ;;
  *) usage ;;
esac
