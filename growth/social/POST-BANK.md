# Post bank v2 (voice-checked, numbers from 2026-10-26 run). Drafts, nothing queued.
X ≤280 / Bluesky ≤300. Same text works on both unless noted.

1. **Tip** — In Claude Code it's `/plugin install sentry@claude-plugins-official`. The @marketplace bit isn't decoration: same names now live in 2+ marketplaces and agents will ask "which one?". Pin it and move on.
2. **Tip** — Cursor MCP: add the server under mcpServers in ~/.cursor/mcp.json, then check it says "ready". Anything else means not ready. Cursor is very literal. (We grade on exactly that line.)
3. **Data** — Last night's installs by agent: Codex 65/65, Claude Code 94%, Grok Build 94%, Pi 66%, Cursor 61% (keyless). Not a ranking of agents, a ranking of how well the ecosystem ships for each one. skillmaxx.gilventures.ai/reports/latest/
4. **Honesty** — New rule: we only call an install "broken" after it fails two nights in a row. 13 add-ons flip-flopped this week. We used to shout about those. Now we label them flaky and shut up about it.
5. **Honesty** — 12 installs "failed" last night only because our sandbox has no API keys. That's not broken, that's shy. We list them separately now so nobody gets blamed for our missing keys.
6. **Feedback ask** — We're brand new and testing 424 agent add-ons a night. Real question: what's the one skill or MCP server you'd want checked before you install it? Reply and we'll run it through all 5 agents.
7. **How we test** — Fresh sandbox, real agent CLI, no credentials. "Pass" = the agent itself lists it as installed (or connected, for MCP). Every result links its log. If we got yours wrong, tell us, we'll rerun it. skillmaxx.gilventures.ai/how-we-test/
8. **Standout** — Superpowers installed clean in 4 agents with zero flakes this week. Stars don't prove installs. Two clean nights in a row do. skillmaxx.gilventures.ai/skills/superpowers/
9. **Tool authors** — Listed for one agent but quietly work in three? Most skills do. Submit yours and we'll show you the logs for Claude Code, Codex, Grok Build, Cursor and Pi, good or bad. skillmaxx.gilventures.ai/submit/
10. **Reference servers** — The official MCP reference servers (fetch, filesystem, git, memory, time) are still the backbone of most setups. Boring is a feature. They're tested every night too.
11. **Safe-today** — Before you install something into your agent: skillmaxx.gilventures.ai/reports/latest/ has an "is it safe to install today?" box. Type the tool, pick your agent. Tell us if it's useful or if we should kill it.
12. **Weekly scorecard (Sun)** — Week 44 install scorecard: 802/890 clean (90.1%). Confirmed broke: 1 add-on (2 installs). Really fixed: 0. Flaky noise we refused to count: 13. Most reliable: Codex. What should we add next week? skillmaxx.gilventures.ai/reports/week/2026-44/
   *(Regenerate numbers Sunday from weekly_scorecard.py.)*
