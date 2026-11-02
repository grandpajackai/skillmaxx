# LinkedIn Sales Navigator playbook (free trial, Brandon's personal account)

Written 2026-11-01. Owner: Brandon (he does every click/send). SkillMaxx CEO keeps this file and drafts notes.
**Rules that apply to every lead here:** [OUTREACH.md §0](OUTREACH.md) (person-verification) and [§0b](OUTREACH.md) (smart-question rule). No individual names live in this file; people go in [SALES-NAV-LEADS.csv](SALES-NAV-LEADS.csv) only after §0 verification.

---

## 0. Ground rules (read first)

- **No bulk export, no scrapers, no browser extensions** (Phantombuster, Dux-Soup, Apollo/Lusha Chrome plugins, "export to CSV" tools). They violate LinkedIn's User Agreement and are the fastest way to get the personal account restricted (we already got follow-restricted on X).
- **Pace:** 15–20 connection requests per day max, spread across the day, weekdays. Stay under ~100/week. If acceptance rate drops below ~30% or LinkedIn shows a warning, pause 3 days.
- **InMail credits:** don't spend up front. Use only for leads who haven't accepted after 7 days. Check the credit count on the trial page (Settings → Subscription).
- **Logging:** type each lead into `SALES-NAV-LEADS.csv` by hand (or tell the CEO in chat and it gets logged). Before the trial ends, copy every lead list's names/URLs into the CSV so nothing is lost.
- **Every note follows §0b:** one specific question from their README or our test results. Never ask what their docs answer; never offer a test we could just run (we run it first, then share).
- **Brandon's final gate (§0):** before sending, check the profile's top job says the right company + "Present" with nothing newer above it.

---

## 1. Saved searches (type these in exactly)

### 1A. Lead search: "SkillMaxx – DevRel & Growth at tested companies"
1. Open Sales Navigator → top bar **Lead filters** (or the search box → "Lead filters").
2. **Current job title** → click *+ Include* and add each of these (press Enter after each):
   `Developer Relations`, `DevRel`, `Developer Advocate`, `Head of Developer Relations`, `Developer Marketing`, `Head of Developer Marketing`, `Developer Experience`, `Partnerships`, `Head of Partnerships`, `Technology Partnerships`, `Ecosystem`, `Head of Growth`, `Growth Marketing`, `Community`, `Head of Community`
3. **Current job title** → *Exclude*: `Intern`, `Recruiter`, `Sales Development`, `Account Executive`
4. **Seniority level** → include `Senior`, `Manager`, `Director`, `Vice President`, `CXO`, `Owner / Partner` (skip Entry/Training).
5. **Company headcount** → include `11-50`, `51-200`, `201-500`, `501-1,000`.
6. **Current company** → *+ Include* and paste the companies from §2 one at a time (start with the top 10). Or attach the Account list from §1C via **Account lists → "SkillMaxx – Tested companies"**.
7. **Geography** (optional): leave blank (remote dev-tools teams).
8. Click **Save search** (top right) → name `SkillMaxx – DevRel/Growth @ tested` → alert frequency **Daily**.

### 1B. Two spotlight variants of the same search (save both)
Spotlights are the pills just above the results list.
- **Variant 1 – "Changed jobs in past 90 days":** run 1A, click the **Changed jobs** spotlight → Save search as `SkillMaxx – job changers 90d`. New-in-role people are building their partner/channel plan and are usually most open.
- **Variant 2 – "Posted on LinkedIn in past 30 days":** run 1A, click **Posted on LinkedIn** → Save as `SkillMaxx – active posters 30d`. Active posters accept and reply far more; read their latest post for a §0b angle.
- (If shown) also try **Shares experiences with you** and **Following your company** for warmer intros.

### 1C. Account search: "SkillMaxx – Tested companies" + alerts
1. Switch to **Account filters**.
2. **Company headcount** → `11-50`, `51-200`, `201-500`, `501-1,000`.
3. **Industry** → `Software Development`, `IT Services and IT Consulting`, `Technology, Information and Internet`.
4. **Keywords** → `MCP OR "Claude Code" OR "agent skills" OR "AI agents" OR "developer platform"`.
5. **Headcount growth** (if available) → `1%+` over 6 months (growing teams buy).
6. **Department headcount → Marketing** → 1+ (someone owns sponsorship spend).
7. Save search → `SkillMaxx – dev-tools 11-1000` (alerts weekly).
8. Separately: search each §2 company by name → **Save** → add to a new Account list `SkillMaxx – Tested companies`.

