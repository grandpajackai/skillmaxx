<!-- Paste into Beehiiv. Title / subtitle / preview text below; body starts at the first heading. -->
**Title:** This week in agent skills #1: we installed 902 things so you don't have to
**Subtitle:** 803 worked. The other 99 have stories.
**Preview text:** Four Grok installs broke overnight, Codex went 65 for 65, and a video plugin crashed the party.

---

## Hi, it's SkillMaxx 👋

Short version of what we do: we take every agent skill, plugin and MCP server we can find, install it in a fresh sandbox inside **Claude Code, Codex, Grok Build, Cursor and Pi**, and write down what happened. No vibes, just logs.

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

## Plot twist of the week: "which auth0 did you mean?"

Four plugins that installed fine on Oct 16 now fail in Grok Build: **auth0, grafana-mcp, postman, pr-review-toolkit**. Nothing about the plugins themselves broke. The same names now live in more than one marketplace, so `grok plugin install auth0 --trust` politely refuses and asks you to pin one with `auth0@<marketplace>`.

**Fix:** add the `@qualifier`. We're updating the commands on SkillMaxx to match.

## New in the directory

- **videogen** (Grok Build): text → video, image → video, script → MP4. It passed its install test on the first try. We're not saying it's showing off, but it's showing off.

## Crowd favorites (by GitHub stars)

- **superpowers**: about 305k ★
- **mattpocock-skills**: about 303k ★
- The official **MCP reference servers** (fetch, filesystem, git, memory, sequential-thinking, time): about 92k ★ each, and still the backbone of half the setups out there

## Things that didn't connect

- **cyanheads PubMed MCP** and **gdharness** failed to connect in Claude Code this week (they passed on Oct 16). gdharness also wants a Godot editor running, which is fair: it's a Godot harness.
- One Claude Code test (postiz) timed out talking to GitHub. That's flaky network, not the plugin. We'll retest.

## How we test (the 20-second version)

Fresh sandbox, no API keys, no credentials, real agent CLI. Pass means the agent itself lists the thing as installed or enabled (or, for MCP, connected). Every result links to its log. Details: https://skillmaxx.gilventures.ai/how-it-works/

---

**Find something that works in *your* agent →** https://skillmaxx.gilventures.ai

Built a skill? Submit it and we'll run it through all five agents: https://skillmaxx.gilventures.ai/submit/

See you next week. Fewer ambiguous auth0s, hopefully.
