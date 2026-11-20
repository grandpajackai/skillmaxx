# Brandon's queue, Fri Nov 20, 2026 (~8:00 AM ET, daily queue routine)

Nothing here was posted or sent for him. Numbers come only from the prep brief (/home/box/skillmaxx-prep/out/2026-11-20/queue.md). Latest published report is 2026-11-20: 906/1,075 installs passed, 428 add-ons (live check True). Per-plugin pass/fail facts come from testing/results/2026-11-20.json. Threads were re-read live through the X API at about 8:00 to 8:20 AM ET.
- All Nov 19 radar picks (mdjunaidap, waldekm, shamsbd71, coffeencode3000, ShantMele, damgreatbrand) were 22 to 35 hours old, so they're stale and dropped.
- No Nov 18 or Nov 19 hand-reply queue file exists and @SkillMaxxAI has no new mentions, so no next-day X follow-ups are due.
- No DMs are due. The Nov 1 X DMs (Expo, ClickHouse, Fullstory, Render, incident.io, Langfuse) already got their one follow-up on Nov 9. Cloudflare, Hugging Face, Greptile and Zyte have closed DMs. Rootly stays blocked until ~Dec 7.
- FusionAuth is do-not-contact (unsubscribed Nov 19).
- Reddit is not a post day. It's comment drafts only, with search text (403 from the box).

## X replies (Open post + paste; spaced through the day)
1. ~9:00 AM: @nestframework official NestJS agent skills (44k followers, 160 likes, 28 replies, posted 6:31 AM ET). https://x.com/nestframework/status/2123741121482489930
   Checked: the README and nest-cli PR #3716. `nest new` already asks which agents and defaults to all (.agents + .claude). Nest-version questions are already asked in the thread and covered by the README. A listing in Claude's official directory isn't mentioned.
   Reply: "Shipping it inside nest new is the smart part. SkillMaxx install-tests 428 agent add-ons nightly in Claude Code, Codex, Cursor, Grok Build and Pi; adding nestjs to the run. Any plan to list it in Claude's official plugin directory, or is your marketplace + npm the main path?"
   PROMISE: add nestjs/agent-skills to data/skills.json before the next nightly run.
2. ~11:00 AM: @simplifyinAI "532 Claude plugins" list (40.9k followers, 16 likes, 3 replies, posted 5:33 AM ET). https://x.com/simplifyinAI/status/2123726359335669777
   Nov 20 results: intuit-quickbooks CC/GB/Pi pass; stripe CC/Codex/GB pass; shopify-ai-toolkit CC/GB pass plus shopify Codex pass; canva CC/Codex/GB pass; hubspot-sales CC/GB pass; legalzoom CC/GB pass; zapier CC/GB pass.
   Reply: "We install-tested all 7 last night: QuickBooks, Stripe, Shopify, Canva, HubSpot, LegalZoom and Zapier installed clean in every coding agent we ran them in. SkillMaxx tests 428 agent add-ons nightly across 5 agents and posts what breaks. Which one stuck for you after week one?"
3. ~1:00 PM: @Mike_Andreuzza Lexington MCP launch (12.8k followers, 3 replies, posted 4:34 AM ET). https://x.com/Mike_Andreuzza/status/2123711481128882540
   Checked lexingtonthemes.com/mcp: the Prima Persona theme is open without a key, the paid plans are $99/$399 a year, and it supports 9 clients. The page doesn't say which client is used most.
   Reply: "Leaving Prima Persona open with no key is a smart way to try it. SkillMaxx install-tests 428 agent add-ons every night across Claude Code, Codex, Cursor, Grok Build and Pi and posts what breaks. Which client are most of the early keys connecting from, Cursor or Claude Code?"
4. Optional, ~3:00 PM: @Dinosn shared EL4CTEO/blender-skills (166k followers, 0 replies, posted 12:26 AM ET). https://x.com/Dinosn/status/2123649217126174920
   Reply: "Handy README detail: the installer puts the skills in both ~/.claude/skills and ~/.agents/skills, so one run covers Claude Code, Codex and Cursor. SkillMaxx install-tests 428 agent add-ons nightly in 5 coding agents; adding these to the run. Tried them with a Blender MCP server?"
   PROMISE: add EL4CTEO/blender-skills to the nightly run.
