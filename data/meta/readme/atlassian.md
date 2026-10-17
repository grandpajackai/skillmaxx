<p align="center">
  <img src="images/atlassian_logo_brand_RGB.svg" alt="Atlassian" width="320">
</p>

<h1 align="center">Atlassian MCP Server</h1>

<p align="center">
  <b>The official Model Context Protocol (MCP) server for Atlassian: a cloud-hosted bridge that gives your AI tools secure, real-time access to Jira, Confluence, Jira Service Management, Bitbucket, Compass, Loom, and the wider Atlassian platform — powered by your Teamwork Graph.</b>
</p>

<!-- Line 1 · Project -->
<p align="center">
  <a href="https://github.com/atlassian/atlassian-mcp-server"><img src="https://img.shields.io/badge/Official-Atlassian-0052CC?logo=atlassian&logoColor=white" alt="Official Atlassian Server"></a>
  <a href="https://github.com/atlassian/atlassian-mcp-server/stargazers"><img src="https://img.shields.io/github/stars/atlassian/atlassian-mcp-server?style=flat&logo=github&label=Stars&color=0052CC" alt="GitHub stars"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/atlassian/atlassian-mcp-server?label=License&color=0052CC" alt="License: Apache 2.0"></a>
  <a href="https://www.atlassian.com/blog/announcements/remote-mcp-server"><img src="https://img.shields.io/badge/Status-Generally_Available-2EBC4F" alt="Status: Generally Available"></a>
</p>

<!-- Line 2 · Protocol & access -->
<p align="center">
  <a href="https://modelcontextprotocol.io"><img src="https://img.shields.io/badge/Model_Context_Protocol-compatible-000000?logo=modelcontextprotocol&logoColor=white" alt="Model Context Protocol compatible"></a>
  <a href="server.json"><img src="https://img.shields.io/badge/MCP_Registry-com.atlassian-000000?logo=modelcontextprotocol&logoColor=white" alt="MCP Registry: com.atlassian"></a>
  <a href="https://support.atlassian.com/security-and-access-policies/docs/understand-atlassian-rovo-mcp-server/"><img src="https://img.shields.io/badge/Auth-OAuth_2.1%20%7C%20API%20token-2EBC4F" alt="Auth: OAuth 2.1 or API token"></a>
  <a href="https://www.atlassian.com/cloud"><img src="https://img.shields.io/badge/Hosting-Atlassian_Cloud-0052CC?logo=atlassian&logoColor=white" alt="Hosting: Atlassian Cloud"></a>
</p>

