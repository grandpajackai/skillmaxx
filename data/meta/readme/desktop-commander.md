# Desktop Commander MCP
### Search, update, manage files and run terminal commands with AI

[![npm downloads](https://img.shields.io/npm/dw/@wonderwhy-er/desktop-commander)](https://www.npmjs.com/package/@wonderwhy-er/desktop-commander)
[![AgentAudit Verified](https://agentaudit.dev/api/badge/desktop-commander)](https://agentaudit.dev/skills/desktop-commander)
[![Trust Score](https://archestra.ai/mcp-catalog/api/badge/quality/wonderwhy-er/DesktopCommanderMCP)](https://archestra.ai/mcp-catalog/wonderwhy-er__desktopcommandermcp)
[![smithery badge](https://smithery.ai/badge/@wonderwhy-er/desktop-commander)](https://smithery.ai/server/@wonderwhy-er/desktop-commander)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support-yellow.svg)](https://www.buymeacoffee.com/wonderwhyer)


[![Discord](https://img.shields.io/badge/Join%20Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/kQ27sNnZr7)


Work with code and text, run processes, and automate tasks, going far beyond other AI editors - while using host client subscriptions instead of API token costs.

<a href="https://glama.ai/mcp/servers/zempur9oh4">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/zempur9oh4/badge" alt="Desktop Commander MCP" />
</a>

## Table of Contents
- [Features](#features)
- [How to install](#how-to-install)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [File Preview UI & Markdown Editor](#file-preview-ui--markdown-editor)
- [Handling Long-Running Commands](#handling-long-running-commands)
- [Work in Progress and TODOs](#roadmap)
- [Sponsors and Supporters](#support-desktop-commander)
- [Website](#website)
- [Media](#media)
- [Testimonials](#testimonials)
- [Frequently Asked Questions](#frequently-asked-questions)
- [Contributing](#contributing)
- [License](#license)

All of your AI development tools in one place.
Desktop Commander puts all dev tools in one chat.
Execute long-running terminal commands on your computer and manage processes through Model Context Protocol (MCP). Built on top of [MCP Filesystem Server](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) to provide additional search and replace file editing capabilities.

## Features

- **Remote AI Control** - Use Desktop Commander from ChatGPT, Claude web, and other AI services via [Remote MCP](https://mcp.desktopcommander.app)
- **File Preview UI** - Visual file previews in Claude Desktop with rendered markdown, inline images, expandable content, built-in markdown editor, and quick "Open in folder" access
- **Enhanced terminal commands with interactive process control**
- **Execute code in memory (Python, Node.js, R) without saving files**
- **Instant data analysis - just ask to analyze CSV/JSON/Excel files**
- **Native Excel file support** - Read, write, edit, and search Excel files (.xlsx, .xls, .xlsm) without external tools
- **PDF support** - Read PDFs with text extraction, create new PDFs from markdown, modify existing PDFs
- **DOCX support** - Read, create, edit, and search Word documents (.docx) with surgical XML editing and markdown-to-DOCX conversion
- **Interact with running processes (SSH, databases, development servers)**
- Execute terminal commands with output streaming
- Command timeout and background execution support
- Process management (list and kill processes)
- Session management for long-running commands
- **Process output pagination** - Read terminal output with offset/length controls to prevent context overflow
- Server configuration management:
  - Get/set configuration values
  - Update multiple settings at once
  - Dynamic configuration changes without server restart
- Full filesystem operations:
  - Read/write files (text, Excel, PDF, DOCX)
  - Create/list directories
  - **Recursive directory listing** with configurable depth and context overflow protection for large folders
  - Move files/directories
  - Search files and content (including Excel content)
  - Get file metadata
  - **Negative offset file reading**: Read from end of files using negative offset values (like Unix tail)
- Code editing capabilities:
  - Surgical text replacements for small changes
  - Full file rewrites for major changes
  - Multiple file support
  - Pattern-based replacements
  - vscode-ripgrep based recursive code or text search in folders
- Local tool-call history and audit logs:
  - Tool calls and arguments are recorded locally on the machine running Desktop Commander
  - Recent call history with bounded output previews is available through `get_recent_tool_calls`
  - Size-based rotation/trimming keeps the active history files bounded
- Safety guardrails (not a sandbox — see [SECURITY.md](SECURITY.md)):
  - Symlink traversal prevention on file operations
  - Command blocklist for accidental execution
  - [Docker isolation](#option-6-docker-installation--auto-updates-no-nodejs-required) for complete isolation

## How to install

### Install in Claude Desktop

Desktop Commander offers multiple installation methods for Claude Desktop.

> **📋 Update & Uninstall Information:** Options 1, 2, 3, 4, and 6 have automatic updates. Option 5 requires manual updates. See below for details.

<details>
<summary><b>Option 1: Install through npx ⭐ Auto-Updates (Requires Node.js)</b></summary>

Just run this in terminal:
```
npx @wonderwhy-er/desktop-commander@latest setup
```

For debugging mode (allows Node.js inspector connection):
```
npx @wonderwhy-er/desktop-commander@latest setup --debug
```

**Command line options during setup:**
- `--debug`: Enable debugging mode for Node.js inspector
- `--no-onboarding`: Disable onboarding prompts for new users

Restart Claude if running.

**✅ Auto-Updates:** Yes - automatically updates when you restart Claude  
**🔄 Manual Update:** Run the setup command again  
**🗑️ Uninstall:** Run `npx @wonderwhy-er/desktop-commander@latest remove`

</details>

<details>
<summary><b>Option 2: Using bash script installer (macOS) ⭐ Auto-Updates (Installs Node.js if needed)</b></summary>

```
curl -fsSL https://raw.githubusercontent.com/wonderwhy-er/DesktopCommanderMCP/refs/heads/main/install.sh | bash
```
This script handles all dependencies and configuration automatically.

**✅ Auto-Updates:** Yes  
**🔄 Manual Update:** Re-run the bash installer command above  
**🗑️ Uninstall:** Run `npx @wonderwhy-er/desktop-commander@latest remove`

</details>

<details>
<summary><b>Option 3: Installing via Smithery ⭐ Auto-Updates (Requires Node.js)</b></summary>

1. **Visit:** https://smithery.ai/server/@wonderwhy-er/desktop-commander
2. **Login to Smithery** if you haven't already
3. **Select your client** (Claude Desktop) on the right side
4. **Install with the provided key** that appears after selecting your client
5. **Restart Claude Desktop**

**✅ Auto-Updates:** Yes - automatically updates when you restart Claude  
**🔄 Manual Update:** Visit the Smithery page and reinstall  

</details>

<details>
<summary><b>Option 4: Add to claude_desktop_config manually ⭐ Auto-Updates (Requires Node.js)</b></summary>

Add this entry to your claude_desktop_config.json:

- On Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
- On Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- On Linux: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "desktop-commander": {
      "command": "npx",
      "args": [
        "-y",
        "@wonderwhy-er/desktop-commander@latest"
      ]
    }
  }
}
```
Restart Claude if running.

**✅ Auto-Updates:** Yes - automatically updates when you restart Claude  
**🔄 Manual Update:** Run the setup command again  
**🗑️ Uninstall:** Run `npx @wonderwhy-er/desktop-commander@latest remove` or remove the entry from your claude_desktop_config.json

</details>

<details>
<summary><b>Option 5: Checkout locally ❌ Manual Updates (Requires Node.js)</b></summary>

```bash
git clone https://github.com/wonderwhy-er/DesktopCommanderMCP.git
cd DesktopCommanderMCP
npm run setup
```
Restart Claude if running.

The setup command will install dependencies, build the server, and configure Claude's desktop app.

**❌ Auto-Updates:** No - requires manual git updates  
**🔄 Manual Update:** `cd DesktopCommanderMCP && git pull && npm run setup`  
**🗑️ Uninstall:** Run `npx @wonderwhy-er/desktop-commander@latest remove` or remove the cloned directory and MCP server entry from Claude config

</details>

<details>
<summary><b>Option 6: Docker Installation 🐳 ⭐ Auto-Updates (No Node.js Required)</b></summary>

Perfect for users who want isolation or don't have Node.js installed. Runs in a sandboxed Docker container with a persistent work environment.

**Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed **and running**, Claude Desktop app installed.

**macOS/Linux:**
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/wonderwhy-er/DesktopCommanderMCP/refs/heads/main/install-docker.sh)
```

**Windows PowerShell:**
```powershell
iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/wonderwhy-er/DesktopCommanderMCP/refs/heads/main/install-docker.ps1'))
```

The installer will check Docker, pull the image, prompt for folder mounting, and configure Claude Desktop.

**Docker persistence:** Your tools, configs, work files, and package caches all survive restarts.

<details>
<summary>Manual Docker Configuration</summary>

**Basic setup (no file access):**
```json
{
  "mcpServers": {
    "desktop-commander-in-docker": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp/desktop-commander:latest"]
    }
  }
}
```

**With folder mounting:**
```json
{
  "mcpServers": {
    "desktop-commander-in-docker": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "/Users/username/Desktop:/mnt/desktop",
        "-v", "/Users/username/Documents:/mnt/documents",
        "mcp/desktop-commander:latest"
      ]
    }
  }
}
```

**Advanced folder mounting:**
```json
{
  "mcpServers": {
    "desktop-commander-in-docker": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-v", "dc-system:/usr",
        "-v", "dc-home:/root", 
        "-v", "dc-workspace:/workspace",
        "-v", "dc-packages:/var",
        "-v", "/Users/username/Projects:/mnt/Projects",
        "-v", "/Users/username/Downloads:/mnt/Downloads",
        "mcp/desktop-commander:latest"
      ]
    }
  }
}
```

</details>

<details>
<summary>Docker Management Commands</summary>

**macOS/Linux:**
```bash
# Check status
bash <(curl -fsSL https://raw.githubusercontent.com/wonderwhy-er/DesktopCommanderMCP/refs/heads/main/install-docker.sh) --status

# Reset all persistent data
bash <(curl -fsSL https://raw.githubusercontent.com/wonderwhy-er/DesktopCommanderMCP/refs/heads/main/install-docker.sh) --reset
```

**Windows PowerShell:**
```powershell
# Check status
$script = (New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/wonderwhy-er/DesktopCommanderMCP/refs/heads/main/install-docker.ps1'); & ([ScriptBlock]::Create("$script")) -Status

# Reset all data
$script = (New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/wonderwhy-er/DesktopCommanderMCP/refs/heads/main/install-docker.ps1'); & ([ScriptBlock]::Create("$script")) -Reset

# Show help
$script = (New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/wonderwhy-er/DesktopCommanderMCP/refs/heads/main/install-docker.ps1'); & ([ScriptBlock]::Create("$script")) -Help
```

**Troubleshooting:** Reset and reinstall from scratch:
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/wonderwhy-er/DesktopCommanderMCP/refs/heads/main/install-docker.sh) --reset && bash <(curl -fsSL https://raw.githubusercontent.com/wonderwhy-er/DesktopCommanderMCP/refs/heads/main/install-docker.sh)
```

</details>

**✅ Auto-Updates:** Yes - `latest` tag automatically gets new