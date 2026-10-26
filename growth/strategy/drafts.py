# Source of truth for the 2-week starter batch. `python3 growth/strategy/drafts.py` regenerates DRAFTS-2026-10-27.md and checks lengths.
# Numbers are from the 2026-10-26 nightly run (src/_data/reports.json). Posts tagged REFRESH must be re-checked the night before.
import json, re, pathlib
S = "skillmaxx.gilventures.ai"
P = {1:"Results",2:"Know-how",3:"Report/newsletter CTA",4:"Sponsors",5:"News take",6:"Leaders",7:"Seasonal",8:"Community/BTS"}
D = []
def day(date, dow, time_x, time_b, time_l, pillar, theme, x, bsky, li, img="", refresh=False, xnote=""):
    D.append(dict(date=date, dow=dow, times=dict(x=time_x, bluesky=time_b, linkedin=time_l), pillar=pillar, theme=theme,
                  x=x, bluesky=bsky, linkedin=li, image=img, refresh=refresh, xnote=xnote))

day("2026-10-27","Tue","9:30 AM","9:30 AM","9:30 AM",1,"Launch + pinned post",
 ["We install agent skills & MCP servers in Claude Code, Codex, Grok, Cursor and Pi every night and write down what actually installs.\n\nLast night: 802 of 890 installs clean. The 88 misses are public too, with logs.\n\nWe're brand new. What should we test next? 👇",
  "Every result, every log, every night (free, no signup):\n"+S+"/reports/latest/"],
 "hi bluesky 👋 we're SkillMaxx. every night we install agent skills, plugins & MCP servers in Claude Code, Codex, Grok, Cursor and Pi, in a fresh sandbox with no API keys, and publish what works.\n\nbrand new and small. reply with a repo and we'll run it through all 5.\n\n"+S,
 "Why SkillMaxx exists\n\nEvery AI coding agent now has skills, plugins and MCP servers. Almost none of them tell you whether a given one installs in the agent you actually use. A README that says \"works with AI agents\" is a hope, not a test.\n\nSo every night we install them for real: 424 add-ons, 902 installs across Claude Code, Codex, Grok, Cursor and Pi, in fresh sandboxes with no API keys. Last night 802 of the 890 we could judge installed cleanly. The failures are published too, with logs, and we only call something broken after it fails two nights in a row.\n\nHonest disclaimer: we launched this month and we're small. So I'm asking:\n• What should we test next?\n• Would a weekly install scorecard be useful for your team, or is it noise?\n\nFree daily report: https://"+S+"/reports/latest/\nWeekly newsletter: https://"+S+"/newsletter/\n\nBrandon, founder",
 img="growth/profiles/pin-chart.png (pass-rate chart) on X and LinkedIn; Bluesky text + link card", xnote="2-post thread: link lives in post 2 so post 1 isn't link-throttled. Pin post 1.")

day("2026-10-28","Wed","9:30 AM","7:30 PM","12:00 PM",5,"News: Agent Skills moves to the AAIF",
 ["Agent Skills now lives at the Agentic AI Foundation, next to MCP. 1M skills, ~280M installs, 70+ platforms.\n\nA shared format means a skill *can* load everywhere. Whether it *does* install in your agent tonight is a separate question. That's the one we test."],
 "agent skills moved to the agentic ai foundation (same home as mcp). anthropic's numbers: 1M skills published, ~280M installs, 70+ platforms.\n\nportable format ≠ portable install. from our runs, the same skill can be clean in codex and flaky in pi. we'll keep checking.",
 "Agent Skills just got a neutral home.\n\nOn Oct 22 Anthropic donated the Agent Skills standard to the Agentic AI Foundation under the Linux Foundation, where MCP already lives. Their numbers: 1 million skills published, nearly 280 million installs, 70+ agent platforms.\n\nWhat it means for teams, in plain terms:\n1. One SKILL.md format can now load across Claude Code, Codex, Cursor, Copilot and more. Less re-packaging per tool.\n2. The roadmap proposes versioned releases and security guidance for people who install skills. Worth watching.\n3. A shared format is not the same as \"works in your agent today\". In our nightly runs, the same add-on can install cleanly in one agent and fail in another.\n\nThat third point is why we test installs every night and publish the logs.\n\nWhat would you want a skills security guide to cover?\n\nSource: https://www.anthropic.com/news/donating-agent-skills-to-the-agentic-ai-foundation",
 img="X: none (text wins for takes). LinkedIn: simple quote card with the 3 numbers")