<!-- Line 3 · Supported products. Two-tone shields: dark logo segment on the left (labelColor), brand-colored product name on the right. Jira Service Management, Compass & Rovo have no simple-icons slug, so they use the official @atlaskit/logo (v20) tile glyphs embedded as SVG data URIs. -->
<p align="center">
  <a href="https://www.atlassian.com/software/jira"><img src="https://img.shields.io/badge/Jira-0052CC?logo=jira&logoColor=white&labelColor=172B4D" alt="Jira"></a>
  <a href="https://www.atlassian.com/software/confluence"><img src="https://img.shields.io/badge/Confluence-0052CC?logo=confluence&logoColor=white&labelColor=172B4D" alt="Confluence"></a>
  <a href="https://www.atlassian.com/software/jira/service-management"><img src="https://img.shields.io/badge/Jira_Service_Management-0052CC?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iI2ZmZmZmZiI+PHBhdGggZD0iTTEyIDBhMTIgMTIgMCAxIDAgMCAyNEExMiAxMiAwIDAgMCAxMiAwem0wIDMuNmE1LjA0IDUuMDQgMCAwIDEgNS4wNCA1LjA0IDUuMDQgNS4wNCAwIDAgMS01LjA0IDUuMDQgNS4wNCA1LjA0IDAgMCAxLTUuMDQtNS4wNEE1LjA0IDUuMDQgMCAwIDEgMTIgMy42em0wIDE2LjhhOC4wNCA4LjA0IDAgMCAxLTUuOTQtMi42MmMuMDMtMS45OCA0LjAyLTMuMDYgNS45NC0zLjA2czUuOTEgMS4wOCA1Ljk0IDMuMDZBOC4wNCA4LjA0IDAgMCAxIDEyIDIwLjR6Ii8+PC9zdmc+&logoColor=white&labelColor=172B4D" alt="Jira Service Management"></a>
  <a href="https://www.atlassian.com/software/bitbucket"><img src="https://img.shields.io/badge/Bitbucket-0052CC?logo=bitbucket&logoColor=white&labelColor=172B4D" alt="Bitbucket"></a>
  <a href="https://www.loom.com/"><img src="https://img.shields.io/badge/Loom-625DF5?logo=loom&logoColor=white&labelColor=172B4D" alt="Loom"></a>
  <a href="https://www.atlassian.com/software/compass"><img src="https://img.shields.io/badge/Compass-94C748?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzk0Yzc0OCIgZD0iTTAgNmE2IDYgMCAwIDEgNi02aDEyYTYgNiAwIDAgMSA2IDZ2MTJhNiA2IDAgMCAxLTYgNkg2YTYgNiAwIDAgMS02LTZ6Ii8+PHBhdGggZmlsbD0iIzEwMTIxNCIgZD0iTTEyLjc1IDcuODc3di0zLjM3bDYuMTYtLjAwN2guMDA3YS41OS41OSAwIDAgMSAuNTgzLjU5OHY2LjE0N2gtMy4zNjZWNy44Nzd6Ii8+PHBhdGggZmlsbD0iIzEwMTIxNCIgZD0iTTEyLjc1IDE0LjYxNXYtMy4zN2gzLjM2OHY2LjE2NWEuNTkuNTkgMCAwIDEtLjU5MS41OUg2LjU4M0EuNTkuNTkgMCAwIDEgNiAxNy40MDJWOC40NjdhLjU5LjU5IDAgMCAxIC41OTEtLjU5aDYuMTZ2My4zNjhIOS4zNzN2My4zN3oiLz48L3N2Zz4=&labelColor=101214" alt="Compass"></a>
  <a href="https://www.atlassian.com/software/rovo"><img src="https://img.shields.io/badge/Rovo-1868DB?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iIzE4NjhkYiIgZD0iTTAgNmE2IDYgMCAwIDEgNi02aDEyYTYgNiAwIDAgMSA2IDZ2MTJhNiA2IDAgMCAxLTYgNkg2YTYgNiAwIDAgMS02LTZ6Ii8+PHBhdGggZmlsbD0iI2ZmZmZmZiIgZD0iTTExLjA1NyA1LjI1N2ExLjU3IDEuNTcgMCAwIDEgMS41MzkuMDE1bDQuNjIxIDIuNjY4Yy40ODQuMjc5Ljc4My43OTcuNzgzIDEuMzU0djUuMzM2YTEuNTYgMS41NiAwIDAgMS0uNzgyIDEuMzU1bC0zLjQ3NCAyLjAwNWEyIDIgMCAwIDAgLjEyLS42OTF2LTUuMzM3YzAtLjczMy0uMzktMS40MDktMS4wMjYtMS43NzRsLTIuNTktMS40OTVWNi42MjZxLjAwMS0uMjQ2LjA3NC0uNDczYy4xMTctLjM2NC4zNjYtLjY4LjcwNy0uODc3eiIvPjxwYXRoIGZpbGw9IiNmZmZmZmYiIGQ9Ik05Ljg4MSA1Ljk0IDYuNDA4IDcuOTQ1QTEuNTYgMS41NiAwIDAgMCA1LjYyNSA5LjN2NS4zMzdjMCAuNTU3LjMgMS4wNzUuNzgzIDEuMzU0bDQuNjIxIDIuNjY4Yy40NzUuMjc0IDEuMDYuMjc5IDEuNTM5LjAxNWwuMDI3LS4wMTlhMS41NyAxLjU3IDAgMCAwIC43ODEtMS4zNXYtMi4wNjdsLTIuNTg5LTEuNDk1YTIuMDUgMi4wNSAwIDAgMS0xLjAyNi0xLjc3NVY2LjYzMWEyIDIgMCAwIDEgLjEyLS42OTEiLz48L3N2Zz4=&amp;logoColor=white&labelColor=101214" alt="Rovo"></a>
</p>

<p align="center">
  <a href="https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/"><b>Getting started</b></a> ·
  <a href="https://support.atlassian.com/atlassian-rovo-mcp-server/docs/supported-tools/"><b>Supported tools</b></a> ·
  <a href="https://support.atlassian.com/security-and-access-policies/docs/understand-atlassian-rovo-mcp-server/"><b>Security &amp; admin</b></a> ·
  <a href="https://community.atlassian.com/"><b>Community</b></a>
</p>

---

The **official Atlassian MCP Server** is a cloud-based bridge between your Atlassian Cloud site and compatible external tools. Once configured, it enables those tools to interact with **Jira, Confluence, Jira Service Management, Bitbucket, Compass, Loom, and Atlassian platform data (Projects, Goals, Teams, Focus, Talent, and the Teamwork Graph)** in real time. Authentication uses **OAuth 2.1** or **API tokens**, so every action respects the user's existing access controls.

With the Atlassian MCP Server, you can:

* **Summarize and search** Jira, Jira Service Management, Confluence, Bitbucket, Projects, Goals, and more without switching tools.
* **Retrieve and review** recordings of videos and meetings from Loom.
* **Create and update** work items or pages based on natural language commands.
* **Automate repetitive work**, like generating work items from meeting notes or specs.

Connect once, then describe what you want — no tab switching and no copy-pasting. Your AI selects and runs the right actions.

It's built for developers, content creators, and project teams who work in IDEs or AI tools and want to use Atlassian data without constantly switching context.

