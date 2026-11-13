#!/bin/bash
# Mac/local entry for the existing mechanical nightly. Does not install a schedule
# unless you run "install" on macOS with the two confirmation variables set.
# Does not disable the Grok Bot routine. Does not send mail, posts, or newsletters.
# Usage: testing/mac_nightly.sh {steps|preflight|dry-run|test|run|local|print-plist|install|uninstall|status}
# install loads a local-only 02:00 America/New_York job. It does not push and does not disable the Grok routine.
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

apply_mode() {
  # Mac entry only. Direct testing/nightly.sh still checks out master unless SKILLMAXX_TRIAL=1.
  dry=${1:-apply}
  if [ "${SKILLMAXX_PRODUCTION:-}" = "yes" ] && [ "${SKILLMAXX_ALLOW_PUSH:-}" = "yes" ]; then
    if [ "$dry" = "dry" ]; then
      echo "Would checkout master and git push. That is production sync, not a trial."
    else
      unset SKILLMAXX_TRIAL
      echo "PRODUCTION=yes and ALLOW_PUSH=yes: nightly.sh will checkout master and may push."
    fi
    return
  fi
  if [ "${SKILLMAXX_PRODUCTION:-}" = "yes" ]; then
    echo "PRODUCTION=yes ignored because ALLOW_PUSH is not yes."
  fi
  if [ "$dry" = "dry" ]; then
    echo "Would set SKILLMAXX_TRIAL=1 and NOPUSH=1. The current branch stays. No fetch, checkout, pull, or push."
  else
    export SKILLMAXX_TRIAL=1
    export NOPUSH=1
    echo "TRIAL=1: stay on the current branch. No fetch, checkout, pull, or push."
  fi
}

