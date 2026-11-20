#!/usr/bin/env python3
"""SkillMaxx nightly test harness.
Installs each skill in each agent CLI inside a throwaway bubblewrap sandbox (sbx.sh) with a fresh HOME,
no credentials, no API keys. Verifies install + that the agent lists it as loaded/enabled (or, for MCP
servers, that the agent's own health check connects; for standalone skills, that the agent lists the skill). Writes testing/results/<date>.json and appends history.json.
Usage: run_tests.py [--agents claude_code,grok_build,...] [--limit N] [--jobs 6] [--only slug,slug]
"""
import json,shutil,re,subprocess,sys,os,datetime,argparse,concurrent.futures as cf,shlex
HERE=os.path.dirname(os.path.abspath(__file__));ROOT=os.path.dirname(HERE);T=os.path.join(os.environ.get("SKILLMAXX_AGENTS","/workspace/agents"),"templates")
SBX=os.path.join(HERE,"sbx.sh");ANSI=re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
# Qualifiers confirmed on Grok 1.0.77. "xAI Official" also works for the xAI git source;
# the owner/repo form needs no shell quotes. The Claude source name is claude-plugins-official
# (a local directory of that basename). @plugin-marketplace is not a registered name.
# Prefer the xAI source when a skill is listed in both.
GROK_NATIVE_QUAL="xai-org/plugin-marketplace"
GROK_CLAUDE_QUAL="claude-plugins-official"
# Standalone Agent Skills (type "skill": a SKILL.md folder in a git repo, installed with the
# vercel-labs `skills` CLI, i.e. `npx skills add <repo> --skill <name>`). Pinned so a CLI release
# can't change results overnight. Telemetry is off (DISABLE_TELEMETRY/DO_NOT_TRACK), so the only
# network is npm (the CLI) and GitHub (the skill repo), the same hosts plugin tests already use.
SKILLS_CLI="skills@1.9.0"
SKILL_AGENT={"claude_code":"claude-code","codex":"codex","grok_build":"grok","cursor":"cursor","pi":"pi"}
# Per-agent "pass" for a standalone skill: the skills CLI installs it for that agent, then the agent's
# own CLI lists it, keyless. Cursor is the exception: cursor-agent can't list skills without signing in,
# so the check is that the SKILL.md landed in ~/.agents/skills AND this cursor-agent build's own code
# reads skills from that folder.
def ere(s): return re.sub(r'([.^$*+?()\[\]{}|\\])',r'\\\1',s)  # escape for grep -E without stray backslashes
def skill_verify(ag,n):
  q=shlex.quote
  if ag=="claude_code":  # the stream-json init event lists loaded skills before any API call
    return ("claude -p --output-format stream-json --verbose ok 2>&1 | grep -m1 -oE '\"skills\":\\[[^]]*\\]'",
            lambda o,n=n: re.search(rf'"skills":\[[^\]]*"{re.escape(n)}"',o.split('---LIST')[-1]) is not None)
  if ag=="codex":  # the model-visible prompt Codex would send, rendered locally
    return (f"codex debug prompt-input > /tmp/cx-prompt.txt 2>&1; grep -oE {q(ere(n)+': .{0,60}')} /tmp/cx-prompt.txt | head -1; grep -oE {q('[^ (]*/'+ere(n)+'/SKILL'+chr(92)+'.md')} /tmp/cx-prompt.txt | head -1",
            lambda o,n=n: re.search(rf"(?m)^{re.escape(n)}: ",o.split('---LIST')[-1]) is not None and f"/{n}/SKILL.md" in o.split('---LIST')[-1])
  if ag=="grok_build":
    return ("grok inspect 2>&1 | sed -n '/^ *Skills (/,/^ *$/p'",
            lambda o,n=n: re.search(rf"\u2514\s+{re.escape(n)}\s",o.split('---LIST')[-1]) is not None)
  if ag=="pi":  # RPC get_commands lists every loaded skill as /skill:<name>
    req=q('{"type":"get_commands","id":"1"}')
    return (f"printf '%s\\n' {req} | timeout 60 pi --mode rpc --offline 2>&1 | grep -o {q(chr(34)+'name'+chr(34)+':'+chr(34)+'skill:'+n+chr(34))} | head -1",
            lambda o,n=n: f'"name":"skill:{n}"' in o.split('---LIST')[-1])
  if ag=="cursor":
    marker='configDir:".agents",subdir:"skills"'
    return (f"D=$(dirname \"$(readlink -f \"$(command -v cursor-agent)\")\"); grep -qF {q(marker)} \"$D\"/index.js && echo 'cursor-agent reads ~/.agents/skills'; grep -H -m1 '^name:' ~/.agents/skills/{q(n)}/SKILL.md",
            lambda o,n=n: "cursor-agent reads ~/.agents/skills" in o.split('---LIST')[-1] and re.search(rf"(?m)/\.agents/skills/{re.escape(n)}/SKILL\.md:name:\s*['\"]?{re.escape(n)}['\"]?\s*$",o.split('---LIST')[-1]) is not None)
  return None
