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
  H=$(mktemp -d /tmp/smx-sbx.XXXXXX); trap 'rm -rf "$H"' EXIT
else
  # Docker Desktop on Mac shares /Users, not every mktemp directory.
  mkdir -p "${HOME}/Library/Caches/skillmaxx-sbx"
  H=$(mktemp -d "${HOME}/Library/Caches/skillmaxx-sbx/sbx.XXXXXX"); trap 'rm -rf "$H"' EXIT
fi
[ -n "$T" ] && [ -d "$T" ] && cp -a "$T/." "$H/"

run_bwrap() {
  bwrap --ro-bind / / --tmpfs /home --tmpfs /root --tmpfs /workspace --tmpfs /cursor --tmpfs /tmp \
    --ro-bind "$AG/node_modules" "$AG/node_modules" --ro-bind "$AG/cursorhome/.local" "$AG/cursorhome/.local" \
    --ro-bind-try "$AG/codex-mirror" "$AG/codex-mirror" --ro-bind-try "$AG/node22" "$AG/node22" \
    --ro-bind "$(dirname "$(readlink -f "$0")")" /tmp/smx-testing \
    --bind "$H" /home/sbx --setenv HOME /home/sbx \
    --setenv PATH "$AG/node22/bin:$AG/node_modules/.bin:$AG/cursorhome/.local/bin:/usr/local/bin:/usr/bin:/bin" \
    --unsetenv GH_TOKEN --unsetenv GITHUB_TOKEN --unsetenv ANTHROPIC_API_KEY --unsetenv OPENAI_API_KEY --unsetenv XAI_API_KEY \
    --chdir /home/sbx --dev /dev --proc /proc --unshare-pid --unshare-ipc --die-with-parent \
    bash -c "$*"
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
  # /tmp is a tmpfs, so the probe path is a symlink made after that mount, not a bind under it.
  args+=("$IMAGE" bash -c "ln -sfn /smx-testing /tmp/smx-testing && $*")
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
