#!/usr/bin/env python3
"""SkillMaxx nightly test harness.
Installs each skill in each agent CLI inside a throwaway bubblewrap sandbox (sbx.sh) with a fresh HOME,
no credentials, no API keys. Verifies install + that the agent lists it as loaded/enabled (or, for MCP
servers, that the agent's own health check connects). Writes testing/results/<date>.json and appends history.json.
Usage: run_tests.py [--agents claude_code,grok_build,...] [--limit N] [--jobs 6] [--only slug,slug]
"""
import json,re,subprocess,sys,os,datetime,argparse,concurrent.futures as cf,shlex
HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.dirname(HERE);T="/workspace/agents/templates"
SBX=os.path.join(HERE,"sbx.sh");ANSI=re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
ap=argparse.ArgumentParser();ap.add_argument("--agents",default="claude_code,codex,grok_build,cursor,pi");ap.add_argument("--limit",type=int,default=0);ap.add_argument("--jobs",type=int,default=6);ap.add_argument("--only",default="");ap.add_argument("--timeout",type=int,default=150)
a=ap.parse_args();AG=a.agents.split(",")
items=json.load(open(os.path.join(ROOT,"data/skills.json")))["items"]
if a.only: items=[i for i in items if i["slug"] in a.only.split(",")]
VERS={}
def ver(cmd):
  try: return ANSI.sub("",subprocess.run([SBX,"",cmd+" 2>&1"],capture_output=True,text=True,timeout=30).stdout).strip().splitlines()[-1]
  except Exception: return "?"
def mcp_cmd(it):
  c=it["install"].get("claude_code") or "";return c.split(" -- ",1)[1] if " -- " in c else None
def mcp_name(it): return re.sub(r"[^a-z0-9]","",it["slug"].lower())[-20:] or "srv"
def cases():
  out=[]
  for it in items:
    s=it["slug"];L=" ".join(it.get("listings",[]));ismcp=it["type"] in("mcp-server","npm-mcp-package")
    for ag in AG:
      if ag=="claude_code":
        if "claude-plugins-official" in L: out.append((it,ag,"claude",f"claude plugin install {s}@claude-plugins-official 2>&1; echo ---LIST; claude plugin list 2>&1",lambda o,s=s: re.search(rf"{re.escape(s)}@claude-plugins-official[\s\S]{{0,120}}enabled",o.split('---LIST')[-1]) is not None))
        elif ismcp and mcp_cmd(it): n=mcp_name(it);out.append((it,ag,"",f"claude mcp add {n} -- {mcp_cmd(it)} 2>&1; echo ---LIST; claude mcp list 2>&1",lambda o,n=n: re.search(rf"^{n}:.*Connected",o.split('---LIST')[-1],re.M) is not None))
      elif ag=="grok_build":
        if "plugin-marketplace" in L or "claude-plugins-official" in L: out.append((it,ag,"grok",f"grok plugin install {s} --trust 2>&1; echo ---LIST; grok plugin list 2>&1",grok_ok))
      elif ag=="codex":
        if "openai/plugins" in L: out.append((it,ag,"codex",f"codex plugin add {s}@openai-plugins-mirror 2>&1; echo ---LIST; codex plugin list 2>&1",lambda o,s=s: re.search(rf"^{re.escape(s)}@openai-plugins-mirror\s+(installed|enabled)",o.split('---LIST')[-1],re.M) is not None))
      elif ag=="cursor":
        if ismcp and mcp_cmd(it):
          n=mcp_name(it);parts=shlex.split(mcp_cmd(it));cfg=json.dumps({"mcpServers":{n:{"command":parts[0],"args":parts[1:]}}})
          out.append((it,ag,"",f"mkdir -p ~/.cursor && echo {shlex.quote(cfg)} > ~/.cursor/mcp.json && cursor-agent mcp enable {n} 2>&1; echo ---LIST; cursor-agent mcp list 2>&1; cursor-agent mcp list-tools {n} 2>&1 | head -8",lambda o,n=n: re.search(rf"^{n}: ready",o.split('---LIST')[-1],re.M) is not None))
      elif ag=="pi":
        m=re.match(r"https://github\.com/([^/]+)/([^/#?]+?)(?:\.git)?/?$",it.get("source_url") or "")
        if m and it["type"]=="plugin":
          repo=f"github.com/{m[1]}/{m[2]}"
          out.append((it,ag,"",f"pi install git:{repo} 2>&1; echo ---LIST; pi list 2>&1; echo ---SKILLS; (find ~/.pi/agent/git/*/*/*/skills -name SKILL.md 2>/dev/null; for f in ~/.pi/agent/git/*/*/*/package.json; do grep -q '\"pi\"' $f 2>/dev/null && echo PIMANIFEST $f; done) | head -5",lambda o,r=m[2]: r.lower() in o.split('---LIST')[-1].split('---SKILLS')[0].lower() and ("SKILL.md" in o.split('---SKILLS')[-1] or "PIMANIFEST" in o.split('---SKILLS')[-1])))
  return out[:a.limit] if a.limit else out
