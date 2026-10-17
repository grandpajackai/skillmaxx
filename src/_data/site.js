import fs from "fs";const d=JSON.parse(fs.readFileSync(new URL("../../data/skills.json",import.meta.url)));
export default {name:"SkillMaxx",url:"https://skillmaxx.dev",checked:d.generated,
 tagline:"Every skill, plugin and MCP server checked against official docs for Claude Code, Codex, Grok Build, Cursor and Pi, with the right install command for each.",
 agents:["claude_code","codex","grok_build","cursor","pi"],
 ldWebsite:{"@context":"https://schema.org","@type":"WebSite","name":"SkillMaxx","url":"https://skillmaxx.dev","potentialAction":{"@type":"SearchAction","target":"https://skillmaxx.dev/?q={query}","query-input":"required name=query"}},
 agentNames:{claude_code:"Claude Code",codex:"Codex",grok_build:"Grok Build",cursor:"Cursor",pi:"Pi"},
 agentColor:{claude_code:"#D97757",codex:"#9CA3AF",grok_build:"#EDEDEF",cursor:"#60A5FA",pi:"#A78BFA"}};