day("2026-10-29","Thu","9:30 AM","7:30 PM","12:00 PM",8,"Test request call-out",
 ["Taking test requests.\n\nReply with one skill, plugin or MCP server you almost installed but didn't trust. We'll run it in Claude Code, Codex, Grok, Cursor and Pi tonight and reply with the logs.\n\nNo catch. We're new and need to know what you actually care about."],
 "open call: reply with a repo you've been side-eyeing. skill, plugin or mcp server.\n\nwe'll run it through claude code, codex, grok, cursor and pi tonight and reply here with what happened, logs included.\n\n(we're new. this is how we learn what matters.)",
 "A question for anyone rolling out AI coding agents to a team:\n\nWhat's the one skill, plugin or MCP server you'd want checked before it goes on everyone's machine?\n\nComment the name or repo. We'll install it tonight in Claude Code, Codex, Grok, Cursor and Pi, in a clean sandbox, and reply with the results and the logs. Free, no strings.\n\nWe're a month old, and this is how we decide what to test next.",
 img="none")

day("2026-10-30","Fri","9:30 AM","7:30 PM","12:00 PM",2,"Myth: stars mean it works",
 ["Myth: lots of GitHub stars = it'll install fine.\n\nStars measure interest. Installs measure installs.\n\nSuperpowers has both (305k⭐ and clean in 4 agents with zero flakes). Plenty of starred repos don't. Check the log before you check the star count."],
 "myth: stars mean it installs.\n\nsuperpowers: 305k stars and clean in 4 agents, zero flakes this week. nice.\nplenty of other well-starred repos: not so much.\n\nstars measure interest. a clean install two nights running measures installs.\n"+S+"/skills/superpowers/",
 "Myth vs. reality for teams choosing agent add-ons\n\nMyth: a repo with lots of GitHub stars will install cleanly in your agent.\nReality: stars measure interest. They say nothing about whether it installs in the agent your team uses.\n\nOur rule of thumb after a month of nightly tests:\n• Check that it lists your agent by name, not \"works with AI agents\".\n• Look for an exact install command per agent.\n• Prefer things with two clean nights in a row over things with one viral week.\n\nOne that passes all three this week: Superpowers, clean in 4 agents with zero flaky runs.\nhttps://"+S+"/skills/superpowers/\n\nWhat's your own rule for trusting an add-on?",
 img="optional screenshot of the Superpowers skill page row", refresh=True)

day("2026-10-31","Sat","11:00 AM","5:00 PM","10:00 AM",7,"Halloween: scariest install log",
 ["Happy Halloween. The scariest thing in our logs this week wasn't a crash.\n\nIt was a tool that passed one night, failed the next, then passed again. 13 of those. We call them flaky and refuse to count them either way.\n\nWhat's the spookiest install you've hit? 🎃"],
 "happy halloween 🎃 the scariest thing in our logs isn't a crash. it's an install that passes, fails, then passes again.\n\n13 add-ons did that this week. we label them flaky and don't count them for or against anyone.\n\nwhat's the worst install you've lived through?",
 "Happy Halloween from SkillMaxx.\n\nThe scariest thing we saw in our logs this week wasn't a hard failure. A crash is easy: you see it, you fix it.\n\nThe scary ones are flaky: an install that passes one night, fails the next, then passes again. We saw 13 of those this week. We now label them flaky and leave them out of both the pass and the fail column, because shouting \"broken!\" after one bad night isn't fair to the people who build these tools.\n\nWhat's the most haunted install you've dealt with?",
 img="optional: dark-mode screenshot of a flaky row", refresh=True)

day("2026-11-01","Sun","6:00 PM","6:00 PM","10:00 AM",3,"Weekly scorecard (week 44) + DST",
 ["Week 44 install scorecard:\n• 802/890 installs clean (90.1%)\n• Broke 2 nights running: 2 installs\n• Really fixed: 0\n• Flaky, not counted: 13\n• Most reliable agent: Codex, 65/65\n\nClocks went back today. Our run is in UTC. It slept fine.\n\n"+S+"/reports/week/2026-44/"],
 "week 44 install scorecard 📊\n802/890 clean (90.1%)\nconfirmed broke: 2 installs\nreally fixed: 0\nflaky, not counted: 13\nmost reliable: codex, 65/65\n\nclocks went back today. our run is on UTC so it slept fine.\n"+S+"/reports/week/2026-44/",
 "Week 44 agent install scorecard\n\n• 802 of 890 judgeable installs clean (90.1%)\n• Confirmed broken after two nights: 2 installs\n• Really fixed this week: 0\n• Flaky results we refused to count: 13\n• Most reliable agent: Codex, 65 of 65\n\nIt's an ecosystem scorecard, not an agent ranking: it shows how well add-ons ship for each agent, in a sandbox with no API keys.\n\nThe full week, with logs: https://"+S+"/reports/week/2026-44/\nThe same scorecard lands in your inbox Tuesdays: https://"+S+"/newsletter/\n\nWhat should we add to next week's scorecard?",
 img="scorecard card image (render from weekly_scorecard.py output)", refresh=True)

