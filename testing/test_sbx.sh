#!/bin/bash
# Fixture checks for testing/sbx.sh. No real bwrap, Docker daemon, image pull, or host command.
set -uo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"
unset SKILLMAXX_NPM_CACHE 2>/dev/null || true
fail() { echo "FAIL: $*" >&2; exit 1; }
bash -n testing/sbx.sh || fail syntax
grep -q '@earendil-works/pi-coding-agent' testing/sandbox/Dockerfile || fail dockerfile_pi
grep -q '@earendil-works/pi-coding-agent' testing/setup_agents.sh || fail setup_pi
grep -q 'refresh_templates.sh' testing/setup_agents.sh || fail setup_calls_refresh
grep -q 'claude-plugins-official' testing/refresh_templates.sh || fail refresh_claude_mirror
grep -q 'grok plugin marketplace add xai-org/plugin-marketplace' testing/refresh_templates.sh || fail setup_grok_native
grep -q 'grok plugin marketplace add $AG/claude-plugins-official' testing/refresh_templates.sh || fail setup_grok_local_claude
grep -q 'codex plugin marketplace add $AG/codex-mirror' testing/refresh_templates.sh || fail setup_codex_local
# Claude reserves claude-plugins-official for anthropics GitHub sources, so a local-path add
# fails. The Claude template uses the official GitHub source. A Grok home must not be created
# by that add: Grok imports known_marketplaces.json and then re-scans GitHub on every install.
remote='claude plugin marketplace add anthropics/claude-plugins-official'
code_lines() { grep -vE '^[[:space:]]*#' "$1" || true; }
code_lines testing/setup_agents.sh | grep -q "$remote" && fail setup_grok_remote_claude
claude_lines=$(code_lines testing/refresh_templates.sh | grep 'SBX_KEEP=$STAGE/claude ' || true)
[ -n "$claude_lines" ] || fail claude_template_missing
printf '%s\n' "$claude_lines" | grep -q "$remote" || fail claude_official_marketplace
printf '%s\n' "$claude_lines" | grep -q 'claude plugin marketplace add $AG/claude-plugins-official' && fail claude_reserved_local_name
grok_lines=$(code_lines testing/refresh_templates.sh | grep 'SBX_KEEP=$STAGE/grok ' || true)
[ -n "$grok_lines" ] || fail setup_grok_local_claude
printf '%s\n' "$grok_lines" | grep -q 'grok plugin marketplace add $AG/claude-plugins-official' || fail setup_grok_local_claude
printf '%s\n' "$grok_lines" | grep -q 'SBX_KEEP=$STAGE/grok "$S" "" ' || fail setup_grok_fresh_home
printf '%s\n' "$grok_lines" | grep -q 'claude plugin marketplace add' && fail setup_grok_remote_claude
printf '%s\n' "$grok_lines" | grep -q 'anthropics/claude-plugins-official' && fail setup_grok_remote_claude
while IFS= read -r line; do
  case "$line" in
    *"$remote"*)
      case "$line" in
        *'SBX_KEEP=$STAGE/claude '*) ;;
        *) fail setup_grok_remote_claude ;;
      esac
      ;;
  esac
done < <(code_lines testing/refresh_templates.sh)
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
grep -q 'claude-plugins-official' "$SBX_RECORD" || fail bwrap_claude_mirror
grep -q -- '--unshare-pid' "$SBX_RECORD" || fail bwrap_pid
grep -q -- '--unsetenv' "$SBX_RECORD" || fail bwrap_unset
grep -q supersecret "$SBX_RECORD" && fail bwrap_leaked_secret
grep -q 'docker should not be called' "$SBX_RECORD" && fail docker_called_despite_bwrap

mkdir -p "$SKILLMAXX_AGENTS/claude-plugins-official"
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
grep -q '/smx-testing:ro' "$SBX_RECORD" || fail docker_probe_mount
grep -q 'ln -sfn /smx-testing /tmp/smx-testing' "$SBX_RECORD" || fail docker_probe_link
grep -q "claude-plugins-official:$SKILLMAXX_AGENTS/claude-plugins-official:ro" "$SBX_RECORD" || fail docker_claude_mirror

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

# npm cache bind is off by default, on when SKILLMAXX_NPM_CACHE is a directory.
export SBX_RECORD="$tmp/bwrap-nocache.txt"
: > "$SBX_RECORD"
PATH="$tmp/both:/usr/bin:/bin" bash testing/sbx.sh "" true || fail bwrap_nocache
grep -q '/tmp/skillmaxx-npm-cache' "$SBX_RECORD" && fail bwrap_npm_default
mkdir -p "$tmp/npmcache"
export SKILLMAXX_NPM_CACHE="$tmp/npmcache"
export SBX_RECORD="$tmp/bwrap-cache.txt"
: > "$SBX_RECORD"
PATH="$tmp/both:/usr/bin:/bin" bash testing/sbx.sh "" true || fail bwrap_cache
grep -q "$SKILLMAXX_NPM_CACHE" "$SBX_RECORD" || fail bwrap_npm_bind
grep -q '/tmp/skillmaxx-npm-cache' "$SBX_RECORD" || fail bwrap_npm_target
export FAKE_DOCKER=ok
export SBX_RECORD="$tmp/docker-cache.txt"
: > "$SBX_RECORD"
PATH="$tmp/dockeronly:/usr/bin:/bin" bash testing/sbx.sh "" true || fail docker_cache
grep -q "$SKILLMAXX_NPM_CACHE:/tmp/skillmaxx-npm-cache" "$SBX_RECORD" || fail docker_npm_bind
unset SKILLMAXX_NPM_CACHE

echo "ok sbx fixture checks (no real container)"
