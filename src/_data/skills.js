import fs from "fs";
const raw=JSON.parse(fs.readFileSync(new URL("../../data/skills.json",import.meta.url)));
const A=["claude_code","codex","grok_build","cursor","pi"];
const merge={"developer tools":"development","observability":"monitoring","mcp (npm)":"mcp servers","learning":"education & research","scientific research":"education & research","data & analytics":"database","files":"utilities","memory":"utilities","reasoning":"utilities","web":"utilities","creativity":"design","migration":"development","location":"other","math":"other","finance":"other","business & operations":"productivity","testing":"development"};
const T={"plugin":"Plugin","mcp-server":"MCP server","npm-mcp-package":"MCP (npm)"};
export default raw.items.map(x=>{const c=(x.category||"other").toLowerCase();const docs=A.filter(a=>x.compatibility[a]==="documented");
 const w=x.name.replace(/^@[^/]+\//,"").split(/[\s\-_/]+/).filter(Boolean);
 return {...x,category:merge[c]||c,typeLabel:T[x.type]||x.type,docs,docCount:docs.length,mono:(w.length>1?w[0][0]+w[1][0]:w[0].slice(0,2)).toUpperCase(),
  featured:x.listings.length>=3};}).sort((a,b)=>a.name.replace(/^@/,"").localeCompare(b.name.replace(/^@/,""),"en",{sensitivity:"base"}));
