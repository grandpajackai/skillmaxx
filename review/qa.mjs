import {chromium} from 'playwright';import fs from 'fs';
const R=process.argv[2]||'r1';fs.mkdirSync(`review/${R}`,{recursive:true});
const axe=fs.readFileSync('node_modules/axe-core/axe.min.js','utf8');
const b=await chromium.launch();const base='http://localhost:8080';
const P=[['/','home'],['/skills/sentry/','skill'],['/matrix/','matrix'],['/how-it-works/','how'],['/submit/','submit'],['/advertise/','advertise'],['/reports/','reports'],['/reports/2026-10-26/','report'],['/404.html','404']];
const errs=[],ax={};
for(const [w,h,s] of [[1440,900,'d'],[390,844,'m']]){const c=await b.newContext({viewport:{width:w,height:h},deviceScaleFactor:1});const p=await c.newPage();
p.on('console',m=>{if(m.type()==='error')errs.push(p.url()+' '+m.text())});p.on('pageerror',e=>errs.push(p.url()+' PAGEERR '+e.message));
for(const [u,f] of P){const r=await p.goto(base+u,{waitUntil:'networkidle'});await p.waitForTimeout(300);
await p.screenshot({path:`review/${R}/${f}-${s}.png`});await p.screenshot({path:`review/${R}/${f}-${s}-full.png`,fullPage:true});
const ow=await p.evaluate(()=>document.documentElement.scrollWidth);if(ow>w)errs.push(`${u} overflow ${ow} at ${w}`);
if(s==='d'){await p.addScriptTag({content:axe});const res=await p.evaluate(async()=>(await axe.run({runOnly:['wcag2a','wcag2aa','best-practice']})).violations.map(v=>`${v.id}(${v.impact}) x${v.nodes.length}: ${v.nodes.slice(0,2).map(n=>n.target.join(' ')).join(' | ')}`));ax[u]=res;
const seo=await p.evaluate(()=>({t:document.title,d:document.querySelector('meta[name=description]')?.content,h1:document.querySelectorAll('h1').length,can:document.querySelector('link[rel=canonical]')?.href,og:!!document.querySelector('meta[property="og:image"]'),lang:document.documentElement.lang}));console.log(u,r.status(),JSON.stringify(seo));}}
await c.close();}
// crawl
const seen=new Set(['/']),q=['/'],bad=[];const c=await b.newContext();const p=await c.newPage();
while(q.length){const u=q.shift();const r=await p.request.get(base+u);if(r.status()>=400){bad.push(u+' '+r.status());continue}
if(!(r.headers()['content-type']||'').includes('html'))continue;const html=await r.text();
for(const m of html.matchAll(/(?:href|src)="([^"#]+)/g)){let l=m[1];if(l.startsWith('http')&&!l.startsWith(base))continue;l=l.replace(base,'');if(!l.startsWith('/'))continue;if(!seen.has(l)){seen.add(l);q.push(l)}}}
console.log('crawled',seen.size,'broken',bad);console.log('console',errs.slice(0,20));console.log('axe',JSON.stringify(ax,null,1));await b.close();
