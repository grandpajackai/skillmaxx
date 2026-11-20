#!/usr/bin/env python3
"""No-LLM, publishable SkillMaxx Weekly issue for one week. Free, offline, stdlib only, no secrets, never sends.

Writes src/newsletter/issue-N.md (same front matter and layout as issues 1-3, permalink /newsletter/issue-N/,
tags: issues) from committed repo data only: src/_data/weeks.json (weekly scorecard), src/_data/reports.json
(nightly reports) and the auto blog posts in src/blog/. Run on Sundays by testing/publish_nightly.sh in the
same auto-merged data PR as that night's report (Mondays it re-runs for the Sunday as an idempotent catch-up).

Rules:
  * One issue per week. The week is the Mon-Sun week containing DATE. If any src/newsletter/issue-*.md already
    has an issueDate (or week:) in that week, nothing is written. An existing issue-N.md is never overwritten.
  * N = highest existing issue-N.md + 1 (*.draft.md files are ignored).
  * The page must be clean copy: the generator refuses to write if it finds placeholder text (TODO, DRAFT,
    HTML comments, None/nan/undefined, "?"-only fields) or the week has no runs.
  * The email send stays held (growth/routines/NEWSLETTER-SEND.md). This script never touches Beehiiv.
Optional Grok polish may edit the published file afterwards; the auto copy is already publishable.

Usage: python3 growth/scripts/newsletter_auto.py [YYYY-MM-DD] [--radar-json PATH] [--dry-run] [--print]
Exit 0 = written or skipped (already published / nothing to publish); 1 = refused (placeholder check failed)."""
import glob, html, json, os, re, sys
from datetime import date, timedelta

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SITE = "https://skillmaxx.gilventures.ai"
AG = {"claude_code": "Claude Code", "codex": "Codex", "grok_build": "Grok Build", "cursor": "Cursor", "pi": "Pi"}
BANNER = "/assets/newsletter/skillmaxx-banner-1200x300.png"
FOOTER = """## 🙏 Tell us

1. **One tool you want tested** before you install it.
2. **Did we get your tool wrong?** Send the link and we'll rerun it and fix the page.

I read every reply.

---

**Sponsor:** This spot is open. Founding rate: **$19 for 1 issue** (or **$59/mo for 4 issues**, about $15 each). Placements are always labeled; see [skillmaxx.gilventures.ai/advertise/](/advertise/)

Built a skill? We'll run it through all five agents: [skillmaxx.gilventures.ai/submit/](/submit/)

</div>
{% include "nlembed.njk" %}
"""
# Anything that would mean the page is not finished copy.
PLACEHOLDER = re.compile(r"<!--|TODO|TBD|FIXME|\bDRAFT\b|\bNone\b|\bnan\b|\bundefined\b|\bnull\b|\{\{|\}\}|lorem|XXX|\?\?|week \?", re.I)


def rd_json(rel, default):
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def fmt(s, year=False):
    x = date.fromisoformat(s) if isinstance(s, str) else s
    return f"{x.strftime('%b')} {x.day}" + (f", {x.year}" if year else "")


def week_bounds(d):
    mon = d - timedelta(days=d.isoweekday() - 1)
    return mon, mon + timedelta(days=6)


def front(path):
    try:
        txt = open(path, encoding="utf-8").read()
    except OSError:
        return {}
    m = re.match(r"---\n(.*?)\n---", txt, re.S)
    out = {}
    for line in (m.group(1).splitlines() if m else []):
        k, _, v = line.partition(":")
        out[k.strip()] = v.strip().strip('"')
    return out


def issues(root=None):
    """{N: path} for published issues (issue-N.md only, never *.draft.md)."""
    out = {}
    for p in glob.glob(os.path.join(root or ROOT, "src/newsletter/issue-*.md")):
        m = re.match(r"issue-(\d+)\.md$", os.path.basename(p))
        if m:
            out[int(m.group(1))] = p
    return out


def issue_for_week(d, root=None):
    """(N, path) of an already published issue dated in d's Mon-Sun week (or tagged with its week), else None."""
    mon, sun = week_bounds(d)
    key = f"{d.isocalendar()[0]}-{d.isocalendar()[1]:02d}"
    for n, p in sorted(issues(root).items()):
        fm = front(p)
        try:
            idate = date.fromisoformat(fm.get("issueDate", "")[:10])
        except ValueError:
            idate = None
        if fm.get("week") == key or (idate and mon <= idate <= sun):
            return n, p
    return None


def next_issue_no(root=None):
    nums = issues(root)
    return max(nums) + 1 if nums else 1


def clean(name):
    """Safe text for a markdown link label inside a template-processed .md page."""
    return re.sub(r"[\[\]{}<>|*_`]", "", str(name)).strip() or "unnamed add-on"


