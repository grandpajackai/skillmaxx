#!/usr/bin/env python3
"""Monday check: is last week's SkillMaxx Weekly issue live? Free, stdlib only, never prints secrets.

For DATE (a Monday, default today ET) the expected issue is the one dated in the previous Mon-Sun week
(growth/scripts/newsletter_auto.py publishes it on Sunday). It reads master's src/newsletter/ via git
(fetching origin/master first in --repo, read-only) and falls back to the working tree. Then it GETs
SITE/newsletter/issue-N/ and expects HTTP 200.

Exit 0: live (or not a Monday). Exit 3: missing; the one-line reason is printed on stdout for the caller,
which posts it with testing/nightly_alert.sh (kind newsletter_missing). This script never posts anything.
Called once each Monday from the hourly watchdog in testing/local_nightly.sh (from 07 ET).
Usage: check_newsletter_live.py [--date YYYY-MM-DD] [--repo DIR] [--site URL] [--any-day]"""
import argparse, os, re, subprocess, sys, urllib.request
from datetime import date, datetime, timedelta

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = "https://skillmaxx.gilventures.ai"


def today_et():
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("America/New_York")).date()
    except Exception:  # pragma: no cover
        return date.today()


def git(repo, *args):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, timeout=60)
    return r.stdout if r.returncode == 0 else None


def list_issues(repo, fetch=True):
    """{N: front-matter text} for src/newsletter/issue-N.md on origin/master (fallback: working tree)."""
    out = {}
    if fetch:
        git(repo, "fetch", "-q", "origin", "+refs/heads/master:refs/remotes/origin/master")
    names = git(repo, "ls-tree", "--name-only", "origin/master", "src/newsletter/")
    if names:
        for path in names.split():
            m = re.match(r"src/newsletter/issue-(\d+)\.md$", path)
            if m:
                out[int(m.group(1))] = (git(repo, "show", f"origin/master:{path}") or "")[:4000]
        if out:
            return out
    d = os.path.join(repo, "src/newsletter")
    for f in os.listdir(d) if os.path.isdir(d) else []:
        m = re.match(r"issue-(\d+)\.md$", f)
        if m:
            out[int(m.group(1))] = open(os.path.join(d, f), encoding="utf-8").read()[:4000]
    return out


def expected_issue(issues, day):
    """(N, week_key, mon, sun) for the issue dated in the Mon-Sun week before `day`; N is None if there is none."""
    sun = day - timedelta(days=day.isoweekday() % 7 or 7) if day.isoweekday() != 7 else day
    mon = sun - timedelta(days=6)
    key = f"{sun.isocalendar()[0]}-{sun.isocalendar()[1]:02d}"
    for n, txt in sorted(issues.items()):
        m = re.search(r'^issueDate:\s*"?(\d{4}-\d\d-\d\d)', txt, re.M)
        w = re.search(r'^week:\s*"?([0-9-]+)', txt, re.M)
        if (w and w.group(1) == key) or (m and mon.isoformat() <= m.group(1) <= sun.isoformat()):
            return n, key, mon, sun
    return None, key, mon, sun


def http_status(url, opener=urllib.request.urlopen):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "skillmaxx-newsletter-check/1.0"})
        with opener(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0


def check(day, issues, site=SITE, opener=urllib.request.urlopen):
    """(ok, message)."""
    n, key, mon, sun = expected_issue(issues, day)
    if n is None:
        return False, (f"No SkillMaxx Weekly issue was published for week {key} ({mon}..{sun}): no src/newsletter/issue-N.md "
                       f"dated in that week on master. The Sunday auto-publish (growth/scripts/newsletter_auto.py) did not run or skipped.")
    url = f"{site.rstrip('/')}/newsletter/issue-{n}/"
    st = http_status(url, opener)
    if st == 200:
        return True, f"issue #{n} live: {url}"
    return False, f"SkillMaxx Weekly issue #{n} (week {key}) is on master but {url} returned HTTP {st or 'no response'} (check the Pages deploy)."


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--date")
    ap.add_argument("--repo", default=ROOT)
    ap.add_argument("--site", default=os.environ.get("SKILLMAXX_SITE", SITE))
    ap.add_argument("--any-day", action="store_true", help="run even if DATE is not a Monday")
    ap.add_argument("--no-fetch", action="store_true")
    a = ap.parse_args(argv)
    day = date.fromisoformat(a.date) if a.date else today_et()
    if day.isoweekday() != 1 and not a.any_day:
        print(f"newsletter check: {day} is not a Monday; nothing to check")
        return 0
    ok, msg = check(day, list_issues(a.repo, fetch=not a.no_fetch), a.site)
    print(("newsletter check: " if ok else "") + msg)
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