def skill_case(it,ag):
  sk=it.get("skill") or {};src,n=sk.get("source"),sk.get("name")
  if not src or not n or ag not in SKILL_AGENT: return None
  v=skill_verify(ag,n)
  if not v: return None
  cmd=(f"export DISABLE_TELEMETRY=1 DO_NOT_TRACK=1 npm_config_update_notifier=false; npx -y {SKILLS_CLI} add {shlex.quote(src)} --skill {shlex.quote(n)} -g -a {SKILL_AGENT[ag]} -y 2>&1 | tail -4; "
       f"echo ---LIST; {v[0]}")
  return (it,ag,"",cmd,v[1])
def mcp_cmd(it):
  c=it["install"].get("claude_code") or "";return c.split(" -- ",1)[1] if " -- " in c else None
def mcp_name(it):
  n=re.sub(r"[^a-z0-9]","",it["slug"].lower())[-20:] or "srv"
  return ("s"+n)[:20] if n[0].isdigit() else n
def npx_package(cmd):
  """Package name from an `npx -y <pkg>` (or `npx --package <pkg>`) MCP start command."""
  if not cmd: return None
  try: parts=shlex.split(cmd)
  except ValueError: return None
  if not parts or parts[0]!="npx": return None
  i=1
  while i<len(parts):
    a=parts[i]
    if a in ("-y","--yes","--no-yes","-q","--quiet","--prefer-offline","--offline","--no-install","--ignore-existing"):
      i+=1; continue
    if a in ("-p","--package") and i+1<len(parts): return parts[i+1]
    if a.startswith("--package="): return a.split("=",1)[1]
    if a.startswith("-") and i+1<len(parts) and not parts[i+1].startswith("-"):
      i+=2; continue
    if a.startswith("-"):
      i+=1; continue
    return a
  return None
def npm_cache_dir():
  env=os.environ.get("SKILLMAXX_NPM_CACHE")
  if env: return env
  if sys.platform=="darwin": return os.path.expanduser("~/Library/Caches/skillmaxx-npm")
  return os.path.join(os.environ.get("XDG_CACHE_HOME",os.path.expanduser("~/.cache")),"skillmaxx-npm")
