<!-- Beehiiv paste-ready DRAFT, not sent. Sends Tue Nov 3. Final pass Oct 30 (stats through the Oct 30 nightly). Monday night: rerun `python3 testing/weekly_scorecard.py` and replace ONLY the scorecard block + the numbers marked (refresh) with the new output; keep the rest. Publish to /newsletter/issue-2/ only after the send (growth/routines/NEWSLETTER-SEND.md). -->
**Title:** SkillMaxx #2: we stopped crying wolf
**Subtitle:** A two-night rule for "broken", MCP tested in all 5 agents, and a question for you.
**Preview text:** 100+ add-ons flip-flopped this week. We refused to call any of them broken.

![SkillMaxx](https://raw.githubusercontent.com/grandpajackai/skillmaxx/master/growth/brand/beehiiv/skillmaxx-banner-1200x300.png)

## hey, Brandon here 👋

Quick confession. In week one we were calling things "broken" and "fixed" off a single night of tests. Then we noticed 13 of our 14 "fixed" items had just flip-flopped. That's not news, that's noise.

So we changed the rules:
- **Broken** now means it failed **two nights in a row**.
- **Flaky** means it flip-flopped (or only passed on a retry). We label it and move on.
- **Needs your key** means it only failed because our sandbox has no API keys. Not the tool's fault.

Good thing we did: over six nights, **117 add-ons flip-flopped** at least once (refresh). Under the old rules that would've been 117 scary headlines. Under the new rules, exactly one thing is confirmed broken.

## 📊 Weekly install scorecard (Oct 25 to Oct 30, 6 nightly runs) (refresh)

**Pass rate trend** (installs we can judge without an API key): 89.3% → 90.1% → 90.8% → 89.2% → 90.9% → **91.1%** (809/888 on Oct 30)
**Confirmed broke (failed 2 nights running):** [gdharness](https://skillmaxx.gilventures.ai/skills/gdharness/) (2 installs). It also wants a running Godot editor, so test it in your own setup before writing it off.
**Really fixed (passing after 2+ bad nights):** nothing yet.
**Flaky, retry before you blame:** 117 add-ons flip-flopped (e.g. Alloydb Omni, @cyanheads/pubmed-mcp-server, Airwallex Dev, Data Engineering, Expo).
**Needs your API key:** 12 installs only failed because our sandbox has no keys.
**Standout of the week:** [Superpowers](https://skillmaxx.gilventures.ai/skills/superpowers/), clean in 4 agents, zero flakes. It teaches your agent brainstorming, subagent-driven development with code review, systematic debugging and red/green TDD.
**Most reliable agents:** 1. Codex 100% · 2. Grok Build 94.4% · 3. Claude Code 94.1% · 4. Pi 65.3% · 5. Cursor 62.7%

Chart + full week: https://skillmaxx.gilventures.ai/reports/week/2026-44/ · Is your tool safe today? https://skillmaxx.gilventures.ai/reports/latest/

## 🧪 New: MCP servers now tested in all 5 agents

Until this week we only tested MCP servers in Claude Code and Cursor. Now they also run in **Codex, Grok Build and Pi**, starting with the Oct 31 nightly. Pass means the agent's own health check says the server connected (for Codex, which has no keyless health check, we run the MCP handshake ourselves and say so). What "pass" means, exactly: https://skillmaxx.gilventures.ai/how-we-test/

## 📖 Two deep dives from our test logs

- **[Which MCP servers work in Claude Code vs Cursor?](https://skillmaxx.gilventures.ai/blog/mcp-servers-claude-code-vs-cursor/)** 614 installs. All 7 official reference servers passed in both; only 23 of 45 npm packages did. If you're picking an MCP server, start here.
- **[809 of 900: what 5,404 installs taught us](https://skillmaxx.gilventures.ai/blog/809-of-900-agent-addon-installs/)** Six nights, five agents, 89% passing, and the patterns behind the other 11%.

## 🔧 Install tips of the week

1. **Pin the marketplace.** Same plugin names now live in more than one marketplace, so agents ask "which one?". Claude Code: `/plugin install sentry@claude-plugins-official`. Grok Build: `grok plugin install auth0@<marketplace>`.
2. **Pin MCP versions too.** "Installs clean" is not the same as "safe". This week a malicious npm MCP package got a GitHub advisory (GHSA-65cr-mcfq-59hh, `@atlisp/mcp` 1.12.14; it was never in our directory). Use exact versions like `npx -y some-mcp@1.2.3`, not `@latest`, and skim what a server can touch before you add it.
3. **One flaky night isn't a verdict.** If an add-on fails once, retry before you rip it out. That's literally why we built the two-night rule.

## 🆕 New on the site

- **[Blog](https://skillmaxx.gilventures.ai/blog/):** long reads built on our own test data.
- **Is it safe to install today?** Type a tool, pick your agent, get last night's answer: https://skillmaxx.gilventures.ai/reports/latest/
- **Every issue, archived:** https://skillmaxx.gilventures.ai/newsletter/

## 🙏 I need your help (seriously)

We're tiny and early, and I'd rather build what you'll use than guess. Hit reply with any of these:
1. **One tool you want tested** before you install it. (Someone on Bluesky did this week; it's in tonight's run.)
2. **Is this scorecard useful or noise?** One word is fine.
3. **Did we get your tool wrong?** Send the link, we'll rerun it and fix the page.

I read every reply.

---

**Sponsor:** This spot is open. Founding rate: **$19 for 1 issue** (or **$59/mo for 4 issues**, about $15 each). Placements are always labeled; see https://skillmaxx.gilventures.ai/advertise/

Built a skill? We'll run it through all five agents: https://skillmaxx.gilventures.ai/submit/
