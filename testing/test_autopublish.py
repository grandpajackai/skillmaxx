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


FIX = os.path.join(ROOT, "testing/fixtures/autopublish")


def fixture():
    """Temp repo root from frozen data (testing/fixtures/autopublish, snapshot of Nov 18, 2026) plus issues 1-3 and the
    two hand-written posts, so the tests don't drift as real issues/posts/weeks are published."""
    t = tempfile.mkdtemp(prefix="smx-auto-")
    for src, rel in [("weeks.json", "src/_data/weeks.json"), ("reports.json", "src/_data/reports.json"),
                     ("runNotes.json", "src/_data/runNotes.json"), ("skills.json", "data/skills.json"),
                     ("results-2026-11-18.json", "testing/results/2026-11-18.json")]:
        os.makedirs(os.path.dirname(os.path.join(t, rel)), exist_ok=True)
        shutil.copy(os.path.join(FIX, src), os.path.join(t, rel))
    for rel in ["src/newsletter/issue-1.md", "src/newsletter/issue-2.md", "src/newsletter/issue-3.md",
                "src/blog/six-nights.njk", "src/blog/mcp-claude-code-vs-cursor.njk",
                "growth/newsletter/mentions.json"]:
        src = os.path.join(ROOT, rel)
        if not os.path.exists(src):
            continue
        os.makedirs(os.path.dirname(os.path.join(t, rel)), exist_ok=True)
        shutil.copy(src, os.path.join(t, rel))
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
    assert "Independent mention" in text
    assert "https://www.autonomous.ai/lamp" in text and "https://github.com/autonomous-ai/lampOS" in text
    assert "Not tested by SkillMaxx; independent mention, not sponsored." in text
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
    t5first = open(os.path.join(t, "src/newsletter/issue-5.md")).read()
    assert "/newsletter/issue-5/" in t5first
    assert "autonomous.ai/lamp" not in t5first and "lampOS" not in t5first, "mentions are one-time per listed issue"
    # Placeholder guard: bad source data -> refuse, write nothing.
    w49 = dict(weeks[0], key="2026-49", start="2026-11-30", end="2026-12-06", standout={"slug": "x", "name": "TODO", "agents": []})
    json.dump([w49, w48] + weeks, open(os.path.join(t, "src/_data/weeks.json"), "w"))
    rc, out = quiet(nl.main, ["2026-12-06"]); assert rc == 1 and "REFUSED" in out and not os.path.exists(os.path.join(t, "src/newsletter/issue-6.md")), out
    # Fresh Sunday radar-json renders real news and strips placeholder-looking items.
    rj = os.path.join(t, "radar.json")
    json.dump([
        {"title": "Fresh MCP release", "url": "https://news.ycombinator.com/item?id=123", "points": 42, "comments": 7},
        {"title": "TBD broken item", "url": "https://news.ycombinator.com/item?id=999", "points": 10, "comments": 1},
    ], open(rj, "w"))
    os.remove(os.path.join(t, "src/newsletter/issue-5.md"))
    rc, out = quiet(nl.main, ["2026-11-29", "--radar-json", rj])
    assert rc == 0 and os.path.exists(os.path.join(t, "src/newsletter/issue-5.md")), out
    t5 = open(os.path.join(t, "src/newsletter/issue-5.md")).read()
    assert "Fresh MCP release" in t5 and "TBD broken item" not in t5 and not nl.problems(t5), t5
    shutil.rmtree(t); print("ok newsletter: numbering, idempotency, front matter, no placeholders, refusal, radar-json")


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
    assert "fetch_radar_hn.py" in s and "check_first_subscriber.py" in s and "send_telegram_requests.py" in s
    assert "SKILLMAXX_PRODUCTION=" not in s and "SKILLMAXX_ALLOW_PUSH=" not in s
    for bad_bh in ("/posts", "save_post", "schedule_post", "create_post"):
        assert bad_bh not in s.lower(), f"publish_nightly.sh must never publish to Beehiiv ({bad_bh})"
    assert subprocess.run(["bash", "-n", os.path.join(ROOT, "testing/publish_nightly.sh")]).returncode == 0
    # Generators are offline: no network or mail code at all. The Monday check only GETs the public site.
    for f in ("growth/scripts/newsletter_auto.py", "growth/scripts/midweek_blog_auto.py", "growth/scripts/weekly_blog_auto.py", "growth/scripts/blog_queue.py"):
        src = open(os.path.join(ROOT, f), encoding="utf-8").read()
        for bad in ("urllib", "requests", "smtplib", "http.client", "socket", "subprocess"):
            assert f"import {bad}" not in src and f"{bad}." not in src, f"{f} must stay offline ({bad})"
    ck = open(os.path.join(ROOT, "testing/check_newsletter_live.py"), encoding="utf-8").read()
    assert "smtplib" not in ck and "method=\"POST\"" not in ck and "data=" not in ck, "the check never posts"
    print("ok publish script: wired, no Buffer/Beehiiv/prod flags")



