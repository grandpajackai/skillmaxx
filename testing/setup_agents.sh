#!/bin/bash
# One-time: install the agent CLIs (no logins) + marketplace templates used by run_tests.py
set -e; AG=/workspace/agents; mkdir -p $AG && cd $AG; [ -f package.json ] || npm init -y >/dev/null
npm i @anthropic-ai/claude-code @openai/codex @xai-official/grok @mariozechner/pi-coding-agent
mkdir -p cursorhome && HOME=$AG/cursorhome bash -c 'curl -fsSL https://cursor.com/install | bash'
[ -d codex-mirror ] || git clone -q --depth 1 https://github.com/openai/plugins codex-mirror
python3 -c "import json;p='codex-mirror/.agents/plugins/marketplace.json';d=json.load(open(p));d['name']='openai-plugins-mirror';json.dump(d,open(p,'w'))"
S=$(dirname "$0")/sbx.sh; T=$AG/templates; rm -rf $T; mkdir -p $T
SBX_KEEP=$T/claude $S "" 'claude plugin marketplace add anthropics/claude-plugins-official'
SBX_KEEP=$T/grok $S "" 'claude plugin marketplace add anthropics/claude-plugins-official; grok plugin marketplace add xai-org/plugin-marketplace'
SBX_KEEP=$T/codex $S "" "codex plugin marketplace add $AG/codex-mirror"
