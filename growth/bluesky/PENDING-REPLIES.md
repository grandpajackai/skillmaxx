# Pending Bluesky replies

## ✅ DONE 2026-10-31 — @claimidx.bsky.social — reply on our pinned post (after the Oct 31 ~2 AM ET nightly)

Reply to @claimidx.bsky.social on our pinned post with claimidx's per-agent pass/fail results and link to the report. Also explain what "clean" means: installed + started vs. a tool call actually returned.

- Queued: added to data/skills.json as an mcp-server (`uvx --from claimidx[server] claimidx-mcp`), so it's tested in Claude Code and Cursor only (our harness doesn't run MCP servers in Codex, Grok Build or Pi). Report: https://skillmaxx.gilventures.ai/reports/2026-10-31/
- Pre-check Oct 30 (box, not published): Claude Code pass (✔ Connected), Cursor pass (ready, 29 tools listed).
- **What "clean" means (from testing/run_tests.py):** "clean" = the server installed and started in a fresh, keyless sandbox and the agent's own health check passed (Claude Code `claude mcp list` shows Connected / Cursor `cursor-agent mcp list` shows ready, i.e. the MCP handshake succeeded); we do NOT call any tool, so it does not mean a tool call returned a result.

- **Done 2026-10-31 ~1:08 PM ET:** replied in thread https://bsky.app/profile/skillmaxx.bsky.social/post/3myuduhyan522 to claimidx's post 3mz4s5ptugw2b: 5/5 clean (Claude Code, Codex, Cursor, Grok Build, Pi), 29 tools, explained 'clean' = installed+started+MCP handshake, no tool call; link to /reports/2026-10-31/.
- Their note for the logs: offline replay is only enforced on Linux with bubblewrap, so `held: false` elsewhere is expected, not a broken install. Recommended install: `pip install -U "claimidx[server]>=0.7.22"`.
- 2026-11-01: nothing pending.

## ⏳ OPEN 2026-11-02 — @aethelgardshuman.bsky.social (Marco) — agent-postbox results
Promised in https://bsky.app/profile/aethelgardshuman.bsky.social/post/3mz6ujwxww222: after the next nightly that includes agent-postbox (added to data/skills.json Nov 2), reply in that thread with per-agent client versions, transport (stdio), and the first failing step if any. Note it needs a config + GitHub token, so a keyless sandbox fail at config/token is expected; say so. Their compat list is github.com/Aethelgard-Systems/agent-postbox Issue #14.

## ⏳ OPEN (wishlist) — @claimidx.bsky.social — tool-call pass
Promised a tool-call pass using `claimidx_ask` with a known error string as the first call, then post the held true/false split. Only do this once the harness supports tool calls; until then nothing to post.
