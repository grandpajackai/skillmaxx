# SkillMaxx

Find agent skills, plugins and MCP servers, and see which coding agents (Claude Code, Codex, Grok Build, Cursor, Pi) they work in. Each one is checked against official docs and tested hands-on in a sandbox.

- Site: https://grandpajackai.github.io/skillmaxx/
- Data: `data/skills.json` (built by `build_data.py`), metadata and logos: `fetch_meta.py`
- Hands-on tests: `testing/` (`setup_agents.sh`, `run_tests.py`, `sbx.sh`, results in `testing/results/`)
- Build: `npm ci && npx @11ty/eleventy`. Set `PATH_PREFIX=/` and `SITE_URL=...` for a custom domain.

Independent, not affiliated with Anthropic, OpenAI, xAI, Anysphere or Pi.
