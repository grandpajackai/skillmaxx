#!/bin/bash
# Rebuild the Claude, Grok, and Codex sandbox templates.
# Does not install CLIs, publish, or set production/push flags.
#
# Claude reserves the marketplace name claude-plugins-official for GitHub sources from the
# anthropics organization. `claude plugin marketplace add <local directory>` fails:
# "The name 'claude-plugins-official' is reserved for official Anthropic marketplaces and
# can only be used with GitHub sources from the 'anthropics' organization."
# The Claude template therefore uses the official source:
#   claude plugin marketplace add anthropics/claude-plugins-official
#
# Grok 1.0.77 reads Claude's known_marketplaces.json when it is in the same home. That GitHub
# source makes `grok plugin marketplace list` show the URL, and every install syncs GitHub again.
# The Grok template is a separate fresh home. It does not run Claude's marketplace add and it is
# not seeded from the Claude template. It registers xAI with
# `grok plugin marketplace add xai-org/plugin-marketplace` and the local checkout with
# `grok plugin marketplace add <path>`. The directory basename claude-plugins-official is the
# source name, which is the pin @claude-plugins-official.
# Codex stays on the local codex-mirror.
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
# Separate fresh homes. The Grok home must not contain Claude's GitHub marketplace entry.
SBX_KEEP=$STAGE/claude "$S" "" "claude plugin marketplace add anthropics/claude-plugins-official"
SBX_KEEP=$STAGE/grok "$S" "" "grok plugin marketplace add xai-org/plugin-marketplace; grok plugin marketplace add $AG/claude-plugins-official"
SBX_KEEP=$STAGE/codex "$S" "" "codex plugin marketplace add $AG/codex-mirror"
T=$AG/templates
rm -rf "$T"
mv "$STAGE" "$T"
trap - EXIT
echo "marketplace templates ready in $T"
