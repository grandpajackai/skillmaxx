---
layout: base.njk
title: "SkillMaxx #2: we stopped crying wolf"
desc: "Issue #2 of SkillMaxx Weekly: a two-night rule for \"broken\", MCP servers tested in all 5 agents, and the Oct 28 to Nov 3 scorecard (900 of 1,036 judgeable installs passed)."
permalink: /newsletter/issue-2/
ogType: article
issue: 2
issueDate: "2026-11-03"
date: 2026-11-03
tags: issues
jsonld: {"@context": "https://schema.org", "@type": "Article", "headline": "SkillMaxx #2: we stopped crying wolf", "datePublished": "2026-11-03", "author": {"@type": "Organization", "name": "SkillMaxx"}, "publisher": {"@type": "Organization", "name": "SkillMaxx"}, "image": "https://skillmaxx.gilventures.ai/assets/newsletter/skillmaxx-banner-1200x300.png"}
---
<div class="wrap prose nlissue">
<p class="crumbs"><a href="/">SkillMaxx</a> / <a href="/newsletter/">Newsletter</a> / Issue #2</p>
<h1 class="ph">SkillMaxx #2: we stopped crying wolf</h1>
<p class="lead">A two-night rule for "broken", MCP tested in all 5 agents, and a question for you.</p>

<p class="callout"><strong>Archive copy.</strong> Written for Tue Nov 3, 2026 with numbers from the Oct 28 to Nov 3 nightly runs. The newest numbers are always on <a href="/reports/latest/">last night's report</a>.</p>

![SkillMaxx](/assets/newsletter/skillmaxx-banner-1200x300.png)

## hey, Brandon here 👋

Quick confession. In week one we were calling things "broken" and "fixed" off a single night of tests. Then we noticed 13 of our 14 "fixed" items had just flip-flopped. That's not news, that's noise.

So we changed the rules:

- **Broken** now means it failed **two nights in a row**.
- **Flaky** means it flip-flopped (or only passed on a retry). We label it and move on.
- **Needs your key** means it only failed because our sandbox has no API keys. Not the tool's fault.

Good thing we did: over the last seven nights, **104 add-ons flip-flopped** at least once. Under the old rules that would've been 104 scary headlines. Under the new rules, exactly one thing is confirmed broken.

## 📊 Weekly install scorecard (Oct 28 to Nov 3, 7 nightly runs)

**Pass rate trend** (installs we can judge without an API key): 89.2% → 90.9% → 91.1% → 86.8% → 86.8% → 86.8% → **86.9%** (900/1,036 on Nov 3). The Oct 31 dip isn't a wave of breakage: that's the night MCP servers started running in Codex, Grok Build and Pi too, so 138 new installs joined the count, and some servers don't connect in those agents yet.

**Confirmed broke (failed 2 nights running):** [notion-mcp-server](/skills/notion-mcp-server/) (2 installs, Claude Code and Cursor). It's an upstream import error with `@notionhq/client` 5.x, not your setup.

**Really fixed (passing after 2+ bad nights):** [Chrome DevTools](/skills/chrome-devtools/) and [Chrome DevTools MCP](/skills/chrome-devtools-mcp/) (2 installs).

**Flaky, retry before you blame:** 104 add-ons flip-flopped (e.g. mcp-local-rag, Azure SQL Developer, korean-law-mcp, @mozilla/firefox-devtools-mcp, Amplitude).

**Needs your API key:** 30 installs only failed because our sandbox has no keys.

**Standout of the week:** [MCP time (reference)](/skills/mcp-time/), clean in all 5 agents, zero flakes. It gives your agent time and timezone conversion.

**Most reliable agents:** 1. Claude Code 94.2% · 2. Grok Build 92.5% · 3. Codex 88.3% · 4. Pi 65.4% · 5. Cursor 64.1%

Weekly charts: [week 44](/reports/week/2026-44/) (Oct 26 to Nov 1) · [week 45](/reports/week/2026-45/) (Nov 2 to 8) · Is your tool safe today? [skillmaxx.gilventures.ai/reports/latest/](/reports/latest/)

## 🧪 New: MCP servers now tested in all 5 agents

Until Oct 31 we only tested MCP servers in Claude Code and Cursor. Since the Oct 31 nightly they also run in **Codex, Grok Build and Pi**. Pass means the agent's own health check says the server connected (for Codex, which has no keyless health check, we run the MCP handshake ourselves and say so). What "pass" means, exactly: [skillmaxx.gilventures.ai/how-we-test/](/how-we-test/)

## 📖 Two deep dives from our test logs

- **[Which MCP servers work in Claude Code vs Cursor?](/blog/mcp-servers-claude-code-vs-cursor/)** 614 installs. All 7 official reference servers passed in both; only 23 of 45 npm packages did. If you're picking an MCP server, start here.
- **[809 of 900: what 5,404 installs taught us](/blog/809-of-900-agent-addon-installs/)** Six nights, five agents, 89% passing, and the patterns behind the other 11%.

## 🔧 Install tips of the week

1. **Pin the marketplace.** Same plugin names now live in more than one marketplace, so agents ask "which one?". Claude Code: `/plugin install sentry@claude-plugins-official`. Grok Build: `grok plugin install auth0@<marketplace>`.
2. **Pin MCP versions too.** "Installs clean" is not the same as "safe". This week a malicious npm MCP package got a GitHub advisory (GHSA-65cr-mcfq-59hh, `@atlisp/mcp` 1.12.14; it was never in our directory). Use exact versions like `npx -y some-mcp@1.2.3`, not `@latest`, and skim what a server can touch before you add it.
3. **One flaky night isn't a verdict.** If an add-on fails once, retry before you rip it out. That's literally why we built the two-night rule.

## 🆕 New on the site

- **[Blog](/blog/):** long reads built on our own test data.
- **Is it safe to install today?** Type a tool, pick your agent, get last night's answer: [skillmaxx.gilventures.ai/reports/latest/](/reports/latest/)
- **Every issue, archived:** [skillmaxx.gilventures.ai/newsletter/](/newsletter/)

## 🙏 I need your help (seriously)

We're tiny and early, and I'd rather build what you'll use than guess. Hit reply with any of these:

1. **One tool you want tested** before you install it. (Two people on Bluesky did. Both tools are in our nightly runs now, and agent-postbox passed in all 5 agents on its first night.)
2. **Is this scorecard useful or noise?** One word is fine.
3. **Did we get your tool wrong?** Send the link, we'll rerun it and fix the page.

I read every reply.

---

**Sponsor:** This spot is open. Founding rate: **$19 for 1 issue** (or **$59/mo for 4 issues**, about $15 each). Placements are always labeled; see [skillmaxx.gilventures.ai/advertise/](/advertise/)

Built a skill? We'll run it through all five agents: [skillmaxx.gilventures.ai/submit/](/submit/)

</div>
{% include "nlembed.njk" %}
