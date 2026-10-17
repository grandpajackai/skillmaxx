import fs from "fs";const d=JSON.parse(fs.readFileSync(new URL("../../data/skills.json",import.meta.url)));
const SITE_URL=(process.env.SITE_URL||"https://grandpajackai.github.io/skillmaxx").replace(/\/$/,"");const BASE=(process.env.PATH_PREFIX??"/skillmaxx/").replace(/\/$/,"");
export default {name:"SkillMaxx",url:SITE_URL,base:BASE,checked:d.generated,
 tagline:"Every skill, plugin and MCP server install-tested in a clean sandbox and checked against official docs for Claude Code, Codex, Grok Build, Cursor and Pi, with the exact install command for each.",
 agents:["claude_code","codex","grok_build","cursor","pi"],
 ldWebsite:{"@context":"https://schema.org","@type":"WebSite","name":"SkillMaxx","url":SITE_URL,"potentialAction":{"@type":"SearchAction","target":SITE_URL+"/?q={query}","query-input":"required name=query"}},
 agentNames:{claude_code:"Claude Code",codex:"Codex",grok_build:"Grok Build",cursor:"Cursor",pi:"Pi"},
 agentColor:{claude_code:"#D97757",codex:"#9CA3AF",grok_build:"#EDEDEF",cursor:"#60A5FA",pi:"#A78BFA"}};
