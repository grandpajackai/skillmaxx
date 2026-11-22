# Sunday recap prep — week ending 2026-11-22 (generated 2026-11-22 02:55 EST on Mac)
<!-- prep {"cmd": "recap", "date": "2026-11-22", "generated": "2026-11-22 02:55 EST on Mac", "source_sha": "dee3023"} -->

Newsletter: issue #4 is already published for this week (src/newsletter/issue-4.md -> https://skillmaxx.gilventures.ai/newsletter/issue-4/, auto from the Mac, no LLM). No draft written. Optional polish = edit that file; the email send stays held.

Sunday blog post: https://skillmaxx.gilventures.ai/blog/week-2026-47/ exists (Mac weekly_blog_auto.py). It is the only Sunday post: check and link it, never write a second Sunday post.

Stats only. Wins/misses wording, the dashboard edit, optional newsletter polish and anything sent stay with Grok.

## Nightly runs, week 2026-47 (2026-11-16–2026-11-22)
- 2026-11-17: 911/1,075 passed (86.8% of tested)
- 2026-11-18: 912/1,075 passed (86.9% of tested)
- 2026-11-19: 906/1,075 passed (86.3% of tested)
- 2026-11-20: 906/1,075 passed (86.3% of tested)
- 2026-11-21: 862/1,085 passed (81.3% of tested)
- 2026-11-22: 831/1,085 passed (77.7% of tested)

## Agent ranking (summed over the week's runs)
- Claude Code: 2032/2208 (92.0%), flaky 20
- Grok Build: 2097/2298 (91.3%), flaky 21
- Codex: 546/696 (78.4%), flaky 8
- Pi: 486/822 (59.1%), flaky 17
- Cursor: 167/306 (54.6%), flaky 22
- fixed: [{"slug": "putervision-vision-memory-mcp", "name": "@putervision/vision-memory-mcp", "n": 2}, {"slug": "desktop-commander", "name": "Desktop Commander", "n": 1}, {"slug": "hyperframes", "name": "Hyperframes", "n": 1}, {"slug": "monday-crm", "name": "Monday Crm", "n": 1}]
- broke: [{"slug": "bitbonsai-mcpvault", "name": "@bitbonsai/mcpvault", "n": 5}, {"slug": "next-ai-drawio-mcp-server", "name": "@next-ai-drawio/mcp-server", "n": 5}, {"slug": "korean-law-mcp", "name": "korean-law-mcp", "n": 5}, {"slug": "putervision-vision-memory-mcp", "name": "@putervision/vision-memory-mcp", "n": 4}, {"slug": "aiterm-mcp", "name": "aiterm-mcp", "n": 4}]
- standout: {"slug": "mcp-time", "name": "MCP time (reference)", "desc": "Time and timezone conversion", "agents": ["claude_code", "codex", "grok_build", "cursor", "pi"], "why": null, "stars": 91859}

## Latest
- Latest published report: **2026-11-22** — 831/1,085 installs passed, 430 add-ons, 15 need a key. Live check: unchecked (HTTPError). https://skillmaxx.gilventures.ai/reports/2026-11-22/
- Per agent: Claude Code 329/374, Codex 79/122, Grok Build 341/389, Cursor 14/57, Pi 68/143
- Previous night: 2026-11-21 862/1,085