def link(i):
    return f"[{clean(i['name'])}](/skills/{i['slug']}/)"


def names(lst, k=5):
    return ", ".join(link(x) for x in (lst or [])[:k])



def mentions_for_issue(n):
    """Independent, unsponsored mentions scheduled for this issue only (growth/newsletter/mentions.json)."""
    doc = rd_json("growth/newsletter/mentions.json", [])
    items = doc.get("mentions") if isinstance(doc, dict) else doc
    out = []
    seen = set()
    for it in items or []:
        if not isinstance(it, dict):
            continue
        issues = it.get("issues") if isinstance(it.get("issues"), list) else []
        if it.get("issue") is not None:
            issues = list(issues) + [it.get("issue")]
        issues = {int(x) for x in issues if str(x).isdigit() or isinstance(x, int)}
        if n not in issues:
            continue
        mid = str(it.get("id") or it.get("section_title") or len(out))
        if mid in seen:
            continue
        title = clean(it.get("section_title") or it.get("title") or "Independent mention")
        body = str(it.get("body") or it.get("body_md") or "").strip()
        disc = str(it.get("disclaimer") or "Not tested by SkillMaxx; independent mention, not sponsored.").strip()
        if not body or PLACEHOLDER.search(body) or PLACEHOLDER.search(title) or PLACEHOLDER.search(disc):
            continue
        seen.add(mid)
        out.append((title, body, disc))
    return out


def tip(wk, rep):
    """One practical tip picked by rule from this week's data (no LLM)."""
    if wk.get("version_changes"):
        return ("**Pin your agent version when something matters.** Agent versions changed during this week's runs. "
                "If an install breaks right after your agent auto-updates, check the agent's changelog before you blame the add-on.")
    if wk.get("flaky_n"):
        return (f"**Retry once before you give up on an install.** {wk['flaky_n']} add-ons passed on some nights and failed on others "
                "this week, usually because of a slow download or a network timeout, not a real bug. "
                "Here's how we tell the two apart: [flaky vs broken installs](/guides/flaky-vs-broken/).")
    if (rep or {}).get("needs_key"):
        return (f"**A failed install is not always a broken add-on.** {rep['needs_key']} installs on {fmt(rep['date'])} only failed because "
                "our sandbox has no API keys. Add the key the README asks for and they're likely to work for you. "
                "Each skill page says when that's the case.")
    return ("**Check the report before you install.** Every add-on page shows the last 10 nightly results per agent, "
            "so you can see in a few seconds if something works in your agent today: [skillmaxx.gilventures.ai/reports/latest/](/reports/latest/)")