**Account alert ideas (turn on for the list):**
- **Funding events** → newly raised = fresh marketing budget; mention their plugin's pass streak in the congrats note.
- **Hiring (new DevRel/marketing roles posted)** → they're investing in developer reach.
- **Senior leadership changes** → new VP Marketing/DevRel = new budget owner (feeds the job-changers search).
- **Company news / product launches** → new plugin or MCP release = we re-test that night and send the result.
- **Headcount growth** spikes.

---

## 2. First 30 target companies (from our test data)

Source: `data/skills.json` + `testing/history.json` (runs 2026-10-16 → 2026-11-01). Every company below has a plugin/MCP that **passes** our nightly installs. Already excluded: everyone in PIPELINE.csv and BRANDON-OUTREACH.md. Results read "agent passes/runs". Codex, Cursor and Pi are only listed where we actually test them; most official-directory plugins are tested on Claude Code + Grok Build only (Grok Build loads Claude Code plugins). Before drafting a note, re-open their README (data/meta/readme/<slug>.md) to confirm the observation is still current.

**How to find the right person:** in Lead search type the company name in **Current company**, then apply the §1A title list. Search text below is what to type in the keyword box if you'd rather do a quick search: `<Company> "developer relations" OR devrel OR "developer marketing" OR partnerships OR growth OR community`.

