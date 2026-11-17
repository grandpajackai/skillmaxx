#!/usr/bin/env python3
"""Data brief for the weekly SkillMaxx blog post. No LLM, no network (unless --suggest), no secrets.

Reads only files already in the repo after the nightly run lands:
  testing/results/<date>.json   raw nightly results (latest vs the latest run >= 7 days earlier)
  src/_data/weeks.json          weekly scorecards (ranking, fixed/broke/flaky, standout)
  src/_data/reports.json        daily reports (needs-key / broken lists for the latest night)
  src/_data/runNotes.json       harness caveats (baselines, nights with no valid run)
  data/skills.json              names/categories
  growth/content/keywords.md    target queries ("- " lines)
Prints Markdown to stdout (or --out FILE). The Sunday routine writes ONE post from it; see
growth/content/BLOG-PLAYBOOK.md.

Usage: python3 growth/scripts/weekly_post_brief.py [--out growth/content/briefs/YYYY-MM-DD.md] [--suggest]
"""
import argparse, glob, json, os, re, sys, urllib.parse, urllib.request
from datetime import date, timedelta

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SITE = "https://skillmaxx.gilventures.ai"
AG = {"claude_code": "Claude Code", "codex": "Codex", "grok_build": "Grok Build", "cursor": "Cursor", "pi": "Pi"}
AG_SLUG = {"claude_code": "claude-code", "codex": "codex", "grok_build": "grok-build", "cursor": "cursor", "pi": "pi"}
SEEDS = ["best mcp servers", "mcp server not working", "claude code plugins", "claude code skills", "cursor mcp",
         "codex mcp", "codex plugins", "grok build", "pi coding agent", "agent skills", "claude skills vs mcp",
         "how to install mcp server", "is mcp server safe"]


