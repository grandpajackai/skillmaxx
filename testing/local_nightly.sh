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

export SKILLMAXX_STATE="$STATE"
# shellcheck source=testing/nightly_alert.sh
. "$ROOT/testing/nightly_alert.sh"
STEP=setup
RUNLOG=
ALERT_ON_FAIL=0
fail() { echo "local nightly: $*" >&2; FAIL_MSG="$*"; exit 1; }

pin_image() {
  # Run every sandbox case by the resolved image ID so a short-name lookup that breaks mid-run
  # cannot stop sbx.sh. The recorded sandbox label stays "skillmaxx-sandbox:local".
  pid_img=$(docker image inspect --format '{{.Id}}' "$1" 2>/dev/null)
  export SKILLMAXX_SANDBOX_IMAGE="${pid_img:-$1}"
  echo "local nightly: sandbox image $1 -> ${SKILLMAXX_SANDBOX_IMAGE}"
}

docker_ready() {
  # Docker CLI and daemon. Clear message when Docker Desktop is closed; this script never starts it.
  STEP=docker
  command -v docker >/dev/null 2>&1 || fail "docker CLI is missing (not on PATH=$PATH). Install Docker Desktop or fix PATH in testing/local.env."
  docker info >/dev/null 2>&1 || fail "Docker Desktop is not running (docker info failed). Open Docker Desktop and leave it running; the nightly never starts Docker itself."
  STEP=image
  if docker image inspect "$IMAGE" >/dev/null 2>&1; then
    pin_image "$IMAGE"
    return 0
  fi
  # Self-heal: Docker 29 with the containerd image store sometimes stops resolving the short name
  # (Nov 15-16) while the image is still present under its full name. Re-tag it from its ID.
  echo "local nightly: short image name $IMAGE did not resolve; looking for the image under another name"
  id=
  case "$IMAGE" in
    */*) ;;
    *) id=$(docker image inspect --format '{{.Id}}' "docker.io/library/$IMAGE" 2>/dev/null) ;;
  esac
  if [ -z "$id" ]; then
    repo=${IMAGE%:*}; tag=${IMAGE##*:}; [ "$tag" = "$IMAGE" ] && tag=latest
    id=$(docker images --no-trunc --format '{{.Repository}}:{{.Tag}} {{.ID}}' 2>/dev/null | awk -v r="$repo" -v t="$tag" '{split($1,a,":"); n=a[1]; sub(/^docker\.io\/library\//,"",n); if (n==r && a[2]==t) {print $2; exit}}')
  fi
  [ -n "$id" ] || fail "local image $IMAGE is missing (not found under any name in docker images). Rebuild it from testing/sandbox before relying on the schedule."
  if docker tag "$id" "$IMAGE" >/dev/null 2>&1 && docker image inspect "$IMAGE" >/dev/null 2>&1; then
    echo "local nightly: self-heal re-tagged $id as $IMAGE"
    pin_image "$IMAGE"
    return 0
  fi
  # Re-tag did not stick: run the same image by its ID.
  docker image inspect "$id" >/dev/null 2>&1 || fail "local image $IMAGE could not be resolved (re-tag of $id failed)."
  echo "local nightly: self-heal using image ID $id for this run"
  IMAGE=$id
  export SKILLMAXX_SANDBOX_IMAGE="$id"
  return 0
}

on_exit() {
  rc=$?
  [ "${SKILLMAXX_LOCK_HELD:-}" = "1" ] && skillmaxx_unlock
  if [ "$ALERT_ON_FAIL" = "1" ]; then
    printf '%s %s\n' "$today" "$rc" > "$STATE/run-finished" 2>/dev/null
    if [ "$rc" != "0" ]; then
      sleep 1  # let tee flush this run's last lines into $RUNLOG
      step=$STEP
      if [ "$STEP" = "nightly.sh" ] && [ -n "$RUNLOG" ]; then
        s2=$(grep -o 'NIGHTLY FAILED at step: [^(]*' "$RUNLOG" 2>/dev/null | tail -1 | sed 's/NIGHTLY FAILED at step: //; s/ *$//')
        [ -n "$s2" ] && step="nightly.sh: $s2"
      fi
      smx_alert "$step" "${FAIL_MSG:-exit code $rc}" "$RUNLOG" "$today" || true
    fi
  fi
  return 0
}

# Hourly launchd watchdog (not 02): alert once a day from 05 ET on if today's 02 run never started
# (Mac asleep or off) or started and is still not finished.
watchdog() {
  [ "$((10#$hour))" -ge 5 ] || return 0
  [ -f "$STATE/watchdog-alerted" ] && [ "$(cat "$STATE/watchdog-alerted")" = "$today" ] && return 0
  [ -f "$STATE/last-success-date" ] && [ "$(cat "$STATE/last-success-date")" = "$today" ] && return 0
  started=$(cut -d' ' -f1 "$STATE/run-started" 2>/dev/null)
  finished=$(cut -d' ' -f1 "$STATE/run-finished" 2>/dev/null)
  if [ "$started" != "$today" ]; then
    step=not-started; msg="The 02:00 ET nightly did not start today (Mac asleep, off, or launchd missed it). Now ${hour}:00 ET."
  elif [ "$finished" != "$today" ]; then
    pid=$(cut -d' ' -f2 "$STATE/run-started" 2>/dev/null)
    if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
      step=still-running; msg="The nightly that started at 02:00 ET is still running at ${hour}:00 ET (pid $pid)."
    else
      step=died; msg="The nightly that started at 02:00 ET stopped without finishing (killed, crash, or the Mac slept)."
    fi
  else
    return 0  # finished with a failure: that run already alerted.
  fi
  echo "local nightly: watchdog: $msg"
  printf '%s\n' "$today" > "$STATE/watchdog-alerted"
  smx_alert "$step" "$msg" "$LOGDIR/run-$today.log" "$today" || true
  return 0
}

if [ "${1:-}" = "--docker-check" ]; then
  docker_ready
  echo "local nightly: Docker is ready for $IMAGE"
  exit 0
fi

if [ "${1:-}" = "--test-alert" ]; then
  # One wiring check. The payload says TEST ONLY so the routine can ignore it.
  smx_alert "test-alert" "TEST ONLY - alert wiring check, ignore" "" "$(TZ=America/New_York date +%F)"
  exit 0
fi

if [ "${1:-}" = "--launchd" ] || [ "${SKILLMAXX_LAUNCHD:-}" = "1" ]; then
  hour=${SKILLMAXX_EASTERN_HOUR:-$(TZ=America/New_York date +%H)}
  today=${SKILLMAXX_EASTERN_DATE:-$(TZ=America/New_York date +%F)}
  if [ "$hour" != "02" ]; then
    echo "local nightly: America/New_York hour is $hour, not 02. Not running."
    watchdog || true
    exit 0
  fi
  if [ -f "$STATE/last-success-date" ] && [ "$(cat "$STATE/last-success-date")" = "$today" ]; then
    echo "local nightly: already succeeded on $today Eastern. Not running again."
    exit 0
  fi
  # A real 02 ET run from here on: any non-zero exit, preflight included, sends one alert.
  ALERT_ON_FAIL=1
  RUNLOG="$LOGDIR/run-$today.log"
  : > "$RUNLOG"
  exec > >(tee -a "$RUNLOG") 2>&1
  printf '%s %s\n' "$today" "$(sh -c 'echo $PPID')" > "$STATE/run-started"
  echo "local nightly: 02 ET run for $today started $(TZ=America/New_York date '+%F %T %Z')"
fi
today=${today:-$(TZ=America/New_York date +%F)}
trap on_exit EXIT

STEP=preflight
command -v git >/dev/null 2>&1 || fail "git is missing"
primary_top=$(git -C "$PRIMARY" rev-parse --show-toplevel) || fail "primary checkout is not a git repo"
if [ "${SKILLMAXX_SKIP_DOCKER:-}" != "1" ]; then
  docker_ready
fi

# shellcheck source=testing/lock.sh
. "$ROOT/testing/lock.sh"
STEP=lock
skillmaxx_lock || { FAIL_MSG="another nightly holds the lock"; exit 3; }
STEP=git-sync

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

# Explicit refspecs: the Mac checkout's remote.origin.fetch only maps a deleted trial branch, so a bare
# "git fetch origin master" leaves origin/master stale and the run would test an old commit.
git -C "$PRIMARY" fetch -q origin "+refs/heads/$REF:refs/remotes/origin/$REF" || { write_source "$REF" "" failed ""; fail "fetch origin/$REF failed. Not running tests on an unknown revision."; }
git -C "$PRIMARY" fetch -q origin "+refs/heads/master:refs/remotes/origin/master" >/dev/null 2>&1 || true
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
STEP=nightly.sh
( cd "$WORK" && bash "$nightly" ) || fail "nightly.sh failed (tests, metadata, report, build, or freshness). No push was attempted."
STEP=copy-results

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
