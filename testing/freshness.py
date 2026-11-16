#!/usr/bin/env python3
"""Local SkillMaxx freshness status. Python 3.9+ stdlib only. No network unless --check-public.

Writes testing/status/freshness.json, freshness.md, and freshness.html (gitignored).
Does not push, deploy, post, or install a schedule.

Clocks, kept separate on purpose:
  generated_at   when this status file was written
  last_success   a testing/logs/nightly-*.log line that reached "done" with no failure
  published_at   a GitHub Pages deployment success time from the public API
                 (--check-public only). Never copied from a local build, a results
                 file, a report JSON, or a git commit.

A local eleventy build is not a public deploy. "NOPUSH set, not pushing" means
that nightly run did not push. git push -q prints nothing on success, so a
finished log without NOPUSH is still not proof of GitHub Pages.

From the repo root (Mac or anywhere else with Python 3):

  python3 testing/freshness.py
  python3 testing/freshness.py --check-public
  open testing/status/freshness.html          # Mac

Existing scheduler: the Grok Bot routine "SkillMaxx nightly refresh" (~2:00 AM ET)
runs testing/nightly.sh until someone pauses that routine. This script does not
pause it. Mac launchd is installed only by testing/mac_nightly.sh install on
the Mac, after SKILLMAXX_GROK_ROUTINE_PAUSED=yes. That variable is an operator
attestation, not a check.

Logs live in testing/logs/ on the machine that ran nightly.sh. They are
gitignored, so another clone cannot see NOPUSH until it has those files.
"""
import argparse, glob, json, os, re, subprocess, sys
from datetime import datetime, timedelta, timezone
from urllib import error, request

try:
    from zoneinfo import ZoneInfo
except ImportError:  # pragma: no cover
    ZoneInfo = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVE_URL = "https://skillmaxx.gilventures.ai/reports/latest/"
DEPLOY_API = "https://api.github.com/repos/grandpajackai/skillmaxx/deployments?environment=github-pages&per_page=5"
STALE_HOURS = 36
RUN_STARTED = re.compile(r"Run started ([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}(?:[+-][0-9]{2}:[0-9]{2}|Z))")
STEP_RE = re.compile(r"^== (\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\S+) (.*)$")
FAIL_RE = re.compile(r"NIGHTLY FAILED at step: (.*?) \(see ")

HOW_TO = [
    "From the repo root, with Python 3 and no extra packages:",
    "python3 testing/freshness.py",
    "python3 testing/freshness.py --check-public",
    "Mac: open testing/status/freshness.html",
    "The Grok Bot routine \"SkillMaxx nightly refresh\" (~2:00 AM ET) still runs testing/nightly.sh until you pause it. This file does not pause it.",
    "Mac launchd, only on the Mac after you pause that routine: SKILLMAXX_INSTALL_SCHEDULE=yes SKILLMAXX_GROK_ROUTINE_PAUSED=yes bash testing/mac_nightly.sh install",
    "Nightly logs are gitignored under testing/logs/ on the machine that ran nightly.sh. This file does not claim a public deploy from a local build.",
]


def _dt(date, time, tzname):
    naive = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S")
    tzname = tzname.strip()
    if tzname in ("UTC", "GMT", "UT"):
        return naive.replace(tzinfo=timezone.utc)
    if tzname in ("EST", "EDT", "ET") and ZoneInfo is not None:
        try:
            return naive.replace(tzinfo=ZoneInfo("America/New_York"))
        except Exception:
            return None
    m = re.fullmatch(r"([+-])(\d{2}):?(\d{2})", tzname)
    if not m:
        return None
    sign = 1 if m.group(1) == "+" else -1
    off = timedelta(hours=sign * int(m.group(2)), minutes=sign * int(m.group(3)))
    return naive.replace(tzinfo=timezone(off))


def parse_log(text):
    """Split a nightly log into runs. A new 'sync master' step starts a run."""
    runs, cur = [], []

    def flush():
        if cur:
            runs.append(summarize_run(cur))
            cur.clear()

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = STEP_RE.match(line)
        if m:
            step = m.group(4).strip()
            if step in ("sync master", "trial branch", "local source") and cur:
                flush()
            stamp = {"date": m.group(1), "time": m.group(2), "tz": m.group(3),
                     "raw": f"{m.group(1)} {m.group(2)} {m.group(3)}"}
            cur.append(("step", step, stamp))
            continue
        if "NOPUSH set, not pushing" in line or (line.startswith("TRIAL:") and ("not pushing" in line or "Push disabled" in line)) or (line.startswith("LOCAL:") and "not pushing" in line):
            cur.append(("nopush",))
        elif "NIGHTLY FAILED" in line:
            fm = FAIL_RE.search(line)
            cur.append(("failed", fm.group(1).strip() if fm else "unknown"))
        elif "another nightly is running" in line:
            cur.append(("overlap",))
    flush()
    return runs


