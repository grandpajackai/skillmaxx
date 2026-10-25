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
- [ ] **Nightly scheduling:** no cron on the box; the nightly relies on a Grok Bot routine (missed Oct 17–24 while usage was out).
- [x] **Branch protection** on `master` enabled 2026-10-25: PR required, `build` check required (strict), no force-push/deletion, admins can bypass (for the nightly routine). Squash-merge + auto-delete branches on.

## In progress / claimed by
| Task | Agent | Branch | Since |
|---|---|---|---|
| Growth workstream (channels, PR drafts, newsletter #1, sponsor kit, analytics rec) | Grok Bot | grokbot/growth | 2026-10-25 |

## Next up
1. Confirm formsubmit activation and DKIM.
2. Fix the 4 ambiguous Grok Build install commands.
3. Decide on Beehiiv Pro vs free before ~Nov 2.
4. Tune Beehiiv form for mobile.
5. Sponsor outreach (needs Brandon's approval; see PLAN.md).

## Session log
- **2026-10-25 · Grok Bot** — Catch-up refresh after Oct 17–24 missed nightlies: +videogen (424 skills), 803/902 tests pass (8 regressions, logged in testing/results/2026-10-25.json). Fixed /advertise mobile overflow and dishonest newsletter text. Swapped newsletter to Beehiiv embed + attribution with fallback link and styled wrapper (screenshots: review/beehiiv/). nightly.sh now builds for the custom domain. Added COLLABORATING.md, STATUS.md, PR CI workflow; enabled branch protection on master (landed via PR #1).
