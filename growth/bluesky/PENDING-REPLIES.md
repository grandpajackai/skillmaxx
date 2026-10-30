# Pending Bluesky replies

## @claimidx.bsky.social — reply on our pinned post (after the Oct 31 ~2 AM ET nightly)

Reply to @claimidx.bsky.social on our pinned post with claimidx's per-agent pass/fail results and link to the report. Also explain what "clean" means: installed + started vs. a tool call actually returned.

- Queued: added to data/skills.json as an mcp-server (`uvx --from claimidx[server] claimidx-mcp`), so it's tested in Claude Code and Cursor only (our harness doesn't run MCP servers in Codex, Grok Build or Pi). Report: https://skillmaxx.gilventures.ai/reports/2026-10-31/
- Pre-check Oct 30 (box, not published): Claude Code pass (✔ Connected), Cursor pass (ready, 29 tools listed).
- **What "clean" means (from testing/run_tests.py):** "clean" = the server installed and started in a fresh, keyless sandbox and the agent's own health check passed (Claude Code `claude mcp list` shows Connected / Cursor `cursor-agent mcp list` shows ready, i.e. the MCP handshake succeeded); we do NOT call any tool, so it does not mean a tool call returned a result.
