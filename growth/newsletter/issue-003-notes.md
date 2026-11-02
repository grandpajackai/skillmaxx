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
