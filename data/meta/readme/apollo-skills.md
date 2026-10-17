# Apollo GraphQL Agent Skills

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-11-green.svg)](#skills)

A collection of skills for AI coding agents working with Apollo GraphQL tools and technologies.

Apollo Skills follow the [Agent Skills](https://agentskills.io/) format and are available on [skills.sh](https://skills.sh/).

## Installation

Install skills using the [Skills CLI](https://skills.sh/docs/cli):

```bash
npx skills add apollographql/skills
```

The CLI guides you through an interactive installation:

1. **Select skills** - Choose which skills to install
2. **Select agents** - Pick target agents (Claude Code, Codex, Cursor, Gemini CLI, Goose, OpenCode)
3. **Installation scope** - Project (committed with your code) or Global
4. **Installation method** - Symlink (recommended) or Copy

```
◇  Found 11 skills
│
◆  Select skills to install
│  ◼ apollo-client
│  ◼ apollo-connectors
│  ◼ apollo-server
│  ○ ...
└
```

## Claude Code Plugin

You can also install skills as a [Claude Code plugin](https://code.claude.com/docs/en/discover-plugins):

First, add the marketplace:

```bash
/plugin marketplace add apollographql/skills
```

Then, install the plugin:

```bash
/plugin install apollo-skills@apollo-marketplace
```

Once installed, skills are available as namespaced slash commands:

| Slash Command | Description |
|---|---|
| `/apollo-skills:apollo-client` | Apollo Client 4.x for React — queries, mutations, caching, local state |
| `/apollo-skills:apollo-connectors` | **Deprecated** — use [`/apollo-skills:graphos-factory`](#graphos-factory) instead |
| `/apollo-skills:apollo-ios` | Apollo iOS — GraphQL client for Swift (iOS, macOS, tvOS, watchOS, visionOS) |
| `/apollo-skills:apollo-kotlin` | Apollo Kotlin — GraphQL client for Android and Kotlin |
| `/apollo-skills:apollo-mcp-server` | Apollo MCP Server — connect AI agents with GraphQL APIs |
| `/apollo-skills:apollo-server` | Apollo Server 4.x — schemas, resolvers, auth, plugins |
| `/apollo-skills:graphos-factory` | GraphOS Factory — build and iterate on an Apollo Connectors subgraph from a REST API |
| `/apollo-skills:graphql-operations` | GraphQL operations — queries, mutations, fragments |
| `/apollo-skills:graphql-schema` | GraphQL schema design — types, naming, pagination, errors |
| `/apollo-skills:rover` | Rover CLI — schema management and local supergraph development |
| `/apollo-skills:rust-best-practices` | Rust best practices — idiomatic Rust following Apollo conventions |
| `/apollo-skills:skill-creator` | Skill creator — guide for creating new Apollo skills |

## GitHub CLI

You can also install skills with the [GitHub CLI](https://cli.github.com/) using `gh skill` (preview):

```bash
# Install skills into the current project for Claude Code
gh skill install apollographql/skills --agent claude-code

# Install at user scope (available everywhere)
gh skill install apollographql/skills --agent claude-code --scope user

# Pin to a specific release (skipped during updates so it won't auto-upgrade)
gh skill install apollographql/skills --pin v1.0.0 --agent claude-code

# Preview skills before installing
gh skill preview apollographql/skills
```

`--agent` supports many hosts beyond Claude Code (Cursor, Codex, Gemini CLI, GitHub Copilot, and more); run `gh skill install --help` for the full list.

## Releases

Releases are tagged with semver and published automatically whenever a content change is merged to `main`. The full list lives at [github.com/apollographql/skills/releases](https://github.com/apollographql/skills/releases).

| Install path | What you get |
|---|---|
| `gh skill install apollographql/skills <name>` | Latest tagged release |
| `gh skill install apollographql/skills <name> --pin v1.0.0` | Pinned to a specific release (skipped during updates) |
| `npx skills add apollographql/skills@<name>` | Latest content from `main` (no tag) |
| Claude Code plugin (`claude plugin install`) | Latest plugin version (auto-updates via `claude plugin update`) |

If you need stability, pin via `gh skill install … --pin vX.Y.Z`. Pinned skills are skipped during `gh skill upgrade`, so you upgrade deliberately. For the freshest content, the other paths track `main` HEAD directly.

## Available Skills

### graphos-factory

Build and iterate on an Apollo Connectors subgraph for a GraphOS supergraph from a REST API, with or without an OpenAPI or Swagger spec. It works with any agent that can run shell commands (Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI and others), and replaces the `apollo-connectors` skill. It is developed in [apollographql/graphos-factory](https://github.com/apollographql/graphos-factory); `skills/graphos-factory/` here is a read-only copy of its latest release, updated by that repository's release workflow.

**Install:**

```bash
npx skills add apollographql/skills@graphos-factory
```

Or from its own repository, with either CLI:

```bash
npx skills add apollographql/graphos-factory
gh skill install apollographql/graphos-factory graphos-factory --agent claude-code   # or codex, cursor, github-copilot, ...
```

In Claude Code it is also part of the [`apollo-skills` plugin](#claude-code-plugin), as `/apollo-skills:graphos-factory`. The first time the agent uses it, the skill downloads its `graphos-factory` binary (about 3 MB) from the release it ships with.

**Use when:**

- Wrapping a REST API as a GraphQL subgraph for your supergraph
- Adding or removing operations or fields on an existing connector subgraph
- Refreshing a connector subgraph against a new version of its spec
- Recording live API traffic as test fixtures

**Categories covered:**

- API discovery and spec intake (OpenAPI 3.x, Swagger 2.0, or no spec)
- Operation and field selection, recorded in a dedicated git workspace
- Connectors schema authoring, naming and mapping
- Verification: composition, connector unit tests, mocked end-to-end and live runs
- Design decisions and hand edits kept across regenerations

**Examples:**

- "Turn this REST API into a subgraph for my supergraph"
- "Build a connector subgraph from this OpenAPI spec"
- "Add the list-issues endpoint to my Gitea subgraph"

**References:**
[SKILL.md](skills/graphos-factory/SKILL.md) ·
[README](https://github.com/apollographql/graphos-factory/blob/main/README.md) ·
[Connectors Language](skills/graphos-factory/graphos-factory-core/references/connectors-language.md) ·
[Mapping Language](skills/graphos-factory/graphos-factory-core/references/mapping-language.md) ·
[Schema Authoring](skills/graphos-factory/graphos-factory-core/references/schema-authoring.md) ·
[Testing](skills/graphos-factory/graphos-factory-core/references/testing.md) ·
[Verification](skills/graphos-factory/references/verification.md)

---

### apollo-federation

Author Apollo Federation subgraph schemas with entities, sharing, and cross-subgraph field resolution.

**Install:**

```bash
npx skills add apollographql/skills --skill apollo-federation
```

**Use when:**

- Creating new subgraph schemas for a federated supergraph
- Defining or modifying entities with `@key`
- Sharing types/fields across subgraphs with `@shareable`
- Working with federation directives (`@external`, `@requires`, `@provides`, `@override`)
- Troubleshooting composition errors

**Categories covered:**

- Entity definition and `@key` patterns (compound, multiple, differing)
- Reference resolvers and computed fields
- Value types with `@shareable`
- Field migration with `@override` (including progressive rollout)
- Entity interfaces with `@interfaceObject`
- Common composition errors and fixes

**Examples:**

- "Create a federated subgraph for my products service"
- "Add a computed field that requires data from another subgraph"
- "Migrate this field from one subgraph to another"

**References:**
[SKILL.md](skills/apollo-federation/SKILL.md) ·
[Directives](skills/apollo-federation/references/directives.md) ·
[Schema Patterns](skills/apollo-federation/references/schema-patterns.md) ·
[Composition](skills/apollo-federation/references/composition.md)

---

### apollo-mcp-server

Configure and use Apollo MCP Server to connect AI agents with GraphQL APIs.

**Install:**

```bash
npx skills add apollographql/skills@apollo-mcp-server
```

**Use when:**

- Setting up Apollo MCP Server for Claude or other AI agents
- Defining MCP tools from GraphQL operations
- Using introspection tools (introspect, search, validate, execute)
- Troubleshooting MCP server connectivity issues

**Categories covered:**

- Server configuration (endpoints, schemas, headers)
- Built-in tools and compact notation
- Operation sources (files, collections, persisted queries)
- Authentication and security
- Health checks and debugging

**Examples:**

- "Set up Apollo MCP Server for my GraphQL endpoint"
- "Configure MCP tools from my GraphQL operations"
- "Debug MCP server connection issues"

**References:**
[SKILL.md](skills/apollo-mcp-server/SKILL.md) ·
[Tools](skills/apollo-mcp-server/references/tools.md) ·
[Configuration](skills/apollo-mcp-server/references/configuration.md) ·
[Troubleshooting](skills/apollo-mcp-server/references/troubleshooting.md)

---

### apollo-router

Configure and run Apollo Router for federated GraphQL supergraphs.

**Install:**

```bash
npx skills add apollographql/skills@apollo-router
```

**Use when:**

- Setting up Apollo Router to run a supergraph
- Configuring routing, headers, or CORS
- Implementing custom plugins (Rhai scripts or coprocessors)
- Configuring telemetry and observability
- Troubleshooting Router performance or connectivity issues

**Categories covered:**

- Installation and quick start
- Router configuration (YAML)
- Header propagation and manipulation
- CORS and authentication
- Rhai scripts and coprocessors
- Telemetry (tracing, metrics, logging)

**Examples:**

- "Set up Apollo Router for my supergraph"
- "Configure CORS for my Router"
- "Add header propagation for authentication"

**References:**
[SKILL.md](skills/apollo-router/SKILL.md) ·
[Configuration](skills/apollo-router/references/configuration.md) ·
[Headers](skills/apollo-router/references/headers.md) ·
[Plugins](skills/apollo-router/references/plugins.md) ·
[Telemetry](skills/apollo-router/references/telemetry.md) ·
[Troubleshooting](skills/apollo-router/references/troubleshooting.md)

---

### apollo-server

Build GraphQL servers with Apollo Server 4.x, including schemas, resolvers, authentication, and plugins.

**Install:**

```bash
npx skills add apollographql/skills@apollo-server
```

**Use when:**

- Setting up a new Apollo Server project
- Writing resolvers or defining GraphQL schemas
- Implementing authentication or authorization
- Creating plugins or custom data sources
- Troubleshooting Apollo Server errors or performance issues

**Categories covered:**

- Quick start setup (standalone and Express)
- Schema definition and type system
- Resolver patterns and best practices
- Context and authentication
- Plugins and lifecycle hooks
- Data sources and DataLoader
- Error handling and formatting

**Examples:**

- "Create an Apollo Server with user authentication"
- "Write resolvers for my GraphQL schema"
- "Add a custom plugin to log all queries"

**References:**
[SKILL.md](skills/apollo-server/SKILL.md) ·
[Resolvers](skills/apollo-server/references/resolvers.md) ·
[Context & Auth](skills/apollo-server/references/context-and-auth.md) ·
[Plugins](skills/apollo-server/references/plugins.md) ·
[Data Sources](skills/apollo-server/references/data-sources.md) ·
[Error Handling](skills/apollo-server/references/error-handling.md) ·
[Troubleshooting](skills/apollo-server/references/troubleshooting.md)

---

### apollo-client

Build React applications with Apollo Client 4.x for GraphQL data management, caching, and local state.

**Install:**

```bash
npx skills add apollographql/skills@apollo-client
```

**Use when:**

- Setting up Apollo Client in a React project
- Writing G