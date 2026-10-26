
## From X radar 2026-10-26
- Security week for agent tooling: Anthropic open-sourced sandbox-runtime (`srt`, wrap any MCP server), NVIDIA SkillSpector (26.1% of 31,132 skills had vulns, per NVIDIA), official MCP servers v2.1.0 patched 8 vulns, the AGENTS.md-in-Downloads attack. Angle: "we install these nightly in sandboxes, here's what we saw."
- Theo's tstack: 9 skills for Claude Code + Codex. Test it across all 5 agents and report.
- Our data point: chrome-devtools-mcp passes Claude Code + Grok Build, fails in Pi (npm prepare script) as of Oct 26.
- Tip: Claude Code `/usage` shows which skills/MCPs eat quota.
- New official MCP servers: Framer, Meta Ads, Walmart.