def test_first_subscriber_alert():
    td = tempfile.mkdtemp()
    st_dir = os.path.join(td, "state")
    os.makedirs(st_dir, exist_ok=True)
    hq_dir = os.path.join(td, "brandon-hq")
    os.makedirs(os.path.join(hq_dir, "hq"), exist_ok=True)
    log_path = os.path.join(td, "alert_calls.json")
    open(os.path.join(hq_dir, "hq", "alert.py"), "w").write(
        "import json, sys\n"
        f"open({log_path!r}, 'a').write(json.dumps(sys.argv[1:]) + '\\n')\n"
        "print('sent=telegram')\n"
    )
    script = os.path.join(ROOT, "testing/check_first_subscriber.py")
    env = {**os.environ, "SKILLMAXX_STATE": st_dir, "SKILLMAXX_BEEHIIV_ENV": "/dev/null"}
    env.pop("BEEHIIV_API_KEY", None)

    r0 = subprocess.run([sys.executable, script, "--hq-dir", hq_dir], capture_output=True, text=True, env=env)
    assert r0.returncode == 0 and not os.path.exists(log_path), r0.stdout + r0.stderr

    # Local test exclusion list + committed SHA-256 hash config both exclude test accounts cleanly.
    open(os.path.join(st_dir, "test-subscribers.json"), "w").write(json.dumps(["excluded-tester@example.com"]))
    snap = os.path.join(st_dir, "beehiiv-subscribers.json")
    open(snap, "w").write(json.dumps([
        {"email": "grandpajackai@gmail.com", "status": "active"},
        {"email": "skillmaxx@gilventures.ai", "status": "active"},
        {"email": "excluded-tester@example.com", "status": "active"},
    ]))
    r1 = subprocess.run([sys.executable, script, "--hq-dir", hq_dir], capture_output=True, text=True, env=env)
    assert r1.returncode == 0 and "0 real subscribers" in r1.stdout and not os.path.exists(log_path), r1.stdout + r1.stderr
    # Also verify committed testing/beehiiv_test_subscribers.json holds 5 valid SHA-256 hashes (no raw emails).
    cfg = json.load(open(os.path.join(ROOT, "testing/beehiiv_test_subscribers.json")))
    assert len(cfg["excluded_sha256"]) == 5 and all(len(h) == 64 for h in cfg["excluded_sha256"])

    open(snap, "w").write(json.dumps([
        {"email": "excluded-tester@example.com", "status": "active"},
        {"email": "reader@example.org", "status": "active", "acquisition_source": "github"},
    ]))
    r2 = subprocess.run([sys.executable, script, "--hq-dir", hq_dir], capture_output=True, text=True, env=env)
    assert r2.returncode == 0 and "alerted for 1 real subscriber" in r2.stdout, r2.stdout + r2.stderr
    calls = open(log_path).read().splitlines()
    assert len(calls) == 1 and "skillmaxx_first_subscriber" in calls[0], calls
    assert os.path.isfile(os.path.join(st_dir, "first-subscriber-alerted.json"))

    r3 = subprocess.run([sys.executable, script, "--hq-dir", hq_dir], capture_output=True, text=True, env=env)
    assert r3.returncode == 0 and "already alerted" in r3.stdout
    assert len(open(log_path).read().splitlines()) == 1
    shutil.rmtree(td)
    print("ok first subscriber alert: test accounts excluded, one-shot hq.alert wired")




