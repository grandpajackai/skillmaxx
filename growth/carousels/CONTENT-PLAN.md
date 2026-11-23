# SkillMaxx weekly carousel content plan

**Date:** 2026-11-20  
**Status:** Live cadence is 1–3 carousels a week (see below). First deck scheduled 2026-11-23.  
**Source research:** `/workspace/carousels-samples/research/muse-skillmaxx-viral-research-2026-11-20.md` (read-only public research, 20 Nov 2026). Used for hook formulas, slide structure, hashtags, watch accounts, and timely-news *topics*. Treat figures in that file as a snapshot, not live facts. Vendor claims stay flagged. Unverified numbers are never copied onto slides.

**Current operational default:** newsletter CTA (`https://skillmaxx.gilventures.ai/newsletter/`) until Brandon picks a comment-keyword path. See §8.

**Cadence in the weekly / daily social top-up (as of 2026-11-23):** **1–3 carousels a week** across X, LinkedIn, and Instagram (Instagram once the account is restored). The four-deck research calendar below is a later target, not the live queue. First live deck: `src/assets/social/carousels/2026-11-23-pass-rate-correction/` (Issue #4 pass-rate correction, scheduled 2026-11-23).

---

## 1. Weekly calendar

Aligned to the eight pillars in `growth/strategy/CONTENT-STRATEGY.md` and the existing daily themes. Carousels are a format on top of that rhythm, not a second editorial calendar.

**Core cadence: four carousels a week (Tue, Wed, Fri, Sun).** Monday is optional when the nightly numbers make a strong how-to hook. Thursday and Saturday stay text-first unless the data (new confirmed breaks, pending/flaky lists, or a seasonal window such as BFCM Nov 27–30) justifies a deck. This keeps production cheap and leaves room for a same-day big-event jump (`≥1k★` tool confirmed broken two nights, or an agent update breaking `≥3` installs — DECISIONS / CONTENT-STRATEGY).

Every deck is rendered twice: **1080×1350** (Instagram, LinkedIn, X) and **1080×1920** (TikTok Photo Mode). Same copy and numbers; taller canvas only. Captions follow the platform playbook in CONTENT-STRATEGY (X: 0–1 hashtag, no link in the main post; Bluesky: link inline; LinkedIn: image post with the link in the body). Hard CTAs still respect the existing “≤2 CTA posts/week” guardrail — the Sunday scorecard plus one mid-week newsletter or keyword ask.

| Day | Theme | Pillars | Carousel | What the generator actually reads |
|---|---|---|---|---|
| Mon (optional) | Install tip / how-to | 2 Industry know-how | `orgchart` — “the stack that actually installed” | `src/_data/reports.json` → `by.claude_code.{pass,broken,total,needs_key}`; `src/_data/latestRows.json` → `rows[].{s,a,st}`; `data/skills.json` items + `data/meta/meta.json` stars/category |
| Tue | Results receipt | 1 Results, 3 Report/newsletter | `news` — last night’s install report | `reports.json` → `date`, `pass`, `tested`, `total`, `broken`, `fail`, `needs_key`, `broke[]`, `fixed[]`, `added[]`, `versions`, `by.<agent>.{pass,total,broken,fail,flaky,needs_key}` |
| Wed | News take | 5 Viral news commentary, 6 Leaders (education only) | `timely` — one story per slide from a **fresh** HN/radar pull at render time | `growth/scripts/fetch_radar_hn.py` (live) or `--radar-json`; optional context only from `reports.json` `versions` and pass counts. **Never** paste research-file figures |
| Thu (optional) | Test request / community, or sponsor on alternate weeks | 8 Community, 4 Sponsorships | Usually a text post, not a carousel. If a deck: “needs a second night” from pending/flaky | `reports.json` → `pending_list[]`, `flaky_list[]`, `added[]`, `removed[]` (`slug`, `name`, `agent`) |
| Fri | Myth vs reality / how we test | 2 Know-how, 1 Results | `maxxing` — honest fails + 5/5 elite | `reports.json` → `by`, `broken`, `pass`, `tested`, `addons`; `latestRows.json` for 5-agent status; `weeks.json` → `trend[]`, `broke_n`, `fixed_n`, `flaky_n` |
| Sat (optional) | Build in public / seasonal | 8 Community, 7 Seasonal | Only in a calendar window (e.g. Founding 12 / BFCM, DECISIONS #6) or a genuine build-in-public hook | Seasonal copy from DECISIONS; numbers still from `reports.json` / `weeks.json` |
| Sun | Weekly scorecard + newsletter CTA | 3 Report/newsletter | `leaderboard` | `src/_data/weeks.json` → `key`, `start`, `end`, `runs`, `ranking[]` (`agent`,`name`,`pass`,`tested`,`rate`,`flaky`,`needs_key`), `trend[]` (`date`,`pass`,`tested`,`rate`), `fixed[]`, `broke[]`, `standout` |

### Data contract (no invented numbers)

The generator (`growth/carousels/generate.py`) loads only committed nightly data:

- `src/_data/reports.json` — one object per night. Latest is selected by `date` (or `--date`).
- `src/_data/weeks.json` — ISO week rollups, matched when `start ≤ report.date ≤ end`.
- `src/_data/latestRows.json` — `{date, rows:[{s, a, st}, ...]}` per-skill per-agent status.
- `data/skills.json` → `items[]` (`slug`, `name`, `type`, `category`, `description`).
- `data/meta/meta.json` — optional `stars` / `repo` (official marketplace repos have stars cleared).

If a field is missing, the slide omits it. It does not estimate, interpolate, or reuse an older night’s figure as if it were tonight’s.

**Template vs. snapshot:** hook examples below use the 2026-11-20 report as a filled-in illustration. Those numbers will change the next night. Treat them as `{field}` templates, not evergreen copy.

Illustration from the 2026-11-20 report (do not reuse after the next nightly): `date=2026-11-20`, `pass=906`, `tested=1050`, `total=1075`, `broken=140`, `needs_key=25`, `fail=169`, `addons=428`, `broke` length 3; Claude Code `pass=340` / `total=372` / `broken=26`; Grok Build `351/387`; Codex `96/120`; Cursor `33/55`; Pi `86/141`; week `2026-47` (`start=2026-11-16`, `end=2026-11-22`, `runs=4`). Agent versions that night: Claude Code 2.1.319, Codex 0.167.0, Grok 1.0.77, Cursor 2026.11.05-86047df, Pi 1.5.0.

---

## 2. Hook formulas

Muse’s research (Section 2) found five formulas that repeat in this niche. Reuse the formula; fill it from nightly fields. Do not invent a sixth “clever” hook that we cannot back with a receipt on slide 2 or 3.

All SkillMaxx examples are **TEMPLATES**. The filled 2026-11-20 wording is marked **EXAMPLE (2026-11-20 report only)**.

### 1. Big-number list promise
The number is the hook. The number must be a real count from last night or this week.

- **TEMPLATE:** `{rep.by.claude_code.pass} Claude Code add-ons that actually installed last night`
- **EXAMPLE (2026-11-20 report only):** “340 Claude Code add-ons that actually installed last night”
- **TEMPLATE:** `{rep.pass} clean installs out of {rep.tested} judged last night`
- **EXAMPLE (2026-11-20 report only):** “906 clean installs out of 1,050 judged last night”
- Cover eyebrow pattern (already in the generator): `NIGHTLY SANDBOX LOGS · {fmt_date(rep.date)}`

### 2. Money / time saved (honest version)
SkillMaxx does not have a measured “dollars saved” figure. Do not invent one. The honest version of this formula is waste avoided: skipped installs that already failed the sandbox, or time not spent on a flaky README.

- **TEMPLATE:** “Stop installing the {rep.broken} add-ons that already failed tonight’s sandbox”
- **EXAMPLE (2026-11-20 report only):** “Stop installing the 140 add-ons that already failed tonight’s sandbox”
- **TEMPLATE:** “{len(weeks.flaky)} tools flipped this week — check the 10-night history before you debug”
- Never use vendor ROI claims, and never repeat the unmeasured “20% more Claude usage” hook from the 9 Nov 2026 @wavaai.feeds post (research flagged it; a same-day fact-check said the percentage was never measured).

### 3. Contrarian / opinionated take
Punch at a problem, not a person (CONTENT-STRATEGY guardrail). SkillMaxx’s moat is visible failures.

- **TEMPLATE:** “Most ‘works with Claude’ pages don’t show what failed. Tonight, {rep.by.claude_code.broken} Claude add-ons did — with logs.”
- **EXAMPLE (2026-11-20 report only):** “Tonight, 26 Claude add-ons failed — with logs.”
- **TEMPLATE:** “Pass rates are not a bake-off. Each agent is tested only on the add-on formats it supports.”
- Keep this one evergreen; it is a methodology fact, not a statistic.

### 4. Identity / system claim
Our system is the nightly sandbox, not a personal “AI team” story.

- **TEMPLATE:** “We re-test {rep.tested} installs across 5 agents every night”
- **EXAMPLE (2026-11-20 report only):** “We re-test 1,050 installs across 5 agents every night”
- **TEMPLATE:** “The SkillMaxx loop: pick an agent → copy the passing command → read the 10-night history”

### 5. Authority as receipt, not borrowed celebrity
We do not borrow “the guy who built Claude Code” unless we are quoting a sourced public post and clearly labeling it. Our authority line is the sandbox itself.

- **TEMPLATE:** “From tonight’s SkillMaxx sandbox, not a vendor blog.”
- **TEMPLATE (only if `standout` is present):** “Tonight’s standout: {standout.name} — {standout.desc}” plus stars only when `meta.json` actually has them.
- **EXAMPLE (2026-11-20 report only):** standout was `MCP time (reference)` with `stars=91859` in `weeks.json` / `reports.json`. Re-read the field before using it; do not hard-code the star count.

**Cover typography rule (from VIRAL-RECIPE.md):** proof in the eyebrow, exact number in the headline, one-line mental model in the subtitle. Slide 1 also needs a visual anchor (org-chart tree or artifact collage), not empty space.

---

## 3. 8–10 slide structure

Research finding: the Instagram sweet spot in this niche is **8–10 slides** (9 of 15 in-window top posts). Pattern:

1. **Cover** — hook + visual anchor + the key number.
2. **One item (or one tight unit) per slide** — a department, a skill, a news story, or a single myth.
3. **Payoff by slide 3** — the reader already has the useful fact, prompt, or number. Do not hold the only payoff for the last slide.
4. **Recap / cheat-sheet** — the list at a glance, saveable.
5. **CTA** — newsletter by default; comment-keyword is a template behind `--cta keyword|hybrid` until Brandon chooses.

v3 mappings:

| Format | Slide 1 | Slide 2 (payoff path) | Mid slides | Recap | CTA | Typical length |
|---|---|---|---|---|---|---|
| `orgchart` | Hook + org chart with `{cc_pass}` | 5-agent strip from `rep.by` (the payoff is “what actually passed tonight”) | One department per slide (5) | Department counts + matrix URL | Newsletter (default) | 9 |
| `maxxing` | Collage hook | What broke tonight (honesty is the payoff) | 5/5 elite, 5-agent reality, 3-step loop, week trend from `weeks.json` | Tonight’s headline counts | Newsletter (default) | 8 |
| `timely` | “This week on the radar” + pull timestamp | Why it matters, tied only to tonight’s `versions` / pass counts | One HN/radar story per slide (3–5) | Titles only, plus sources | Newsletter (default) | 8–9 |
| `news` / `leaderboard` | Existing 6-slide receipts | Payoff already lands on slides 2–3 (broke/fixed, rankings) | Keep current body | Use the last body slide as the cheat-sheet until a later pass adds a dedicated recap | Existing newsletter boxes | 6 today; upgrade later if these become the Tue/Sun flagships |

Hold-back (research): it is fine to show the list on-slide and point the CTA at the full matrix or the weekly issue. It is not fine to invent a “full 29” or any other ungated count that is not in the data.

---

## 4. Hashtags (3–5 core)

Research: tags are not the driver; the CTA and the saveable slide are. Several top posts used only 3–5 tags. Do not stuff 13.

**Core set (use 3, then add 0–2 topic tags):**

1. `#ClaudeCode`
2. `#ClaudeAI`
3. `#AITools`

**Topic-tag pool (pick to match the deck, never all at once):** `#DeveloperTools` `#ClaudeSkills` `#AIAgents` `#AIWorkflow` `#MCP`

**Guidance**

- Instagram / TikTok: 3–5 total. Core three plus one topic tag is the default. A fifth only when it is truly specific (`#MCP` on a timely MCP story).
- X: 0–1, usually zero (CONTENT-STRATEGY).
- Bluesky: 0–1; prefer natural keywords in the sentence (claude code, mcp, cursor) so custom feeds can pick the post up.
- LinkedIn: 3–5 at the end is fine; do not let tags replace the full-context body.
- Never use a tag we did not mean. Never invent a campaign tag until Brandon asks for one.

---

## 5. TikTok Photo Mode (1080×1920)

TikTok calls this a photo post, not a Reel. Research: up to 35 images, recommended **1080×1920**; winners in this niche still used 8–12 slides. Photo posts sit in the For You feed next to videos; **saves** are the tell, so the recap slide should be worth screenshotting.

v3 generator flag: `--size 1080x1920` or `--size both`. Output folders are `v3-<name>-<date>/` (4:5) and `v3-<name>-tiktok-<date>/` (9:16). Same data, same slide count, taller padding.

**When publishing (later, and only after Brandon says post — nothing posts from this plan):**

- Caption can be long (TikTok photo captions up to 4,000 characters). Put the list and the source lines in the caption as well as on-slide.
- Photo title cap is 90 characters: use the hook, including the search phrase (“Claude Code skills”, “MCP server install”).
- Music: TikTok may auto-add a sound via API publishing; in-app, add a sound manually. Instagram carousels have no native audio. Plan the TikTok sound as an in-app step if we ever post.
- If a slide uses realistic AI-generated imagery, apply TikTok’s AI-generated label (Integrity guidelines effective 24 Sep 2026). Current SkillMaxx decks are typography, icons, and data — not photoreal generated people — but label anything that later is.
- Export is PNG for review. A JPEG/WebP pass can be added later if TikTok prefers those types; do not block review on it.

---

## 6. Weekly timely-news slot (Wednesday)

This is the pillar 5/6 slot. **Muse Section 3 is a topic menu, not a fact sheet.**

Use the ten topics as *what to look for* in a fresh pull. Do not copy numbers, star counts, benchmark scores, dollar-per-task figures, breach-impact counts, or vendor showcase metrics from the research file onto a slide or into a caption.

**Sourcing rule (mandatory):**

1. At render time, run `growth/scripts/fetch_radar_hn.py` (keyless HN Algolia, same helper the Sunday newsletter uses) or pass a just-written `--radar-json`. Queries: `mcp server`, `claude code`, `agent skills`, `codex cli`, `cursor mcp`.
2. Each story slide may show only: the story title, the HN URL, the external URL, **HN points and comment counts as of the pull**, and the pull timestamp. Those engagement counts are first-party from the API at render time, labeled “as of pull.”
3. If a URL is a vendor blog, product page, or official announcement, mark the slide **Vendor source**. If the title asserts a metric SkillMaxx did not measure, mark it **Vendor claim — not independently verified**. Never restate the metric as a SkillMaxx fact.
4. SkillMaxx context on a news slide is limited to fields from *tonight’s* `reports.json` (for example, “Claude Code in last night’s sandbox: {versions.claude_code}”). No cross-product bake-off scores unless they come from our own tests.
5. If the pull returns fewer than three usable stories, skip the timely deck that week rather than padding with stale research items.
6. Section 3 items that do not appear in the fresh pull are dropped. They can be mentioned in a planning note (“still watching”) but they do not get a slide.

**Section 3 topic slots (week of 16–22 Nov 2026 — for editorial awareness only):**

1. Claude Code “Code Mode” / chained tool calls — watch official + independent writeups; no unverified speedup claims.
2. Claude Code Projects rebuilt as parallel threads — include cost/limit warnings only if a primary source states them, and attribute the source.
3. New Codex models — any quality or cost comparison is a claim unless it is our sandbox result.
4. Gemini 4 Hydrogen + Orchestrator — Google performance and quota figures are **vendor claims**.
5. Devin Bots / supervisor-agent race — showcase delivery stats are **vendor claims**.
6. Instagram Edits for Mac + MCP — useful how-to if independently sourced; note missing official setup docs if still true at pull time.
7. Official `anthropics/skills` repo traction — re-read the live star count at pull time; do not reuse a research-file snapshot. License nuance (source-available vs open source) if still accurate.
8. Third-party coding-agent indexes — cite the index and date; these are not SkillMaxx tests.
9. Cursor / Fireworks extension incident — report only what the vendor/security sources disclosed; no speculation on attribution or extra victim counts.
10. Claude Code auto-mode / hooks trust dialog — pair with our own `versions.claude_code` if the nightly pin is in that line.

Bonus slots in the research (Instagram MCP connectors; OpenCode subagents) follow the same rule: only if they show up in the fresh pull or a dated primary source opened at render time.

**Claim language on-slide:** a small amber pill, e.g. `VENDOR CLAIM`, plus a one-line source (`HN · {points} pts · {date}` or the publisher name). Captions repeat the flag. Do not launder a claim by paraphrasing it without the number.

---

## 7. 15 watch accounts (weekly refresh)

From Muse Section 4. Follower counts in the research were already flagged as possibly stale and were not re-checked live. Do not treat them as current. Refresh is **read-only public pages** — no logins, follows, likes, comments, or DMs.

**What to look at each week (same checklist for every handle):**

- Latest carousel or photo post: hook formula (which of the five), whether the payoff lands by slide 3.
- Slide count and structure (cover / one-item / recap / CTA).
- CTA type: comment keyword (note the word), save prompt, or link-in-bio.
- Visible hashtag count and which tags repeat.
- Whether they rode a timely-news hook, and whether numbers were sourced or just asserted.
- Outlier signal only when it is publicly visible (likes/comments, or saves on TikTok). Record the retrieval date. Do not invent a view count.

| # | Handle | Where | Why watch / what to steal carefully |
|---|---|---|---|
| 1 | @ai.byarsh | Instagram | Closest SkillMaxx comp: Claude add-ons, free-vs-paid, comment-keyword almost every post. Watch hook numbers and department-style lists. |
| 2 | @artem.novitckii | Instagram | Format + honest rankings; author of an open-source carousel skill. Watch cover collage → dense list transitions, and how he gates links. |
| 3 | @theroshankrishna | Instagram | “AI agent team” system posts and `AGENT`-style keyword CTAs. Useful for multi-agent framing, not for copying unverified salary claims. |
| 4 | @jayantcreates.ai | Instagram | Claude × Instagram automation. Accuracy matters: commenters have pushed back on “native connection” claims — do not repeat those claims. |
| 5 | @vaibhavsisinty | Instagram | Large-account playbook: idea generation and pre-post testing; watch how they optimize for saves. |
| 6 | @nick_saraev | Instagram + YouTube | Cross-platform agent-builder systems. Watch workflow explainers, not growth-hack CTAs we cannot fulfill. |
| 7 | Sabrina Ramonov / Blotato | YouTube (+ IG) | Automation roundups as a discovery source. Also listed on TikTok as @sabrina_ramonov. |
| 8 | Nate Herk | YouTube (+ IG/X/LinkedIn) | Plain-English n8n + Claude Code; posting-skill formats. |
| 9 | @gayatri.tech | Instagram | Breakout / high-outlier workflows. Watch hooks that travel beyond follower count. |
| 10 | @code.with.ahsan | Instagram | AI agents coding listicles; another high-outlier format watch. |
| 11 | @kirodotdev | Instagram | Small account, historically high views-per-follower in third-party breakout lists (those view figures were not re-verified). Watch formats that punch above size. |
| 12 | @luispdoesai | Instagram | Micro-creator outlier signal — hooks often show up here before big accounts copy them. |
| 13 | @hex.gar | Instagram | “Stack I actually use” carousel template. |
| 14 | @aiwithbhushan | Instagram | Listicle + comment-for-list CTAs. Benchmark the keyword, not the tool-count hype. |
| 15 | @networkchuck | Instagram + YouTube | Security + Claude audience. Useful when the timely slot is a security story (topic 9). |

**Closest comps (research ranking, for priority):** @ai.byarsh, @artem.novitckii, @kayvon.ai, @chase.h.ai, @jayantcreates.ai, @seb.ai, @hugh_candoit, @sahni.ai / @thesanskaarsingh. Kayvon, Chase, Seb, and Hugh are not in the 15-row table but should be glanced at in the same weekly pass when time allows.

**TikTok-specific handles to scan in the same pass:** @wavaai.feeds, @futurastudi0, @nowyouknow_ai, @tinoi.flows, @nextpath.ai, @the.ai.leverage, @zdenomucina, @askyourdigitalagency, @angusscutt.ai, @maverickgpt, @yury.ai, @nocode.joshua, @github.awesome, @sabrina_ramonov, @alliekmiller. Public search for this niche was stale (many top photo posts were Mar–Apr 2026). Note dates. Do not present off-window posts as “this week.” No TikTok handle was confirmed for @ai.byarsh or @artem.novitckii.

**Alternates if a handle goes quiet:** Ryan Doser, Julian Goldie, @handlytech, @aifrontierindex.

Suggested log path if we start keeping notes: `growth/carousels/WATCH-YYYY-MM-DD.md`. Optional; do not create noise for a week with nothing new.

---

## 8. CTA options (Brandon’s call)

**Research finding:** on Instagram in this niche, a single-word comment keyword that promises a DM is the engagement engine. Comments often approach or exceed likes. Link-in-bio as the *primary* CTA underperforms here. Official product announcements with no keyword (example given: @claudeai) can still get likes and relatively few comments.

**That does not automatically mean SkillMaxx should switch.** A keyword CTA that is not fulfilled is worse than a plain newsletter URL. Brandon has not chosen. The generator keeps the **newsletter CTA as the default** until he does. `--cta keyword` and `--cta hybrid` exist as placeholders for samples only.

No option is “the official SkillMaxx CTA” until he says so. The “suggested default if he wants to test a keyword later” is marked as a suggestion, not a decision.

### Option A — Link in bio / newsletter URL (current default)

- **What:** Last slide and caption point at `https://skillmaxx.gilventures.ai/newsletter/` (site), with the Beehiiv subscribe URL available from the existing newsletter CTA rule when we are on Buffer text posts. X keeps the link out of the main post (thread post 2 on CTA days).
- **Cost:** $0. No new tools. Fits the owned-audience goal (CONTENT-STRATEGY: follows → community → newsletter → sponsors).
- **Coverage:** Works on every channel (IG, TikTok, LinkedIn, X, Bluesky).
- **Tradeoff:** Research says this will likely get fewer comments than a keyword. It does get a subscriber onto a list we own, which a DM does not do by itself. No fulfillment work, no DM limits, no automation-account risk.
- **Best for:** Now, and for any week we cannot staff replies.

### Option B — Comment keyword + manual DM replies

- **What:** “Comment SCORE and I’ll send the report link” (keyword is a placeholder). A person — Brandon, or someone he designates — DMs commenters the newsletter or `/reports/latest/` link.
- **Cost:** $0 software, but it costs Brandon’s (or a designee’s) time, every post, until the thread dies.
- **Platform limits and gaps (cite, and do not treat unofficial folklore as policy):**
  - **Instagram:** Comment-to-private-reply is a documented Graph API pattern: **one private reply per comment, within 7 days**; further messages wait for the person to reply (Chatfuel’s own messaging-limits doc; Meta’s messaging window). Instagram does **not** publish a daily cold-DM cap. Community “30–50/day” figures are folklore — do not plan as if they were official. Replies to people who commented on our post are user-initiated, which is the safer shape, but bursts can still get throttled.
  - **TikTok:** No documented official comment-to-DM for a personal/creator login. Many people cannot be messaged at all, depending on their privacy settings. TikTok’s Business Messaging API is a separate, regional/beta path. Manual DMs will miss a large share of commenters. No published daily cap.
  - **X:** Official documented cap: **500 sent Direct Messages per day**, all devices combined ([Understanding X limits](https://help.x.com/en/rules-and-policies/x-limits)). A widely reported *message-request* cap for first contact with people who do not follow you (often quoted as 7/day on free accounts, higher on Premium) appears in secondary writeups; it was **not** on the official limits page retrieved for this plan, so treat it as unverified. X also restricts unsolicited automated replies. A keyword on X is mostly a reply-thread, not a native DM funnel.
  - **LinkedIn:** No open DM API for this use. Messaging is largely limited to connections; InMail is a paid product. Keyword CTAs here are weak unless we only reply as a human to comments on our page post.
- **Tradeoff:** Highest engagement *if* every commenter actually gets the link. On a viral IG post that can be hundreds or thousands of comments (top niche posts in the research had comment counts in the thousands). A single person cannot fulfill that by hand. Risk of looking broken if we ask for a comment and go silent. No extra account-ban risk beyond ordinary manual use, as long as we do not use unofficial browser bots.

### Option C — Free tiers of DM automation (official APIs only)

Unofficial “browser bot” tools that log into Instagram or TikTok with a password are against those platforms’ terms and are **out of scope**. Official-API tools lower risk; they do not remove it. Meta can still restrict an account for spammy or off-policy messaging even when the software is a partner.

Checked 2026-11-20:

| Tool | Official free-tier facts (as of this date) | Coverage | Honest catch |
|---|---|---|---|
| **Manychat** | Official Help Center (updated 29 Oct 2026): Free plan is $0, **25 Active Contacts per month**, **1 user / 1 inbox seat**, **up to 2 channels** from Instagram, TikTok, Facebook Messenger, Telegram, **up to 4 live automations**. Comment-to-DM is described as a supported automation type. “Powered by Manychat” branding on first contact. WhatsApp/SMS/email are not on Free. New pricing model dated 2 Mar 2026. Sources: [Free plan](https://help.manychat.com/en/articles/17742189-free-plan), [Active Contacts](https://help.manychat.com/en/articles/17742213-active-contacts). | IG + TikTok possible on Free (2 of those 4). **Not X, not LinkedIn.** | 25 contacts/month is a test, not a viral safety net. Web plans describe overages on paid tiers; do not assume Free will quietly keep sending past 25. |
| **Chatfuel** | Official billing docs list **paid** Business/Agency plans and a **7-day free trial** with $15 in credits — not a permanent free plan ([Plans and Pricing](https://chatfuel.com/docs/billing/chatfuel-plans-and-pricing), [pricing](https://chatfuel.com/pricing)). Comment automations and messaging windows are documented for the product ([Instagram automations](https://chatfuel.com/docs/instagram/instagram-tasks): 1 DM after a new contact comments, then wait). | IG, Facebook, TikTok on the paid product. **Not X, not LinkedIn.** | A third-party comparison (DM Compared, Oct 2026) claims a permanent free comment-autoreply tier with no contact cap. **That claim is not confirmed on Chatfuel’s own billing docs** fetched the same day. Do not plan as if unlimited free Chatfuel comment-to-DM is guaranteed. |
| **ReplyRush** | Vendor pricing/blog claims a free plan with **1,500 DMs per month**, 1 Instagram + 1 Facebook account. | Instagram (+ Facebook). **Not TikTok, X, or LinkedIn** on the materials reviewed. | Vendor-written. The public pricing table also listed “Comment Auto Reply” as missing on Free in one rendering, which **conflicts** with the vendor blog that says comment-to-DM is included. Re-check inside an account before relying on it. Still official-API-shaped, still not zero risk. |

**Account-risk summary:** official Graph API / partner tools + user-initiated comments = lowest reasonable risk, not zero. Password-based bots = do not use. Automating X or LinkedIn DMs with unofficial scrapers = do not use. TikTok automation should stay inside a documented business API or a tool that explicitly uses it; Manychat lists TikTok as a connectable Free-plan channel, but fulfillment will still follow TikTok’s privacy and regional API limits.

### Option D — Hybrid

Last slide shows the newsletter URL **and** a keyword (“Or comment SCORE and I’ll DM the same link”). Caption leads with the URL so anyone who never gets a DM can still subscribe. Fulfill the keyword only on Instagram (Manychat Free for the first 25 contacts, manual after that, or manual-only). Other platforms keep the newsletter URL as the real CTA.

**Tradeoff:** Honest about fulfillment limits; splits the ask (CONTENT-STRATEGY prefers one CTA per post — a hybrid should be worded as one action with a fallback, not two competing asks). Still Brandon’s time or a 25-contact ceiling unless he pays for a tool.

### Suggested default (not a decision)

- **Keep Option A (newsletter URL) as the live default.** That is already how v2 decks and this v3 generator ship, and it matches the owned-audience goal plus the “don’t promise a DM we cannot send” constraint.
- **If Brandon wants to trial a keyword later:** start with **Option D, Instagram-only**, keyword placeholder `SCORE`, fulfillment either manual or Manychat Free (25 Active Contacts) as a time-boxed test, and leave X / LinkedIn / TikTok on the newsletter URL. Review after 2–3 posts whether comments and actual subscribers moved. Do not turn this on in a posted carousel until a fulfillment path is staffed.
- This is a suggestion. It is his call.

---

## 9. Generator v3

Free, local, no posts. Updates in `growth/carousels/generate.py`:

```bash
python3 growth/carousels/generate.py --format v3 --size both --cta newsletter --out /workspace/carousels-samples --zip
python3 growth/carousels/generate.py --format timely --date 2026-11-20 --size both --out /tmp/carousels --zip
python3 growth/carousels/generate.py --format orgchart --v3 --cta hybrid --keyword SCORE --size 1080x1920
```

- `--format v3` renders `orgchart`, `maxxing`, and `timely`.
- `--v3` upgrades orgchart/maxxing to the 8–10 slide structure (payoff, recap, CTA variants). Legacy `--format v2` stays on the previous 6–7 slide decks.
- `--size 1080x1350|1080x1920|both` (default 1080×1350).
- `--cta newsletter|keyword|hybrid` (default `newsletter`).
- `--keyword WORD` (default `SCORE`) — only affects keyword/hybrid CTA slides.
- `--radar-json PATH` optional; otherwise `fetch_radar_hn.py` runs at render time.

Nothing in this pipeline talks to Buffer, X, or any social API.

---

## 10. What this is not

- Not a posting schedule in Buffer.
- Not a change to Beehiiv (newsletter emails stay unsent drafts while subscribers are tests).
- Not Gil Marketing work.
- Not a decision on the comment-keyword CTA.
