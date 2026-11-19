#!/usr/bin/env python3
"""Grok-free prep for the SkillMaxx judgment routines. No LLM, no secrets in output, never posts or sends.

Each subcommand does only the mechanical part of one Grok routine (fetch, list, count, format) and writes
<out>/<cmd>.md (for the routine to read) plus <cmd>.json. The Grok routine keeps the judgment step.

  xradar    X radar context: latest published numbers, X URLs already used (14 d), ready-made X search
            strings, HN stories (keyless Algolia). X itself has no free API: Grok's X tools still fetch posts.
  queue     Brandon's Mon/Wed/Fri queue base: numbers, last radar picks, open Bluesky promises,
            LinkedIn leads not yet queued, X-route sponsor rows, HN threads. Reddit is 403 (no fetch).
  bluesky   Bluesky community (public AppView, keyless): profile counts, unanswered replies to our posts,
            follow-backs, unfollow candidates (FOLLOWS.md rule), keyword search candidates, open promises.
  outreach  Daily sponsor outreach: follow-ups due, first-touch targets, approved queue files, facts.
            --zoho (box only): read-only Inbox/Spam/Sent scan for replies/duplicates per due domain via
            growth/scripts/zoho_mail.py list (never send/reply).
  pipeline  Weekly pipeline: counts by status, Contacted aging (7/14 d), top Targets, BFCM window flag.
  recap     Sunday recap stats + newsletter-draft.md (no-LLM draft of the next issue, src/newsletter format): week scorecard, nightly trend, pipeline counts, emails sent, blog/newsletter
            status, merged PRs (gh, if logged in), Bluesky follower count.

Usage: prep.py CMD [--date YYYY-MM-DD] [--out DIR] [--offline] [--zoho]
Stdlib only. Network: skillmaxx site, public Bluesky AppView, hn.algolia.com, optional gh. All keyless.
"""
import argparse, csv, glob, json, os, re, socket, subprocess, sys, urllib.parse, urllib.request
from datetime import date, datetime, timedelta, timezone

try:
    from zoneinfo import ZoneInfo
    ET = ZoneInfo("America/New_York")
except Exception:  # pragma: no cover
    ET = None

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SITE = "https://skillmaxx.gilventures.ai"
BSKY = "https://api.bsky.app/xrpc"          # public.api.bsky.app 403s searchPosts; api.bsky.app is keyless
OUR_BSKY = "skillmaxx.bsky.social"
AG = {"claude_code": "Claude Code", "codex": "Codex", "grok_build": "Grok Build", "cursor": "Cursor", "pi": "Pi"}
KEYWORDS = ["mcp server", "claude code skills", "claude code plugin", "agent skills", "codex plugin",
            "cursor mcp", "grok build", "pi coding agent", "skill.md"]
UA = "skillmaxx-prep/1.0 (+https://skillmaxx.gilventures.ai)"
OFFLINE = False
# Routines also write untracked notes into the box's working copy; read both (deduped by file name).
EXTRA_ROOTS = [r for r in ("/workspace/skillmaxx",) if os.path.isdir(r) and os.path.abspath(r) != ROOT]
TECH = re.compile(r"\b(mcp|claude|codex|cursor|grok|llm|coding agents?|ai agents?|skill\.md|skills?|plugins?|github|npx|anthropic|openai)\b", re.I)


def now_et():
    return datetime.now(ET) if ET else datetime.now()


def rd_json(rel, default=None):
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def rd_text(rel):
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def get(url, timeout=20):
    if OFFLINE:
        raise OSError("offline")
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def get_json(url):
    st, b = get(url)
    return json.loads(b)


def pipeline_rows():
    try:
        with open(os.path.join(ROOT, "growth/sponsors/PIPELINE.csv"), encoding="utf-8") as f:
            return list(csv.DictReader(f))
    except OSError:
        return []


DATE_RE = re.compile(r"20\d\d-\d\d-\d\d")


def dates_in(s):
    out = []
    for m in DATE_RE.findall(s or ""):
        try:
            out.append(date.fromisoformat(m))
        except ValueError:
            pass
    return out


def domain_of(row):
    d = (row.get("contact_detail") or "").strip()
    if "@" in d:
        return d.split("@", 1)[1].lower().strip(" >")
    w = (row.get("website") or "").lower()
    w = re.sub(r"^https?://", "", w).split("/")[0]
    return w[4:] if w.startswith("www.") else w


def multi_glob(rel_pattern):
    seen = {}
    for base in [ROOT] + EXTRA_ROOTS:
        for p in sorted(glob.glob(os.path.join(base, rel_pattern))):
            seen.setdefault(os.path.basename(p), p)
    return [seen[k] for k in sorted(seen)]


_SENT = None


def sent_index():
    """email -> [(date, kind)] from growth/outreach/sent/*-email-results.json (repo + box working copy)."""
    global _SENT
    if _SENT is None:
        _SENT = {}
        for p in multi_glob("growth/outreach/sent/*results.json"):
            try:
                j = json.load(open(p, encoding="utf-8"))
            except (OSError, ValueError):
                continue
            for x in (j if isinstance(j, list) else j.get("results", [])):
                if not isinstance(x, dict) or str(x.get("http", 200)) != "200":
                    continue
                ds = dates_in(str(x.get("sent_at") or "")) or dates_in(os.path.basename(p))
                to = (x.get("to") or "").lower().strip()
                if to and ds:
                    _SENT.setdefault(to, []).append((ds[0], x.get("kind") or ""))
    return _SENT


def sent_for(row):
    return sorted(sent_index().get((row.get("contact_detail") or "").lower().strip(), []))


def last_touch(row):
    ds = dates_in(row.get("date_contacted", "")) + dates_in(row.get("outreach_sent", "")) + [d for d, _ in sent_for(row)]
    return max(ds) if ds else None


def followups_sent(row):
    t = (row.get("outreach_sent") or "").lower()
    n = set(re.findall(r"follow-?up\s*#?\s*(\d)", t))
    n |= {k[2:] for _, k in sent_for(row) if k.startswith("fu")}
    n = len(n)
    if "final" in t and "sent" in t and n == 0:
        n = 1
    return n