def test_telegram_requests():
    td = tempfile.mkdtemp()
    st_dir = os.path.join(td, "state")
    os.makedirs(st_dir, exist_ok=True)
    hq_dir = os.path.join(td, "brandon-hq")
    os.makedirs(os.path.join(hq_dir, "hq"), exist_ok=True)
    log_path = os.path.join(td, "tg_calls.json")
    open(os.path.join(hq_dir, "hq", "alert.py"), "w").write(
        "import json, sys\n"
        f"open({log_path!r}, 'a').write(json.dumps(sys.argv[1:]) + '\\n')\n"
        "print(json.dumps({'ping': True, 'reason': 'ok', 'channels': ['mac', 'telegram']}))\n"
    )
    script = os.path.join(ROOT, "testing/send_telegram_requests.py")
    env = {**os.environ, "SKILLMAXX_STATE": st_dir}
    reqs = json.load(open(os.path.join(ROOT, "growth/telegram/REQUESTS.json")))
    assert any(r["id"] == "req-002-github-skillmaxx-vault" for r in reqs)
    r1 = subprocess.run([sys.executable, script, "--hq-dir", hq_dir], capture_output=True, text=True, env=env)
    assert r1.returncode == 0 and f"({len(reqs)} sent" in r1.stdout, r1.stdout + r1.stderr
    calls = open(log_path).read().splitlines()
    assert len(calls) == len(reqs) and "--severity" in calls[0] and "critical" in calls[0], calls
    r2 = subprocess.run([sys.executable, script, "--hq-dir", hq_dir], capture_output=True, text=True, env=env)
    assert r2.returncode == 0 and "already sent" in r2.stdout, r2.stdout
    assert len(open(log_path).read().splitlines()) == len(reqs)
    st2 = os.path.join(td, "state2")
    hq2 = os.path.join(td, "hq2")
    os.makedirs(os.path.join(hq2, "hq"), exist_ok=True)
    open(os.path.join(hq2, "hq", "alert.py"), "w").write(
        "import json\nprint(json.dumps({'ping': False, 'reason': 'quiet_hours', 'channels': []}))\n"
    )
    r3 = subprocess.run([sys.executable, script, "--hq-dir", hq2], capture_output=True, text=True, env={**os.environ, "SKILLMAXX_STATE": st2})
    assert r3.returncode == 0 and "(0 sent" in r3.stdout and not os.path.exists(os.path.join(st2, "telegram-requests-sent.json")), r3.stdout
    shutil.rmtree(td)
    print("ok telegram requests: critical bypasses quiet hours, sends once per id, tracks state")



def test_blog_queue():
    qdir = os.path.join(ROOT, "growth/content/queue")
    qfiles = sorted(glob.glob(os.path.join(qdir, "*.njk")))
    assert len(qfiles) == 8, f"expected 8 queued blog drafts, got {len(qfiles)}"
    bq = load("growth/scripts/blog_queue.py", "bq")
    assert bq.find_queued(ROOT, "midweek-2026-48", "2026-11-24") is None, "must not publish before draft date"
    assert bq.find_queued(ROOT, "midweek-2026-48", "2026-11-25") is not None

    t = fixture()
    shutil.copytree(qdir, os.path.join(t, "growth/content/queue"))
    reps = json.load(open(os.path.join(t, "src/_data/reports.json")))
    weeks = json.load(open(os.path.join(t, "src/_data/weeks.json")))
    r48 = dict(reps[0], date="2026-11-25", prev_date="2026-11-18")
    json.dump([r48] + reps, open(os.path.join(t, "src/_data/reports.json"), "w"))
    shutil.copy(os.path.join(t, "testing/results/2026-11-18.json"), os.path.join(t, "testing/results/2026-11-25.json"))
    w48 = dict(weeks[0], key="2026-48", start="2026-11-23", end="2026-11-29", first="2026-11-25", last="2026-11-29",
               trend=[dict(weeks[0]["trend"][-1], date="2026-11-25"), dict(weeks[0]["trend"][-1], date="2026-11-29")])
    json.dump([w48] + weeks, open(os.path.join(t, "src/_data/weeks.json"), "w"))
    shutil.copy(os.path.join(t, "testing/results/2026-11-18.json"), os.path.join(t, "testing/results/2026-11-29.json"))

    mw = load("growth/scripts/midweek_blog_auto.py", "mwq"); mw.ROOT = t
    rc, out = quiet(mw.main, ["2026-11-25"])
    pmw = os.path.join(t, "src/blog/midweek-2026-48.njk")
    assert rc == 0 and os.path.exists(pmw), out
    txt_mw = open(pmw, encoding="utf-8").read()
    assert "[[SMX:" not in txt_mw and "Why npm MCP servers fail" in txt_mw
    assert json.loads(fm(txt_mw)["jsonld"])["@type"] == "BlogPosting"

    wb = load("growth/scripts/weekly_blog_auto.py", "wbq"); wb.ROOT = t
    rc, out = quiet(wb.main, ["2026-11-29"])
    pwb = os.path.join(t, "src/blog/week-2026-48.njk")
    assert rc == 0 and os.path.exists(pwb), out
    txt_wb = open(pwb, encoding="utf-8").read()
    assert "[[SMX:" not in txt_wb and "why Pi lags on plugins" in txt_wb
    assert json.loads(fm(txt_wb)["jsonld"])["@type"] == "BlogPosting"
    shutil.rmtree(t)
    print("ok blog queue: 8 drafts, date gate, token refresh, JSON-LD valid")



