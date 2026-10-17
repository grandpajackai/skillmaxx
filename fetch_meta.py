#!/usr/bin/env python3
"""Fetch logos (local, optimized), GitHub repo, stars, last-updated and README for each skill.
No API tokens: uses public github.com pages, raw.githubusercontent.com and github.com/<owner>.png avatars."""
import json,re,os,io,urllib.request,urllib.parse,html,concurrent.futures as cf
from PIL import Image
ROOT=os.path.dirname(os.path.abspath(__file__));LOGO=os.path.join(ROOT,"src/assets/logos");RD=os.path.join(ROOT,"data/meta/readme")
MIR="/workspace/agents/codex-mirror";UA={"User-Agent":"SkillMaxx-metadata/1.0 (+https://skillmaxx.dev)"}
MKT={"anthropics/claude-plugins-official","anthropics/claude-plugins-public","openai/plugins","xai-org/plugin-marketplace"}
cc={p["name"]:p for p in json.load(open(os.path.join(ROOT,"mp.json")))["plugins"]}
gk={p["name"]:p for p in json.load(open(os.path.join(ROOT,"grok_mp.json")))["plugins"]}
cxm={p["name"]:p for p in json.load(open(os.path.join(MIR,".agents/plugins/marketplace.json")))["plugins"]}
def get(u,t=15,raw=False):
  r=urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=t);b=r.read(3_000_000);return (b,r.headers.get("content-type","")) if raw else b.decode("utf-8","replace")
def gh(u):
  m=re.match(r"https?://github\.com/([^/]+)/([^/#?]+?)(?:\.git)?(?:/tree/[^/]+/(.+?))?/?$",u or "");return (m[1],m[2],m[3]) if m else None
def save_img(slug,b,ct):
  if b[:5]==b"<?xml" or b"<svg" in b[:500] or "svg" in ct:
    if len(b)>60_000: return None
    p=f"{slug}.svg";open(os.path.join(LOGO,p),"wb").write(b);return p
  im=Image.open(io.BytesIO(b)).convert("RGBA");im.thumbnail((96,96),Image.LANCZOS)
  if im.width<16: return None
  p=f"{slug}.webp";im.save(os.path.join(LOGO,p),"WEBP",quality=85,method=6);return p
def favicon(site):
  try:
    h=get(site,10);best=None
    for m in re.finditer(r"<link[^>]+>",h,re.I):
      t=m[0];rel=re.search(r'rel=["\']([^"\']+)',t,re.I);hr=re.search(r'href=["\']([^"\']+)',t,re.I)
      if rel and hr and "icon" in rel[1].lower():
        sc=2 if "apple" in rel[1].lower() else 1
        if not best or sc>best[0]: best=(sc,urllib.parse.urljoin(site,html.unescape(hr[1])))
    return best[1] if best else urllib.parse.urljoin(site,"/favicon.ico")
  except Exception: return None
def meta(it):
  s=it["slug"];out={"slug":s,"logo":None,"logo_src":None,"repo":None,"stars":None,"updated":None,"readme":False}
  cands=[it.get("source_url"),(cc.get(s) or {}).get("homepage"),(gk.get(s) or {}).get("homepage")]
  src=cc.get(s,{}).get("source");cands.append(src.get("url") if isinstance(src,dict) else None);cands.append(((gk.get(s) or {}).get("source") or {}).get("url"))
  repos=[gh(u) for u in cands if u];own=[r for r in repos if r and f"{r[0]}/{r[1]}" not in MKT];mk=[r for r in repos if r and f"{r[0]}/{r[1]}" in MKT]
  repo=own[0] if own else (mk[0] if mk else None);L=[]
  if s in cxm:
    d=os.path.join(MIR,(cxm[s].get("source") or {}).get("path") or "/nonexistent")
    try:
      m=json.load(open(os.path.join(d,".codex-plugin/plugin.json"))).get("interface",{})
      for k in("logo","composerIcon"):
        if m.get(k): L.append(("file",os.path.normpath(os.path.join(d,m[k]))))
      if m.get("websiteURL"): L.append(("fav",m["websiteURL"]))
    except Exception: pass
  if own: L.append(("url",f"https://github.com/{own[0][0]}.png?size=96","GitHub org avatar"))
  elif mk and ((cc.get(s,{}).get("author") or {}).get("name","")).lower().startswith("anthropic"): L.append(("url","https://github.com/anthropics.png?size=96","GitHub org avatar"))
  for u in cands:
    if u and not gh(u) and u.startswith("http"): L.append(("fav",u))
  for x in L:
    try:
      if x[0]=="file": b=open(x[1],"rb").read();ct="svg" if x[1].endswith(".svg") else "";lab="Codex marketplace manifest"
      elif x[0]=="url": b,ct=get(x[1],15,True);lab=x[2]
      else:
        f=favicon(x[1])
        if not f: continue
        b,ct=get(f,10,True);lab="site favicon"
      p=save_img(s,b,ct)
      if p: out["logo"]=p;out["logo_src"]=lab;break
    except Exception: continue
  if repo:
    o,r,path=repo;out["repo"]=f"https://github.com/{o}/{r}"+(f"/tree/HEAD/{path}" if path else "")
    try:
      h=get(f"https://github.com/{o}/{r}")
      m=re.search(r'"stargazerCount":(\d+)',h)
      if m: out["stars"]=int(m[1])
    except Exception: pass
    try:
      r2=urllib.request.urlopen(urllib.request.Request(f"https://github.com/{o}/{r}/latest-commit/HEAD"+(f"/{path}" if path else ""),headers={**UA,"Accept":"application/json"}),timeout=15)
      out["updated"]=json.loads(r2.read()).get("date")
    except Exception: pass
    for name in ["README.md","readme.md","Readme.md"]:
      try:
        t=get(f"https://raw.githubusercontent.com/{o}/{r}/HEAD/{(path+'/') if path else ''}{name}")
        open(os.path.join(RD,f"{s}.md"),"w").write(t[:12000]);out["readme"]=True;break
      except Exception: continue
  return out
if __name__=="__main__":
  items=json.load(open(os.path.join(ROOT,"data/skills.json")))["items"]
  with cf.ThreadPoolExecutor(10) as ex: res=list(ex.map(meta,items))
  json.dump({r["slug"]:r for r in res},open(os.path.join(ROOT,"data/meta/meta.json"),"w"),indent=0)
  print({"items":len(res),"logos":sum(1 for r in res if r["logo"]),"repos":sum(1 for r in res if r["repo"]),"stars":sum(1 for r in res if r["stars"] is not None),"updated":sum(1 for r in res if r["updated"]),"readme":sum(r["readme"] for r in res)})
  from collections import Counter;print(Counter(r["logo_src"] for r in res))
