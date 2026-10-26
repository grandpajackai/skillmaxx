import {chromium} from 'playwright';
const b=await chromium.launch();const c=await b.newContext({viewport:{width:390,height:844},bypassCSP:false});const p=await c.newPage();
const net=[];p.on('response',async r=>{const u=r.url();if(/beehiiv/.test(u))net.push([r.status(),u.slice(0,110),r.headers()['cache-control'],r.headers()['age'],r.headers()['cf-cache-status'],r.headers()['last-modified']].join(' | '))});
await p.goto('https://skillmaxx.gilventures.ai/?nc='+Date.now()+'#newsletter',{waitUntil:'networkidle'});await p.waitForTimeout(5000);
const el=await p.$('#newsletter');await el.scrollIntoViewIfNeeded();const out=process.argv[2];await el.screenshot({path:out});
console.log(JSON.stringify(await p.evaluate(()=>{const f=document.querySelector('.bhf iframe');const r=f.getBoundingClientRect();return {w:r.width,h:r.height,src:f.src}})));
for(const f of p.frames()){if(/beehiiv/.test(f.url())){try{console.log('frame',await f.evaluate(()=>{const i=document.querySelector('input[type=email]');const h=document.querySelector('h1,h2,h3,p');return {iw:i&&i.getBoundingClientRect().width,hfs:h&&getComputedStyle(h).fontSize,ht:h&&h.textContent.slice(0,40)}}))}catch(e){}}}
console.log(net.join('\n'));await b.close();
