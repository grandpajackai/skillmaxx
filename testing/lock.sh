# Portable nightly lock. Source from bash; do not execute.
# mkdir is atomic on macOS and Linux. flock(1) is not on macOS.
# The lock is local to this machine. It does not stop a second machine.
# bash 3.2 (the macOS system bash) does not update $$ inside a subshell, so the
# pid is taken from a child sh process's PPID.
skillmaxx_self_pid() { sh -c 'echo $PPID'; }
skillmaxx_lock() {
  LOCKDIR=${SKILLMAXX_LOCKDIR:-/tmp/skillmaxx-nightly.lockdir}
  if mkdir "$LOCKDIR" 2>/dev/null; then
    skillmaxx_self_pid > "$LOCKDIR/pid" || true
    SKILLMAXX_LOCK_HELD=1
    return 0
  fi
  old=
  [ -f "$LOCKDIR/pid" ] && old=$(cat "$LOCKDIR/pid" 2>/dev/null || true)
  if [ -n "$old" ] && kill -0 "$old" 2>/dev/null; then
    echo "another nightly is running"
    return 3
  fi
  rm -rf "$LOCKDIR"
  if mkdir "$LOCKDIR" 2>/dev/null; then
    skillmaxx_self_pid > "$LOCKDIR/pid" || true
    SKILLMAXX_LOCK_HELD=1
    echo "removed stale nightly lock${old:+ (pid $old)}"
    return 0
  fi
  echo "another nightly is running"
  return 3
}
skillmaxx_unlock() {
  [ "${SKILLMAXX_LOCK_HELD:-}" = 1 ] || return 0
  if [ -n "${LOCKDIR:-}" ] && [ -d "$LOCKDIR" ]; then
    mine=$(cat "$LOCKDIR/pid" 2>/dev/null || true)
    if [ "$mine" = "$(skillmaxx_self_pid)" ] || [ ! -f "$LOCKDIR/pid" ]; then
      rm -rf "$LOCKDIR"
    fi
  fi
  SKILLMAXX_LOCK_HELD=0
}