def summarize_run(events):
    steps, nopush, failed, done, overlap = [], False, None, None, False
    saw_build = False
    for ev in events:
        if ev[0] == "step":
            step, stamp = ev[1], ev[2]
            steps.append(step)
            if step == "build":
                saw_build = True
            if step == "done":
                done = stamp
        elif ev[0] == "nopush":
            nopush = True
        elif ev[0] == "failed":
            failed = ev[1]
        elif ev[0] == "overlap":
            overlap = True
    build_done = False
    if saw_build and ("commit data" in steps or "done" in steps):
        build_done = True
    if saw_build and failed and "build" not in failed.lower():
        build_done = True
    if failed and "build" in failed.lower():
        build_done = False
    if not steps and overlap and not failed:
        kind = "overlap"
    elif failed:
        kind = "error"
    elif done:
        kind = "ok"
    elif steps:
        kind = "incomplete"
    else:
        kind = "empty"
    done_dt = _dt(done["date"], done["time"], done["tz"]) if done else None
    last_step = None
    for ev in reversed(events):
        if ev[0] == "step":
            last_step = ev[2]
            break
    return {"kind": kind, "steps": steps, "nopush": nopush, "failed": failed, "done": done,
            "done_dt": done_dt, "overlap": overlap, "build_completed": build_done,
            "last_step_dt": _dt(last_step["date"], last_step["time"], last_step["tz"]) if last_step else None}


def _rel(root, path):
    return os.path.relpath(path, root)


def latest_results(root):
    files = sorted(glob.glob(os.path.join(root, "testing", "results", "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].json")))
    if not files:
        return None
    path = files[-1]
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    rows = data.get("results") or []
    return {"source": _rel(root, path), "run_at": data.get("run_at"),
            "pass": sum(1 for r in rows if r.get("status") == "pass"), "total": len(rows)}