def build(d, root=None, radar=None):
    """(N, text, slug_info) for the week containing d, or (None, reason, None) when nothing should be published."""
    global ROOT
    if root:
        ROOT = root
    mon, sun = week_bounds(d)
    key = f"{d.isocalendar()[0]}-{d.isocalendar()[1]:02d}"
    weeks = rd_json("src/_data/weeks.json", []) or []
    wk = next((w for w in weeks if w.get("key") == key), None)
    if not wk or not wk.get("runs") or not wk.get("trend"):
        return None, f"week {key} has no runs in src/_data/weeks.json", None
    reps = sorted([r for r in rd_json("src/_data/reports.json", []) or [] if r.get("date") and mon.isoformat() <= r["date"] <= d.isoformat()],
                  key=lambda r: r["date"])
    rep = reps[-1] if reps else {}
    trend = [t for t in wk["trend"] if t.get("date", "") <= d.isoformat()] or wk["trend"]
    last = trend[-1]
    p, tot, tested = last["pass"], last["total"], last.get("tested") or last["total"]
    rate = round(100 * p / tested, 1) if tested else 0
    n = next_issue_no()
    first, lastd = trend[0]["date"], last["date"]
    span = f"{fmt(first)} to {fmt(lastd)}" if first != lastd else fmt(lastd)
    runs = len(trend)
    title = f"SkillMaxx #{n}: {p:,} of {tot:,} agent add-on installs passed"
    desc = (f"Issue #{n} of SkillMaxx Weekly: {p:,} of {tot:,} installs of skills, plugins and MCP servers passed on {fmt(lastd, True)}. "
            f"{wk.get('fixed_n', 0)} fixed, {wk.get('broke_n', 0)} broke, {wk.get('flaky_n', 0)} flaky.")
    jl = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": title, "datePublished": d.isoformat(),
                     "author": {"@type": "Organization", "name": "SkillMaxx"}, "publisher": {"@type": "Organization", "name": "SkillMaxx"},
                     "image": f"{SITE}{BANNER}"})
    L = ["---", "layout: base.njk", f"title: {json.dumps(title)}", f"desc: {json.dumps(desc)}",
         f"permalink: /newsletter/issue-{n}/", "ogType: article", f"issue: {n}", f'issueDate: "{d.isoformat()}"',
         f"date: {d.isoformat()}", "tags: issues", f'week: "{key}"', f"jsonld: {jl}", "---",
         '<div class="wrap prose nlissue">',
         f'<p class="crumbs"><a href="/">SkillMaxx</a> / <a href="/newsletter/">Newsletter</a> / Issue #{n}</p>',
         f'<h1 class="ph">{html.escape(title)}</h1>',
         f'<p class="lead">{p:,} of {tot:,} installs passed on {fmt(lastd)}. <span class="muted">Test data from {span}, {sun.year}.</span></p>', "",
         f"![SkillMaxx]({BANNER})", "", "## hey, Brandon here 👋", ""]
    # Story paragraph, all from the scorecard.
    prev = next((w for w in weeks if w.get("end", "") < mon.isoformat() and w.get("trend")), None)
    move = ""
    if prev:
        pt = prev["trend"][-1]
        prate = round(100 * pt["pass"] / (pt.get("tested") or pt["total"]), 1) if (pt.get("tested") or pt["total"]) else 0
        diff = round(rate - prate, 1)
        verb = "up" if diff > 0 else "down" if diff < 0 else "flat"
        move = (f" That's {verb} from {prate}% on {fmt(pt['date'])}" + (f" ({abs(diff)} points)." if diff else ".")
                if not wk.get("baseline_start") else " We started a new test baseline this week, so we don't compare it with earlier weeks.")
    L += [f"This week we ran {runs} nightly install test{'s' if runs != 1 else ''} ({span}) of agent skills, plugins and MCP servers "
          f"in Claude Code, Codex, Grok Build, Cursor and Pi. On the latest night, {rate}% of the installs we can judge without an API key passed.{move}", "",
          f"**{wk.get('fixed_n', 0)}** add-on{'s' if wk.get('fixed_n', 0) != 1 else ''} started working, **{wk.get('broke_n', 0)}** broke "
          f"(failed two nights running) and **{wk.get('flaky_n', 0)}** flipped between pass and fail.", ""]
    if wk.get("no_valid_run"):
        L += [f"We skipped {', '.join(fmt(x) for x in wk['no_valid_run'])} on purpose: a problem in our own test setup made those nights "
              "untrustworthy, so they're marked \"no valid run\" on the [reports page](/reports/). No numbers beat wrong numbers.", ""]
    vc = wk.get("version_changes") or []
    if vc:
        L += ["Agent updates this week: " + "; ".join(
            f"{AG.get(v.get('agent'), v.get('agent'))} {clean(v.get('from', ''))} → {clean(v.get('to', ''))} ({fmt(v['date'])})" for v in vc if v.get("date"))
              + ". When an agent updates, some changes can come from the agent, not the add-on.", ""]
    L += ["This issue is put together automatically from our nightly test logs, and every number links to the report it came from.", "",
          f"## 📊 This week's numbers ({fmt(lastd)})", "",
          f"**{p:,} of {tot:,} installs passed** ({rate}% of the {tested:,} we can judge without an API key).", ""]
    if len(trend) > 1:
        L += ["Night by night: " + " · ".join(f"{fmt(t['date'])} {t['pass']:,}/{t['total']:,}" for t in trend) + ".", ""]
    by = rep.get("by") or {}
    if by and rep.get("date") == lastd:
        rows = []
        for k, v in by.items():
            judge = (v.get("total") or 0) - (v.get("needs_key") or 0)
            if judge > 0:
                rows.append((v.get("pass", 0) / judge, AG.get(k, k), v.get("pass", 0), judge))
        rows.sort(reverse=True)
        nk = sorted({v.get("needs_key") or 0 for v in by.values()})
        L += [f"**By agent on {fmt(lastd)}** (installs we can judge without an API key" + (f"; {nk[0]} per agent need a key" if len(nk) == 1 and nk[0] else "") + "):", "",
              "| Agent | Passed | Rate |", "|---|---|---|"] + [f"| {nm} | {ps} / {j} | {r * 100:.1f}% |" for r, nm, ps, j in rows] + [""]
    elif wk.get("ranking"):
        L += [f"**By agent, all {runs} nights summed** (installs we can judge without an API key):", "", "| Agent | Passed | Rate |", "|---|---|---|"]
        L += [f"| {r['name']} | {r['pass']} / {r['tested']} | {r['rate']}% |" for r in wk["ranking"]] + [""]
    so = wk.get("standout") or {}
    if so.get("slug"):
        k = len(so.get("agents") or [])
        L += [f"**Standout:** {link(so)} installed clean in {'all 5' if k == 5 else f'{k} of 5'} agents this week with no flakes."
              + (f" {clean(so['desc']).rstrip('.')}." if so.get("desc") else ""), ""]
    parts = []
    for label, kk in (("Fixed", "fixed"), ("Broke", "broke"), ("Flaky", "flaky")):
        if wk.get(kk):
            more = wk.get(f"{kk}_n", len(wk[kk])) - min(5, len(wk[kk]))
            parts.append(f"**{label}:** {names(wk[kk])}" + (f" and {more} more" if more > 0 else "") + ".")
    L += (parts and [" ".join(parts), ""]) or ["Nothing got fixed or broke this week.", ""]
    links = [f"Full report: [skillmaxx.gilventures.ai/reports/{lastd}/](/reports/{lastd}/)",
             f"Week chart: [skillmaxx.gilventures.ai/reports/week/{key}/](/reports/week/{key}/)",
             "Is your tool safe today? [skillmaxx.gilventures.ai/reports/latest/](/reports/latest/)"]
    L += [" · ".join(links), ""]
    blog = []
    if os.path.exists(os.path.join(ROOT, f"src/blog/midweek-{key}.njk")):
        t = front(os.path.join(ROOT, f"src/blog/midweek-{key}.njk")).get("title", "Mid-week check")
        blog.append(f"- Wednesday: [{clean(t)}](/blog/midweek-{key}/)")
    if os.path.exists(os.path.join(ROOT, f"src/blog/week-{key}.njk")):
        t = front(os.path.join(ROOT, f"src/blog/week-{key}.njk")).get("title", "This week's data write-up")
        blog.append(f"- Sunday: [{clean(t)}](/blog/week-{key}/)")
    if blog:
        L += ["## 📝 On the blog", ""] + blog + [""]
    radar_lines = []
    for item in (radar or []):
        if not isinstance(item, dict):
            continue
        t = clean(item.get("title") or "")
        u = str(item.get("url") or item.get("hn") or "").strip()
        if not t or not u.startswith(("http://", "https://")) or PLACEHOLDER.search(t) or PLACEHOLDER.search(u):
            continue
        pts = int(item.get("points") or 0)
        hn = str(item.get("hn") or "").strip()
        extra = f" ({pts} pts" + (f", [HN]({hn})" if hn and hn != u and not PLACEHOLDER.search(hn) else "") + ")" if pts else ""
        radar_lines.append(f"- [{t}]({u}){extra}")
        if len(radar_lines) >= 4:
            break
    if radar_lines:
        L += ["## 👀 On our radar (not tested by us yet)", ""] + radar_lines + ["", "Want one of these in the nightly run? Reply with the name.", ""]
    for title, body, disc in mentions_for_issue(n):
        L += [f"## {title}", "", body, "", f"*{disc}*", ""]
    L += ["## 🔧 Tip of the week", "", tip(wk, rep), "", FOOTER]
    return n, "\n".join(L), key


