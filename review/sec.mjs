import {chromium} from 'playwright';const b=await chromium.launch();const R=process.argv[2];
const p=await b.newPage({viewport:{width:1440,height:900}});await p.goto('http://localhost:8080/');
for(const [y,n] of [[850,'s1'],[1700,'s2']]){await p.evaluate(y=>scrollTo(0,y),y);await p.waitForTimeout(200);await p.screenshot({path:`review/${R}/home-${n}-d.png`})}
await p.goto('http://localhost:8080/matrix/');await p.screenshot({path:`review/${R}/matrix-d.png`});
const m=await b.newPage({viewport:{width:390,height:844}});await m.goto('http://localhost:8080/');await m.evaluate(()=>scrollTo(0,1200));await m.waitForTimeout(200);await m.screenshot({path:`review/${R}/home-s1-m.png`});
await m.goto('http://localhost:8080/');await m.click('[data-open-search]');await m.waitForSelector('#pq:focus');await m.keyboard.type('postgres');await m.waitForTimeout(300);await m.screenshot({path:`review/${R}/palette-m.png`});
await b.close();
