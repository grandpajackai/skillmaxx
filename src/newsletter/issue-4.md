---
layout: base.njk
title: "SkillMaxx #4: 831 of 1,085 agent add-on installs passed"
desc: "Issue #4 of SkillMaxx Weekly: 831 of 1,085 installs of skills, plugins and MCP servers passed on Nov 22, 2026. 5 fixed, 68 broke, 31 flaky."
permalink: /newsletter/issue-4/
ogType: article
issue: 4
issueDate: "2026-11-22"
date: 2026-11-22
tags: issues
week: "2026-47"
jsonld: {"@context": "https://schema.org", "@type": "Article", "headline": "SkillMaxx #4: 831 of 1,085 agent add-on installs passed", "datePublished": "2026-11-22", "author": {"@type": "Organization", "name": "SkillMaxx"}, "publisher": {"@type": "Organization", "name": "SkillMaxx"}, "image": "https://skillmaxx.gilventures.ai/assets/newsletter/skillmaxx-banner-1200x300.png"}
---
<div class="wrap prose nlissue">
<p class="crumbs"><a href="/">SkillMaxx</a> / <a href="/newsletter/">Newsletter</a> / Issue #4</p>
<h1 class="ph">SkillMaxx #4: 831 of 1,085 agent add-on installs passed</h1>
<p class="lead">831 of 1,085 installs passed on Nov 22. <span class="muted">Test data from Nov 17 to Nov 22, 2026.</span></p>

![SkillMaxx](/assets/newsletter/skillmaxx-banner-1200x300.png)

## hey, Brandon here 👋

This week we ran 6 nightly install tests (Nov 17 to Nov 22) of agent skills, plugins and MCP servers in Claude Code, Codex, Grok Build, Cursor and Pi. On the latest night, 77.7% of the installs we can judge without an API key passed. That's down from 87.1% on Nov 14 (9.4 points).

**5** add-ons started working, **68** broke (failed two nights running) and **31** flipped between pass and fail.

This issue is put together automatically from our nightly test logs, and every number links to the report it came from.

## 📊 This week's numbers (Nov 22)

**831 of 1,085 installs passed** (77.7% of the 1,070 we can judge without an API key).

Night by night: Nov 17 911/1,075 · Nov 18 912/1,075 · Nov 19 906/1,075 · Nov 20 906/1,075 · Nov 21 862/1,085 · Nov 22 831/1,085.

**By agent on Nov 22** (installs we can judge without an API key; 3 per agent need a key):

| Agent | Passed | Rate |
|---|---|---|
| Claude Code | 329 / 371 | 88.7% |
| Grok Build | 341 / 386 | 88.3% |
| Codex | 79 / 119 | 66.4% |
| Pi | 68 / 140 | 48.6% |
| Cursor | 14 / 54 | 25.9% |

**Standout:** [MCP time (reference)](/skills/mcp-time/) installed clean in all 5 agents this week with no flakes. Time and timezone conversion.

**Fixed:** [@putervision/vision-memory-mcp](/skills/putervision-vision-memory-mcp/), [Desktop Commander](/skills/desktop-commander/), [Hyperframes](/skills/hyperframes/), [Monday Crm](/skills/monday-crm/) and 1 more. **Broke:** [@bitbonsai/mcpvault](/skills/bitbonsai-mcpvault/), [@next-ai-drawio/mcp-server](/skills/next-ai-drawio-mcp-server/), [korean-law-mcp](/skills/korean-law-mcp/), [@putervision/vision-memory-mcp](/skills/putervision-vision-memory-mcp/), [aiterm-mcp](/skills/aiterm-mcp/) and 63 more. **Flaky:** [mcp-local-rag](/skills/mcp-local-rag/), [comfyui-mcp](/skills/comfyui-mcp/), [@ironbee-ai/devtools](/skills/ironbee-ai-devtools/), [Hyperframes](/skills/hyperframes/), [@rate-api/mcp](/skills/rate-api-mcp/) and 26 more.

Full report: [skillmaxx.gilventures.ai/reports/2026-11-22/](/reports/2026-11-22/) · Week chart: [skillmaxx.gilventures.ai/reports/week/2026-47/](/reports/week/2026-47/) · Is your tool safe today? [skillmaxx.gilventures.ai/reports/latest/](/reports/latest/)

## 📝 On the blog

- Wednesday: [Mid-week check, Nov 19: 906 of 1,075 agent add-on installs passed](/blog/midweek-2026-47/)
- Sunday: [Agent add-on installs, week of Nov 16, 2026: 831 of 1,070 passed](/blog/week-2026-47/)

## 👀 On our radar (not tested by us yet)

- [How the Claude Code team thinks about verification](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/) (297 pts, [HN](https://news.ycombinator.com/item?id=50529612))
- [Tokendoctor – See what your Claude Code use overpays](https://github.com/localixai/tokendoctor) (34 pts, [HN](https://news.ycombinator.com/item?id=50526584))
- [Show HN: agent-mcts – Monte Carlo tree search on top of Claude Code](https://github.com/natsu0529/agent-mcts) (15 pts, [HN](https://news.ycombinator.com/item?id=50589235))
- [Rebuilding the Metabase MCP server: lessons for MCP tool design](https://www.metabase.com/blog/mcp-tool-design-lessons) (11 pts, [HN](https://news.ycombinator.com/item?id=50535081))

Want one of these in the nightly run? Reply with the name.

## Independent mention

Autonomous [Lamp](https://www.autonomous.ai/lamp) is a programmable desk robot running the open-source [lampOS](https://github.com/autonomous-ai/lampOS). It gives supported AI agents a physical interface through its camera, microphone, speaker, light and movement, and builders can examine the code and create their own skills.

*Not tested by SkillMaxx; independent mention, not sponsored.*

## 🔧 Tip of the week

**Retry once before you give up on an install.** 31 add-ons passed on some nights and failed on others this week, usually because of a slow download or a network timeout, not a real bug. Here's how we tell the two apart: [flaky vs broken installs](/guides/flaky-vs-broken/).

## 🙏 Tell us

1. **One tool you want tested** before you install it.
2. **Did we get your tool wrong?** Send the link and we'll rerun it and fix the page.

I read every reply.

---

**Sponsor:** This spot is open. Founding rate: **$19 for 1 issue** (or **$59/mo for 4 issues**, about $15 each). Placements are always labeled; see [skillmaxx.gilventures.ai/advertise/](/advertise/)

Built a skill? We'll run it through all five agents: [skillmaxx.gilventures.ai/submit/](/submit/)

</div>
{% include "nlembed.njk" %}