def prewarm_npm(pkgs,jobs=3,timeout=400):
  """Fetch npx packages into a shared cache once, before any agent health-check.
  Each sandbox home is still empty of accounts and config. The agent's own connect
  timeout then measures server start, not a first-time npm download. Same cache is
  used for all 5 agents. Timeouts are unchanged."""
  pkgs=sorted({p for p in pkgs if p})
  if not pkgs or os.environ.get("SKILLMAXX_SKIP_PREWARM")=="1": return
  cache=npm_cache_dir(); os.makedirs(cache,exist_ok=True); os.environ["SKILLMAXX_NPM_CACHE"]=cache
  print(f"pre-warming {len(pkgs)} npm packages into {cache}",file=sys.stderr,flush=True)
  env={**os.environ,"SKILLMAXX_PREWARM_NPX":"1"}
  def one(pkg):
    js="console.log('WARM_OK')"; cmd=f"npx -y --package={shlex.quote(pkg)} -- node -e {shlex.quote(js)}"
    try:
      p=subprocess.run([SBX,"",cmd],capture_output=True,text=True,timeout=timeout,env=env)
      ok="WARM_OK" in (p.stdout+p.stderr)
    except subprocess.TimeoutExpired:
      ok=False
    print(("ok" if ok else "fail"),pkg,file=sys.stderr,flush=True)
    return ok
  with cf.ThreadPoolExecutor(min(jobs,len(pkgs))) as ex:
    list(ex.map(one,pkgs))
def uvx_cmd(cmd):
  """Normalized `uvx ...` invocation from an MCP start command, or None."""
  if not cmd: return None
  try: parts=shlex.split(cmd)
  except ValueError: return None
  if not parts or parts[0]!="uvx": return None
  return " ".join(shlex.quote(p) for p in parts)
def uv_cache_dir():
  env=os.environ.get("SKILLMAXX_UV_CACHE")
  if env: return env
  if sys.platform=="darwin": return os.path.expanduser("~/Library/Caches/skillmaxx-uv")
  return os.path.join(os.environ.get("XDG_CACHE_HOME",os.path.expanduser("~/.cache")),"skillmaxx-uv")
def prewarm_uvx(cmds,jobs=2,timeout=180):
  """Fetch uvx packages/venvs into a shared UV_CACHE_DIR once before any agent health-check."""
  cmds=sorted({c for c in cmds if c})
  if not cmds or os.environ.get("SKILLMAXX_SKIP_PREWARM")=="1": return
  cache=uv_cache_dir(); os.makedirs(cache,exist_ok=True); os.environ["SKILLMAXX_UV_CACHE"]=cache
  print(f"pre-warming {len(cmds)} uvx commands into {cache}",file=sys.stderr,flush=True)
  def one(cmd):
    try:
      p=subprocess.run([SBX,"",f"python3 /tmp/smx-testing/mcp_probe.py {cmd}"],capture_output=True,text=True,timeout=timeout)
      ok="PROBE OK" in (p.stdout+p.stderr)
    except subprocess.TimeoutExpired:
      ok=False
    print(("ok" if ok else "fail"),cmd,file=sys.stderr,flush=True)
    return ok
  with cf.ThreadPoolExecutor(min(jobs,len(cmds))) as ex:
    list(ex.map(one,cmds))
def grok_plugin_install(slug,listings):
  L=" ".join(listings or [])
  if "plugin-marketplace" in L: qual=GROK_NATIVE_QUAL
  elif "claude-plugins-official" in L: qual=GROK_CLAUDE_QUAL
  else: return None
  return f"grok plugin install {slug}@{qual} --trust 2>&1; echo ---LIST; grok plugin list 2>&1"
