#!/usr/bin/env python3
"""Weekly scorecard, built only from src/_data/reports.json (same data as the daily /reports/ pages).
Usage: weekly_scorecard.py [--write] [END_DATE] [DAYS=7]
  default  print the newsletter scorecard markdown for the 7 days ending END_DATE (default: latest run)
  --write  also write src/_data/weeks.json (Eleventy builds /reports/week/YYYY-WW/ + the index, and the
           /advertise/ chart) and a weekly scorecard post draft in growth/weekly/YYYY-WW.md.
Honest counting: "broke" = failed 2 nights running, needs-a-key failures are counted apart, flaky items are
never the standout. Never sends, posts or queues anything."""
import json, os, sys, datetime as dt
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://skillmaxx.gilventures.ai"
AG = ["claude_code", "codex", "grok_build", "cursor", "pi"]
NAME = {"claude_code": "Claude Code", "codex": "Codex", "grok_build": "Grok Build", "cursor": "Cursor", "pi": "Pi"}
args = [a for a in sys.argv[1:] if a != "--write"]; WRITE = "--write" in sys.argv
reps = sorted(json.load(open(os.path.join(ROOT, "src/_data/reports.json"))), key=lambda r: r["date"])
pct = lambda p, t: round(p / t * 100, 1) if t else None
tested = lambda r: r.get("tested", r["total"])
wkey = lambda d: "%04d-%02d" % dt.date.fromisoformat(d).isocalendar()[:2]

def chart(trend):
    """tiny static SVG line chart of the honest pass rate (pass / installs we can judge without a key)"""
    W, H, P = 560, 180, 34
    pts = [t for t in trend if t["rate"] is not None]
    if not pts: return ""
    lo = max(0, min(t["rate"] for t in pts) - 5); hi = min(100, max(t["rate"] for t in pts) + 2)
    hi = hi if hi > lo else lo + 1
    xs = lambda i: P + (W - 2 * P) * (i / (len(pts) - 1) if len(pts) > 1 else 0.5)
    ys = lambda v: H - P - (H - 2 * P) * (v - lo) / (hi - lo)
    path = " ".join(f"{'M' if i == 0 else 'L'}{xs(i):.1f},{ys(t['rate']):.1f}" for i, t in enumerate(pts))
    g = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-labelledby="ct" class="chart" xmlns="http://www.w3.org/2000/svg">',
         f'<title id="ct">Install pass rate by night: ' + ", ".join(f"{t['date']} {t['rate']}%" for t in pts) + '</title>',
         f'<line x1="{P}" y1="{H-P}" x2="{W-P}" y2="{H-P}" stroke="currentColor" stroke-opacity=".25"/>',
         f'<text x="4" y="{ys(hi)+4:.0f}" font-size="11" fill="currentColor">{hi:.0f}%</text><text x="4" y="{ys(lo)+4:.0f}" font-size="11" fill="currentColor">{lo:.0f}%</text>',
         f'<path d="{path}" fill="none" stroke="#22c55e" stroke-width="3" stroke-linejoin="round"/>']
    for i, t in enumerate(pts):
        g.append(f'<circle cx="{xs(i):.1f}" cy="{ys(t["rate"]):.1f}" r="4" fill="#22c55e"/><text x="{xs(i):.1f}" y="{ys(t["rate"])-9:.1f}" font-size="11" text-anchor="middle" fill="currentColor">{t["rate"]}%</text>'
                 f'<text x="{xs(i):.1f}" y="{H-P+16}" font-size="11" text-anchor="middle" fill="currentColor">{t["date"][5:]}</text>')
    return "".join(g) + "</svg>"

def week(wk, key):
    trend = [{"date": r["date"], "pass": r["pass"], "tested": tested(r), "total": r["total"], "needs_key": r.get("needs_key", 0),
              "rate": pct(r["pass"], tested(r))} for r in wk]
    agg = {}
    for r in wk:
        for a, v in r["by"].items():
            x = agg.setdefault(a, Counter()); x["pass"] += v["pass"]; x["tested"] += v["total"] - v.get("needs_key", 0)
            x["flaky"] += v.get("flaky", 0); x["broken"] += v.get("broken", 0); x["needs_key"] += v.get("needs_key", 0)
    rank = sorted([{"agent": a, "name": NAME.get(a, a), "pass": v["pass"], "tested": v["tested"], "rate": pct(v["pass"], v["tested"]),
                    "flaky": v["flaky"], "needs_key": v["needs_key"]} for a, v in agg.items()],
                  key=lambda x: (-(x["rate"] or 0), x["flaky"], -x["tested"]))
    names = {}; c = {k: Counter() for k in ("fixed", "broke", "flaky")}
    for r in wk:
        for k, f in (("fixed", "fixed"), ("broke", "broke"), ("flaky", "flaky_list")):
            for x in r.get(f) or []: c[k][x["slug"]] += 1; names[x["slug"]] = x["name"]
    top = lambda k: [{"slug": s, "name": names[s], "n": n} for s, n in c[k].most_common(5)]
    flaky = set(c["flaky"])
    sos = [r["standout"] for r in wk if r.get("standout") and r["standout"]["slug"] not in flaky]
    so = max(reversed(sos), key=lambda x: (len(x.get("agents", [])), x.get("stars") or 0)) if sos else None
    vc = [dict(v, date=r["date"]) for r in wk for v in r.get("version_changes", [])]
    y, w = map(int, key.split("-"))
    return {"key": key, "start": dt.date.fromisocalendar(y, w, 1).isoformat(), "end": dt.date.fromisocalendar(y, w, 7).isoformat(),
            "first": wk[0]["date"], "last": wk[-1]["date"], "runs": len(wk), "trend": trend, "ranking": rank,
            "fixed": top("fixed"), "broke": top("broke"), "flaky": top("flaky"), "fixed_n": sum(c["fixed"].values()),
            "broke_n": sum(c["broke"].values()), "flaky_n": len(flaky), "needs_key": wk[-1].get("needs_key", 0),
            "standout": so, "version_changes": vc, "svg": chart(trend)}

