# SkillMaxx — one-page launch plan (draft, 2026-10-16)

**What:** Cross-agent directory of agent skills/plugins/MCP servers with install commands per agent (Claude Code, Codex, Grok Build, Cursor, Pi) + weekly email. Status labels: `documented` (official source publishes it) vs `unknown`. Add `tested` only once the CI test harness exists.

## Stack (≈$0/mo)
- **Site:** static site (Astro or Eleventy) generated from `data/skills.json`; one page per item + category + "works in X" pages for search traffic.
- **Hosting:** Cloudflare Pages free plan (unlimited static bandwidth, 500 builds/mo) or GitHub Pages (free, 100 GB/mo soft bandwidth). Recommend Cloudflare Pages.
- **Repo/CI:** GitHub free; GitHub Actions free for public repos (2,000 min/mo on private).
- **Analytics:** Cloudflare Web Analytics (free).
- **Domain:** see costs below.

## Newsletter options (verify prices at signup)
| Tool | Free tier | First paid tier |
|---|---|---|
| Beehiiv | Launch plan free up to 2,500 subs; built-in ad network | Scale ~ $43/mo (annual) |
| Kit (ConvertKit) | Free up to 10,000 subs (newer limit) | Creator from ~$33/mo (1k subs) |
| Buttondown | Free up to 100 subs | ~$9/mo (1k subs) |
| Substack | Free (10% of paid subs) | — (no native sponsor tools) |
Recommendation: **Beehiiv free** (sponsor network + referrals) — $0 until 2,500 subs.

## Nightly update pipeline (GitHub Actions cron, 02:00 ET)
1. Pull official catalogs: `anthropics/claude-plugins-official` marketplace.json, xAI Grok Build marketplace, OpenAI Codex catalog, `modelcontextprotocol/servers` + official MCP Registry, npm search (`keywords:mcp`), GitHub topic search (`claude-skill`, `agent-skills`, `mcp-server`).
2. Normalize → diff vs `skills.json` → open PR with new/changed/removed items; agent writes descriptions & categories.
3. Phase 2: in a throwaway container, run each agent's install command and record pass/fail → `tested` status.
4. Build + deploy to Cloudflare Pages on merge. Weekly: agent drafts "New this week" issue from diffs (owner approves sends at first).

## First sponsor targets (companies already shipping agent plugins/MCP)
Exa, Firecrawl, Tavily, Browser Use, Skyvern, TinyFish, Composio, Supabase, Neon, Sentry, Vercel, Context7/Upstash, CodeRabbit, PostHog. Comparable rate cards: CodexStacks $49/issue, $79/mo featured, $29/mo category; AI Indigo $199/30-day featured MCP; MCPHubz $399/mo Staff Pick. Launch pricing ~ $49/issue, $79/mo featured. **No outreach until owner approves.**

## Costs (all need owner approval before purchase)
| Item | Price | Notes |
|---|---|---|
| skillmaxx.dev | $12.20/yr Cloudflare (first yr reported $8.20–12.20); Porkbun $8.75 yr1 / $12.87 renew | available per RDAP 404 |
| Hosting, CI, analytics | $0 | free tiers |
| Newsletter | $0 to 2,500 subs (Beehiiv) | |
| Email for sponsors | $0 (forwarding via Cloudflare Email Routing) | |
| **Year-1 total** | **≈ $8–13** | |
Optional: skillsmaxx.com or agentskillmaxx.com $10.46/yr (Cloudflare) as a redirect.

## Milestones
Wk1: domain, site live with 50 items. Wk2: 300+ items via pipeline, newsletter signup. Wk3–4: first issue, post to X/HN/r/ClaudeAI, sponsor page live. Month 2: install testing → `tested` badges.