day("2026-11-02","Mon","9:30 AM","7:30 PM","12:00 PM",2,"Install tip: pin the marketplace",
 ["Claude Code tip: install with the marketplace pinned.\n\n/plugin install sentry@claude-plugins-official\n\nThe @ part isn't decoration. Same plugin names now live in 2+ marketplaces, and without it your agent stops to ask which one you meant."],
 "claude code tip: pin the marketplace.\n\n/plugin install sentry@claude-plugins-official\n\nsame plugin names now exist in 2+ marketplaces. skip the @ and the agent asks \"which one?\". pin it, move on.\n\nnewsletter #2 is out tomorrow, free: "+S+"/newsletter/",
 "Monday tip for anyone standardizing Claude Code across a team:\n\nInstall plugins with the marketplace pinned:\n/plugin install sentry@claude-plugins-official\n\nWhy it matters: the same plugin names now exist in more than one marketplace. Without the @marketplace part, the agent stops and asks which one you meant, and in a shared setup script that's how two laptops end up with two different plugins.\n\nPut the pinned form in your onboarding docs and you'll never debug that one.\n\nWe test installs like this every night across 5 agents. Our free weekly newsletter (issue #2 is out tomorrow) has one tip like this plus the scorecard: https://"+S+"/newsletter/",
 img="terminal screenshot of the pinned install command")

day("2026-11-03","Tue","9:30 AM","7:30 PM","12:00 PM",3,"Newsletter #2 is out",
 ["SkillMaxx Weekly #2 is out: what installed, what broke two nights running, one install tip, zero fluff.\n\nIt's free. Hit reply and tell us if it's useful or noise. We actually read them."
  ,"Subscribe here: "+S+"/newsletter/"],
 "SkillMaxx Weekly #2 just went out 📬 scorecard, what broke two nights running, one install tip.\n\nfree. reply to the email and tell us if it's useful or noise, we read every one.\n"+S+"/newsletter/",
 "Issue #2 of SkillMaxx Weekly went out this morning.\n\nWhat's inside:\n• The weekly install scorecard across Claude Code, Codex, Grok, Cursor and Pi\n• What broke two nights in a row (and what we refused to call broken)\n• One install tip you can paste today\n\nIt's free, about a 3-minute read, and I'd genuinely like to hear if it's useful or noise. Every reply gets read.\n\nhttps://"+S+"/newsletter/\n\nBrandon",
 img="newsletter header image", xnote="2-post thread, link in post 2.")

day("2026-11-04","Wed","9:30 AM","7:30 PM","4:00 PM",6,"Leaders: Cursor's Agent SDK and computer use",
 ["Cursor shipped computer control and an Agent SDK in the same stretch: agents as code, prompts in Markdown, tools in TypeScript.\n\nThe trend: agents pick up more tools faster than anyone tests them. More reason to know what installs before your agent does."],
 "cursor's agent SDK (prompts in markdown, tools in typescript) plus desktop control in one stretch. busy team.\n\nfrom our side: cursor is the agent where add-ons most often install but don't report \"ready\". 27/52 last night. more tools, more reasons to check.",
 "What Cursor's last two launches tell us about where coding agents are going\n\nIn quick succession Cursor shipped (1) agents that can drive desktop apps like the iOS Simulator, and (2) an Agent SDK: agents defined as code, prompts in Markdown, tools in TypeScript, with built-in evals.\n\nThe lesson for teams isn't \"switch tools\". It's that agents are gaining capabilities faster than most teams can vet them. Every new tool an agent can call is one more thing that has to install, connect and behave.\n\nTwo practical habits:\n1. Keep a short allow-list of add-ons your team has actually verified.\n2. Re-check after agent updates. In our runs, Cursor is where add-ons most often install but don't report \"ready\" (27 of 52 last night, without API keys).\n\nHow is your team vetting new agent tools?",
 img="none on X; LinkedIn: per-agent pass chart", refresh=True)

