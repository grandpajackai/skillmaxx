#!/bin/bash
# Run a command in a throwaway bubblewrap sandbox: read-only system, empty /home,/workspace,/root,/cursor,
# fresh HOME (copied from an optional template), network allowed (needed to clone/npx).
# usage: sbx.sh <template-home-or-empty> <cmd...>
set -e; T="$1"; shift
if [ -n "$SBX_KEEP" ]; then H="$SBX_KEEP"; mkdir -p "$H"; else H=$(mktemp -d /tmp/smx-sbx.XXXXXX); trap 'rm -rf "$H"' EXIT; fi
[ -n "$T" ] && [ -d "$T" ] && cp -a "$T/." "$H/"
AG=/workspace/agents
exec_bwrap(){ bwrap --ro-bind / / --tmpfs /home --tmpfs /root --tmpfs /workspace --tmpfs /cursor --tmpfs /tmp \
 --ro-bind $AG/node_modules $AG/node_modules --ro-bind $AG/cursorhome/.local $AG/cursorhome/.local --ro-bind-try $AG/codex-mirror $AG/codex-mirror \
 --bind "$H" /home/sbx --setenv HOME /home/sbx --setenv PATH "$AG/node_modules/.bin:$AG/cursorhome/.local/bin:/usr/local/bin:/usr/bin:/bin" \
 --unsetenv GH_TOKEN --unsetenv GITHUB_TOKEN --unsetenv ANTHROPIC_API_KEY --unsetenv OPENAI_API_KEY --unsetenv XAI_API_KEY \
 --chdir /home/sbx --dev /dev --proc /proc --unshare-pid --unshare-ipc --die-with-parent "$@"; }
exec_bwrap bash -c "$*"
