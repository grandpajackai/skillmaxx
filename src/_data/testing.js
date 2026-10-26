import fs from "fs";
const dir=new URL("../../testing/results/",import.meta.url);
let f=[];try{f=fs.readdirSync(dir).filter(x=>x.endsWith(".json")).sort()}catch{}
const last=f.length?JSON.parse(fs.readFileSync(new URL(f[f.length-1],dir))):null;
const by={};if(last)for(const r of last.results){by[r.agent]??={pass:0,fail:0};by[r.agent][r.status]++}
const total=last?.results.length||0,pass=last?.results.filter(r=>r.status==="pass").length||0;
export default {runAt:last?.run_at||null,runDate:last?.run_at?last.run_at.slice(0,10):null,versions:last?.versions||{},by,total,pass,fail:total-pass,
 addons:last?new Set(last.results.map(r=>r.slug)).size:0,runs:f.length};
