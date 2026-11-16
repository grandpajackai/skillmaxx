// Nights with no published daily report, so /reports/<date>/ never 404s for them.
// Explicit notes come from runNotes.json (no_valid_run: the run finished but a harness bug broke it;
// no_report: the run stopped or never produced results). Any other missing date from gap_notes_from
// up to yesterday (America/New_York) or the latest report gets default_no_report automatically.
import fs from "fs";
const rd=(p,d)=>{try{return JSON.parse(fs.readFileSync(new URL(p,import.meta.url)))}catch{return d}};
const reports=rd("./reports.json",[]),notes=rd("./runNotes.json",{});
const have=new Set(reports.map(r=>r.date));
const explicit=new Map();
for(const n of notes.no_valid_run||[])explicit.set(n.date,{date:n.date,why:n.why,kind:"no_valid_run"});
for(const n of notes.no_report||[])explicit.set(n.date,{date:n.date,why:n.why,kind:"no_report"});
const fmt=d=>d.toISOString().slice(0,10);
const etToday=new Intl.DateTimeFormat("en-CA",{timeZone:"America/New_York",year:"numeric",month:"2-digit",day:"2-digit"}).format(new Date());
const y=new Date(etToday+"T00:00:00Z");y.setUTCDate(y.getUTCDate()-1);
const latest=reports.map(r=>r.date).sort().pop()||fmt(y);
const end=[fmt(y),latest].sort().pop();
const gaps=[];
if(notes.gap_notes_from){
 for(const d=new Date(notes.gap_notes_from+"T00:00:00Z");fmt(d)<=end;d.setUTCDate(d.getUTCDate()+1)){
  const s=fmt(d);if(have.has(s))continue;
  gaps.push(explicit.get(s)||{date:s,why:notes.default_no_report||"No report this night.",kind:"no_report",auto:true});
 }
}
for(const [s,g] of explicit)if(!have.has(s)&&!gaps.some(x=>x.date===s))gaps.push(g);
gaps.sort((a,b)=>a.date<b.date?1:-1);
const sorted=reports.map(r=>r.date).sort();
for(const g of gaps){g.prev=sorted.filter(d=>d<g.date).pop()||null;g.next=sorted.find(d=>d>g.date)||null}
export default gaps;
