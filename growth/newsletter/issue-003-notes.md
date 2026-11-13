# SkillMaxx Weekly #3: notes (draft, not sent)

Sends Tue 2026-11-10. Issue #2 (Nov 3) is final; anything below that's urgent can go into #2's Monday-night refresh instead.

## From X radar 2026-10-31
- **Safety (consider for #2's Monday refresh):** a tampered Anthropic.claude-code VS Code extension (2.1.312/2.1.313) was served from Cursor's extension marketplace on Oct 29 (~2:27 AM–1:35 PM PT), up to 5,000 users; it added an `svc-telemetry` SSH key and persistence. Not built by Anthropic; fixed in 2.1.314. Check: `grep svc-telemetry ~/.ssh/authorized_keys`. Sources: cursor.com/blog/claude-code-extension-security-notice, Microsoft Security blog (Oct 30). Angle: pin versions, don't let auto-update be your install policy. Not an add-on we test.
- **Expo joined Grok Build's official marketplace** (our Oct 31 re-fetch). Oct 31 nightly: clean in Grok Build, Claude Code and Codex; all 36 xAI Official plugins installed clean in Grok Build. (Trend post went out Oct 31.)
- Grok Build alpha 1.0.71–1.0.73: FastMCP/official-SDK MCP tools use about half the context; hooks accept `failClosed`. Our sandbox is still on grok 1.0.62.
- Claude Code "mods" (small in-terminal plugins: panels, commands) are a new add-on type; consider whether to list them.
- LiteLLM CVE-2026-114612 (GHSA-7hp6-4w63-5g45, CVSS 9.9): internal_user could become proxy_admin via the MCP stdio endpoint. Verify against the advisory before using.
- New to test: Renoise (Codex marketplace), Android skills (30+), Paweł Huryn's 43 product skills, Airbyte MCP, Vercel agent-desktop, Mollie plugins + MCP.

## From X radar 2026-11-01
- **Token cost tools are the week's theme:** Microsoft Research + UC Berkeley's TokenEconomizer (github.com/microsoft/TokenEconomizer) claims 18.4–30.9% cheaper agent runs in Claude Code, Codex, Copilot CLI and Pi (their benchmark, unverified by us). Add it to the nightly so we can report whether it installs in each.
- **Skill safety:** NVIDIA SkillSpector (github.com/NVIDIA/SkillSpector) scans skills for prompt injection and exfil before install; plus explainers on invisible Unicode Tag characters in skill files and the AGENTS.md trick that adds an MCP server to ~/.codex/config.toml. Possible "scan, then install-test" angle.
- **MCP goes mainstream:** Roblox's Q3 shareholder letter charts daily users of its MCP server (via @AndrewCurran_).
- Nov 1 nightly: 895 of 1,061 installs passed (30 of the 166 failures only need an API key).
- New to test: xdock, deskstats, text-to-cad, linkedin-mcp-server plugins, Open Design Agent Kit, K-Dense scientific-agent-skills.

## From X radar 2026-11-02
- **Stageshow (benjitaylor/skills)**: a faux-UI and cursor-demo skill from Benji Taylor (head of design at X), released Oct 31. His launch post has 1.33M views. Our sandbox check this morning: `npx skills add benjitaylor/skills` installed it for Claude Code, Codex, Cursor and Pi in one command. That was an install check only, not an output check. Trend post went out Nov 2.
- **TokenEconomizer follow-up**: the README installs register in Claude Code 2.1.197, Codex 0.163.0 and Pi 1.4.0 (box sandbox, Nov 2, ~10:10 AM ET). Its release notes pin tested ranges (Claude Code 2.1.300–2.1.310, Codex 0.153.1–0.164.0, Pi 1.2.0–1.3.0), so only our Codex falls inside one. Our sandbox Claude Code (2.1.197) is well behind current releases and is worth bumping before #3. No savings were measured.
- **second-read on Grok Build**: the marketplace adds, then install says "No marketplace plugin named second-read". Installing from a local clone works. The likely cause is the root `"source": "./"` in .claude-plugin/marketplace.json. Brandon is filing the issue. Angle: marketplace.json patterns that Claude Code accepts but Grok Build doesn't.
- **Gotcha**: a stray `.mcp.json` in a parent folder loads MCP servers into every session below it (via @giorgiafontane's thread).
- **Reddit API (unverified)**: jordanburke/reddit-mcp-server's README says Reddit stopped accepting new public Data API requests Oct 31, ends RSS Nov 13, and starts removal Jan 12 2027. Verify with Reddit before using.
- X news trends, headlines only: harness engineering, Anthropic blocking game recreations, invisible watermarks on older Claude models.
- New to test: Stageshow, deed-page-skill (author OK'd), second-read, TokenEconomizer (in nightly?), claude-workflow-recorder, Weasel icons skill, shadcn 100 charts MCP, Immersive Fusion observability MCP, REA (`npx rea-agents setup`). Gap: skills-CLI (`npx skills add`) installs aren't a run_tests.py test type yet.

## From X radar 2026-11-10
- **"One install, every agent" is the new launch pitch**: StarSling Skills (`npx skills add starslingdev/skills`, Claude Code/Codex/Cursor, via @DanKornas) and wshobson/agents both lead with cross-agent installs. Good test targets for the nightly.
- **Viral skill launch**: a "youtube agent skill" with 11 /yt-* commands for Claude Code hit 24.6k views and 750 bookmarks in a day (@TemsYanik). Repo not named yet.
- **MCP safety, unverified**: ha-mcp (Home Assistant) reportedly exposes 45 destructive tools out of 77 (@naveendas96's test).

## From X radar, Nov 11
- MCPJam Conformance: spec checks for MCP servers (protocol, OAuth, Apps, Tasks) with a score and fixes. https://x.com/mcpjams/status/2120279953912791399
- Modern Web Guidance 1.0 (Chrome, Firefox, Edge, MDN): agent skills that stop agents writing JS for things HTML/CSS do natively. https://x.com/LabubuNoBB/status/2120329614765768813
- Unverified: Mittwald says attackers came in through its MCP server, 56 customer projects compromised. Verify with a primary source first. https://x.com/botnewsnetwork/status/2120223376207999056

## From X radar, Nov 13
- Floorplan: Claude Code plugin that maps an app's files, endpoints and screens into a zoomable map; local, MIT. https://x.com/HeyGurisaroy/status/2121131247242301650
- Simular box: a cloud Ubuntu desktop that Claude Code, Codex and Cursor drive through one MCP server. https://x.com/benjaminwolfe_/status/2120917718891139177
- Skill Issue (@Palakonweb): agent skills ranked by real usage, with an MCP server for discovery. https://x.com/EveryDevAi/status/2121155103004708945
