import fs from "fs";
const d=JSON.parse(fs.readFileSync(new URL("../../data/skills.json",import.meta.url)));
export default d.items.map(x=>({...x,category:(x.category||"other").toLowerCase()})).sort((a,b)=>a.name.localeCompare(b.name));
