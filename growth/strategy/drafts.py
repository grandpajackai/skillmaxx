# Source of truth for the 2-week starter batch. `python3 growth/strategy/drafts.py` regenerates DRAFTS-2026-10-27.md + .json and checks every post's length.
# Rule (Brandon, 2026-10-26): LinkedIn is the quality bar. X and Bluesky carry the same full context (who, what, when, what it means), as threads.
# Default = single posts with full context; threads only where needed (<=2/channel/week). X: 1-4 posts, post 1 stands alone and names the company/tool, each post <=280 (URLs count 23). Bluesky: 1-3 posts, each <=300. LinkedIn 350-1,400 chars.
# Numbers from the 2026-10-26 nightly run (src/_data/reports.json). REFRESH = re-check the night before.
import json, re, pathlib
S = "skillmaxx.gilventures.ai"
P = {1:"Results",2:"Know-how",3:"Report/newsletter CTA",4:"Sponsors",5:"News take",6:"Leaders",7:"Seasonal",8:"Community/BTS"}
D = json.loads(r"""[
 {
  "date": "2026-10-27",
  "dow": "Tue",
  "times": {
   "x": "9:30 AM",
   "bluesky": "9:30 AM",
   "linkedin": "9:30 AM"
  },
  "pillar": 1,
  "theme": "Launch + pinned post",
  "x": [
   "Every night we install 424 agent skills, plugins and MCP servers into Claude Code, Codex, Grok, Cursor and Pi, and publish what actually works.\n\nLast night: 802 of 890 installs clean. The 88 misses are public too, with logs.\n\nWhat should we test next?\nskillmaxx.gilventures.ai/reports/latest/"
  ],
  "bluesky": [
   "hi bluesky 👋 we're SkillMaxx. every night we install 424 agent skills, plugins and MCP servers into Claude Code, Codex, Grok, Cursor and Pi, with no API keys, and publish what works.\n\nlast night: 802 of 890 clean. reply with a repo and we'll test it.\nskillmaxx.gilventures.ai/reports/latest/"
  ],
  "linkedin": "Why SkillMaxx exists\n\nEvery AI coding agent now has skills, plugins and MCP servers. Almost none of them tell you whether a given one installs in the agent you actually use. A README that says \"works with AI agents\" is a hope, not a test.\n\nSo every night we install them for real: 424 add-ons, 902 installs across Claude Code, Codex, Grok, Cursor and Pi, in fresh sandboxes with no API keys. Last night 802 of the 890 we could judge installed cleanly. The failures are published too, with logs, and we only call something broken after it fails two nights in a row.\n\nHonest disclaimer: we launched this month and we're small. So I'm asking:\n• What should we test next?\n• Would a weekly install scorecard be useful for your team, or is it noise?\n\nFree daily report: https://skillmaxx.gilventures.ai/reports/latest/\nWeekly newsletter: https://skillmaxx.gilventures.ai/newsletter/\n\nBrandon, founder",
  "image": "growth/profiles/pin-chart.png (pass-rate chart) on X and LinkedIn; Bluesky text + link card",
  "refresh": false,
  "xnote": "Pin it. Image: pass-rate chart.",
  "alt": "Bar chart of last night's install pass rate per agent: Codex 65/65, Claude Code 340/367, Grok 313/331, Pi 57/87, Cursor 27/52."
 },
 {
  "date": "2026-10-28",
  "dow": "Wed",
  "times": {
   "x": "9:30 AM",
   "bluesky": "7:30 PM",
   "linkedin": "12:00 PM"
  },
  "pillar": 5,
  "theme": "News: Agent Skills moves to the AAIF",
  "x": [
   "Anthropic just gave away Agent Skills.\n\nOn Oct 22 it donated the open standard for teaching AI agents new tasks to the Agentic AI Foundation (Linux Foundation), the same home as MCP.\n\n1M skills published. ~280M installs. 70+ platforms.",
   "What's a skill? A folder with a SKILL file that teaches an agent one job, plus any scripts it needs.\n\nIt started inside Claude Code. Now ChatGPT, Cursor, Copilot and VS Code all load them.",
   "What changes for devs:\n• one format across agents, less repackaging\n• a proposed roadmap: versioned releases + security guidance for people installing skills\n\nWhat doesn't change: a shared format ≠ \"installs in your agent today.\"",
   "In our nightly runs, the same add-on can install clean in one agent and fail in another. That gap is what we test.\n\nWhat should a skills security guide cover?\n\nSource: anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation"
  ],
  "bluesky": [
   "Anthropic donated Agent Skills to the Agentic AI Foundation on Oct 22. it's the open standard for teaching AI agents new tasks (a folder with a SKILL file), and it now sits next to MCP under the Linux Foundation.\n\ntheir numbers: 1M skills, ~280M installs, 70+ platforms.",
   "what it means: one format across Claude Code, Codex, Cursor, Copilot and more, plus a proposed roadmap with versioned releases and security guidance.\n\nwhat it doesn't mean: portable format ≠ portable install. in our runs the same add-on can pass in one agent and fail in another.",
   "what would you want a skills security guide to cover?\n\nanthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation"
  ],
  "linkedin": "Agent Skills just got a neutral home.\n\nOn Oct 22 Anthropic donated the Agent Skills standard to the Agentic AI Foundation under the Linux Foundation, where MCP already lives. Their numbers: 1 million skills published, nearly 280 million installs, 70+ agent platforms.\n\nWhat it means for teams, in plain terms:\n1. One SKILL file format can now load across Claude Code, Codex, Cursor, Copilot and more. Less re-packaging per tool.\n2. The roadmap proposes versioned releases and security guidance for people who install skills. Worth watching.\n3. A shared format is not the same as \"works in your agent today\". In our nightly runs, the same add-on can install cleanly in one agent and fail in another.\n\nThat third point is why we test installs every night and publish the logs.\n\nWhat would you want a skills security guide to cover?\n\nSource: https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation",
  "image": "X: none (text wins for takes). LinkedIn: simple quote card with the 3 numbers",
  "refresh": false,
  "xnote": "",
  "alt": "Card with three numbers: 1M skills published, about 280M installs, 70+ agent platforms."
 },
 {
  "date": "2026-10-29",
  "dow": "Thu",
  "times": {
   "x": "9:30 AM",
   "bluesky": "7:30 PM",
   "linkedin": "12:00 PM"
  },
  "pillar": 8,
  "theme": "Test request call-out",
  "x": [
   "Got a skill, plugin or MCP server you almost installed but didn't trust? Reply with it.\n\nTonight we'll install it in Claude Code, Codex, Grok, Cursor and Pi in a clean sandbox and reply with pass/fail per agent and the logs. Free.\n\nYour requests decide what we test next."
  ],
  "bluesky": [
   "open call: got a skill, plugin or MCP server you almost installed but didn't trust?\n\nreply with the repo. tonight we'll install it in Claude Code, Codex, Grok, Cursor and Pi in a clean sandbox and reply with pass/fail per agent and the logs. free. we're new; this is how we pick tests."
  ],
  "linkedin": "A question for anyone rolling out AI coding agents to a team:\n\nWhat's the one skill, plugin or MCP server you'd want checked before it goes on everyone's machine?\n\nComment the name or repo. We'll install it tonight in Claude Code, Codex, Grok, Cursor and Pi, in a clean sandbox, and reply with the results and the logs. Free, no strings.\n\nWe're a month old, and this is how we decide what to test next.",
  "image": "none",
  "refresh": false,
  "xnote": "",
  "alt": ""
 },
 {
  "date": "2026-10-30",
  "dow": "Fri",
  "times": {
   "x": "9:30 AM",
   "bluesky": "7:30 PM",
   "linkedin": "12:00 PM"
  },
  "pillar": 2,
  "theme": "Myth: stars mean it works",
  "x": [
   "305,000 GitHub stars don't tell you if a tool installs in your AI agent. Superpowers has them and installed clean in 4 agents with zero flaky runs this week.\n\nOur 3 checks: names your agent, exact install command per agent, two clean nights in a row.\n\nYour rule?"
  ],
  "bluesky": [
   "myth: lots of GitHub stars = it installs fine in your agent.\n\nSuperpowers has 305k stars *and* installed clean in 4 agents with zero flaky runs this week. our 3 checks: names your agent, exact install command per agent, two clean nights in a row.\nskillmaxx.gilventures.ai/skills/superpowers/"
  ],
  "linkedin": "Myth vs. reality for teams choosing agent add-ons\n\nMyth: a repo with lots of GitHub stars will install cleanly in your agent.\nReality: stars measure interest. They say nothing about whether it installs in the agent your team uses.\n\nOur rule of thumb after a month of nightly tests:\n• Check that it lists your agent by name, not \"works with AI agents\".\n• Look for an exact install command per agent.\n• Prefer things with two clean nights in a row over things with one viral week.\n\nOne that passes all three this week: Superpowers, clean in 4 agents with zero flaky runs.\nhttps://skillmaxx.gilventures.ai/skills/superpowers/\n\nWhat's your own rule for trusting an add-on?",
  "image": "optional screenshot of the Superpowers skill page row",
  "refresh": true,
  "xnote": "REFRESH Superpowers status the night before.",
  "alt": ""
 },
 {
  "date": "2026-10-31",
  "dow": "Sat",
  "times": {
   "x": "11:00 AM",
   "bluesky": "5:00 PM",
   "linkedin": "10:00 AM"
  },
  "pillar": 7,
  "theme": "Halloween: scariest install log",
  "x": [
   "Happy Halloween 🎃 The scariest thing in our install logs this week: 13 tools that passed one night, failed the next, then passed again.\n\nA crash you can fix. Flaky works on your laptop, fails in CI. So we leave flaky tools out of pass and fail.\n\nYour most haunted install?"
  ],
  "bluesky": [
   "happy halloween 🎃 the scariest thing in our install logs this week: 13 tools that passed one night, failed the next, then passed again.\n\na crash you can fix. flaky works on your laptop and fails in CI. so we leave those out of both pass and fail.\n\nyour most haunted install?"
  ],
  "linkedin": "Happy Halloween from SkillMaxx.\n\nThe scariest thing we saw in our logs this week wasn't a hard failure. A crash is easy: you see it, you fix it.\n\nThe scary ones are flaky: an install that passes one night, fails the next, then passes again. We saw 13 of those this week. We now label them flaky and leave them out of both the pass and the fail column, because shouting \"broken!\" after one bad night isn't fair to the people who build these tools.\n\nWhat's the most haunted install you've dealt with?",
  "image": "optional: dark-mode screenshot of a flaky row",
  "refresh": true,
  "xnote": "",
  "alt": ""
 },
 {
  "date": "2026-11-01",
  "dow": "Sun",
  "times": {
   "x": "6:00 PM",
   "bluesky": "6:00 PM",
   "linkedin": "10:00 AM"
  },
  "pillar": 3,
  "theme": "Weekly scorecard (week 44) + DST",
  "x": [
   "Week 44 install scorecard for AI coding agents: 802 of 890 installs worked (90.1%) across Claude Code, Codex, Grok, Cursor and Pi.\n\nCodex went 65 for 65. Confirmed broken: 2. Really fixed: 0. Flaky, not counted: 13.\n\nFull week + logs: skillmaxx.gilventures.ai/reports/week/2026-44/"
  ],
  "bluesky": [
   "week 44 install scorecard 📊 802 of 890 add-on installs worked (90.1%) across Claude Code, Codex, Grok, Cursor and Pi.\n\nCodex went 65 for 65. confirmed broken: 2. really fixed: 0. flaky, not counted: 13.\n\nskillmaxx.gilventures.ai/reports/week/2026-44/"
  ],
  "linkedin": "Week 44 agent install scorecard\n\n• 802 of 890 judgeable installs clean (90.1%)\n• Confirmed broken after two nights: 2 installs\n• Really fixed this week: 0\n• Flaky results we refused to count: 13\n• Most reliable agent: Codex, 65 of 65\n\nIt's an ecosystem scorecard, not an agent ranking: it shows how well add-ons ship for each agent, in a sandbox with no API keys.\n\nThe full week, with logs: https://skillmaxx.gilventures.ai/reports/week/2026-44/\nThe same scorecard lands in your inbox Tuesdays: https://skillmaxx.gilventures.ai/newsletter/\n\nWhat should we add to next week's scorecard?",
  "image": "scorecard card image (render from weekly_scorecard.py output)",
  "refresh": true,
  "xnote": "",
  "alt": "Weekly scorecard card: 802 of 890 installs clean, 90.1%. Codex 65 of 65. Broken 2, fixed 0, flaky 13."
 },
 {
  "date": "2026-11-02",
  "dow": "Mon",
  "times": {
   "x": "9:30 AM",
   "bluesky": "7:30 PM",
   "linkedin": "12:00 PM"
  },
  "pillar": 2,
  "theme": "Install tip: pin the marketplace",
  "x": [
   "Claude Code tip: pin the marketplace when you install a plugin.\n\n/plugin install sentry@claude-plugins-official\n\nThe same plugin names now exist in 2+ marketplaces. Skip the @ and the agent asks which one, or teammates end up with different plugins."
  ],
  "bluesky": [
   "claude code tip: pin the marketplace when you install a plugin.\n\n/plugin install sentry@claude-plugins-official\n\nsame plugin names now exist in 2+ marketplaces. skip the @ and the agent asks which one, or two laptops get different plugins.\n\nfree weekly tips: skillmaxx.gilventures.ai/newsletter/"
  ],
  "linkedin": "Monday tip for anyone standardizing Claude Code across a team:\n\nInstall plugins with the marketplace pinned:\n/plugin install sentry@claude-plugins-official\n\nWhy it matters: the same plugin names now exist in more than one marketplace. Without the @marketplace part, the agent stops and asks which one you meant, and in a shared setup script that's how two laptops end up with two different plugins.\n\nPut the pinned form in your onboarding docs and you'll never debug that one.\n\nWe test installs like this every night across 5 agents. Our free weekly newsletter (issue #2 is out tomorrow) has one tip like this plus the scorecard: https://skillmaxx.gilventures.ai/newsletter/",
  "image": "terminal screenshot of the pinned install command",
  "refresh": false,
  "xnote": "",
  "alt": "Terminal screenshot: /plugin install sentry@claude-plugins-official"
 },
 {
  "date": "2026-11-03",
  "dow": "Tue",
  "times": {
   "x": "9:30 AM",
   "bluesky": "7:30 PM",
   "linkedin": "12:00 PM"
  },
  "pillar": 3,
  "theme": "Newsletter #2 is out",
  "x": [
   "SkillMaxx Weekly #2 is out: a free 3-minute email on which AI agent add-ons actually install.\n\nThe scorecard for Claude Code, Codex, Grok, Cursor and Pi, what broke 2 nights running, and one tip you can paste today. Useful or noise? Tell us.\n\nskillmaxx.gilventures.ai/newsletter/"
  ],
  "bluesky": [
   "SkillMaxx Weekly #2 just went out 📬 a free 3-minute email on which AI agent add-ons actually install: the scorecard for Claude Code, Codex, Grok, Cursor and Pi, what broke two nights running, and one tip.\n\nuseful or noise? reply and tell us.\nskillmaxx.gilventures.ai/newsletter/"
  ],
  "linkedin": "Issue #2 of SkillMaxx Weekly went out this morning.\n\nWhat's inside:\n• The weekly install scorecard across Claude Code, Codex, Grok, Cursor and Pi\n• What broke two nights in a row (and what we refused to call broken)\n• One install tip you can paste today\n\nIt's free, about a 3-minute read, and I'd genuinely like to hear if it's useful or noise. Every reply gets read.\n\nhttps://skillmaxx.gilventures.ai/newsletter/\n\nBrandon",
  "image": "newsletter header image",
  "refresh": false,
  "xnote": "",
  "alt": ""
 },
 {
  "date": "2026-11-04",
  "dow": "Wed",
  "times": {
   "x": "9:30 AM",
   "bluesky": "7:30 PM",
   "linkedin": "4:00 PM"
  },
  "pillar": 6,
  "theme": "Leaders: Cursor's Agent SDK and computer use",
  "x": [
   "Cursor just shipped two big things in quick succession:\n\n1. agents that can drive desktop apps, like the iOS Simulator\n2. an Agent SDK: agents as code, prompts in Markdown, tools in TypeScript\n\nThe real story is what this does to your toolchain 👇",
   "Agents are gaining capabilities faster than most teams can vet them.\n\nEvery new tool an agent can call is one more thing that has to install, connect and behave.",
   "Receipt from our runs: Cursor is where add-ons most often install but never report \"ready.\" 27 of 52 passed last night (no API keys).\n\nNot a knock on Cursor. It's the strictest about what \"ready\" means.",
   "Two habits worth stealing:\n• keep a short allow-list of add-ons your team has verified\n• re-check after every agent update\n\nHow is your team vetting new agent tools?"
  ],
  "bluesky": [
   "Cursor shipped desktop control (agents driving apps like the iOS Simulator) and an Agent SDK (prompts in Markdown, tools in TypeScript, built-in evals) in quick succession.\n\nagents are gaining tools faster than teams can vet them.",
   "receipt from our nightly runs: Cursor is where add-ons most often install but don't report \"ready\": 27 of 52 last night, no API keys.\n\ntwo habits: a short allow-list of verified add-ons, and a re-check after every agent update. how does your team vet?"
  ],
  "linkedin": "What Cursor's last two launches tell us about where coding agents are going\n\nIn quick succession Cursor shipped (1) agents that can drive desktop apps like the iOS Simulator, and (2) an Agent SDK: agents defined as code, prompts in Markdown, tools in TypeScript, with built-in evals.\n\nThe lesson for teams isn't \"switch tools\". It's that agents are gaining capabilities faster than most teams can vet them. Every new tool an agent can call is one more thing that has to install, connect and behave.\n\nTwo practical habits:\n1. Keep a short allow-list of add-ons your team has actually verified.\n2. Re-check after agent updates. In our runs, Cursor is where add-ons most often install but don't report \"ready\" (27 of 52 last night, without API keys).\n\nHow is your team vetting new agent tools?",
  "image": "none on X; LinkedIn: per-agent pass chart",
  "refresh": true,
  "xnote": "REFRESH Cursor numbers.",
  "alt": ""
 },
 {
  "date": "2026-11-05",
  "dow": "Thu",
  "times": {
   "x": "9:30 AM",
   "bluesky": "7:30 PM",
   "linkedin": "12:00 PM"
  },
  "pillar": 4,
  "theme": "Tool authors + how sponsorship works",
  "x": [
   "Built a skill, plugin or MCP server? It likely works in more AI agents than your README says.\n\nSubmit it free: we install it nightly in Claude Code, Codex, Grok, Cursor and Pi, with logs per agent. Sponsor slots are labeled; money never changes a result.\n\nskillmaxx.gilventures.ai/submit/"
  ],
  "bluesky": [
   "build a skill, plugin or MCP server? it probably works in more agents than your README says.\n\nsubmit it free and we'll install it nightly in Claude Code, Codex, Grok, Cursor and Pi, with logs. labeled sponsor slots exist too; paying never changes a result.\nskillmaxx.gilventures.ai/submit/"
  ],
  "linkedin": "For teams who build agent skills, plugins or MCP servers\n\nTwo ways to work with SkillMaxx:\n\n1. Free: submit your tool and we'll install it every night in Claude Code, Codex, Grok, Cursor and Pi, with the exact install command for each and the logs, good or bad. Most tools listed for one agent turn out to work in two or three more.\nhttps://skillmaxx.gilventures.ai/submit/\n\n2. Paid, clearly labeled: founding sponsor slots (featured listing, newsletter, category page) from $15. The first 10 sponsors lock the founding rate for 6 months.\nhttps://skillmaxx.gilventures.ai/advertise/\n\nThe one rule: money never changes a test result or a ranking. If a sponsor's tool fails, the site says so, and we'll help fix it.\n\nAudience is small and early, and we share real numbers with every sponsor monthly.",
  "image": "none",
  "refresh": false,
  "xnote": "",
  "alt": ""
 },
 {
  "date": "2026-11-06",
  "dow": "Fri",
  "times": {
   "x": "9:30 AM",
   "bluesky": "7:30 PM",
   "linkedin": "12:00 PM"
  },
  "pillar": 1,
  "theme": "How we test (and our limits)",
  "x": [
   "\"Passed\" on SkillMaxx means one thing, and it isn't \"this tool is good.\"\n\nFresh sandbox, real agent CLI, no keys. Pass = the agent itself lists it installed or connected. Broken = fails 2 nights running. Pass/fail/pass = flaky.\n\nWrong? We'll rerun it.\nskillmaxx.gilventures.ai/how-we-test/"
  ],
  "bluesky": [
   "\"passed\" on SkillMaxx means one thing, and it isn't \"this tool is good.\"\n\nfresh sandbox, real agent CLI, no credentials. pass = the agent says installed/connected. broken = fails 2 nights running. pass/fail/pass = flaky.\n\ngot one wrong? we'll rerun it.\nskillmaxx.gilventures.ai/how-we-test/"
  ],
  "linkedin": "How we test, including what it can't tell you\n\nEvery night, for each add-on and each agent:\n1. A fresh sandbox, the real agent CLI, no credentials.\n2. Pass means the agent itself lists the add-on as installed, or connected for MCP servers.\n3. Broken means it failed two nights in a row. One bad night is \"pending\"; pass/fail/pass is \"flaky\".\n4. Failures that only need an API key get their own label, so nobody gets blamed for our missing keys.\n\nWhat a pass doesn't prove: that the tool does its job well. It proves it installs and connects in that agent today.\n\nIf you think we got your tool wrong, tell us and we'll rerun it.\nhttps://skillmaxx.gilventures.ai/how-we-test/",
  "image": "simple 4-step diagram",
  "refresh": false,
  "xnote": "",
  "alt": "Four-step diagram: fresh sandbox, real agent CLI, no credentials, agent reports installed."
 },
 {
  "date": "2026-11-07",
  "dow": "Sat",
  "times": {
   "x": "11:00 AM",
   "bluesky": "5:00 PM",
   "linkedin": "10:00 AM"
  },
  "pillar": 8,
  "theme": "What we got wrong: flaky vs broken",
  "x": [
   "We used to call a tool \"broken\" after one failed install. But some fail at random: Qodo failed one night, passed the next. Now broken = fails two nights in a row. One-offs are flagged flaky. How do you tell flaky from broken?"
  ],
  "bluesky": [
   "something we got wrong early on: we called a tool \"broken\" after one failed install. but some fail at random: Qodo failed one night, passed the next.\n\nnow broken = fails two nights in a row; one-offs are flaky.\n\nhow do you tell? skillmaxx.gilventures.ai/guides/flaky-vs-broken/"
  ],
  "linkedin": "One rule we changed in SkillMaxx's first month\n\nWe used to mark a tool \"broken\" the first time its install failed. That turned out to be wrong. Some installs fail at random: a slow network, a registry hiccup, a timing issue. Qodo failed one night and passed the next, and we had already called it broken.\n\nSo we changed the rule:\n• Broken means it failed two nights in a row.\n• One bad night is pending, not broken.\n• Pass, fail, pass is labeled flaky and left out of both columns.\n\nThe lesson for teams running AI agents: one red result is a signal, not a verdict. Re-run before you rip a tool out, and track flakiness separately so it doesn't hide real breakage or get blamed on the tool's author.\n\nHow does your team tell flaky from actually broken?\n\nThe full write-up: https://skillmaxx.gilventures.ai/guides/flaky-vs-broken/\n\nBrandon",
  "image": "simple flaky vs broken status card (two rows: pass/fail/pass = flaky, fail/fail = broken). Bluesky alt text: Status card. Flaky: pass, fail, pass across three nights, not counted. Broken: fail two nights in a row.",
  "refresh": false,
  "xnote": "Brandon's trimmed opener.",
  "alt": "Status card. Flaky: pass, fail, pass across three nights, not counted. Broken: fail two nights in a row."
 },
 {
  "date": "2026-11-08",
  "dow": "Sun",
  "times": {
   "x": "6:00 PM",
   "bluesky": "6:00 PM",
   "linkedin": "10:00 AM"
  },
  "pillar": 3,
  "theme": "Weekly scorecard (week 45)",
  "x": [
   "Week 45 install scorecard for AI coding agents:\n\n[pass] of [judgeable] installs worked ([%]) across Claude Code, Codex, Grok, Cursor and Pi.\n\n[one-line hook from the week's biggest change] 🧵",
   "Most reliable agent: [agent], [x of y]\nConfirmed broken (2 nights running): [n]\nReally fixed: [n]\nFlaky, not counted: [n]",
   "Full week with logs: skillmaxx.gilventures.ai/reports/week/2026-45/\n\nWhat should we test next week?"
  ],
  "bluesky": [
   "week 45 install scorecard 📊\n\n[pass] of [judgeable] add-on installs worked ([%]) across Claude Code, Codex, Grok, Cursor and Pi.\n\nmost reliable: [agent]. confirmed broken: [n]. really fixed: [n]. flaky, not counted: [n].",
   "[the week's biggest change, one line]\n\nreply with what we should test next week.\nskillmaxx.gilventures.ai/reports/week/2026-45/"
  ],
  "linkedin": "Week 45 agent install scorecard\n\n• [pass] of [judgeable] installs clean ([%])\n• Confirmed broken after two nights: [n]\n• Really fixed: [n]\n• Flaky results we refused to count: [n]\n• Most reliable agent: [agent]\n\nFull week with logs: https://skillmaxx.gilventures.ai/reports/week/2026-45/\nGet it Tuesdays: https://skillmaxx.gilventures.ai/newsletter/\n\nWhat would make this more useful for your team?",
  "image": "scorecard card image",
  "refresh": true,
  "xnote": "",
  "alt": "Weekly scorecard card for week 45 (fill from weekly_scorecard.py)."
 },
 {
  "date": "2026-11-09",
  "dow": "Mon",
  "times": {
   "x": "9:30 AM",
   "bluesky": "7:30 PM",
   "linkedin": "12:00 PM"
  },
  "pillar": 7,
  "theme": "Q4: audit your agent setup before code freeze",
  "x": [
   "Q4 cleanup for your AI coding agent before the December code freeze:\n\n1. List every MCP server and plugin\n2. Remove what nobody used\n3. Pin marketplaces in install commands\n4. Write down your agent versions\n5. Re-check installs after the next update\n\nWhat's on your list?"
  ],
  "bluesky": [
   "q4 chore before december code freeze: open your AI agent's MCP config and remove every server nobody used this quarter. then pin marketplaces, note your agent versions, and re-check installs after the next update.\n\nhow many MCP servers are you running right now?"
  ],
  "linkedin": "A Q4 housekeeping list for teams using AI coding agents\n\nBefore December code freezes and holiday handoffs, 20 minutes on this saves a messy January:\n\n1. List every MCP server and plugin each agent loads.\n2. Remove what nobody used this quarter. Fewer tools in context, fewer surprises.\n3. Pin marketplaces in install commands (name@marketplace) so every laptop gets the same thing.\n4. Write down the agent versions you're on. When something breaks after an update, you'll know what changed.\n5. Re-check installs after the next agent update. We do that nightly and publish it free: https://skillmaxx.gilventures.ai/reports/latest/\n\nWhat's on your team's Q4 tooling list?",
  "image": "checklist card",
  "refresh": false,
  "xnote": "",
  "alt": "Checklist card with the 5 Q4 cleanup steps."
 }
]""")

