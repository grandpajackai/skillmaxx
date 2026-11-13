<!-- Issue #3, Fri Nov 13, 2026. Numbers only from published data: src/_data/reports.json (Nov 8, Nov 12, Nov 13 runs), weeks.json (week 45 = Nov 2-8, 6 runs) and runNotes.json. Outside items come from growth/newsletter/issue-003-notes.md and are labeled "not tested by us yet". Archived at /newsletter/issue-3/. Paste-ready HTML: issue-003-beehiiv.html. -->
**Title:** SkillMaxx #3: new agents, new baseline, and a bug that was ours
**Subtitle:** We upgraded all 5 agents, skipped 3 nights we couldn't trust, and found one more mistake of our own.
**Preview text:** 863 of 1,070 installs passed on the new agent versions. Here's what that number does and doesn't mean.

![SkillMaxx](https://raw.githubusercontent.com/grandpajackai/skillmaxx/master/growth/brand/beehiiv/skillmaxx-banner-1200x300.png)

## hey, Brandon here 👋

Big week behind the scenes, and not all of it pretty. Here's the honest version.

**1. We moved to the latest agents.** Until Nov 8 our nightly tests ran on older agent versions. Since Nov 12 they run on current releases:

| Agent | Before (to Nov 8) | Now (from Nov 12) |
|---|---|---|
| Claude Code | 2.1.197 | 2.1.319 |
| Codex | 0.163.0 | 0.167.0 |
| Grok Build | 1.0.62 | 1.0.77 |
| Cursor | 2026.10.16 | 2026.11.05 |
| Pi | 1.4.0 | 1.5.0 |

You run the new versions, so that's what we should test. The catch: scores before and after Nov 12 aren't a like-for-like comparison, so we treat Nov 12 as a fresh start. Nothing gets called "broke" or "fixed" across that line.

**2. We skipped three nights on purpose.** On Nov 9, 10 and 11 a bug in our own test harness stopped Grok Build from scanning its Claude plugin marketplace, so lots of Grok Build installs "failed" for no fault of the add-ons. We fixed the harness and did not publish those three nights. They're marked "no valid run" on the [reports page](https://skillmaxx.gilventures.ai/reports/#no-valid-run). No numbers beat wrong numbers.

**3. One more mistake, also ours.** The new test sandbox was missing `uvx`, the tool that starts Python MCP servers. So MCP time, MCP fetch, MCP git and claimidx (20 installs across all 5 agents) failed on Nov 12 and 13. All 20 passed on Nov 8. Don't avoid those servers because of our report: treat them as untested until the next run on the fixed sandbox.

## 📊 The new baseline (Nov 13)

**863 of 1,070 installs passed** (82.6% of the 1,045 we can judge without an API key). Nov 12 was 866. The last run on the old versions, Nov 8, was 919.

So what's the drop? Of the installs that passed on Nov 8, 57 failed on Nov 12's new setup, and 4 went the other way. 20 of those 57 are the `uvx` mistake above. The rest we're re-checking on the new versions before we say anything about them.

**By agent on Nov 13** (installs we can judge without an API key; 5 per agent need a key):

| Agent | Passed | Rate |
|---|---|---|
| Claude Code | 332 / 366 | 90.7% |
| Grok Build | 345 / 381 | 90.6% |
| Codex | 86 / 114 | 75.4% |
| Pi | 77 / 135 | 57.0% |
| Cursor (MCP servers) | 23 / 49 | 46.9% |

**Standout:** [MCP sequential-thinking (reference)](https://skillmaxx.gilventures.ai/skills/mcp-sequential-thinking/) installed clean in all 5 agents on both new-baseline nights.

**Still wobbly on Nov 13** (failed once, re-checking): @cyanheads/pubmed-mcp-server and Airwallex Dev (Claude Code and Grok Build), @rigour-labs/mcp (Grok Build).

Full report: https://skillmaxx.gilventures.ai/reports/2026-11-13/ · What changed on Nov 12: https://skillmaxx.gilventures.ai/reports/2026-11-12/ · Is your tool safe today? https://skillmaxx.gilventures.ai/reports/latest/

## 🗓️ Last full week on the old versions (Nov 2 to 8, 6 runs)

**919 of 1,040** judgeable installs passed on Nov 8 (88.4%). **0** confirmed broke, **17** really fixed (including notion-mcp-server, which broke in issue #2, and the Clangd, Csharp, Gopls and Jdtls LSP plugins), **19** flip-flopped. Most reliable agent: Claude Code at 94.2%. Chart: https://skillmaxx.gilventures.ai/reports/week/2026-45/

## 👀 On our radar (not tested by us yet)

- **[Floorplan](https://x.com/HeyGurisaroy/status/2121131247242301650):** a Claude Code plugin that maps your app's files, endpoints and screens into a zoomable map. Local, MIT.
- **[Modern Web Guidance 1.0](https://x.com/LabubuNoBB/status/2120329614765768813):** agent skills, credited to the Chrome, Firefox, Edge and MDN teams, meant to stop agents writing JavaScript for things HTML and CSS already do.
- **[MCPJam Conformance](https://x.com/mcpjams/status/2120279953912791399):** spec checks for MCP servers (protocol, OAuth, Apps, Tasks) with a score and suggested fixes.
- **[Skill Issue](https://x.com/EveryDevAi/status/2121155103004708945):** agent skills ranked by real usage, with an MCP server for discovery.

Want one of these in the nightly run? Reply with the name.

## 🔧 Tip of the week

**Pin your agent version when something matters.** This week proved it: the same add-on can behave differently on a newer agent release. If an install breaks right after your agent auto-updates, check the agent's changelog before you blame the add-on.

## 🙏 Tell us

1. **One tool you want tested** before you install it.
2. **Did we get your tool wrong?** Send the link and we'll rerun it and fix the page.
3. **Was the honest-mistakes section useful, or too much inside baseball?**

I read every reply.

---

**Sponsor:** This spot is open. Founding rate: **$19 for 1 issue** (or **$59/mo for 4 issues**, about $15 each). Placements are always labeled; see https://skillmaxx.gilventures.ai/advertise/

Built a skill? We'll run it through all five agents: https://skillmaxx.gilventures.ai/submit/
