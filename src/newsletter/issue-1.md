---
layout: base.njk
title: "SkillMaxx #1: we installed 902 agent plugins so you don't have to"
desc: "Issue #1 of SkillMaxx Weekly: 803 of 902 sandboxed installs passed across Claude Code, Codex, Grok Build, Cursor and Pi. Codex went 65 for 65."
permalink: /newsletter/issue-1/
ogType: article
issue: 1
issueDate: "2026-10-25"
tags: issues
jsonld: {"@context":"https://schema.org","@type":"Article","headline":"SkillMaxx #1: we installed 902 agent plugins so you don't have to","datePublished":"2026-10-25","author":{"@type":"Organization","name":"SkillMaxx"},"publisher":{"@type":"Organization","name":"SkillMaxx"},"image":"https://skillmaxx.gilventures.ai/assets/newsletter/skillmaxx-banner-1200x300.png"}
---
<div class="wrap prose nlissue">
<p class="crumbs"><a href="/">SkillMaxx</a> / <a href="/newsletter/">Newsletter</a> / Issue #1</p>
<h1 class="ph">SkillMaxx #1: we installed 902 things so you don't have to</h1>
<p class="lead">803 worked. The other 99 have stories. <span class="muted">Test data from Oct 25, 2026.</span></p>

<p class="callout"><strong>Since this issue:</strong> MCP servers are now tested in all 5 agents (Codex, Grok Build and Pi too, not only Claude Code and Cursor), and "broken" now means failed two nights running. The newest numbers are always on <a href="/reports/latest/">last night's report</a>. Deep dives: <a href="/blog/mcp-servers-claude-code-vs-cursor/">MCP servers in Claude Code vs Cursor</a> and <a href="/blog/809-of-900-agent-addon-installs/">809 of 900 installs</a>.</p>

![SkillMaxx](/assets/newsletter/skillmaxx-banner-1200x300.png)

## ok so here's the deal 👋

We take every agent skill, plugin and MCP server we can find, install it in a fresh sandbox in **Claude Code, Codex, Grok Build, Cursor and Pi**, and write down what happened. No vibes. Just logs.

This is issue #1. Here's the scoreboard.

## The scoreboard (tested Oct 25)

| Agent | Passed | Rate |
|---|---|---|
| Codex | 65 / 65 | **100%** 🏆 |
| Grok Build | 314 / 331 | 95% |
| Claude Code | 338 / 367 | 92% |
| Pi | 57 / 87 | 66% |
| Cursor (MCP servers) | 29 / 52 | 56% |
| **All** | **803 / 902** | **89%** |

The directory now tracks **424** skills, plugins and MCP servers.

Codex: flawless. Didn't even break a sweat. Cursor: 29 of 52 MCP servers connected in our keyless sandbox. Most of the misses want an API key or an account, so don't panic, just bring your own keys. Full list: [https://skillmaxx.gilventures.ai/guides/best-mcp-servers-cursor/](/guides/best-mcp-servers-cursor/)

## Plot twist: "which auth0 did you mean?"

Four plugins that installed fine on Oct 16 now fail in Grok Build: **auth0, grafana-mcp, postman, pr-review-toolkit**. The plugins didn't break. The same names now live in more than one marketplace, so Grok politely refuses and asks you to pin one, like `auth0@<marketplace>`.

**Fix:** add the `@qualifier`. What does install in Grok Build: [https://skillmaxx.gilventures.ai/guides/what-installs-in-grok-build/](/guides/what-installs-in-grok-build/)

## New kid: videogen

**videogen** (Grok Build) does text → video, image → video, script → MP4. Passed its install test on the first try. Not saying it's showing off. It's showing off.

## Crowd favorites (GitHub stars)

- **superpowers**: about 305k ★
- **mattpocock-skills**: about 303k ★
- The official **MCP reference servers** (fetch, filesystem, git, memory, sequential-thinking, time): about 92k ★ each, and still the backbone of half the setups out there

## Things that ghosted us

- **cyanheads PubMed MCP** and **gdharness** stopped connecting in Claude Code (both passed Oct 16). gdharness also wants a Godot editor running. Fair, it's a Godot harness.
- One Claude Code test (postiz) timed out talking to GitHub. Flaky network, not the plugin. Retesting.

## How we test (20 seconds)

Fresh sandbox, no API keys, real agent CLI. Pass means the agent itself lists it as installed or enabled (for MCP, connected). Every result links to its log: [https://skillmaxx.gilventures.ai/how-it-works/](/how-it-works/)

---

**Find what works in *your* agent →** [https://skillmaxx.gilventures.ai](/)

Built a skill? We'll run it through all five agents: [https://skillmaxx.gilventures.ai/submit/](/submit/)

**Want this spot?** Founding sponsors: **$19 for 1 issue** (or **$59/mo for 4 issues**, about $15 each). Hit reply or see [https://skillmaxx.gilventures.ai/advertise/](/advertise/)

See you next week. Fewer ambiguous auth0s, hopefully.

</div>
{% include "nlembed.njk" %}
