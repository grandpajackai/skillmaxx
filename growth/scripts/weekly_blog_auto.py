#!/usr/bin/env python3
"""No-LLM weekly blog post from the weekly scorecard (src/_data/weeks.json). Free, offline, no secrets.
Writes src/blog/week-<YYYY-WW>.njk for the newest week whose last day is <= DATE (default today ET).
Skips if the file exists or the week has no runs. Run on Sundays by testing/publish_nightly.sh, which ships it
in the same data PR as that night's report. Facts only from repo data; Brandon can still hand-write the
Sunday deep-dive (growth/content/BLOG-PLAYBOOK.md) on top of this.
Usage: python3 growth/scripts/weekly_blog_auto.py [YYYY-MM-DD] [--force]"""
import json, os, sys, html
from datetime import date
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SLUG = {"claude_code": "claude-code", "codex": "codex", "grok_build": "grok-build", "cursor": "cursor", "pi": "pi"}

def fmt(d):
    x = date.fromisoformat(d); return f"{x.strftime('%b')} {x.day}, {x.year}"

def items(lst, verb):
    if not lst: return f"<p>Nothing {verb} this week.</p>"
    li = "".join(f'<li><a href="/skills/{html.escape(i["slug"])}/">{html.escape(i["name"])}</a>'
                 + (f' ({i["n"]} agent/night results)' if i.get("n") else "") + "</li>" for i in lst[:10])
    more = f"<p class=\"muted\">And {len(lst) - 10} more on the scorecard.</p>" if len(lst) > 10 else ""
    return f"<ul>{li}</ul>{more}"

def main(argv):
    day = next((a for a in argv if not a.startswith("-")), None) or date.today().isoformat()
    weeks = json.load(open(os.path.join(ROOT, "src/_data/weeks.json")))
    w = next((x for x in sorted(weeks, key=lambda x: x["end"], reverse=True) if x["end"] <= day and x.get("runs")), None)
    if not w: print("no complete week with runs"); return 0
    out = os.path.join(ROOT, "src/blog", f"week-{w['key']}.njk")
    if os.path.exists(out) and "--force" not in argv: print("exists:", out); return 0
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
