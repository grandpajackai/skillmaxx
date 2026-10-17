import fs from "fs";import MarkdownIt from "markdown-it";
const rd=p=>{try{return JSON.parse(fs.readFileSync(new URL(p,import.meta.url)))}catch{return {}}};
const META=rd("../../data/meta/meta.json"),HIST=rd("../../testing/history.json");
const md=new MarkdownIt({html:false,linkify:true});
const readme=(slug,repo)=>{try{let t=fs.readFileSync(new URL(`../../data/meta/readme/${slug}.md`,import.meta.url),"utf8");
 t=t.replace(/<!--[\s\S]*?-->/g,"");const lines=t.split("\n");let out=[],n=0;for(const l of lines){out.push(l);n+=l.length;if(n>2200&&l.trim()==="")break}
 const raw=repo&&repo.match(/github\.com\/([^/]+)\/([^/]+)(?:\/tree\/HEAD\/(.+))?/);
 let h=md.render(out.join("\n"));
 // drop images (remote, untrusted) and make relative links absolute to the repo
 h=h.replace(/<(\/?)h([1-6])/g,(m,c,n)=>`<${c}h${Math.min(6,+n+2)}`).replace(/<img[^>]*>/g,"").replace(/href="(?!https?:|#|mailto:)([^"]+)"/g,(m,u)=>raw?`href="https://github.com/${raw[1]}/${raw[2]}/blob/HEAD/${raw[3]?raw[3]+"/":""}${u}"`:'href="#"').replace(/<a /g,'<a rel="nofollow noopener" ');
 return {html:h,truncated:n<t.length}}catch{return null}};
const raw=JSON.parse(fs.readFileSync(new URL("../../data/skills.json",import.meta.url)));
const A=["claude_code","codex","grok_build","cursor","pi"];
const merge={"developer tools":"development","observability":"monitoring","mcp (npm)":"mcp servers","learning":"education & research","scientific research":"education & research","data & analytics":"database","files":"utilities","memory":"utilities","reasoning":"utilities","web":"utilities","creativity":"design","migration":"development","location":"other","math":"other","finance":"other","business & operations":"productivity","testing":"development"};
const T={"plugin":"Plugin","mcp-server":"MCP server","npm-mcp-package":"MCP (npm)"};
export default raw.items.map(x=>{const c=(x.category||"other").toLowerCase();const docs=A.filter(a=>x.compatibility[a]==="documented");
 const w=x.name.replace(/^@[^/]+\//,"").split(/[\s\-_/]+/).filter(Boolean);
 const m={...(META[x.slug]||{})};if(m.repo&&/github\.com\/(anthropics\/claude-plugins-(official|public)|openai\/plugins|xai-org\/plugin-marketplace)\b/.test(m.repo))m.stars=null;const test={},eff={};for(const a of A){const h=HIST[`${x.slug}|${a}`];if(h&&h.length){const l=h[h.length-1];test[a]={status:l.status,at:l.at,log:l.log,history:h.slice(-10)}}eff[a]=test[a]?(test[a].status==='pass'?'tested':'failed'):x.compatibility[a]}
 const tested=A.filter(a=>eff[a]==='tested');const install={...x.install};if(test.pi&&test.pi.status==='pass'&&!install.pi){const g=(x.source_url||'').match(/github\.com\/([^/]+)\/([^/#?]+)/);if(g)install.pi=`pi install git:github.com/${g[1]}/${g[2].replace(/\.git$/,'')}`}
 return {...x,install,meta:m,logo:m.logo?('/assets/logos/'+m.logo):null,test,eff,tested,testedCount:tested.length,readme:m.readme?readme(x.slug,m.repo):null,category:merge[c]||c,catLabel:(merge[c]||c).replace(/\b\w/g,m=>m.toUpperCase()).replace(/\bMcp\b/,"MCP").replace(/\bAi\b/,"AI").replace(/\bApi\b/,"API"),typeLabel:T[x.type]||x.type,docs,docCount:docs.length,mono:(w.length>1?w[0][0]+w[1][0]:w[0].slice(0,2)).toUpperCase(),
  featured:x.listings.length>=3};}).sort((a,b)=>a.name.replace(/^@/,"").localeCompare(b.name.replace(/^@/,""),"en",{sensitivity:"base"}));
