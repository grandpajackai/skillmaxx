# Brandon's queue, Mon Nov 16, 2026 (~8:00 AM ET, daily queue routine)

Nothing here was posted or sent for him. Numbers: Nov 14 run (latest published: 910/1,070, 427 add-ons, new baseline). No Nov 15 or Nov 16 report published yet (both 404 at ~8:00 AM ET). Threads read via X API. @SkillMaxxAI hand-posted no replies since Nov 13; one unanswered reply to our Nov 14 Buffer post (@BlackSoilMo), listed as optional. Prior radar picks (Nov 13–15) are stale and dropped. Reddit still 403 from the box (old.reddit .json redirects to login): no comment drafts, no Reddit post on the plan. No LinkedIn accepts reported. X DMs: nothing new due (the Nov 1 DMs got their one follow-up in Monday Nov 9's queue; the rule is one follow-up, then stop).

## X replies (Open post + paste; no intent links)

1. @mattpocockuk "A brief history of AI Coding since Nov 2025" (392k followers, 1,040 likes, 115 replies, 44k views, posted 6:16 AM ET)
   https://x.com/mattpocockuk/status/2122287575557706226
   Context: his Mar entry says "Skills explosion... (superpowers already ahead of the game here)". Nobody in the thread asks about skills working across agents. Our data (Nov 14): superpowers passes in Claude Code, Codex, Grok Build and Pi; 40 add-ons pass in one agent but break in another.
   ```
   Superpowers being early shows in our data: it installs clean in Claude Code, Codex, Grok Build and Pi. SkillMaxx install-tests 427 agent add-ons across 5 coding agents nightly, and 40 pass in one agent but break in another. Does "works in every agent" make 2027's list?
   ```

2. @badlogicgames (Mario Zechner, Pi creator) pi-durable talk at the Vienna AI Engineering Meetup (81k followers, 295 likes, 18 replies, posted 6:06 AM ET)
   https://x.com/badlogicgames/status/2122285153871696290
   Context: read earendil.com/posts/pi-durable (Oct 1). Pi Durable is a separate harness; extensions are defineExtension bundles. The post doesn't say whether Pi coding-agent packages carry over. Thread asks what "durable" persists; nobody asks about packages. Our @SkillMaxxAI Pi-packages tip goes out at 9:30 AM ET today.
   ```
   Great talk. We run the Pi coding agent in our nightly install tests (SkillMaxx tests agent add-ons across 5 coding agents; 86 of 140 Pi installs passed in our last published run). Do Pi packages load into a Pi Durable registry as-is, or need a defineExtension port?
   ```

3. @rauchg introduces xeet, an X post renderer built as an "autorepo" (920k followers, 1,366 likes, 155 replies, posted 11:27 PM ET Sun)
   https://x.com/rauchg/status/2122184794209714368
   Context: Vercel is in our pipeline (form follow-up due today), so this is a no-pitch warm-up. xeet-rs.vercel.app covers wasm, the Rust crate and a CLI, with no skill or MCP mention. Thread already asks about A/B tests, regressions and Vercel OG.
   ```
   Verification engineering is the right name for it. We run the same idea on agent add-ons: SkillMaxx install-tests 427 skills, plugins and MCP servers in 5 coding agents nightly. With agents as half the audience, any plan to ship xeet as a skill or MCP tool for draft previews?
   ```

4. @DYoung_AI Google Labs' Stitch Design Skills (12.2k followers, 5 replies, posted 4:41 AM ET; repo is trending on GitHub today)
   https://x.com/DYoung_AI/status/2122263658508022180
   Tested ~8:05 AM ET: `npx skills add google-labs-code/stitch-skills --all -y` in a clean folder installed 16 skills, with folders named stitch-extract-design-md, stitch-manage-design-system and so on (from `stitch::` names). stitch-code-to-design's SKILL.md still links `../extract-design-md/SKILL.md` and `../manage-design-system/SKILL.md`, and those folders don't exist in this layout. The README lists npx skills as the selective path and warns about dependencies; it doesn't cover this.
   ```
   Ran npx skills add google-labs-code/stitch-skills --all in a clean folder: 16 skills landed as stitch-extract-design-md etc., but code-to-design still links ../extract-design-md/SKILL.md. SkillMaxx install-tests agent add-ons nightly. Anyone confirmed that handoff works?
   ```

5. Optional follow-up: @BlackSoilMo replied to our Nov 14 "Boring is a feature" post (MCP time server); not answered yet
   https://x.com/BlackSoilMo/status/2121639920934474099
   ```
   Agreed. That one's been the quietest server in our runs, which is exactly what you want under a long chain. Got a favorite boring one we should add to the nightly?
   ```

## LinkedIn connection picks (§0 verified)

- Rootly: Sylvain Kalache, Head of AI Labs / Developer Relations. Find: Sales Nav > Current company `Rootly` > Keywords `Sylvain Kalache`. Free: `Sylvain Kalache Rootly`
  Evidence: rootly.com/events/2026-running-production-with-agents (Oct 27 2026, "Our Head of AI Labs, Sylvain Kalache, moderated") · conf42.com Observability talk Sep 10 2026 (Head of AI Labs @ Rootly) · kube.fm interview Sep 22 2026 · sylvainkalache.com ("Currently leading developer relations and AI Labs at Rootly"). No newer role found.
  Checked live: the Rootly-AI-Labs/rootly-claude-plugin README (commit Nov 11) says "Moved to rootlyhq/agent-skills", but claude-plugins-official still points rootly at the legacy repo (sha 65832aa).
  Note: Hi Sylvain, the Rootly plugin installed clean in Claude Code and Grok Build in our latest nightly install tests. The README now says it moved to rootlyhq/agent-skills, but Claude's official directory still installs the legacy repo. Is that listing moving over? Would love to connect.
  (This is also the LinkedIn route for Rootly, #19 on BRANDON-OUTREACH.md. No pitch until after he accepts.)

- Confident AI (DeepEval): Jeffrey Ip, Founder/CEO. Find: Sales Nav > Current company `Confident AI` > Keywords `Jeffrey Ip`. Free: `Jeffrey Ip Confident AI`
  Evidence: ycombinator.com/companies/confident-ai (live Nov 16: Active Founders, Founder/CEO, creator of DeepEval) · his X @jeffr_yyy bio "Building production monitoring for AI @confident_ai", posting Confident AI launches Nov 9–10 2026. No newer role found.
  Checked live: skills/deepeval/SKILL.md hands off to the deepeval-tracing and deepeval-otel skills, but skills/README.md only installs `--skill "deepeval"` (npx) and only copies skills/deepeval (Claude Code).
  Note: Hi Jeffrey, the DeepEval plugin installed clean in Claude Code and Grok Build in our latest nightly install tests. The main deepeval skill hands off to deepeval-tracing and deepeval-otel, but the README's npx and copy steps install only deepeval. On purpose? Would love to connect.

- Sonatype: Brian Fox, Co-founder & CTO. Find: Sales Nav > Current company `Sonatype` > Keywords `Brian Fox`. Free: `Brian Fox Sonatype`
  Evidence: sonatype.com/resources/webinars/human-engineer-in-the-ai-era (Nov 19 2026 webinar, "Brian Fox, CTO at Sonatype") · Sonatype LinkedIn post on his FINOS OSFF talk and keynote (Nov 2026, "Co-founder and CTO"). No newer role found.
  Checked live: the sonatype-guide-claude-plugin README asks you to export SONATYPE_GUIDE_TOKEN in a shell profile; guide.sonatype.com/mcp says every config needs an API token. No OAuth mentioned.
  Note: Hi Brian, the Sonatype Guide plugin installed clean in Claude Code, Grok Build and Pi in our latest nightly install tests. Setup still asks for SONATYPE_GUIDE_TOKEN in a shell profile while more MCP servers move to OAuth. Is OAuth on the Guide roadmap? Would love to connect.

After they accept (tell me and I'll queue it): Thanks for connecting, {name}! / I run SkillMaxx, a free directory that install-tests 427 agent skills, plugins and MCP servers nightly across Claude Code, Codex, Cursor, Grok Build and Pi. / Site: https://skillmaxx.gilventures.ai / X: https://x.com/SkillMaxxAI · Bluesky: https://bsky.app/profile/skillmaxx.bsky.social / Anything you'd want us to test next?

## Founder video (Monday): "Our test was the bug" (~45s)
```
Vertical, phone, one take is fine.
0–5s, on camera: "Two nights last week, my tests said the most basic MCP servers were broken in every coding agent. They weren't. My test machine was."
5–20s, screen on skillmaxx.gilventures.ai/reports/2026-11-14/: "Every night we run about a thousand installs of agent add-ons in Claude Code, Codex, Grok Build, Cursor and Pi. On Nov 12 and 13, the official time, fetch and git servers failed in all five. The logs said 'uvx not found'. Our new test machine was missing the tool that launches them."
20–35s, back on camera: "We fixed the machine, not the results. Next night all three passed everywhere, and 910 of 1,070 installs passed, up from 863."
35–45s: "If we're going to call someone's tool broken, our side has to be right first. Every result has a log. It's free. Link in bio." On-screen URL: skillmaxx.gilventures.ai
```

## Build-in-public drafts (standalone, intent links OK)

- Our test was the bug (uvx missing on the new test machine)
  Link: https://x.com/intent/post?text=Our%20test%20was%20the%20bug.%0A%0AOn%20Nov%2012%20and%2013%2C%20the%20official%20time%2C%20fetch%20and%20git%20MCP%20servers%20%22failed%22%20in%20all%205%20agents%20we%20test.%20Logs%3A%20our%20new%20test%20machine%20lacked%20uvx%2C%20which%20launches%20them.%0A%0AFixed.%20Nov%2014%3A%20all%20three%20passed%20everywhere%2C%20and%20910%20of%201%2C070%20installs%20passed%20%28863%20before%29.
  ```
Our test was the bug.

On Nov 12 and 13, the official time, fetch and git MCP servers "failed" in all 5 agents we test. Logs: our new test machine lacked uvx, which launches them.

Fixed. Nov 14: all three passed everywhere, and 910 of 1,070 installs passed (863 before).
  ```

- 40 add-ons pass in one agent, break in another
  Link: https://x.com/intent/post?text=In%20our%20last%20published%20run%20%28Nov%2014%29%2C%2040%20agent%20add-ons%20installed%20clean%20in%20one%20coding%20agent%20and%20broke%20in%20another.%0A%0AWe%20test%20427%20add-ons%20nightly%20in%20Claude%20Code%2C%20Codex%2C%20Grok%20Build%2C%20Cursor%20and%20Pi.%0A%0ACheck%20%22works%20with%20every%20agent%22%20before%20you%20install.%20What%20should%20we%20test%20next%3F
  ```
In our last published run (Nov 14), 40 agent add-ons installed clean in one coding agent and broke in another.

We test 427 add-ons nightly in Claude Code, Codex, Grok Build, Cursor and Pi.

Check "works with every agent" before you install. What should we test next?
  ```

- Pass rates by agent
  Link: https://x.com/intent/post?text=Install%20pass%20rates%20by%20coding%20agent%2C%20Nov%2014%3A%0A%0AGrok%20Build%20354%2F386%0AClaude%20Code%20343%2F371%0ACodex%2095%2F119%0APi%2086%2F140%0ACursor%2032%2F54%20%28MCP%20servers%20only%29%0A%0AEach%20agent%20installs%20add-ons%20its%20own%20way.%20Which%20one%20do%20you%20install%20into%20first%3F
  ```
Install pass rates by coding agent, Nov 14:

Grok Build 354/386
Claude Code 343/371
Codex 95/119
Pi 86/140
Cursor 32/54 (MCP servers only)

Each agent installs add-ons its own way. Which one do you install into first?
  ```

## Carried (not repeated; only if not done)
- Fri Nov 13: LinkedIn requests to James Russo (HeyGen), Adonai Vera (Voxel51), Jason Zhou (Superdesign). Wed Nov 11: Tina Lei (Endor Labs), Chris Griffing (GitKraken), Nango follow-up to Bastien Beurier. Text in those queue files.

## Notes
- Final email follow-ups due today (Exa, Firecrawl, Composio, Browser Use, CodeRabbit, Skyvern, Bright Data, Apify, Browserbase, E2B, Axiom, Semgrep, Mem0, Parallel AI, Prisma, Amplitude, Aikido, Zapier, Linear, Vercel, Nimble, Carbone) belong to the 11 AM outreach run (Zoho API), not Brandon. Vercel's form had no reply; the @rauchg reply above is a no-pitch warm-up.
- Directory candidates: google-labs-code/stitch-skills (16 skills; Codex marketplace + `npx plugins add` for Claude Code/Cursor); rootlyhq/agent-skills (new canonical Rootly repo, 7 read-only skills; the official directory still points at the legacy repo).
- Skipped: @thsottiaux Codex "model at capacity" fix (1.7k replies, no angle of ours); Scandit (no verifiable named contact).
- Bluesky: nothing notable for Brandon.
