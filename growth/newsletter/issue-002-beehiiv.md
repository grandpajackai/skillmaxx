<!-- Beehiiv paste-ready FINAL, not yet sent. Sends Tue Nov 3. Refreshed 2026-11-03 ~3 AM ET from `python3 testing/weekly_scorecard.py` (Oct 28 to Nov 3, 7 runs). Beehiiv draft post_d4f7cc7e still holds the Oct 30 text: the connector's edit_post_content is blocked on the free plan, so paste these blocks in the Beehiiv editor. Publish to /newsletter/issue-2/ only after the send (growth/routines/NEWSLETTER-SEND.md). -->
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

Good thing we did: over the last seven nights, **104 add-ons flip-flopped** at least once. Under the old rules that would've been 104 scary headlines. Under the new rules, exactly one thing is confirmed broken.

## 📊 Weekly install scorecard (Oct 28 to Nov 3, 7 nightly runs)

**Pass rate trend** (installs we can judge without an API key): 89.2% → 90.9% → 91.1% → 86.8% → 86.8% → 86.8% → **86.9%** (900/1,036 on Nov 3). The Oct 31 dip isn't a wave of breakage: that's the night MCP servers started running in Codex, Grok Build and Pi too, so 138 new installs joined the count, and some servers don't connect in those agents yet.
**Confirmed broke (failed 2 nights running):** [notion-mcp-server](https://skillmaxx.gilventures.ai/skills/notion-mcp-server/) (2 installs, Claude Code and Cursor). It's an upstream import error with `@notionhq/client` 5.x, not your setup.
**Really fixed (passing after 2+ bad nights):** [Chrome DevTools](https://skillmaxx.gilventures.ai/skills/chrome-devtools/) and [Chrome DevTools MCP](https://skillmaxx.gilventures.ai/skills/chrome-devtools-mcp/) (2 installs).
**Flaky, retry before you blame:** 104 add-ons flip-flopped (e.g. mcp-local-rag, Azure SQL Developer, korean-law-mcp, @mozilla/firefox-devtools-mcp, Amplitude).
**Needs your API key:** 30 installs only failed because our sandbox has no keys.
**Standout of the week:** [MCP time (reference)](https://skillmaxx.gilventures.ai/skills/mcp-time/), clean in all 5 agents, zero flakes. It gives your agent time and timezone conversion.
**Most reliable agents:** 1. Claude Code 94.2% · 2. Grok Build 92.5% · 3. Codex 88.3% · 4. Pi 65.4% · 5. Cursor 64.1%

This week's chart: https://skillmaxx.gilventures.ai/reports/week/2026-45/ · Last full week: https://skillmaxx.gilventures.ai/reports/week/2026-44/ · Is your tool safe today? https://skillmaxx.gilventures.ai/reports/latest/

## 🧪 New: MCP servers now tested in all 5 agents

Until Oct 31 we only tested MCP servers in Claude Code and Cursor. Since the Oct 31 nightly they also run in **Codex, Grok Build and Pi**. Pass means the agent's own health check says the server connected (for Codex, which has no keyless health check, we run the MCP handshake ourselves and say so). What "pass" means, exactly: https://skillmaxx.gilventures.ai/how-we-test/

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
1. **One tool you want tested** before you install it. (Two people on Bluesky did. Both tools are in our nightly runs now, and agent-postbox passed in all 5 agents on its first night.)
2. **Is this scorecard useful or noise?** One word is fine.
3. **Did we get your tool wrong?** Send the link, we'll rerun it and fix the page.

I read every reply.

---

**Sponsor:** This spot is open. Founding rate: **$19 for 1 issue** (or **$59/mo for 4 issues**, about $15 each). Placements are always labeled; see https://skillmaxx.gilventures.ai/advertise/

Built a skill? We'll run it through all five agents: https://skillmaxx.gilventures.ai/submit/
