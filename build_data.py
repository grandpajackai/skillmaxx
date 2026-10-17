import json,re,urllib.request,concurrent.futures as cf
A=["claude_code","codex","grok_build","cursor","pi"]
CC_MP="https://github.com/anthropics/claude-plugins-official";CX_MP="https://github.com/openai/plugins";GK_MP="https://github.com/xai-org/plugin-marketplace"
CC_DOC="https://code.claude.com/docs/en/discover-plugins";CX_DOC="https://developers.openai.com/codex/plugins";GK_DOC="https://x.ai/news/grok-plugin-marketplace";GK_AUTO="https://docs.x.ai/build/features/skills-plugins-marketplaces"
CC_MCP="https://docs.anthropic.com/en/docs/claude-code/mcp";CX_MCP="https://developers.openai.com/codex/mcp";CU_MCP="https://cursor.com/docs/context/mcp"
NAMES={"github":"GitHub","gitlab":"GitLab","posthog":"PostHog","mongodb":"MongoDB","clickhouse":"ClickHouse","hubspot":"HubSpot","huggingface":"Hugging Face","duckdb":"DuckDB","coderabbit":"CodeRabbit","sonarqube":"SonarQube","planetscale":"PlanetScale","pyright-lsp":"Pyright LSP","typescript-lsp":"TypeScript LSP","context7":"Context7","firebase":"Firebase","devtools":"DevTools","chrome-devtools":"Chrome DevTools","api":"API","mcp":"MCP","ios":"iOS","macos":"macOS","ai":"AI","sdk":"SDK","lsp":"LSP","sql":"SQL","aws":"AWS","gcp":"GCP","ui":"UI","dev":"Dev","cli":"CLI","pr":"PR","n8n":"n8n","openai":"OpenAI","dbt":"dbt","css":"CSS","html":"HTML"}
def disp(slug,given=None):
  if given and given!=slug and not given.islower(): return given
  if slug in NAMES: return NAMES[slug]
  return " ".join(NAMES.get(w,w.capitalize()) for w in re.split(r"[-_]",slug))
def key(s): return re.sub(r"[^a-z0-9]","",s.lower().replace("-official",""))
def empty(): return {"install":{a:None for a in A},"compatibility":{a:"unknown" for a in A},"compat_sources":{a:None for a in A},"listings":[]}
items={}
def get(slug,name=None):
  k=key(slug)
  if k not in items: items[k]={"slug":slug,"name":disp(slug,name),"description":"","source_url":None,"category":"other","type":"plugin",**empty()}
  return items[k]
def setc(it,a,cmd,src):
  it["install"][a]=cmd;it["compatibility"][a]="documented";it["compat_sources"][a]=src
cc=json.load(open("mp.json"))["plugins"]
for p in cc:
  n=p["name"];it=get(n,p.get("displayName"))
  it["description"]=it["description"] or p.get("description","")[:300]
  s=p.get("source");it["source_url"]=it["source_url"] or p.get("homepage") or (s.get("url") if isinstance(s,dict) else f"{CC_MP}/tree/main/{str(s).lstrip('./')}")
  it["category"]=(p.get("category") or it["category"]).lower();it["listings"].append(CC_MP)
  setc(it,"claude_code",f"/plugin install {n}@claude-plugins-official",CC_DOC)
  # Grok Build docs: auto-reads Claude Code plugins
  if not it["install"]["grok_build"]:
    it["compatibility"]["grok_build"]="documented";it["compat_sources"]["grok_build"]=GK_AUTO;it["install"]["grok_build"]="Auto-loaded from your Claude Code plugins (no extra setup per xAI docs)"
g=json.load(open("grok_mp.json"))["plugins"]
for p in g:
  n=p["name"];it=get(n,p.get("displayName"))
  it["description"]=it["description"] or p.get("description","")[:300]
  it["source_url"]=it["source_url"] or p.get("homepage") or f"{GK_MP}/tree/main/plugins/{n}"
  if it["category"]=="other": it["category"]=(p.get("category") or "other").lower()
  it["listings"].append(GK_MP);setc(it,"grok_build",f"grok plugin install {n} --trust",GK_DOC)