def test_newsletter_skeletons():
    sdir = os.path.join(ROOT, "growth/newsletter/skeletons")
    for n in (5, 6):
        doc = json.load(open(os.path.join(sdir, f"issue-{n}.json")))
        assert doc["issue"] == n and doc["spotlight"]["heading"] and doc["evergreen_section"]["heading"]
        assert len(doc["tell_us_prompts"]) == 3 and "section_prompts" in doc

    t = fixture()
    shutil.copytree(sdir, os.path.join(t, "growth/newsletter/skeletons"))
    nl = load("growth/scripts/newsletter_auto.py", "nls"); nl.ROOT = t
    # Issue 4 first (must not use issue 5 skeleton)
    assert nl.main(["2026-11-22"]) == 0
    weeks = json.load(open(os.path.join(t, "src/_data/weeks.json")))
    w48 = dict(weeks[0], key="2026-48", start="2026-11-23", end="2026-11-29", trend=[dict(weeks[0]["trend"][-1], date="2026-11-29")])
    w49 = dict(weeks[0], key="2026-49", start="2026-11-30", end="2026-12-06", trend=[dict(weeks[0]["trend"][-1], date="2026-12-06")])
    json.dump([w49, w48] + weeks, open(os.path.join(t, "src/_data/weeks.json"), "w"))
    shutil.copy(os.path.join(t, "testing/results/2026-11-18.json"), os.path.join(t, "testing/results/2026-11-29.json"))
    shutil.copy(os.path.join(t, "testing/results/2026-11-18.json"), os.path.join(t, "testing/results/2026-12-06.json"))

    rj = os.path.join(t, "radar.json")
    json.dump([{"title": "Fresh Sunday HN item", "url": "https://news.ycombinator.com/item?id=555", "points": 31, "comments": 4}], open(rj, "w"))

    rc5, out5 = quiet(nl.main, ["2026-11-29", "--radar-json", rj])
    p5 = os.path.join(t, "src/newsletter/issue-5.md")
    assert rc5 == 0 and os.path.exists(p5), out5
    t5 = open(p5, encoding="utf-8").read()
    assert "Spotlight: Cross-agent MCP compatibility" in t5
    assert "This week's receipt" in t5
    assert "Fresh Sunday HN item" in t5
    assert "BFCM-FEATURED-DEC" in t5
    assert not nl.problems(t5), nl.problems(t5)

    rc6, out6 = quiet(nl.main, ["2026-12-06", "--radar-json", rj])
    p6 = os.path.join(t, "src/newsletter/issue-6.md")
    assert rc6 == 0 and os.path.exists(p6), out6
    t6 = open(p6, encoding="utf-8").read()
    assert "Spotlight: Plugins vs. standalone skills vs. MCP servers" in t6
    assert "This week by format" in t6
    assert "Why missing API keys are not bugs" in t6
    assert "Fresh Sunday HN item" in t6
    assert not nl.problems(t6), nl.problems(t6)
    shutil.rmtree(t)
    print("ok newsletter skeletons: issues 5 and 6 render planned evergreen sections, live receipts, fresh radar, zero placeholders")

if __name__ == "__main__":
    test_newsletter(); test_midweek(); test_sunday_guard(); test_monday_check(); test_alert_wiring(); test_publish_script(); test_first_subscriber_alert(); test_telegram_requests(); test_blog_queue(); test_newsletter_skeletons()
    print("test_autopublish: all ok")
