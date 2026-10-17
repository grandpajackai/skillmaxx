# Apollo.io MCP Server

> The official Apollo.io Model Context Protocol server for prospecting, lead enrichment, sales intelligence, and outreach workflows.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![MCP Registry](https://img.shields.io/badge/MCP%20Registry-io.github.apolloio%2Fapollo--mcp-6E56CF.svg)](https://registry.modelcontextprotocol.io/)
[![Version](https://img.shields.io/badge/version-0.1.1-informational.svg)](server.json)

**Provider:** Official, first-party server built and maintained by [Apollo.io](https://www.apollo.io/).

Bring Apollo.io prospecting, enrichment, and outreach directly into your favorite MCP-compatible AI application — GitHub Copilot, Visual Studio Code, Cursor, Claude Code, Claude Desktop, and Claude Cowork.

- **Apollo.io:** <https://www.apollo.io/>
- **Model Context Protocol:** <https://modelcontextprotocol.io/>
- **License:** [MIT](LICENSE)

---

## Table of Contents

- [Overview](#overview)
- [Key Capabilities](#key-capabilities)
- [Prerequisites](#prerequisites)
- [Install in Visual Studio Code and GitHub Copilot](#install-in-visual-studio-code-and-github-copilot)
- [Install in Cursor](#install-in-cursor)
- [Install in Claude Code](#install-in-claude-code)
- [Install in Claude Desktop or Claude Cowork](#install-in-claude-desktop-or-claude-cowork)
- [Generic MCP Client Configuration](#generic-mcp-client-configuration)
- [Authentication and Authorization](#authentication-and-authorization)
- [Usage Examples](#usage-examples)
- [Available Tools and Capabilities](#available-tools-and-capabilities)
- [Model Recommendations](#model-recommendations)
- [Safety and Responsible Usage](#safety-and-responsible-usage)
- [Privacy and Data Handling](#privacy-and-data-handling)
- [Troubleshooting](#troubleshooting)
- [Official MCP Registry](#official-mcp-registry)
- [Development and Contribution](#development-and-contribution)
- [Versioning and Releases](#versioning-and-releases)
- [Security](#security)
- [Support](#support)
- [Credits](#credits)
- [License](#license)

---

## Overview

The Apollo.io MCP server exposes Apollo.io's go-to-market data and workflows through the [Model Context Protocol](https://modelcontextprotocol.io/), so MCP-compatible AI applications can prospect for people and companies, enrich contacts, query sales analytics, and load leads into outreach sequences using natural language.

- **Hosted and maintained by Apollo.io.** The server runs remotely — there is nothing to build, host, or run locally.
- **Transport:** Streamable HTTP.
- **Endpoint:**

  ```text
  https://mcp.apollo.io/mcp
  ```

- **Authentication:** Handled through Apollo.io OAuth. You sign in with your Apollo.io account and authorize access from your MCP client; the server then acts with your Apollo.io permissions. See [Authentication and Authorization](#authentication-and-authorization).

This repository also ships an optional Apollo plugin for Claude Code and Cowork that bundles ready-made workflow skills (`/apollo:*` commands) on top of the same MCP server.

---

## Key Capabilities

The following capabilities are confirmed by the server tools and skills in this repository:

- **People prospecting** — search Apollo's people database by title, seniority, location, and company attributes.
- **Company prospecting** — search organizations by industry, size, location, and keywords.
- **Contact and account enrichment** — match and enrich people and organizations, individually or in bulk.
- **Outreach sequence workflows** — find sequences, and add or remove/stop contacts in a sequence.
- **Sales analytics** — query email, call, meeting, task, opportunity, sequence, and conversation-intelligence metrics and return formatted breakdowns.
- **Contact management** — create Apollo contacts as part of enrichment and sequence-loading workflows.

> The remote server may expose additional tools beyond those exercised by the bundled skills. The list above reflects what is confirmed in this repository. See [Available Tools and Capabilities](#available-tools-and-capabilities).

---

## Prerequisites

- **An Apollo.io account.** Sign in at <https://www.apollo.io/>.
- **Apollo.io permissions and credits.** Actions run with your account's permissions, and some actions consume Apollo credits (for example, enrichment). See [Safety and Responsible Usage](#safety-and-responsible-usage). For plan, credit, and permission details, see the [Apollo documentation](https://docs.apollo.io).

- **An MCP-compatible client** that supports the Streamable HTTP transport, such as:
  - GitHub Copilot in Visual Studio Code
  - Cursor
  - Claude Code
  - Claude Desktop / Claude Cowork
  - Other MCP clients (see [Generic MCP Client Configuration](#generic-mcp-client-configuration))
- **No local runtime required.** The server is remote and hosted by Apollo.io — you do **not** need Node.js, Docker, or a local installation to use it. (The optional Claude Code / Cowork plugin installs workflow skills locally through your client's plugin system, but the MCP server itself remains remote.)

---

## Install in Visual Studio Code and GitHub Copilot

The Apollo.io MCP server is published in the official Model Context Protocol Registry, but it is **not yet discoverable in the curated GitHub MCP Registry or the VS Code MCP gallery**. Until then, add it manually with the configuration below.

### Option A — workspace configuration file

Create a `.vscode/mcp.json` file in your workspace:

```json
{
  "servers": {
    "apollo": {
      "type": "http",
      "url": "https://mcp.apollo.io/mcp"
    }
  }
}
```

### Option B — command palette

1. Open the Command Palette (`Cmd/Ctrl + Shift + P`).
2. Run **MCP: Add Server**.
3. Choose the HTTP (Streamable HTTP) server type when prompted.
4. Enter the URL `https://mcp.apollo.io/mcp` and name the server `apollo`.

### Expected authentication and first run

1. Add the MCP server using either option above.
2. Start or enable the `apollo` server.
3. Complete Apollo.io authentication in the browser window that opens.
4. Approve the requested access for your Apollo.io workspace.
5. Open Copilot Chat in **Agent** mode.
6. Confirm that the Apollo tools are listed and available to the agent.

> For the current terminology and behavior, see the VS Code documentation on MCP servers: <https://code.visualstudio.com/docs/copilot/chat/mcp-servers>.

---

## Install in Cursor

Add the remote Streamable HTTP endpoint to your Cursor MCP configuration (for example, `~/.cursor/mcp.json`, or the project-level `.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "apollo": {
      "type": "http",
      "url": "https://mcp.apollo.io/mcp"
    }
  }
}
```

Then:

1. Open Cursor settings and confirm the `apollo` server is listed under MCP.
2. Authenticate with your Apollo.io account when prompted.
3. Approve the requested access, then use Apollo tools from the agent.

> This repository also includes a Cursor plugin manifest (`.cursor-plugin/plugin.json`) that references the same remote endpoint (`.mcp.json`), so no local package needs to run.

---

## Install in Claude Code

You can connect the server in either of two ways.

### Option A — add the remote MCP server directly

```bash
claude mcp add --transport http apollo https://mcp.apollo.io/mcp
```

Then run `/mcp` inside Claude Code, select **apollo**, and authenticate.

### Option B — install the Apollo plugin (adds `/apollo:*` workflow skills)

1. Add this plugin's marketplace:

   ```text
   /plugin marketplace add apolloio/apollo-mcp-plugin
   ```

2. Install the plugin:

   ```text
   /plugin install apollo@apollo-plugin-marketplace
   ```

3. Restart Claude Code so the MCP server starts correctly.

The plugin automatically configures the Apollo MCP server — no manual config files. After installing, authenticate with `/mcp` and run `/apollo:*` commands (see [Available Tools and Capabilities](#available-tools-and-capabilities)).

---

## Install in Claude Desktop or Claude Cowork

Claude Desktop and Claude Cowork are separate from Claude Code (the CLI). Use the steps below for the desktop-based clients.

### Cowork (one-click)

Click to install in a single step:

**[Install in Cowork](https://claude.ai/desktop/customize/plugins/new?marketplace=apolloio/apollo-mcp-plugin&plugin=apollo)**

Then restart Cowork so the MCP server starts correctly.

### Claude Desktop

Add the Apollo connector from your Claude settings, then authenticate:

1. Open **Settings** and connect the Apollo.io connector (Apollo appears as a remote MCP server).
2. Complete Apollo.io authentication in your browser.
3. Approve the requested access.
4. Confirm Apollo tools are available in a new chat.

> Exact menu labels and navigation vary by Claude Desktop version. See Anthropic's documentation for the current steps to add a remote MCP connector.

---

## Generic MCP Client Configuration

For any other MCP-compatible client that supports Streamable HTTP:

```json
{
  "name": "apollo",
  "type": "streamable-http",
  "url": "https://mcp.apollo.io/mcp"
}
```

> Exact property names vary between clients. Some clients use `type: "http"` (as in the VS Code and Cursor examples above) and some use `type: "streamable-http"`. Consult your client's MCP documentation for the precise schema.

---

## Authentication and Authorization

The Apollo MCP server uses **Apollo.io OAuth**. Only confirmed behavior is documented here.

- **Sign-in flow.** When you connect the server, your client opens an Apollo.io sign-in and authorization window. After you approve access, your client can call Apollo tools on your behalf.
- **Workspace and permissions.** The server acts with the authenticated user's Apollo.io permissions. You can only access data and perform actions your Apollo.io account is allowed to.
- **Reconnecting.** In Claude Code you can re-run `/mcp`, select **apollo**, and re-authenticate. In other clients, re-trigger authentication from the client's MCP or connector settings.
- **Revoking access.** Remove or disconnect the `apollo` server from your MCP client to stop it from acting on your behalf. To manage authorizations at the account level, use your Apollo.io account settings.

> OAuth authorization-server metadata is discoverable at `https://mcp.apollo.io/.well-known/oauth-authorization-server`. Beyond that, this README does not assert a specific OAuth specification or profile.

---

## Usage Examples

Natural-language prompts you can try once the server is connected:

```text
Find software engineering leaders at B2B SaaS companies in Germany with 200–1,000 employees.
```

```text
Enrich these business contacts and return their current title, company, and verified business email when available.
```

```text
Show email and call performance by rep for this quarter, sorted by calls made.
```

```text
Add the selected contacts to my Apollo sequence "Q1 Enterprise Outbound" — show a preview before enrolling.
```

If you installed the Claude Code / Cowork plugin, the same workflows are available as slash commands:

- `/apollo:prospect VP of Engineering at Series B+ SaaS companies in the US, 200-1000 employees`
- `/apollo:enrich-lead https://www.linkedin.com/in/example`
- `/apollo:sequence-load add 20 VP Sales at SaaS companies to my "Q1 Outbound" sequence`
- `/apollo:analytics Show me team call connect rate this quarter by rep`

> **Review before you act.** For consequential actions — enrichment (credit-consuming) and adding contacts to a sequence (potentially outbound) — review the exact targets and parameters before confirming the operation.

---

## Available Tools and Capabilities

The remote server provides the underlying Apollo tools; the tools listed below are those **confirmed in this repository** through the bundled workflow skills. The full, authoritative tool set is provided by the remote server and may evolve independently of this document.

### Workflow skills (Claude Code / Cowork plugin)

High-value skills that chain multiple Apollo to