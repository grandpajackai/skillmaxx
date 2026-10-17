# SkillMaxx Design Brief (Oct 16, 2026)
Screenshots: research/*.png (grokstacks, codexstacks, mcphubz, aiindigo, smithery, glama, mcpso, vercel, raycast, linear), 1440x900 above-the-fold.

## 1. Competitor teardown
| Site | Does well | Does poorly |
|---|---|---|
| GrokStacks / CodexStacks (same template) | Honest specific sub-hero ("331 listings… every install command copied from source"), "updated every night" badge, newsletter inline, category + "Best for…" chips | Single-agent only; generic dark/purple; chips wall; no visual hierarchy for cards; no compatibility proof |
| MCPHubz | Pivoted to a clear single action ("Scan your site free") — one CTA, one promise | Directory buried; terminal-gimmick logo; mixed purposes |
| AI Indigo | "Find the Right AI Tool — In Seconds", ⌘K, popular queries, big count (11,530+) | Emoji-heavy nav, ecosystem clutter, ad slots feel spammy |
| Smithery | Big confident hero, usage counts ("22.49k uses") as social proof, polished cards | Requires account; MCP-only; no cross-agent view |
| Glama | Huge scale (100k servers), live "Updated <timestamp>", faceted counts | Dense, ugly, overwhelming; no curation |
| mcp.so | Sponsor monetization proven | Sponsor wall *above* content destroys trust |
| Vercel Templates | Left facet sidebar + clean image cards, great filtering | n/a (benchmark) |
| Raycast Store | ⌘K search, Featured row, author avatars, install counts, gorgeous icons, one-click install | n/a |
| Linear | Typographic restraint, Inter Display, crisp 1px borders, subtle gradients, product-shot-as-hero | n/a |

**Gap nobody fills:** "Will this work in *my* agent, and how do I install it there?" Every competitor is single-ecosystem or untested. That is our whole pitch.

## 2. The 5-second value proposition
Current hero "Every agent skill. Every coding agent." is a slogan, not an outcome. The visitor must instantly get: **(what) one directory of skills/MCP servers, (proof) tested across 5 agents, (outcome) copy the right install command for your agent.**

Hero copy options:
1. **H1:** "Find agent skills that actually work in *your* agent." **Sub:** "Every skill, plugin and MCP server tested nightly in Claude Code, Codex, Grok Build, Cursor and Pi — with the exact install command for each."
2. **H1:** "One skill. Five agents. The right install command." Sub as above.
3. **H1:** "Stop guessing if a skill works in your agent." **Sub:** "We test them every night so you don't have to."
Recommend #1. Pair with an **agent picker** directly under the H1: "I use: [Claude Code] [Codex] [Grok Build] [Cursor] [Pi]" — selecting one personalizes the whole site (persisted in localStorage) and swaps every install snippet. This is the signature interaction.

## 3. Redesign spec
**Layout (desktop)**
1. Slim nav: logo, Browse, Matrix, New, Newsletter, Submit; ⌘K search pill; "Advertise" text link.
2. Hero (left 7 cols): eyebrow badge "● Tested last night · 21:00 ET" (live from data), H1, sub, agent picker, big search (⌘K / "/"). Right 5 cols: **animated live demo card** — a skill card whose install snippet cycles through the 5 agents with compatibility pills lighting up.
3. Stat strip: "58 skills · 5 agents · 290 compatibility checks · updated nightly" (real numbers only).
4. "How it works" 3 steps: Pick your agent → Find a skill → Copy the tested command.
5. Featured / Trending row (Raycast-style horizontal, includes 1 clearly-labeled Sponsored slot).
6. Browse: left facet sidebar (Type, Category, Works in, Status) + card grid (Vercel pattern), sort: Popular / New / Most compatible.
7. Compatibility matrix teaser (mini heatmap, link to full).
8. Newsletter block: "SkillMaxx Weekly — new skills + what broke, every Tuesday."
9. Footer: methodology, independence disclosure, GitHub.

**Typography:** Inter Display / Geist for headings (600, tight -0.02em tracking, H1 64/72 desktop, 40/44 mobile), Inter 15/24 body, Geist Mono / JetBrains Mono for install commands and counts (tabular-nums).

**Color (dark-first, light mode supported):** bg #0A0A0B, surface #111113, border rgba(255,255,255,.08), text #EDEDEF / muted #8A8F98. Brand accent electric lime #C6F432 (distinct from every purple competitor) with secondary cyan #22D3EE for gradients. Status: works #22C55E, partial #F59E0B, fails #EF4444, unknown neutral #52525B (dashed outline). Per-agent identity dots (small, muted) for the 5 agents.

**Components**
- Skill card: icon/monogram, name, one-line purpose, type badge (Skill/Plugin/MCP), 5 agent pills with status, GitHub stars + "tested 2d ago", hover → reveal copy-install for selected agent.
- Install block: tabs per agent, copy button with "Copied ✓" toast, "verified on <date>" footnote, link to source docs.
- Matrix: sticky header + first column, sortable, cell tooltips with test log excerpt, filter "works in all 5".
- Command palette (⌘K): fuzzy search over skills, categories, agents.
- Skill detail page: hero with purpose, compatibility panel, install tabs, "what it does" bullets, permissions/risk notes, related skills, changelog of test results (sparkline).

**Interactions:** agent picker personalizes everything; 150ms ease-out hover lift + border brighten; skeleton loaders; URL-synced filters; keyboard nav (/, ⌘K, j/k); prefers-reduced-motion respected.

**Trust signals:** live "last tested" timestamp; methodology page explaining tests; per-cell evidence; "Independent — not affiliated with Anthropic/OpenAI/xAI/Anysphere"; Sponsored labeled clearly and capped at 1 per row (avoid mcp.so's wall); GitHub repo link; source link on every install command.

**Empty / unknown states:** never a bare "unknown". Show dashed grey pill "Not yet tested" with tooltip "Queued for tonight's run" + "Report it works" link. No-results search: suggest closest matches, popular categories, and "Submit this skill". Matrix toggle "Hide untested". Before nightly testing exists, label honestly: "Verified from docs" (blue-ish outline) vs "Tested" (solid).

**Mobile:** H1 40px, agent picker as horizontally scrollable segmented control, search sticky under nav, facets in bottom sheet, cards single column with pills condensed to 5 dots + legend, matrix becomes per-skill accordion, 44px tap targets, copy button full-width.

## 4. Fixes to current build (shots/home.png)
- Hero doesn't explain outcome → apply copy #1 + picker.
- 58 identical cards in one undifferentiated wall → add Featured row, facets, sort, pagination/"load more".
- Pills mostly "unknown" read as broken → new unknown treatment + "Verified from docs" tier.
- Fix name capitalization; add icons/monograms so cards are scannable.
