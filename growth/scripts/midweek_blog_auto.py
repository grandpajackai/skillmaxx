#!/usr/bin/env python3
"""No-LLM mid-week blog post: "Mid-week check" movers and add-on-type roundup. Free, offline, stdlib only.

Writes src/blog/midweek-<YYYY-WW>.njk -> /blog/midweek-<YYYY-WW>/ (ISO week of DATE), from committed data only:
src/_data/reports.json (nightly reports: pass counts, per agent, broke/fixed lists), testing/results/<DATE>.json
(per-install results) and data/skills.json (add-on type). Run on Wednesdays by testing/publish_nightly.sh in the
same auto-merged data PR as that night's report (Thursday re-runs as a catch-up; the week key makes it idempotent).

Never collides with the Sunday post (/blog/week-<YYYY-WW>/, growth/scripts/weekly_blog_auto.py) or data pages
(/reports/..., /best/..., /works-in/...): different slug prefix, and it refuses to run on a Sunday.
Skips (exit 0) if the file exists, the date is not Wed/Thu (unless --force), or there is no report this week.
Usage: python3 growth/scripts/midweek_blog_auto.py [YYYY-MM-DD] [--force] [--dry-run]"""
import html, json, os, sys
from datetime import date, timedelta

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
import blog_queue

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SLUG = {"claude_code": "claude-code", "codex": "codex", "grok_build": "grok-build", "cursor": "cursor", "pi": "pi"}
AG = {"claude_code": "Claude Code", "codex": "Codex", "grok_build": "Grok Build", "cursor": "Cursor", "pi": "Pi"}
TYPE = {"plugin": "Plugins", "mcp-server": "MCP servers", "npm-mcp-package": "MCP servers (npm)", "skill": "Agent Skills"}


def rd_json(rel, default):
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def fmt(s, year=False):
    x = date.fromisoformat(s) if isinstance(s, str) else s
    return f"{x.strftime('%b')} {x.day}" + (f", {x.year}" if year else "")


def rate(p, t):
    return round(100 * p / t, 1) if t else 0.0


def week_key(d):
    y, w, _ = d.isocalendar()
    return f"{y}-{w:02d}"


def out_path(d):
    return os.path.join(ROOT, "src/blog", f"midweek-{week_key(d)}.njk")


def moves(reps):
    """Unique (slug, agent) broke/fixed items across reports, newest status wins (fixed later cancels broke)."""
    last = {}
    for r in reps:
        for kind in ("broke", "fixed"):
            for i in r.get(kind) or []:
                last[(i["slug"], i.get("agent"))] = (kind, r["date"], i)
    out = {"broke": [], "fixed": []}
    for (slug, agent), (kind, d, i) in last.items():
        out[kind].append({"slug": slug, "name": i.get("name") or slug, "agent": agent, "date": d, "stars": i.get("stars") or 0})
    for k in out:
        out[k].sort(key=lambda x: (-(x["stars"] or 0), x["name"].lower()))
    return out


def group(lst):
    """Group per-install moves by add-on: [{slug, name, agents[], date(latest), stars}] keeping the input order."""
    out = {}
    for i in lst:
        g = out.setdefault(i["slug"], {"slug": i["slug"], "name": i["name"], "agents": [], "date": i["date"], "stars": i["stars"]})
        if i["agent"] not in g["agents"]:
            g["agents"].append(i["agent"])
        g["date"] = max(g["date"], i["date"])
    return list(out.values())


def li(lst, verb):
    if not lst:
        return f"<p>Nothing {verb} since last Wednesday.</p>"
    g = group(lst)
    rows = "".join(f'<li><a href="/skills/{html.escape(i["slug"])}/">{html.escape(i["name"])}</a> in '
                   + ", ".join(f'<a href="/works-in/{SLUG.get(a, a)}/">{AG.get(a, a)}</a>' for a in sorted(i["agents"], key=lambda a: list(AG).index(a) if a in AG else 9))
                   + f' ({fmt(i["date"])})</li>' for i in g[:12])
    more = f'<p class="muted">And {len(g) - 12} more add-ons on the <a href="/reports/">daily reports</a>.</p>' if len(g) > 12 else ""
    return f"<ul>{rows}</ul>{more}"