def next_due(row):
    """Computed hint only: the date in next_follow_up matching how many follow-ups were already sent."""
    nf = row.get("next_follow_up") or ""
    if nf.lower().startswith("none"):
        return None, nf
    ds = dates_in(nf)
    if not ds:
        return None, nf
    sent = followups_sent(row)
    # If dates are all in the past and some were sent, pick the first one not yet consumed.
    idx = min(sent, len(ds) - 1) if len(ds) > 1 else 0
    if sent >= len(ds) and "final" in nf.lower():
        return None, nf + " [final already sent per logs]"
    lt = last_touch(row)
    if lt and lt >= ds[idx]:
        return None, nf + f" [touched {lt} on/after due]"
    return ds[idx], nf


# ---------------------------------------------------------------- shared facts
def facts(d):
    reps = rd_json("src/_data/reports.json", []) or []
    reps = sorted([r for r in reps if r.get("date")], key=lambda r: r["date"])
    out = {"latest_report": None}
    if not reps:
        return out
    r = reps[-1]
    by = {AG.get(k, k): f"{v.get('pass', 0)}/{v.get('total', 0)}" for k, v in (r.get("by") or {}).items()}
    out["latest_report"] = {
        "date": r["date"], "pass": r.get("pass"), "total": r.get("total"), "tested": r.get("tested"),
        "addons": r.get("addons"), "needs_key": r.get("needs_key"), "by_agent": by,
        "url": f"{SITE}/reports/{r['date']}/", "versions": r.get("versions"), "by_raw": r.get("by") or {},
    }
    try:
        st, body = get(out["latest_report"]["url"])
        out["latest_report"]["live"] = st == 200 and b"No report this night" not in body
    except Exception as e:
        out["latest_report"]["live"] = f"unchecked ({type(e).__name__})"
    if len(reps) > 1:
        p = reps[-2]
        out["previous_report"] = {"date": p["date"], "pass": p.get("pass"), "total": p.get("total")}
    out["report_age_days"] = (d - date.fromisoformat(r["date"])).days
    return out


def facts_md(f):
    r = f.get("latest_report")
    if not r:
        return ["- No reports in src/_data/reports.json."]
    pv = f.get("previous_report")
    lines = [f"- Latest published report: **{r['date']}** — {r['pass']:,}/{r['total']:,} installs passed, "
             f"{r.get('addons') or '?'} add-ons, {r.get('needs_key')} need a key. Live check: {r.get('live')}. {r['url']}",
             "- Per agent: " + ", ".join(f"{k} {v}" for k, v in r["by_agent"].items())]
    if pv:
        lines.append(f"- Previous night: {pv['date']} {pv['pass']:,}/{pv['total']:,}")
    if f.get("report_age_days", 0) > 1:
        lines.append(f"- ⚠ Latest report is {f['report_age_days']} days old; check before quoting 'last night'.")
    return lines


def hn(query, since_days=2, n=8):
    ts = int((datetime.now(timezone.utc) - timedelta(days=since_days)).timestamp())
    q = urllib.parse.urlencode({"query": query, "tags": "story", "numericFilters": f"created_at_i>{ts}",
                                "hitsPerPage": n})
    try:
        j = get_json(f"https://hn.algolia.com/api/v1/search?{q}")
    except Exception as e:
        return {"error": type(e).__name__}
    return [{"title": h.get("title"), "points": h.get("points"), "comments": h.get("num_comments"),
             "url": h.get("url"), "hn": f"https://news.ycombinator.com/item?id={h.get('objectID')}",
             "created": h.get("created_at")} for h in j.get("hits", [])]


def hn_block(kw_list, since_days=2):
    seen, items = set(), []
    for k in kw_list:
        res = hn(k, since_days)
        if isinstance(res, dict):
            return [], res["error"]
        for h in res:
            if h["hn"] in seen:
                continue
            seen.add(h["hn"]); h["keyword"] = k; items.append(h)
    items.sort(key=lambda h: -(h.get("points") or 0))
    return items[:15], None


def radar_files(days, d):
    out = []
    for p in multi_glob("growth/x-radar/*.md"):
        m = DATE_RE.search(os.path.basename(p))
        if m and 0 <= (d - date.fromisoformat(m.group(0))).days <= days:
            out.append(p)
    return out


XURL = re.compile(r"https://(?:x|twitter)\.com/([A-Za-z0-9_]+)/status/(\d+)")


def used_x_urls(d, days=14):
    used = {}
    for p in radar_files(days, d):
        for m in XURL.finditer(open(p, encoding="utf-8").read()):
            used.setdefault(f"https://x.com/{m.group(1)}/status/{m.group(2)}", os.path.basename(p))
    return used


# ---------------------------------------------------------------- xradar
def cmd_xradar(d, a):
    f = facts(d)
    used = used_x_urls(d)
    handles = {}
    for u in used:
        h = u.split("/")[3]
        handles[h] = handles.get(h, 0) + 1
    since = (d - timedelta(days=1)).isoformat()
    searches = [f'"{k}" min_faves:20 -is:retweet lang:en since:{since}' for k in KEYWORDS[:7]]
    searches += [f"(skills OR plugins OR mcp) (\"claude code\" OR codex OR cursor) min_replies:5 since:{since}"]
    hn_items, hn_err = hn_block(["mcp", "claude code", "agent skills", "codex"], 2)
    data = {"facts": f, "used_x_urls": used, "frequent_handles": sorted(handles.items(), key=lambda x: -x[1])[:15],
            "x_search_strings": searches, "hn": hn_items, "hn_error": hn_err}
    md = [f"# X radar prep — {d} (generated {stamp()})", "",
          "Mechanical prep only (no LLM). X has no free API, so finding and reading posts stays with Grok's X tools.", "",
          "## Numbers to quote (only these)"] + facts_md(f) + ["", "## Ready-made X searches (paste into the X search tool)"]
    md += [f"- `{s}`" for s in searches]
    md += ["", f"## Already used in the last 14 days ({len(used)} posts) — skip these"]
    md += [f"- {u} ({src})" for u, src in list(used.items())[:60]]
    md += ["", "## Accounts we engaged most (14 d) — vary the picks"]
    md += [f"- @{h} ×{n}" for h, n in data["frequent_handles"]]
    md += ["", "## Hacker News, last 48 h (keyless Algolia)"]
    md += [f"- error: {hn_err}"] if hn_err else [f"- {h['title']} ({h['points']} pts, {h['comments']} comments) {h['hn']}" for h in hn_items] or ["- none"]
    return data, md


