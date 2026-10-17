import {chromium} from 'playwright';const base=process.argv[2];const root=new URL(base).origin;const pre=new URL(base).pathname;
const b=await chromium.launch();const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
const fails=[];p.on('response',r=>{if(r.status()>=400)fails.push(r.status()+' '+r.url())});
await p.goto(base,{waitUntil:'networkidle'});const fonts=await p.evaluate(async()=>{await document.fonts.ready;return [...document.fonts].filter(f=>f.status==='loaded').length});
await p.click('.ag[data-agent=codex]');await p.waitForTimeout(500);const q=await p.textContent('#grid .card:not([hidden]) .quick code').catch(()=>null);
await p.keyboard.press('Control+k');await p.fill('#pq','sentry');await p.keyboard.press('Enter');await p.waitForURL(/skills/);const palUrl=p.url();
await p.goto(base+'matrix/',{waitUntil:'networkidle'});
// crawl
const seen=new Set([pre]),Q=[pre],bad=[];while(Q.length){const u=Q.shift();const r=await p.request.get(root+u);if(r.status()>=400){bad.push(u+' '+r.status());continue}
 if(!(r.headers()['content-type']||'').includes('html'))continue;const h=await r.text();for(const m of h.matchAll(/(?:href|src)="([^"#?]+)/g)){let l=m[1];if(l.startsWith('http')){if(!l.startsWith(root))continue;l=l.slice(root.length)}if(!l.startsWith('/'))continue;if(!seen.has(l)){seen.add(l);Q.push(l)}}}
const outside=[...seen].filter(u=>!u.startsWith(pre));
console.log(JSON.stringify({fontsLoaded:fonts,quickCmd:q,palUrl,crawled:seen.size,broken:bad,outsidePrefix:outside,respFails:fails,errs}));await b.close();
