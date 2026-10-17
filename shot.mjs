import {chromium} from 'playwright';
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1366,height:900}});
for(const [u,f] of [['/','home'],['/skills/github/','skill-github'],['/matrix/','matrix']]){await p.goto('http://localhost:8080'+u);await p.screenshot({path:`shots/${f}.png`,fullPage:true});}
await b.close();