def problems(text):
    body = text.split("\n---\n", 1)[-1]
    return sorted({m.group(0) for m in PLACEHOLDER.finditer(body)})


def main(argv):
    radar_path = None
    pos = []
    i = 0
    while i < len(argv):
        if argv[i] == "--radar-json" and i + 1 < len(argv):
            radar_path = argv[i + 1]
            i += 2
            continue
        if not argv[i].startswith("-"):
            pos.append(argv[i])
        i += 1
    day = pos[0] if pos else None
    d = date.fromisoformat(day) if day else date.today()
    have = issue_for_week(d)
    if have:
        print(f"newsletter: issue #{have[0]} already covers the week of {d} ({os.path.relpath(have[1], ROOT)}); nothing written")
        return 0
    radar = rd_json(os.path.relpath(radar_path, ROOT), []) if radar_path and os.path.exists(radar_path) else []
    if radar_path and os.path.isabs(radar_path) and os.path.exists(radar_path):
        try:
            radar = json.load(open(radar_path, encoding="utf-8"))
        except (OSError, ValueError):
            radar = []
    n, text, key = build(d, radar=radar)
    if n is None:
        print(f"newsletter: skipped: {text}")
        return 0
    bad = problems(text)
    if bad:
        print(f"newsletter: REFUSED issue #{n}: placeholder text {bad}")
        return 1
    out = os.path.join(ROOT, "src/newsletter", f"issue-{n}.md")
    if os.path.exists(out):  # never overwrite (next_issue_no makes this impossible, belt and braces)
        print(f"newsletter: {out} exists; nothing written")
        return 0
    if "--print" in argv:
        print(text)
    if "--dry-run" in argv:
        print(f"newsletter: dry run, would write src/newsletter/issue-{n}.md (week {key})")
        return 0
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"newsletter: wrote src/newsletter/issue-{n}.md (week {key}) -> /newsletter/issue-{n}/")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
