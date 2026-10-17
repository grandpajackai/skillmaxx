import {chromium,devices} from 'playwright';
const b=await chromium.launch();
const go=async(ctxo,pages,suf)=>{const c=await b.newContext(ctxo);const p=await c.newPage();for(const [u,f] of pages){await p.goto('http://localhost:8080'+u,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);await p.screenshot({path:`shots/${f}-${suf}.png`,fullPage:true});}await c.close();};
const P=[['/','home'],['/skills/sentry/','skill-sentry'],['/matrix/','matrix'],['/how-it-works/','how-it-works']];
await go({viewport:{width:1440,height:900}},P,'desktop');
await go({...devices['iPhone 13']},P,'mobile');
const c=await b.newContext({viewport:{width:1440,height:900}});const p=await c.newPage();await p.goto('http://localhost:8080/');await p.click('.ag[data-agent=codex]');await p.waitForTimeout(200);await p.screenshot({path:'shots/home-picker-codex-desktop.png'});
const m=await b.newContext({...devices['iPhone 13']});const q=await m.newPage();await q.goto('http://localhost:8080/#browse');await q.click('#fopen');await q.waitForTimeout(400);await q.screenshot({path:'shots/filters-sheet-mobile.png'});
await b.close();