cx=json.load(open("codex_mp.json"))["plugins"]
def man(p):
  path=p["source"].get("path","").lstrip("./")
  for f in [".codex-plugin/plugin.json"]:
    try: return p,json.load(urllib.request.urlopen(f"https://raw.githubusercontent.com/openai/plugins/main/{path}/{f}",timeout=15))
    except Exception: return p,{}
with cf.ThreadPoolExecutor(16) as ex: res=list(ex.map(man,cx))
for p,m in res:
  n=p["name"];iface=m.get("interface",{}) if isinstance(m.get("interface"),dict) else {}
  it=get(n,iface.get("displayName"))
  it["description"]=it["description"] or (m.get("description") or iface.get("shortDescription") or "")[:300]
  it["source_url"]=it["source_url"] or f"{CX_MP}/tree/main/{p['source'].get('path','').lstrip('./')}"
  if it["category"]=="other": it["category"]=(p.get("category") or "other").lower()
  it["listings"].append(CX_MP);setc(it,"codex",f"codex plugin add {n}@openai-curated",CX_DOC)
# MCP reference servers (generic client syntax documented by each client)
old=json.load(open("data/skills.json"))["items"]
for o in old:
  if o["type"]=="mcp-server":
    it=get(o["slug"],o["name"]);it.update(name=o["name"],description=o["description"],source_url=o["source_url"],category=o["category"],type="mcp-server")
    it["listings"].append("https://github.com/modelcontextprotocol/servers")
    for a,src in [("claude_code",CC_MCP),("codex",CX_MCP),("cursor",CU_MCP)]: setc(it,a,o["install"][a],src)
# npm MCP packages: commands shown, status unknown (per-package not verified)
npm=json.load(open("npm.json"))["objects"];added=0
for o in npm:
  pk=o["package"];n=pk["name"]
  if added>=45 or not pk.get("description") or not pk.get("links",{}).get("repository"): continue
  if not re.search(r"mcp",n+pk["description"],re.I) or re.search(r"sdk|transport|core|react|framework|library|types",n+" "+pk["description"],re.I): continue
  slug=n.replace("@","").replace("/","-");
  if key(slug) in items: continue
  it=get(slug);it.update(name=n,description=pk["description"][:300],source_url=pk["links"]["repository"],category="mcp (npm)",type="npm-mcp-package")
  it["listings"].append(f"https://www.npmjs.com/package/{n}")
  run=f"npx -y {n}";short=slug.split("-")[-1][:20]
  it["install"].update(claude_code=f"claude mcp add {short} -- {run}",codex=f"codex mcp add {short} -- {run}",cursor=f'~/.cursor/mcp.json → {{"mcpServers":{{"{short}":{{"command":"npx","args":["-y","{n}"]}}}}}}')
  it["notes"]="Commands use each client's generic MCP stdio syntax; this package's npx entrypoint is not verified, so status stays unknown. Check the README for required env vars/args."
  added+=1
for it in items.values():
  it["listing_url"]=it["listings"][0];it.setdefault("notes","")
  if it["compatibility"]["grok_build"]=="documented" and it["compat_sources"]["grok_build"]==GK_AUTO: it["notes"]=(it["notes"]+" Grok Build status relies on xAI docs saying Grok reads Claude Code plugins automatically.").strip()
out=sorted(items.values(),key=lambda x:x["name"].lower())
json.dump({"generated":"2026-10-16","status_legend":{"documented":"official source (compat_sources[agent]) publishes the install method; NOT tested by SkillMaxx","unknown":"no official per-item documentation found"},"sources":[CC_MP,CX_MP,GK_MP,"https://github.com/modelcontextprotocol/servers","https://registry.npmjs.org (keywords:mcp-server)",CC_DOC,CX_DOC,GK_DOC,GK_AUTO,CC_MCP,CX_MCP,CU_MCP],"items":out},open("data/skills.json","w"),indent=1)
from collections import Counter
print(len(out),{a:sum(i["compatibility"][a]=="documented" for i in out) for a in A},Counter(i["type"] for i in out))
bad=[i["slug"] for i in out for a in A if i["compatibility"][a]=="documented" and not i["compat_sources"][a]];print("missing src",bad)
