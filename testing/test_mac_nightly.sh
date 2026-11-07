#!/bin/bash
# Fixture checks for testing/mac_nightly.sh. No git pull, no tests, no launchd load.
set -uo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"
fail() { echo "FAIL: $*" >&2; exit 1; }

bash -n testing/mac_nightly.sh || fail syntax_mac
bash -n testing/nightly.sh || fail syntax_nightly
bash -n testing/lock.sh || fail syntax_lock

grep -q 'skillmaxx_lock' testing/nightly.sh || fail nightly_lock
grep -q 'flock' testing/nightly.sh && fail nightly_still_uses_flock
grep -q 'SKILLMAXX_AGENTS' testing/nightly.sh || fail agents_env
grep -q 'SKILLMAXX_AGENTS:-/workspace/agents' testing/sbx.sh || fail sbx_default

# Install and uninstall must refuse on this non-Mac and must not write a plist.
if bash testing/mac_nightly.sh install >/tmp/smx-install.txt 2>&1; then fail install_should_fail; fi
grep -q 'macOS' /tmp/smx-install.txt || fail install_message
[ ! -f "${HOME}/Library/LaunchAgents/com.gilventures.skillmaxx.nightly.plist" ] || fail plist_written
if bash testing/mac_nightly.sh uninstall >/tmp/smx-uninstall.txt 2>&1; then fail uninstall_should_fail; fi
grep -q 'macOS' /tmp/smx-uninstall.txt || fail uninstall_message

# Plist text is printable here and must not start a run on load.
bash testing/mac_nightly.sh print-plist >/tmp/smx-plist.xml || fail print_plist
grep -q 'StartCalendarInterval' /tmp/smx-plist.xml || fail plist_schedule
grep -q '<integer>2</integer>' /tmp/smx-plist.xml || fail plist_hour
grep -q 'mac_nightly.sh' /tmp/smx-plist.xml || fail plist_script
grep -q 'Does not disable the Grok Bot routine' /tmp/smx-plist.xml || fail plist_cutover
grep -q 'RunAtLoad' /tmp/smx-plist.xml && fail plist_run_at_load

# Fixture lock: holder, refusal, then stale recovery after the holder is gone.
tmp=$(mktemp -d)
export SKILLMAXX_LOCKDIR="$tmp/lock"
( . testing/lock.sh; skillmaxx_lock >/dev/null; sleep 30 ) &
holder=$!
i=0
while [ "$i" -lt 30 ]; do
  if [ -f "$tmp/lock/pid" ] && kill -0 "$(cat "$tmp/lock/pid")" 2>/dev/null; then break; fi
  i=$((i + 1)); sleep 0.1
done
[ -f "$tmp/lock/pid" ] || fail lock_not_held
if ( . testing/lock.sh; skillmaxx_lock >/dev/null ); then fail second_lock_should_fail; fi
kill "$holder" 2>/dev/null || true
wait "$holder" 2>/dev/null || true
( . testing/lock.sh; skillmaxx_lock ) >"$tmp/stale.txt" || fail stale_acquire
grep -q 'removed stale nightly lock' "$tmp/stale.txt" || fail stale_message
( . testing/lock.sh; skillmaxx_unlock )
rm -rf "$tmp"
unset SKILLMAXX_LOCKDIR

# Push gate is a fixture stub. It must not call the real nightly.
stub=$(mktemp)
cat > "$stub" << 'EOF'
#!/bin/bash
printf 'NOPUSH=%s\n' "${NOPUSH-unset}"
EOF
chmod +x "$stub"
out=$(SKILLMAXX_ENV_FILE=/dev/null SKILLMAXX_SKIP_PREFLIGHT=1 SKILLMAXX_NIGHTLY="$stub" bash testing/mac_nightly.sh run)
echo "$out" | grep -q 'NOPUSH=1' || fail push_gate
out=$(SKILLMAXX_ENV_FILE=/dev/null SKILLMAXX_ALLOW_PUSH=yes SKILLMAXX_SKIP_PREFLIGHT=1 SKILLMAXX_NIGHTLY="$stub" bash testing/mac_nightly.sh run)
echo "$out" | grep -q 'NOPUSH=unset' || fail allow_push
rm -f "$stub"

# Live on this machine: dry-run and a refused run must not move HEAD.
before=$(git rev-parse HEAD)
dirty=$(git status --porcelain | grep -v '__pycache__' || true)
bash testing/mac_nightly.sh dry-run >/tmp/smx-dry.txt || fail dry_run
grep -q 'bubblewrap' /tmp/smx-dry.txt || fail dry_bwrap
grep -q 'unsandboxed' /tmp/smx-dry.txt || fail dry_no_host_fallback
grep -q 'does not send' /tmp/smx-dry.txt || fail dry_send
grep -q 'build_data.py' /tmp/smx-dry.txt || fail dry_build_data
if SKILLMAXX_ENV_FILE=/dev/null bash testing/mac_nightly.sh run >/tmp/smx-run.txt 2>&1; then fail run_should_block; fi
grep -q 'nightly.sh was not started' /tmp/smx-run.txt || fail run_refusal
after=$(git rev-parse HEAD)
[ "$before" = "$after" ] || fail head_moved
now=$(git status --porcelain | grep -v '__pycache__' || true)
[ "$dirty" = "$now" ] || fail worktree_changed

echo "ok fixture+live mac nightly checks"
echo "LIVE preflight (this VM, not a Mac install):"
bash testing/mac_nightly.sh preflight > /tmp/smx-preflight.txt || true
grep -E '^(ok|blocked|preflight:)' /tmp/smx-preflight.txt
