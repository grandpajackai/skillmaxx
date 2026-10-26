# Reddit pack (account u/SkillMaxxHQ). DRAFTS, nothing posted.

Rules notes are from each sub's known rules; **re-read the sidebar right before posting**, they change. General: one sub per day max, reply to every comment for the first 2 hours, no cross-posting the same text, disclose "I built this".
New-account caution: u/SkillMaxxHQ has little karma. Several subs filter new accounts, so spend a few days commenting helpfully first, or post from your personal account with disclosure (your call).

---
## 1. r/mcp — flair: Showcase / Resource
**Rules to respect:** MCP-related only, self-promo allowed as showcase with disclosure, no spam/repeat posts.

**Title:** I install MCP servers in 5 agents every night with no API keys. Here's what actually connects (and I need feedback)

**Body:**
I built a little test rig (disclosure: it's my project, SkillMaxx). Every night it adds MCP servers to fresh sandboxes for Claude Code, Codex, Grok Build, Cursor and Pi, and counts a server as working only if the agent reports it connected and lists its tools.

Things I learned that might save you time:
- **Most "failures" are missing keys, not bugs.** 12 installs last night only failed because the sandbox has no credentials, so I now list those separately.
- **One bad night means nothing.** 13 servers/plugins flip-flopped this week. I only call something broken after two failing nights in a row.
- **Cursor is strict.** In ~/.cursor/mcp.json the server has to show "ready". 27 of 46 judgeable installs did.
- The official reference servers (fetch, filesystem, git, memory, time) are still the most boring and most reliable.

Results are public: https://skillmaxx.gilventures.ai/reports/latest/

Honest questions, because it's early:
1. Is "installs + connects with no keys" a useful signal for you, or do you need a deeper test (actually calling a tool)?
2. Which servers should I add?
3. If I got your server wrong, tell me and I'll rerun it.

---
## 2. r/ClaudeAI — flair: "Built with Claude" (or Productivity) 
**Rules to respect:** must be about Claude; self-promo only with clear disclosure and value in the post; no low-effort link drops.

**Title:** Tested 367 Claude Code plugin installs in clean sandboxes. Notes on what fails and why

**Body:**
Disclosure: I run SkillMaxx, a free directory that test-installs agent plugins every night. Sharing the Claude Code findings because they're useful on their own:

- 340 of 367 Claude Code installs passed last night. 6 of the misses only needed an API key.
- **Always pin the marketplace**: `/plugin install sentry@claude-plugins-official`. Plugin names now exist in multiple marketplaces.
- Grok Build auto-loads Claude Code plugins, so many plugins work in both without the author doing anything.
- Flip-flopping installs are common (network, rate limits), so I wait for 2 bad nights before calling anything broken.

Per-plugin results with logs: https://skillmaxx.gilventures.ai/reports/latest/

I'd really like feedback: what's the Claude Code plugin you'd most want checked before installing? And is this kind of report useful or overkill?

---
## 3. r/cursor — flair: Showcase / Resources
**Rules to respect:** Cursor-related, showcase flair for projects, no referral/affiliate links.

**Title:** Which MCP servers actually connect in Cursor? I test them every night (free list)

**Body:**
I made a list of every MCP server I could install in a real Cursor CLI sandbox (no accounts, no keys), counting it only if Cursor says ready and lists tools. Disclosure: it's my project.

Current numbers: 27 of 46 judgeable installs connected; 6 more only failed for lack of an API key. Full list with the exact mcp.json entry for each: https://skillmaxx.gilventures.ai/guides/best-mcp-servers-cursor/

Tip that fixed most of my own issues: if Cursor shows anything other than "ready", it's not running, and the log usually says it wants a key or an argument.

What MCP servers are you using in Cursor that I'm missing? I'll add them to the nightly run.

---
## 4. r/SideProject — flair: none needed
**Rules to respect:** self-promo is the point; be genuine, no fake engagement.

**Title:** I built a directory that installs every AI agent plugin every night and publishes what breaks. 10 days in, $0 spent, here's what I learned

**Body:**
SkillMaxx (https://skillmaxx.gilventures.ai) installs 424 agent skills/plugins/MCP servers across 5 coding agents every night and posts the results.

What I learned in 10 days:
- My first daily reports were mostly noise. 13 of 14 "fixed" items were flaky. Now I need 2 bad nights before I call anything broken.
- Being honest about limits (no API keys in the sandbox) made the data more trustworthy, not less.
- Static site + nightly script + GitHub Pages = $0 running cost.

I'd love blunt feedback: does the homepage make sense in 5 seconds? Would you subscribe to a weekly install scorecard, or is that a snooze?