def markdown(w):
    L = lambda x: f"[{x['name']}]({SITE}/skills/{x['slug']}/)"
    out = [f"## Weekly scorecard ({w['first']} to {w['last']}, {w['runs']} nightly run{'s' if w['runs'] != 1 else ''})", ""]
    out.append("**Pass rate trend** (installs we can judge without an API key): " + " → ".join(f"{t['date'][5:]} {t['pass']}/{t['tested']} ({t['rate']}%)" for t in w["trend"]))
    out.append(f"**Confirmed broke (failed 2 nights running):** " + (", ".join(L(x) for x in w["broke"]) or "nothing") + f" ({w['broke_n']} installs)")
    out.append(f"**Really fixed (passing after 2+ bad nights):** " + (", ".join(L(x) for x in w["fixed"]) or "nothing") + f" ({w['fixed_n']} installs)")
    if w["flaky_n"]: out.append(f"**Flaky, ignore the drama:** {w['flaky_n']} add-ons flip-flopped (e.g. " + ", ".join(x["name"] for x in w["flaky"][:5]) + "). We don't call these broken or fixed.")
    if w["needs_key"]: out.append(f"**Needs your API key:** {w['needs_key']} installs only failed because our sandbox has no keys. Not broken, just shy.")
    for v in w["version_changes"]:
        if v["broke"]: out.append(f"**Agent update:** {NAME.get(v['agent'], v['agent'])} {v['from']} → {v['to']} ({v['date']}): {v['broke']} installs stopped working.")
    if w["standout"]: out.append(f"**Standout of the week:** {L(w['standout'])}, clean in {len(w['standout']['agents'])} agents, zero flakes. {w['standout'].get('desc', '')}")
    out.append("**Most reliable agents:** " + " · ".join(f"{i+1}. {x['name']} {x['rate']}%" for i, x in enumerate(w["ranking"])))
    out += ["", f"Chart + full week: {SITE}/reports/week/{w['key']}/ · Is your tool safe today? {SITE}/reports/latest/"]
    return "\n".join(out)

def post(w):
    best = w["ranking"][0] if w["ranking"] else None; t = w["trend"][-1]
    lines = [f"Week {w['key']} install scorecard: {t['pass']}/{t['tested']} installs clean ({t['rate']}%).",
             f"Confirmed broke: {w['broke_n']}. Really fixed: {w['fixed_n']}. Flaky noise we refused to count: {w['flaky_n']}."]
    if best: lines.append(f"Most reliable agent: {best['name']} ({best['rate']}%).")
    tail = f"{SITE}/reports/week/{w['key']}/"
    out = {}
    for k, lim in (("X", 280), ("Bluesky", 300)):
        ls = list(lines); s = "\n".join(ls + [tail])
        while len(s) > lim and len(ls) > 1: ls.pop(); s = "\n".join(ls + [tail])
        out[k] = s
    md = [f"# Weekly scorecard post drafts: {w['key']}", "", "Status: DRAFT, waiting on Brandon's review. Not queued in Buffer, not posted.", ""]
    for k, lim in (("X", 280), ("Bluesky", 300)): md += [f"## {k} ({len(out[k])}/{lim} chars)", "", "```", out[k], "```", ""]
    return "\n".join(md)

if __name__ == "__main__":
    end = args[0] if args else reps[-1]["date"]; days = int(args[1]) if len(args) > 1 else 7
    start = (dt.date.fromisoformat(end) - dt.timedelta(days=days - 1)).isoformat()
    wk = [r for r in reps if start <= r["date"] <= end]
    if not wk: sys.exit(f"no reports between {start} and {end}")
    print(markdown(week(wk, wkey(end))))
    if WRITE:
        groups = {}
        for r in reps: groups.setdefault(wkey(r["date"]), []).append(r)
        weeks = sorted([week(v, k) for k, v in groups.items()], key=lambda w: w["key"], reverse=True)
        json.dump(weeks, open(os.path.join(ROOT, "src/_data/weeks.json"), "w"), indent=1)
        os.makedirs(os.path.join(ROOT, "growth/weekly"), exist_ok=True)
        open(os.path.join(ROOT, f"growth/weekly/{weeks[0]['key']}.md"), "w").write(post(weeks[0]))
