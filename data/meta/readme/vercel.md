# vercel-plugin

## Getting Started

### Supported Tools

| Tool                                                          | Status    |
| ------------------------------------------------------------- | --------- |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | Supported |
| [Cursor](https://www.cursor.com)                              | Supported |
| [GitHub Copilot CLI](https://github.com/github/copilot-cli)   | Supported |
| [OpenAI Codex](https://openai.com/index/codex/)               | Supported |
| [Grok Build](https://x.ai/news/grok-build-cli)                | Supported |
| [Kimi Code](https://kimi.com)                                 | Supported |
| [OpenCode](https://opencode.ai) 2                             | Supported |

### Prerequisites

- One of the supported AI coding tools listed above
- Node.js 18+
- [Bun](https://bun.sh)

### Installation

```bash
npx plugins add vercel/vercel-plugin
```

That's it. The plugin installs Vercel context, skills, and a lightweight default hook profile.

For OpenCode 2, install it as a native OpenCode plugin:

```bash
opencode plugin add github:vercel/vercel-plugin
```

OpenCode loads the same skills, agents, commands (`/vercel:deploy`, `/vercel:env`, `/vercel:status`, `/vercel:bootstrap`), session context, and Vercel MCP server. Run `/mcps` in OpenCode to sign in to the MCP server. Node.js and Bun are not needed for OpenCode.

## What It Does

This plugin gives AI agents a **relational knowledge graph** of the Vercel ecosystem plus a bundled skill library covering products, libraries, CLI, APIs, and workflows.

## How Do I Use This?

After installing, the plugin keeps automatic behavior lightweight. Session-start activation now only kicks in for empty directories and detected Vercel, Next.js, or eve projects, and Vercel skills are no longer auto-injected on every tool call or every prompt by default. The default post-tool path is now observer-only. The skills remain available for direct use, and the repo still keeps the injection engine for targeted or future opt-in workflows.

## Vercel MCP connection

The bundled `.mcp.json` connects to `https://mcp.vercel.com`. Authenticate and grant
access to the intended teams before using account tools. MCP supports both reads
and writes, including inspecting projects and logs, creating deployments, and
updating resources. Inspect the tools and schemas exposed by your connection.
Domain registration requires a quote and explicit approval; digital subscriptions,
credits, and add-on purchases are unavailable through MCP.

## Components

### Ecosystem Graph (`vercel.md`)

A text-form relational graph covering:

- All Vercel products and their relationships
- Decision matrices for choosing the right tool
- Common cross-product workflows
- Migration awareness for sunset products

### Skills (34 skills)

| Skill                   | Covers                                                                                                                               |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `access-protected-vercel-deployment` | Authenticated CLI and browser access to protected preview and production deployments using `vc curl`, OIDC, and Trusted Sources |
| `ai-gateway`            | Unified model API, provider routing, failover, cost tracking, 100+ models                                                            |
| `ai-sdk`                | AI SDK 7 — text/object generation, streaming, tool calling, agents, MCP, providers, embeddings                                       |
| `auth`                  | Authentication integrations — Clerk, Better Auth, Descope, Auth0 setup for Next.js with Marketplace provisioning                     |
| `bootstrap`             | Project bootstrapping orchestrator — linking, env provisioning, db setup, first-run commands                                         |
| `build-agents`          | Default eve-first agent builder — create AI agents, agent apps, tools, channels, schedules, and Slack agents                         |
| `cdn-caching`           | Diagnose cache hit rate, stale content, revalidation behavior, per-request cache reasons, and ISR read/write cost across CDN/ISR/PPR |
| `chat-sdk`              | Multi-platform chat bots — Slack, Telegram, Teams, Discord, Google Chat, GitHub, Linear                                              |
| `create-a-backend`      | Backend product and framework selection — Functions, Services, containers, Workflow, Queues, and databases                          |
| `custom-metrics`        | Emit numeric application and business measurements from Functions and query them with `vc metrics`                                 |
| `daemons`               | Vercel Daemons — long-running Dockerfile-built workers declared under `daemons` in vercel.json, instances per region, SIGTERM, Queues poll mode |
| `deployments-cicd`      | Deployment and CI/CD — deploy, promote, rollback, --prebuilt, CI workflow files                                                      |
| `domains`              | Public domain search and pricing, CLI and Registrar API operations, project domains, DNS, transfers, and renewals                    |
| `env-vars`              | Environment variable management — .env files, vercel env commands, OIDC tokens                                                       |
| `eve`                   | Filesystem-first framework for durable AI agents, agent applications, channels, sandboxes, schedules, evals, and frontend clients    |
| `flags-sdk`             | Feature flags and A/B tests — Flags SDK, provider adapters, `vercel flags` CLI, precompute, Flags Explorer                           |
| `is-agentic`            | Score how ready a website, domain, or public MCP endpoint is for AI agents, and act on the Is Agentic report                        |
| `knowledge-update`      | Knowledge update guidance for the plugin                                                                                             |
| `marketplace`           | Integration discovery and installation (`vercel integration add` / `vercel install`), provider agent skills, auto-provisioned env vars, unified billing |
| `microfrontends`        | Multi-zone and microfrontend architecture, routing, deployment boundaries, and shared dependencies                                   |
| `queues`                | Vercel Queues — durable topics, `@vercel/queue` publish/consume, consumer groups, retries, delays, idempotency, Queues vs Workflows   |
| `react-best-practices`  | React/Next.js performance optimization — 64 rules across 8 categories                                                                |
| `routing-middleware`    | Request interception before cache, rewrites, redirects, personalization — Edge/Node.js/Bun runtimes                                  |
| `runtime-cache`         | Ephemeral per-region key-value cache, tag-based invalidation, shared across Functions/Middleware/Builds                              |
| `vercel-agent`          | Vercel Agent chat (dashboard, Slack), code review, investigations, approved actions, product installation                            |
| `vercel-cli`            | All CLI commands — deploy, env, dev, domains, cache management, MCP integration, marketplace                                         |
| `vercel-connect`        | Managed OAuth tokens and third-party connections for apps, MCP servers, and eve agents                                               |
| `vercel-firewall`       | DDoS protection, WAF rules, rate limiting, bot filtering, and IP controls                                                            |
| `vercel-functions`      | Node.js, Bun, Python, and Rust runtimes on Fluid Compute, streaming, WebSockets, Cron Jobs, configuration                         |
| `vercel-sandbox`        | Ephemeral Firecracker microVMs for running untrusted/AI-generated code safely                                                        |
| `vercel-services`       | Multiple frontends and backends in one project, with public rewrites and private service bindings                                    |
| `vercel-storage`        | Blob, Global Config (formerly Edge Config), Neon Postgres, Upstash Redis, migration from sunset packages                             |
| `verification`          | Full-story verification — infers user story, verifies end-to-end browser → API → data → response                                     |
| `workflow`              | Workflow SDK — durable execution, WorkflowAgent, steps, Worlds, pause/resume                                                         |

Next.js framework guidance comes from Next.js itself, following the [official agent setup](https://nextjs.org/docs/app/guides/ai-agents): version-matched docs bundled in `node_modules/next/dist/docs/` (with `AGENTS.md` generated by `next dev` on 16.3+), plus workflow skills installed with `npx skills add vercel/next.js`. The plugin points agents there instead of shipping its own Next.js skills.

### Agents (3 specialists)

| Agent                   | Expertise                                                                       |
| ----------------------- | ------------------------------------------------------------------------------- |
| `deployment-expert`     | CI/CD pipelines, deploy strategies, troubleshooting, environment variables      |
| `performance-optimizer` | Core Web Vitals, rendering strategies, caching, asset optimization              |
| `ai-architect`          | AI application design, model selection, streaming architecture, MCP integration |

### Commands (4 commands)

| Command                    | Purpose                                                 |
| -------------------------- | ------------------------------------------------------- |
| `/vercel-plugin:bootstrap` | Bootstrap project — linking, env provisioning, db setup |
| `/vercel-plugin:deploy`    | Deploy to Vercel (preview or production)                |
| `/vercel-plugin:env`       | Manage environment variables                            |
| `/vercel-plugin:status`    | Project status overview                                 |

### Hooks

Lifecycle hooks that run automatically during your session:

- **Session start context injection** — Injects a thin Vercel session context plus the knowledge-update guidance for empty directories and detected Vercel, Next.js, or eve projects
- **Session start repo profiler** — Scans config files and dependencies to set likely-skill hints, but only after that same activation check passes

## Usage

After installing, session context is injected automatically only for empty directories and detected Vercel, Next.js, or eve projects. Vercel skills are available on demand, and you can invoke them directly via slash commands:

```
/vercel-plugin:build-agents
/vercel-plugin:ai-sdk
/vercel-plugin:deploy prod
```

## Telemetry

Telemetry is on by default and can be disabled with `VERCEL_PLUGIN_TELEMETRY=off`.

What is collected:

- `dau:active_today`: sent at most once per UTC day when the plugin runs.
- `plugin:first_use`: sent once per local user profile the first time the plugin successfully reports telemetry.
- `plugin:version`: sent with telemetry batches so usage can be grouped by plugin version.
- `plugin:install_id`: the locally stored random installation UUID.
- `plugin:agent_harness`: each distinct detected agent harness category observed per installation per UTC day.
- `skill:invoked`: the name of a skill or command that ships with this plugin (for example `ai-sdk`, `workflow`, `deploy`) each time it is loaded through the agent's `Skill` tool — whether you typed the slash command or the model chose it. See [Skill telemetry](#skill-telemetry) below.
- `skill:injected`: the same skill names, sent when the plugin's opt-in injection hooks (`pretooluse-skill-inject`, `u