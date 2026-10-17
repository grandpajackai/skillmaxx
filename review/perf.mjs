import {chromium} from 'playwright';const b=await chromium.launch();
for(const u of ['/','/skills/sentry/','/matrix/']){const c=await b.newContext({viewport:{width:390,height:844}});const p=await c.newPage();const cdp=await c.newCDPSession(p);
await cdp.send('Network.emulateNetworkConditions',{offline:false,latency:150,downloadThroughput:1.6e6/8,uploadThroughput:7.5e5/8});await cdp.send('Emulation.setCPUThrottlingRate',{rate:4});
let bytes=0;p.on('response',async r=>{try{bytes+=(await r.body()).length}catch{}});
await p.goto('http://localhost:8080'+u,{waitUntil:'load'});
const m=await p.evaluate(()=>new Promise(res=>{new PerformanceObserver(l=>{const e=l.getEntries();res({lcp:Math.round(e[e.length-1].startTime),fcp:Math.round(performance.getEntriesByName('first-contentful-paint')[0]?.startTime),cls:0,dom:document.querySelectorAll('*').length})}).observe({type:'largest-contentful-paint',buffered:true})}));
const cls=await p.evaluate(()=>new Promise(r=>{let s=0;new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)s+=e.value}).observe({type:'layout-shift',buffered:true});setTimeout(()=>r(s.toFixed(3)),500)}));
console.log(u,JSON.stringify({...m,cls,kb:Math.round(bytes/1024)}));await c.close()}await b.close();
