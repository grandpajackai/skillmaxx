#!/bin/bash
# Run one install command in a throwaway sandbox.
# Linux host with bwrap: the existing bubblewrap (read-only /, fresh HOME, network on, no API keys).
# Otherwise a local Docker image skillmaxx-sandbox:local, non-privileged, read-only, current uid.
# Never runs the command on the host. Does not start Docker and does not pull an image.
# usage: sbx.sh <template-home-or-empty> <cmd...>
set -e
T="$1"; shift
AG=${SKILLMAXX_AGENTS:-/workspace/agents}
IMAGE=${SKILLMAXX_SANDBOX_IMAGE:-skillmaxx-sandbox:local}
if [ -n "${SBX_KEEP:-}" ]; then H="$SBX_KEEP"; mkdir -p "$H"
elif command -v bwrap >/dev/null 2>&1 || [ "$(uname -s)" != "Darwin" ]; then
  H=$(mktemp -d /tmp/smx-sbx.XXXXXX); trap 'rm -rf "$H" 2>/dev/null || true' EXIT
else
  # Docker Desktop on Mac shares /Users, not every mktemp directory.
  mkdir -p "${HOME}/Library/Caches/skillmaxx-sbx"
  H=$(mktemp -d "${HOME}/Library/Caches/skillmaxx-sbx/sbx.XXXXXX"); trap 'rm -rf "$H" 2>/dev/null || true' EXIT
fi
[ -n "$T" ] && [ -d "$T" ] && cp -a "$T/." "$H/"
# Optional pre-warmed npm cache (SKILLMAXX_NPM_CACHE). Bind-mounted at /tmp/skillmaxx-npm-cache; ~/.npm/_cacache (and _prebuilds) are
# symlinked to that shared cache, while ~/.npm/_npx stays private so parallel
# jobs do not race on extract. A first-time npx download is not charged against
# the agent's MCP connect timeout.
# The rest of HOME stays empty (no accounts or API keys).
NPM_CACHE_MOUNT=
if [ -n "${SKILLMAXX_NPM_CACHE:-}" ] && [ -d "$SKILLMAXX_NPM_CACHE" ]; then
  NPM_CACHE_MOUNT=1
fi
# Symlink the cache from a path that is not a mount point under $H, so the
# throwaway HOME can still be deleted after the container exits.
NPM_LINK=""
if [ "$NPM_CACHE_MOUNT" = 1 ]; then
  # Share only the content-addressable cache. Each sandbox gets its own ~/.npm/_npx
  # so parallel jobs do not race on npx extract/rename (ENOTEMPTY).
  NPM_LINK="mkdir -p /home/sbx/.npm/_npx /tmp/skillmaxx-npm-cache/_cacache /tmp/skillmaxx-npm-cache/_prebuilds && ln -sfn /tmp/skillmaxx-npm-cache/_cacache /home/sbx/.npm/_cacache && ln -sfn /tmp/skillmaxx-npm-cache/_prebuilds /home/sbx/.npm/_prebuilds && "
fi

run_bwrap() {
  bwrap --ro-bind / / --tmpfs /home --tmpfs /root --tmpfs /workspace --tmpfs /cursor --tmpfs /tmp \
    --ro-bind "$AG/node_modules" "$AG/node_modules" --ro-bind "$AG/cursorhome/.local" "$AG/cursorhome/.local" \
    --ro-bind-try "$AG/codex-mirror" "$AG/codex-mirror" --ro-bind-try "$AG/claude-plugins-official" "$AG/claude-plugins-official" --ro-bind-try "$AG/node22" "$AG/node22" \
    --ro-bind "$(dirname "$(readlink -f "$0")")" /tmp/smx-testing \
    --bind "$H" /home/sbx ${NPM_CACHE_MOUNT:+--bind "$SKILLMAXX_NPM_CACHE" /tmp/skillmaxx-npm-cache} --setenv HOME /home/sbx \
    --setenv PATH "$AG/node22/bin:$AG/node_modules/.bin:$AG/cursorhome/.local/bin:/usr/local/bin:/usr/bin:/bin" \
    --unsetenv GH_TOKEN --unsetenv GITHUB_TOKEN --unsetenv ANTHROPIC_API_KEY --unsetenv OPENAI_API_KEY --unsetenv XAI_API_KEY \
    --chdir /home/sbx --dev /dev --proc /proc --unshare-pid --unshare-ipc --die-with-parent \
    bash -c "$NPM_LINK$*"
}

run_docker() {
  testing_dir=$(cd "$(dirname "$0")" && pwd)
  args=(docker run --rm --read-only --cap-drop ALL --security-opt no-new-privileges --network bridge --init
    --tmpfs /tmp:rw,exec,nosuid,nodev --tmpfs /root:rw,nosuid,nodev --tmpfs /workspace:rw,nosuid,nodev --tmpfs /cursor:rw,nosuid,nodev
    -v "$H:/home/sbx" -v "${testing_dir}:/smx-testing:ro"
    -e HOME=/home/sbx
    -e PATH=/opt/skillmaxx/node_modules/.bin:/opt/cursorhome/.local/bin:/usr/local/bin:/usr/bin:/bin
    -u "$(id -u):$(id -g)" -w /home/sbx)
  [ -d "$AG/codex-mirror" ] && args+=(-v "$AG/codex-mirror:$AG/codex-mirror:ro")
  [ -d "$AG/claude-plugins-official" ] && args+=(-v "$AG/claude-plugins-official:$AG/claude-plugins-official:ro")
  if [ "$NPM_CACHE_MOUNT" = 1 ]; then args+=(-v "$SKILLMAXX_NPM_CACHE:/tmp/skillmaxx-npm-cache"); fi
  # /tmp is a tmpfs, so the probe path is a symlink made after that mount, not a bind under it.
  args+=("$IMAGE" bash -c "ln -sfn /smx-testing /tmp/smx-testing && $NPM_LINK$*")
  "${args[@]}"
}

if command -v bwrap >/dev/null 2>&1; then
  run_bwrap "$@"
elif command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1 && docker image inspect "$IMAGE" >/dev/null 2>&1; then
  run_docker "$@"
else
  echo "sbx: refusing an unsandboxed run. Need bwrap, or a running Docker daemon and local image $IMAGE. Not starting Docker and not pulling." >&2
  exit 1
fi
