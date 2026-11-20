# SkillMaxx Carousel v2 — Viral Recipe & Design Spec

**Updated:** 2026-11-20  
**Target formats:** 1080×1350 (4:5 portrait) PNG slides for Instagram, LinkedIn (PDF/image carousel), and X.  
**Brand system:** Dark obsidian (`#0A0A0B`), card surface (`#121215`), SkillMaxx lime (`#C6F432`), crisp `#EDEDEF` display Inter + `JetBrains Mono` badges. Never generic templates; zero paid Canva dependency.

---

## 1. Reference Breakdown

### Primary References (screenshots in `/workspace/carousels-samples/references-2026-11-20/`)

1. **`ai.byarsh` — "42 Things to Install in Claude"** ([Instagram](https://www.instagram.com/p/DfWR5BWiGct/), 7 slides, 11.6K likes, 7,202 comments)
   - **Slide 1 (Hook + Org Chart):** Specific proof eyebrow (`MY CLAUDE SETUP · 60 DAYS OF LOGS`), large two-tone headline (`42 Things to Install in Claude`), 1-line mental-model subtitle (`One CEO, five departments`), and a full-bleed **org-chart tree diagram** (`CEO: Claude Code` → dashed connector lines → 5 department cards with custom icons + item counts).
   - **Slides 2–6 (Department Deep Dives):** One department per slide (`Build`, `Design`, `Grow`, `Make`, `Run`). Includes:
     - Top kicker (`DEPARTMENT 1 OF 5 · BUILD · 8 ADD-ONS`)
     - Horizontal **5-tab department progress pill bar** highlighting the current slide
     - **Numbered compact rows** (up to 7–8 per slide): left SVG icon box + **Tool Name** + colored **Role/Type label** + 1-line job description + oversized right-hand monospace index (`01`, `02`, …) + compact metric pill.
   - **Slide 7 (Closer + Keyword CTA):** Callback headline (`42 hires. Start with one.`) + comment-keyword CTA (`Comment SETUP and I'll send it over`).

2. **`artem.novitckii` — "The art of Claude maxxing"** ([Instagram](https://www.instagram.com/p/De4AwvFlFga/), 7 slides, 8.6K+ likes, 4.2K+ comments)
   - **Slide 1 (Visual Artifact Collage):** Minimal centered serif/display hook (`The art of Claude maxxing`) ringed by 7–8 **tilted, tactile UI/developer artifacts** (Windows/macOS permission dialog, terminal splash, `SKILL.md` diskette, blueprint roll, `07:00` scheduled clock, nested subagent dolls, mobile chat preview). Triggers instant developer recognition and stops the scroll without needing a 3-sentence explanation.
   - **Hook + CTA Pairing:** High-identity title + single keyword CTA (`Comment "MAXX" and I'll send you my full Claude maxxing setup`).

### 5 Additional 2026 Viral Examples in This Niche

3. **`davidarnoux` — "18 dense cheat sheets for Claude Code"** ([LinkedIn](https://www.linkedin.com/posts/davidarnoux_claude-code-cheat-sheets-activity-7467862178923040768-70XN), 20 slides, 58+ comments)
   - Dense standalone reference cards (install, slash commands, `CLAUDE.md`, MCP, skills, hooks, subagents, security) ending with: `"want all 18 as a PDF? comment CHEATS, i'll DM it."`
4. **`rakhul-karthick` — "5 Levels of Claude Code"** ([LinkedIn](https://www.linkedin.com/posts/rakhul-karthick_5-levels-of-claude-code-activity-7491838319044173824-f164), 37+ comments)
   - Progression ladder framing (Memory → Skills → MCP Tools → Subagents → Autopilot) where each slide solves the bottleneck left by the previous one, paired with `"save it for setup night"`.
5. **`taki.gpt` — Custom "last 30 days" Claude Code skill** ([Instagram](https://www.instagram.com/p/DV3n04bDYek/))
   - Concrete time-boxed proof + single-keyword DM magnet (`Comment "Claude" for the full setup guide`).
6. **`codewithbrij` — "Corrected Claude Code Project Structure"** ([Instagram](https://www.instagram.com/p/DcxQBHMjpE1/))
   - Visual map of exact files/folders (`.claude/rules/`, `.claude/skills/`, `.claude/agents/`, `.mcp.json`) with a save-oriented CTA (`Save this map for your next Claude Code project`).
7. **`dailydoseofds_` — "Skill bundles in Hermes agent"** ([Instagram](https://www.instagram.com/p/DcQH2I-E-VB/))
   - Deep-dive on one underrated workflow mechanic with 3 numbered architectural takeaways and zero fluff.

---

## 2. Distilled Viral Mechanics for SkillMaxx v2

1. **Concrete proof in the eyebrow + headline:** Never generic ("Weekly AI Update"). Use exact verified nightly numbers (`340 skills that actually install in Claude Code`, `906 / 1,050 clean installs`).
2. **Slide 1 must carry a visual anchor, not empty space:** Either an **org-chart tree** (`orgchart` format) or an **artifact collage** (`maxxing` format) built from real terminal cards, `SKILL.md` badges, sandbox dialogs, and live counts.
3. **Orientation & momentum on body slides:** A horizontal department pill bar (`BUILD · SHIP · DATA · WORK · GUARD`) tells readers where they are in the deck and compels swiping through all 5 departments.
4. **High-density scannable rows:** Icon badge + Name + Type/Role pill + 1-line job description + monospace `01..07` index + **real pass-coverage badge** (`5/5 PASS`, `4/4 PASS`). Strictly zero invented numbers.
5. **Show failures transparently:** SkillMaxx's moat is honesty — include broken/failing counts alongside passes (e.g., `maxxing` Slide 2 shows real tonight's failures by agent).
6. **Callback + Comment-Keyword CTA on the final slide:**
   - `orgchart` CTA: `Comment "INSTALL"`
   - `maxxing` CTA: `Comment "MAXX"`
   - **Operational flag:** Comment-keyword CTAs require a DM fulfillment path (e.g., ManyChat, OmniSocials `create_automation`, or manual replies on Instagram/LinkedIn/X) before posting live, so commenters actually receive the promised link/commands.

---

## 3. Suggested Muse Scrape (if deeper reference polish is wanted)

Only slides 1–2 of `ai.byarsh` (`DfWR5BWiGct`) and slide 1 of `artem.novitckii` (`De4AwvFlFga`) were saved locally. If Brandon wants v3 refinements:
- Ask Muse to capture **slides 3–7 of `ai.byarsh` (`DfWR5BWiGct`)** (especially Slide 7's exact closing card layout) and **slides 2–7 of `artem.novitckii` (`De4AwvFlFga`)** (how he transitions from the collage cover to dense tutorial/list slides).
