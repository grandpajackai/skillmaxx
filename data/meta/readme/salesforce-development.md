# salesforce-development

**Salesforce platform development for agents**

Build apps and agents on the Salesforce Platform with shared skills, Salesforce CLI, and configured MCP tools. The plugin uses your Salesforce DX project and selected org to guide development. Describe your task in natural language.

Choose your coding agent: [Claude Code quick start](#quick-start) or [Use with Codex](#use-with-codex). Each coding agent loads its supported commands and hooks; see the setup and behavior below.

## Quick Start

This quick start covers Claude Code. For Codex CLI 0.145.0 or later on a POSIX host with Bash and Python 3.8 or later, see [Use with Codex](#use-with-codex).

1. **Install prerequisites:**
   - [Claude Code](https://claude.ai/code) — requires Claude Code 2.1.222 or later
   - [Node.js LTS](https://nodejs.org). The bundled language servers run under `node`.
   - [Salesforce CLI](https://developer.salesforce.com/tools/salesforcecli). The MCP host and deploy hooks shell out to `sf`.
   - Python 3.8+. The org-detection, deploy-safety, and agent-validation hooks use Python under the hood.

2. Authorize your Salesforce org. From a terminal or command window, use the `org login web` Salesforce CLI command which opens a browser where you log into your org with your authentication credentials:
   ```bash
   sf org login web --alias my-org --set-default
   ```

3. In Claude Code, install the plugin from the official `claude-plugins-official` marketplace (pre-registered, no `marketplace add` needed):
   ```text
   /plugin install salesforce-development@claude-plugins-official
   ```
   Marketplace versions can differ. Check the installed version in `/plugin`. To use the latest
   release published by Salesforce, install from the Salesforce-hosted marketplace:
   ```text
   /plugin marketplace add forcedotcom/sf-skills
   /plugin install salesforce-development@salesforce
   ```
   If switching marketplaces, use `/plugin` to disable the previous copy so only one copy is enabled.

4. (Optional) Validate your environment:
   ```text
   /salesforce-development:setup
   ```

You're all set. Open a Salesforce DX project and start describing what you need.

## Example Prompts

Once you're all set up, use natural language to describe what you want to do; there's no need to memorize any slash commands:

- "Create an Apex service class to handle Account territory assignments."
- "Generate a custom object `Project__c` with fields for Name, Status, Due Date, and Owner."
- "Deploy the current changes to my sandbox."
- "Write test class for AccountTerritoryService and run it."
- "Validate a deployment to production."
- "Build a permission set that grants read access to Accounts and Contacts."
- “What can I do here?”

## Verify, Update, and Uninstall in Claude Code

- **Verify:** `/plugin` lists `salesforce-development`. `/salesforce-development:status` shows the org/project banner. `"${CLAUDE_PLUGIN_ROOT}"/bin/lsp-doctor` checks the bundled language-server host.
- **Update:** if you installed from `claude-plugins-official`, updates happen automatically; to update manually run `/plugin update salesforce-development@claude-plugins-official`. If you installed from the `salesforce` marketplace, run `/plugin marketplace update salesforce` then `/plugin update salesforce-development@salesforce`.
- **Uninstall:** `/plugin uninstall salesforce-development@claude-plugins-official` (or `@salesforce`, matching however you installed it). If you added the `salesforce` marketplace, also run `/plugin marketplace remove salesforce`.

## What's Included

### Skills

| Area | Skills |
|------|--------|
| **Discovery** | `platform-capability-search` — Generated public-channel capability overview, domain drilldown, installed-versus-available guidance, and on-demand org-feature detection |
| **Environment** | `platform-environment-validate` — Prerequisite scan (Salesforce CLI, Code Analyzer, Node, NPM, Git, MCP, source tracking) with guided installation and update |
| **Project and org lifecycle** | `dx-project-create` — Scaffold a new Salesforce DX project from scratch (template → generate → relocate → auth → default → source tracking); `dx-org-manage` — Create scratch orgs, take org snapshots, open orgs in the browser |
| **Apex** | `platform-apex-generate`, `platform-apex-anonymous-run` (anonymous Apex + debug-log capture), `platform-apex-test-generate`, `platform-apex-test-run`, `platform-apex-logs-debug` |
| **Automation** | `automation-flow-generate` — Screen, Autolaunched, Record-Triggered, and Scheduled Flows |
| **Declarative metadata** | `platform-custom-object-generate`, `platform-custom-field-generate`, `platform-custom-metadata-type-generate`, `platform-custom-setting-generate`, `platform-custom-application-generate`, `platform-custom-tab-generate`, `platform-custom-report-type-generate`, `platform-list-view-generate`, `platform-value-set-generate`, `platform-validation-rule-generate`, `platform-flexipage-generate`, `platform-lightning-app-coordinate` |
| **Data and API context** | `platform-data-manage` — Create, update, delete, import, export, seed, and clean up org records; `platform-soql-query` — SOQL/SOSL authoring, optimization, and query-plan analysis; `platform-data-and-tooling-api-context-get` — Standard-object and Tooling API field/schema reference |
| **Metadata discovery** | `platform-metadata-discovery-get` — Find what already exists in the org and pick the right tool (metadata grounding, scoped SOQL, `sf sobject`, `sf org list metadata`, source retrieval); `platform-metadata-grounding-get` — Find metadata by meaning when the API name is unknown, via the Metadata Grounding MCP (requires Salesforce Catalog in the org) |
| **Deploy and retrieve** | `platform-metadata-deploy` (incl. the production validate → quick-deploy path), `platform-metadata-retrieve`, `platform-manifest-generate` (build `package.xml` / `destructiveChanges.xml`), `platform-metadata-api-context-get`, `platform-destructive-deploy` |
| **Security** | `platform-permission-set-generate`, `platform-sharing-owd-configure`, `platform-sharing-rules-generate` |
| **Reporting** | `platform-report-generate` |
| **LSP** | `platform-lsp-integrate` — Contract and fallbacks for the bundled language-server tools |
| **Headless 360 MCP** | `platform-headless-360-integrate` — Setup, call contract, and errors for the Salesforce-hosted Headless 360 MCP server (`discover`, `describe`, `dispatch`), with confirm-before-write. Task-specific Setup workflows, including Field History Tracking, are discovered and described from H360 at runtime. |

### What Else Is in the Box

- **Claude Code agents** — `salesforce-dev`, the primary Salesforce development agent (activates automatically in Salesforce projects — `sfdx-project.json` present — and routes requests skills-first, then SF CLI, then direct API as a last resort). Code-analysis and Well-Architected review — the `dx-code-analyzer-*` skills, `platform-architecture-analyze`, and the read-only `architecture-review` agent — now live in the separate **salesforce-code-quality** plugin.
- **Claude Code slash commands** — `/salesforce-development:discover` (computed public-channel capability overview/drilldown, `plugins <text>` for on-demand uninstalled-plugin matching, and optional on-demand `features [--target-org <alias>] [--refresh] [--json]`), `:plugin-install` (one-confirmation install for a trusted same-session marketplace recommendation; source confirmation for anything else), `:plugin-recommendations` (view or change how readily uninstalled plugins get proposed; add `--project` to change it for the current project only), `:telemetry`, `:setup`, `:status`, `:org`, `:login`, `:logout`, `:set-default`, `:project`, `:reset-source-tracking`, `:welcome`, `:feedback` (manual-only — see [Feedback](#-feedback) below).
- **Headless 360 opt-in** — H360 defaults off. In disabled mode its launcher completes an empty MCP handshake without starting the proxy, minting auth, or making network requests. Claude Code users enable the **Headless 360 MCP server** plugin setting. Codex CLI and desktop users ask **“Enable Headless 360 in Codex”** to save a local preference, then start a new session normally. No special environment variable or terminal launch is required for that saved opt-in. Enable it only after H360 has been activated in the target org. See `platform-headless-360-integrate` for setup and validation scope, and the [integration design](docs/design/headless-360-mcp-server.md) for startup, authentication, and agent flows.

  Codex saves this user-wide preference and the installed launcher's location in `~/.sf/salesforce-development/headless-360.json`, outside the plugin cache, so the preference survives plugin updates and applies to both CLI and desktop. H360 inherits the selected chat's project directory, rather than the plugin cache or the desktop app's launch directory. If a plugin version update reports that setup is required, ask to enable H360 again to refresh the launcher registration. Ask to disable it to save `false`; neither action changes an org. After registering the launcher, advanced users can still override the opt-in with `SF_HEADLESS_360_ENABLED=enabled|disabled`. Existing environment-only setups must run the local enable command once to register the launcher. If an override is present, it takes precedence over the saved setting. The launcher honors Node on PATH first, then checks `~/.local/bin`, `~/.volta/bin`, `~/.asdf/shims`, `~/.local/share/mise/shims`, `/opt/homebrew/bin`, and `/usr/local/bin`. Node must be installed; it does not download a runtime or source shell profiles. Arbitrary version-manager locations may still require PATH configuration.
- **MCP servers** — `salesforce-metadata-experts` (metadata guidance), `salesforce-metadata-grounding` (finds metadata by meaning through Salesforce Catalog; available in orgs where Catalog is provisioned. `status` and setup report it as an optional row that warns when it is not connected, without blocking), `salesforce-headless-360` (the optional Salesforce-hosted Headless 360 server: org state, Setup settings, and feature access that no CLI command reads; disabled by default. `status` and setup report H360 separately, recommend enabling it for live Setup answers, and probe only when local opt-in is known enabled. Cached health is labeled; endpoint reachability does not prove host tool exposure. See `platform-headless-360-integrate`), and `salesforce-lsp`, a local host that lazily spawns the **Apex** and **SOQL** language servers and exposes their semantic capabilities as MCP tools. See the `platform-lsp-integrate` skill for the tool contract.
- **Hooks** — org-context detection on session start; a production deploy-safety gate and an Apex pre-deploy diagnostics gate on `sf project deploy`; and skills-first advisories that, when no installed skill matches, also propose an uninstalled plugin whose curated description does.

In Claude Code, your progress through **Connect → Project → Build → Test → Deploy → Observe** is tracked from real, successful actions in your project — never assumed. Run `/salesforce-development:discover journey inspect` to review it, or `journey reset` to clear it.

## 💬 Feedback

In Claude Code, run `/salesforce-development:feedback` to submit a rating. It's a manual-only
command (it never shows up in the model's own suggestions) that asks a single 1-5 satisfaction
question right in chat and records it as a local telemetry event — the only thing that leaves your
machine is that numeric rating, tagged the same coarse way as every other telemetry event.

The manual feedback command doesn't collect ratings in Codex. Its optional end-of-turn numeric prompt requires `SFDX_FEEDBACK=1`, enabled telemetry, and eligible activity.

## More Information

- **[Developer guide](https://developer.salesforce.com/docs/platform/salesforce-skills-plugins/guide/salesforce-development-overview.html)** — installation, project a