# SkillMaxx — STATUS (single source of truth)

**Every agent reads this before starting and appends to the Session log when done.** See [COLLABORATING.md](COLLABORATING.md).

## Current state (as of 2026-10-25)
- **Live:** https://skillmaxx.gilventures.ai (GitHub Pages, HTTPS enforced; Let's Encrypt cert valid to 2027-01-14). Old `grandpajackai.github.io/skillmaxx` 301-redirects.
- **Repo:** `grandpajackai/skillmaxx` (public), default branch `master`.
- **Newsletter:** Beehiiv publication *SkillMaxx's Newsletter* — https://skillmaxxs-newsletter.beehiiv.com/subscribe. Embed form ID `2487fe2a-f3f4-4080-86de-b965ea008f48` (homepage `#newsletter`), plus `attribution.js` in every page head; fallback link shown under the form.
- **Other forms:** `/submit/` and `/advertise/` post to formsubmit.co → skillmaxx@gilventures.ai.
- **Data:** 424 skills (372 plugins, 45 npm MCP packages, 7 MCP reference servers). Docs-verified installs: Claude Code 322, Codex 72, Grok Build 331, Cursor 7, Pi 0.
- **Sandboxed install tests (2026-10-25):** 803 / 902 pass — Claude Code 338/367, Codex 65/65, Grok Build 314/331, Cursor 29/52, Pi 57/87.
- **QA (2026-10-25):** 17/17 click tests, 812 pages crawled / 0 broken, axe clean on 7 key pages, no console errors or overflow at 1440 and 390 px.
- **Email:** Zoho Mail Free on gilventures.ai (skillmaxx@, info@). MX/SPF/Zoho TXT verified via dns.google; DKIM `zmail._domainkey` was missing on 2026-10-25 and re-added that day.
- **Cost:** $0.