def cases():
  out=[]
  for it in items:
    s=it["slug"];L=" ".join(it.get("listings",[]));ismcp=it["type"] in("mcp-server","npm-mcp-package")
    if it["type"]=="skill":
      out+=[c for c in (skill_case(it,ag) for ag in AG) if c];continue
    for ag in AG:
      if ag=="claude_code":
        if "claude-plugins-official" in L: out.append((it,ag,"claude",f"claude plugin install {s}@claude-plugins-official 2>&1 && (claude plugin enable {s}@claude-plugins-official >/dev/null 2>&1 || true); echo ---LIST; claude plugin list 2>&1",lambda o,s=s: re.search(rf"{re.escape(s)}@claude-plugins-official[\s\S]{{0,120}}enabled",o.split('---LIST')[-1]) is not None))
        elif ismcp and mcp_cmd(it): n=mcp_name(it);out.append((it,ag,"",f"claude mcp add {n} -- {mcp_cmd(it)} 2>&1; echo ---LIST; claude mcp list 2>&1",lambda o,n=n: re.search(rf"^{n}:.*Connected",o.split('---LIST')[-1],re.M) is not None))
      elif ag=="grok_build":
        cmd=grok_plugin_install(s,it.get("listings",[]))
        if cmd: out.append((it,ag,"grok",cmd,grok_ok))
        elif ismcp and mcp_cmd(it): n=mcp_name(it);out.append((it,ag,"",f"grok mcp add {n} -- {mcp_cmd(it)} 2>&1; echo ---LIST; grok mcp list 2>&1; grok mcp doctor 2>&1",lambda o,n=n: re.search(rf"^\s*{n} \(stdio[\s\S]*?handshake OK",o.split('---LIST')[-1],re.M) is not None and "0 healthy" not in o))
      elif ag=="codex":
        if "openai/plugins" in L: out.append((it,ag,"codex",f"codex plugin add {s}@openai-plugins-mirror 2>&1; echo ---LIST; codex plugin list 2>&1",lambda o,s=s: re.search(rf"^{re.escape(s)}@openai-plugins-mirror\s+(installed|enabled)",o.split('---LIST')[-1],re.M) is not None))
        elif ismcp and mcp_cmd(it):  # Codex CLI has no MCP health check: verify Codex registers it enabled, then handshake the exact command it would launch
          n=mcp_name(it);out.append((it,ag,"",f"codex mcp add {n} -- {mcp_cmd(it)} 2>&1; echo ---LIST; codex mcp list 2>&1; python3 /tmp/smx-testing/mcp_probe.py {mcp_cmd(it)} 2>&1",lambda o,n=n: re.search(rf"^{n}\s+.*\benabled\b",o.split('---LIST')[-1],re.M) is not None and "PROBE OK" in o))
      elif ag=="cursor":
        if ismcp and mcp_cmd(it):
          n=mcp_name(it);parts=shlex.split(mcp_cmd(it));cfg=json.dumps({"mcpServers":{n:{"command":parts[0],"args":parts[1:]}}})
          out.append((it,ag,"",f"mkdir -p ~/.cursor && echo {shlex.quote(cfg)} > ~/.cursor/mcp.json && cursor-agent mcp enable {n} 2>&1; echo ---LIST; cursor-agent mcp list 2>&1; cursor-agent mcp list-tools {n} 2>&1 | head -8",lambda o,n=n: re.search(rf"^{n}: ready",o.split('---LIST')[-1],re.M) is not None))
      elif ag=="pi":
        if ismcp and mcp_cmd(it): n=mcp_name(it);out.append((it,ag,"",f"pi mcp add {n} -- {mcp_cmd(it)} 2>&1; echo ---LIST; pi mcp list 2>&1",lambda o,n=n: re.search(rf"^{n}: connected",o.split('---LIST')[-1],re.M) is not None));continue
        m=re.match(r"https://github\.com/([^/]+)/([^/#?]+?)(?:\.git)?/?$",it.get("source_url") or "")
        if m and it["type"]=="plugin":
          repo=f"github.com/{m[1]}/{m[2]}"
          out.append((it,ag,"",f"pi install git:{repo} 2>&1; echo ---LIST; pi list 2>&1; echo ---SKILLS; (find ~/.pi/agent/git/*/*/*/skills -name SKILL.md 2>/dev/null; for f in ~/.pi/agent/git/*/*/*/package.json; do grep -q '\"pi\"' $f 2>/dev/null && echo PIMANIFEST $f; done) | head -5",lambda o,r=m[2]: r.lower() in o.split('---LIST')[-1].split('---SKILLS')[0].lower() and ("SKILL.md" in o.split('---SKILLS')[-1] or "PIMANIFEST" in o.split('---SKILLS')[-1])))
  lim=getattr(globals().get("a"),"limit",0)
  return out[:lim] if lim else out