say_dependencies() {
  cat <<'EOF'
Mechanical steps inside testing/nightly.sh (same behavior as the Grok routine's script):
  1. git fetch, checkout master, fast-forward pull. Needs the git credentials this machine already has. This script does not create or change credentials.
  2. Update local marketplace mirrors when they exist: Codex (SKILLMAXX_AGENTS/codex-mirror, then rename it to openai-plugins-mirror) and the Claude official catalog (SKILLMAXX_AGENTS/claude-plugins-official, cloned if missing, pulled only, not renamed). Then rebuild the Claude, Grok, and Codex templates. Claude reserves the name claude-plugins-official for anthropics GitHub sources, so the Claude template uses `claude plugin marketplace add anthropics/claude-plugins-official`. The Grok template is a separate home that registers the local directory with `grok plugin marketplace add`. A Grok home created by Claude's GitHub marketplace add keeps that URL, and Grok re-scans GitHub on every install.
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

The Grok routine keeps assistant work and publishing. This schedule does not turn it off and does not push.
  1. From the trial checkout (stay on this branch; do not checkout master):
     git fetch origin cursor/local-freshness-status-74c8
     git merge --ff-only origin/cursor/local-freshness-status-74c8
     python3 -m venv .venv && .venv/bin/pip install pillow && npm ci
     export PATH="$PWD/.venv/bin:$PATH"
     docker build --platform linux/arm64 -t skillmaxx-sandbox:local -f testing/sandbox/Dockerfile testing/sandbox
     Copy testing/local.env.example to testing/local.env and set SKILLMAXX_AGENTS to a directory under your home.
     Do not set SKILLMAXX_PRODUCTION or SKILLMAXX_ALLOW_PUSH for the trial.
     bash testing/setup_agents.sh
  4. bash testing/mac_nightly.sh preflight
  5. Trial: bash testing/mac_nightly.sh run
     That sets SKILLMAXX_TRIAL=1. The branch is kept. There is no fetch, checkout, pull, or push.
     A data commit, if any, stays on this branch. master is not updated.
  6. Read testing/logs/nightly-<date>.log and run: python3 testing/freshness.py
  7. One immediate local run, then the 02:00 America/New_York job. Neither pushes or checks out master:
     bash testing/mac_nightly.sh local
     SKILLMAXX_INSTALL_SCHEDULE=yes bash testing/mac_nightly.sh install
     Do not set SKILLMAXX_PRODUCTION or SKILLMAXX_ALLOW_PUSH.
     Each run fast-forwards a disposable worktree to origin/$SKILLMAXX_SOURCE_REF (default: this branch). After this PR is on master, set SKILLMAXX_SOURCE_REF=master in testing/local.env so the catalog is not stuck on the PR branch. That fetch does not push.
     Durable files: ~/.local/share/skillmaxx/ (logs, results, status, source.json).
     The trial checkout and its data commit are not reset.

Install (macOS only. This cloud VM cannot load launchd):
  SKILLMAXX_INSTALL_SCHEDULE=yes bash testing/mac_nightly.sh install
  Launchd wakes hourly and the script runs only when America/New_York hour is 02. It does not use RunAtLoad. Assistant catalog, QA, and publishing stay on the Grok routine.

Verify the morning after the first scheduled run:
  - One testing/logs/nightly-<date>.log, with a done line or a NIGHTLY FAILED line.
  - python3 testing/freshness.py --check-public
  - The Grok routine did not also write a run (still paused).
  - If push was allowed: published_at comes from GitHub Pages, not from the local build.

Rollback on the Mac:
  bash testing/mac_nightly.sh uninstall
  Uninstall removes the launchd job only. It does not re-enable or disable the Grok routine. Turn that routine back on yourself if you still want it.

Non-secret config: testing/local.env (see testing/local.env.example).
  SKILLMAXX_AGENTS   templates, codex mirror, and claude-plugins-official mirror, under your home on a Mac. Default /workspace/agents.
  SKILLMAXX_TRIAL=1   mac_nightly.sh run sets this unless both production flags are yes.
  SKILLMAXX_PRODUCTION=yes and SKILLMAXX_ALLOW_PUSH=yes   together: checkout master and push. Do not set these for the trial.

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
  if [ -d "$SKILLMAXX_AGENTS/claude-plugins-official" ]; then
    check 0 "claude mirror" "$SKILLMAXX_AGENTS/claude-plugins-official"
  else
    check 0 "claude mirror" "missing; nightly.sh already continues without it and says so. Grok Claude-catalog installs need this local path."
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
    if docker run --rm "$img" sh -c 'command -v uvx' >/dev/null 2>&1; then
      check 0 "uvx in image" "Python MCP servers can start"
    else
      check 0 "uvx in image" "MISSING. Python MCP servers (mcp-time, mcp-fetch, mcp-git, claimidx) will fail and the 4 AM import holds. Fix: docker build -t $img -f testing/sandbox/Dockerfile.add-uv testing/sandbox"
    fi
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
  apply_mode dry
  echo "Dry run finished. Nothing was executed."
}

cmd_run() {
  load_env
  apply_mode
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
  <string>Local SkillMaxx tests, metadata, reports, build, and freshness at 02:00 America/New_York. No git push and no master checkout. Does not disable the Grok Bot routine. Assistant catalog, QA, and publishing stay with that routine.</string>
  <key>WorkingDirectory</key>
  <string>$ROOT</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>$ROOT/testing/mac_nightly.sh</string>
    <string>local</string>
    <string>--launchd</string>
  </array>
  <key>StartCalendarInterval</key>
  <array>
$(h=0; while [ "$h" -lt 24 ]; do printf '    <dict><key>Hour</key><integer>%s</integer><key>Minute</key><integer>0</integer></dict>\n' "$h"; h=$((h + 1)); done)
  </array>
  <key>StandardOutPath</key>
  <string>$HOME/.local/share/skillmaxx/logs/launchd.log</string>
  <key>StandardErrorPath</key>
  <string>$HOME/.local/share/skillmaxx/logs/launchd.log</string>
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
    echo "Not installed. Set SKILLMAXX_INSTALL_SCHEDULE=yes to load the local-only launchd job."
    return 2
  fi
  if ! bash "$ROOT/testing/local_nightly.sh" --docker-check; then
    echo "Not installed. Docker is not ready, so the 02:00 Eastern job would fail."
    return 1
  fi
  mkdir -p "${HOME}/Library/LaunchAgents" "$HOME/.local/share/skillmaxx/logs"
  cmd_print_plist > "$PLIST"
  uid=$(id -u)
  launchctl bootout "gui/${uid}/${LABEL}" 2>/dev/null || true
  launchctl bootstrap "gui/${uid}" "$PLIST"
  echo "Installed $PLIST. It runs at 02:00 America/New_York and does not push. The Grok routine was not disabled."
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
  echo "Usage: testing/mac_nightly.sh {steps|preflight|dry-run|test|run|local|print-plist|install|uninstall|status}" >&2
  return 2
}

cmd=${1:-steps}
case "$cmd" in
  steps) cmd_steps ;;
  preflight) cmd_preflight ;;
  dry-run) cmd_dry_run ;;
  test) cmd_test ;;
  run) cmd_run ;;
  local) shift; exec bash "$ROOT/testing/local_nightly.sh" "$@" ;;
  print-plist) cmd_print_plist ;;
  install) cmd_install ;;
  uninstall) cmd_uninstall ;;
  status) cmd_status ;;
  *) usage ;;
esac