def latest_report(root):
    path = os.path.join(root, "src", "_data", "reports.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        data = data[0] if data else None
    if not isinstance(data, dict):
        return None
    return {"source": "src/_data/reports.json", "run_at": data.get("run_at"), "date": data.get("date")}


def repo_nightly_commit(root):
    """Commit in this clone only. A fixture directory inside the repo is not its own clone."""
    try:
        top = subprocess.check_output(
            ["git", "-C", root, "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL, text=True, timeout=5).strip()
        if os.path.realpath(top) != os.path.realpath(root):
            return None
        out = subprocess.check_output(
            ["git", "-C", root, "log", "-1", "--format=%H%x09%cI%x09%s", "--grep=^data: nightly refresh"],
            stderr=subprocess.DEVNULL, text=True, timeout=5)
    except (subprocess.SubprocessError, OSError):
        return None
    line = out.strip()
    if not line or "\t" not in line:
        return None
    sha, committed_at, subject = line.split("\t", 2)
    return {"sha": sha, "committed_at": committed_at, "subject": subject,
            "note": "Commit time in this clone. Not proof of push and not published_at."}


def load_runs(root):
    files = sorted(glob.glob(os.path.join(root, "testing", "logs", "nightly-*.log")))
    found = []
    for path in files:
        with open(path, encoding="utf-8", errors="replace") as f:
            text = f.read()
        for run in parse_log(text):
            run["source"] = _rel(root, path)
            found.append(run)
    return found


def _iso(dt):
    if dt is None:
        return None
    return dt.isoformat()


def summary_text(s):
    bits = []
    state = s["local_state"]
    if state == "unknown":
        bits.append("No local nightly log reached done.")
    elif state == "error":
        bits.append("Latest nightly log failed at step: %s." % (s.get("failed_step") or "unknown"))
    elif state == "stale":
        bits.append("Last local nightly success is older than %s hours." % s["stale_after_hours"])
    elif state == "running":
        bits.append("A nightly log has started and has no done line yet.")
    elif state == "ok":
        bits.append("A local nightly log reached done within the freshness window.")
    if s["nopush"] is True:
        bits.append("That log says this run did not push.")
    if s.get("source_sync"):
        bits.append("Source sync %s for %s at %s." % (s["source_sync"], s.get("source_ref"), (s.get("source_sha") or "")[:12]))
    if s.get("tests_total") is not None:
        bits.append("Install score %s/%s pass is separate from whether the pipeline finished." % (s["tests_pass"], s["tests_total"]))
    if s["local_build_completed"]:
        bits.append("The log got through the local build. That is not a public deploy.")
    if not s["checked_public"]:
        bits.append("Public site was not checked. published_at is unset.")
    elif s["live_page_matches_local_results"]:
        bits.append("The live /reports/latest/ page shows the same test run_at as the local results file.")
    elif s["publish_state"] == "content_mismatch":
        bits.append("The live page shows a different test run than the newest local results file.")
    elif s["publish_state"] == "unreachable":
        bits.append("The public check did not succeed.")
    if s["published_at"]:
        bits.append("published_at is the newest GitHub Pages deployment success time, not the local build time.")
        commit = s.get("repo_nightly_commit") or {}
        sha = s.get("published_sha")
        if sha and commit.get("sha"):
            if sha == commit["sha"]:
                bits.append("That deployment sha matches the newest nightly commit in this clone.")
            else:
                bits.append("That deployment sha does not match the newest nightly commit in this clone.")
    else:
        bits.append("No GitHub Pages deployment time was verified.")
    return " ".join(bits)


def assess(root, now=None, stale_hours=STALE_HOURS, public=None):
    now = now or datetime.now(timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    runs = load_runs(root)
    oks = [r for r in runs if r["kind"] == "ok"]
    newest = runs[-1] if runs else None
    last = oks[-1] if oks else None
    notes, evidence = [], []
    if newest is None:
        local_state = "unknown"
        notes.append("No testing/logs/nightly-*.log here. Logs are gitignored and stay on the machine that ran nightly.sh.")
    elif newest["kind"] == "error":
        local_state = "error"
        evidence.append("%s failed at step: %s" % (newest["source"], newest["failed"]))
    elif newest["kind"] == "incomplete":
        stamp = newest["last_step_dt"]
        recent = stamp is not None and (now - stamp) <= timedelta(hours=6)
        local_state = "running" if recent else "error"
        if not recent:
            notes.append("Log stopped before done and without a NIGHTLY FAILED line.")
        evidence.append("%s has steps but no done line." % newest["source"])
    elif newest["kind"] == "overlap" and last is None:
        local_state = "unknown"
        notes.append("Newest log only recorded that another nightly was already running.")
    else:
        chosen = newest if newest["kind"] == "ok" else last
        done_dt = chosen["done_dt"] if chosen else None
        if done_dt is None:
            local_state = "unknown"
            notes.append("A done line was found but its timezone could not be read, so age was not guessed.")
        elif (now - done_dt) > timedelta(hours=stale_hours):
            local_state = "stale"
        else:
            local_state = "ok"
        if newest["kind"] == "overlap":
            notes.append("Newest log line is a lock skip. last_success is the previous finished run.")
    if last and last["done"]:
        evidence.append("%s reached done at %s." % (last["source"], last["done"]["raw"]))
        if last["nopush"]:
            evidence.append("%s says this run did not push." % last["source"])
    nopush = None
    build = False
    failed_step = None
    if newest:
        nopush = True if newest["nopush"] else False if newest["kind"] == "ok" else None
        build = bool(newest["build_completed"])
        failed_step = newest["failed"]
    results = latest_results(root)
    report = latest_report(root)
    commit = repo_nightly_commit(root)
    if results:
        evidence.append("Local results %s run_at %s (%s/%s pass). This is a test timestamp, not a deploy."
                        % (results["source"], results["run_at"], results["pass"], results["total"]))
    if report and report.get("run_at"):
        evidence.append("Repo report %s run_at %s. In-repo data is not a public deploy."
                        % (report["source"], report["run_at"]))
    if commit:
        evidence.append("Git commit %s at %s (%s). Commit time is not published_at."
                        % (commit["sha"][:12], commit["committed_at"], commit["subject"]))
    source = None
    source_path = os.path.join(root, "testing", "source.json")
    if os.path.exists(source_path):
        try:
            loaded = json.load(open(source_path, encoding="utf-8"))
            source = loaded if isinstance(loaded, dict) else None
        except (OSError, json.JSONDecodeError):
            source = None
    if source:
        evidence.append("Source %s %s sync %s. This is the checkout that was tested, not a deploy."
                        % (source.get("source_ref"), source.get("source_sha"), source.get("source_sync")))
    if nopush is False:
        notes.append("Log has no NOPUSH line and no TRIAL not-pushing line. git push -q is silent on success, so this is not proof of a push or of GitHub Pages.")
    status = {
        "schema_version": 1,
        "generated_at": _iso(now.astimezone(timezone.utc)),
        "last_success": _iso(last["done_dt"]) if last else None,
        "published_at": None,
        "local_state": local_state,
        "publish_state": "not_pushed" if nopush else "unverified",
        "checked_public": public is not None,
        "live_page_matches_local_results": False,
        "nopush": nopush,
        "local_build_completed": build,
        "local_build_is_public_deploy": False,
        "failed_step": failed_step,
        "test_run_at": results["run_at"] if results else None,
        "test_run_source": results["source"] if results else None,
        "tests_pass": results["pass"] if results else None,
        "tests_total": results["total"] if results else None,
        "report_run_at": report.get("run_at") if report else None,
        "report_source": report["source"] if report else None,
        "public_report_run_at": None,
        "public_report_source": None,
        "stale_after_hours": stale_hours,
        "source_ref": source.get("source_ref") if source else None,
        "source_sha": source.get("source_sha") if source else None,
        "source_sync": source.get("source_sync") if source else None,
        "repo_nightly_commit": commit,
        "published_sha": None,
        "sources": {"last_success": last["source"] if last else None, "published_at": None},
        "evidence": evidence,
        "notes": notes,
        "how_to_run": HOW_TO,
    }
    if public is not None:
        _apply_public(status, public)
    status["summary"] = summary_text(status)
    return status


def _apply_public(status, public):
    err = public.get("error")
    page = public.get("page") or ""
    published = public.get("published_at")
    if not public.get("ok") and not page and not published:
        if status["publish_state"] != "not_pushed":
            status["publish_state"] = "unreachable"
        if err:
            status["notes"].append(err)
        return
    m = RUN_STARTED.search(page)
    if m:
        status["public_report_run_at"] = m.group(1)
        status["public_report_source"] = public.get("page_url") or LIVE_URL
        status["evidence"].append("Live page %s contains Run started %s."
                                   % (status["public_report_source"], m.group(1)))
    elif page:
        status["notes"].append("Live page was fetched but no Run started timestamp was found. Not treated as a match.")
    if published:
        status["published_at"] = published
        status["published_sha"] = public.get("published_sha")
        status["sources"]["published_at"] = public.get("published_at_source") or DEPLOY_API
        status["evidence"].append("GitHub Pages success time %s sha %s from %s."
                                   % (published, status["published_sha"] or "unknown", status["sources"]["published_at"]))
    match = bool(status["test_run_at"] and status["public_report_run_at"] == status["test_run_at"])
    status["live_page_matches_local_results"] = match
    if status["nopush"] is True:
        status["publish_state"] = "not_pushed"
        if match:
            status["notes"].append("Nightly log did not push. The live page currently shows the same test run_at, so the data is public by some other push.")
        elif status["public_report_run_at"]:
            status["notes"].append("Nightly log did not push. The live page shows a different test run.")
    elif match:
        status["publish_state"] = "live_matches"
    elif status["public_report_run_at"]:
        status["publish_state"] = "content_mismatch"
    elif not public.get("ok") and not published:
        status["publish_state"] = "unreachable"
    if err and (not public.get("ok") or not published):
        status["notes"].append(err)


def _http_get(url, timeout=20):
    req = request.Request(url, headers={
        "User-Agent": "skillmaxx-freshness",
        "Accept": "application/vnd.github+json",
    })
    with request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read(750_000).decode("utf-8", "replace")


def check_public(timeout=20):
    """One live read of the public report page and the public Pages deployment API.
    Failures stay in the returned dict. Nothing is written outside the status files.
    """
    out = {"ok": False, "error": None, "page": "", "page_url": LIVE_URL,
           "published_at": None, "published_at_source": None, "published_sha": None}
    errors = []
    try:
        status, body = _http_get(LIVE_URL, timeout=timeout)
        if status == 200:
            out["page"] = body
        else:
            errors.append("Live page HTTP %s." % status)
    except (error.URLError, TimeoutError, OSError) as exc:
        errors.append("Live page fetch failed: %s." % exc)
    try:
        status, body = _http_get(DEPLOY_API, timeout=timeout)
        if status != 200:
            errors.append("Deployment API HTTP %s." % status)
        else:
            published, source, sha = _newest_pages_success(json.loads(body), timeout)
            out["published_at"] = published
            out["published_at_source"] = source
            out["published_sha"] = sha
            if not published:
                errors.append("Deployment API returned no successful github-pages status.")
    except (error.URLError, TimeoutError, OSError, json.JSONDecodeError, ValueError) as exc:
        errors.append("Deployment API fetch failed: %s." % exc)
    out["ok"] = bool(out["page"])
    if errors:
        out["error"] = " ".join(errors)
    return out


def _newest_pages_success(deployments, timeout):
    if not isinstance(deployments, list):
        return None, None
    best = None
    best_src = None
    best_sha = None
    for dep in deployments[:5]:
        if not isinstance(dep, dict):
            continue
        url = dep.get("statuses_url")
        if not url:
            continue
        try:
            status, body = _http_get(url, timeout=timeout)
        except (error.URLError, TimeoutError, OSError):
            continue
        if status != 200:
            continue
        try:
            statuses = json.loads(body)
        except json.JSONDecodeError:
            continue
        if not isinstance(statuses, list):
            continue
        for st in statuses:
            if isinstance(st, dict) and st.get("state") == "success" and st.get("created_at"):
                if best is None or st["created_at"] > best:
                    best = st["created_at"]
                    best_src = url
                    best_sha = dep.get("sha")
                break
    return best, best_src, best_sha


def _esc(value):
    return (str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def render_md(status):
    c = status["repo_nightly_commit"]
    lines = [
        "# SkillMaxx freshness",
        "",
        status["summary"],
        "",
        "| Clock | Value | Meaning |",
        "|---|---|---|",
        "| generated_at | %s | When this file was written |" % _cell(status["generated_at"]),
        "| last_success | %s | Nightly log reached done (%s) |" % (_cell(status["last_success"]), _cell(status["sources"]["last_success"])),
        "| published_at | %s | GitHub Pages success time (%s) |" % (_cell(status["published_at"]), _cell(status["sources"]["published_at"])),
        "",
        "## Local nightly",
        "",
        "- local_state: `%s`" % status["local_state"],
        "- nopush: `%s`" % status["nopush"],
        "- local_build_completed: `%s` (never a public deploy)" % status["local_build_completed"],
        "- failed_step: `%s`" % status["failed_step"],
        "- test_run_at: `%s` from `%s`" % (_cell(status["test_run_at"]), _cell(status["test_run_source"])),
        "- tests: %s / %s pass" % (_cell(status["tests_pass"]), _cell(status["tests_total"])),
        "- report_run_at: `%s` from `%s` (in the repo; not a deploy)" % (_cell(status["report_run_at"]), _cell(status["report_source"])),
        "",
        "## Public site",
        "",
        "- publish_state: `%s`" % status["publish_state"],
        "- checked_public: `%s`" % status["checked_public"],
        "- live_page_matches_local_results: `%s`" % status["live_page_matches_local_results"],
        "- public_report_run_at: `%s`" % _cell(status["public_report_run_at"]),
        "- published_sha: `%s`" % _cell(status.get("published_sha")),
        "- local_build_is_public_deploy: `false`",
        "",
        "## Repo commit",
        "",
    ]
    if c:
        lines.append("- `%s` %s — %s" % (c["sha"][:12], c["committed_at"], c["subject"]))
        lines.append("- %s" % c["note"])
    else:
        lines.append("- No `data: nightly refresh` commit found in this clone.")
    lines += ["", "## Evidence", ""]
    lines += ["- %s" % item for item in status["evidence"]] or ["- (none)"]
    if status["notes"]:
        lines += ["", "## Notes", ""]
        lines += ["- %s" % item for item in status["notes"]]
    lines += ["", "## Run this", ""]
    lines += ["- %s" % item for item in status["how_to_run"]]
    lines.append("")
    return "\n".join(lines)


def _cell(value):
    return "—" if value is None else str(value)


def render_html(status):
    c = status["repo_nightly_commit"]
    commit = "<p>No <code>data: nightly refresh</code> commit found in this clone.</p>"
    if c:
        commit = "<p><code>%s</code> %s — %s</p><p>%s</p>" % (
            _esc(c["sha"][:12]), _esc(c["committed_at"]), _esc(c["subject"]), _esc(c["note"]))
    ev = "".join("<li>%s</li>" % _esc(x) for x in status["evidence"]) or "<li>(none)</li>"
    notes = "".join("<li>%s</li>" % _esc(x) for x in status["notes"])
    how = "".join("<li><code>%s</code></li>" % _esc(x) if x.startswith("python3") or x.startswith("Mac:") or x[:2].isdigit()
                  else "<li>%s</li>" % _esc(x) for x in status["how_to_run"])
    rows = [
        ("generated_at", status["generated_at"], "When this file was written"),
        ("last_success", status["last_success"], "Nightly log reached done"),
        ("published_at", status["published_at"], "GitHub Pages deployment success time"),
    ]
    tr = "".join("<tr><th>%s</th><td>%s</td><td>%s</td></tr>" % (_esc(a), _esc(_cell(b)), _esc(c)) for a, b, c in rows)
    return """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>SkillMaxx freshness</title>
<style>
body{font:16px/1.45 system-ui,sans-serif;margin:2rem auto;max-width:42rem;color:#1c1917;background:#fafaf9}
h1{font-size:1.4rem} table{border-collapse:collapse;width:100%%}
th,td{border-bottom:1px solid #e7e5e4;text-align:left;padding:.4rem .5rem;vertical-align:top}
code{font-size:.9em} .state{font-weight:600}
</style></head><body>
<h1>SkillMaxx freshness</h1>
<p>%s</p>
<table><thead><tr><th>Clock</th><th>Value</th><th>Meaning</th></tr></thead><tbody>%s</tbody></table>
<h2>Local nightly</h2>
<ul>
<li>local_state: <span class="state">%s</span></li>
<li>nopush: %s</li>
<li>local_build_completed: %s (never a public deploy)</li>
<li>failed_step: %s</li>
<li>test_run_at: %s from %s</li>
<li>tests: %s / %s pass</li>
<li>report_run_at: %s from %s (in the repo; not a deploy)</li>
</ul>
<h2>Public site</h2>
<ul>
<li>publish_state: <span class="state">%s</span></li>
<li>checked_public: %s</li>
<li>live_page_matches_local_results: %s</li>
<li>public_report_run_at: %s</li>
<li>published_sha: %s</li>
<li>local_build_is_public_deploy: false</li>
</ul>
<h2>Repo commit</h2>
%s
<h2>Evidence</h2><ul>%s</ul>
%s
<h2>Run this</h2><ul>%s</ul>
</body></html>
""" % (_esc(status["summary"]), tr, _esc(status["local_state"]), _esc(status["nopush"]),
       _esc(status["local_build_completed"]), _esc(status["failed_step"]),
       _esc(_cell(status["test_run_at"])), _esc(_cell(status["test_run_source"])),
       _esc(_cell(status["tests_pass"])), _esc(_cell(status["tests_total"])),
       _esc(_cell(status["report_run_at"])), _esc(_cell(status["report_source"])),
       _esc(status["publish_state"]), _esc(status["checked_public"]),
       _esc(status["live_page_matches_local_results"]), _esc(_cell(status["public_report_run_at"])),
       _esc(_cell(status.get("published_sha"))),
       commit, ev, ("<h2>Notes</h2><ul>%s</ul>" % notes) if notes else "", how)


def write_status(status, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    paths = {}
    for name, text in (("freshness.json", json.dumps(status, indent=2) + "\n"),
                       ("freshness.md", render_md(status)),
                       ("freshness.html", render_html(status))):
        path = os.path.join(out_dir, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        paths[name] = path
    return paths


def main(argv=None):
    p = argparse.ArgumentParser(description="Write local SkillMaxx freshness status. Does not deploy.")
    p.add_argument("--root", default=ROOT)
    p.add_argument("--out", help="output directory (default: <root>/testing/status)")
    p.add_argument("--stale-hours", type=float, default=STALE_HOURS)
    p.add_argument("--check-public", action="store_true",
                   help="read the live report page and the public GitHub Pages deployment API")
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args(argv)
    public = check_public() if args.check_public else None
    status = assess(args.root, stale_hours=args.stale_hours, public=public)
    out = args.out or os.path.join(args.root, "testing", "status")
    paths = write_status(status, out)
    if not args.quiet:
        print(status["summary"])
        print(paths["freshness.json"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
