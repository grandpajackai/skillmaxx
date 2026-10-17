# Quarkus Agent MCP

[![MCP Toplist](https://mcptoplist.com/badge/pulsemcp%2Fquarkus-agent-mcp.svg)](https://mcptoplist.com/server/pulsemcp%2Fquarkus-agent-mcp)

<p align="center">
  <img src="logo.png" width="250" alt="Quarkus Agent MCP Logo">
</p>

A standalone MCP server that enables AI coding agents to create, manage, and interact with Quarkus applications. It runs as a separate process that survives app crashes, giving agents the ability to create projects, check for updates, read extension skills, control application lifecycle, proxy Dev MCP tools, and search Quarkus documentation.

Part of the [DevStar](https://github.com/quarkusio/quarkus/discussions/53093) working group.

## Prerequisites

- Java 21+
- Docker or Podman (for documentation search)
- One of: [Quarkus CLI](https://quarkus.io/guides/cli-tooling), [Maven](https://maven.apache.org), or [JBang](https://www.jbang.dev/download/) (for creating new projects)

## Installation

### Claude Code plugin

Add the marketplace and install the plugin:

```bash
claude plugin marketplace add quarkusio/quarkus-agent-mcp
claude plugin install quarkus-agent@quarkus-tools
```

This installs the plugin and configures the MCP server automatically. Requires [JBang](https://www.jbang.dev/download/).

### Via JBang (recommended)

[JBang](https://www.jbang.dev/download/) resolves the uber-jar from Maven Central automatically — no build step needed.

#### Claude Code

```bash
claude mcp add -s user quarkus-agent -- jbang quarkus-agent-mcp@quarkusio
```

#### VS Code / GitHub Copilot

Add to `.vscode/mcp.json` in your workspace:

```json
{
  "servers": {
    "quarkus-agent": {
      "type": "stdio",
      "command": "jbang",
      "args": ["quarkus-agent-mcp@quarkusio"]
    }
  }
}
```

#### IBM Bob

Add to `.bob/mcp.json`:

```json
{
  "mcpServers": {
    "quarkus-agent": {
      "command": "${env:JBANG_HOME}/bin/jbang",
      "args": [
        "quarkus-agent-mcp@quarkusio"
      ],
      "env": {
        "JAVA_HOME": "${env:JAVA_HOME}"
      },
      "disabled": false
    }
  }
}
```

> **Why absolute paths?** Bob inherits system PATH, not your shell PATH. See [Troubleshooting](#jbang-or-java-not-found-enoent) below.

#### Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "quarkus-agent": {
      "command": "jbang",
      "args": ["quarkus-agent-mcp@quarkusio"]
    }
  }
}
```

#### Windsurf

Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "quarkus-agent": {
      "command": "jbang",
      "args": ["quarkus-agent-mcp@quarkusio"]
    }
  }
}
```

#### JetBrains IDEs (IntelliJ IDEA, WebStorm, etc.)

In **Settings → Tools → AI Assistant → MCP Servers** (or the GitHub Copilot MCP settings), add a server with an **absolute path** to `jbang`:

```json
{
  "mcpServers": {
    "quarkus-agent": {
      "type": "stdio",
      "command": "/home/you/.jbang/bin/jbang",
      "args": ["quarkus-agent-mcp@quarkusio"]
    }
  }
}
```

> **Why absolute paths?** JetBrains IDEs launched from the desktop inherit the **system PATH**, not your shell PATH (`~/.bashrc` / `~/.zshrc`). Tools installed via SDKMAN!, JBang's default installer, asdf, or mise are typically on the shell PATH only — so the IDE can't find them. See [Troubleshooting](#jbang-or-java-not-found-enoent) below.

Alternatively, use the direct download method with an absolute path to `java`:

```json
{
  "mcpServers": {
    "quarkus-agent": {
      "type": "stdio",
      "command": "/path/to/java",
      "args": ["-jar", "/path/to/quarkus-agent-mcp-runner.jar"]
    }
  }
}
```

### Via direct download

Download the uber-jar from the [latest GitHub Release](https://github.com/quarkusio/quarkus-agent-mcp/releases/latest), then:

```bash
claude mcp add -s user quarkus-agent -- java -jar /path/to/quarkus-agent-mcp-runner.jar
```

### Native binary (Linux & macOS)

Pre-built native binaries are available on each [GitHub Release](https://github.com/quarkusio/quarkus-agent-mcp/releases/latest). They start instantly and use significantly less memory than the JVM version — ideal for VPS and resource-constrained environments. No JVM or JBang installation required.

> **Note:** Windows is not supported for the native binary. Use the [JBang](#via-jbang-recommended) or [direct download](#via-direct-download) method instead.

#### Quick install (recommended)

Detects your platform, downloads the latest binary to `~/.local/bin/`, and registers it with Claude Code:

```bash
curl -sL https://raw.githubusercontent.com/quarkusio/quarkus-agent-mcp/main/install.sh | bash
```

To update to a newer version, run the same command again.

#### Manual install

##### Linux (x86_64)

```bash
VERSION=$(curl -sI https://github.com/quarkusio/quarkus-agent-mcp/releases/latest | grep -i ^location: | sed 's|.*/||' | tr -d '\r')
mkdir -p ~/.local/bin
curl -L -o ~/.local/bin/quarkus-agent-mcp \
  "https://github.com/quarkusio/quarkus-agent-mcp/releases/download/${VERSION}/quarkus-agent-mcp-${VERSION}-linux-x86_64"
chmod +x ~/.local/bin/quarkus-agent-mcp

claude mcp add -s user quarkus-agent -- ~/.local/bin/quarkus-agent-mcp
```

##### macOS (Apple Silicon)

```bash
VERSION=$(curl -sI https://github.com/quarkusio/quarkus-agent-mcp/releases/latest | grep -i ^location: | sed 's|.*/||' | tr -d '\r')
mkdir -p ~/.local/bin
curl -L -o ~/.local/bin/quarkus-agent-mcp \
  "https://github.com/quarkusio/quarkus-agent-mcp/releases/download/${VERSION}/quarkus-agent-mcp-${VERSION}-macos-aarch64"
chmod +x ~/.local/bin/quarkus-agent-mcp

claude mcp add -s user quarkus-agent -- ~/.local/bin/quarkus-agent-mcp
```

##### macOS (Intel)

```bash
VERSION=$(curl -sI https://github.com/quarkusio/quarkus-agent-mcp/releases/latest | grep -i ^location: | sed 's|.*/||' | tr -d '\r')
mkdir -p ~/.local/bin
curl -L -o ~/.local/bin/quarkus-agent-mcp \
  "https://github.com/quarkusio/quarkus-agent-mcp/releases/download/${VERSION}/quarkus-agent-mcp-${VERSION}-macos-x86_64"
chmod +x ~/.local/bin/quarkus-agent-mcp

claude mcp add -s user quarkus-agent -- ~/.local/bin/quarkus-agent-mcp
```

To update to a newer version, re-run the install script above or repeat these commands.

### Build from source

```bash
git clone https://github.com/quarkusio/quarkus-agent-mcp.git
cd quarkus-agent-mcp
./mvnw package -DskipTests -Dquarkus.package.jar.type=uber-jar
```

This produces the uber-jar at `target/quarkus-agent-mcp-1.0.0-SNAPSHOT-runner.jar` (version may vary).

```bash
claude mcp add -s user quarkus-agent -- java -jar /path/to/quarkus-agent-mcp/target/quarkus-agent-mcp-1.2.11-runner.jar
```

#### Verify

After registering, ask your agent something like:

> "Search the Quarkus docs for how to create a REST endpoint"

If the MCP server is working, the agent will use `quarkus_searchDocs` and return documentation results.

## Usage

### Creating a new Quarkus app

Ask your agent to build a Quarkus application using natural language. The agent uses the MCP tools automatically.

**Example conversation:**

> **You:** Create a Quarkus REST API with a greeting endpoint and a PostgreSQL database
>
> **Agent:** _(uses `quarkus_create` to scaffold the project with `rest-jackson,jdbc-postgresql,hibernate-orm-panache` extensions — the app starts automatically in dev mode and a `CLAUDE.md` is generated with project-specific workflow instructions)_
>
> **Agent:** _(calls `quarkus_skills` to learn the correct patterns for Panache, REST, and other extensions before writing any code)_
>
> **You:** Add a `Greeting` entity and a REST endpoint that stores and retrieves greetings
>
> **Agent:** _(writes the code following patterns from skills, then runs tests using `quarkus_callTool` — via a subagent if supported)_

### Development workflow

The MCP server guides the agent through the optimal Quarkus development workflow:

```
NEW PROJECT                           EXISTING PROJECT

1. quarkus_create                     1. quarkus_start
   → scaffolds + auto-starts             → starts dev mode
   → generates CLAUDE.md
                                      2. quarkus_skills
2. quarkus_skills                        → learn extension patterns
   → learn extension patterns            → query 'quarkus-update' to check version

3. quarkus_searchDocs                 3. quarkus_searchDocs
   → look up APIs, config                → look up APIs, config

4. Write code + tests                 4. Write code + tests

5. Run tests                          5. Run tests
   → quarkus_callTool                    → quarkus_callTool
   → devui-testing_runTests              → devui-testing_runTests

6. Iterate
```

If the app is **already running in your own terminal**, use `quarkus_attach` instead of `quarkus_start` and the rest of the workflow is unchanged.

Attaching requires that the app expose a Dev MCP server. `quarkus_start` passes `-Dquarkus.dev-mcp.enabled=true` itself, so apps it launches always do; an app you started by hand does so only if Dev MCP is enabled for it — commonly `enabled=true` in `~/.quarkus/dev-mcp.properties`, which applies to every project, or `quarkus.dev-mcp.enabled=true` in the project's `application.properties`. `quarkus_attach` calls the server before registering anything and reports what to fix if it gets no answer, rather than attaching to something the proxy tools cannot reach.

Since the process belongs to your terminal, `quarkus_stop` only detaches, and `quarkus_restart` and `quarkus_logs` give way to `devui-logstream_forceRestart` and `devui-logstream_logHistory` through `quarkus_callTool`.

**Key points:**

- **Hot reload** is automatic in Quarkus dev mode — triggered on the next access (HTTP request or test run), not on file save.
- **Skills before code** — the agent reads extension-specific skills to learn correct patterns, testing approaches, and common pitfalls before writing any code.
- **Tests via subagents** — if your agent supports subagents, test execution can be dispatched to one so the main conversation stays responsive.
- **The MCP server survives crashes** — if the app crashes due to a code error, the agent can use `devui-exceptions_getLastException` to get structured exception details (class, message, stack trace, user code location) and fix it. Use `quarkus_logs` for broader context.
- **CLAUDE.md** — every new project gets a `CLAUDE.md` with Quarkus-specific workflow instructions that guide the agent.

### What the agent can do with a running app

Once a Quarkus app is running in dev mode, the agent can discover and use all Dev MCP tools via `quarkus_searchTools` and `quarkus_callTool`. The tool list is **dynamic** — it changes when extensions are added or removed, so the agent should re-discover tools after any extension change. Typical tools include:

| Capability | How to discover | Example |
|-----------|----------------|---------|
| Testing | `quarkus_searchTools` query: `test` | Run all tests, run a specific test class |
| Configuration | `quarkus_searchTools` query: `config` | View and change config properties |
| Extensions | `quarkus_searchTools` query: `extension` | Add or remove extensions at runtime |
| Endpoints | `quarkus_searchTools` query: `endpoint` | List all REST endpoints and their URLs |
| Dev Services | `quarkus_searchTools` query: `dev-services` | View database URLs, container info |
| Log levels | `quarkus_searchTools` query: `log` | Change log levels at runtime |
| Exceptions | `devui-exceptions_getLastException` | Get last compilation/deployment/runtime exception with stack trace and source location |

### Extension skills

The agent can read extension-specific coding skills using `quarkus_skills`. Skills contain patterns, testing guidelines, and common pitfalls for each extension — things like "always use `@Transactional` for write operations with Panache" or "don't create REST clients manually, let CDI inject them."

When called without a query, skills are organized by category (Web, Data, Security, Core, etc.) for easier discovery.

Skills are loaded using a four-layer chai