#!/bin/bash
# Intended for a nightly cron (e.g. `0 2 * * * /workspace/skillmaxx/testing/nightly.sh`). Not scheduled yet.
set -e; cd "$(dirname "$0")/.."
(cd /workspace/agents/codex-mirror && git pull -q --ff-only || true)
python3 testing/run_tests.py --jobs 8 && python3 fetch_meta.py && npx @11ty/eleventy
