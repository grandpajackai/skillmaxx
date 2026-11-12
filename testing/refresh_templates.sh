#!/bin/bash
# Rebuild the Claude, Grok, and Codex sandbox templates from the local marketplace checkouts.
# Does not install CLIs, publish, or set production/push flags.
#
# Grok 1.0.77 reads Claude's known_marketplaces.json. `claude plugin marketplace add
# anthropics/claude-plugins-official` stores a GitHub source there and keeps a checkout beside it.
# Grok imports the GitHub URL and ignores that checkout, so `grok plugin marketplace list` shows
# the URL and every install syncs GitHub again. Registering the directory with
# `grok plugin marketplace add <path>` stores a filesystem path. The directory basename
# claude-plugins-official is the source name, which is the pin @claude-plugins-official.
set -euo pipefail
AG=${SKILLMAXX_AGENTS:-/workspace/agents}
HERE=$(cd "$(dirname "$0")" && pwd)
S=$HERE/sbx.sh
[ -d "$AG/claude-plugins-official/.claude-plugin" ] || {
  echo "claude marketplace mirror missing at $AG/claude-plugins-official (testing/setup_agents.sh clones it)" >&2
  exit 1
}
[ -d "$AG/codex-mirror" ] || {
  echo "codex mirror missing at $AG/codex-mirror (testing/setup_agents.sh clones it)" >&2
  exit 1
}
mkdir -p "$AG"
STAGE=$(mktemp -d "$AG/templates-stage.XXXXXX")
cleanup() { [ -d "$STAGE" ] && rm -rf "$STAGE"; }
trap cleanup EXIT
# New homes, so the Grok home has no leftover GitHub marketplace entry.
SBX_KEEP=$STAGE/claude "$S" "" "claude plugin marketplace add $AG/claude-plugins-official"
SBX_KEEP=$STAGE/grok "$S" "" "grok plugin marketplace add xai-org/plugin-marketplace; grok plugin marketplace add $AG/claude-plugins-official"
SBX_KEEP=$STAGE/codex "$S" "" "codex plugin marketplace add $AG/codex-mirror"
T=$AG/templates
rm -rf "$T"
mv "$STAGE" "$T"
trap - EXIT
echo "marketplace templates ready in $T"
