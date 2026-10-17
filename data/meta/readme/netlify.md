# Netlify Context and Tools

Public Netlify skills for AI coding agents. Each skill is a focused, factual reference for a Netlify platform primitive — designed to help agents build correctly on Netlify without needing to search docs.

## Skills

| Skill | What it covers |
|---|---|
| [netlify-functions](skills/netlify-functions/SKILL.md) | Serverless functions — modern syntax, routing, background/scheduled/streaming |
| [netlify-edge-functions](skills/netlify-edge-functions/SKILL.md) | Edge compute — Deno runtime, middleware, geolocation |
| [netlify-blobs](skills/netlify-blobs/SKILL.md) | Object storage — key-value and binary data |
| [netlify-database](skills/netlify-database/SKILL.md) | Managed Postgres (Neon) with Drizzle ORM and migrations |
| [netlify-image-cdn](skills/netlify-image-cdn/SKILL.md) | Image transformation and optimization via CDN |
| [netlify-forms](skills/netlify-forms/SKILL.md) | HTML form handling, AJAX submissions, spam filtering |
| [netlify-config](skills/netlify-config/SKILL.md) | `netlify.toml` — redirects, headers, build settings, deploy contexts, environment variables |
| [netlify-frameworks](skills/netlify-frameworks/SKILL.md) | Framework adapters for Vite, Astro, TanStack, and Next.js |
| [netlify-caching](skills/netlify-caching/SKILL.md) | CDN cache control, cache tags, purge, stale-while-revalidate |
| [netlify-ai-gateway](skills/netlify-ai-gateway/SKILL.md) | AI Gateway proxy for OpenAI, Anthropic, and Google SDKs |
| [netlify-identity](skills/netlify-identity/SKILL.md) | User authentication — signups, logins, OAuth, role-based access control |
| [netlify-deploy](skills/netlify-deploy/SKILL.md) | CLI install/auth, site linking, Git-based and manual deploys, CI deploys, deploy troubleshooting |
| [netlify-access-control](skills/netlify-access-control/SKILL.md) | Protecting sites and previews — password protection, team-only access, visibility defaults, SSO |
| [netlify-agent-runner](skills/netlify-agent-runner/SKILL.md) | Running Claude, Codex, or Gemini agent tasks remotely against a site's repo |
| [netlify-mcp-servers](skills/netlify-mcp-servers/SKILL.md) | MCP servers on Netlify Functions — transport, authentication, connecting clients |

### References

Some skills include `references/` subdirectories with deeper content:

- [User-uploaded images pipeline](skills/netlify-image-cdn/references/user-uploads.md) — composing Functions + Blobs + Image CDN
- [Vite on Netlify](skills/netlify-frameworks/references/vite.md)
- [Astro on Netlify](skills/netlify-frameworks/references/astro.md)
- [TanStack Start on Netlify](skills/netlify-frameworks/references/tanstack.md)
- [Next.js on Netlify](skills/netlify-frameworks/references/nextjs.md)
- [Advanced identity patterns](skills/netlify-identity/references/advanced-patterns.md) — external providers, role-based access, server-side validation
- [CLI commands reference](skills/netlify-deploy/references/cli-commands.md)
- [Deployment patterns](skills/netlify-deploy/references/deployment-patterns.md)
- [netlify.toml guide](skills/netlify-deploy/references/netlify-toml.md)

## Installation

