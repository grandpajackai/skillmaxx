#!/bin/bash
# SkillMaxx nightly refresh. Run by the "SkillMaxx nightly refresh" Grok Bot routine (~2 AM ET).
# Every run logs to testing/logs/nightly-<date>.log (gitignored) and exits non-zero with the failing step named.
# Failed installs are retried once (--retry 1); daily_report.py only calls something broken after 2 failing nights.
# Steps: sync master -> refresh codex mirror -> sandboxed install tests -> metadata -> daily report + post drafts -> build -> data-only commit + push.
set -uo pipefail; cd "$(dirname "$0")/.."; ROOT=$PWD
D=$(date +%F); LOG=testing/logs/nightly-$D.log; mkdir -p testing/logs
exec > >(tee -a "$LOG") 2>&1
exec 9>/tmp/skillmaxx-nightly.lock; flock -n 9 || { echo "another nightly is running"; exit 3; }
step(){ echo "== $(date '+%F %T %Z') $1"; }
die(){ echo "!! NIGHTLY FAILED at step: $1 (see $ROOT/$LOG)"; exit 1; }
NOPUSH=${NOPUSH:-}
step "sync master"
git fetch -q origin && git checkout -q master && git pull -q --ff-only origin master || die "git sync (dirty tree or diverged master?)"
step "codex mirror"   # setup_agents.sh renames the marketplace locally; reset it so pull never aborts on a dirty file
M=/workspace/agents/codex-mirror
if [ -d $M ]; then
  git -C $M checkout -q -- .agents/plugins/marketplace.json; git -C $M pull -q --ff-only || echo "warn: mirror pull failed, using cached copy"
  python3 -c "import json;p='$M/.agents/plugins/marketplace.json';d=json.load(open(p));d['name']='openai-plugins-mirror';json.dump(d,open(p,'w'))"
fi
[ -d /workspace/agents/templates/claude ] || die "agent templates missing (run testing/setup_agents.sh)"
step "install tests"; python3 testing/run_tests.py --jobs 8 --retry 1 || die "run_tests.py"
step "metadata"; for i in 1 2; do python3 fetch_meta.py && break; [ $i = 2 ] && die "fetch_meta.py"; echo "retrying fetch_meta in 60s"; sleep 60; done
step "daily report"; python3 testing/daily_report.py || die "daily_report.py"
step "weekly pages"; python3 testing/weekly_scorecard.py --write > /dev/null || die "weekly_scorecard.py"
step "build"; SITE_URL=https://skillmaxx.gilventures.ai PATH_PREFIX=/ npx @11ty/eleventy --quiet || die "eleventy build"
step "commit data"
git add testing/history.json testing/results data src/assets/logos src/_data/reports.json src/_data/latestRows.json src/_data/weeks.json growth/daily growth/weekly
if git diff --cached --quiet; then echo "no data changes"; else
  git -c user.name="SkillMaxx Grok Bot" -c user.email=skillmaxx@mail.grokbot.com commit -q -m "data: nightly refresh $D" || die "commit"
  [ -n "$NOPUSH" ] && echo "NOPUSH set, not pushing" || git push -q origin master || die "push (branch protection / auth?)"
fi
step "done"; python3 -c "import json;r=json.load(open('testing/results/$D.json'))['results'];print(sum(x['status']=='pass' for x in r),'/',len(r),'pass')"
