export default function(c){
 c.addPassthroughCopy({"src/assets":"assets"});
 c.addFilter("json",v=>JSON.stringify(v));
 c.addFilter("agentName",k=>({claude_code:"Claude Code",codex:"Codex",grok_build:"Grok Build",cursor:"Cursor",pi:"Pi"})[k]);
 return {dir:{input:"src",output:"_site"},htmlTemplateEngine:"njk"};
}