day("2026-11-05","Thu","9:30 AM","7:30 PM","12:00 PM",4,"Tool authors + how sponsorship works",
 ["Tool authors: listed for one agent but quietly work in three? Most do.\n\nSubmit yours and we'll show you the logs for Claude Code, Codex, Grok, Cursor and Pi, good or bad. Free.\n\n(We have sponsor slots too. Money never changes a test result. Ever.)"],
 "if you build a skill or mcp server: submit it and we'll show you how it installs in claude code, codex, grok, cursor and pi, logs and all. free.\n\nwe also sell clearly-labeled sponsor slots. paying never changes a result.\n"+S+"/submit/",
 "For teams who build agent skills, plugins or MCP servers\n\nTwo ways to work with SkillMaxx:\n\n1. Free: submit your tool and we'll install it every night in Claude Code, Codex, Grok, Cursor and Pi, with the exact install command for each and the logs, good or bad. Most tools listed for one agent turn out to work in two or three more.\nhttps://"+S+"/submit/\n\n2. Paid, clearly labeled: founding sponsor slots (featured listing, newsletter, category page) from $15. The first 10 sponsors lock the founding rate for 6 months.\nhttps://"+S+"/advertise/\n\nThe one rule: money never changes a test result or a ranking. If a sponsor's tool fails, the site says so, and we'll help fix it.\n\nAudience is small and early, and we share real numbers with every sponsor monthly.",
 img="none")

day("2026-11-06","Fri","9:30 AM","7:30 PM","12:00 PM",1,"How we test (and our limits)",
 ["How a SkillMaxx test works:\n1. fresh sandbox\n2. the real agent CLI\n3. zero credentials\n4. pass = the agent itself lists it installed (or connected, for MCP)\n5. broken = fails 2 nights in a row\n\nWhat it doesn't prove: that the tool is good. Just that it installs."],
 "how we test, honestly:\nfresh sandbox, real agent CLI, no API keys.\npass = the agent itself says installed/connected.\nbroken = fails 2 nights running.\n\nwhat it doesn't prove: that the tool is good at its job. got one wrong? tell us, we'll rerun it.\n"+S+"/how-we-test/",
 "How we test, including what it can't tell you\n\nEvery night, for each add-on and each agent:\n1. A fresh sandbox, the real agent CLI, no credentials.\n2. Pass means the agent itself lists the add-on as installed, or connected for MCP servers.\n3. Broken means it failed two nights in a row. One bad night is \"pending\"; pass/fail/pass is \"flaky\".\n4. Failures that only need an API key get their own label, so nobody gets blamed for our missing keys.\n\nWhat a pass doesn't prove: that the tool does its job well. It proves it installs and connects in that agent today.\n\nIf you think we got your tool wrong, tell us and we'll rerun it.\nhttps://"+S+"/how-we-test/",
 img="simple 4-step diagram")

day("2026-11-07","Sat","11:00 AM","5:00 PM","10:00 AM",8,"What we got wrong: flaky vs broken",
 ["Something we got wrong: we used to mark a tool \"broken\" after one failed install. But some just fail randomly. Qodo failed one night and passed the next.\n\nNow a tool only counts as broken after it fails two nights in a row, and one-off failures are labeled flaky.\n\nHow do you tell flaky from actually broken in your setup?"],
 "something we got wrong early on: we called a tool \"broken\" after one failed install. but some installs just fail at random. qodo failed one night, passed the next.\n\nnow broken = fails two nights in a row. one-offs get labeled flaky.\n\nhow we decide: skillmaxx.gilventures.ai/guides/flaky-vs-broken/",
 "One rule we changed in SkillMaxx's first month\n\nWe used to mark a tool \"broken\" the first time its install failed. That turned out to be wrong. Some installs fail at random: a slow network, a registry hiccup, a timing issue. Qodo failed one night and passed the next, and we had already called it broken.\n\nSo we changed the rule:\n• Broken means it failed two nights in a row.\n• One bad night is pending, not broken.\n• Pass, fail, pass is labeled flaky and left out of both columns.\n\nThe lesson for teams running AI agents: one red result is a signal, not a verdict. Re-run before you rip a tool out, and track flakiness separately so it doesn't hide real breakage or get blamed on the tool's author.\n\nHow does your team tell flaky from actually broken?\n\nThe full write-up: https://skillmaxx.gilventures.ai/guides/flaky-vs-broken/\n\nBrandon",
 img="simple flaky vs broken status card (two rows: pass/fail/pass = flaky, fail/fail = broken). Bluesky alt text: Status card. Flaky: pass, fail, pass across three nights, not counted. Broken: fail two nights in a row.")