| # | Company | What we test | Our pass results | README observation + smart-question angle | Sales Nav search |
|---|---|---|---|---|---|
| 1 | Superdesign | Superdesign plugin (design skill for coding agents) (`superdesign`) | Claude Code 9/9, Grok Build 9/9 | README says it works in "Claude Code, Cursor, Codex, and 70+ others" via `npx skills add`, but the native plugin path is Claude Code only. Angle: We only verify Claude Code + Grok Build; ask which of the 70+ agents drives the most real installs. | Current company: `Superdesign` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 2 | RevenueCat | RevenueCat AI Toolkit plugin (MCP + IAP skills) (`revenuecat`) | Claude Code 9/9, Grok Build 9/9 | Ships two plugins (`revenuecat` + `revenuecat-play-billing`) and says the marketplace targets Claude Code, Cursor, Codex and Visual Studio. Angle: Ask whether most users install the Play Billing add-on or just the core plugin. | Current company: `RevenueCat` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 3 | Convex | Convex backend plugin (skill + subagent + quickstart) (`convex`) | Claude Code 9/9, Grok Build 9/9, Pi 9/9 | README pitches plain-English asks ("no backend knowledge required"), i.e. aimed at non-developers. Angle: Ask what share of plugin users are non-developers vs existing Convex devs. | Current company: `Convex` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 4 | Mintlify | Mintlify plugin (skill + 2 MCP servers) (`mintlify`) | Claude Code 9/9, Grok Build 9/9 | Bundles a read-only Search MCP and a write Admin MCP whose edits land as PRs; also offers `npx skills add`. Angle: Ask whether teams turn on the Admin MCP or stay read-only. | Current company: `Mintlify` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 5 | Rootly | Rootly incident plugin for Claude Code (`rootly`) | Claude Code 9/9, Grok Build 9/9 | Built around `/rootly:deploy-check` before deploys, Claude Code-branded README. Angle: Ask whether deploy-check is the most-used command or incident investigation. | Current company: `Rootly` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 6 | Postiz | Postiz social-scheduling plugin (`postiz`) | Claude Code 9/9, Grok Build 9/9 | README lists 16 agent surfaces incl. Grok Build and Grok Bot; skill install via `npx skills add gitroomhq/postiz-agent`. Angle: Ask which agent surface brings most signups (we see Claude Code + Grok Build pass). | Current company: `Postiz` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 7 | You.com | You.com Web Search & Research plugin (`youdotcom-agent-skills`) | Claude Code 9/9, Grok Build 8/9 | Basic search works with no account via a free MCP profile; full features need OAuth/API key. Angle: Ask what share of free-profile installs convert to signed-in. | Current company: `You.com` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 8 | Endor Labs | Endor Labs AI Plugins (Agent Kit distribution) (`ai-plugins`) | Claude Code 9/9, Grok Build 9/9 | Mirror repo for Claude Code, Codex, Gemini CLI, Antigravity, Cursor IDE and Cursor SDK; version bumps are manual release actions (v2.2.3). Angle: Ask whether Codex/Cursor packages ship on the same release cadence as Claude Code. | Current company: `Endor Labs` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 9 | Shippo | Shippo AI plugin (9 skills + OAuth MCP) (`shippo`) | Claude Code 9/9, Grok Build 9/9 | Ships Claude Code, Codex, ClawHub and a ChatGPT knowledge pack from one canonical skills folder. Angle: Ask which channel (plugin vs knowledge pack) gets more real usage. | Current company: `Shippo` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 10 | Astronomer | Astronomer agents plugin (Airflow MCP + `af` CLI) (`astronomer-data-agents`) | Claude Code 9/9, Grok Build 9/9, Pi 9/9 | README has dedicated Claude Code and Cursor sections plus an `af` CLI. Our Pi tests also pass. Angle: Ask whether Pi/terminal agents are on their radar given the CLI. | Current company: `Astronomer` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 11 | Altimate AI | Altimate Code plugin (dbt/warehouse delegation) (`altimate-code`) | Claude Code 9/9, Grok Build 9/9 | Plugin delegates work to the separate altimate-code CLI agent. Angle: Ask whether users mostly come in via the plugin or the standalone CLI. | Current company: `Altimate AI` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 12 | Synthflow | Synthflow voice-agent plugin (`synthflow`) | Claude Code 9/9, Grok Build 9/9 | Three regional MCP endpoints; a region mismatch breaks the connection (connector handles it, plugin needs manual choice). Angle: Ask how often region mismatch shows up in support. | Current company: `Synthflow` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 13 | TinyFish | TinyFish Grok Build plugin (web agent MCP) (`tinyfish`) | Grok Build 9/9 | Integrations for Claude, Grok, Kiro, Hermes, Pi, LangChain, ADK, Dify, n8n. Angle: Ask whether the Pi package (`@tiny-fish/pi`) is meant to be the reference install for terminal agents. | Current company: `TinyFish` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 14 | Octen | Octen Grok Build plugin (search MCP) (`octen`) | Grok Build 9/9 | README documents a name-resolution edge case and tells users to pin `octen@plugin-marketplace`. Angle: Ask how often users hit the ambiguous-name install error. | Current company: `Octen` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 15 | GitKraken | GitKraken plugin (Preview) (`gitkraken`) | Claude Code 9/9, Grok Build 9/9 | Marked "currently in Preview"; covers GitHub, GitLab, Azure DevOps, Bitbucket, Jira. Angle: Ask what has to land before it leaves Preview. | Current company: `GitKraken` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 16 | Voxel51 | FiftyOne computer-vision skills (`fiftyone`) | Claude Code 9/9, Grok Build 9/9 | Skills pair with a separate FiftyOne MCP server for 80+ operators. Angle: Ask whether most users install skills + MCP together or skills alone. | Current company: `Voxel51` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 17 | DataHub | DataHub skills plugin (`datahub-skills`) | Claude Code 9/9, Grok Build 9/9 | Enrich skill shows a before/after plan and asks approval before writes. Angle: Ask whether catalog search or enrich is the bigger driver. | Current company: `DataHub` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 18 | Atlan | Atlan agent toolkit / plugin (`atlan`) | Claude Code 9/9, Grok Build 9/9 | Local MCP server is deprecated in favor of hosted mcp.atlan.com; README setup still says "Install from marketplace (when available)" though it's in the official directory. Angle: Ask whether the README line will be updated now that it's listed. | Current company: `Atlan` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 19 | NightVision | NightVision DAST agent skills (`nightvision`) | Claude Code 9/9, Grok Build 9/9, Pi 9/9 | Portable Agent Skills folders; Claude Code via their own nvsecurity marketplace. Angle: Ask which agents beyond Claude Code they see in the wild. | Current company: `NightVision` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 20 | Confident AI | DeepEval plugin (`deepeval`) | Claude Code 9/9, Grok Build 9/9, Pi 9/9 | Open-source eval framework with Confident AI as the hosted product; Pi tests pass too. Angle: Ask what share of plugin users go on to Confident AI cloud. | Current company: `Confident AI` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 21 | Sonatype | Sonatype Guide plugin (supply-chain MCP) (`sonatype-guide`) | Claude Code 9/9, Grok Build 9/9, Pi 9/9 | Requires a token exported in shell profile before use; we see Pi pass too. Angle: Ask whether OAuth is planned to replace the env-var token step. | Current company: `Sonatype` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 22 | Windsor.ai | Windsor.ai marketing-data plugin (`windsor-ai`) | Claude Code 9/9, Grok Build 9/9 | Write actions (pause campaigns, budgets) always need confirmation; new campaigns created paused. Angle: Ask which write action users trust first. | Current company: `Windsor.ai` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 23 | Wingspan | Wingspan contractor-payments plugin (`wingspan`) | Claude Code 9/9, Grok Build 9/9, Pi 9/9 | Everything it creates is a draft; it never sends money. Pi tests pass. Angle: Ask whether drafts-only is permanent or a v1 guardrail. | Current company: `Wingspan` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 24 | Circleback | Circleback MCP plugin (`circleback`) | Claude Code 9/9, Grok Build 9/9, Pi 0/9 | README is two lines and points to circleback.ai/docs/mcp for setup. Angle: Ask whether a fuller in-repo README is planned (directories render it). | Current company: `Circleback` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 25 | Output.ai | Output framework plugin (`outputai`) | Claude Code 9/9, Grok Build 9/9 | "Designed for Claude Code"; Temporal under the hood; encrypted credentials via CLI. Angle: Ask whether other agents (Codex, Grok Build) are a target; Grok Build passes for us. | Current company: `Output.ai` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 26 | HeyGen (HyperFrames) | HyperFrames plugin (HTML-to-video for agents) (`hyperframes`) | Claude Code 9/9, Codex 9/9, Grok Build 9/9 | Ships for Claude Code and Codex (openai-curated) plus a desktop studio app. Angle: Ask whether Codex or Claude Code drives more renders. | Current company: `HeyGen` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 27 | Ory | Lumen local semantic code search plugin (`lumen`) | Claude Code 9/9, Grok Build 9/9 | Publishes reproducible benchmarks: up to 39% lower cost, 66% fewer output tokens. Angle: Ask if they'd want the benchmark run across Grok Build (passes install for us). | Current company: `Ory` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 28 | TDengine (TAOS Data) | TDengine IDMP skills (`idmp-plugin`) | Claude Code 9/9, Grok Build 9/9, Pi 9/9 | Needs `idmp-cli` installed and logged in first (Node 16+). Angle: Ask whether the CLI step will be bundled into the plugin. | Current company: `TDengine` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 29 | Appwrite | Appwrite plugin (SDK skills + hosted MCP) (`appwrite`) | Claude Code 9/9, Grok Build 9/9 | Two install paths: official directory (`appwrite@claude-plugins-official`) or their own marketplace (`appwrite@appwrite`). Angle: Ask which path they want new users on. | Current company: `Appwrite` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |
| 30 | Scandit | Scandit SDK plugin (`scandit-sdk`) | Claude Code 9/9, Grok Build 9/9 | 86 skills via one `npx plugins add scandit/skills` command that auto-detects your agents; also one-click in Codex and Cursor marketplaces. Angle: ask whether the auto-detect installer or the marketplaces drive more installs. | Current company: `Scandit` · Keywords: `"developer relations" OR devrel OR "developer marketing" OR partnerships OR "head of growth" OR community` · Seniority: Manager+ |