def xlen(t): return len(re.sub(r"https?://\S+|"+re.escape(S)+r"\S*|anthropic\.com/\S+","x"*23,t))
def lens():
    probs=[]
    for d in D:
        if not 1<=len(d["x"])<=4: probs.append((d["date"],"x-count",len(d["x"])))
        for i,t in enumerate(d["x"]):
            if xlen(t)>280: probs.append((d["date"],"x",i+1,xlen(t)))
        if not 1<=len(d["bluesky"])<=3: probs.append((d["date"],"bsky-count",len(d["bluesky"])))
        for i,t in enumerate(d["bluesky"]):
            if len(t)>300: probs.append((d["date"],"bsky",i+1,len(t)))
        if not 350<=len(d["linkedin"])<=1400: probs.append((d["date"],"li",len(d["linkedin"])))
    return probs

if __name__=="__main__":
    here=pathlib.Path(__file__).parent
    pr=lens(); print("length problems:",pr)
    for d in D: d["pname"]=P[d["pillar"]]
    json.dump(D,open(here/"drafts-2026-10-27.json","w"),indent=1,ensure_ascii=False)
    o=["# Starter batch: Tue Oct 27 → Mon Nov 9, 2026 (DRAFTS)","","Status: DRAFT. Nothing queued in Buffer, nothing posted. Each post needs Brandon's OK. Generated from `drafts.py`; edit there and rerun.","Times are America/New_York. REFRESH = re-pull numbers the night before. X and Bluesky are threads: each numbered block is one post.",""]
    for d in D:
        o+=[f"## {d['dow']} {d['date']}: {d['theme']}", f"Pillar {d['pillar']} ({P[d['pillar']]}){' · REFRESH' if d['refresh'] else ''} · Image: {d['image'] or 'none'}"+(f" · Alt text: {d['alt']}" if d.get('alt') else ""),""]
        o+=[f"### X ({d['times']['x']}, {len(d['x'])}-post thread)"+(f" · {d['xnote']}" if d['xnote'] else "")]
        for i,t in enumerate(d["x"]): o+=[f"{i+1}/{len(d['x'])} ({xlen(t)}/280)","```",t,"```"]
        o+=[f"### Bluesky ({d['times']['bluesky']}, {len(d['bluesky'])} post{'s' if len(d['bluesky'])>1 else ''})"]
        for i,t in enumerate(d["bluesky"]): o+=[f"{i+1}/{len(d['bluesky'])} ({len(t)}/300)","```",t,"```"]
        o+=[f"### LinkedIn ({d['times']['linkedin']}) · {len(d['linkedin'])} chars","```",d["linkedin"],"```",""]
    (here/"DRAFTS-2026-10-27.md").write_text("\n".join(o))
