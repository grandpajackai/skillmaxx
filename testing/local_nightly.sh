#!/bin/bash
# Local-only mechanical nightly. No git push, no master checkout, no data commit.
# Updates one disposable worktree from SKILLMAXX_SOURCE_REF, runs nightly.sh there
# with SKILLMAXX_LOCAL=1, and copies logs, results, and freshness to SKILLMAXX_STATE.
# Does not reset the primary checkout. Called by testing/mac_nightly.sh local.
set -uo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
PRIMARY=${SKILLMAXX_PRIMARY:-$ROOT}
ENV_FILE=${SKILLMAXX_ENV_FILE:-$PRIMARY/testing/local.env}
if [ -f "$ENV_FILE" ]; then
  set -a
  # shellcheck disable=SC1090
  . "$ENV_FILE"
  set +a
fi
PRIMARY=${SKILLMAXX_PRIMARY:-$ROOT}
STATE=${SKILLMAXX_STATE:-$HOME/.local/share/skillmaxx}
WORK=${SKILLMAXX_WORKTREE:-$STATE/work}
REF=${SKILLMAXX_SOURCE_REF:-$(git -C "$PRIMARY" rev-parse --abbrev-ref HEAD)}
IMAGE=${SKILLMAXX_SANDBOX_IMAGE:-skillmaxx-sandbox:local}
LOGDIR="$STATE/logs"
mkdir -p "$LOGDIR" "$STATE/results"
# First run keeps the primary checkout's existing results (including a trial data commit) without moving that checkout.
if [ -z "$(ls -A "$STATE/results" 2>/dev/null)" ] && [ -d "$PRIMARY/testing/results" ]; then
  cp -a "$PRIMARY/testing/results/." "$STATE/results/" 2>/dev/null || true
fi
if [ ! -f "$STATE/history.json" ] && [ -f "$PRIMARY/testing/history.json" ]; then
  cp "$PRIMARY/testing/history.json" "$STATE/history.json"
fi
export SKILLMAXX_AGENTS="${SKILLMAXX_AGENTS:-/workspace/agents}"

fail() { echo "local nightly: $*" >&2; exit 1; }

if [ "${1:-}" = "--docker-check" ]; then
  command -v docker >/dev/null 2>&1 || fail "docker CLI is missing. Not starting Docker."
  docker info >/dev/null 2>&1 || fail "Docker daemon is not running. Not starting Docker."
  docker image inspect "$IMAGE" >/dev/null 2>&1 || fail "local image $IMAGE is missing."
  echo "local nightly: Docker is ready for $IMAGE"
  exit 0
fi

if [ "${1:-}" = "--launchd" ] || [ "${SKILLMAXX_LAUNCHD:-}" = "1" ]; then
  hour=${SKILLMAXX_EASTERN_HOUR:-$(TZ=America/New_York date +%H)}
  today=${SKILLMAXX_EASTERN_DATE:-$(TZ=America/New_York date +%F)}
  if [ "$hour" != "02" ]; then
    echo "local nightly: America/New_York hour is $hour, not 02. Not running."
    exit 0
  fi
  if [ -f "$STATE/last-success-date" ] && [ "$(cat "$STATE/last-success-date")" = "$today" ]; then
    echo "local nightly: already succeeded on $today Eastern. Not running again."
    exit 0
  fi
fi

command -v git >/dev/null 2>&1 || fail "git is missing"
primary_top=$(git -C "$PRIMARY" rev-parse --show-toplevel) || fail "primary checkout is not a git repo"
if [ "${SKILLMAXX_SKIP_DOCKER:-}" != "1" ]; then
  command -v docker >/dev/null 2>&1 || fail "docker CLI is missing. Not starting Docker."
  docker info >/dev/null 2>&1 || fail "Docker daemon is not running. Not starting Docker."
  docker image inspect "$IMAGE" >/dev/null 2>&1 || fail "local image $IMAGE is missing. Build it before relying on the schedule."
fi

# shellcheck source=testing/lock.sh
. "$ROOT/testing/lock.sh"
skillmaxx_lock || exit 3
trap 'skillmaxx_unlock' EXIT

write_source() {
  python3 - "$STATE/source.json" "$1" "$2" "$3" "$4" << 'PY'
import json, sys
path, ref, sha, sync, master = sys.argv[1:]
json.dump({
    "source_ref": ref,
    "source_sha": sha,
    "source_sync": sync,
    "origin_master_sha": None if master in ("", "unknown") else master,
}, open(path, "w"), indent=2)
open(path, "a").write("\n")
PY
}

