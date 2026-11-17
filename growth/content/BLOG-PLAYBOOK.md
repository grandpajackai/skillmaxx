# Weekly blog post playbook (SEO + AEO)

One post a week, written by the Sunday recap routine from a data brief. Everything else (per-agent pages,
best-by-category pages, per-skill "does it work" answers, sitemap, llms.txt) regenerates on every deploy from
the nightly data with no LLM and no credits.

## Inputs (free)
1. `python3 growth/scripts/weekly_post_brief.py --out growth/content/briefs/<YYYY-MM-DD>.md` (add `--suggest`
   for fresh Google autocomplete). Reads only committed repo files.
2. `growth/content/keywords.md` (plus the "GSC queries" section once Search Console is verified).
3. `growth/VOICE.md` for tone.

## Pick the angle (2 minutes)
- Choose the single most useful story in the brief: a pass-rate move of 1+ point for an agent, a well-known
  add-on that newly broke or got fixed, or a pattern (e.g. "npm MCP servers fail in Pi for one reason").
- Choose 1 primary query from the brief's "Target queries" (searcher wording), plus 2–3 secondary.
- If the brief has no real story (all changes under 1 point, nothing notable broke or got fixed), skip the
  week and say so in the run summary. Never pad.

## Write it (~800–1200 words)
- **Title / H1:** the primary query as a question or a direct claim with a number, e.g.
  "Which MCP servers work in Codex? 22 of 45 in our Nov 14 test". Under 65 characters if possible.
- **Answer first:** the first paragraph answers the H1 in 2–3 plain sentences with the number and the date
  ("As of Nov 14, 2026, …"). An answer engine should be able to quote it alone.
- **Question H2s:** 3–5 H2s phrased the way people search ("Why does X fail in Cursor?",
  "How do I install X in Claude Code?"). Each H2 opens with a 1–2 sentence direct answer, then detail.
- **Data table:** at least one HTML table from the brief (agent, before, after, change; or add-on, agents).
- **Dated facts only:** every number comes from the brief and names its run date. Mention the brief's
  caveats whenever a number is affected by them (harness changes, nights with no valid run).
- **Internal links (4+):** the relevant `/works-in/<agent>/`, `/best/<category>/`, 2+ `/skills/<slug>/`
  pages, `/reports/latest/` or the weekly scorecard, and `/how-we-test/`.
- **FAQ block:** 3–4 Q&As at the end via `{% set faqs = [...] %}{% set art = {...} %}{% include "faq.njk" %}`
  (it emits FAQPage + Article JSON-LD). Answers are standalone, 1–3 sentences, with the date.
- **No hype:** no "game-changing", "revolutionary", no superlatives the data doesn't show, no em-dash
  chains, no invented quotes, no pricing. Say "installs and loads in a sandbox", not "works perfectly".
- **Close:** one line on what we'll re-check next week, and the related-links row.

## File format
`src/blog/<slug>.njk`, copying the front matter of `src/blog/mcp-claude-code-vs-cursor.njk`:
`layout: base.njk`, `title`, `permalink: /blog/<keyword-slug>/` (primary query words, no date),
`tags: blog`, `issueDate: "YYYY-MM-DD"`, `ogType: article`, `desc` (≤155 chars, includes the number),
`jsonld` (BlogPosting with headline, datePublished, author/publisher Organization SkillMaxx). Body starts
with `<div class="wrap prose"><p class="muted">Mon D, YYYY · Data from run(s) …</p><h1 class="ph">…</h1>`
and ends with `{% include "nlembed.njk" %}`. New posts appear on /blog/, in the sitemap and in the
build automatically.

## Ship it
Branch `blog/<YYYY-MM-DD>`, PR, wait for the PR build (it runs `review/check_built_site.py`), squash-merge,
then curl the live URL once and add one line to STATUS.md. Never force-push.

## Checklist (paste into the PR body)
- [ ] H1 = primary query, answer in first paragraph with number + date
- [ ] 3–5 question H2s, each answered in its first sentence
- [ ] ≥1 data table; every number traceable to the brief
- [ ] caveats mentioned where they apply
- [ ] ≥4 internal links (works-in, best, 2 skill pages, report/how-we-test)
- [ ] FAQ include with 3–4 Q&As
- [ ] 800–1200 words, no hype, `desc` ≤155 chars
