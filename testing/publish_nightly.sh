#!/bin/bash
# Grok-free publisher for one Mac nightly (Nov 17). Runs on the Mac after a successful 02:00 ET run
# (called by testing/local_nightly.sh; the hourly watchdog retries until noon ET).
# Usage: testing/publish_nightly.sh [DATE] [RESULTS.json]
#   DATE defaults to today (America/New_York); RESULTS defaults to $SKILLMAXX_STATE/results/DATE.json.
# Steps: fresh clone of origin/master in $SKILLMAXX_STATE/publish (never the test worktree) ->
#   testing/import_mac_run.py (same provenance holds as the 4 AM routine) -> data-only branch + PR ->
#   wait for the required "build" check -> squash-merge -> Pages deploys -> check /reports/DATE/ is live.
# A hold (exit 2) publishes nothing: the site shows the default gap note for that night.
# Pushes only a data/nightly-* branch with the gh login already on this machine. Never pushes master,
# never uses SKILLMAXX_PRODUCTION/ALLOW_PUSH, sends no mail or posts. Alerts reuse testing/nightly_alert.sh.
# Disable with SKILLMAXX_AUTO_PUBLISH=0 in testing/local.env.
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
STATE=${SKILLMAXX_STATE:-$HOME/.local/share/skillmaxx}
export SKILLMAXX_STATE="$STATE"
D=${1:-$(TZ=America/New_York date +%F)}
RES=${2:-$STATE/results/$D.json}
PUB=${SKILLMAXX_PUBLISH_DIR:-$STATE/publish}
REPO=${SKILLMAXX_REPO:-grandpajackai/skillmaxx}
SITE=${SKILLMAXX_SITE:-https://skillmaxx.gilventures.ai}
LOG="$STATE/logs/publish-$D.log"
[ -d /opt/homebrew/bin ] && PATH="/opt/homebrew/bin:$PATH"
export PATH
mkdir -p "$STATE/logs"
exec > >(tee -a "$LOG") 2>&1
# shellcheck source=testing/nightly_alert.sh
. "$HERE/nightly_alert.sh"
status() { printf '%s %s\n' "$D" "$1" > "$STATE/publish-status"; }
fail() {
  echo "publish: FAILED: $*"; status failed
  # One alert per night; the hourly watchdog retries quietly after that.
  if [ "$(cat "$STATE/publish-alerted" 2>/dev/null)" != "$D" ]; then
    printf '%s\n' "$D" > "$STATE/publish-alerted"
    smx_alert "publish" "$*" "$LOG" "$D" || true
  fi
  exit 1
}

mkdir "$STATE/publish.lock" 2>/dev/null || { [ -n "$(find "$STATE/publish.lock" -mmin +90 2>/dev/null)" ] && rm -rf "$STATE/publish.lock" && mkdir "$STATE/publish.lock"; } || { echo "publish: another publish is running"; exit 0; }
trap 'rm -rf "$STATE/publish.lock"' EXIT
echo "publish: $D start $(TZ=America/New_York date '+%F %T %Z')"
[ "${SKILLMAXX_AUTO_PUBLISH:-1}" = "0" ] && { echo "publish: SKILLMAXX_AUTO_PUBLISH=0, skipping"; exit 0; }
[ -f "$RES" ] || fail "no results file $RES"
command -v gh >/dev/null || fail "gh is not installed"
gh auth status >/dev/null 2>&1 || fail "gh is not logged in on this Mac (run: gh auth login)"
SHA=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("source_sha") or "")' "$STATE/source.json" 2>/dev/null)
[ -n "$SHA" ] || fail "no source_sha in $STATE/source.json (provenance unknown)"

if [ ! -d "$PUB/.git" ]; then
  git clone -q "https://github.com/$REPO.git" "$PUB" || fail "git clone failed"
fi
cd "$PUB" || fail "no $PUB"
git fetch -q origin "+refs/heads/master:refs/remotes/origin/master" || fail "git fetch failed"
if git cat-file -e "origin/master:testing/results/$D.json" 2>/dev/null; then
  echo "publish: $D is already on master"; status published; exit 0
fi
git checkout -q -f -B "data/nightly-$D" origin/master && git clean -fdq || fail "could not reset $PUB"

python3 testing/import_mac_run.py "$RES" --source-sha "$SHA"; rc=$?
if [ "$rc" = 2 ]; then
  status hold
  smx_alert "publish-hold" "$D not published: import_mac_run.py held it (see log). The site shows the default gap note." "$LOG" "$D" || true
  exit 2
