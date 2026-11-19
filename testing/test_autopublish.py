#!/usr/bin/env python3
"""Offline tests for the no-LLM auto content (Nov 18): newsletter issue (numbering, idempotency, no placeholders),
Wednesday post, single-Sunday-post guard, Monday newsletter check (mocked HTTP), and the alert kind/wiring.
No network (the alert test uses a local 127.0.0.1 server), no sends, no Beehiiv."""
import glob, http.server, importlib.util, io, json, os, re, shutil, subprocess, sys, tempfile, threading, urllib.error
from datetime import date

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def fixture():
    """Temp repo root with the real committed data the generators read."""
    t = tempfile.mkdtemp(prefix="smx-auto-")
    for rel in ["src/_data/weeks.json", "src/_data/reports.json", "src/_data/runNotes.json", "data/skills.json",
                "testing/results/2026-11-18.json"] + glob.glob("src/newsletter/issue-[0-9]*.md", root_dir=ROOT) + glob.glob("src/blog/*.njk", root_dir=ROOT):
        os.makedirs(os.path.dirname(os.path.join(t, rel)), exist_ok=True)
        shutil.copy(os.path.join(ROOT, rel), os.path.join(t, rel))
    return t


def fm(text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    assert m, "no front matter"
    return {l.split(":", 1)[0].strip(): l.split(":", 1)[1].strip() for l in m.group(1).splitlines() if ":" in l}


def quiet(fn, *a):
    old = sys.stdout; sys.stdout = io.StringIO()
    try:
        rc = fn(*a); return rc, sys.stdout.getvalue()
    finally:
        sys.stdout = old


def test_newsletter():
    t = fixture()
    nl = load("growth/scripts/newsletter_auto.py", "nl"); nl.ROOT = t
    open(os.path.join(t, "src/newsletter/issue-4.draft.md"), "w").write("draft, must not count")
    assert nl.next_issue_no() == 4, "drafts must not change numbering"
    assert nl.issue_for_week(date(2026, 11, 22)) is None
    rc, out = quiet(nl.main, ["2026-11-22"])
    p = os.path.join(t, "src/newsletter/issue-4.md")
    assert rc == 0 and os.path.exists(p), out
    text = open(p, encoding="utf-8").read()
    f = fm(text)
    ref = fm(open(os.path.join(ROOT, "src/newsletter/issue-3.md"), encoding="utf-8").read())
    assert set(ref) <= set(f), f"missing front matter keys: {set(ref) - set(f)}"
    assert f["permalink"] == "/newsletter/issue-4/" and f["issue"] == "4" and f["tags"] == "issues" and f["issueDate"] == '"2026-11-22"'
    assert "permalink: false" not in text and "eleventyExcludeFromCollections" not in text
    json.loads(f["jsonld"])
    assert nl.problems(text) == [], nl.problems(text)
    for bad in ("<!--", "TODO", "DRAFT", "None", "undefined", "nan%", "??"):
        assert bad not in text, bad
    assert text.rstrip().endswith('{% include "nlembed.njk" %}') and '<div class="wrap prose nlissue">' in text
    assert "/reports/week/2026-47/" in text and "Issue #4" in text
    # Idempotent: same day, later day of the same week, and Monday catch-up for the Sunday all skip without touching it.
    m0 = os.stat(p).st_mtime_ns
    for day in ("2026-11-22", "2026-11-21", "2026-11-16"):
        rc, out = quiet(nl.main, [day]); assert rc == 0 and "already covers" in out, out
    assert os.stat(p).st_mtime_ns == m0 and open(p, encoding="utf-8").read() == text
    assert len(glob.glob(os.path.join(t, "src/newsletter/issue-*.md"))) == 4 + 1  # 1-4 plus the draft
    # Next week numbers to 5 once there is data; a week without runs publishes nothing.
    rc, out = quiet(nl.main, ["2026-11-29"]); assert rc == 0 and "no runs" in out and not os.path.exists(os.path.join(t, "src/newsletter/issue-5.md")), out
    weeks = json.load(open(os.path.join(t, "src/_data/weeks.json")))
    w48 = dict(weeks[0], key="2026-48", start="2026-11-23", end="2026-11-29")
    json.dump([w48] + weeks, open(os.path.join(t, "src/_data/weeks.json"), "w"))
    rc, out = quiet(nl.main, ["2026-11-29"]); assert rc == 0 and os.path.exists(os.path.join(t, "src/newsletter/issue-5.md")), out
    assert "/newsletter/issue-5/" in open(os.path.join(t, "src/newsletter/issue-5.md")).read()
    # Placeholder guard: bad source data -> refuse, write nothing.
    w49 = dict(weeks[0], key="2026-49", start="2026-11-30", end="2026-12-06", standout={"slug": "x", "name": "TODO", "agents": []})
    json.dump([w49, w48] + weeks, open(os.path.join(t, "src/_data/weeks.json"), "w"))
    rc, out = quiet(nl.main, ["2026-12-06"]); assert rc == 1 and "REFUSED" in out and not os.path.exists(os.path.join(t, "src/newsletter/issue-6.md")), out
    shutil.rmtree(t); print("ok newsletter: numbering, idempotency, front matter, no placeholders, refusal")


def test_midweek():
    t = fixture()
    mw = load("growth/scripts/midweek_blog_auto.py", "mw"); mw.ROOT = t
    for day, why in (("2026-11-22", "Sunday"), ("2026-11-17", "not a Wednesday")):
        rc, out = quiet(mw.main, [day]); assert rc == 0 and not glob.glob(os.path.join(t, "src/blog/midweek-*")), (why, out)
    rc, out = quiet(mw.main, ["2026-11-18"])
    p = os.path.join(t, "src/blog/midweek-2026-47.njk")
    assert rc == 0 and os.path.exists(p), out
    text = open(p, encoding="utf-8").read(); f = fm(text)
    assert f["permalink"] == "/blog/midweek-2026-47/" and f["tags"] == "blog" and f["layout"] == "base.njk" and f["issueDate"] == '"2026-11-18"'
    assert json.loads(f["jsonld"])["@type"] == "BlogPosting" and f["title"] and f["desc"]
    assert len(json.loads(f["desc"])) <= 160
    for href in ("/works-in/", "/skills/", "/reports/2026-11-18/", "/reports/latest/", "/how-we-test/", "/best/"):
        assert f'href="{href}' in text, href
    assert '<p class="answer">' in text and "<table" in text and "{{" not in text and "None" not in text
    sunday = load("growth/scripts/weekly_blog_auto.py", "wb1")
    assert not sunday.sunday_posts("2026-11-22", "2026-47", t), "the Wednesday post must not count as a Sunday post"
    m0 = os.stat(p).st_mtime_ns
    rc, out = quiet(mw.main, ["2026-11-19"]); assert "exists" in out and os.stat(p).st_mtime_ns == m0, out  # Thu catch-up skips
    shutil.rmtree(t); print("ok midweek: Wed only, distinct URL, SEO fields, links, idempotent")


def test_sunday_guard():
    t = fixture()
    wb = load("growth/scripts/weekly_blog_auto.py", "wb"); wb.ROOT = t
    weeks = json.load(open(os.path.join(t, "src/_data/weeks.json")))
    rc, out = quiet(wb.main, ["2026-11-22"]); p = os.path.join(t, "src/blog/week-2026-47.njk")
    assert rc == 0 and os.path.exists(p), out
    rc, out = quiet(wb.main, ["2026-11-22"]); assert "exists" in out, out
    rc, out = quiet(wb.main, ["2026-11-23"]); assert "exists" in out, out  # Monday catch-up: same week, no duplicate
    # Another post already dated that Sunday (e.g. hand/Grok) -> the auto post is not written.
    t2 = fixture(); wb.ROOT = t2
    open(os.path.join(t2, "src/blog/hand.njk"), "w").write('---\nlayout: base.njk\ntitle: "x"\npermalink: /blog/x/\ntags: blog\nissueDate: "2026-11-22"\n---\nbody\n')
    rc, out = quiet(wb.main, ["2026-11-22"])
    assert "already exists" in out and not os.path.exists(os.path.join(t2, "src/blog/week-2026-47.njk")), out
    # Repo invariant: at most one blog post per Sunday in the committed tree.
    seen = {}
    for b in glob.glob(os.path.join(ROOT, "src/blog/*.njk")):
        m = re.search(r'^issueDate:\s*"?(\d{4}-\d\d-\d\d)', open(b, encoding="utf-8").read(), re.M)
        if m and date.fromisoformat(m.group(1)).isoweekday() == 7:
            assert m.group(1) not in seen, f"two Sunday posts on {m.group(1)}: {seen[m.group(1)]}, {b}"
            seen[m.group(1)] = b
    shutil.rmtree(t); shutil.rmtree(t2); print("ok sunday guard: one post per Sunday")


class Resp:
    def __init__(self, status): self.status = status
    def __enter__(self): return self
    def __exit__(self, *a): return False


def test_monday_check():
    ck = load("testing/check_newsletter_live.py", "ck")
    issues = {3: 'issueDate: "2026-11-13"\n', 4: 'issueDate: "2026-11-22"\nweek: "2026-47"\n'}
    assert ck.expected_issue(issues, date(2026, 11, 23))[:2] == (4, "2026-47")
    assert ck.expected_issue(issues, date(2026, 11, 16))[:2] == (3, "2026-46")
    assert ck.expected_issue({3: issues[3]}, date(2026, 11, 23))[0] is None
    urls = []
    def ok(req, timeout=0): urls.append(req.full_url); return Resp(200)
    def nf(req, timeout=0): raise urllib.error.HTTPError(req.full_url, 404, "nf", {}, None)
    def down(req, timeout=0): raise OSError("no route")
    good, msg = ck.check(date(2026, 11, 23), issues, "https://example.test", ok)
    assert good and urls == ["https://example.test/newsletter/issue-4/"], msg
    good, msg = ck.check(date(2026, 11, 23), issues, "https://example.test", nf); assert not good and "HTTP 404" in msg and "issue-4" in msg
    good, msg = ck.check(date(2026, 11, 23), issues, "https://example.test", down); assert not good and "no response" in msg
    good, msg = ck.check(date(2026, 11, 23), {3: issues[3]}, "https://example.test", ok); assert not good and "No SkillMaxx Weekly issue" in msg
    assert ck.main(["--date", "2026-11-24", "--no-fetch"]) == 0  # not a Monday: no check
    print("ok monday check: expected issue, 200/404/down/missing")


def test_alert_wiring():
    """nightly_alert.sh posts kind=newsletter_missing; the watchdog's Monday check calls it once; nothing secret printed."""
    got = []
    class H(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            got.append((self.path, self.headers.get("Authorization"), json.loads(self.rfile.read(int(self.headers["Content-Length"])))))
            self.send_response(404 if self.path.startswith("/newsletter") else 200); self.end_headers()
        def do_GET(self):
            self.send_response(404); self.end_headers()
        def log_message(self, *a): pass
    srv = http.server.HTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_port}"
    st = tempfile.mkdtemp(); key = "k" * 12 + "SECRETKEY"
    env = {**os.environ, "SKILLMAXX_ALERT_WEBHOOK_URL": base + "/hook-secret-path", "SKILLMAXX_ALERT_WEBHOOK_KEY": key,
           "SKILLMAXX_ALERT_ENV": "/dev/null", "SKILLMAXX_STATE": st}
    env.pop("SKILLMAXX_ALERT_DISABLE", None)
    out = subprocess.run(["bash", "-c", f'. "{ROOT}/testing/nightly_alert.sh"; SMX_ALERT_KIND=newsletter_missing smx_alert newsletter "issue missing" "" 2026-11-23'],
                         capture_output=True, text=True, env=env).stdout
    assert got and got[-1][2]["kind"] == "newsletter_missing" and got[-1][2]["step"] == "newsletter" and got[-1][1] == f"Bearer {key}", got
    assert "hook-secret-path" not in out and key not in out and "http=200" in out, out
    out = subprocess.run(["bash", "-c", f'. "{ROOT}/testing/nightly_alert.sh"; smx_alert x "y" "" 2026-11-23'], capture_output=True, text=True, env=env).stdout
    assert got[-1][2]["kind"] == "nightly_failure", "default kind unchanged"
    # Watchdog wiring: Monday 08 ET with a primary checkout that has no issue for last week -> retry first, alert on 2nd miss.
    prim = fixture(); subprocess.run(["git", "init", "-q", prim], check=True)
    # Today's run "succeeded" and published, so the rest of the watchdog stays quiet and never runs a publish.
    open(os.path.join(st, "last-success-date"), "w").write("2026-11-23\n")
    open(os.path.join(st, "publish-status"), "w").write("2026-11-23 published\n")
    n0 = len(got)
    wenv = {**env, "SKILLMAXX_PRIMARY": prim, "SKILLMAXX_WATCHDOG_ANY_OS": "1", "SKILLMAXX_LAUNCHD": "1",
            "SKILLMAXX_EASTERN_DATE": "2026-11-23", "SKILLMAXX_SITE": base, "SKILLMAXX_ENV_FILE": "/dev/null",
            "SKILLMAXX_EASTERN_HOUR": "08", "SKILLMAXX_AUTO_PUBLISH": "0", "SKILLMAXX_SOURCE_REF": "master"}
    r1 = subprocess.run(["bash", f"{ROOT}/testing/local_nightly.sh"], capture_output=True, text=True, env=wenv)
    assert "No SkillMaxx Weekly issue" in r1.stdout and len(got) == n0, r1.stdout + r1.stderr
    assert open(os.path.join(st, "newsletter-checked")).read().strip() == "2026-11-23 retry"
    r2 = subprocess.run(["bash", f"{ROOT}/testing/local_nightly.sh"], capture_output=True, text=True, env={**wenv, "SKILLMAXX_EASTERN_HOUR": "09"})
    assert len(got) == n0 + 1 and got[-1][2]["kind"] == "newsletter_missing", r2.stdout
    r3 = subprocess.run(["bash", f"{ROOT}/testing/local_nightly.sh"], capture_output=True, text=True, env={**wenv, "SKILLMAXX_EASTERN_HOUR": "10"})
    assert len(got) == n0 + 1, "one alert per Monday"
    for r in (r1, r2, r3):
        assert key not in r.stdout + r.stderr and "hook-secret-path" not in r.stdout + r.stderr
    # Not Monday -> no check at all.
    os.remove(os.path.join(st, "newsletter-checked"))
    subprocess.run(["bash", f"{ROOT}/testing/local_nightly.sh"], capture_output=True, text=True, env={**wenv, "SKILLMAXX_EASTERN_DATE": "2026-11-24"})
    assert not os.path.exists(os.path.join(st, "newsletter-checked"))
    srv.shutdown(); shutil.rmtree(st); shutil.rmtree(prim)
    print("ok alert wiring: kind newsletter_missing, retry then one alert, no secrets printed")


def test_publish_script():
    s = open(os.path.join(ROOT, "testing/publish_nightly.sh"), encoding="utf-8").read()
    assert "newsletter_auto.py" in s and "midweek_blog_auto.py" in s and "weekly_blog_auto.py" in s
    assert "buffer_weekly" not in s.split("# Sundays: do not run buffer_weekly.py")[0], "Buffer stays off"
    assert "SKILLMAXX_PRODUCTION=" not in s and "SKILLMAXX_ALLOW_PUSH=" not in s and "beehiiv" not in s.lower()
    assert subprocess.run(["bash", "-n", os.path.join(ROOT, "testing/publish_nightly.sh")]).returncode == 0
    # Generators are offline: no network or mail code at all. The Monday check only GETs the public site.
    for f in ("growth/scripts/newsletter_auto.py", "growth/scripts/midweek_blog_auto.py", "growth/scripts/weekly_blog_auto.py"):
        src = open(os.path.join(ROOT, f), encoding="utf-8").read()
        for bad in ("urllib", "requests", "smtplib", "http.client", "socket", "subprocess"):
            assert f"import {bad}" not in src and f"{bad}." not in src, f"{f} must stay offline ({bad})"
    ck = open(os.path.join(ROOT, "testing/check_newsletter_live.py"), encoding="utf-8").read()
    assert "smtplib" not in ck and "method=\"POST\"" not in ck and "data=" not in ck, "the check never posts"
    print("ok publish script: wired, no Buffer/Beehiiv/prod flags")


if __name__ == "__main__":
    test_newsletter(); test_midweek(); test_sunday_guard(); test_monday_check(); test_alert_wiring(); test_publish_script()
    print("test_autopublish: all ok")