## Open issues
- [ ] **formsubmit.co activation** for skillmaxx@gilventures.ai not confirmed — check the Zoho inbox for the one-time activation email, else /submit and /advertise entries are dropped.
- [ ] **Beehiiv Pro trial ends ~2026-11-02** — decide: downgrade to free (check the embed form still works) or pay.
- [ ] **Beehiiv form inner padding** is large; on 390 px the email field is cramped. Reduce padding/heading size in the Beehiiv form editor (can't style a cross-origin iframe from the site).
- [ ] **Grok Build ambiguous installs:** auth0, grafana-mcp, postman, pr-review-toolkit now need `@<qualifier>`; update listed commands.
- [ ] **Re-verify DKIM** resolves (`dns.google/resolve?name=zmail._domainkey.gilventures.ai&type=TXT`).
- [ ] **Nightly scheduling:** no cron on the box; the nightly relies on a Grok Bot routine (missed Oct 17–24 while usage was out). Since 2026-10-25 nightly.sh logs every run to testing/logs/nightly-<date>.log and names the failing step.
- [ ] **Stripe Payment Links pending** (Brandon connecting his Stripe account, up to 12 h). Then paste the 4 URLs into src/_data/sponsorLinks.json (success URL /sponsor/thanks/?slot=<key>); see growth/sponsors/PLAYBOOK.md.
- [ ] **Grok Build fails rose 17 → 25** in the 2026-10-25 22:00 re-run (795/902 pass overall vs 803); check whether these are flaky or new upstream breakage.
- [x] **Branch protection** on `master` enabled 2026-10-25: PR required, `build` check required (strict), no force-push/deletion, admins can bypass (for the nightly routine). Squash-merge + auto-delete branches on.

## In progress / claimed by
| Task | Agent | Branch | Since |
|---|---|---|---|
| _(none)_ | | | |

## Next up
0. Watch https://github.com/skillmatic-ai/awesome-agent-skills/pull/219 (opened 2026-10-25) and reply to review comments.
1. Confirm formsubmit activation and DKIM.
2. Fix the 4 ambiguous Grok Build install commands.
3. Decide on Beehiiv Pro vs free before ~Nov 2.
4. Tune Beehiiv form for mobile.
5. Growth (see growth/): approve the skillmatic PR draft, paste newsletter #1 into Beehiiv, create a Cloudflare account for Web Analytics, approve the outreach drafts (growth/outreach/).

## Session log
- **2026-10-25 · Grok Bot** — Catch-up refresh after Oct 17–24 missed nightlies: +videogen (424 skills), 803/902 tests pass (8 regressions, logged in testing/results/2026-10-25.json). Fixed /advertise mobile overflow and dishonest newsletter text. Swapped newsletter to Beehiiv embed + attribution with fallback link and styled wrapper (screenshots: review/beehiiv/). nightly.sh now builds for the custom domain. Added COLLABORATING.md, STATUS.md, PR CI workflow; enabled branch protection on master (landed via PR #1).
- **2026-10-25 · Grok Bot** — SEO/AEO pass (PR grokbot/seo-aeo-review): robots meta, twitter/og tags, og:type article, unique titles/descriptions on all 438 pages (dup skill names/descs disambiguated, double-escaping fixed), JSON-LD: WebSite+Organization, ItemList (homepage), SoftwareApplication+BreadcrumbList per skill, Article+FAQPage on guides and Article on issue #1; question H2s with direct answers + FAQ blocks + internal links on both guides; /newsletter/ archive + /newsletter/issue-1/; /llms.txt; robots.txt welcomes AI crawlers; sitemap with lastmod, 404 noindexed. Owner dashboard got a Content review section.
- **2026-10-25 · Grok Bot** — Growth workstream: growth/CHANNELS.md (25 channels ranked, rules checked: heilcheng excludes directories, travisvn bans AI-assisted PRs, awesome-claude-code takes issue-form submissions only, punkpeye is servers only), PR draft for skillmatic-ai/awesome-agent-skills (not opened), newsletter issue #1, SPONSORS.md (founding pricing, 12 targets), 3 cold-intro drafts (not sent), analytics recommendation (Cloudflare Web Analytics; needs an account). Nothing submitted, sent, or created.
- **2026-10-25 · Grok Bot**: Opened the external PR https://github.com/skillmatic-ai/awesome-agent-skills/pull/219 ("Add SkillMaxx" under Skill Marketplaces & directories) from the fork grandpajackai/awesome-agent-skills, branch add-skillmaxx.
- **2026-10-25 · Grok Bot**: New logo (check-X mark, option B of 3; see growth/brand/README.md) rolled out to the header, footer, favicon (svg/ico/png), apple-touch-icon, the new site.webmanifest and the OG image. Beehiiv assets are in growth/brand/beehiiv/ (upload to Beehiiv still to do). QA: click tests pass, 816 pages / 0 broken, axe clean, no console errors.
- **2026-10-25 · Grok Bot**: X kit in growth/x/ (profile, avatar/header, 35-post bank posts.json, 2 data charts, reply playbook, 20 follows). Nothing posted yet.
- **2026-10-25 · Grok Bot**: Finalized newsletter issue #1 (growth/newsletter/issue-001.md, Beehiiv copy issue-001-beehiiv.md with banner + $19 founding-sponsor line). Added data-driven SEO guides /guides/best-mcp-servers-cursor/ (29/52) and /guides/what-installs-in-grok-build/ (314/331), linked in footer "Guides", each with the Beehiiv embed (src/_includes/nlembed.njk).
- **2026-10-25 · Grok Bot**: /advertise/ now shows regular prices struck through ($49/issue, $79/mo, $29/mo category) beside founding prices ($19, $29, $15, $49 bundle) under a "Founding sponsor pricing, first 10 sponsors" badge; inquiry form options updated. SPONSORS.md aligned (first 10, was 5) and a Black Friday/Cyber Monday sponsor promo (Nov 27–30) noted. 390px: no overflow.
- **2026-10-25 · Grok Bot**: Nightly fix (PR #10). The Oct 25 ~2:06 AM ET failure left no trace because nightly.sh wrote no log; it also never committed/pushed data and its codex-mirror pull could abort on the locally renamed marketplace.json. nightly.sh now logs per run (testing/logs/, gitignored), takes a lock, names the failing step, resets+renames the mirror, retries fetch_meta, and pushes a data-only commit. Verified by a full run 21:51–22:00 ET: 795/902 pass, pushed as b5e210d. Sponsor setup (PR #11): Book now buttons on /advertise/ (scroll to inquiry with slot preselected; Stripe links drop into src/_data/sponsorLinks.json), /sponsor/thanks/ asset intake (formsubmit, noindex), media kit section with build-time stats only, growth/sponsors/PLAYBOOK.md and PIPELINE.md (12 targets, 0/10 founding booked). Stripe pending.
