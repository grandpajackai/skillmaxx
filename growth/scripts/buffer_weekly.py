#!/usr/bin/env python3
"""Weekly Buffer top-up without Grok: 3 templated posts per channel (Mon/Wed/Fri of next week) built only
from the latest weekly scorecard (src/_data/weeks.json). Slots (ET): X 9:30 AM, LinkedIn 12:00 PM, Bluesky 7:30 PM.
Default saves them as Buffer DRAFTS (Brandon taps "schedule" in Buffer: zero credits). Set
SKILLMAXX_BUFFER_MODE=schedule in the key file to queue them directly instead.
Key: ~/.skillmaxx-secrets/buffer.env (chmod 600) with BUFFER_API_KEY=... from https://publish.buffer.com/settings/api
The key is read from that file only, sent in a header, never printed. Without it the script prints the plan and exits 0.
Skips a post whose text is already scheduled/drafted (dedupe by text). Free plan: max 10 scheduled per channel.
Usage: python3 growth/scripts/buffer_weekly.py [--dry-run] [--week-of YYYY-MM-DD (the Monday)]"""
import json, os, sys, urllib.request
from datetime import date, datetime, timedelta, timezone
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SITE = "https://skillmaxx.gilventures.ai"
API = "https://api.buffer.com"
ORG = "6adfb3f8d2cea8f4b234c15b"
CH = {"x": ("6adfb5c92f1f5ed648deaa83", 9, 30, 280), "linkedin": ("6adfc4f12f1f5ed648df8e37", 12, 0, 1400),
      "bluesky": ("6adfbe402f1f5ed648def519", 19, 30, 300)}
KEYFILE = os.path.expanduser(os.environ.get("SKILLMAXX_BUFFER_ENV", "~/.skillmaxx-secrets/buffer.env"))

def env():
    e = {}
    if os.path.exists(KEYFILE):
        for line in open(KEYFILE):
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.strip().split("=", 1); e[k] = v.strip().strip('"').strip("'")
    return e

def et_offset(d):  # US Eastern: EDT 2nd Sun Mar .. 1st Sun Nov
    y = d.year
    mar = date(y, 3, 8) + timedelta((6 - date(y, 3, 8).weekday()) % 7)
    nov = date(y, 11, 1) + timedelta((6 - date(y, 11, 1).weekday()) % 7)
    return "-04:00" if mar <= d < nov else "-05:00"

def posts(w):
    t = w["trend"][-1]; p, n = t["pass"], t["tested"]; rate = round(100 * p / n, 1) if n else 0
    rk = w["ranking"]; top = rk[0] if rk else None
    wk = f"{SITE}/reports/week/{w['key']}/"
    a = (f"Last week we ran real installs of agent skills, plugins and MCP servers in 5 coding agents. "
         f"Latest night: {p:,} of {n:,} passed ({rate}%). {w.get('fixed_n', 0)} fixed, {w.get('broke_n', 0)} broke. Scorecard: {wk}")
    by = ", ".join(f"{r['name']} {r['rate']}%" for r in rk)
    b = (f"Install pass rate by agent last week: {by}. Each agent gets the add-ons it supports, so it's add-on readiness, "
         f"not an agent ranking. {SITE}/works-in/")
    c = (f"{w.get('flaky_n', 0)} agent add-ons passed some nights and failed others last week. One bad install isn't "
         f"proof it's broken. Check the night-by-night history before you give up on one: {SITE}/reports/")
    return [a, b, c]

def gql(key, q, v):
    req = urllib.request.Request(API, json.dumps({"query": q, "variables": v}).encode(),
                                 {"Content-Type": "application/json", "Authorization": "Bearer " + key})
    return json.load(urllib.request.urlopen(req, timeout=30))

LIST = """query($org: OrganizationId!, $ch: [ChannelId!]) { posts(first: 50, input: {organizationId: $org,
  filter: {channelIds: $ch, status: [scheduled, draft]}}) { edges { node { id text status } } } }"""
CREATE = """mutation($input: CreatePostInput!) { createPost(input: $input) {
  ... on PostActionSuccess { post { id dueAt } } ... on MutationError { message } } }"""

def main(argv):
    # Disabled: the Grok Buffer connector already schedules X, LinkedIn and Bluesky.
    # Running this would create duplicate drafts or posts. Quiet no-op, exit 0, no API, no alert.
    print("buffer_weekly: disabled (Grok Buffer connector schedules posts); no-op")
    return 0
    dry = "--dry-run" in argv
    weeks = sorted(json.load(open(os.path.join(ROOT, "src/_data/weeks.json"))), key=lambda x: x["end"], reverse=True)
    w = next((x for x in weeks if x.get("runs")), None)
    if not w: print("no week with runs"); return 0
    today = date.today()
    mon = date.fromisoformat(argv[argv.index("--week-of") + 1]) if "--week-of" in argv else today + timedelta(7 - today.weekday())
    texts = posts(w); e = env(); key = e.get("BUFFER_API_KEY"); mode = e.get("SKILLMAXX_BUFFER_MODE", "draft")
    if not key: print(f"no BUFFER_API_KEY in {KEYFILE}: plan only"); dry = True
    made = 0
    for name, (cid, hh, mm, lim) in CH.items():
        have = set()
        if not dry:
            r = gql(key, LIST, {"org": ORG, "ch": [cid]})
            have = {(ed["node"].get("text") or "").strip() for ed in (((r.get("data") or {}).get("posts") or {}).get("edges") or [])}
        for i, txt in enumerate(texts):
            d = mon + timedelta(2 * i)  # Mon, Wed, Fri
            due = f"{d.isoformat()}T{hh:02d}:{mm:02d}:00{et_offset(d)}"
            if len(txt) > lim: txt = txt[:lim - 1] + "…"
            if txt.strip() in have: print(f"{name} {due}: already in Buffer, skip"); continue
            if dry: print(f"[plan] {name} {due} ({mode}): {txt}"); continue
            inp = {"channelId": cid, "text": txt, "schedulingType": "automatic", "mode": "customScheduled", "dueAt": due,
                   "saveToDraft": mode != "schedule"}
            r = gql(key, CREATE, {"input": inp}); res = ((r.get("data") or {}).get("createPost") or {})
            if res.get("post"): made += 1; print(f"{name} {due}: {mode} ok")
            else: print(f"{name} {due}: FAILED {res.get('message') or r.get('errors')}")
    print(f"buffer_weekly: {made} created ({mode})"); return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