def grok_ok(o):
  pre,post=o.split('---LIST')[0],o.split('---LIST')[-1]
  m=re.search(r"Installed \d+ plugin\(s\) from [^:]+: ([^\n]+)",pre)
  return bool(m) and all(re.search(rf":\s+{re.escape(n.strip())}\s+\[",post) for n in m[1].split(","))
def run(c):
  it,ag,tpl,cmd,check=c
  try:
    p=subprocess.run([SBX,f"{T}/{tpl}" if tpl else "",cmd],capture_output=True,text=True,timeout=a.timeout);o=ANSI.sub("",p.stdout+p.stderr);ok=check(o)
  except subprocess.TimeoutExpired as e: o=f"TIMEOUT after {a.timeout}s";ok=False
  lines=[l for l in o.splitlines() if l.strip() and not l.startswith("WARNING: proceeding")]
  if "---LIST" in o:
    pre=[l for l in o.split("---LIST")[0].splitlines() if l.strip() and not l.startswith("WARNING")][-3:]
    post=[l for l in o.split("---LIST",1)[1].splitlines() if l.strip()]
    hit=[l for l in post if it["slug"].lower() in l.lower() or mcp_name(it) in l or "SKILL.md" in l or "Status" in l or "ready" in l or "tools" in l.lower()][:4]
    lines=pre+["$ verify:"]+(hit or post[-3:])
  return {"slug":it["slug"],"agent":ag,"status":"pass" if ok else "fail","log":"\n".join(lines[-9:])[-700:]}
if __name__=="__main__":
  today=datetime.datetime.now().astimezone().isoformat(timespec="minutes")
  cs=cases();print(f"{len(cs)} cases",file=sys.stderr);res=[]
  with cf.ThreadPoolExecutor(a.jobs) as ex:
    for i,r in enumerate(ex.map(run,cs)):
      res.append(r)
      if i%25==0: print(i,r["slug"],r["agent"],r["status"],file=sys.stderr,flush=True)
  VERS={"claude_code":ver("claude --version"),"codex":ver("codex --version"),"grok_build":ver("grok --version"),"cursor":ver("cursor-agent --version"),"pi":"pi "+ver("pi --version")}
  os.makedirs(os.path.join(HERE,"results"),exist_ok=True)
  out={"run_at":today,"versions":VERS,"sandbox":"bubblewrap, fresh HOME, no credentials/API keys","results":res}
  rp=os.path.join(HERE,"results",today[:10]+".json")
  if os.path.exists(rp):
    old=json.load(open(rp));keep={(r["slug"],r["agent"]) for r in res};out["results"]=[r for r in old["results"] if (r["slug"],r["agent"]) not in keep]+res
  json.dump(out,open(rp,"w"),indent=1)
  hp=os.path.join(HERE,"history.json");h=json.load(open(hp)) if os.path.exists(hp) else {}
  for r in res:
    L=h.setdefault(f'{r["slug"]}|{r["agent"]}',[])
    if L and L[-1]["at"][:10]==today[:10]: L.pop()  # one result per day: a re-run replaces that day's entry
    L.append({"at":today,"status":r["status"],"log":r["log"]})
  json.dump(h,open(hp,"w"),indent=0)
  from collections import Counter;print(json.dumps(Counter(f'{r["agent"]}:{r["status"]}' for r in out["results"]),indent=0))