def rd(rel, default=None):
    try:
        with open(os.path.join(ROOT, rel), encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def results_files():
    return sorted(glob.glob(os.path.join(ROOT, "testing", "results", "*.json")))


def load_run(path):
    d = json.load(open(path, encoding="utf-8"))
    return os.path.basename(path)[:10], {(r["slug"], r["agent"]): r["status"] for r in d["results"]}


def rates(run):
    out = {}
    for (slug, a), s in run.items():
        p, t = out.get(a, (0, 0))
        out[a] = (p + (s == "pass"), t + 1)
    return out


def keywords():
    try:
        txt = open(os.path.join(ROOT, "growth", "content", "keywords.md"), encoding="utf-8").read()
    except OSError:
        return []
    return [l[2:].strip() for l in txt.splitlines() if l.startswith("- ") and not l.startswith("- \"") and "**" not in l and len(l) < 90]


def suggest(existing):
    new = []
    for s in SEEDS:
        u = "https://suggestqueries.google.com/complete/search?client=firefox&hl=en&q=" + urllib.parse.quote(s)
        try:
            req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
            for q in json.load(urllib.request.urlopen(req, timeout=10))[1]:
                if q not in existing and q not in new:
                    new.append(q)
        except Exception as e:  # network is optional; never fail the brief
            new.append(f"(autocomplete failed for '{s}': {e.__class__.__name__})")
    return new


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--suggest", action="store_true", help="also pull fresh Google autocomplete (free, network)")
    a = ap.parse_args()

    files = results_files()
    if not files:
        sys.exit("no testing/results/*.json yet")
    cur_date, cur = load_run(files[-1])
    cutoff = (date.fromisoformat(cur_date) - timedelta(days=7)).isoformat()
    prev_files = [f for f in files if os.path.basename(f)[:10] <= cutoff]
    prev_date, prev = load_run(prev_files[-1]) if prev_files else (None, {})
    names = {x["slug"]: x for x in (rd("data/skills.json", {}) or {}).get("items", [])}
    nm = lambda s: names.get(s, {}).get("name", s)
    weeks = rd("src/_data/weeks.json", []) or []
    reports = rd("src/_data/reports.json", []) or []
    notes = rd("src/_data/runNotes.json", {}) or {}

    L = []
    p = L.append
    p(f"# Weekly post brief: run {cur_date}" + (f" vs {prev_date}" if prev_date else ""))
    p("")
    p("Every number below comes from committed nightly results. Use only these numbers in the post.")
    p("")
    # caveats first so the writer can't miss them
    cav = []
    for b in notes.get("baselines", []):
        if prev_date is None or b.get("start", "") > prev_date:
            cav.append(f"Baseline change from {b['start']}: {b.get('why','')} Caveat: {b.get('caveat','')}")
    for n in notes.get("no_valid_run", []):
        if prev_date and prev_date < n["date"] <= cur_date:
            cav.append(f"No valid run on {n['date']}: {n['why']}")
    if cav:
        p("## Caveats (must be mentioned if they affect a claim)")
        for c in cav:
            p(f"- {c}")
        p("")

    rc, rp = rates(cur), rates(prev)
    p("## Pass rate by agent (week over week)")
    p("| Agent | " + (f"{prev_date} | " if prev_date else "") + f"{cur_date} | Change | Page |")
    p("|---|" + ("---|" if prev_date else "") + "---|---|---|")
    for k, n in AG.items():
        if k not in rc:
            continue
        c = rc[k]; cr = 100 * c[0] / c[1]
        row = f"| {n} | "
        if prev_date and k in rp:
            q = rp[k]; pr = 100 * q[0] / q[1]
            row += f"{q[0]}/{q[1]} ({pr:.1f}%) | {c[0]}/{c[1]} ({cr:.1f}%) | {cr - pr:+.1f} pts |"
        else:
            row += ("– | " if prev_date else "") + f"{c[0]}/{c[1]} ({cr:.1f}%) | – |"
        p(row + f" {SITE}/works-in/{AG_SLUG[k]}/ |")
    tc = sum(v[0] for v in rc.values()), sum(v[1] for v in rc.values())
    p(f"\nAll agents: {tc[0]} of {tc[1]} installs passed on {cur_date}.")
    if prev:
        tp = sum(v[0] for v in rp.values()), sum(v[1] for v in rp.values())
        p(f"All agents on {prev_date}: {tp[0]} of {tp[1]}.")
    p("")

    if prev:
        broke = sorted({(s, a) for (s, a), v in cur.items() if v != "pass" and prev.get((s, a)) == "pass"})
        fixed = sorted({(s, a) for (s, a), v in cur.items() if v == "pass" and prev.get((s, a)) not in (None, "pass")})
        added = sorted({s for s, _ in cur} - {s for s, _ in prev})
        removed = sorted({s for s, _ in prev} - {s for s, _ in cur})

        def grp(pairs):
            d = {}
            for s, ag in pairs:
                d.setdefault(s, []).append(AG[ag])
            return d

        for title, pairs in (("Newly failing (passed on %s, not on %s)" % (prev_date, cur_date), broke),
                             ("Newly passing (failed on %s, passed on %s)" % (prev_date, cur_date), fixed)):
            g = grp(pairs)
            p(f"## {title}: {len(pairs)} installs across {len(g)} add-ons")
            for s, ags in sorted(g.items(), key=lambda x: (-len(x[1]), nm(x[0]).lower()))[:25]:
                p(f"- {nm(s)} ({', '.join(ags)}): {SITE}/skills/{s}/")
            if len(g) > 25:
                p(f"- …and {len(g) - 25} more")
            p("")
        if added or removed:
            p(f"## Catalog changes: {len(added)} added, {len(removed)} removed")
            for s in added[:15]:
                p(f"- added: {nm(s)}: {SITE}/skills/{s}/")
            for s in removed[:15]:
                p(f"- removed: {nm(s)}")
            p("")

    if weeks:
        w = weeks[0]
        p(f"## Weekly scorecard {w['key']} ({w['start']} to {w['end']}, {w['runs']} valid runs)")
        p(f"Page: {SITE}/reports/week/{w['key']}/")
        p("Ranking (pass rate over the week's runs):")
        for r in w.get("ranking", []):
            p(f"- {r['name']}: {r['pass']}/{r['tested']} ({r['rate']}%), flaky {r.get('flaky',0)}, needs key {r.get('needs_key',0)}")
        if w.get("standout"):
            s = w["standout"]
            p(f"Standout: {s['name']} ({s.get('why','')}): {SITE}/skills/{s['slug']}/")
        p(f"Fixed {w.get('fixed_n',0)}, broke {w.get('broke_n',0)}, flaky {w.get('flaky_n',0)}, needs key {w.get('needs_key',0)}")
        if len(weeks) > 1:
            w2 = weeks[1]
            p(f"Previous week {w2['key']}: " + ", ".join(f"{r['name']} {r['rate']}%" for r in w2.get("ranking", [])))
        p("")
    if reports:
        r = reports[0]
        p(f"## Latest night ({r['date']}): {r['pass']}/{r['total']} passed, {r['needs_key']} need an API key, {r['broken']} broken, {r['pending']} pending")
        p(f"Report: {SITE}/reports/{r['date']}/  Always-current: {SITE}/reports/latest/")
        p("")

    # keyword matches: score each target query by overlap with this week's story words
    bag = set()
    for k, n in AG.items():
        if k in rc and (not prev or abs(100 * rc[k][0] / rc[k][1] - 100 * rp.get(k, rc[k])[0] / rp.get(k, rc[k])[1]) >= 1):
            bag |= set(n.lower().split())
    for (s, ag), v in cur.items():
        if prev and (prev.get((s, ag)) == "pass") != (v == "pass"):
            bag |= set(re.findall(r"[a-z]{3,}", (nm(s) + " " + names.get(s, {}).get("category", "") + " " + names.get(s, {}).get("type", "")).lower()))
            bag |= set(AG[ag].lower().split())
    bag |= {"mcp", "plugins", "skills", "best", "working", "work"}
    kws = keywords()
    scored = sorted(((len(set(re.findall(r"[a-z0-9.]+", q)) & bag), q) for q in kws), key=lambda x: (-x[0], x[1]))
    p("## Target queries that match this week's data (pick 1 primary + 2–3 secondary)")
    for sc, q in scored[:12]:
        if sc:
            p(f"- {q}  (overlap {sc})")
    p("")
    p("## Internal links to use")
    p(f"- {SITE}/works-in/<agent>/ (one per agent above), {SITE}/best/, {SITE}/reports/latest/, {SITE}/how-we-test/")
    p("")
    if a.suggest:
        new = suggest(set(kws))
        p("## Fresh Google autocomplete (not yet in keywords.md; add the real ones)")
        for q in new[:40]:
            p(f"- {q}")
        p("")

    text = "\n".join(L) + "\n"
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        open(a.out, "w", encoding="utf-8").write(text)
        print(f"wrote {a.out}")
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()
