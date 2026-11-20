#!/usr/bin/env python3
"""No-LLM weekly blog post from the weekly scorecard (src/_data/weeks.json). Free, offline, no secrets.
Writes src/blog/week-<YYYY-WW>.njk for the newest week whose last day is <= DATE (default today ET).
Skips if the file exists or the week has no runs. Run on Sundays by testing/publish_nightly.sh, which ships it
in the same data PR as that night's report. Facts only from repo data; Brandon can still hand-write the
Sunday deep-dive (growth/content/BLOG-PLAYBOOK.md) on top of this.
Single Sunday post (Nov 18): this script is the only source of the Sunday post. It writes nothing if any other
src/blog/*.njk is already dated that Sunday (issueDate) or uses /blog/week-<key>/, so a hand/Grok post and the
auto post never both go out. The Grok Sunday recap only checks and links /blog/week-<key>/.
The Wednesday post is growth/scripts/midweek_blog_auto.py (/blog/midweek-<key>/), never dated a Sunday.
Usage: python3 growth/scripts/weekly_blog_auto.py [YYYY-MM-DD] [--force]"""
import glob, json, os, re, sys, html
from datetime import date

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import blog_queue
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SLUG = {"claude_code": "claude-code", "codex": "codex", "grok_build": "grok-build", "cursor": "cursor", "pi": "pi"}

def fmt(d):
    x = date.fromisoformat(d); return f"{x.strftime('%b')} {x.day}, {x.year}"

def fmt_short(d):
    x = date.fromisoformat(d); return f"{x.strftime('%b')} {x.day}"

def rd_json(rel, default):
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default

def items(lst, verb):
    if not lst: return f"<p>Nothing {verb} this week.</p>"
    li = "".join(f'<li><a href="/skills/{html.escape(i["slug"])}/">{html.escape(i["name"])}</a>'
                 + (f' ({i["n"]} agent/night results)' if i.get("n") else "") + "</li>" for i in lst[:10])
    more = f"<p class=\"muted\">And {len(lst) - 10} more on the scorecard.</p>" if len(lst) > 10 else ""
    return f"<ul>{li}</ul>{more}"

def sunday_posts(sunday, key, root=None):
    """Blog sources already dated this Sunday or claiming /blog/week-<key>/ (the single-Sunday-post guard)."""
    hits = []
    for p in sorted(glob.glob(os.path.join(root or ROOT, "src/blog", "*.njk"))):
        head = open(p, encoding="utf-8").read().split("\n---", 2)[0][:3000]
        if re.search(r'^issueDate:\s*"?%s"?\s*$' % re.escape(sunday), head, re.M) or f"/blog/week-{key}/" in head:
            hits.append(p)
    return hits