> [!IMPORTANT]
> **v2 is now the recommended version.** New setups should use `https://mcp.atlassian.com/v2/mcp`, which exposes more tools and more products. Existing v1 connections automatically start to expose and use v2 tools; incompatible clients may need to clear cached client IDs or `.well-known` credentials to keep authenticating. For setup steps, see [Getting started with the Atlassian MCP Server](https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/).

## One-click setup

Pick your AI client below to install the official Atlassian MCP Server. Each button uses your client's native install link, so you don't need to edit any JSON config by hand.

<table align="center">
  <tr>
    <td align="center" width="180">
      <a href="https://cursor.com/en/install-mcp?name=Atlassian-Rovo-MCP&config=eyJ1cmwiOiJodHRwczovL21jcC5hdGxhc3NpYW4uY29tL3YyL21jcCJ9">
        <img src="https://img.shields.io/badge/Cursor-000000?style=for-the-badge&logo=cursor&logoColor=white" alt="Add to Cursor"><br>
        <b>Add to Cursor</b>
      </a>
      <br><sub>Reference issues and log work in your codebase.</sub>
    </td>
    <td align="center" width="180">
      <a href="https://vscode.dev/redirect/mcp/install?name=Atlassian-Rovo-MCP&config=%7B%22url%22%3A%22https%3A%2F%2Fmcp.atlassian.com%2Fv2%2Fmcp%22%2C%22type%22%3A%22http%22%7D">
        <img src="https://img.shields.io/badge/VS_Code-0098FF?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iI2ZmZmZmZiI+PHBhdGggZD0iTTE3LjUgMiA5LjIgOS42IDQuNiA2LjEgMyA2Ljl2MTAuMmwxLjYuOCA0LjYtMy41IDguMyA3LjZMMjEgMjFWM3pNNi40IDEybDIuOS0yLjJ2NC40em0xMS4xIDQuOS01LjQtNC45IDUuNC00Ljl6Ii8+PC9zdmc+&logoColor=white" alt="Add to VS Code"><br>
        <b>Add to VS Code</b>
      </a>
      <br><sub>Search and create Jira issues via GitHub Copilot.</sub>
    </td>
    <td align="center" width="180">
      <a href="https://chatgpt.com/apps/atlassian-rovo/connector_692de805e3ec8191834719067174a384">
        <img src="https://img.shields.io/badge/ChatGPT-10A37F?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0iI2ZmZmZmZiI+PHBhdGggZD0iTTEyIDIgMyA3djEwbDkgNSA5LTVWN3ptMCAyLjMgNi41IDMuNkwxMiAxMS41IDUuNSA3Ljl6TTUgOS42bDYgMy4zdjYuOGwtNi0zLjN6bTE0IDB2Ni44bC02IDMuM3YtNi44eiIvPjwvc3ZnPg==&logoColor=white" alt="Add to ChatGPT"><br>
        <b>Add to ChatGPT</b>
      </a>
      <br><sub>Search, summarize, and create right from ChatGPT.</sub>
    </td>
    <td align="center" width="180">
      <a href="https://claude.ai/directory/connectors/atlassian">
        <img src="https://img.shields.io/badge/Claude-D97757?style=for-the-badge&logo=claude&logoColor=white" alt="Add to Claude"><br>
        <b>Add to Claude</b>
      </a>
      <br><sub>Bring Jira and Confluence into Claude workflows.</sub>
    </td>
  </tr>
</table>

### Let your agent do the setup

Most AI coding agents can install, authenticate, and configure the server themselves. Copy and paste this prompt into your agent:

```
Set up Atlassian MCP for this agent using the official setup guide at
https://support.atlassian.com/atlassian-rovo-mcp-server/docs/getting-started-with-the-atlassian-remote-mcp-server/
and the MCP server URL https://mcp.atlassian.com/v2/mcp. Then start the Atlassian MCP
authentication flow so I can sign in.
```

Or add the server manually with your client's own command:

| Client | Command or configuration |
| --- | --- |
| Claude Code | `claude mcp add --transport http atlassian https://mcp.atlassian.com/v2/mcp`, then run `/mcp` in a session to authenticate |
| Codex | `codex mcp add atlassian --url https://mcp.atlassian.com/v2/mcp` |
| Claude Desktop | **Settings → Extensions → Browse extensions → Plugins**, then search for **Atlassian** |
| Codex Desktop | **Plugins** or **Connectors**, then install **Atlassian Rovo** |
| VS Code / GitHub Copilot | Extensions view → search `@mcp Atlassian` → **Install** |
| Cursor | [Atlassian plugin for Cursor with MCP](https://cursor.com/marketplace/atlassian) → **Add to Cursor** |
| Windsurf | **Cascade → MCP servers → Add Server → Add custom server**, with `serverUrl` set to `https://mcp.atlassian.com/v2/mcp` |
| Any other MCP client | Use the server URL `https://mcp.atlassian.com/v2/mcp` |

## Contents

* [One-click setup](#one-click-setup)
* [Supported clients](#supported-clients)
* [Plugin packaging and compatibility](#plugin-packaging-and-compatibility)
* [Supp