# ---------------------------------------------------------------- queue
def latest_radar_picks(d):
    files = [p for p in radar_files(2, d) if "queue" not in p]
    if not files:
        return None, []
    p = files[-1]
    txt = open(p, encoding="utf-8").read()
    picks = []
    lines = txt.splitlines()
    seen = set()
    for i, line in enumerate(lines):
        for m in XURL.finditer(line):
            u = f"https://x.com/{m.group(1)}/status/{m.group(2)}"
            if u in seen:
                continue
            seen.add(u)
            ctx = line.replace(m.group(0), "").strip(" -*")
            j = i - 1
            while not ctx and j >= 0:
                c = lines[j].strip()
                if c and not c.startswith("```") and not c.startswith("#"):
                    ctx = c
                j -= 1
            picks.append({"url": u, "context": ctx[:200]})
    return os.path.basename(p), picks


def open_promises():
    txt = rd_text("growth/bluesky/PENDING-REPLIES.md")
    return [l.lstrip("# ").strip() for l in txt.splitlines() if l.startswith("## ") and "OPEN" in l]


def cmd_queue(d, a):
    f = facts(d)
    rfile, picks = latest_radar_picks(d)
    queued_txt = "\n".join(open(p, encoding="utf-8").read() for p in glob.glob(os.path.join(ROOT, "growth/x-radar/*queue*.md")))
    leads = []
    try:
        with open(os.path.join(ROOT, "growth/sponsors/SALES-NAV-LEADS.csv"), encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                if r.get("date_requested") or r.get("date_accepted"):
                    continue
                name = (r.get("lead_name") or "").strip()
                if name and name in queued_txt:
                    continue
                leads.append({k: r.get(k) for k in ("company", "lead_name", "title", "linkedin_url", "status", "smart_question_angle")})
    except OSError:
        pass
    accepted = []
    try:
        with open(os.path.join(ROOT, "growth/sponsors/SALES-NAV-LEADS.csv"), encoding="utf-8") as fh:
            accepted = [{"company": r["company"], "lead_name": r["lead_name"], "date_accepted": r["date_accepted"]}
                        for r in csv.DictReader(fh) if r.get("date_accepted") and not r.get("after_accept_sent")]
    except OSError:
        pass
    xrows = [{"company": r["company"], "status": r["status"], "next_follow_up": r["next_follow_up"],
              "contact_detail": r["contact_detail"]} for r in pipeline_rows()
             if (r.get("contact_route") == "x" or "X DM" in (r.get("next_follow_up") or "")) and r.get("status") not in ("Lost", "Bounced")]
    hn_items, hn_err = hn_block(["mcp server", "claude code", "agent skills"], 3)
    data = {"facts": f, "radar_file": rfile, "radar_picks": picks, "open_bluesky_promises": open_promises(),
            "linkedin_leads_not_queued": leads, "linkedin_accepted_need_followup": accepted,
            "x_route_sponsor_rows": xrows, "hn": hn_items, "hn_error": hn_err,
            "reddit": "Reddit .json/.rss return 403 from the box and the Mac: no fetch; use search links only."}
    md = [f"# Brandon's queue prep — {d} (generated {stamp()})", "", "Mechanical prep only. Nothing here was posted or sent.", "",
          "## Numbers to quote (only these)"] + facts_md(f)
    md += ["", f"## Latest X radar picks ({rfile or 'no radar file in the last 2 days'}) — re-read each thread before queuing"]
    md += [f"- {p['url']} — {p['context']}" for p in picks] or ["- none"]
    md += ["", "## Open Bluesky promises (growth/bluesky/PENDING-REPLIES.md)"] + ([f"- {x}" for x in data["open_bluesky_promises"]] or ["- none"])
    md += ["", "## LinkedIn: accepted, after-accept note not sent"] + ([f"- {x['lead_name']} ({x['company']}), accepted {x['date_accepted']}" for x in accepted] or ["- none"])
    md += ["", f"## LinkedIn leads in SALES-NAV-LEADS.csv not yet requested or queued ({len(leads)})"]
    md += [f"- {x['lead_name']}, {x['title']} @ {x['company']} {x['linkedin_url'] or ''}" for x in leads[:10]] or ["- none (find new ones; §0 verification stays with Grok)"]
    md += ["", "## Sponsor rows routed to X (DM/reply)"] + ([f"- {x['company']} [{x['status']}] {x['contact_detail']} — {x['next_follow_up']}" for x in xrows] or ["- none"])
    md += ["", "## Reddit", "- " + data["reddit"], "", "## Hacker News, last 72 h"]
    md += [f"- error: {hn_err}"] if hn_err else [f"- {h['title']} ({h['points']} pts, {h['comments']} comments) {h['hn']}" for h in hn_items] or ["- none"]
    return data, md


# ---------------------------------------------------------------- bluesky
def bsky(method, **params):
    return get_json(f"{BSKY}/{method}?{urllib.parse.urlencode(params, doseq=True)}")


def bsky_all(method, key, actor, cap=1000):
    out, cur = [], None
    while len(out) < cap:
        p = {"actor": actor, "limit": 100}
        if cur:
            p["cursor"] = cur
        j = bsky(method, **p)
        out += j.get(key, [])
        cur = j.get("cursor")
        if not cur:
            break
    return out


def post_url(uri, handle):
    return f"https://bsky.app/profile/{handle}/post/{uri.rsplit('/', 1)[-1]}"


def cmd_bluesky(d, a):
    data = {"errors": []}
    md = [f"# Bluesky community prep — {d} (generated {stamp()})", "",
          "Public AppView API, keyless, read-only. Nothing was liked, followed, unfollowed or posted.", ""]
    try:
        prof = bsky("app.bsky.actor.getProfile", actor=OUR_BSKY)
        data["profile"] = {k: prof.get(k) for k in ("followersCount", "followsCount", "postsCount")}
        followers = {x["handle"] for x in bsky_all("app.bsky.graph.getFollowers", "followers", OUR_BSKY)}
        follows = {x["handle"] for x in bsky_all("app.bsky.graph.getFollows", "follows", OUR_BSKY)}
        our_did = prof.get("did")
    except Exception as e:
        data["errors"].append(f"profile/graph: {type(e).__name__}: {e}")
        followers, follows, our_did = set(), set(), None
    md += ["## Account"]
    md += [f"- Followers {data['profile']['followersCount']} · following {data['profile']['followsCount']} · posts {data['profile']['postsCount']}"] if data.get("profile") else ["- unavailable"]
    data["follow_backs"] = sorted(followers - follows)
    md += ["", "## Follow-back candidates (they follow us, we don't follow them)"] + ([f"- @{h}" for h in data["follow_backs"]] or ["- none"])
    # FOLLOWS.md 7-day rule
    cands = []
    for line in rd_text("growth/bluesky/FOLLOWS.md").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4 or not DATE_RE.match(cells[0]):
            continue
        h = cells[1].lstrip("@")
        fb = cells[3].lower()
        if "unfollowed" in fb or "kept" in fb or fb.startswith("yes"):
            continue
        age = (d - date.fromisoformat(cells[0][:10])).days
        if age > 7 and h in follows and h not in followers:
            cands.append({"handle": h, "followed": cells[0], "age_days": age, "note": cells[3]})
    data["unfollow_candidates"] = cands
    md += ["", "## Unfollow candidates (FOLLOWS.md rule: followed >7 days ago, still not following back, not 'kept')"]
    md += [f"- @{c['handle']} (followed {c['followed']}, {c['age_days']} d; log says: {c['note']})" for c in cands] or ["- none"]
    # Replies to our recent posts that we have not answered
    unanswered = []
    try:
        feed = bsky("app.bsky.feed.getAuthorFeed", actor=OUR_BSKY, limit=30, filter="posts_no_replies").get("feed", [])
        for it in feed:
            p = it.get("post", {})
            if (p.get("replyCount") or 0) == 0:
                continue
            th = bsky("app.bsky.feed.getPostThread", uri=p["uri"], depth=2).get("thread", {})
            for rep in th.get("replies", []) or []:
                rp = rep.get("post", {})
                if not rp or rp.get("author", {}).get("did") == our_did:
                    continue
                ours = any(r2.get("post", {}).get("author", {}).get("did") == our_did for r2 in rep.get("replies", []) or [])
                if not ours:
                    unanswered.append({"from": rp["author"]["handle"], "text": rp.get("record", {}).get("text", "")[:280],
                                       "url": post_url(rp["uri"], rp["author"]["handle"]), "on": post_url(p["uri"], OUR_BSKY),
                                       "at": rp.get("indexedAt")})
    except Exception as e:
        data["errors"].append(f"feed/thread: {type(e).__name__}: {e}")
    data["unanswered_replies"] = unanswered
    md += ["", "## Replies to our posts with no reply from us (last 30 posts)"]
    md += [f"- @{u['from']} ({u['at'][:10] if u.get('at') else '?'}): “{u['text']}” {u['url']} (on {u['on']})" for u in unanswered] or ["- none"]
    # Keyword search candidates
    since = (datetime.now(timezone.utc) - timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
    seen, cand = set(), []
    for k in KEYWORDS:
        try:
            j = bsky("app.bsky.feed.searchPosts", q=k, limit=25, sort="top", since=since, lang="en")
        except Exception as e:
            data["errors"].append(f"search {k}: {type(e).__name__}")
            continue
        for p in j.get("posts", []):
            h = p.get("author", {}).get("handle", "")
            if p["uri"] in seen or h == OUR_BSKY or not TECH.search(p.get("record", {}).get("text", "")):
                continue
            seen.add(p["uri"])
            cand.append({"keyword": k, "handle": h, "followers_us": h in followers, "we_follow": h in follows,
                         "likes": p.get("likeCount", 0), "replies": p.get("replyCount", 0),
                         "text": p.get("record", {}).get("text", "")[:280], "url": post_url(p["uri"], h),
                         "at": p.get("indexedAt")})
    cand.sort(key=lambda c: -(c["likes"] + 2 * c["replies"]))
    data["search_candidates"] = cand[:25]
    md += ["", "## Keyword search candidates, last 3 days (top 25 by likes + 2×replies)"]
    md += [f"- [{c['keyword']}] @{c['handle']} ({c['likes']}♥ {c['replies']}↩{', follows us' if c['followers_us'] else ''}): “{c['text']}” {c['url']}" for c in data["search_candidates"]] or ["- none"]
    data["open_promises"] = open_promises()
    md += ["", "## Open promises (PENDING-REPLIES.md)"] + ([f"- {x}" for x in data["open_promises"]] or ["- none"])
    md += ["", "## Numbers to quote (only these)"] + facts_md(facts(d))
    if data["errors"]:
        md += ["", "## Fetch errors"] + [f"- {e}" for e in data["errors"]]
    return data, md


# ---------------------------------------------------------------- outreach
def zoho_index():
    """Read-only. Returns list of (folder, from, to, subject, time) for Inbox, Spam, Sent."""
    sys.path.insert(0, os.path.join(ROOT, "growth", "scripts"))
    import zoho_mail  # noqa: E402  (reads creds itself; never prints them)
    idx = []
    for fn in ("Inbox", "Spam", "Sent"):
        for m in zoho_mail.list_folder(fn, 1000):
            t = int(m.get("receivedTime") or m.get("sentDateInGMT") or 0) / 1000
            idx.append({"folder": fn, "from": (m.get("fromAddress") or "").lower(),
                        "to": urllib.parse.unquote(m.get("toAddress") or "").lower(), "subject": m.get("subject") or "",
                        "time": datetime.fromtimestamp(t, ET).strftime("%Y-%m-%d %H:%M") if t else "",
                        "messageId": m.get("messageId"), "folderId": m.get("folderId")})
    return idx


def mail_for(idx, dom):
    if not dom:
        return [], []
    replies = [m for m in idx if m["folder"] != "Sent" and dom in m["from"]]
    sent = [m for m in idx if m["folder"] == "Sent" and dom in m["to"]]
    return replies, sent


def approved_queues():
    out = []
    for base in (ROOT, "/workspace/skillmaxx"):
        for p in sorted(glob.glob(os.path.join(base, "growth/outreach/queue-*")))[-2:]:
            out.append({"dir": p, "files": sorted(os.listdir(p))[:40] if os.path.isdir(p) else []})
    return out


def cmd_outreach(d, a):
    rows = pipeline_rows()
    idx, zerr = None, None
    if a.zoho:
        try:
            idx = zoho_index()
        except SystemExit as e:
            zerr = str(e)
        except Exception as e:
            zerr = f"{type(e).__name__}: {e}"
    due, targets = [], []
    for r in rows:
        st = r.get("status", "")
        if st.startswith("Contacted") and r.get("contact_route") == "email":
            nd, raw = next_due(r)
            if nd and nd <= d:
                item = {"company": r["company"], "to": r["contact_detail"], "status": st, "next_follow_up": raw,
                        "computed_due": nd.isoformat(), "followups_sent": followups_sent(r),
                        "last_touch": (last_touch(r) or "").__str__(), "domain": domain_of(r)}
                if idx is not None:
                    rep, sent = mail_for(idx, item["domain"])
                    item["replies"] = [f"{m['time']} {m['folder']} from {m['from']}: {m['subject']}" for m in rep]
                    item["sent_count"] = len(sent)
                    item["last_sent"] = max((m["time"] for m in sent), default="")
                    item["last_sent_message"] = next((f"f={m['folderId']} m={m['messageId']}" for m in sorted(sent, key=lambda m: m["time"])[-1:]), "")
                    item["flag"] = "REPLY FOUND — skip, tell Brandon" if rep else (
                        "Zoho Sent shows a send on/after the due date — likely already done" if item["last_sent"] and item["last_sent"][:10] >= item["computed_due"] else 
                        "sent within 5 days — check for duplicate" if item["last_sent"] and item["last_sent"][:10] >= (d - timedelta(days=5)).isoformat() else "")
                due.append(item)
        elif st == "Target" and r.get("contact_route") == "email" and "@" in (r.get("contact_detail") or ""):
            t = {"company": r["company"], "to": r["contact_detail"], "notes": (r.get("notes") or "")[:160], "domain": domain_of(r)}
            if idx is not None:
                rep, sent = mail_for(idx, t["domain"])
                t["already_mailed"] = len(sent) > 0 or len(rep) > 0
            targets.append(t)
    sent_today = multi_glob(f"growth/outreach/sent/{d}-*.json")
    data = {"facts": facts(d), "due_followups": due, "first_touch_targets": targets[:15], "approved_queues": approved_queues(),
            "zoho_checked": idx is not None, "zoho_error": zerr, "sent_logs_today": [os.path.basename(p) for p in sent_today],
            "weekday": d.isoweekday() <= 5}
    md = [f"# Sponsor outreach prep — {d} (generated {stamp()})", "",
          "Mechanical prep only. Nothing was sent. Zoho was only read (list Inbox/Spam/Sent)." if idx is not None else
          f"Mechanical prep only. Nothing was sent. Zoho NOT checked ({zerr or 'run with --zoho on the box'}): do the per-recipient reply/duplicate checks yourself.",
          "", "## Facts to re-check drafts against"] + facts_md(data["facts"])
    md += ["", f"## Email follow-ups due by {d} ({len(due)}) — computed from PIPELINE.csv; verify sequence position"]
    for i in due:
        z = ""
        if idx is not None:
            z = f" · Zoho: {i['sent_count']} sent, last {i['last_sent'] or '—'} {i['last_sent_message']}"
            if i["replies"]:
                z += " · replies: " + " | ".join(i["replies"][:3])
        md.append(f"- **{i['company']}** <{i['to']}> [{i['status']}] due {i['computed_due']} (field: {i['next_follow_up']}; "
                  f"follow-ups sent ≈{i['followups_sent']}, last touch {i['last_touch']}){z}{' · ⚠ ' + i['flag'] if i.get('flag') else ''}")
    if not due:
        md.append("- none")
    md += ["", f"## First-touch email targets (status Target, top {len(data['first_touch_targets'])})"]
    md += [f"- {t['company']} <{t['to']}>{' · ⚠ already in Zoho' if t.get('already_mailed') else ''} — {t['notes']}" for t in data["first_touch_targets"]] or ["- none"]
    md += ["", "## Approved queue folders (latest)"] + [f"- {q['dir']}: {', '.join(q['files'][:12])}" for q in data["approved_queues"]] or ["- none"]
    md += ["", f"## Sent logs already written today: {', '.join(data['sent_logs_today']) or 'none'}"]
    return data, md


# ---------------------------------------------------------------- pipeline
def counts(rows):
    c = {}
    for r in rows:
        c[r.get("status") or "?"] = c.get(r.get("status") or "?", 0) + 1
    return dict(sorted(c.items(), key=lambda x: -x[1]))


def cmd_pipeline(d, a):
    rows = pipeline_rows()
    week0 = d - timedelta(days=d.isoweekday() - 1)
    aging7, aging14, contacted_week = [], [], 0
    for r in rows:
        if not r.get("status", "").startswith("Contacted"):
            continue
        lt = last_touch(r)
        if lt and lt >= d - timedelta(days=7):
            contacted_week += 1 if dates_in(r.get("date_contacted", "")) and min(dates_in(r["date_contacted"])) >= d - timedelta(days=7) else 0
        if not lt:
            continue
        age = (d - lt).days
        item = {"company": r["company"], "route": r["contact_route"], "last_touch": lt.isoformat(), "age": age,
                "followups_sent": followups_sent(r), "next_follow_up": r.get("next_follow_up")}
        (aging14 if age >= 14 else aging7 if age >= 7 else []).append(item)
    booked_txt = rd_text("growth/sponsors/PIPELINE.md")
    m = re.search(r"Founding sponsors booked:\s*\**(\d+)\s*/\s*10", booked_txt)
    targets = [{"company": r["company"], "route": r["contact_route"], "contact": r["contact_detail"]} for r in rows if r.get("status") == "Target"][:8]
    bfcm = date(d.year, 11, 24) <= d <= date(d.year, 12, 1)
    data = {"counts": counts(rows), "total": len(rows), "founding_booked": int(m.group(1)) if m else None,
            "new_contacted_last_7d": contacted_week, "aging_7_13": aging7, "aging_14_plus": aging14,
            "top_targets": targets, "bfcm_window": bfcm, "facts": facts(d)}
    md = [f"# Sponsor pipeline prep — week of {week0} (generated {stamp()})", "",
          "Counts from growth/sponsors/PIPELINE.csv. Stripe, Beehiiv and the decision to draft or ask stay with Grok.", "",
          "## Counts by status"] + [f"- {k}: {v}" for k, v in data["counts"].items()] + [f"- Total rows: {len(rows)}",
          f"- Founding sponsors booked (PIPELINE.md): {data['founding_booked']}/10",
          f"- First contacted in the last 7 days: {contacted_week}", f"- BFCM window (Nov 24–Dec 1): {'YES' if bfcm else 'no'}"]
    md += ["", f"## Contacted, last touch 7–13 days ago ({len(aging7)}) — Follow-up 1 candidates"]
    md += [f"- {i['company']} ({i['route']}) last {i['last_touch']} ({i['age']} d), follow-ups ≈{i['followups_sent']}; field: {i['next_follow_up']}" for i in aging7] or ["- none"]
    md += ["", f"## Contacted, last touch ≥14 days ago ({len(aging14)}) — Follow-up 2 / Lost-Nurture candidates"]
    md += [f"- {i['company']} ({i['route']}) last {i['last_touch']} ({i['age']} d), follow-ups ≈{i['followups_sent']}; field: {i['next_follow_up']}" for i in aging14] or ["- none"]
    md += ["", "## Top Target rows"] + [f"- {t['company']} ({t['route']}: {t['contact']})" for t in targets] or ["- none"]
    md += ["", "## Numbers for any batch draft"] + facts_md(data["facts"])
    return data, md


# ---------------------------------------------------------------- recap
def cmd_recap(d, a):
    weeks = rd_json("src/_data/weeks.json", []) or []
    wk = next((w for w in weeks if w.get("start", "") <= d.isoformat() <= w.get("end", "")), weeks[0] if weeks else {})
    start = d - timedelta(days=6)
    sent = 0
    for lst in sent_index().values():
        sent += sum(1 for dd, _ in lst if start <= dd <= d)
    blog = sorted(glob.glob(os.path.join(ROOT, "src/blog/week-*"))) + sorted(glob.glob(os.path.join(ROOT, "src/blog/*.njk")))
    news = sorted(glob.glob(os.path.join(ROOT, "src/newsletter/issue-*.md")))
    prs = []
    try:
        out = subprocess.run(["gh", "pr", "list", "-R", "grandpajackai/skillmaxx", "--state", "merged", "--search",
                              f"merged:>={start.isoformat()}", "--json", "number,title,mergedAt", "--limit", "60"],
                             capture_output=True, text=True, timeout=60)
        if out.returncode == 0:
            prs = json.loads(out.stdout or "[]")
    except Exception:
        prs = None
    bs = None
    try:
        p = bsky("app.bsky.actor.getProfile", actor=OUR_BSKY)
        bs = {"followers": p.get("followersCount"), "following": p.get("followsCount"), "posts": p.get("postsCount")}
    except Exception:
        pass
    radar = [os.path.basename(p) for p in radar_files(6, d)]
    data = {"week": wk.get("key"), "trend": wk.get("trend"), "ranking": wk.get("ranking"),
            "fixed": wk.get("fixed"), "broke": wk.get("broke"), "standout": wk.get("standout"),
            "pipeline_counts": counts(pipeline_rows()), "emails_sent_7d": sent, "merged_prs_7d": prs,
            "bluesky": bs, "radar_files_7d": radar, "blog_files": [os.path.basename(b) for b in blog][-5:],
            "newsletter_issues": [os.path.basename(n) for n in news], "facts": facts(d)}
    os.makedirs(a.out, exist_ok=True)
    key = wk.get("key") or f"{d.isocalendar()[0]}-{d.isocalendar()[1]:02d}"
    published = published_issue_for_week(d)
    if published:
        issue_no = published[0]
        data["newsletter_draft"] = {"issue": issue_no, "published": os.path.relpath(published[1], ROOT), "path": None}
        nl_line = (f"Newsletter: issue #{issue_no} is already published for this week ({os.path.relpath(published[1], ROOT)} -> "
                   f"{SITE}/newsletter/issue-{issue_no}/, auto from the Mac, no LLM). No draft written. Optional polish = edit that file; the email send stays held.")
    else:
        issue_no, draft = newsletter_draft(d, wk, data["facts"])
        with open(os.path.join(a.out, "newsletter-draft.md"), "w", encoding="utf-8") as fh:
            fh.write(draft)
        data["newsletter_draft"] = {"issue": issue_no, "path": os.path.join(a.out, "newsletter-draft.md")}
        nl_line = (f"Newsletter: issue #{issue_no} is NOT published yet (the Mac Sunday auto-publish has not run or skipped). "
                   f"Fallback no-LLM draft written to {os.path.join(a.out, 'newsletter-draft.md')} (unsent, unpublished).")
    post = os.path.join(ROOT, "src/blog", f"week-{key}.njk")
    data["sunday_post"] = {"key": key, "exists": os.path.exists(post), "url": f"{SITE}/blog/week-{key}/"}
    blog_line = (f"Sunday blog post: {SITE}/blog/week-{key}/ " + ("exists (Mac weekly_blog_auto.py)." if data["sunday_post"]["exists"] else "is NOT in the repo yet.")
                 + " It is the only Sunday post: check and link it, never write a second Sunday post.")
    md = [f"# Sunday recap prep — week ending {d} (generated {stamp()})", "",
          nl_line, "", blog_line, "",
          "Stats only. Wins/misses wording, the dashboard edit, optional newsletter polish and anything sent stay with Grok.", "",
          f"## Nightly runs, week {wk.get('key')} ({wk.get('start')}–{wk.get('end')})"]
    md += [f"- {t['date']}: {t['pass']:,}/{t['total']:,} passed ({t.get('rate')}% of tested)" for t in (wk.get("trend") or [])] or ["- no runs"]
    md += ["", "## Agent ranking (summed over the week's runs)"] + [f"- {x['name']}: {x['pass']}/{x['tested']} ({x['rate']}%), flaky {x.get('flaky')}" for x in (wk.get("ranking") or [])]
    for k in ("fixed", "broke", "standout"):
        v = wk.get(k)
        if v:
            md += [f"- {k}: {json.dumps(v)[:400]}"]
    md += ["", "## Latest"] + facts_md(data["facts"])
    md += ["", "## Pipeline counts"] + [f"- {k}: {v}" for k, v in data["pipeline_counts"].items()]
    md += [f"- Sponsor emails logged sent (last 7 d, sent/*-email-results.json): {sent}"]
    md += ["", "## Merged PRs, last 7 days"] + ([f"- #{p['number']} {p['title']}" for p in prs] if prs else [f"- {'gh unavailable' if prs is None else 'none'}"])
    md += ["", "## Channels"]
    md += [f"- Bluesky: {bs['followers']} followers, {bs['following']} following, {bs['posts']} posts" if bs else "- Bluesky: unavailable"]
    md += [f"- X radar/queue files this week: {len(radar)}", f"- Blog files (latest): {', '.join(data['blog_files'])}",
           f"- Newsletter issues on site: {', '.join(data['newsletter_issues'])}",
           "- Stripe, Beehiiv subscriber count and X/Buffer analytics: not fetched here (Grok connectors)."]
    return data, md


# ---------------------------------------------------------------- newsletter draft (part of recap)
NL_FOOTER = """## 🙏 Tell us

1. **One tool you want tested** before you install it.
2. **Did we get your tool wrong?** Send the link and we'll rerun it and fix the page.

I read every reply.

---

**Sponsor:** This spot is open. Founding rate: **$19 for 1 issue** (or **$59/mo for 4 issues**, about $15 each). Placements are always labeled; see [skillmaxx.gilventures.ai/advertise/](/advertise/)

Built a skill? We'll run it through all five agents: [skillmaxx.gilventures.ai/submit/](/submit/)

</div>
{% include "nlembed.njk" %}
"""


def fmt_d(s):
    try:
        x = date.fromisoformat(s)
        return x.strftime("%b ") + str(x.day)
    except (TypeError, ValueError):
        return str(s)


def published_issue_for_week(d):
    """(N, path) of a src/newsletter/issue-N.md already dated in d's Mon-Sun week (growth/scripts/newsletter_auto.py)."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("newsletter_auto", os.path.join(ROOT, "growth/scripts/newsletter_auto.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod.issue_for_week(d, ROOT)
    except Exception:
        return None


def next_issue_no():
    nums = [int(m.group(1)) for p in multi_glob("src/newsletter/issue-*.md")
            for m in [re.match(r"issue-(\d+)\.md$", os.path.basename(p))] if m]
    return (max(nums) + 1) if nums else 1


def newsletter_draft(d, wk, f):
    """No-LLM draft of the next SkillMaxx Weekly issue, mirroring src/newsletter/issue-N.md. Real numbers only."""
    n = next_issue_no()
    r = f.get("latest_report") or {}
    trend = wk.get("trend") or []
    last = trend[-1] if trend else {}
    key = wk.get("key", "")
    span = f"{fmt_d(wk.get('first') or wk.get('start'))} to {fmt_d(wk.get('last') or wk.get('end'))}"
    title = f"SkillMaxx #{n}: week {key.split('-')[-1] if key else '?'} in agent installs"
    p, tot = last.get("pass", r.get("pass")), last.get("total", r.get("total"))
    desc = (f"Issue #{n} of SkillMaxx Weekly: {p:,} of {tot:,} installs passed on {fmt_d(last.get('date', r.get('date')))}; "
            f"{wk.get('fixed_n', 0)} fixed, {wk.get('broke_n', 0)} broke, {wk.get('flaky_n', 0)} flaky ({span}).") if p and tot else f"Issue #{n} of SkillMaxx Weekly."
    jl = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": title, "datePublished": d.isoformat(),
                     "author": {"@type": "Organization", "name": "SkillMaxx"}, "publisher": {"@type": "Organization", "name": "SkillMaxx"},
                     "image": f"{SITE}/assets/newsletter/skillmaxx-banner-1200x300.png"})
    L = ["---", "layout: base.njk", f"title: {json.dumps(title)}", f"desc: {json.dumps(desc)}",
         "# DRAFT from growth/prep/prep.py recap (no LLM). Not built (eleventy ignores *.draft.md) and not sent.",
         "# To publish: polish, rename to issue-%d.md, set permalink: /newsletter/issue-%d/, remove the two draft lines below, add tags: issues." % (n, n),
         "permalink: false", "eleventyExcludeFromCollections: true",
         "ogType: article", f"issue: {n}", f'issueDate: "{d.isoformat()}"', f"date: {d.isoformat()}", f"jsonld: {jl}", "---",
         '<div class="wrap prose nlissue">',
         f'<p class="crumbs"><a href="/">SkillMaxx</a> / <a href="/newsletter/">Newsletter</a> / Issue #{n}</p>',
         f'<h1 class="ph">{title}</h1>',
         f'<p class="lead">{desc.split(": ", 1)[-1]}</p>', "",
         "![SkillMaxx](/assets/newsletter/skillmaxx-banner-1200x300.png)", "",
         "## hey, Brandon here 👋", "",
         "<!-- DRAFT: write 2–4 short paragraphs in growth/VOICE.md voice: the week's story, any mistakes of ours, what changed. Facts below only. -->",
         f"This week we ran {wk.get('runs', len(trend))} nightly install tests ({span}) of agent skills, plugins and MCP servers in Claude Code, Codex, Grok Build, Cursor and Pi.", ""]
    if wk.get("no_valid_run"):
        L += [f"Nights with no valid run (not published): {', '.join(fmt_d(x) for x in wk['no_valid_run'])}.", ""]
    if wk.get("version_changes"):
        L += [f"Agent version changes this week: {json.dumps(wk['version_changes'])[:300]}", ""]
    L += [f"## 📊 This week's numbers ({fmt_d(last.get('date', r.get('date')))})", ""]
    if p and tot:
        tested = last.get("tested")
        L += [f"**{p:,} of {tot:,} installs passed**" + (f" ({last.get('rate')}% of the {tested:,} we can judge without an API key)." if tested else "."), ""]
    if len(trend) > 1:
        L += ["Night by night: " + " · ".join(f"{fmt_d(t['date'])} {t['pass']:,}/{t['total']:,}" for t in trend) + ".", ""]
    by = r.get("by_raw") or {}
    if by:
        rows = []
        for k, v in by.items():
            judge = (v.get("total") or 0) - (v.get("needs_key") or 0)
            if judge > 0:
                rows.append((v.get("pass", 0) / judge, AG.get(k, k), v.get("pass", 0), judge))
        rows.sort(reverse=True)
        nk = sorted({v.get("needs_key") or 0 for v in by.values()})
        L += [f"**By agent on {fmt_d(r.get('date'))}** (installs we can judge without an API key"
              + (f"; {nk[0]} per agent need a key" if len(nk) == 1 and nk[0] else "") + "):", "",
              "| Agent | Passed | Rate |", "|---|---|---|"]
        L += [f"| {name} | {ps} / {j} | {rate * 100:.1f}% |" for rate, name, ps, j in rows] + [""]
    so = wk.get("standout")
    if so:
        L += [f"**Standout:** [{so['name']}](/skills/{so['slug']}/) installed clean in {len(so.get('agents') or [])} of 5 agents"
              + (f" ({so['why']})." if so.get("why") else "."), ""]

    def names(lst):
        return ", ".join(f"[{x['name']}](/skills/{x['slug']}/)" for x in (lst or [])[:5])
    L += [f"**{wk.get('fixed_n', 0)}** fixed" + (f" (including {names(wk.get('fixed'))})" if wk.get("fixed") else "")
          + f", **{wk.get('broke_n', 0)}** broke" + (f" (including {names(wk.get('broke'))})" if wk.get("broke") else "")
          + f", **{wk.get('flaky_n', 0)}** flaky" + (f" (including {names(wk.get('flaky'))})" if wk.get("flaky") else "") + ".", ""]
    links = []
    if r.get("date"):
        links.append(f"Full report: [skillmaxx.gilventures.ai/reports/{r['date']}/](/reports/{r['date']}/)")
    if key:
        links.append(f"Week chart: [skillmaxx.gilventures.ai/reports/week/{key}/](/reports/week/{key}/)")
    links.append("Is your tool safe today? [skillmaxx.gilventures.ai/reports/latest/](/reports/latest/)")
    L += [" · ".join(links), ""]
    blog = multi_glob(f"src/blog/week-{key}.njk") if key else []
    if blog:
        L += ["## 📝 On the blog", "", f"This week's data write-up: [skillmaxx.gilventures.ai/blog/week-{key}/](/blog/week-{key}/)", ""]
    picks = []
    for pth in reversed(radar_files(6, d)):
        for m in XURL.finditer(open(pth, encoding="utf-8").read()):
            u = f"https://x.com/{m.group(1)}/status/{m.group(2)}"
            if u not in picks:
                picks.append(u)
    L += ["## 👀 On our radar (not tested by us yet)", "",
          "<!-- DRAFT: pick up to 4 from the week's X radar files and write one line each; candidates: "
          + (" ".join(picks[:8]) or "none found") + " -->", "",
          "Want one of these in the nightly run? Reply with the name.", "",
          "## 🔧 Tip of the week", "", "<!-- DRAFT: one practical tip grounded in this week's data. -->", "", NL_FOOTER]
    return n, "\n".join(L)


# ---------------------------------------------------------------- main
def stamp():
    return now_et().strftime("%Y-%m-%d %H:%M %Z") + f" on {socket.gethostname().split('.')[0]}"


def source_sha():
    try:
        return subprocess.run(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"], capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:
        return ""


CMDS = {"xradar": cmd_xradar, "queue": cmd_queue, "bluesky": cmd_bluesky, "outreach": cmd_outreach,
        "pipeline": cmd_pipeline, "recap": cmd_recap}


def main(argv=None):
    global OFFLINE
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=list(CMDS))
    ap.add_argument("--date")
    ap.add_argument("--out", default=".")
    ap.add_argument("--name", help="output basename (default: CMD)")
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--zoho", action="store_true", help="outreach only: read-only Zoho scan (box)")
    a = ap.parse_args(argv)
    OFFLINE = a.offline
    d = date.fromisoformat(a.date) if a.date else now_et().date()
    data, md = CMDS[a.cmd](d, a)
    meta = {"cmd": a.cmd, "date": d.isoformat(), "generated": stamp(), "source_sha": source_sha()}
    os.makedirs(a.out, exist_ok=True)
    base = os.path.join(a.out, a.name or a.cmd)
    md.insert(1, f"<!-- prep {json.dumps(meta)} -->")
    with open(base + ".md", "w", encoding="utf-8") as f:
        f.write("\n".join(md).rstrip() + "\n")
    with open(base + ".json", "w", encoding="utf-8") as f:
        json.dump({"meta": meta, **data}, f, indent=1, default=str)
    print(f"prep {a.cmd}: wrote {base}.md")


if __name__ == "__main__":
    main()
