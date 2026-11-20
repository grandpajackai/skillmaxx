# Queued blog drafts (4 weeks starting Nov 23, 2026)

Drafts in this folder stay outside `src/blog/` until their scheduled publish date so Eleventy
does not publish them early. On or after each file's `YYYY-MM-DD` date prefix, the Mac
no-LLM auto-publishers (`growth/scripts/midweek_blog_auto.py` and
`growth/scripts/weekly_blog_auto.py`, invoked by `testing/publish_nightly.sh`) pick up the
matching draft, refresh every `[[SMX:...]]` token from the latest committed nightly data
(`testing/results/<date>.json`, `src/_data/reports.json`, `src/_data/weeks.json`,
`data/skills.json`, `src/_data/runNotes.json`), validate JSON-LD and placeholders, and write
the finished `.njk` post into `src/blog/`.

| Publish date | ISO week | File -> Output | Live URL | Angle / target query |
|---|---|---|---|---|
| Wed 2026-11-25 | 2026-48 | `2026-11-25--midweek-2026-48.njk` -> `src/blog/midweek-2026-48.njk` | `/blog/midweek-2026-48/` | MCP servers vs plugins (`cursor mcp server not working`, `best mcp servers for claude code`) |
| Sun 2026-11-29 | 2026-48 | `2026-11-29--week-2026-48.njk` -> `src/blog/week-2026-48.njk` | `/blog/week-2026-48/` | Week 48 scorecard + why Pi lags on plugins (`claude code plugins vs skills`) |
| Wed 2026-12-02 | 2026-49 | `2026-12-02--midweek-2026-49.njk` -> `src/blog/midweek-2026-49.njk` | `/blog/midweek-2026-49/` | API-key failures vs broken MCP servers (`is mcp server safe to use`) |
| Sun 2026-12-06 | 2026-49 | `2026-12-06--week-2026-49.njk` -> `src/blog/week-2026-49.njk` | `/blog/week-2026-49/` | Week 49 scorecard + Codex vs Claude Code vs Cursor MCP (`best mcp servers for codex`) |
| Wed 2026-12-09 | 2026-50 | `2026-12-09--midweek-2026-50.njk` -> `src/blog/midweek-2026-50.njk` | `/blog/midweek-2026-50/` | Pass rates by category (`best claude code plugins for developers`) |
| Sun 2026-12-13 | 2026-50 | `2026-12-13--week-2026-50.njk` -> `src/blog/week-2026-50.njk` | `/blog/week-2026-50/` | Week 50 scorecard + Grok Build vs Claude Code (`grok build vs claude code`) |
| Wed 2026-12-16 | 2026-51 | `2026-12-16--midweek-2026-51.njk` -> `src/blog/midweek-2026-51.njk` | `/blog/midweek-2026-51/` | Skills vs plugins vs MCP servers (`claude skills vs mcp vs plugins`) |
| Sun 2026-12-20 | 2026-51 | `2026-12-20--week-2026-51.njk` -> `src/blog/week-2026-51.njk` | `/blog/week-2026-51/` | Week 51 scorecard + Pi MCP vs GitHub plugins (`pi coding agent mcp`) |
