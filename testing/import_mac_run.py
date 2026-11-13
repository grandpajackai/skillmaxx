#!/usr/bin/env python3
"""Import one Mac nightly results file into the repo so it can be published (used by the 4 AM routine).
Usage: python3 testing/import_mac_run.py RESULTS.json [--source-sha SHA] [--check]
  RESULTS.json  a copy of ~/.local/share/skillmaxx/results/<date>.json from the Mac
  --source-sha  source_sha from the Mac's ~/.local/share/skillmaxx/source.json (must be on origin/master)
  --check       validate only; change nothing
Holds (exit 2, nothing written) when the run is not publishable:
  - Grok Build marketplace-scan errors ("Couldn't scan every marketplace"), the Nov 9-11 harness bug
  - a missing/unknown agent version, a date listed under no_valid_run, a run_at that doesn't match the file name
  - an install count more than 5% off the last published run, or slugs not in data/skills.json
  - a source sha that is not on origin/master
  - installs failing only because the sandbox image has no uvx (override: --allow-missing-uvx)
A change of agent versions is NOT a hold: the daily report shows an agent-update callout, and planned
baseline switches are listed in src/_data/runNotes.json. On success it writes testing/results/<date>.json,
appends testing/history.json (one entry per case per day, same as run_tests.py), then runs daily_report.py
and weekly_scorecard.py --write. The Eleventy build, PR and merge are left to the caller."""
import json, os, sys, glob, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCAN = "Couldn't scan every marketplace"
NOUVX = ('Executable not found in $PATH: "uvx"', "spawn uvx ENOENT")  # sandbox image is missing uv (harness gap)
DOCKER = "Docker (skillmaxx-sandbox:local, not privileged), fresh HOME, no credentials/API keys"

def main(argv):
    if not argv or argv[0].startswith("-"):
        sys.exit(__doc__)
    path = argv[0]; check = "--check" in argv
    sha = argv[argv.index("--source-sha") + 1] if "--source-sha" in argv else None
    run = json.load(open(path)); res = run.get("results") or []
    date = os.path.basename(path)[:10]
    notes = json.load(open(os.path.join(ROOT, "src/_data/runNotes.json")))
    skills = {x["slug"] for x in json.load(open(os.path.join(ROOT, "data/skills.json")))["items"]}
    pub = sorted(glob.glob(os.path.join(ROOT, "testing/results/*.json")))
    prev = [f for f in pub if os.path.basename(f)[:10] < date]
    last = json.load(open(prev[-1])) if prev else None
    holds = []
    if run.get("run_at", "")[:10] != date: holds.append(f"run_at {run.get('run_at')} does not match file date {date}")
    if date in {x["date"] for x in notes.get("no_valid_run", [])}: holds.append(f"{date} is listed as no valid run")
    scan = sum(SCAN in (r.get("log", "") + r.get("first_log", "")) for r in res)
    if scan: holds.append(f"{scan} Grok Build marketplace-scan errors (harness bug, not add-on breakage)")
    nouvx = sum(any(m in (r.get("log", "") + r.get("first_log", "")) for m in NOUVX) for r in res)
    if nouvx and "--allow-missing-uvx" not in argv:
        holds.append(f"{nouvx} installs failed because the sandbox has no uvx (harness gap: rebuild the image with testing/sandbox/Dockerfile.add-uv)")
    v = run.get("versions") or {}
    bad = [a for a in ("claude_code", "codex", "grok_build", "cursor", "pi") if not v.get(a) or "?" in v[a]]
    if bad: holds.append(f"unknown agent version for {', '.join(bad)}")
    if last:
        n0 = len(last["results"])
        if n0 and abs(len(res) - n0) > 0.05 * n0: holds.append(f"{len(res)} installs vs {n0} in the last published run (>5% off)")
    unknown = sorted({r["slug"] for r in res} - skills)
    if unknown: holds.append(f"{len(unknown)} slugs not in data/skills.json (e.g. {', '.join(unknown[:3])})")
    if sha:
        subprocess.run(["git", "-C", ROOT, "fetch", "-q", "origin", "master"], check=False)
        if subprocess.run(["git", "-C", ROOT, "merge-base", "--is-ancestor", sha, "origin/master"]).returncode != 0:
            holds.append(f"source sha {sha[:12]} is not on origin/master")
    p = sum(r["status"] == "pass" for r in res)
    print(f"{date}: {p}/{len(res)} pass, grok scan errors {scan}, no-uvx failures {nouvx}, versions {v}")
    if last and (last.get("versions") or {}) != v:
        print("note: agent versions differ from the last published run; the report shows this (not a hold)")
    if holds:
        print("HOLD, not publishable:\n  - " + "\n  - ".join(holds)); return 2
    if check:
        print("check only: publishable, nothing written"); return 0
    if "bubblewrap" in run.get("sandbox", "") and "--linux" not in argv:
        run["sandbox"] = DOCKER  # run_tests.py before Nov 13 hard-coded bubblewrap; the Mac runs in Docker
    out = os.path.join(ROOT, "testing/results", date + ".json")
    json.dump(run, open(out, "w"), indent=1)
    hp = os.path.join(ROOT, "testing/history.json"); h = json.load(open(hp)) if os.path.exists(hp) else {}
    for r in res:
        L = h.setdefault(f'{r["slug"]}|{r["agent"]}', [])
        L[:] = [e for e in L if e["at"][:10] != date]
        L.append({"at": run["run_at"], "status": r["status"], "log": r["log"]})
        L.sort(key=lambda e: e["at"])
    json.dump(h, open(hp, "w"), indent=0)
    for cmd in (["python3", "testing/daily_report.py"], ["python3", "testing/weekly_scorecard.py", "--write"]):
        subprocess.run(cmd, cwd=ROOT, check=True, stdout=subprocess.DEVNULL if "weekly" in cmd[1] else None)
    print(f"imported {out}; reports.json, latestRows.json, weeks.json and history.json updated")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
