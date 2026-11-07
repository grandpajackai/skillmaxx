# This repository has moved to [dominodatalab/domino-ai-plugin](https://github.com/dominodatalab/domino-ai-plugin)

# Domino Data Lab Plugin for Claude Code, ChatGPT, Codex, Cursor, Gemini CLI, and Antigravity

One source tree, several distributions. This repository is a **Claude Code plugin** as checked
in; the same checkout is a **Codex / ChatGPT plugin** (and builds the package for the OpenAI
plugin directory), a **Cursor plugin**, a **Gemini CLI extension**, and an **Antigravity
plugin** (`plugin.json` plus `mcp_config.json`). All of them share the
same skills; all but the OpenAI directory package, which is skills-only, also carry the same
always-on guidance and the same Domino MCP server.

> **Moved from `dominodatalab/domino-claude-plugin`.** That repository is deprecated and receives
> no new releases; this one replaces it. To switch an existing install, see
> [Updating (Claude Code)](#updating-claude-code).

## Overview

The plugin gives AI coding assistants skills for the main Domino Data Lab surfaces:

- **Workspaces**: Jupyter, VS Code, RStudio configuration and management
- **Jobs**: Batch execution, scheduled jobs, and monitoring
- **Environments**: Custom Docker environments and package management
- **Datasets**: Data versioning with snapshots and sharing
- **NetApp Volumes**: Enterprise-grade multi-terabyte storage with near-instant snapshots
- **Apps**: Deploy React, Streamlit, and Dash applications
- **Models**: Deploy, monitor, and manage model endpoints
- **GenAI**: Trace and evaluate AI agents with the Domino SDK
- **Distributed Computing**: Spark, Ray, Dask and Open MPI clusters, and Slurm HPC
- **Projects, Launchers, Flows, governance, tags and properties, LLM access, and the Domino APIs and SDKs**

Skills say which Domino versions they apply to; see [Compatibility](#compatibility).

## What ships where

| Component | Claude Code | ChatGPT / Codex | Cursor | Gemini CLI | Antigravity |
| --- | --- | --- | --- | --- | --- |
| `skills/` (35 skills) | ✅ | ✅ | ✅ | ✅ discovered from `skills/` | ✅ imported from `skills/` |
| Domino MCP server (`mcp-servers/`) | ✅ via `mcp-servers/domino_mcp_server/.mcp.json` (stdio) | Codex local install: ✅ via `mcp.json` (stdio). Public directory: needs a hosted HTTPS endpoint (see [OpenAI build](#openai-build)) | ✅ via `.cursor-plugin/mcp.json` (stdio; credentials from the env file, see [Your Domino URL and token](#your-domino-url-and-token)) | ✅ via `gemini-extension.json` (stdio; Gemini CLI asks for the same two values at install) | ✅ via `mcp_config.json` (stdio; credentials from `agy`'s environment or the env file) |
| Domino docs MCP server (`https://docs.domino.ai/mcp`) | ✅ via `.mcp.json` | Codex local install: ✅ via `mcp.json`. Not in the public directory package | ✅ via `.cursor-plugin/mcp.json` | ✅ via `gemini-extension.json` | ✅ via `mcp_config.json` |
| Always-on Domino guidance (`rules/domino.md`) | ✅ loaded at every session start by a `SessionStart` hook | Codex local install: the lead section, as the bundled MCP server's instructions. Not available to skills-only directory plugins | ✅ always-applied plugin rule (`alwaysApply: true`) | ✅ the extension's context file (`contextFileName`) | ✅ always-on rule (`trigger: always_on`) in the installed copy |
| Subagents (`agents/`) | ✅ routers that preload their skills | ❌ | Routing prompts only: Cursor loads `agents/` without `skills:` or `tools:`, so nothing is preloaded | ❌ the files are `_`-prefixed, which Gemini CLI skips (its sub-agent schema differs) | Imported as prompts (`agy` reports 3 agents); `skills:` and `tools:` are Claude Code fields |
| Output styles (`output-styles/`) | ✅ | ❌ Claude-only | ❌ | ❌ | ❌ |
| Hook examples (`hooks/`) | Docs only | ❌ | ❌ | ❌ | ❌ |
| Manifest | `.claude-plugin/plugin.json` | `plugin.json` ([Agent Plugins](https://agent-plugins.org) format) | `.cursor-plugin/plugin.json` | `gemini-extension.json` | `plugin.json`, read by `agy`, plus `mcp_config.json` |

Skills are written provider-neutral. Where an instruction really is host-specific (for example
which instructions file or MCP config file to write), the skill gives both the Claude Code and
the Codex variant. CI enforces this; see [Skill rules](#skill-rules).

---

## Your Domino URL and token

Inside a Domino Workspace, Job or App, nothing is needed: the bundled MCP server calls Domino
through `$DOMINO_API_PROXY`, which adds your identity. Leave the settings below empty there.

Everywhere else (your laptop, CI), the MCP server needs two values:

| Setting | What to enter | Where to get it |
|---|---|---|
| **Domino URL** (`DOMINO_HOST`) | The address you open Domino at in your browser: `https://` and the host name, no path, for example `https://domino.example.com` | Your browser's address bar while you use Domino. Not `DOMINO_API_HOST`, which inside Domino is an in-cluster address |
| **Token** (`DOMINO_TOKEN`) | A Personal Access Token, or a service account token for automation | In Domino: **Account** > **Account settings** > **Personal Access Token** > **Generate new Token**, choose an expiry, copy it ([docs](https://docs.domino.ai/cloud/reference/api/domino-api-authentication)). Legacy API keys don't work |

Each host takes them its own way:

| Host | How |
|---|---|
| Claude Code | Asks for both when you enable the plugin; the token goes to your system's secure credential store. Change them later in `/plugin` → **Installed** → **dominodatalab** → **Configure options**, then start a new session |
| Gemini CLI | Asks at `gemini extensions install` (the token first, then the URL); the token goes to the system keychain. Change them with `gemini extensions config dominodatalab` |
| Codex and the ChatGPT desktop app | Can't ask. Write the env file below at exactly `~/.config/domino-mcp-server/.env`: Codex starts the server with a stripped environment and passes no other location |
| Cursor | Doesn't ask. Write the env file below. `.cursor-plugin/mcp.json` also forwards `DOMINO_HOST` and `DOMINO_TOKEN` from the environment Cursor runs in, which the Cursor CLI may not share with your shell |
| Antigravity | Doesn't ask. Write the env file below, or start `agy` with `DOMINO_HOST` and `DOMINO_TOKEN` in its environment |
| Any host | The env file below, or `DOMINO_HOST` and `DOMINO_TOKEN` in the environment the host starts the server with |

**The env file** is `~/.config/domino-mcp-server/.env` (or `$XDG_CONFIG_HOME/domino-mcp-server/.env`,
or the file `$DOMINO_MCP_ENV_FILE` names; under Codex only the first, since Codex passes the server
neither variable). This writes it readable only by you, without the token
appearing on screen or in your shell history:

```bash
bash -c 'mkdir -p ~/.config/domino-mcp-server && umask 077 &&
  read -r -p "Domino URL (https://...): " host && read -rs -p "Domino token: " token && echo &&
  printf "DOMINO_HOST=%s\nDOMINO_TOKEN=%s\n" "$host" "$token" > ~/.config/domino-mcp-server/.env'
```

When values come from more than one place, the host's own settings win, then the environment, then
the env file.

**Check it:** start a new session and ask "Which Domino user am I connected as?". The assistant
calls the server's `get_domino_environment_info`, which reports where each value came from and the
user the token belongs to, or exactly what to fix:

| Message | Fix |
|---|---|
| `DOMINO_HOST is not set` or `DOMINO_TOKEN is not set` | The host passed nothing; set the values as the table above shows for your host |
| `HTTP 401` | The token is wrong, expired or revoked; generate a new one |
| `... failed: ...` (no HTTP response) | Check the URL against your browser's address bar, and your network (VPN, or `HTTPS_PROXY` on a corporate network) |
| `uses http://` or `must be a URL starting with https://` | Use the `https://` address |
| `returned a non-JSON response` | The URL points at a login page or another site; copy it from the address bar while you're in Domino |
| `DOMINO_API_KEY is set` | Legacy API keys are not supported; use a Personal Access Token |

## Installation: Claude Code

### Prerequisites

- **Claude Code CLI** v2.1.133 or later (`claude --version` to check). Plugins exist since 2.0.12,
  but the subagents need the `skills:` preload (2.0.43) and plugin skills reachable from a
  subagent through the Skill tool (2.1.133). Tested on 2.1.300.
- Access to a Domino Data Lab instance
- Outside a Domino Workspace: your Domino URL and a Personal Access Token for the bundled MCP
  server. Claude Code asks for both when you enable the plugin ([Your Domino URL and token](#your-domino-url-and-token))
- **`uv`** package manager ([install guide](https://github.com/astral-sh/uv)) — required for the bundled Domino MCP server

### Recommended: install from GitHub

The repository is its own marketplace (`.claude-plugin/marketplace.json`, named
`domino-marketplace`), so Claude Code can install and update the plugin straight from GitHub:

```bash
claude plugin marketplace add dominodatalab/domino-ai-plugin
claude plugin install dominodatalab@domino-marketplace
```

Claude Code installs a copy and replaces it when a release changes the plugin's `version`.
Auto-update is off by default for marketplaces other than Anthropic's: turn it on under
`/plugin` → **Marketplaces**, or set `autoUpdate` in your settings:

```json
{
  "extraKnownMarketplaces": {
    "domino-marketplace": {
      "source": { "source": "github", "repo": "dominodatalab/domino-ai-plugin" },
      "autoUpdate": true
    }
  }
}
```

The marketplace also maps the old entry name `domino-claude-plugin` to `dominodatalab`, so a
setting written for the old name keeps working.

**Already installed from a local marketplace (Options 1 and 3)?** Claude Code won't add a second
source under the same name, `domino-marketplace`. Remove the local one first, including any
`extraKnownMarketplaces` entry you added for it in `.claude/settings.json`, then run the two
commands above:

```bash
claude plugin marketplace remove domino-marketplace
```

Inside a Domino Workspace, leave the image's local marketplace as it is.

### Option 1: Local Marketplace Install (the Domino Workspace layout)

This approach registers the plugin through Claude Code's native marketplace system so it persists across sessions.

**Step 1: Clone the repository and create a marketplace wrapper**

```bash
git clone https://github.com/dominodatalab/domino-ai-plugin.git

mkdir -p ~/.claude/marketplaces/domino/.claude-plugin
mkdir -p ~/.claude/marketplaces/domino/plugins

mv domino-ai-plugin ~/.claude/marketplaces/domino/plugins/domino-claude-plugin
```

**Step 2: Create the marketplace manifest**

```bash
cat > ~/.claude/marketplaces/domino/.claude-plugin/marketplace.json << 'EOF'
{
  "name": "domino-marketplace",
  "owner": {
    "name": "Domino Data Lab",
    "email": "support@dominodatalab.com"
  },
  "plugins": [
    {
      "name": "domino-claude-plugin",
      "description": "Domino Data Lab plugin - workspaces, jobs, environments, datasets, apps, models, and more",
      "source": "./plugins/domino-claude-plugin",
      "category": "development"
    }
  ]
}
EOF
```

> **Why `domino-claude-plugin`?** Claude Code tracks a marketplace install as
> `<entry name>@<marketplace>`, so the entry keeps the name it had before the repo moved.
> Existing installs and Domino workspaces keep updating without a reinstall. Only the clone URL
> changed.

**Step 3: Register the marketplace and install the plugin**

Launch Claude Code and run:

```
/plugin marketplace add /home/<your-username>/.claude/marketplaces/domino
/plugin install domino-claude-plugin@domino-marketplace
```

> **Note:** Replace `<your-username>` with your actual username, or use the full absolute path (e.g., `/home/ubuntu/.claude/marketplaces/domino`). The `~` shorthand may not expand correctly.

**Step 4: Restart Claude Code**, then verify with `/plugin` → **Installed** tab.

### Option 2: Direct Plugin Directory (Development / Quick Start)

```bash
git clone https://github.com/dom