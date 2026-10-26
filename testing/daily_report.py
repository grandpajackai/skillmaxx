#!/usr/bin/env python3
"""Build daily report data + (big-event-only) social post drafts from real nightly results.
Reads testing/results/*.json (one per nightly run), data/skills.json, data/meta/meta.json.
Writes src/_data/reports.json (Eleventy builds /reports/<date>/ from it), src/_data/latestRows.json
(the "Is X safe to install today?" lookup on /reports/latest/) and, only when something big happened,
growth/daily/<date>.md (X + Bluesky drafts; never posts or queues anything).

Honest statuses for each install (slug x agent) tonight:
  pass       installed and loaded (a pass that needed the retry, or that flipped fail->pass->fail lately, is also "flaky")
  needs_key  failed because the add-on wants an API key / token / account our keyless sandbox doesn't have
  pending    failed tonight (after a retry) but passed last night: we re-check tomorrow before calling it broken
  broken     failed two nights in a row (the only thing we call "broke")
  flaky      status flip-flopped across the last 3 runs or only passed on retry. Never picked as the standout.
Numbers come only from those files; a field with no data is left out."""
import json, glob, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://skillmaxx.gilventures.ai"
AG = ["claude_code", "codex", "grok_build", "cursor", "pi"]
NAME = {"claude_code": "Claude Code", "codex": "Codex", "grok_build": "Grok Build", "cursor": "Cursor", "pi": "Pi"}
POPULAR = 1000  # GitHub stars: a "popular tool" for big-event post drafts
KEY = re.compile(r"api[_ -]?key|access[_ ]token|_token\b|\btoken (is )?(required|missing|not set)|environment variables?\b.{0,40}(not set|required|missing)|"
                 r"(missing|invalid) (required )?environment|is not set|credentials?\b|unauthori[sz]ed|\b401\b|personal access token", re.I)
rd = lambda p, d=None: json.load(open(os.path.join(ROOT, p))) if os.path.exists(os.path.join(ROOT, p)) else d
items = {x["slug"]: x for x in rd("data/skills.json", {"items": []})["items"]}
meta = rd("data/meta/meta.json", {})
nm = lambda s: items.get(s, {}).get("name", s)
stars = lambda s: (meta.get(s) or {}).get("stars") or 0

def keyed(run):
    """slugs whose failure logs (any agent) say a key/token/credential is missing"""
    return {r["slug"] for r in run["results"] if r["status"] == "fail" and KEY.search(r.get("log", "") + r.get("first_log", ""))}

def classify(runs, i):
    cur = runs[i]; prev = runs[i - 1] if i else None; pp = runs[i - 2] if i > 1 else None
    st = lambda run: {(r["slug"], r["agent"]): r["status"] for r in run["results"]} if run else {}
    c, p, q = st(cur), st(prev), st(pp)
    keys = keyed(cur) | (keyed(prev) if prev else set())
    rows = {}
    for r in cur["results"]:
        k = (r["slug"], r["agent"]); v = r["status"]
        flaky = r.get("retry") == "pass" or (k in p and k in q and q[k] != p[k] and p[k] != v)
        if v == "pass": s = "pass"
        elif r["slug"] in keys: s = "needs_key"
        elif p.get(k) == "fail": s = "broken"
        else: s = "pending"
        rows[k] = {"s": s, "flaky": flaky}
    return rows, c, p, q, keys

