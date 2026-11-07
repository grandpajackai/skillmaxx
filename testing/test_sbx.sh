#!/bin/bash
# Fixture checks for testing/sbx.sh. No real bwrap, Docker daemon, image pull, or host command.
set -uo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"
fail() { echo "FAIL: $*" >&2; exit 1; }
bash -n testing/sbx.sh || fail syntax
grep -q '@earendil-works/pi-coding-agent' testing/sandbox/Dockerfile || fail dockerfile_pi
grep -q '@earendil-works/pi-coding-agent' testing/setup_agents.sh || fail setup_pi
grep -q -- '--privileged' testing/sbx.sh && fail sbx_privileged_flag

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/both" "$tmp/dockeronly"
cat > "$tmp/both/bwrap" << 'EOF'
#!/bin/bash
printf '%s\n' "$@" > "$SBX_RECORD"
exit 0
EOF
cat > "$tmp/both/docker" << 'EOF'
#!/bin/bash
echo "docker should not be called" >> "$SBX_RECORD"
exit 99
EOF
cat > "$tmp/dockeronly/docker" << 'EOF'
#!/bin/bash
printf '%s\n' "$@" >> "$SBX_RECORD"
case "${FAKE_DOCKER:-ok}" in
  down) exit 1;;
  noimage) [ "$1" = "info" ] && exit 0; exit 1;;
esac
exit 0
EOF
chmod +x "$tmp/both/bwrap" "$tmp/both/docker" "$tmp/dockeronly/docker"

# bwrap wins when both exist, and the secret value is not passed through.
export SBX_RECORD="$tmp/bwrap.txt"
export ANTHROPIC_API_KEY=supersecret
export SKILLMAXX_AGENTS="$tmp/agents"
mkdir -p "$SKILLMAXX_AGENTS"
PATH="$tmp/both:/usr/bin:/bin" bash testing/sbx.sh "" true || fail bwrap_run
grep -q -- '--ro-bind' "$SBX_RECORD" || fail bwrap_ro
grep -q -- '--unshare-pid' "$SBX_RECORD" || fail bwrap_pid
grep -q -- '--unsetenv' "$SBX_RECORD" || fail bwrap_unset
grep -q supersecret "$SBX_RECORD" && fail bwrap_leaked_secret
grep -q 'docker should not be called' "$SBX_RECORD" && fail docker_called_despite_bwrap

# Docker path: strict flags, secret not in argv, payload not executed on the host.
unset -f true 2>/dev/null || true
marker="$tmp/host-ran"
export SBX_RECORD="$tmp/docker.txt"
export FAKE_DOCKER=ok
: > "$SBX_RECORD"
PATH="$tmp/dockeronly:/usr/bin:/bin" bash testing/sbx.sh "" "touch $marker" || fail docker_run
[ ! -e "$marker" ] || fail docker_ran_on_host
grep -q -- '--read-only' "$SBX_RECORD" || fail docker_ro
grep -q -- '--cap-drop' "$SBX_RECORD" || fail docker_cap
grep -q 'ALL' "$SBX_RECORD" || fail docker_cap_all
grep -q 'no-new-privileges' "$SBX_RECORD" || fail docker_nonew
grep -q -- '--privileged' "$SBX_RECORD" && fail docker_privileged
grep -q -- '--network=host' "$SBX_RECORD" && fail docker_hostnet
grep -q -- '--pid=host' "$SBX_RECORD" && fail docker_hostpid
grep -q supersecret "$SBX_RECORD" && fail docker_leaked_secret
grep -q 'skillmaxx-sandbox:local' "$SBX_RECORD" || fail docker_image

# Daemon down: refuse, do not touch the host.
export FAKE_DOCKER=down
: > "$SBX_RECORD"
if PATH="$tmp/dockeronly:/usr/bin:/bin" bash testing/sbx.sh "" "touch $marker" >/tmp/sbx-down.txt 2>&1; then fail down_should_fail; fi
[ ! -e "$marker" ] || fail down_ran_on_host
grep -q 'unsandboxed' /tmp/sbx-down.txt || fail down_message

# Image missing: same refusal.
export FAKE_DOCKER=noimage
if PATH="$tmp/dockeronly:/usr/bin:/bin" bash testing/sbx.sh "" "touch $marker" >/tmp/sbx-noimage.txt 2>&1; then fail noimage_should_fail; fi
[ ! -e "$marker" ] || fail noimage_ran_on_host
echo "ok sbx fixture checks (no real container)"
