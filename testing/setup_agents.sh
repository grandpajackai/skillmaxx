#!/bin/bash
# One-time: install the agent CLIs (no logins) + marketplace templates used by run_tests.py
set -e; AG=${SKILLMAXX_AGENTS:-/workspace/agents}; IMAGE=${SKILLMAXX_SANDBOX_IMAGE:-skillmaxx-sandbox:local}
mkdir -p "$AG" && cd "$AG"
if command -v bwrap >/dev/null 2>&1; then
  [ -f package.json ] || npm init -y >/dev/null
  # Pi package is the one the nightly sandbox runs (MCP needs 0.99+). The old name is 0.73.1.
  npm i @anthropic-ai/claude-code @openai/codex @xai-official/grok @earendil-works/pi-coding-agent
  mkdir -p cursorhome && HOME=$AG/cursorhome bash -c 'curl -fsSL https://cursor.com/install | bash'
else
  echo "No bwrap. Agent CLIs come from Linux image $IMAGE, not a host npm install."
  docker image inspect "$IMAGE" >/dev/null
fi
[ -d codex-mirror ] || git clone -q --depth 1 https://github.com/openai/plugins codex-mirror
python3 -c "import json;p='codex-mirror/.agents/plugins/marketplace.json';d=json.load(open(p));d['name']='openai-plugins-mirror';json.dump(d,open(p,'w'))"
# Full catalog checkout. Keep this directory name: it is Grok's source name and the install pin.
# Keep marketplace.json's name field: Claude installs still pin @claude-plugins-official.
[ -d claude-plugins-official ] || git clone -q --depth 1 https://github.com/anthropics/claude-plugins-official claude-plugins-official
bash "$(dirname "$0")/refresh_templates.sh"
