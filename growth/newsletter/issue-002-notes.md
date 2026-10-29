# SkillMaxx Weekly #2: notes (draft, not sent)

Sends Tuesday. The daily report is web-only; this weekly email is the only email subscribers get.

## Template: Weekly scorecard section
Generate it from real data right before sending (never type numbers by hand):

```bash
python3 testing/weekly_scorecard.py            # last 7 days ending at the latest run
python3 testing/weekly_scorecard.py 2026-11-02 # week ending on a given date
```

It covers: pass rate trend, most fixed, most broken, flaky (broke and fixed in the same week), standout of the week, per-agent results and the most reliable agent, plus a link to /reports/.

## Preview (data through 2026-10-26, only 2 runs so far; regenerate before sending)

## Weekly scorecard (2026-10-25 to 2026-10-26, 2 nightly runs)

**Pass rate trend:** 10-25 795/902 (88.1%) → 10-26 802/902 (88.9%)
**Most fixed:** none (0 installs fixed this week)
**Most broken:** [gdharness](https://skillmaxx.gilventures.ai/skills/gdharness/) ×2, [@putervision/vision-memory-mcp](https://skillmaxx.gilventures.ai/skills/putervision-vision-memory-mcp/) ×1, [Expo](https://skillmaxx.gilventures.ai/skills/expo/) ×1, [MCP git (reference)](https://skillmaxx.gilventures.ai/skills/mcp-git/) ×1, [Mergify](https://skillmaxx.gilventures.ai/skills/mergify/) ×1 (9 installs newly broke this week)
**Flaky (broke and fixed in the same week, worth a retry before blaming):** @cyanheads/pubmed-mcp-server, Airwallex Dev, Alloydb Omni, Claude Code Setup, Claude Security, Clay, Dash0, Data Engineering, Pydantic AI, Qodo, UI Theme Designer, Ui5 Modernization, Valtown
**Standout of the week:** [Qodo](https://skillmaxx.gilventures.ai/skills/qodo/), clean in 4 agents. Bring Qodo's codebase intelligence, coding standards, and code review into your coding agent.
**Per-agent (latest run):** Codex 65/65 (100.0%) · Grok Build 313/331 (94.6%) · Claude Code 340/367 (92.6%) · Pi 57/87 (65.5%) · Cursor 27/52 (51.9%)
**Most reliable agent this week:** Codex

Every night's full results: https://skillmaxx.gilventures.ai/reports/

## Other sections (carry over from #1)
- New this week, docs changes, one guide link, sponsor slot.

## From X radar 2026-10-28
- Claude Code official marketplace hit 315 entries; our Oct 28 nightly: 311/315 installed+enabled clean in Claude Code (report /reports/2026-10-28/).
- Security-scanner wave: safemcp (MCP config audit), NVIDIA SkillSpector (31,132 skills analyzed, 26.1% with ≥1 vulnerability, 5.2% likely malicious per Liu et al. 2026), Forever Security writeup on a prompt-injected MCP server landing in Codex's machine-wide config. Angle: install-clean isn't the same as safe; pin versions.
- Version bumps: Claude Code 2.1.311 (subagents can use late-connecting MCP servers), Grok Build 1.0.72 (50% context cut for FastMCP tools).
- New official MCP servers: Tempo, Podbean, Ikiform, BugTape.
- New skills to test: PGX DB Agent Skill, Hallmark, UI Craft Skills.
