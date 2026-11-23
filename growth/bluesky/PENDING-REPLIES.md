# Pending Bluesky replies

## ✅ DONE 2026-10-31 — @claimidx.bsky.social — reply on our pinned post (after the Oct 31 ~2 AM ET nightly)

Reply to @claimidx.bsky.social on our pinned post with claimidx's per-agent pass/fail results and link to the report. Also explain what "clean" means: installed + started vs. a tool call actually returned.

- Queued: added to data/skills.json as an mcp-server (`uvx --from claimidx[server] claimidx-mcp`), so it's tested in Claude Code and Cursor only (our harness doesn't run MCP servers in Codex, Grok Build or Pi). Report: https://skillmaxx.gilventures.ai/reports/2026-10-31/
- Pre-check Oct 30 (box, not published): Claude Code pass (✔ Connected), Cursor pass (ready, 29 tools listed).
- **What "clean" means (from testing/run_tests.py):** "clean" = the server installed and started in a fresh, keyless sandbox and the agent's own health check passed (Claude Code `claude mcp list` shows Connected / Cursor `cursor-agent mcp list` shows ready, i.e. the MCP handshake succeeded); we do NOT call any tool, so it does not mean a tool call returned a result.

- **Done 2026-10-31 ~1:08 PM ET:** replied in thread https://bsky.app/profile/skillmaxx.bsky.social/post/3myuduhyan522 to claimidx's post 3mz4s5ptugw2b: 5/5 clean (Claude Code, Codex, Cursor, Grok Build, Pi), 29 tools, explained 'clean' = installed+started+MCP handshake, no tool call; link to /reports/2026-10-31/.
- Their note for the logs: offline replay is only enforced on Linux with bubblewrap, so `held: false` elsewhere is expected, not a broken install. Recommended install: `pip install -U "claimidx[server]>=0.7.22"`.
- 2026-11-01: nothing pending.

## ✅ DONE 2026-11-09 — @aethelgardshuman.bsky.social (Marco) — agent-postbox results
Promised in https://bsky.app/profile/aethelgardshuman.bsky.social/post/3mz6ujwxww222: after the next nightly that includes agent-postbox (added to data/skills.json Nov 2), reply in that thread with per-agent client versions, transport (stdio), and the first failing step if any. Note it needs a config + GitHub token, so a keyless sandbox fail at config/token is expected; say so. Their compat list is github.com/Aethelgard-Systems/agent-postbox Issue #14.
- **Done 2026-11-09 ~1:20 PM ET:** replied to his post 3mze735ijck2f (our reply 3mzvk3ewyul2p): passed in all 5 agents every night Nov 3–8, stdio via npx; Claude Code 2.1.197 connected, Codex 0.163.0, Grok 1.0.62, Cursor 2026.10.16, Pi 1.4.0 each found 9 tools; no failing step (keyless start held); linked /skills/agent-postbox/. **Done 2026-11-23 ~8:31 AM ET (GitHub side):** posted updated results from `skillmaxxai` on https://github.com/Aethelgard-Systems/agent-postbox/issues/14#issuecomment-7102664968 — passed in all 5 agents on every published nightly from 2026-11-03 through 2026-11-23 (15 runs); stdio via `npx`; keyless start; client versions from the 2026-11-23 run (Claude Code 2.1.319, Codex 0.167.0, Grok Build 1.0.77, Cursor 2026.11.05-86047df, Pi 1.5.0).

## ⏳ OPEN (wishlist) — @claimidx.bsky.social — tool-call pass
Promised a tool-call pass using `claimidx_ask` with a known error string as the first call, then post the held true/false split. Only do this once the harness supports tool calls; until then nothing to post.

## ⏳ OPEN (wishlist) — @claimidx.bsky.social — compare first error line across nights
Nov 8 they suggested: before calling something broken, compare the first error line on both failing nights (same error = broken; different errors = likely environment). Replied Nov 9 (3mzvk5t4zd32p) that it's going on our list. Nothing more to post until the harness does it.

## ✅ DONE 2026-11-19 — @younesjd.dev (Younes Jaaidi) — Angular testing skill results
- **Done 2026-11-19 ~1:40 PM ET:** replied under our promise post (reply 3n2opa6ie2k2l): installed and loaded in all 5 agents on each of the last 3 nightly runs, keyless sandbox, link to /skills/angular-testing/.
Promised 2026-11-16 in a Bluesky reply (our post https://bsky.app/profile/skillmaxx.bsky.social/post/3n2h5chrt5c2a): nightly results across all 5 agents for his skill. Install: `npx skills add marmicode/skills --skill angular-testing` (repo github.com/marmicode/skills).
**2026-11-16 update: skill added, blocker gone.** Brandon chose to add standalone-skill testing instead of posting a correction (the drafted correction reply is dropped, do NOT post it). The harness now has item type `skill` (installed with the pinned skills CLI, then each agent must list it; Cursor = SKILL.md lands in ~/.agents/skills, which Cursor's CLI reads). `angular-testing` is in data/skills.json and is in the Nov 17 2 AM Mac run. Sandbox check on the Mac Nov 16 (not published, not a nightly): pass in all 5 agents.
**Next:** after the Nov 17 report publishes (4 AM ET routine), reply in his thread with the real per-agent results and links to https://skillmaxx.gilventures.ai/skills/angular-testing/ and the Nov 17 report. Draft it for Brandon's OK first; mark ✅ once posted. If Nov 17 doesn't publish, wait for the next published night; never quote the unpublished sandbox check as nightly results.
