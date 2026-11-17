// Build-time data for the programmatic answer pages (/works-in/<agent>/, /best/<category>/) and the
// "Does X work in <agent>?" answer on every skill page. Every number comes from the latest real nightly
// run (src/_data/latestRows.json + testing/history.json, via skills.js). Nothing here is invented.
import fs from "fs";import skills from "./skills.js";
const rd=p=>{try{return JSON.parse(fs.readFileSync(new URL(p,import.meta.url)))}catch{return null}};
const LR=rd("./latestRows.json")||{date:null,rows:[]};
const A=["claude_code","codex","grok_build","cursor","pi"];
const NAME={claude_code:"Claude Code",codex:"Codex",grok_build:"Grok Build",cursor:"Cursor",pi:"Pi"};
const SLUG={claude_code:"claude-code",codex:"codex",grok_build:"grok-build",cursor:"cursor",pi:"pi"};
const TYPES={"plugin":"plugins","skill":"Agent Skills","mcp-server":"reference MCP servers","npm-mcp-package":"npm MCP servers"};
const MIN_CAT=10;      // a category page needs at least this many add-ons that passed somewhere
const SKIP_CAT=new Set(["other"]);
const fmt=d=>{if(!d)return "";const [y,m,dd]=d.split("-").map(Number);return new Date(Date.UTC(y,m-1,dd)).toLocaleDateString("en-US",{month:"short",day:"numeric",year:"numeric",timeZone:"UTC"})};
const st={};for(const r of LR.rows)st[`${r.s}|${r.a}`]=r.st; // same statuses as /reports/latest/
const date=LR.date;const dateLabel=fmt(date);
const ANS={pass:"Yes",needs_key:"Likely, once you add your API key",broken:"No",pending:"Unclear (re-checking)",flaky:"Flaky"};
const why={pass:a=>`it installed and loaded in ${NAME[a]} in a clean sandbox with no credentials`,needs_key:a=>`it failed in ${NAME[a]} only because our keyless sandbox has no API key or account, so it should work once you add yours`,broken:a=>`the install or load check failed in ${NAME[a]} two nights running`,pending:a=>`it failed in ${NAME[a]} once and is re-checked on the next nightly run`,flaky:a=>`it has flip-flopped between pass and fail in ${NAME[a]} across recent nights`};
const list=a=>a.length<=1?a.join(""):a.slice(0,-1).join(", ")+" and "+a[a.length-1];
// per-skill answer + FAQ (only for agents we actually tested last night)
const answers={};
for(const s of skills){const rows=A.filter(a=>st[`${s.slug}|${a}`]).map(a=>({a,name:NAME[a],slug:SLUG[a],st:st[`${s.slug}|${a}`]}));
 if(!rows.length)continue;
 const yes=rows.filter(r=>r.st==="pass").map(r=>r.name),key=rows.filter(r=>r.st==="needs_key").map(r=>r.name),no=rows.filter(r=>!["pass","needs_key"].includes(r.st)).map(r=>r.name),untested=A.filter(a=>!rows.find(r=>r.a===a)).map(a=>NAME[a]);
 const parts=[];if(yes.length)parts.push(`yes in ${list(yes)}`);if(key.length)parts.push(`in ${list(key)} it needs your own API key (it failed only for lack of credentials)`);if(no.length)parts.push(`not reliably in ${list(no)}`);
 let lead=`As of ${dateLabel}: ${parts.join("; ")}.`;if(untested.length)lead+=` Not tested in ${list(untested)} (no install path we can test there yet).`;
 answers[s.slug]={lead,rows:rows.map(r=>({...r,label:ANS[r.st],q:`Does ${s.name} work in ${r.name}?`,a:`${ANS[r.st]}. In SkillMaxx's nightly install test on ${dateLabel}, ${why[r.st](r.a)}.`}))};}
// per-agent pages
const agents=A.map(a=>{const by={pass:[],needs_key:[],broken:[],pending:[],flaky:[]};
 for(const s of skills){const v=st[`${s.slug}|${a}`];if(v)by[v].push(s)}
 const tested=Object.values(by).reduce((n,x)=>n+x.length,0);
 const groups=Object.entries(TYPES).map(([t,label])=>({type:t,label,items:by.pass.filter(s=>s.type===t)})).filter(g=>g.items.length);
 return {key:a,name:NAME[a],slug:SLUG[a],tested,pass:by.pass.length,needsKey:by.needs_key,broken:by.broken,pending:[...by.pending,...by.flaky],groups,rate:tested?Math.round(by.pass.length*1000/tested)/10:0}}).filter(x=>x.tested>=10);
// per-category "best" pages: ranked by agents passed, then GitHub stars
const cats={};for(const s of skills){if(SKIP_CAT.has(s.category))continue;const ok=A.filter(a=>st[`${s.slug}|${a}`]==="pass");if(!A.some(a=>st[`${s.slug}|${a}`]))continue;
 (cats[s.category]??={key:s.category,label:s.catLabel,slug:s.category.replace(/&/g,"and").replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,""),items:[]}).items.push({s,ok,okNames:ok.map(a=>NAME[a]),stars:s.meta.stars||0})}