fi
[ "$rc" = 0 ] || fail "import_mac_run.py exited $rc"

SUNDAY=0; [ "$(python3 -c 'import sys,datetime; print(datetime.date.fromisoformat(sys.argv[1]).isoweekday())' "$D")" = 7 ] && SUNDAY=1
if [ "$SUNDAY" = 1 ] && [ -f growth/scripts/weekly_blog_auto.py ]; then
  python3 growth/scripts/weekly_blog_auto.py "$D" || echo "publish: weekly blog post skipped (generator error)"
fi
# Grok-free routine prep committed with the data (growth/prep/prep.py: no LLM, no sends, keyless reads only).
# Mondays: sponsor-pipeline counts/aging for the 9 AM routine. Sundays: recap stats for the 6 PM routine.
# The box prep loop (/home/box/skillmaxx-prep) writes fresher same-day copies; these are the committed record.
DOW=$(python3 -c 'import sys,datetime; print(datetime.date.fromisoformat(sys.argv[1]).isoweekday())' "$D")
if [ -f growth/prep/prep.py ] && { [ "$DOW" = 1 ] || [ "$DOW" = 7 ]; }; then
  PREP=$(mktemp -d)
  if [ "$DOW" = 1 ]; then
    python3 growth/prep/prep.py pipeline --date "$D" --out "$PREP" >/dev/null && mkdir -p growth/sponsors/briefs \
      && cp "$PREP/pipeline.md" "growth/sponsors/briefs/pipeline-$D.md" || echo "publish: pipeline prep skipped"
  else
    python3 growth/prep/prep.py recap --date "$D" --out "$PREP" >/dev/null && mkdir -p growth/weekly \
      && cp "$PREP/recap.md" "growth/weekly/recap-prep-$D.md" || echo "publish: recap prep skipped"
  fi
  rm -rf "$PREP"
fi
SUM=$(python3 -c 'import json,sys; r=json.load(open(sys.argv[1]))["results"]; print("%d/%s" % (sum(x["status"] == "pass" for x in r), format(len(r), ",")))' "testing/results/$D.json")
ADD=(); for f in testing/results testing/history.json src/_data/reports.json src/_data/latestRows.json src/_data/weeks.json growth/daily growth/weekly growth/sponsors/briefs src/blog; do [ -e "$f" ] && ADD+=("$f"); done
git add -- "${ADD[@]}"
git diff --cached --quiet && { echo "publish: nothing changed"; status published; exit 0; }
git -c user.name=grandpajackai -c user.email=grandpajackai@gmail.com commit -qm "data: nightly refresh $D ($SUM)" || fail "commit failed"
BR="data/nightly-$D-$(date +%H%M)"
git push -q origin "HEAD:refs/heads/$BR" || fail "git push of $BR failed"
PR=$(gh pr create -R "$REPO" --base master --head "$BR" --title "data: nightly refresh $D ($SUM)" \
  --body "Automatic Mac publish (testing/publish_nightly.sh, no Grok). Source $SHA. import_mac_run.py provenance checks passed. Data files only.") || fail "gh pr create failed"
echo "publish: $PR"

merged=0
for i in 1 2 3; do
  sleep 20
  gh pr checks "$PR" -R "$REPO" --required --watch --interval 30 >/dev/null 2>&1 || { sleep 30; gh pr checks "$PR" -R "$REPO" --required >/dev/null 2>&1 || fail "required check failed on $PR"; }
  if gh pr merge "$PR" -R "$REPO" --squash --delete-branch >/dev/null 2>&1; then merged=1; break; fi
  echo "publish: merge refused (master moved?), updating branch, try $i"
  gh pr update-branch "$PR" -R "$REPO" >/dev/null 2>&1 || true
done
[ "$merged" = 1 ] || fail "could not merge $PR"
status merged
echo "publish: merged $PR; waiting for $SITE/reports/$D/"
for i in $(seq 1 30); do
  page=$(curl -sf --max-time 20 "$SITE/reports/$D/" 2>/dev/null)
  if [ -n "$page" ] && ! printf '%s' "$page" | grep -q 'No report this night'; then
    status published; echo "publish: live $SITE/reports/$D/"
    # Sundays: do not run buffer_weekly.py. Buffer posting is handled by the Grok Buffer
    # connector; the Mac script would only create duplicates. weekly_blog_auto.py is unchanged.
    exit 0
  fi
  sleep 30
done
fail "merged $PR but $SITE/reports/$D/ is not live after 15 min (check the Pages workflow)"
