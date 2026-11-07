#!/bin/bash
# Repeatable local nightly: fast-forward a disposable worktree, never push, never reset the primary checkout.
set -uo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
fail() { echo "FAIL: $*" >&2; exit 1; }
bash -n "$ROOT/testing/local_nightly.sh" || fail syntax
bash -n "$ROOT/testing/nightly.sh" || fail nightly_syntax

# Outside 02:00 Eastern the launchd entry exits without touching git.
out=$(SKILLMAXX_LAUNCHD=1 SKILLMAXX_EASTERN_HOUR=15 bash "$ROOT/testing/local_nightly.sh" 2>&1) || fail hour_gate_failed
echo "$out" | grep -q 'not 02' || fail hour_gate_message

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
origin="$tmp/origin"
primary="$tmp/primary"
work="$tmp/work"
state="$tmp/state"
git init -q -b src "$origin"
git -C "$origin" config user.email t@example.com
git -C "$origin" config user.name t
echo v1 > "$origin/README"
git -C "$origin" add README
git -C "$origin" commit -qm v1
git clone -q "$origin" "$primary"
git -C "$primary" config user.email t@example.com
git -C "$primary" config user.name t
echo kept > "$primary/trial-data"
git -C "$primary" add trial-data
git -C "$primary" commit -qm 'local trial data'
kept=$(git -C "$primary" rev-parse HEAD)
origin_n=$(git -C "$origin" rev-list --count HEAD)

cat > "$tmp/stub.sh" << 'EOF'
#!/bin/bash
mkdir -p testing/results testing/logs
echo out >> testing/results/kept.txt
echo dirty >> README
day=$(date +%F)
printf '== %s 02:00:00 UTC local source\nLOCAL: not pushing\n== %s 02:00:01 UTC done\n1 / 2 pass\n' "$day" "$day" > "testing/logs/nightly-$day.log"
EOF
chmod +x "$tmp/stub.sh"

run() {
  SKILLMAXX_PRIMARY="$primary" SKILLMAXX_STATE="$state" SKILLMAXX_WORKTREE="$work" \
    SKILLMAXX_SOURCE_REF=src SKILLMAXX_ENV_FILE=/dev/null SKILLMAXX_SKIP_DOCKER=1 \
    SKILLMAXX_NIGHTLY="$tmp/stub.sh" SKILLMAXX_LOCKDIR="$tmp/lock" \
    bash "$ROOT/testing/mac_nightly.sh" local
}

run >/tmp/local1.txt || fail first_run
run >/tmp/local2.txt || fail second_run
[ "$(git -C "$primary" rev-parse HEAD)" = "$kept" ] || fail primary_moved
[ "$(git -C "$origin" rev-list --count HEAD)" = "$origin_n" ] || fail pushed
[ -f "$state/results/kept.txt" ] || fail results_not_durable
grep -q '"source_sync": "ok"' "$state/source.json" || fail source_sync
grep -q '"source_ref": "src"' "$state/source.json" || fail source_ref
first_sha=$(git -C "$work" rev-parse HEAD)

echo v2 >> "$origin/README"
git -C "$origin" add README
git -C "$origin" commit -qm v2
run >/tmp/local3.txt || fail third_run
[ "$(git -C "$work" rev-parse HEAD)" = "$(git -C "$origin" rev-parse HEAD)" ] || fail did_not_fast_forward
[ "$(git -C "$work" rev-parse HEAD)" != "$first_sha" ] || fail sha_unchanged
[ "$(git -C "$primary" rev-parse HEAD)" = "$kept" ] || fail primary_moved_after_update
grep -q "$(git -C "$origin" rev-parse HEAD)" "$state/source.json" || fail source_sha
[ "$(git -C "$origin" rev-list --count HEAD)" = "$((origin_n + 1))" ] || fail origin_count

# A local commit in the disposable worktree is kept and blocks the next run. No reset.
echo stray > "$work/stray"
git -C "$work" add stray
git -C "$work" -c user.email=t@example.com -c user.name=t commit -qm stray
stray=$(git -C "$work" rev-parse HEAD)
if run >/tmp/local-blocked.txt 2>&1; then fail should_block_local_commit; fi
grep -q 'Not resetting' /tmp/local-blocked.txt || fail block_message
[ "$(git -C "$work" rev-parse HEAD)" = "$stray" ] || fail stray_reset
[ "$(git -C "$primary" rev-parse HEAD)" = "$kept" ] || fail primary_reset

# Plist is local-only and fires hourly so 02:00 Eastern does not depend on the Mac timezone.
bash "$ROOT/testing/mac_nightly.sh" print-plist >/tmp/smx-plist.xml || fail plist
grep -q 'local' /tmp/smx-plist.xml || fail plist_local
grep -q -- '--launchd' /tmp/smx-plist.xml || fail plist_launchd
grep -q 'America/New_York' /tmp/smx-plist.xml || fail plist_eastern
grep -q 'No git push' /tmp/smx-plist.xml || fail plist_nopush
grep -q 'Does not disable the Grok Bot routine' /tmp/smx-plist.xml || fail plist_assistant
grep -q 'SKILLMAXX_PRODUCTION' /tmp/smx-plist.xml && fail plist_production
grep -q 'RunAtLoad' /tmp/smx-plist.xml && fail plist_run_at_load
grep -c '<key>Hour</key>' /tmp/smx-plist.xml | grep -q '^24$' || fail plist_hours

echo "ok local nightly repeat, update, and no-push checks"
