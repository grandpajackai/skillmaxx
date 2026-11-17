# SkillMaxx keyword list (free sources)

Input for the weekly post (`growth/scripts/weekly_post_brief.py` matches this week's data against the
`- ` lines below) and for picking new answer pages. Keep one query per line, lowercase, real searcher wording.
Gathered 2026-11-16 from free sources: Google autocomplete (`suggestqueries.google.com`, client=firefox),
and Hacker News titles (hn.algolia.com, Sep–Nov 2026). Reddit's search API refused the box's requests, so
Reddit isn't in this pass; add titles by hand when you see them. Refresh autocomplete any time with
`python3 growth/scripts/weekly_post_brief.py --suggest` (free, no LLM).

**Google Search Console:** not connected yet. Once Brandon verifies the site (see "Search Console" at the
bottom), paste the top queries from Performance → Queries (last 28 days) into the "GSC queries" section.
Those beat everything else here because they're queries we already show up for.

## Compatibility / "does it work" (our strongest fit: answer pages + per-skill answers)
- mcp server not working cursor
- cursor mcp server not working
- cursor mcp server no tools or prompts
- cursor not detecting mcp server
- cursor not using mcp server
- codex mcp server not working
- mcp server not starting
- mcp server not showing up in claude desktop
- does mcp work with codex
- figma mcp server not working
- atlassian mcp server not working
- grok build vs claude code
- grok build vs cursor
- pi coding agent mcp
- pi coding agent vs claude code

## "Best X" lists (→ /best/<category>/ and /works-in/<agent>/)
- best mcp servers for claude code
- best mcp servers for codex
- best mcp servers for coding
- best mcp servers for developers
- best claude code plugins
- best claude code plugins for developers
- best claude code plugins for web development
- best claude code plugins and skills
- claude code plugins list
- codex plugins list
- cursor mcp servers
- cursor mcp list
- cursor mcp directory
- claude code skills directory
- claude code skills library
- claude code mcp servers

## How-to / setup (→ per-skill install commands, guides)
- how to install mcp server in claude code
- how to install mcp server in cursor
- how to install mcp server in codex
- claude code mcp config file location
- claude code mcp add
- codex mcp add
- codex mcp config
- cursor mcp.json
- claude code plugin marketplace add
- claude code plugin marketplace install
- grok build install
- pi coding agent install

## Concepts / comparisons (→ weekly posts)
- claude code plugins vs skills
- claude skills vs mcp
- claude skills vs mcp vs plugins
- codex plugins vs skills
- codex plugins vs mcp
- cursor rules vs skills
- skill.md vs agent.md
- skill.md format
- agent skills specification

## Safety (→ how-we-test, weekly posts)
- is mcp server safe to use
- are local mcp servers safe
- is github mcp server safe
- is playwright mcp server safe to use

## Topic signals from Hacker News (Sep–Nov 2026, by points)
- "MCP server that reduces Claude Code context consumption by 98%" (570): token/context cost of MCP
- "Agent Skills" (544, 376) and "SkillsBench: Benchmarking how well agent skills work" (364): skills quality/benchmarks
- "Show HN: Agent Skills Leaderboard" (135), "Agent-skills-eval" (79): demand for skill testing (our angle)
- "MCP-Scanner – Scan MCP Servers for vulnerabilities" (168), "The State of MCP Security" (38): MCP safety
- "Show HN: Mcp2cli – 96-99% fewer tokens than native MCP" (146): MCP vs CLI/skills
- "Agent skills that bring team coding standards to Claude Code and Codex" (75): cross-agent skills

## GSC queries
(empty until Search Console is verified)

## Search Console
DNS for gilventures.ai is on Namecheap BasicDNS (nameservers `dns1/dns2.registrar-servers.com`, checked
2026-11-16 via dns.google). The site itself is GitHub Pages (`skillmaxx.gilventures.ai` CNAME →
`grandpajackai.github.io`).
- **Fastest (URL-prefix property, HTML tag):** Search Console → Add property → URL prefix
  `https://skillmaxx.gilventures.ai/` → choose "HTML tag" → copy only the `content="…"` value → set it as the
  GitHub Actions *variable* `GOOGLE_SITE_VERIFICATION` (repo Settings → Secrets and variables → Actions →
  Variables) → re-run "Deploy to GitHub Pages" → click Verify. The build adds
  `<meta name="google-site-verification">` to every page only when that variable is set.
- **Alternative (Domain property, covers all of gilventures.ai):** Namecheap → Domain List → gilventures.ai →
  Advanced DNS → Add New Record → TXT, Host `@`, Value `google-site-verification=…` → Verify. Don't touch the
  existing Zoho MX/SPF/DKIM records.
- After verifying: Sitemaps → submit `https://skillmaxx.gilventures.ai/sitemap.xml`.