def build(d):
    """(path, text) or (None, reason)."""
    reps = sorted([r for r in rd_json("src/_data/reports.json", []) or [] if r.get("date")], key=lambda r: r["date"])
    mon = d - timedelta(days=d.isoweekday() - 1)
    cur = next((r for r in reversed(reps) if mon.isoformat() <= r["date"] <= d.isoformat()), None)
    if not cur:
        return None, f"no nightly report between {mon} and {d}"
    cd = cur["date"]
    base = next((r for r in reversed(reps) if r["date"] <= (date.fromisoformat(cd) - timedelta(days=7)).isoformat()), None)
    window = [r for r in reps if (base["date"] if base else "0") < r["date"] <= cd]
    mv = moves(window)
    p, n, tested = cur["pass"], cur["total"], cur.get("tested") or cur["total"] - cur.get("needs_key", 0)
    r_now = rate(p, tested)
    # Per agent, latest vs a week earlier.
    rows = []
    for a, v in (cur.get("by") or {}).items():
        j = v.get("total", 0) - v.get("needs_key", 0)
        bv = (base or {}).get("by", {}).get(a) if base else None
        bj = (bv.get("total", 0) - bv.get("needs_key", 0)) if bv else 0
        before = f"{rate(bv['pass'], bj)}%" if bv and bj else "–"
        ch = round(rate(v.get("pass", 0), j) - rate(bv["pass"], bj), 1) if bv and bj else None
        rows.append((rate(v.get("pass", 0), j), f'<tr><th scope="row"><a href="/works-in/{SLUG.get(a, a)}/">{AG.get(a, a)}</a></th>'
                     f'<td>{v.get("pass", 0)} / {j}</td><td>{rate(v.get("pass", 0), j)}%</td><td>{before}</td>'
                     f'<td>{"–" if ch is None else ("+" if ch > 0 else "") + str(ch)}</td></tr>'))
    agent_rows = "".join(r for _, r in sorted(rows, reverse=True))
    # By add-on type from the per-install results.
    res = rd_json(f"testing/results/{cd}.json", {}).get("results") or []
    skills_items = rd_json("data/skills.json", {}).get("items") or []
    types = {i["slug"]: i.get("type") for i in skills_items}
    agg = {}
    for x in res:
        t = TYPE.get(types.get(x["slug"]), "Other")
        a = agg.setdefault(t, {"n": 0, "p": 0, "addons": set()})
        a["n"] += 1; a["p"] += x["status"] == "pass"; a["addons"].add(x["slug"])
    type_rows = "".join(f'<tr><th scope="row">{html.escape(t)}</th><td>{len(v["addons"])}</td><td>{v["n"]}</td><td>{v["p"]}</td><td>{rate(v["p"], v["n"])}%</td></tr>'
                        for t, v in sorted(agg.items(), key=lambda kv: -kv[1]["n"]))
    type_sec = ("<h2>Which kinds of add-ons install most reliably?</h2>"
                f"<p>On {fmt(cd)}, by add-on type (raw pass rate; installs that only need an API key count as not passed here):</p>"
                '<div class="tw"><table class="matrix"><thead><tr><th>Type</th><th>Add-ons</th><th>Installs</th><th>Passed</th><th>Rate</th></tr></thead>'
                f"<tbody>{type_rows}</tbody></table></div>") if type_rows else ""
    notes = rd_json("src/_data/runNotes.json", {}) or {}
    lo = base["date"] if base else cd
    caveats = [f'{fmt(b["start"])}: new test baseline. {html.escape(b.get("why", "").rstrip("."))}.' for b in notes.get("baselines") or [] if lo < b.get("start", "") <= cd]
    caveats += [f'{fmt(x["date"])}: no valid run.' for x in notes.get("no_valid_run") or [] if lo < x.get("date", "") <= cd]
    if base and cur.get("versions") and base.get("versions") and cur["versions"] != base["versions"]:
        caveats.append("Agent versions changed since the comparison night, so some moves may come from the agents, not the add-ons.")
    cav = f'<p class="muted">Caveats: {" ".join(caveats)}</p>' if caveats else ""
    key = week_key(d)
    prev_key = week_key(d - timedelta(days=7))
    since = f"since {fmt(base['date'])}" if base else "this week"
    delta = (f" A week earlier ({fmt(base['date'])}) it was {base['pass']:,} of {base['total']:,} ({rate(base['pass'], base.get('tested') or base['total'])}%)."
             if base else "")
    title = f"Mid-week check, {fmt(cd)}: {p:,} of {n:,} agent add-on installs passed"
    desc = f"{fmt(cd, True)}: {p:,} of {n:,} installs of skills, plugins and MCP servers passed in 5 coding agents. {len(mv['broke'])} broke and {len(mv['fixed'])} got fixed {since}."
    jsonld = json.dumps({"@context": "https://schema.org", "@type": "BlogPosting", "headline": title, "datePublished": d.isoformat(),
                         "description": desc, "author": {"@type": "Organization", "name": "SkillMaxx"}, "publisher": {"@type": "Organization", "name": "SkillMaxx"}})
    sunday = os.path.exists(os.path.join(ROOT, "src/blog", f"week-{prev_key}.njk"))
    queued = blog_queue.find_queued(ROOT, f"midweek-{key}", d.isoformat())
    if queued:
        _, qpath = queued
        agent_table = (
            '<div class="tw"><table class="matrix"><thead><tr><th>Agent</th>'
            f'<th>Passed ({fmt(cd)})</th><th>Rate</th><th>{fmt(base["date"]) if base else "Week before"}</th>'
            f'<th>Change (points)</th></tr></thead><tbody>{agent_rows}</tbody></table></div>'
        )
        tokens = blog_queue.build_common_tokens(res, skills_items, cur, notes, lo, cd)
        extra_cav = list(tokens.pop("CAVEAT_LIST", []))
        if base and cur.get("versions") and base.get("versions") and cur["versions"] != base["versions"]:
            extra_cav.append("Agent versions changed since the comparison night, so some moves may come from the agents, not the add-ons.")
        tokens.update({
            "ISSUE_DATE": d.isoformat(),
            "ISSUE_DATE_FMT": fmt(d, True),
            "WEEK_KEY": key,
            "PREV_WEEK_KEY": prev_key,
            "CD": cd,
            "CD_FMT": fmt(cd),
            "CD_FMT_FULL": fmt(cd, True),
            "BASE_CLAUSE": f", compared with {fmt(base['date'])}" if base else "",
            "BASE_SENTENCE": delta,
            "SINCE": since,
            "PASS": f"{p:,}",
            "TOTAL": f"{n:,}",
            "TESTED": f"{tested:,}",
            "RATE": f"{r_now}",
            "NEEDS_KEY": f"{cur.get('needs_key', 0):,}",
            "BROKEN": f"{cur.get('broken', 0):,}",
            "PENDING": f"{cur.get('pending', 0):,}",
            "FLAKY": f"{cur.get('flaky', 0):,}",
            "ADDONS": f"{cur.get('addons') or len(skills_items):,}",
            "BROKE_N": str(len(mv["broke"])),
            "FIXED_N": str(len(mv["fixed"])),
            "AGENT_COMPARISON_TABLE": agent_table,
            "BROKE_LIST": li(mv["broke"], "broke"),
            "FIXED_LIST": li(mv["fixed"], "got fixed"),
            "CAVEATS_HTML": f'<p class="muted">Caveats: {" ".join(extra_cav)}</p>' if extra_cav else "",
            "SUNDAY_LINK_PART": f' · <a href="/blog/week-{prev_key}/">last Sunday’s weekly write-up</a>' if sunday else "",
        })
        rendered, err = blog_queue.render_queued_template(qpath, tokens)
        if err:
            return None, err
        return out_path(d), rendered
    body = f"""---
layout: base.njk
title: {json.dumps(title)}
permalink: /blog/midweek-{key}/
tags: blog
issueDate: "{d.isoformat()}"
ogType: article
desc: {json.dumps(desc)}
jsonld: {jsonld}
---
<div class="wrap prose"><p class="muted">{fmt(d, True)} · Data from the {fmt(cd)} nightly run{f", compared with {fmt(base['date'])}" if base else ""} · generated from the nightly reports</p>
<h1 class="ph">{html.escape(title)}</h1>
<p class="answer">As of {fmt(cd, True)}, {p:,} of {n:,} sandboxed installs of agent skills, plugins and MCP servers passed in Claude Code, Codex, Grok Build, Cursor and Pi ({r_now}% of the {tested:,} we can judge without an API key).{delta} {len(mv['broke'])} add-on installs broke (failed two nights running) and {len(mv['fixed'])} got fixed {since}.</p>
<h2>How did each agent do this week?</h2>
<div class="tw"><table class="matrix"><thead><tr><th>Agent</th><th>Passed ({fmt(cd)})</th><th>Rate</th><th>{fmt(base['date']) if base else "Week before"}</th><th>Change (points)</th></tr></thead><tbody>{agent_rows}</tbody></table></div>
<p>Each agent is tested on different add-ons (only the kinds it supports), so this shows how ready those add-ons are, not a ranking of the agents.</p>
<h2>What broke {since}?</h2>{li(mv['broke'], 'broke')}
<h2>What got fixed {since}?</h2>{li(mv['fixed'], 'got fixed')}
{type_sec}
{cav}
<p>Full numbers: <a href="/reports/{cd}/">{fmt(cd)} report</a> · <a href="/reports/latest/">latest report</a> · <a href="/best/">best add-ons by category</a> · <a href="/matrix/">compatibility matrix</a>{f' · <a href="/blog/week-{prev_key}/">last Sunday’s weekly write-up</a>' if sunday else ""} · <a href="/how-we-test/">how we test</a>.</p>
</div>
"""
    return out_path(d), body


def main(argv):
    day = next((a for a in argv if not a.startswith("-")), None)
    d = date.fromisoformat(day) if day else date.today()
    if d.isoweekday() == 7:
        print("midweek: never on a Sunday (the Sunday post is weekly_blog_auto.py)"); return 0
    if d.isoweekday() not in (3, 4) and "--force" not in argv:
        print(f"midweek: {d} is not a Wednesday or Thursday; skipped"); return 0
    out = out_path(d)
    if os.path.exists(out) and "--force" not in argv:
        print("midweek: exists:", os.path.relpath(out, ROOT)); return 0
    path, body = build(d)
    if path is None:
        print("midweek: skipped:", body); return 0
    if "--dry-run" in argv:
        print(body); print("midweek: dry run, would write", os.path.relpath(path, ROOT)); return 0
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    print("midweek: wrote", os.path.relpath(path, ROOT), f"-> /blog/midweek-{week_key(d)}/"); return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
