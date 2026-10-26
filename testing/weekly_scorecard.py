#!/usr/bin/env python3
"""Weekly scorecard for the newsletter, built only from src/_data/reports.json
(the same data as the daily /reports/ pages). Usage: weekly_scorecard.py [END_DATE] [DAYS=7]
Prints markdown to paste into the weekly issue. Never sends anything."""
import json, os, sys, datetime as dt
from collections import Counter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://skillmaxx.gilventures.ai"
NAME = {"claude_code": "Claude Code", "codex": "Codex", "grok_build": "Grok Build", "cursor": "Cursor", "pi": "Pi"}
reps = sorted(json.load(open(os.path.join(ROOT, "src/_data/reports.json"))), key=lambda r: r["date"])
end = sys.argv[1] if len(sys.argv) > 1 else reps[-1]["date"]
days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
start = (dt.date.fromisoformat(end) - dt.timedelta(days=days - 1)).isoformat()
wk = [r for r in reps if start <= r["date"] <= end]
if not wk: sys.exit(f"no reports between {start} and {end}")
pct = lambda p, t: f"{p/t*100:.1f}%" if t else "n/a"
out = [f"## Weekly scorecard ({wk[0]['date']} to {wk[-1]['date']}, {len(wk)} nightly run{'s' if len(wk)!=1 else ''})", ""]
out.append("**Pass rate trend:** " + " → ".join(f"{r['date'][5:]} {r['pass']}/{r['total']} ({pct(r['pass'], r['total'])})" for r in wk))
fixed = Counter(); broke = Counter(); names = {}
for r in wk:
    for x in r.get("fixed", []): fixed[x["slug"]] += 1; names[x["slug"]] = x["name"]
    for x in r.get("broke", []): broke[x["slug"]] += 1; names[x["slug"]] = x["name"]
flaky = set(fixed) & set(broke)
for s in flaky: fixed.pop(s); broke.pop(s)
top = lambda c: ", ".join(f"[{names[s]}]({SITE}/skills/{s}/) ({n} agent-fix{'es' if n>1 else ''})" if False else f"[{names[s]}]({SITE}/skills/{s}/) ×{n}" for s, n in c.most_common(5)) or "none"
out.append(f"**Most fixed:** {top(fixed)} ({sum(fixed.values())} installs fixed this week)")
out.append(f"**Most broken:** {top(broke)} ({sum(broke.values())} installs newly broke this week)")
if flaky: out.append(f"**Flaky (broke and fixed in the same week, worth a retry before blaming):** " + ", ".join(sorted(names[s] for s in flaky)))
sos = [r["standout"] for r in wk if r.get("standout")]
if sos:
    so = max(reversed(sos), key=lambda x: len(x.get("agents", []))); s = so["slug"]
    out.append(f"**Standout of the week:** [{so['name']}]({SITE}/skills/{s}/), clean in {len(so.get('agents', []))} agents. {so.get('desc','')}")
last = wk[-1]["by"]
best = sorted(last.items(), key=lambda kv: (-kv[1]["pass"] / kv[1]["total"], -kv[1]["total"]))
out.append("**Per-agent (latest run):** " + " · ".join(f"{NAME.get(a,a)} {v['pass']}/{v['total']} ({pct(v['pass'], v['total'])})" for a, v in best))
out.append(f"**Most reliable agent this week:** {NAME.get(best[0][0], best[0][0])}")
out += ["", f"Every night's full results: {SITE}/reports/"]
print("\n".join(out))