def report(runs, i):
    cur = runs[i]; prev = runs[i - 1] if i else None
    rows, c, p, q, keys = classify(runs, i)
    cnt = lambda pred: sum(1 for v in rows.values() if pred(v))
    rep = {"date": cur["run_at"][:10], "run_at": cur["run_at"], "versions": cur.get("versions", {}),
           "total": len(rows), "pass": cnt(lambda v: v["s"] == "pass"), "addons": len({s for s, _ in rows}),
           "needs_key": cnt(lambda v: v["s"] == "needs_key"), "broken": cnt(lambda v: v["s"] == "broken"),
           "pending": cnt(lambda v: v["s"] == "pending"), "flaky": cnt(lambda v: v["flaky"]),
           "retried": sum(1 for r in cur["results"] if r.get("retry")), "by": {}}
    rep["fail"] = rep["total"] - rep["pass"]
    rep["tested"] = rep["total"] - rep["needs_key"]  # installs we can judge without a key
    for a in AG:
        mine = [v for (s, g), v in rows.items() if g == a]
        if mine:
            b = {x: sum(v["s"] == x for v in mine) for x in ("pass", "needs_key", "broken", "pending")}
            b.update(total=len(mine), fail=len(mine) - b["pass"], flaky=sum(v["flaky"] for v in mine))
            rep["by"][a] = b
    li = lambda pred: sorted([{"slug": s, "name": nm(s), "agent": g, "stars": stars(s) or None} for (s, g), v in rows.items() if pred((s, g), v)],
                             key=lambda x: (x["name"].lower(), x["agent"]))
    if prev:
        rep["prev_date"] = prev["run_at"][:10]
        rep["prev_pass"] = sum(v == "pass" for v in p.values()); rep["prev_total"] = len(p)
        # broke = confirmed: 2nd failing night in a row after passing the night before that (needs 3 runs of history)
        rep["broke"] = li(lambda k, v: v["s"] == "broken" and q.get(k) == "pass")
        # fixed = passes tonight after failing 2+ nights; a single-night blip that came back is flaky, not fixed
        rep["fixed"] = li(lambda k, v: v["s"] == "pass" and p.get(k) == "fail" and q.get(k) == "fail" and k[0] not in keys and not v["flaky"])
        rep["pending_list"] = li(lambda k, v: v["s"] == "pending")
        rep["flaky_list"] = li(lambda k, v: v["flaky"])
        ps = {s for s, _ in p}
        rep["added"] = sorted([{"slug": s, "name": nm(s)} for s in {s for s, _ in c} - ps], key=lambda x: x["name"].lower())
        rep["removed"] = sorted([{"slug": s, "name": nm(s)} for s in ps - {s for s, _ in c}], key=lambda x: x["name"].lower())
        # agent update callout: version changed and installs that passed last night now fail (pending or broken)
        vc = []
        for a in AG:
            va, vb = (prev.get("versions") or {}).get(a), (cur.get("versions") or {}).get(a)
            if va and vb and va != vb and "?" not in (va, vb):
                n = [x for x in li(lambda k, v: k[1] == a and v["s"] in ("pending", "broken") and p.get(k) == "pass")]
                vc.append({"agent": a, "from": va, "to": vb, "broke": len(n), "items": n[:10]})
        rep["version_changes"] = vc
    rep["needs_key_list"] = li(lambda k, v: v["s"] == "needs_key")
    rep["broken_list"] = li(lambda k, v: v["s"] == "broken")
    # standout: clean everywhere it was tested tonight, nothing flaky/pending/broken for it; new, then confirmed-fixed, then agents, then stars
    bad = {s for (s, g), v in rows.items() if v["s"] != "pass" or v["flaky"]}
    passing = {}
    for (s, g), v in rows.items():
        if s not in bad: passing.setdefault(s, []).append(g)
    if passing:
        added = {x["slug"] for x in rep.get("added", [])}; fixed = {x["slug"] for x in rep.get("fixed", [])}
        best = max(passing, key=lambda s: (s in added, s in fixed, len(passing[s]), stars(s), s))
        why = "new tonight" if best in added else "fixed after failing 2+ nights" if best in fixed else None
        rep["standout"] = {"slug": best, "name": nm(best), "desc": items.get(best, {}).get("description", "")[:200],
                           "agents": [a for a in AG if a in passing[best]], "why": why, "stars": stars(best) or None}
    return rep, rows

def main():
    files = sorted(glob.glob(os.path.join(ROOT, "testing/results/*.json")))
    runs = [json.load(open(f)) for f in files]
    out = [report(runs, i) for i in range(len(runs))]
    reps = sorted([r for r, _ in out], key=lambda r: r["date"], reverse=True)
    json.dump(reps, open(os.path.join(ROOT, "src/_data/reports.json"), "w"), indent=1)
    if out:
        rep, rows = out[-1]
        lr = [{"s": s, "n": nm(s), "a": g, "st": v["s"], "f": 1 if v["flaky"] else 0} for (s, g), v in sorted(rows.items())]
        json.dump({"date": rep["date"], "rows": lr}, open(os.path.join(ROOT, "src/_data/latestRows.json"), "w"), separators=(",", ":"))
        draft(rep)
    print(f"reports: {len(reps)} (latest {reps[0]['date'] if reps else '-'})")

def events(r):
    ev = []
    for x in r.get("broke", []):
        if (x.get("stars") or 0) >= POPULAR:
            ev.append(f"{x['name']} ({x['stars']:,} stars) broke in {NAME[x['agent']]}, 2 nights running.")
    for v in r.get("version_changes", []):
        if v["broke"] >= 3:
            ev.append(f"{NAME[v['agent']]} updated {v['from']} → {v['to']} and {v['broke']} installs that worked the night before stopped working.")
    return ev

def draft(r):
    """Only big events get a post draft: a popular tool confirmed broken, or an agent update breaking 3+ installs."""
    ev = events(r)
    path = os.path.join(ROOT, f"growth/daily/{r['date']}.md")
    if not ev:
        if os.path.exists(path): os.remove(path)  # stale draft from before the big-events rule
        print("no big event tonight: no daily post draft")
        return
    url = f"{SITE}/reports/latest/"
    out = {}
    for k, lim in (("X", 280), ("Bluesky", 300)):
        lines = ["Heads up from last night's install run:"] + ev
        tail = ["Is your setup safe? Check before you install: " + url]
        t = "\n".join(lines + tail)
        while len(t) > lim and len(lines) > 2: lines.pop(); t = "\n".join(lines + tail)
        out[k] = t
    os.makedirs(os.path.dirname(path), exist_ok=True)
    md = [f"# Big-event post drafts: {r['date']}", "", "Status: DRAFT, waiting on Brandon's review. Not queued in Buffer, not posted.",
          f"Why there's a draft: {'; '.join(ev)}", f"Source: testing/results/{r['date']}.json (run {r['run_at']}). Report: {SITE}/reports/{r['date']}/", ""]
    for k, lim in (("X", 280), ("Bluesky", 300)):
        md += [f"## {k} ({len(out[k])}/{lim} chars)", "", "```", out[k], "```", ""]
    open(path, "w").write("\n".join(md))

if __name__ == "__main__":
    main()
