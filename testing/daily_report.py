#!/usr/bin/env python3
"""Build daily report data + social post drafts from real nightly results.
Reads testing/results/*.json (one per nightly run), data/skills.json, data/meta/meta.json.
Writes src/_data/reports.json (Eleventy builds /reports/<date>/ from it) and
growth/daily/<date>.md (X + Bluesky drafts for the latest run; never posts anything).
Numbers come only from those files; a field with no data is left out."""
import json, glob, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://skillmaxx.gilventures.ai"
AG = ["claude_code", "codex", "grok_build", "cursor", "pi"]
NAME = {"claude_code": "Claude Code", "codex": "Codex", "grok_build": "Grok Build", "cursor": "Cursor", "pi": "Pi"}
rd = lambda p, d=None: json.load(open(os.path.join(ROOT, p))) if os.path.exists(os.path.join(ROOT, p)) else d
items = {x["slug"]: x for x in rd("data/skills.json", {"items": []})["items"]}
meta = rd("data/meta/meta.json", {})

def report(cur, prev):
    res = cur["results"]; st = {(r["slug"], r["agent"]): r["status"] for r in res}
    rep = {"date": cur["run_at"][:10], "run_at": cur["run_at"], "versions": cur.get("versions", {}),
           "total": len(res), "pass": sum(r["status"] == "pass" for r in res),
           "addons": len({r["slug"] for r in res}), "by": {}}
    rep["fail"] = rep["total"] - rep["pass"]
    for a in AG:
        p = sum(1 for (s, g), v in st.items() if g == a and v == "pass"); t = sum(1 for (s, g) in st if g == a)
        if t: rep["by"][a] = {"pass": p, "fail": t - p, "total": t}
    nm = lambda s: items.get(s, {}).get("name", s)
    if prev:
        pst = {(r["slug"], r["agent"]): r["status"] for r in prev["results"]}
        rep["prev_date"] = prev["run_at"][:10]
        rep["prev_pass"] = sum(v == "pass" for v in pst.values()); rep["prev_total"] = len(pst)
        flip = lambda a, b: sorted([{"slug": s, "name": nm(s), "agent": g} for (s, g), v in st.items() if pst.get((s, g)) == a and v == b], key=lambda x: (x["name"].lower(), x["agent"]))
        rep["broke"] = flip("pass", "fail"); rep["fixed"] = flip("fail", "pass")
        ps = {s for s, _ in pst}
        rep["added"] = sorted([{"slug": s, "name": nm(s)} for s in {s for s, _ in st} - ps], key=lambda x: x["name"].lower())
        rep["removed"] = sorted([{"slug": s, "name": nm(s)} for s in ps - {s for s, _ in st}], key=lambda x: x["name"].lower())
    # standout: passes in the most agents tonight; new additions first, then newly fixed, then GitHub stars
    passing = {}
    for (s, g), v in st.items():
        if v == "pass": passing.setdefault(s, []).append(g)
    if passing:
        added = {x["slug"] for x in rep.get("added", [])}; fixed = {x["slug"] for x in rep.get("fixed", [])}
        best = max(passing, key=lambda s: (s in added, s in fixed, len(passing[s]), (meta.get(s) or {}).get("stars") or 0, s))
        why = "new tonight" if best in added else "fixed tonight" if best in fixed else None
        stars = (meta.get(best) or {}).get("stars")
        rep["standout"] = {"slug": best, "name": nm(best), "desc": items.get(best, {}).get("description", "")[:200],
                           "agents": [a for a in AG if a in passing[best]], "why": why, "stars": stars}
    return rep

def main():
    files = sorted(glob.glob(os.path.join(ROOT, "testing/results/*.json")))
    runs = [json.load(open(f)) for f in files]
    reps = [report(c, runs[i - 1] if i else None) for i, c in enumerate(runs)]
    reps.sort(key=lambda r: r["date"], reverse=True)
    json.dump(reps, open(os.path.join(ROOT, "src/_data/reports.json"), "w"), indent=1)
    if reps: draft(reps[0])
    print(f"reports: {len(reps)} (latest {reps[0]['date'] if reps else '-'})")

def draft(r):
    url = f"{SITE}/reports/{r['date']}/"
    b, f, ad = r.get("broke"), r.get("fixed"), r.get("added")
    lines = [f"Last night we installed {r['addons']} agent add-ons for real: {r['pass']}/{r['total']} installs passed."]
    ch = []
    if f is not None: ch.append(f"{len(f)} fixed")
    if b is not None: ch.append(f"{len(b)} broke")
    if ad: ch.append(f"{len(ad)} new")
    if ch: lines.append(", ".join(ch).capitalize() + " since the last run" + (" (we see you, " + str(len(b)) + ")." if b else "."))
    top = sorted(r["by"].items(), key=lambda kv: kv[1]["pass"] / kv[1]["total"], reverse=True)
    if top:
        a, v = top[0]; lines.append(f"Cleanest run: {NAME[a]} {v['pass']}/{v['total']}.")
    s = r.get("standout")
    def build(extra):
        return "\n".join(lines + extra + [f"Full report: {url}"])
    out = {}
    for k, lim in (("X", 280), ("Bluesky", 300)):
        extra = [f"Standout: {s['name']}, " + (s['why'] + ", " if s['why'] else "") + f"clean in {len(s['agents'])} agents."] if s else []
        if k == "Bluesky": extra.append("Every install, real logs, nightly.")
        t = build(extra)
        while len(t) > lim and len(lines) > 1:  # drop optional lines until it fits
            if extra: extra.pop()
            else: lines.pop()
            t = build(extra)
        out[k] = t
    os.makedirs(os.path.join(ROOT, "growth/daily"), exist_ok=True)
    md = [f"# Daily post drafts: {r['date']}", "", "Status: DRAFT, waiting on Brandon's review. Not queued in Buffer, not posted.",
          f"Source: testing/results/{r['date']}.json (run {r['run_at']}). Report: {url}", ""]
    for k, lim in (("X", 280), ("Bluesky", 300)):
        md += [f"## {k} ({len(out[k])}/{lim} chars)", "", "```", out[k], "```", ""]
    open(os.path.join(ROOT, f"growth/daily/{r['date']}.md"), "w").write("\n".join(md))

if __name__ == "__main__":
    main()