One command installs the skills into any project, from the released [`@netlify/skills`](https://www.npmjs.com/package/@netlify/skills) package:

```bash
npx @netlify/skills@latest add --all
```

It writes the skills into the agent directory already in the project (`.claude/`, `.agents/`, or `.grok/`) and never guesses: with none, or more than one, it asks for `--agent`.

| Agent | `--agent` | Skills directory |
|---|---|---|
| Claude Code | `claude-code` | `.claude/skills/` |
| Cursor | `cursor` | `.agents/skills/` |
| Codex | `codex` | `.agents/skills/` |
| Gemini CLI | `gemini-cli` | `.agents/skills/` |
| GitHub Copilot, VS Code | `github-copilot` | `.agents/skills/` |
| Grok Build | `grok` | `.grok/skills/` |
| Anything else | | `--dest <dir>` |

Each directory is the project-level skills location in that agent's own docs: [Claude Code](https://code.claude.com/docs/en/skills), [Cursor](https://cursor.com/docs/context/skills), [Codex](https://developers.openai.com/codex/skills), [Gemini CLI](https://geminicli.com/docs/cli/skills/), [GitHub Copilot](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills), and [Grok](https://docs.x.ai/build/features/skills-plugins-marketplaces). Cursor, Codex, Gemini CLI, and Copilot all read the shared `.agents/skills/`. The generated `.cursor/rules/` files and the `codex/AGENTS.md` router under [Other ways to install](#other-ways-to-install) are the older formats for those two agents; they still work, but they are not what `add` writes.

`add netlify-functions` installs one skill, `check` reports what is installed and whether it is current, and `update` brings it up to date. See [Install skills and keep them current](#install-skills-and-keep-them-current).

### Other ways to install

Each agent's plugin marketplace carries the same skills, packaged the way that agent manages plugins (with the Netlify MCP server bundled where the format allows). Use one of these when you want the agent, not the repo, to own the install.

#### Codex Desktop App

Install the Netlify plugin from the [Codex plugin directory](https://developers.openai.com/codex/plugins/) in the Codex desktop app.

The plugin lets Codex deploy to Netlify without leaving your coding workflow. You can create projects, generate preview URLs, deploy to production, validate build configuration, and inspect deploy status and logs. For full details, refer to [Deploy from Codex with the Netlify Plugin](https://www.netlify.com/changelog/2026-03-27-deploy-from-codex-netlify-plugin/).

#### Codex CLI

Copy the pre-built `codex/` directory into your project root:

```bash
git clone --depth 1 https://github.com/netlify/context-and-tools.git /tmp/netlify-skills && \
  cp -r /tmp/netlify-skills/codex . && \
  rm -rf /tmp/netlify-skills
```

This gives you `codex/AGENTS.md` (the skill router) and `codex/skills/` with all Netlify skills. Codex discovers `AGENTS.md` automatically and activates skills by name using `$skill-name` syntax.

#### GitHub Copilot CLI

Copy the pre-built `codex/` directory into your project root, then point Copilot CLI at it:

```bash
git clone --depth 1 https://github.com/netlify/context-and-tools.git /tmp/netlify-skills && \
  cp -r /tmp/netlify-skills/codex . && \
  rm -rf /tmp/netlify-skills
```

```bash
export COPILOT_CUSTOM_INSTRUCTIONS_DIRS="$PWD/codex"
```

Copilot CLI reads `AGENTS.md` from any directory listed in `COPILOT_CUSTOM_INSTRUCTIONS_DIRS` and uses it as a router into the skill files under `codex/skills/`. Add the export to your shell profile to persist across sessions.

#### Claude Code

Add the marketplace and install the plugin:

```
/plugin marketplace add netlify/context-and-tools
/plugin install netlify-skills@netlify-context-and-tools
```

This installs all Netlify skills into Claude Code. The included `skills/CLAUDE.md` acts as a router — it tells the agent which skill to read based on what you're building.

#### VS Code

VS Code's [agent plugins](https://code.visualstudio.com/docs/agent-customization/agent-plugins) use the same plugin format as Claude Code, so VS Code installs the skills directly from this repository — no separate build step or generated output. VS Code auto-detects the plugin from `.claude-plugin/plugin.json` and loads the `skills/` directory and the bundled Netlify MCP server (`.mcp.json`).

Add this repository as a plugin marketplace, then install:

1. Add the marketplace source `netlify/context-and-tools` to the `chat.plugins.marketplaces` setting.
2. Open the Extensions view, search `@agentPlugins`, find **netlify-skills**, and click **Install**.

Or install directly from source via the command palette: `Cmd+Shift+P` / `Ctrl+Shift+P` → **Chat: Install Plugin From Source** → enter `https://github.com/netlify/context-and-tools.git`.

#### Cursor

Install from the [Cursor plugin marketplace](https://cursor.com/marketplace):

1. Open Cursor Settings (`Cmd+,` / `Ctrl+,`)
2. Go to **Plugins**
3. Search for **netlify-skills**
4. Click **Install**

Or install via the command palette: `Cmd+Shift+P` → **Plugins: Install Plugin** → search **netlify-skills**.

This installs 21 `.mdc` rule files covering all Netlify platform primitives. A router rule (`netlify-skills-router.mdc`) is always active and directs the agent to the right skill for the task.

<details>
<summary>Manual installation (without the plugin marketplace)</summary>

Copy pre-built rule files directly into your project:

```bash
git clone --depth 1 https://github.com/netlify/context-and-tools.git /tmp/netlify-skills && \
  mkdir -p .cursor/rules && \
  cp /tmp/netlify-skills/cursor/rules/*.mdc .cursor/rules/ && \
  rm -rf /tmp/netlify-skills
```

This copies `.mdc` rule files into `.cursor/rules/`, where Cursor automatically discovers them.

</details>



#### Grok Build

Netlify is listed in the [official xAI plugin marketplace](https://github.com/xai-org/plugin-marketplace). In Grok Build, open the extensions modal (`/plugins`) and use the **Marketplace** tab to find and install **netlify**.

Grok Build uses the same plugin format as Claude Code, so it installs all Netlify skills directly from this repository — no separate build step or generated output. Marketplace sources live in `~/.grok/config.toml` under `[[marketplace.sources]]`; if the xAI marketplace isn't already configured, add it there. See the [xAI Skills, Plugins & Marketplaces docs](https://docs.x.ai/build/features/skills-plugins-marketplaces) for details.

#### Netlify MCP server

The Claude Code, VS Code, and Grok Build plugins (and the Gemini CLI extension) also register the [official Netlify MCP server](https://docs.netlify.com/build/build-with-ai/netlify-mcp-server/), giving the agent tools to create and manage Netlify projects, deploys, and environment variables — not just the reference skills.

It connects to Netlify's hosted server over HTTP (`https://netlify-mcp.netlify.app/mcp`) and authorizes via OAuth on first use — no token or local install required. The rules-based integrations (Cursor, Codex, Copilot) don't bundle the MCP server — add it to those clients manually using the [Netlify MCP docs](https://docs.netlify.com/build/build-with-ai/netlify-mcp-server/).

#### Other AI agents

Each `SKILL.md` file is a self-contained reference with YAML frontmatter (`name` and `description`) and markdown body. Feed them into any agent's context as needed.

## Hosted skills, manifest, and npm

Every release publishes the skills to two places you can consume without cloning this repo:

- **Hosted:** `https://netlify-agent-skills.netlify.app` — `manifest.json` and `skills/<name>/<file>` for the latest release, `versions.json` listing every published version, and immutable copies at `v/<version>/…`.
- **npm:** [`@netlify/skills`](https://www.npmjs.com/package/@netlify/skills) — every skill plus `manifest.json` and the `netlify-skills` command, which installs single skills out of the package.

Skill files under `v/<version>/` are exact `git archive` bytes of the tag and never change. Each `v/<version>/manifest.json` is regenerated on publish, but its `tree_hash` formula is frozen for `schema_version: 1`, so a pinned hash stays valid.

The manifest is the contract every client syncs against. It lists each skill's name, status (`active` or `deprecated`), its own `version`, prior names, description, a per-file SHA-256, and a `tree_hash` over path, executable bit, and content that changes whenever any file in the skill changes, so "am I stale?" is one hash comparison.

Skills change independently, so each carries its own version: the release in which its files last changed. The set might be at 1.6.0 while `netlify-functions` is still at 1.4.2 because nothing in it has moved since. Pin a skill by its own version: `v/1.4.2/skills/netlify-functions/…`. Nobody maintains these by hand; they are derived from git tags at publish time.

```bash