const categories=Object.values(cats).map(c=>{c.items.sort((x,y)=>y.ok.length-x.ok.length||y.stars-x.stars||x.s.name.localeCompare(y.s.name));c.passing=c.items.filter(i=>i.ok.length);c.perAgent=A.map(a=>({a,name:NAME[a],n:c.items.filter(i=>i.ok.includes(a)).length,t:c.items.filter(i=>st[`${i.s.slug}|${a}`]).length})).filter(x=>x.t);return c}).filter(c=>c.passing.length>=MIN_CAT).sort((a,b)=>b.passing.length-a.passing.length);
// JSON-LD (built here so it is always valid JSON)
const URL0=(process.env.SITE_URL||"https://grandpajackai.github.io/skillmaxx").replace(/\/$/,"");
const ORG={"@type":"Organization","name":"SkillMaxx","url":URL0+"/"};
const crumbs=(items)=>({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items.map(([n,u],i)=>({"@type":"ListItem","position":i+1,"name":n,"item":URL0+u}))});
const faqLd=qs=>({"@context":"https://schema.org","@type":"FAQPage","mainEntity":qs.map(f=>({"@type":"Question","name":f.q,"acceptedAnswer":{"@type":"Answer","text":f.a}}))});
const itemList=(name,items)=>({"@context":"https://schema.org","@type":"ItemList","name":name,"numberOfItems":items.length,"itemListElement":items.slice(0,100).map((s,i)=>({"@type":"ListItem","position":i+1,"name":s.name,"url":`${URL0}/skills/${s.slug}/`}))});
const dataset=(name,desc,url)=>({"@context":"https://schema.org","@type":"Dataset","name":name,"description":desc,"url":URL0+url,"dateModified":date,"temporalCoverage":date,"creator":ORG,"publisher":ORG,"isAccessibleForFree":true,"measurementTechnique":"Real install of each add-on in the agent's CLI inside a clean sandbox with no credentials, re-run nightly","distribution":{"@type":"DataDownload","encodingFormat":"application/json","contentUrl":URL0+"/index.json"}});
for(const s of skills){const x=answers[s.slug];if(x)x.ld=faqLd(x.rows)}
for(const g of agents){const u=`/works-in/${g.slug}/`,t=`Which skills, plugins and MCP servers work in ${g.name}?`;
 g.title=t;g.faqs=[
  {q:`How many agent add-ons work in ${g.name}?`,a:`In SkillMaxx's nightly install test on ${dateLabel}, ${g.pass} of ${g.tested} add-ons we tested in ${g.name} (${g.rate}%) installed and loaded in a clean sandbox with no credentials.`},
  {q:`Why do some add-ons fail in ${g.name}?`,a:`Of the ${g.tested-g.pass} that didn't pass on ${dateLabel}, ${g.needsKey.length} failed only because our keyless sandbox has no API key or account, ${g.broken.length} failed two nights running, and ${g.pending.length} were a one-night failure or flip-flopping and get re-checked on the next run.`},
  {q:`How does SkillMaxx test add-ons in ${g.name}?`,a:`Every night we run the real install command in ${g.name}'s CLI in a throwaway sandbox, then check that the add-on loads (plugins enabled, MCP servers connected with tools listed). A failure is retried once, and something is called broken only after two failing nights.`}];
 g.ld=[dataset(`${g.name} add-on compatibility (SkillMaxx nightly install tests)`,`Nightly pass/fail install results for ${g.tested} skills, plugins and MCP servers in ${g.name}.`,u),itemList(`Add-ons that installed in ${g.name} on ${dateLabel}`,g.groups.flatMap(x=>x.items)),faqLd(g.faqs),crumbs([["SkillMaxx","/"],["Works in","/works-in/"],[g.name,u]])];}
for(const c of categories){const u=`/best/${c.slug}/`;const mcp=/mcp/i.test(c.label);c.noun=mcp?"MCP servers":`${c.label.toLowerCase()} add-ons`;c.title=mcp?"Best MCP servers that actually install in coding agents (tested)":`Best ${c.label} plugins and MCP servers that actually install (tested)`;
 const top=c.passing.slice(0,3).map(i=>i.s.name);
 c.faqs=[{q:`What are the best ${c.noun} for coding agents?`,a:`Ranked by how many of 5 coding agents they installed in on ${dateLabel}, then GitHub stars, the top ${c.noun} in SkillMaxx's nightly test are ${list(top)}. ${c.passing.length} of ${c.items.length} tested ${c.noun} passed in at least one agent.`},
  ...c.perAgent.filter(p=>p.t>=3).map(p=>({q:`How many ${c.noun} work in ${p.name}?`,a:`${p.n} of ${p.t} ${c.noun} we tested in ${p.name} installed and loaded on ${dateLabel}.`}))];
 c.ld=[itemList(c.title,c.passing.map(i=>i.s)),faqLd(c.faqs),crumbs([["SkillMaxx","/"],["Best by category","/best/"],[c.label,u]])];}
export default {date,dateLabel,answers,agents,categories,agentSlug:SLUG};