- Skipped: @badlogicgames (an OpenAI caching bug, not our lane); @swyx on Cursor Origin (not our lane); @hexobuilds (same topic as #2, so no near-duplicate); @waldekm (engaged 3 times in 14 days).
- Directory candidates: nestjs/agent-skills, EL4CTEO/blender-skills (2.5k stars), elementalsouls/Claude-BugHunter (13.4k stars, trending), Lexington MCP (paid; keyless Prima Persona), moka-harness, hearth (Home Repo CLI).

## Reddit (comments only)
- r/ClaudeAI: search `plugin not loading` or `plugin installed but skills` (sort New, past week). The comment covers `claude --plugin-dir ./your-plugin plugin details your-plugin` and pinning `@claude-plugins-official`.
- r/cursor: search `skills folder` or `.agents/skills` (sort New, past week). The comment covers which folders Cursor reads and the MCP "ready" check. Cursor was 33/55 last night.

## LinkedIn connection picks (§0)
- DataHub: Lakshay Nasa, Developer Advocate. VERIFIED.
  Sources: (1) the luma.com/user/lakshayn host page, "Developer Advocate @DataHub", which lists DataHub Office Hours he hosted Nov 10 and Nov 17, 2026, plus upcoming sessions on Nov 24, Dec 1 and Dec 18; (2) his LinkedIn, Developer Advocate at DataHub, Feb 2026 to Present, plus a repost on Nov 10, 2026; (3) the DataHub March 2026 Town Hall intro and github.com/lakshay-nasa. No newer role was found; he was at Zyte until Dec 2025.
  Angle: the datahub-skills README Evals skill (answers in a fresh agent, no verdict, DataHub judge). Result: datahub-skills passed in CC and GB on Nov 20.
  Note: "Hi Lakshay, the DataHub skills plugin installed clean in Claude Code and Grok Build in our latest nightly install tests. The new evals skill answers each eval in a fresh agent and leaves the verdict to DataHub's judge. Are teams using it to compare coding agents? Would love to connect."
- TinyFish: Simantak Dabhade, DevRel and Growth. VERIFIED.
  Sources: (1) the tinyfish.ai/blog/author/simantak-dabhade page (live, "DevRel and Growth", latest post Nov 5, 2026); (2) his LinkedIn, TinyFish DevRel/Growth. No newer role was found; Sangria is his own open-source project.
  Angle: the tinyfish-web-agent-integrations README says the Pi package works through an MCP adapter or the TinyFish CLI. Result: tinyfish passed in GB on Nov 20.
  Note: "Hi Simantak, the TinyFish Grok Build plugin installed clean in our latest nightly install tests. Your Pi package reaches TinyFish through either an MCP adapter or the TinyFish CLI. Which path do Pi users actually pick? Would love to connect."
- Atlan: Vivek Dubey, Product, Growth & Community. VERIFIED (Brandon confirms "Present").
  Sources: (1) atlan.com/context-and-chaos/experts/vivek-dubey (live: "leads product, growth, and community at Atlan"); (2) his LinkedIn posts promoting Atlan's Oct 28, 2026 Context Conference (Oct 2026). No newer role was found.
  Angle: the atlanhq/agent-toolkit README still says "Install from marketplace (when available)", but atlan is already in claude-plugins-official. Result: atlan passed in CC and GB on Nov 20.
  Note: "Hi Vivek, the Atlan plugin installed clean in Claude Code and Grok Build in our latest nightly install tests. It's already in Claude's official directory, but the agent-toolkit README still says "Install from marketplace (when available)". Is that line getting updated? Would love to connect."
- Not used: You.com Jan Yake (LinkedIn only, so UNVERIFIED); Ory Vincent Kraus (no dated source within 90 days); NightVision, Synthflow and Wingspan (no fitting named contact found).

## LinkedIn after-accept (drafted Nov 16 in chat, not marked sent anywhere; Brandon skips any already sent)
Chris Griffing (GitKraken, replied), Adonai Vera (Voxel51), Liran Tal (Snyk), Ríona Hegarty (Aiven), Yukta Kandhari. The text is in the Nov 20 queue message.

## Notes
- Bluesky: the Younes Jaaidi angular-testing promise was DONE Nov 19 (the prep list is stale because PENDING-REPLIES.md is uncommitted in /workspace/wt-1119). angular-testing passed in all 5 agents again on Nov 20. Nothing else notable.
- The owner dashboard "Brandon's queue" section was not updated by this run, because the pages/canvas tools weren't available to the subagent.

---
## Full queue message as delivered
# Brandon's SkillMaxx queue: Fri Nov 20 (~25 min)
Numbers: last night's report (Nov 20) had 906 of 1,075 installs passing across 428 add-ons. https://skillmaxx.gilventures.ai/reports/2026-11-20/
Yesterday's X radar picks were 22 to 35 hours old, so I dropped them. No next-day follow-ups and no DMs are due today. Nothing has been posted or sent.

## 1. X replies (spread through the day: tap Open post, Reply, paste)

**1 · ~9:00 AM: @nestframework, official NestJS agent skills** (44k followers, 160 likes, 28 replies, 1.5h old)
Open post: https://x.com/nestframework/status/2123741121482489930
```
Shipping it inside nest new is the smart part. SkillMaxx install-tests 428 agent add-ons nightly in Claude Code, Codex, Cursor, Grok Build and Pi; adding nestjs to the run. Any plan to list it in Claude's official plugin directory, or is your marketplace + npm the main path?
```
(I checked first: `nest new` already installs them for all agents by default, and the README covers Nest versions. The official-directory question isn't answered anywhere.)

**2 · ~11:00 AM: @simplifyinAI, "532 Claude plugins" list** (40.9k followers, 3 replies, still early)
Open post: https://x.com/simplifyinAI/status/2123726359335669777
```
We install-tested all 7 last night: QuickBooks, Stripe, Shopify, Canva, HubSpot, LegalZoom and Zapier installed clean in every coding agent we ran them in. SkillMaxx tests 428 agent add-ons nightly across 5 agents and posts what breaks. Which one stuck for you after week one?
```

**3 · ~1:00 PM: @Mike_Andreuzza, Lexington MCP launch** (12.8k followers, 3 replies)
Open post: https://x.com/Mike_Andreuzza/status/2123711481128882540
```
Leaving Prima Persona open with no key is a smart way to try it. SkillMaxx install-tests 428 agent add-ons every night across Claude Code, Codex, Cursor, Grok Build and Pi and posts what breaks. Which client are most of the early keys connecting from, Cursor or Claude Code?
```

**4 · Optional, ~3:00 PM: @Dinosn shared blender-skills** (166k followers, 0 replies so far)
Open post: https://x.com/Dinosn/status/2123649217126174920
```
Handy README detail: the installer puts the skills in both ~/.claude/skills and ~/.agents/skills, so one run covers Claude Code, Codex and Cursor. SkillMaxx install-tests 428 agent add-ons nightly in 5 coding agents; adding these to the run. Tried them with a Blender MCP server?
```

## 2. Reddit (comments only; leave 5+ min between them)

**r/ClaudeAI**: search `plugin not loading` or `plugin installed but skills` (sort New, past week). Pick a thread where someone's plugin or skill isn't showing up.
```
Two checks that catch most of these:

1. Pin the marketplace when you install: claude plugin install <name>@claude-plugins-official. A lot of plugin names now exist in more than one marketplace.
2. Run claude plugin list and make sure it says enabled. Installed and enabled aren't the same thing.

If it's a standalone skill, check the folder: Claude Code reads .claude/skills/. Some installers default to .agents/skills/, which Codex and Cursor read but Claude Code doesn't.

(Disclosure: I run SkillMaxx, which install-tests agent add-ons every night, so I hit this a lot.)
```

**r/cursor** (later in the day): search `skills folder` or `mcp not showing` (sort New, past week).
```
Two things to check:

- Skills: Cursor reads .agents/skills/ and .cursor/skills/ (project or ~/), and it also loads .claude/skills/. So a skill you installed for Claude Code often already works in Cursor.
- MCP: run cursor-agent mcp list. Anything other than "ready" means the tools won't show up, and the log usually says it wants a key or an argument.

In our nightly install tests, 33 of 55 Cursor installs passed last night. Disclosure: I run SkillMaxx (nightly install tests across 5 coding agents).
```

## 3. LinkedIn

**New connection requests** (I checked each person against two independent sources; before you send, make sure the top job says the company and "Present")

- **Lakshay Nasa, Developer Advocate, DataHub**
  Sales Nav: Current company `DataHub` · Keywords `Lakshay Nasa` · Free search: `Lakshay Nasa DataHub`
  Sources: he hosted DataHub Office Hours on Nov 10 and Nov 17 (Luma), and his LinkedIn shows Feb 2026 to Present.
```
Hi Lakshay, the DataHub skills plugin installed clean in Claude Code and Grok Build in our latest nightly install tests. The new evals skill answers each eval in a fresh agent and leaves the verdict to DataHub's judge. Are teams using it to compare coding agents? Would love to connect.
```
- **Simantak Dabhade, DevRel and Growth, TinyFish**
  Sales Nav: Current company `TinyFish` · Keywords `Simantak Dabhade` · Free search: `Simantak Dabhade TinyFish`
  Sources: his TinyFish blog author page (latest post Nov 5) and his LinkedIn.
```
Hi Simantak, the TinyFish Grok Build plugin installed clean in our latest nightly install tests. Your Pi package reaches TinyFish through either an MCP adapter or the TinyFish CLI. Which path do Pi users actually pick? Would love to connect.
```
- **Vivek Dubey, Product, Growth & Community, Atlan**
  Sales Nav: Current company `Atlan` · Keywords `Vivek Dubey` · Free search: `Vivek Dubey Atlan`
  Sources: his atlan.com expert page (live) and his Oct 2026 posts about Atlan's Context Conference.
```
Hi Vivek, the Atlan plugin installed clean in Claude Code and Grok Build in our latest nightly install tests. It's already in Claude's official directory, but the agent-toolkit README still says "Install from marketplace (when available)". Is that line getting updated? Would love to connect.
```

**After-accept messages** (I drafted these Nov 16 and nothing shows them as sent; skip any you already sent)

Chris Griffing (GitKraken; he replied that auth fits best in MCP servers):
```
Thanks Chris, that split makes sense: auth stays in the MCP server, skills carry the know-how.

The GitKraken plugin installed clean in Claude Code and Grok Build again in last night's run.

If GitKraken does ship skills, would they live inside the same plugin or as a separate pack?

Site: https://skillmaxx.gilventures.ai
X: https://x.com/SkillMaxxAI
Bluesky: https://bsky.app/profile/skillmaxx.bsky.social
```
Adonai Vera (Voxel51):
```
Thanks for connecting, Adonai!

I run SkillMaxx, a free directory that install-tests 428 agent skills, plugins and MCP servers every night across Claude Code, Codex, Cursor, Grok Build and Pi. The FiftyOne plugin installed clean in Claude Code and Grok Build again last night.

Site: https://skillmaxx.gilventures.ai
X: https://x.com/SkillMaxxAI
Bluesky: https://bsky.app/profile/skillmaxx.bsky.social

When Voxel51 Agent learns a workflow as a skill, does it write a standard SKILL.md that people could share?
```
Liran Tal (Snyk):
```
Thanks for connecting, Liran!

I run SkillMaxx, a free directory that install-tests 428 agent skills, plugins and MCP servers every night across Claude Code, Codex, Cursor, Grok Build and Pi.

Site: https://skillmaxx.gilventures.ai
X: https://x.com/SkillMaxxAI
Bluesky: https://bsky.app/profile/skillmaxx.bsky.social

Did Snyk's skills audit end up checking whether skills actually install, or content only?
```
Ríona Hegarty (Aiven):
```
Thanks for connecting, Ríona!

I run SkillMaxx, a free directory that install-tests 428 agent skills, plugins and MCP servers every night across Claude Code, Codex, Cursor, Grok Build and Pi. Aiven's plugin installed clean in Claude Code and Grok Build in last night's run.

Site: https://skillmaxx.gilventures.ai
X: https://x.com/SkillMaxxAI
Bluesky: https://bsky.app/profile/skillmaxx.bsky.social

Anything on Aiven's agent roadmap you'd like us to keep an eye on?
```
Yukta Kandhari:
```
Thanks for connecting, Yukta!

I run SkillMaxx, a free directory that install-tests 428 agent skills, plugins and MCP servers every night across Claude Code, Codex, Cursor, Grok Build and Pi.

Site: https://skillmaxx.gilventures.ai
X: https://x.com/SkillMaxxAI
Bluesky: https://bsky.app/profile/skillmaxx.bsky.social

What are you building with agents these days?
```

## Notes
- Bluesky: nothing for you. Younes's angular-testing promise was closed Nov 19, and the skill passed in all 5 agents again last night.
- Still blocked: FusionAuth is do-not-contact; Sylvain Kalache (Rootly) is blocked until ~Dec 7.