## Pipeline counts
- Contacted: 101
- Target: 26
- dm-closed: 7
- declined-warm: 4
- Replied: 4
- Bounced: 4
- call-only: 2
- blocked-form: 2
- x-only: 1
- opted-out: 1
- Contacted (unconfirmed): 1
- Warm - inbound: 1
- Sponsor emails logged sent (last 7 d, sent/*-email-results.json): 8

## Merged PRs, last 7 days
- #149 Log the Toolsmith Weekly reply
- #148 Add MIT license
- #147 Move Bluesky posting off Buffer so Instagram can use the free slot
- #146 data: nightly refresh 2026-11-21 (862/1,085)
- #145 Write launch-kit marketing-status.json at the end of Mac publish
- #144 Lamp mention: use Autonomous-provided overview for issue 4
- #143 Add weekly carousel content plan and v3 local generator
- #142 Fix nightly harness install bugs (mcp_name, claude plugin enable, _npx/uvx prewarm, 300s timeout)
- #141 Add standalone sponsor media kit page (/media-kit/)
- #140 Add nightly MCP/plugin SEO pages and log 2026-11-20 listing outreach
- #139 Add newsletter skeletons for issues #5 and #6
- #138 Add dated blog queue and 8 data-grounded drafts (Nov 25–Dec 20)
- #137 Add --animate MP4 mode and newsletter CTAs to v2 carousels
- #136 Add Lamp/lampOS newsletter mention and Autonomous inbound pipeline
- #135 Log AI Agents Listing sign-in and HeyClaude GitHub queue
- #134 Nov 20 listings, Telegram request channel & Carousel v2
- #133 Nov 20 CEO asks: fresh Sunday newsletter radar, subscribe P.S., directory tracking, first-subscriber alert, goals & local carousels
- #132 Sponsor outreach 2026-11-20: paused on Xata bounce, reconcile PIPELINE from Zoho Sent
- #131 Add official NestJS and Blender Core skills to the nightly catalog
- #130 data: nightly refresh 2026-11-20 (906/1,075)
- #129 data: nightly refresh 2026-11-19 (906/1,075)
- #128 test_autopublish: frozen fixtures (no drift after issue #4 / new posts)
- #127 Auto newsletter issue (Sun) + Wednesday blog post + single Sunday post guard + Monday newsletter check (no LLM, Mac)
- #126 prep recap: no-LLM weekly newsletter draft
- #125 Disable Mac Sunday Buffer top-up (avoid duplicate posts)
- #124 Grok-free routine prep briefs (X radar, queue, Bluesky, outreach, pipeline, recap)
- #123 data: nightly refresh 2026-11-18 (912/1,075)
- #122 publish_nightly: fix pass count in PR title
- #121 data: nightly refresh 2026-11-17 ()
- #120 Grok-free nightly publish from the Mac (+ Sunday blog/Buffer, alert fixes)
- #119 Directory submissions list + awesome-list PR log
- #118 Newsletter signup on every data, skill, report and blog page
- #117 Mac nightly: alert on no-results/killed runs + 06 ET intake dead-man
- #116 Add Cloudflare Web Analytics beacon
- #115 sitemap: list every /works-in/ and /best/ page
- #114 SEO/AEO content engine: data-driven answer pages, JSON-LD, sitemap/llms.txt, weekly post brief
- #113 docs: log Nov 16 day-to-day ops audit and Buffer refill
- #112 STATUS: form-submission alerts via box watcher
- #111 STATUS: log live intake end-to-end test
- #110 Queue rewritten Better Stack and Sourcery pitches for Nov 17
- #109 Test standalone Agent Skills nightly (type skill); add angular-testing
- #108 Mac nightly: fetch with explicit refspecs so origin/master is current
- #107 how-we-test: PickAPlugin Related directories link; Nov 16 queue, leads, Bluesky log
- #106 Mac nightly: failure alert, watchdog, image self-heal; gap pages for nights with no report
- #105 Sponsor pipeline weekly 2026-11-16: 25 new targets, due list (no sends)
- #90 Shorten SkillMaxx forms and prepare a real inbox

## Channels
- Bluesky: 15 followers, 36 following, 90 posts
- X radar/queue files this week: 2
- Blog files (latest): index.njk, mcp-claude-code-vs-cursor.njk, midweek-2026-47.njk, six-nights.njk, week-2026-47.njk
- Newsletter issues on site: issue-1.md, issue-2.md, issue-3.md, issue-4.md
- Stripe, Beehiiv subscriber count and X/Buffer analytics: not fetched here (Grok connectors).
