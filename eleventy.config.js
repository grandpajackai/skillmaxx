export default function(c){
 c.addPassthroughCopy({"src/assets":"assets"});
 c.addFilter("host",u=>{try{return new URL(u).hostname.replace(/^www\./,"")}catch(e){return "Listing"}});
 c.addFilter("listingLabel",u=>/anthropics\//.test(u)?"Claude marketplace":/xai-org\//.test(u)?"Grok marketplace":/openai\//.test(u)?"Codex marketplace":/npmjs/.test(u)?"npm":(()=>{try{return new URL(u).hostname.replace(/^www\./,"")}catch(e){return "Listing"}})());
 c.addFilter("json",v=>JSON.stringify(v));
 c.addFilter("agentName",k=>({claude_code:"Claude Code",codex:"Codex",grok_build:"Grok Build",cursor:"Cursor",pi:"Pi"})[k]);
 c.addFilter("statusLabel",s=>s==="documented"?"Verified from docs":s==="tested"?"Tested":"Not yet tested");
 c.addFilter("uniq",a=>[...new Set(a)]);
 c.addFilter("pluck",(a,k)=>a.map(x=>x[k]));
 c.addFilter("where",(a,k,v)=>a.filter(x=>x[k]===v));
 c.addFilter("related",(all,s)=>all.filter(x=>x.category===s.category&&x.slug!==s.slug).sort((a,b)=>b.docCount-a.docCount).slice(0,4));
 c.addFilter("sumDocs",a=>a.reduce((n,x)=>n+x.docCount,0));
 return {dir:{input:"src",output:"_site"},htmlTemplateEngine:"njk"};
}