git -C "$PRIMARY" fetch -q origin "$REF" || { write_source "$REF" "" failed ""; fail "fetch origin/$REF failed. Not running tests on an unknown revision."; }
git -C "$PRIMARY" fetch -q origin master >/dev/null 2>&1 || true
master_sha=$(git -C "$PRIMARY" rev-parse --verify --quiet origin/master || echo unknown)
if [ ! -e "$WORK/.git" ]; then
  mkdir -p "$(dirname "$WORK")"
  git -C "$PRIMARY" worktree add --detach "$WORK" "origin/$REF" || fail "could not add worktree $WORK"
fi
work_top=$(git -C "$WORK" rev-parse --show-toplevel) || fail "worktree is not a git checkout"
if [ "$work_top" = "$primary_top" ]; then
  fail "refusing to clean the primary checkout $primary_top"
fi
ahead=$(git -C "$WORK" rev-list --count "origin/$REF..HEAD" || echo 1)
if [ "$ahead" != "0" ]; then
  sha=$(git -C "$WORK" rev-parse HEAD)
  write_source "$REF" "$sha" "blocked" "$master_sha"
  fail "worktree $WORK has $ahead local commit(s) not in origin/$REF. Not resetting them."
fi
git -C "$WORK" checkout -q -- . || fail "could not restore generated files in the disposable worktree"
git -C "$WORK" clean -fd -e node_modules -e .venv >/dev/null || fail "could not clear untracked files in the disposable worktree"
git -C "$WORK" merge -q --ff-only "origin/$REF" || { write_source "$REF" "$(git -C "$WORK" rev-parse HEAD)" failed "$master_sha"; fail "origin/$REF is not a fast-forward. Not resetting."; }
sha=$(git -C "$WORK" rev-parse HEAD)
write_source "$REF" "$sha" ok "$master_sha"
mkdir -p "$WORK/testing"
cp "$STATE/source.json" "$WORK/testing/source.json"

if [ -d "$STATE/results" ]; then
  mkdir -p "$WORK/testing/results"
  cp -a "$STATE/results/." "$WORK/testing/results/" 2>/dev/null || true
fi
[ -f "$STATE/history.json" ] && cp "$STATE/history.json" "$WORK/testing/history.json"
if [ -d "$PRIMARY/node_modules" ] && [ ! -e "$WORK/node_modules" ]; then
  ln -s "$PRIMARY/node_modules" "$WORK/node_modules"
fi
if [ -x "$PRIMARY/.venv/bin/python3" ]; then
  PATH="$PRIMARY/.venv/bin:$PATH"
fi
if [ -d /opt/homebrew/bin ]; then
  PATH="/opt/homebrew/bin:$PATH"
fi
export PATH SKILLMAXX_LOCAL=1 SKILLMAXX_TRIAL=1 NOPUSH=1 SKILLMAXX_SOURCE_REF="$REF" SKILLMAXX_SOURCE_SYNC=ok SKILLMAXX_EXTERNAL_LOCK=1
unset SKILLMAXX_PRODUCTION SKILLMAXX_ALLOW_PUSH

nightly=${SKILLMAXX_NIGHTLY:-$WORK/testing/nightly.sh}
( cd "$WORK" && bash "$nightly" ) || fail "nightly.sh failed. No push was attempted."

mkdir -p "$LOGDIR" "$STATE/results" "$STATE/status"
if [ -d "$WORK/testing/logs" ]; then
  cp -a "$WORK/testing/logs/." "$LOGDIR/" 2>/dev/null || true
fi
if [ -d "$WORK/testing/results" ]; then
  cp -a "$WORK/testing/results/." "$STATE/results/"
fi
[ -f "$WORK/testing/history.json" ] && cp "$WORK/testing/history.json" "$STATE/history.json"
[ -f "$WORK/src/_data/reports.json" ] && cp "$WORK/src/_data/reports.json" "$STATE/reports.json"
if [ -d "$WORK/testing/status" ]; then
  cp -a "$WORK/testing/status/." "$STATE/status/"
fi
if [ "${1:-}" = "--launchd" ] || [ "${SKILLMAXX_LAUNCHD:-}" = "1" ]; then
  TZ=America/New_York date +%F > "$STATE/last-success-date"
fi
echo "local nightly: source $REF $sha copied to $STATE. No commit and no push."