### Top 10 order (why)
1. Superdesign – claims 70+ agents; we can show which ones verifiably install.
2. RevenueCat – multi-agent marketplace + two plugins; clean data angle.
3. Convex – targets non-devs; install reliability matters most for them.
4. Mintlify – docs company, natural sponsor fit for a directory of dev tools.
5. Rootly – incident vendor; competitors (incident.io) already in pipeline, so category page fits.
6. Postiz – already lists Grok Build/Grok Bot; we confirm Grok Build passes.
7. You.com – search category next to Exa/Tavily; free MCP profile.
8. Endor Labs – ships to 6 agent hosts; cross-agent verification is exactly our product.
9. Shippo – one skills source to 4 channels; cross-agent proof.
10. Astronomer – passes on Pi too; data-eng category page.

---

## 3. Daily routine (15–20/day)
1. Open the 3 saved searches; take new results first (job changers, then active posters).
2. For each lead: §0 check (role current, ≥2 sources, one ≤90 days, nothing newer). Log in CSV with `verified=yes/no`.
3. Pick the matching §2 row, write the note (≤300 chars) with one §0b question. Ask the CEO to draft if unsure.
4. Send connection request; log `date_requested`.
5. After accept: send the standard after-accept message (site, X, Bluesky links) per LINKEDIN-NOTES; log `date_accepted`.
6. No accept in 7 days → optional InMail (log `inmail_used=yes`). No reply after a second touch → stop.

## 4. Before the trial ends
- Check the trial end date (Settings → Subscription) and put it in STATUS.md.
- 3 days before: open each lead list and type every name + profile URL into SALES-NAV-LEADS.csv by hand.
- Note which saved searches worked best (acceptance rate) so they can be rebuilt with free LinkedIn search later.
