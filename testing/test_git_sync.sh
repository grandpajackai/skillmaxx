#!/bin/bash
# Real git repos for trial branch preservation and production sync failure. No network.
set -uo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
fail() { echo "FAIL: $*" >&2; exit 1; }
bash -n testing/git_sync.sh || fail syntax
grep -q 'skillmaxx_sync' testing/nightly.sh || fail nightly_calls_sync
grep -q 'git checkout' testing/nightly.sh && fail nightly_checks_out_inline
grep -q 'TRIAL: not pushing' testing/nightly.sh || fail trial_skips_push

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
origin="$tmp/origin"
work="$tmp/work"
git init -q -b master "$origin"
git -C "$origin" config user.email t@example.com
git -C "$origin" config user.name t
echo a > "$origin/a"
git -C "$origin" add a
git -C "$origin" commit -qm a
git clone -q "$origin" "$work"
git -C "$work" config user.email t@example.com
git -C "$work" config user.name t
git -C "$work" checkout -q -b cursor/local-freshness-status-74c8
base=$(git -C "$work" rev-parse HEAD)

# Trial does not contact a broken origin and does not leave the branch.
git -C "$work" remote set-url origin "$origin/missing"
(
  cd "$work"
  unset NOPUSH
  SKILLMAXX_TRIAL=1
  # shellcheck disable=SC1091
  . "$ROOT/testing/git_sync.sh"
  skillmaxx_sync
  printf 'NOPUSH=%s\n' "$NOPUSH"
) >"$tmp/trial.txt" || fail trial_sync
grep -q 'staying on cursor/local-freshness-status-74c8' "$tmp/trial.txt" || fail trial_message
grep -q 'NOPUSH=1' "$tmp/trial.txt" || fail trial_nopush
[ "$(git -C "$work" rev-parse --abbrev-ref HEAD)" = "cursor/local-freshness-status-74c8" ] || fail trial_branch
[ "$(git -C "$work" rev-parse HEAD)" = "$base" ] || fail trial_head

# Production fetch failure happens before checkout, so the branch stays.
(
  cd "$work"
  unset SKILLMAXX_TRIAL
  # shellcheck disable=SC1091
  . "$ROOT/testing/git_sync.sh"
  skillmaxx_sync
) >"$tmp/fetch-fail.txt" 2>&1 && fail fetch_should_fail
[ "$(git -C "$work" rev-parse --abbrev-ref HEAD)" = "cursor/local-freshness-status-74c8" ] || fail fetch_switched
[ "$(git -C "$work" rev-parse HEAD)" = "$base" ] || fail fetch_moved

# Diverged master: production checks out master, then ff-only pull fails.
git -C "$work" remote set-url origin "$origin"
git -C "$work" checkout -q master
echo b >> "$work/a"
git -C "$work" add a
git -C "$work" commit -qm b
echo c > "$origin/c"
git -C "$origin" add c
git -C "$origin" commit -qm c
git -C "$work" checkout -q -b feature
(
  cd "$work"
  unset SKILLMAXX_TRIAL
  # shellcheck disable=SC1091
  . "$ROOT/testing/git_sync.sh"
  skillmaxx_sync
) >"$tmp/ff.txt" 2>&1 && fail ff_should_fail
[ "$(git -C "$work" rev-parse --abbrev-ref HEAD)" = "master" ] || fail ff_not_on_master

# The same divergence does not move a trial branch.
git -C "$work" checkout -q feature
feature_head=$(git -C "$work" rev-parse HEAD)
(
  cd "$work"
  SKILLMAXX_TRIAL=1
  # shellcheck disable=SC1091
  . "$ROOT/testing/git_sync.sh"
  skillmaxx_sync
) >"$tmp/trial-feature.txt" || fail trial_feature
[ "$(git -C "$work" rev-parse --abbrev-ref HEAD)" = "feature" ] || fail trial_feature_branch
[ "$(git -C "$work" rev-parse HEAD)" = "$feature_head" ] || fail trial_feature_head

# Trial on master is refused with no reset.
git -C "$work" checkout -q master
master_head=$(git -C "$work" rev-parse HEAD)
(
  cd "$work"
  SKILLMAXX_TRIAL=1
  # shellcheck disable=SC1091
  . "$ROOT/testing/git_sync.sh"
  skillmaxx_sync
) >"$tmp/trial-master.txt" 2>&1 && fail trial_master_should_fail
grep -q 'refuses branch master' "$tmp/trial-master.txt" || fail trial_master_message
[ "$(git -C "$work" rev-parse --abbrev-ref HEAD)" = "master" ] || fail trial_master_branch
[ "$(git -C "$work" rev-parse HEAD)" = "$master_head" ] || fail trial_master_head
(
  cd "$work"
  SKILLMAXX_TRIAL=1
  # shellcheck disable=SC1091
  . "$ROOT/testing/git_sync.sh"
  skillmaxx_trial_commit_ok
) >"$tmp/commit-master.txt" 2>&1 && fail commit_master_should_fail

# Dirty trial branch is refused and the edit is left in place.
git -C "$work" checkout -q feature
echo dirt >> "$work/a"
(
  cd "$work"
  SKILLMAXX_TRIAL=1
  # shellcheck disable=SC1091
  . "$ROOT/testing/git_sync.sh"
  skillmaxx_sync
) >"$tmp/dirty.txt" 2>&1 && fail dirty_should_fail
grep -q 'dirty worktree' "$tmp/dirty.txt" || fail dirty_message
[ "$(git -C "$work" rev-parse --abbrev-ref HEAD)" = "feature" ] || fail dirty_branch
grep -q dirt "$work/a" || fail dirty_edit_lost

echo "ok git sync trial and failure checks"