day("2026-11-08","Sun","6:00 PM","6:00 PM","10:00 AM",3,"Weekly scorecard (week 45)",
 ["Week 45 install scorecard:\n• [pass]/[judgeable] installs clean ([%])\n• Confirmed broke (2 nights): [n]\n• Really fixed: [n]\n• Flaky, not counted: [n]\n• Most reliable agent: [agent]\n\nWhat should we add next week?\n"+S+"/reports/week/2026-45/"],
 "week 45 install scorecard 📊\n[pass]/[judgeable] clean ([%])\nconfirmed broke: [n]\nreally fixed: [n]\nflaky, not counted: [n]\nmost reliable: [agent]\n\nreply with what we should test next week.\n"+S+"/reports/week/2026-45/",
 "Week 45 agent install scorecard\n\n• [pass] of [judgeable] installs clean ([%])\n• Confirmed broken after two nights: [n]\n• Really fixed: [n]\n• Flaky results we refused to count: [n]\n• Most reliable agent: [agent]\n\nFull week with logs: https://"+S+"/reports/week/2026-45/\nGet it Tuesdays: https://"+S+"/newsletter/\n\nWhat would make this more useful for your team?",
 img="scorecard card image", refresh=True)

day("2026-11-09","Mon","9:30 AM","7:30 PM","12:00 PM",7,"Q4: audit your agent setup before code freeze",
 ["Q4 checklist before the December code freeze:\n\n☐ list every MCP server your agent loads\n☐ remove the ones nobody used this quarter\n☐ pin marketplaces in install commands\n☐ re-check installs after the next agent update\n\nFuture-you in January says thanks."],
 "q4 chore before code freeze: open your agent's mcp config and delete every server nobody touched this quarter.\n\nfewer servers = fewer tools in context, fewer things to break after the next agent update.\n\nhow many are you running right now? be honest.",
 "A Q4 housekeeping list for teams using AI coding agents\n\nBefore December code freezes and holiday handoffs, 20 minutes on this saves a messy January:\n\n1. List every MCP server and plugin each agent loads.\n2. Remove what nobody used this quarter. Fewer tools in context, fewer surprises.\n3. Pin marketplaces in install commands (name@marketplace) so every laptop gets the same thing.\n4. Write down the agent versions you're on. When something breaks after an update, you'll know what changed.\n5. Re-check installs after the next agent update. We do that nightly and publish it free: https://"+S+"/reports/latest/\n\nWhat's on your team's Q4 tooling list?",
 img="checklist card")

def lens():
    probs=[]
    for d in D:
        for i,t in enumerate(d["x"]):
            n=len(re.sub(r"https?://\S+|"+re.escape(S)+r"\S*","x"*23,t))
            if n>280: probs.append((d["date"],"x",i,n))
        if len(d["bluesky"])>300: probs.append((d["date"],"bsky",len(d["bluesky"])))
        if not 350<=len(d["linkedin"])<=1400: probs.append((d["date"],"li",len(d["linkedin"])))
    return probs

if __name__=="__main__":
    here=pathlib.Path(__file__).parent
    pr=lens(); print("length problems:",pr)
    json.dump(D,open(here/"drafts-2026-10-27.json","w"),indent=1,ensure_ascii=False)
    o=["# Starter batch: Tue Oct 27 → Mon Nov 9, 2026 (DRAFTS)","","Status: DRAFT. Nothing queued in Buffer, nothing posted. Each post needs Brandon's OK. Generated from `drafts.py`; edit there and rerun.","Times are America/New_York. REFRESH = re-pull numbers from `src/_data/reports.json` / `testing/weekly_scorecard.py` the night before.",""]
    for d in D:
        o+= [f"## {d['dow']} {d['date']}: {d['theme']}", f"Pillar {d['pillar']} ({P[d['pillar']]}){' · REFRESH' if d['refresh'] else ''} · Image: {d['image'] or 'none'}",""]
        o+= [f"### X ({d['times']['x']})"+(f" · {d['xnote']}" if d['xnote'] else "")]
        for i,t in enumerate(d["x"]): o+= [f"Post {i+1}:" if len(d['x'])>1 else "", "```", t, "```"]
        o+= [f"### Bluesky ({d['times']['bluesky']}) · {len(d['bluesky'])}/300","```",d["bluesky"],"```",f"### LinkedIn ({d['times']['linkedin']}) · {len(d['linkedin'])} chars","```",d["linkedin"],"```",""]
    (here/"DRAFTS-2026-10-27.md").write_text("\n".join(o))
