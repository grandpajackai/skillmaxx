# Launch drafts: Show HN + Product Hunt (DRAFTS, not posted)

Brandon posts these himself from his own accounts. HN and Product Hunt penalize automated or promotional accounts. Re-pull the numbers from the latest nightly report the day you post. Everything below is from the **Oct 30, 2026 nightly** (`src/_data/latestRows.json`, /reports/2026-10-30/).

Facts used: 900 installs, 423 add-ons, 5 agents. 809 installed clean, 79 broke, 12 needed an API key the sandbox doesn't have. Per agent: Codex 65/65, Claude Code 341/367, Grok Build 317/330, Cursor 30/52, Pi 56/86. 65 add-ons pass in 3+ agents. Sandbox versions are older than current releases (Claude Code 2.1.197, Grok 1.0.62), so say so if anyone asks.

Known caveats to state up front: MCP servers are only tested in Claude Code and Cursor today (Codex, Grok Build and Pi MCP coverage is in progress), and "clean" means it installs and starts/connects. We don't call tools yet.

---

## Show HN

**Title (≤80 chars):**
Show HN: SkillMaxx – we install 900 coding-agent add-ons nightly to see what works

**URL:** https://skillmaxx.gilventures.ai/reports/latest/

**First comment (post right after submitting):**
Hi HN, I'm Brandon. Agent skills, plugins and MCP servers are multiplying fast, and "works with Claude Code, Cursor, Codex…" claims are rarely tested. So every night we install each add-on in a fresh sandbox for Claude Code, Codex, Grok Build, Cursor and Pi, and publish the result and the log.

Last night (Oct 30): 900 installs across 423 add-ons. 809 installed clean, 79 broke, 12 only failed because the sandbox has no API key. The spread by agent surprised us: Codex 65/65, Claude Code 341/367, Grok Build 317/330, Cursor 30/52, Pi 56/86. Only 65 add-ons pass in 3 or more agents.

Limits, honestly: "clean" means it installs and starts or connects. We don't call tools yet. MCP servers are only tested in Claude Code and Cursor so far, and our sandbox agent versions lag the latest releases.

It's free. I'd love feedback on what a deeper test should look like, and which add-ons we should add.

---

## Product Hunt

**Name:** SkillMaxx
**Tagline (≤60 chars):** Nightly install tests for AI coding-agent add-ons
**Topics:** Developer Tools, Artificial Intelligence, Open Source (check Open Source applies before picking)

**Description (≤260 chars):**
Every night SkillMaxx installs 900+ skills, plugins and MCP servers in Claude Code, Codex, Grok Build, Cursor and Pi in clean sandboxes, and publishes what works, what breaks and the logs. Free directory, daily reports.

**Maker comment:**
Hey Product Hunt 👋 I built SkillMaxx because "works in every agent" rarely holds. On Oct 30 we ran 900 installs: 809 clean, 79 broken, 12 needing a key. Codex was 65/65, while Cursor was 30/52 and Pi 56/86. Only 65 of 423 add-ons pass in 3+ agents. Today "clean" means it installs and connects; tool-call tests are next. What should we test that we aren't?

**Gallery ideas (real screenshots only):** the Oct 30 report table, one add-on's per-agent page, one failure log.