def main(argv):
    day = next((a for a in argv if not a.startswith("-")), None) or date.today().isoformat()
    weeks = json.load(open(os.path.join(ROOT, "src/_data/weeks.json")))
    w = next((x for x in sorted(weeks, key=lambda x: x["end"], reverse=True) if x["end"] <= day and x.get("runs")), None)
    if not w: print("no complete week with runs"); return 0
    out = os.path.join(ROOT, "src/blog", f"week-{w['key']}.njk")
    if os.path.exists(out) and "--force" not in argv: print("exists:", out); return 0
    other = [p for p in sunday_posts(w["end"], w["key"]) if os.path.abspath(p) != os.path.abspath(out)]
    if other:
        print("Sunday post already exists, not writing a second one:", ", ".join(os.path.relpath(p, ROOT) for p in other)); return 0
    t = w["trend"][-1]; p, n = t["pass"], t["tested"]; rate = round(100 * p / n, 1) if n else 0
    runs = w["runs"]; span = f"{fmt(w['start'])} to {fmt(w['end'])}"
    title = f"Agent add-on installs, week of {fmt(w['start'])}: {p:,} of {n:,} passed"
    desc = (f"{runs} nightly runs of real installs of skills, plugins and MCP servers in Claude Code, Codex, Grok Build, "
            f"Cursor and Pi, {span}. Latest night: {p:,} of {n:,} passed ({rate}%). What got fixed, what broke, what is flaky.")
    rows = "".join(f'<tr><th scope="row"><a href="/works-in/{SLUG.get(r["agent"], r["agent"])}/">{html.escape(r["name"])}</a></th>'
                   f'<td>{r["tested"]}</td><td>{r["pass"]}</td><td>{r["rate"]}%</td><td>{r.get("needs_key", 0)}</td></tr>'
                   for r in w["ranking"])
    s = w.get("standout") or {}
    standout = (f'<h2>Standout add-on</h2><p><a href="/skills/{html.escape(s["slug"])}/">{html.escape(s["name"])}</a> '
                f'installed cleanly in {len(s.get("agents") or [])} agents this week. {html.escape((s.get("desc") or "")[:200])}</p>') if s.get("slug") else ""
    vc = w.get("version_changes") or []
    vers = f"<p class=\"muted\">Agent versions changed during the week ({len(vc)} updates), so some changes may come from the agents, not the add-ons.</p>" if vc else ""
    queued = blog_queue.find_queued(ROOT, f"week-{w['key']}", day)
    if queued:
        _, qpath = queued
        last_d = t["date"]
        res = rd_json(f"testing/results/{last_d}.json", {}).get("results") or []
        skills_items = rd_json("data/skills.json", {}).get("items") or []
        reps = rd_json("src/_data/reports.json", []) or []
        rep = next((r for r in reps if r.get("date") == last_d), reps[0] if reps else {})
        notes = rd_json("src/_data/runNotes.json", {}) or {}
        tokens = blog_queue.build_common_tokens(res, skills_items, rep, notes, w["start"], last_d)
        cavs = list(tokens.pop("CAVEAT_LIST", []))
        if vc:
            cavs.append(f"Agent versions changed during the week ({len(vc)} updates), so some changes may come from the agents, not the add-ons.")
        ranking_table = (
            '<div class="tw"><table class="matrix"><thead><tr><th>Agent</th><th>Tested</th><th>Passed</th>'
            f'<th>Rate</th><th>Needs a key</th></tr></thead><tbody>{rows}</tbody></table></div>'
        )
        trend_rows = "".join(
            f'<tr><th scope="row"><a href="/reports/{html.escape(tr["date"])}/">{fmt_short(tr["date"])}</a></th>'
            f'<td>{tr["pass"]:,}</td><td>{tr["tested"]:,}</td><td>{round(100 * tr["pass"] / tr["tested"], 1) if tr["tested"] else 0}%</td>'
            f'<td>{tr.get("needs_key", 0):,}</td></tr>'
            for tr in (w.get("trend") or [])
        )
        trend_table = (
            '<div class="tw"><table class="matrix"><thead><tr><th>Night</th><th>Passed</th><th>Tested</th>'
            f'<th>Rate</th><th>Needs a key</th></tr></thead><tbody>{trend_rows}</tbody></table></div>'
        )
        standout_html = (
            f'<p><a href="/skills/{html.escape(s["slug"])}/">{html.escape(s["name"])}</a> '
            f'installed cleanly in {len(s.get("agents") or [])} agents this week. {html.escape((s.get("desc") or "")[:200])}</p>'
            if s.get("slug") else "<p>No single add-on cleared the multi-agent standout bar cleanly across all runs this week.</p>"
        )
        tokens.update({
            "WEEK_KEY": w["key"],
            "WEEK_START": w["start"],
            "WEEK_START_FMT": fmt(w["start"]),
            "WEEK_START_SHORT": fmt_short(w["start"]),
            "WEEK_END": w["end"],
            "WEEK_END_FMT": fmt(w["end"]),
            "WEEK_SPAN": span,
            "WEEK_RUNS": str(runs),
            "LATEST_DATE": last_d,
            "LATEST_DATE_FMT": fmt(last_d),
            "PASS": f"{p:,}",
            "TESTED": f"{n:,}",
            "TOTAL": f"{t.get('total', n):,}",
            "RATE": str(rate),
            "FIXED_N": str(w.get("fixed_n", 0)),
            "BROKE_N": str(w.get("broke_n", 0)),
            "FLAKY_N": str(w.get("flaky_n", 0)),
            "NEEDS_KEY": str(w.get("needs_key", 0)),
            "WEEK_RANKING_TABLE": ranking_table,
            "WEEK_TREND_TABLE": trend_table,
            "WEEK_FIXED_LIST": items(w.get("fixed") or [], "got fixed"),
            "WEEK_BROKE_LIST": items(w.get("broke") or [], "broke"),
            "WEEK_FLAKY_LIST": items(w.get("flaky") or [], "flipped"),
            "WEEK_STANDOUT_HTML": standout_html,
            "WEEK_VERSIONS_HTML": vers,
            "CAVEATS_HTML": f'<p class="muted">Caveats: {" ".join(cavs)}</p>' if cavs else "",
        })
        rendered, err = blog_queue.render_queued_template(qpath, tokens)
        if err:
            print("weekly blog queue error:", err)
            return 1
        open(out, "w", encoding="utf-8").write(rendered)
        print("wrote", os.path.relpath(out, ROOT))
        return 0
    jsonld = json.dumps({"@context": "https://schema.org", "@type": "BlogPosting", "headline": title, "datePublished": w["end"],
                         "author": {"@type": "Organization", "name": "SkillMaxx"}, "publisher": {"@type": "Organization", "name": "SkillMaxx"}})
    body = f"""---
layout: base.njk
title: {json.dumps(title)}
permalink: /blog/week-{w['key']}/
tags: blog
issueDate: "{w['end']}"
ogType: article
desc: {json.dumps(desc)}
jsonld: {jsonld}
---
<div class="wrap prose"><p class="muted">{fmt(w['end'])} · Data from {runs} nightly runs, {span} · generated from the weekly scorecard</p>
<h1 class="ph">{html.escape(title)}</h1>
<p class="answer">From {span} we ran {runs} nightly install tests of agent skills, plugins and MCP servers in five coding agents. On the latest night ({fmt(t['date'])}), {p:,} of {n:,} installs passed ({rate}%). {w.get('fixed_n', 0)} add-ons started working, {w.get('broke_n', 0)} broke and {w.get('flaky_n', 0)} flipped between nights.</p>
<h2>Pass rate by agent</h2>
<div class="tw"><table class="matrix"><thead><tr><th>Agent</th><th>Tested</th><th>Passed</th><th>Rate</th><th>Needs a key</th></tr></thead><tbody>{rows}</tbody></table></div>
<p>Each agent is tested on different add-ons (only the kinds it supports), so this shows how ready those add-ons are, not a ranking of the agents.</p>
{vers}
<h2>Fixed this week</h2>{items(w.get('fixed') or [], 'got fixed')}
<h2>Broke this week</h2>{items(w.get('broke') or [], 'broke')}
<h2>Flaky (passed some nights, failed others)</h2>{items(w.get('flaky') or [], 'flipped')}
{standout}
<p>Full numbers: <a href="/reports/week/{w['key']}/">weekly scorecard</a> · <a href="/reports/">daily reports</a> · <a href="/how-we-test/">how we test</a>.</p>
</div>
"""
    open(out, "w").write(body); print("wrote", os.path.relpath(out, ROOT)); return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
