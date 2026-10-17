# StackHawk Agent Skills

Your agent writes the code. Nothing checks if it's exploitable.

StackHawk agent skills fix that. Install once and your coding agent can configure security scans, run them against your live app, parse the findings, and fix what it found — all in the same session.

## Try It Free
14 days free, no card required. [auth.stackhawk.com/wingman](https://auth.stackhawk.com/wingman)


**Your AI coding agent is also your security team.**

StackHawk agent skills teach your AI coding agent to find security vulnerabilities as you build, report your security posture across applications, and help you fix what it finds — all without leaving your workflow. No context switching, no tickets to another team. Your agent scans, reports, and remediates.

Works with **Claude Code**, **Codex**, **Gemini CLI**, **GitHub Copilot**, **OpenCode**, **Cursor**, and anywhere the [Agent Skills standard](https://agentskills.io) is supported.

---

## Four Skills, One Security Workflow

### [hawkscan](./plugins/hawkscan/) — Scan & Fix

Embeds [HawkScan](https://www.stackhawk.com) DAST scanning directly into your coding loop. Your agent configures the scanner, runs it against your live app, parses the findings, and generates prioritized fix tasks — then re-scans to confirm the fix worked.

```
Code changes → Configure HawkScan → Run scan → Parse findings → Fix → Re-scan
```

**Use it when:** you're building features, finishing a PR, or setting up security testing for a new project.

### [stackhawk-api](./plugins/api/) — Report & Analyze

Queries the StackHawk platform API to give you a picture of your security posture across all your applications. Your agent authenticates, pulls findings data, and presents actionable summaries.

```
Question → Authenticate → Query API → Present Results → Suggest Next Actions
```

**Use it when:** you want to know what needs attention, what changed since the last scan, or which apps are falling behind.

### [hawkscan-ci](./plugins/hawkscan-ci/) — Wire It Into CI

Once HawkScan works locally, this skill graduates it into your CI/CD pipeline. It detects your CI provider, prompts for trigger and blocking behavior, and writes or patches the workflow file. Provider-agnostic — works with GitHub Actions, GitLab, Jenkins, CircleCI, and more.

```
Local scan works → Detect CI provider → Plan integration → Set secret (CI store or external manager) → Write workflow → Verify and report
```

**Use it when:** you have `stackhawk.yml` working locally and want every PR or scheduled build to scan automatically.

### [stackhawk-data-seed](./plugins/stackhawk-data-seed/) — Seed Scan Data

Drives the `hawk perch seed` flow to generate checked-in seed artifacts — SQL scripts, HTTP fixtures, gRPC stubs, and a credentials handoff file — so HawkScan has real data to reach non-trivial application paths.

```
Analyze repo → Design seed manifest → Generate artifacts → Finalize and hand off to hawkscan
```

**Use it when:** your scan is hitting dead ends because endpoints require specific request data or auth state to reach.

---

## Quick Start

### 1. Get your API key

Sign up or log in at [app.stackhawk.com](https://app.stackhawk.com), go to **Settings → API Keys**, and create a key.

```bash
export HAWK_API_KEY=hawk.xxxxxxxxxxxx.xxxxxxxxxxxx
```

### 2. Install for your platform

#### Claude Code

```
/plugin marketplace add stackhawk/agent-skills
/plugin install wingman@stackhawk      # installs hawkscan + api + data-seed + optimize
```

Advanced — install individually instead:

```
# /plugin install hawkscan@stackhawk
# /plugin install stackhawk-api@stackhawk
# /plugin install hawkscan-ci@stackhawk
# /plugin install stackhawk-data-seed@stackhawk
# /plugin install stackhawk-optimize@stackhawk
```

#### Codex

```
/plugin marketplace add stackhawk/agent-skills
/plugin install hawkscan@stackhawk
/plugin install stackhawk-api@stackhawk
/plugin install hawkscan-ci@stackhawk
/plugin install stackhawk-data-seed@stackhawk
/plugin install stackhawk-optimize@stackhawk
```

Or use `/plugin install wingman@stackhawk` to get hawkscan, stackhawk-api, stackhawk-data-seed, and stackhawk-optimize in one install.

#### Gemini CLI

```bash
gemini extensions install https://github.com/stackhawk/agent-skills
```

#### GitHub Copilot

```
copilot plugin marketplace add stackhawk/agent-skills-marketplace
copilot plugin install wingman@stackhawk
```

`wingman` bundles the four default skills (`hawkscan`, `stackhawk-api`,
`stackhawk-data-seed`, `stackhawk-optimize`). Copilot has no plugin-dependency
mechanism, so wingman ships these as bundled copies rather than resolving them.

To add `hawkscan-ci` on top of an existing `wingman` install (it is not a
wingman dependency, but is separately installable):

```
copilot plugin install hawkscan-ci@stackhawk
```

To install skills individually **instead of** `wingman` (do not run this after
installing `wingman` — it duplicates the four skills you already have):

```
copilot plugin install hawkscan@stackhawk
copilot plugin install stackhawk-api@stackhawk
copilot plugin install hawkscan-ci@stackhawk
copilot plugin install stackhawk-data-seed@stackhawk
copilot plugin install stackhawk-optimize@stackhawk
```

Plugins install to `~/.copilot/installed-plugins/stackhawk/<plugin>/`. Confirm
they appear under **GitHub Copilot → Configure Skills** in VS Code.

Skill names differ between the two install paths above. The `wingman` bundle
namespaces its copies, so they list as `hawkscan`, `stackhawk-api`,
`stackhawk-data-seed`, and `stackhawk-optimize`. A per-plugin install reads the
source skill instead, so `stackhawk-api` and `stackhawk-optimize` list as `api`
and `optimize`. Renaming the source skills would change their invocation names
on every platform, so it is deferred to a separate major release.

#### OpenCode

Skills are auto-discovered from `.opencode/skills/`. Clone and copy (`-L` dereferences
the repo's internal skill symlinks so the copies work standalone):

```bash
git clone https://github.com/stackhawk/agent-skills.git
mkdir -p .opencode/skills
cp -rL agent-skills/.opencode/skills/* .opencode/skills/

# Global install (all projects):
mkdir -p ~/.config/opencode/skills
cp -rL agent-skills/.opencode/skills/* ~/.config/opencode/skills/
```

Installs `hawkscan`, `stackhawk-api`, `hawkscan-ci`, `stackhawk-data-seed`, and `stackhawk-optimize`.

#### Cursor

```bash
# macOS / Linux
git clone https://github.com/stackhawk/agent-skills.git
bash agent-skills/scripts/install.sh --platform cursor --target .
```

```powershell
# Windows
git clone https://github.com/stackhawk/agent-skills.git
.\agent-skills\scripts\install.ps1 -Platform cursor
```

Installs Cursor rules (`.cursor/rules/`), skills (`.cursor/skills/`), and the stop hook that auto-triggers a scan when you finish coding.

#### skills CLI (npx)

Works with any agent the [`skills` CLI](https://github.com/vercel-labs/skills) supports. One command installs the current GA release for every agent it detects:

```bash
npx skills add stackhawk/agent-skills-marketplace --all
```

Add `-g` to install globally (every project) instead of into the current one. To move to the next release later (the CLI re-fetches the marketplace repo and re-copies changed skills; this update path is expected from the CLI source and is checked after each release):

```bash
npx skills update
```

Skill names are the namespaced ones: `hawkscan`, `stackhawk-api`, `hawkscan-ci`, `stackhawk-data-seed`, and `stackhawk-optimize`. Install from `stackhawk/agent-skills-marketplace`, not this repo — the marketplace carries the released skills, while this repo's `main` is unreleased work.

**Skills only, no hooks.** The `skills` CLI installs `SKILL.md` and `references/` for each skill. It does not install the hawkscan plugin's hooks, so the automatic scan after a code change does not fire. Claude Code, Codex, and Copilot users who want the hooks should install the plugin instead — the slash commands above, or the scriptable form:

```bash
# Claude Code (no global install needed)
npx @anthropic-ai/claude-code plugin marketplace add stackhawk/agent-skills-marketplace
npx @anthropic-ai/claude-code plugin install wingman@stackhawk

# Codex
codex plugin marketplace add stackhawk/agent-skills-marketplace
codex plugin add hawkscan@stackhawk

# GitHub Copilot
copilot plugin marketplace add stackhawk/agent-skills-marketplace
copilot plugin install wingman@stackhawk
```

### 3. Try it

```
> "Scan my API for security vulnerabilities"

> "What's my security posture across all apps?"
```

---

## What You Can Do

### Scanning Workflows (hawkscan skill)

| Say this... | Your agent will... |
|-------------|---------------|
| "Set up HawkScan for my Express API" | Generate a `stackhawk.yml` config based on your stack |
| "Scan my app for security issues" | Validate config, run `hawk scan`, parse findings |
| "Turn these scan findings into fix tasks" | Prioritize by severity, generate actionable fix guidance |
| "I'm finishing up this feature" | Proactively suggest a security scan before you merge |
| "My HawkScan auth is failing" | Debug your authentication configuration |
| "Set up HawkScan in my CI pipeline" | Generate CI-specific config with commit tagging |

### Reporting Workflows (api skill)

| Say this... | Your agent will... |
|-------------|---------------|
| "What's my security posture?" | Pull untriaged findings across all apps, present as a summary table |
| "Show me findings for payment-api" | Drill down: scan → alerts → findings with severity, CWE, paths |
| "Which apps haven't been scanned recently?" | Flag stale apps with no scan in 30+ days |
| "What changed since the last scan?" | Diff two scans, show new and resolved findings |

---

## Supported Configurations

**API & App Types:** REST/OpenAPI, GraphQL, gRPC, SOAP, JSON-RPC, standard web apps

**Authentication Patterns:** Bearer token injection, form login (username/password), cookie sessions, OAuth2/external IdP (Auth0, Okta, Cognito), external command, custom scripts

**Scan Runtimes:** `hawk` CLI (recommended for local/agentic use), Docker (`stackhawk/hawkscan`)

**Environments:** Local development, CI/CD (GitHub Actions, GitLab CI, Jenkins, etc.)

---

## How It Works

These are [Agent Skills](https://agentskills.io) — they teach AI coding agents domain-specific knowledge through structured markdown files. No runtime dependencies are installed. No code runs in the background.

- **Skill files** define step-by-step workflows with decision logic (assess → configure → execute → parse → act)
- **Reference files** provide endpoint catalogs, config patterns, and pre-built recipes loaded on demand
- The hawkscan skill calls the `hawk` CLI or Docker to run scans
- The api skill calls the StackHawk REST API via `curl` and `jq`

### Repository Structure

```
plugins/
├── hawkscan/                    HawkScan DAST scanning
│   └── skills/hawkscan/
│       ├── SKILL.md             scan workflow
│       └── references/          CLI flags, config patterns, findings schema, Docker, install
├── api/                         StackHawk API reporting
│   └── skills/api/
│       ├── SKILL.md             reporting workflow
│       └── references/          auth flow, endpoint catalog, reporting recipes
├── hawkscan-ci/                 CI/CD pipeline integration
│   └── skills/hawkscan-ci/
│       ├── SKILL.md             CI wiring workflow
│       └── references/          execution shapes, app startup, failure semantics
└── stackhawk-data-seed/         Scan data seeding
    └── skills/stackhawk-data-seed/
        └── SKILL.md             hawk perch seed workflow
skills/                          Symlinks for Gemini/Copilot discovery
cursor/                          Generated Cursor .mdc rules
scripts/install.sh               Installer for Cursor and Copilot (macOS/Linux)
scripts/install.ps1              Installer for Cursor and Copilot (Windows)
scripts/generate-marketplace-catalogs.py   Builds local inst