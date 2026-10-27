---
layout: base.njk
title: "SkillMaxx #2: we stopped crying wolf"
desc: "Issue #2 of SkillMaxx Weekly: a two-night broken rule, the first weekly install scorecard, and a pin-the-marketplace tip. Publishes with the Nov 3 email send."
permalink: /newsletter/issue-2/
ogType: article
issue: 2
issueDate: "2026-11-03"
eleventyExcludeFromCollections: true
# Remove eleventyExcludeFromCollections and keep tags: issues after the Beehiiv send (see growth/routines/NEWSLETTER-SEND.md).
# Content is also client-date-gated until Tue Nov 3, 2026 9:00 AM ET (same pattern as the BFCM banner).
tags: []
jsonld: {"@context":"https://schema.org","@type":"Article","headline":"SkillMaxx #2: we stopped crying wolf","datePublished":"2026-11-03","author":{"@type":"Organization","name":"SkillMaxx"},"publisher":{"@type":"Organization","name":"SkillMaxx"},"image":"https://skillmaxx.gilventures.ai/assets/newsletter/skillmaxx-banner-1200x300.png"}
---
<div class="wrap prose nlissue">
<p class="crumbs"><a href="/">SkillMaxx</a> / <a href="/newsletter/">Newsletter</a> / Issue #2</p>

<div id="nl-issue2-soon" class="card static" style="margin:12px 0;border-color:rgba(198,244,50,.45)">
<p style="margin:0"><b>Issue #2 publishes Tuesday Nov 3, 2026</b> with the first SkillMaxx Weekly email send. This page unlocks the same morning. Source draft: <code>growth/newsletter/issue-002-beehiiv.md</code>.</p>
</div>

<div id="nl-issue2" hidden>
<h1 class="ph">SkillMaxx #2: we stopped crying wolf</h1>
<p class="lead">A new two-night rule, a weekly scorecard, and a question for you. <span class="muted">First email send: Nov 3, 2026.</span></p>

![SkillMaxx](/assets/newsletter/skillmaxx-banner-1200x300.png)

## hey, Brandon here 👋

Quick confession. In week one we were calling things "broken" and "fixed" off a single night of tests. Then we noticed 13 of our 14 "fixed" items had just flip-flopped. That's not news, that's noise.

So we changed the rules:
- **Broken** now means it failed **two nights in a row**.
- **Flaky** means it flip-flopped. We label it and move on.
- **Needs your key** means it only failed because our sandbox has no API keys. Not the tool's fault.

Less drama, more truth. Here's the first scorecard under the new rules.

## 📊 Weekly install scorecard (2026-10-25 to 2026-10-26, 2 nightly runs)

**Pass rate trend** (installs we can judge without an API key): 10-25 795/890 (89.3%) → 10-26 802/890 (90.1%)
**Confirmed broke (failed 2 nights running):** [gdharness](https://skillmaxx.gilventures.ai/skills/gdharness/) (2 installs)
**Really fixed (passing after 2+ bad nights):** nothing (0 installs)
**Flaky, ignore the drama:** 13 add-ons flip-flopped (e.g. Airwallex Dev, @cyanheads/pubmed-mcp-server, Alloydb Omni, Claude Code Setup, Claude Security). We don't call these broken or fixed.
**Needs your API key:** 12 installs only failed because our sandbox has no keys. Not broken, just shy.
**Standout of the week:** [Superpowers](https://skillmaxx.gilventures.ai/skills/superpowers/), clean in 4 agents, zero flakes.
**Most reliable agents:** 1. Codex 100.0% · 2. Claude Code 93.9% · 3. Grok Build 93.5% · 4. Pi 65.5% · 5. Cursor 60.9%

Chart + full week: [https://skillmaxx.gilventures.ai/reports/week/2026-44/](/reports/week/2026-44/) · Is your tool safe today? [https://skillmaxx.gilventures.ai/reports/latest/](/reports/latest/)

## 🔧 Install tip of the week

Pin the marketplace. Same plugin names now live in more than one marketplace, so agents ask "which one?". In Claude Code: `/plugin install sentry@claude-plugins-official`. In Grok Build: `grok plugin install auth0@<marketplace>`.

## 🆕 New on the site

- **Is it safe to install today?** Type a tool, pick your agent, get last night's answer: [https://skillmaxx.gilventures.ai/reports/latest/](/reports/latest/)
- **Weekly scorecard pages** with a chart: [https://skillmaxx.gilventures.ai/reports/week/2026-44/](/reports/week/2026-44/)

## 🙏 I need your help (seriously)

We're tiny and early, and I'd rather build what you'll use than guess. Hit reply with any of these:
1. **One tool you want tested** before you install it.
2. **Is this scorecard useful or noise?** One word is fine.
3. **Did we get your tool wrong?** Send the link, we'll rerun it and fix the page.

I read every reply.

---

**Want this spot?** Founding sponsors: **$19 for 1 issue** (or **$59/mo for 4 issues**, about $15 each). Money never changes a test result. [https://skillmaxx.gilventures.ai/advertise/](/advertise/)

Built a skill? We'll run it through all five agents: [https://skillmaxx.gilventures.ai/submit/](/submit/)
</div>
</div>
<script>(function(){var n=Date.now();if(n>=Date.parse("2026-11-03T14:00:00Z")){var a=document.getElementById("nl-issue2"),b=document.getElementById("nl-issue2-soon");if(a)a.hidden=false;if(b)b.hidden=true}})()</script>
{% include "nlembed.njk" %}
