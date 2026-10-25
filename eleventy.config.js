import { EleventyHtmlBasePlugin } from "@11ty/eleventy";
export default function(c){
 c.addPlugin(EleventyHtmlBasePlugin);
 c.addPassthroughCopy({"src/assets":"assets"});c.addPassthroughCopy({"src/root":"/"});
 c.addFilter("host",u=>{try{return new URL(u).hostname.replace(/^www\./,"")}catch(e){return "Listing"}});
 c.addFilter("listingLabel",u=>/anthropics\//.test(u)?"Claude marketplace":/xai-org\//.test(u)?"Grok marketplace":/openai\//.test(u)?"Codex marketplace":/npmjs/.test(u)?"npm":(()=>{try{return new URL(u).hostname.replace(/^www\./,"")}catch(e){return "Listing"}})());
 c.addFilter("json",v=>JSON.stringify(v));
 c.addFilter("agentName",k=>({claude_code:"Claude Code",codex:"Codex",grok_build:"Grok Build",cursor:"Cursor",pi:"Pi"})[k]);
 c.addFilter("statusLabel",s=>({documented:"Verified from docs",tested:"Tested ✓",failed:"Failed",unknown:"Not yet tested"})[s]||"Not yet tested");
 c.addFilter("ago",d=>{if(!d)return "";const s=(Date.now()-new Date(d))/864e5;return s<1?"today":s<2?"yesterday":s<60?Math.round(s)+" days ago":s<730?Math.round(s/30)+" months ago":Math.round(s/365)+" years ago"});
 c.addFilter("kfmt",n=>n==null?"":n>=1000?(n/1000).toFixed(n>=10000?0:1)+"k":String(n));
 c.addFilter("day",d=>d?String(d).slice(0,10):"");
 c.addFilter("uniq",a=>[...new Set(a)]);
 c.addFilter("pluck",(a,k)=>a.map(x=>x[k]));
 c.addFilter("where",(a,k,v)=>a.filter(x=>x[k]===v));
 c.addFilter("related",(all,s)=>{const tok=t=>new Set((t||"").toLowerCase().match(/[a-z]{4,}/g)||[]);const st=tok(s.name+" "+s.description);const sc=x=>{const xt=tok(x.name+" "+x.description);let i=0;for(const w of xt)if(st.has(w))i++;return i/(st.size+xt.size-i||1)+(x.category===s.category?.15:0)+x.testedCount*.02};return all.filter(x=>x.slug!==s.slug).map(x=>[sc(x),x]).sort((a,b)=>b[0]-a[0]).slice(0,4).map(a=>a[1])});
 c.addFilter("sumDocs",a=>a.reduce((n,x)=>n+x.docCount,0));
 return {pathPrefix:process.env.PATH_PREFIX??"/skillmaxx/",dir:{input:"src",output:"_site"},htmlTemplateEngine:"njk"};
}