def grok_ok(o):
  pre,post=o.split('---LIST')[0],o.split('---LIST')[-1]
  m=re.search(r"Installed \d+ plugin\(s\) from [^:]+: ([^\n]+)",pre)
  return bool(m) and all(re.search(rf":\s+{re.escape(n.strip())}\s+\[",post) for n in m[1].split(","))
def ver(cmd):
  try: return ANSI.sub("",subprocess.run([SBX,"",cmd+" 2>&1"],capture_output=True,text=True,timeout=30).stdout).strip().splitlines()[-1]
  except Exception: return "?"
def run(c):
  r=run1(c);n=0
  while r["status"]=="fail" and n<a.retry:  # retry a failed install once (or --retry times) in a fresh sandbox
    n+=1;r2=run1(c);r2["retry"]=r2["status"];r2["first_log"]=r["log"][-300:];r=r2
  return r
def run1(c):
  it,ag,tpl,cmd,check=c
  try:
    p=subprocess.run([SBX,f"{T}/{tpl}" if tpl else "",cmd],capture_output=True,text=True,timeout=a.timeout);o=ANSI.sub("",p.stdout+p.stderr);ok=check(o)
  except subprocess.TimeoutExpired as e: o=f"TIMEOUT after {a.timeout}s";ok=False
  lines=[l for l in o.splitlines() if l.strip() and not l.startswith("WARNING: proceeding")]
  if "---LIST" in o:
    pre=[l for l in o.split("---LIST")[0].splitlines() if l.strip() and not l.startswith("WARNING")][-3:]
    post=[l for l in o.split("---LIST",1)[1].splitlines() if l.strip()]
    hit=[l for l in post if it["type"]=="skill" or it["slug"].lower() in l.lower() or mcp_name(it) in l or "SKILL.md" in l or "Status" in l or "ready" in l or "tools" in l.lower() or "PROBE" in l or "handshake" in l or "enabled" in l or "✗" in l or "✘" in l or "error" in l.lower() or "failed" in l.lower() or "timed out" in l.lower()][:4]
    lines=pre+["$ verify:"]+(hit or post[-3:])
  return {"slug":it["slug"],"agent":ag,"status":"pass" if ok else "fail","log":"\n".join(lines[-9:])[-700:]}
if __name__=="__main__":
  ap=argparse.ArgumentParser();ap.add_argument("--agents",default="claude_code,codex,grok_build,cursor,pi");ap.add_argument("--limit",type=int,default=0);ap.add_argument("--jobs",type=int,default=6);ap.add_argument("--only",default="");ap.add_argument("--timeout",type=int,default=300);ap.add_argument("--retry",type=int,default=0)
  a=ap.parse_args();AG=a.agents.split(",")
  items=json.load(open(os.path.join(ROOT,"data/skills.json")))["items"]
  if a.only: items=[i for i in items if i["slug"] in a.only.split(",")]
  today=datetime.datetime.now().astimezone().isoformat(timespec="minutes")
  prewarm_npm({npx_package(mcp_cmd(it)) for it in items}|({SKILLS_CLI} if any(it["type"]=="skill" for it in items) else set()))
  prewarm_uvx({uvx_cmd(mcp_cmd(it)) for it in items})
  cs=cases();print(f"{len(cs)} cases",file=sys.stderr);res=[]
  with cf.ThreadPoolExecutor(a.jobs) as ex:
    for i,r in enumerate(ex.map(run,cs)):
      res.append(r)
      if i%25==0: print(i,r["slug"],r["agent"],r["status"],file=sys.stderr,flush=True)
  VERS={"claude_code":ver("claude --version"),"codex":ver("codex --version"),"grok_build":ver("grok --version"),"cursor":ver("cursor-agent --version"),"pi":"pi "+ver("pi --version")}
  os.makedirs(os.path.join(HERE,"results"),exist_ok=True)
  out={"run_at":today,"versions":VERS,"sandbox":("bubblewrap" if shutil.which("bwrap") else "Docker (skillmaxx-sandbox:local, not privileged)")+", fresh HOME, no credentials/API keys","results":res}
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
