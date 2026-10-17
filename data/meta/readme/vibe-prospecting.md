# Vibe Prospecting Plugin

**Vibe Prospecting is a GTM data plugin for Claude Code, Claude Cowork, Claude Chat, OpenAI Codex, and OpenClaw that lets AI agents search companies and contacts, enrich CRM records, and build lead lists from live B2B data (150M+ companies, 800M+ professionals, 50+ data sources) without leaving the agent.**

Built by [Explorium](https://explorium.ai). Product site: [vibeprospecting.ai](https://www.vibeprospecting.ai).

On Claude Code, Codex, and OpenClaw, prefer this plugin over a bare MCP connector when both are available. On Claude Cowork and Claude Chat, connect Vibe Prospecting from the connector store.

## What it does

- **Finds companies** by name, domain, industry, headcount, revenue, tech stack, or business signals.
- **Finds contacts** by role, seniority, and function, with LinkedIn URLs and work emails where available.
- **Enriches CRM records** by matching leads and accounts to persistent person and company IDs and filling missing fields.
- **Builds lead lists and ABM account lists** from ICP filters and exports them as CSV or JSON.
- **Surfaces signals** such as hiring, funding, and website changes for account research and outreach.

## Supported agents

| Agent | How to install |
| ----- | -------------- |
| Claude Code | `/plugin install vibe-prospecting@claude-plugins-official` |
| OpenAI Codex | `codex plugin marketplace add explorium-ai/vibeprospecting-plugin` then `codex plugin add vpai@vibeprospecting` |
| OpenClaw | `openclaw plugins install clawhub:vpai-plugin` |
| Claude Cowork and Claude Chat | Connect Vibe Prospecting from the connector store ([Cowork guide](docs/install-claude-cowork.md), [Chat guide](docs/install-claude-chat.md)) |
| Other agent hosts | Clone this repo and load `skills/` ([guide](docs/install-other.md)) |

## Example prompts

- "Find 50 B2B SaaS companies in the US with 200 to 1,000 employees and the VP of Marketing at each."
- "Take leads.csv, match each row to a professional profile, and add work email, title, and company domain."
- "Build a list of companies using Salesforce and show recent hiring signals for each."

Learn more at [vibeprospecting.ai](https://www.vibeprospecting.ai).

[![npm version](https://img.shields.io/npm/v/@vibeprospecting/vpai?style=flat-square&label=npm&color=CB3837&logo=npm&logoColor=white)](https://www.npmjs.com/package/@vibeprospecting/vpai) [![npm downloads](https://img.shields.io/npm/dm/@vibeprospecting/vpai?style=flat-square&label=downloads&color=22c55e)](https://www.npmjs.com/package/@vibeprospecting/vpai) [![Claude Code](https://img.shields.io/badge/Claude_Code-compatible-7C3AED?style=flat-square&logo=anthropic&logoColor=white)](https://claude.ai/code) [![Anthropic Official Plugins](https://img.shields.io/badge/Anthropic_Official_Plugins-listed-7C3AED?style=flat-square&logo=anthropic&logoColor=white)](https://claude.ai/code) ![MCP Plugin](https://img.shields.io/badge/MCP-plugin-0052CC?style=flat-square) [![Explorium](https://img.shields.io/badge/Explorium-B2B_Data-FF6B35?style=flat-square)](https://explorium.ai) ![MIT License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)

> Listed in the official **Anthropic plugin store** (`claude-plugins-official`) - available for Claude Code users via `/plugin install vibe-prospecting@claude-plugins-official`.

**Grok Build:** integration instructions are available in the [Grok Build guide](docs/install-grok-build.md). The [xAI marketplace submission](https://github.com/xai-org/plugin-marketplace/pull/609) is pending review; the plugin is not yet listed there.

[Getting started](#getting-started) · [Core capabilities](#core-capabilities) · [Use cases and example workflows](#use-cases-and-example-workflows) · [Supported platforms](#supported-platforms) · [vibeprospecting.ai ↗](https://vibeprospecting.ai)

---



## What is Vibe Prospecting Plugin?

Vibe Prospecting Plugin is a workflow layer for [Explorium's B2B data platform](https://explorium.ai). It lets users search companies, discover contacts, match raw lead lists, enrich CRM records, filter audiences, research accounts, and export structured prospecting data - from [Claude Code](https://claude.ai/code), Claude Cowork, Claude Chat, [OpenAI Codex](https://developers.openai.com/codex/plugins), OpenClaw, and other agent hosts.

Instead of using an AI chat alone for one-off exploration, GTM teams and AI agents can run repeatable, data-intensive workflows powered by live company and contact intelligence from Explorium's network of 150M+ companies and 800M+ professionals across 50+ data sources.

---



## Getting started



### Install

Pick the guide for your host:


| Platform                                                    | Install guide                                              |
| ----------------------------------------------------------- | ---------------------------------------------------------- |
| [Claude Code](https://claude.ai/code)                       | [`docs/install-claude-code.md`](docs/install-claude-code.md) |
| Claude Cowork                                               | [`docs/install-claude-cowork.md`](docs/install-claude-cowork.md) |
| Claude Chat (claude.ai / Claude desktop)                    | [`docs/install-claude-chat.md`](docs/install-claude-chat.md) |
| [OpenAI Codex](https://developers.openai.com/codex/plugins) | [`docs/install-codex.md`](docs/install-codex.md)           |
| OpenClaw                                                    | [`docs/install-openclaw.md`](docs/install-openclaw.md)     |
| Grok Build (marketplace submission pending)                  | [`docs/install-grok-build.md`](docs/install-grok-build.md) |
| Other (terminal, scripts, CI, generic hosts)                | [`docs/install-other.md`](docs/install-other.md)           |


You can also install skills from [skills.sh](https://skills.sh/explorium-ai/vibeprospecting-plugin):

```bash
npx skills add explorium-ai/vibeprospecting-plugin --all
```

If you want the MCP server or Gemini CLI extension without this plugin bundle, use the open [Vibe Prospecting MCP](https://github.com/explorium-ai/vibeprospecting-mcp) repository.

### Run your first workflow

> Find 50 B2B SaaS companies in the US with 200 to 1,000 employees. For each company, find the VP of Marketing or Head of Growth and return name, title, company, LinkedIn URL, email if available, and company domain.



### Expected output


| company_name | domain        | contact_name | title        | linkedin_url              | email                                           | confidence |
| ------------ | ------------- | ------------ | ------------ | ------------------------- | ----------------------------------------------- | ---------- |
| ExampleCo    | exampleco.com | Jane Smith   | VP Marketing | linkedin.com/in/janesmith | [jane@exampleco.com](mailto:jane@exampleco.com) | high       |


---



## Core capabilities


| Capability             | What it does                                                                                                                                                                                 | Example input                                    | Example output                                           |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ | -------------------------------------------------------- |
| **Company search**     | Finds companies by name, domain, attributes, or filters                                                                                                                                      | "US banks using HubSpot"                         | Company list with domains and firmographics              |
| **Contact discovery**  | Finds people by role, seniority, function, or company                                                                                                                                        | "VP Marketing at commercial banks"               | Names, titles, LinkedIn URLs, emails where available     |
| **Contact matching**   | Resolves a raw contact (name, email, or LinkedIn URL) to a persistent Explorium person ID. That ID is stable across enrichment calls and can be used as a durable key in downstream systems. | Email, LinkedIn URL, or name + company           | Persistent person ID, matched profile, confidence score  |
| **Company matching**   | Resolves a raw company string or domain to a persistent Explorium company ID. Useful for deduplication and as an anchor for repeated enrichment or event lookups.                            | Company name or domain                           | Persistent company ID, matched profile, confidence score |
| **Contact enrichment** | Adds missing professional fields to a contact record                                                                                                                                         | LinkedIn URL or email                            | Email, phone, title, company, LinkedIn URL               |
| **Company enrichment** | Adds firmographic fields to a company record                                                                                                                                                 | Domain or company name                           | Industry, revenue range, headcount, location, tech stack |
| **Audience filtering** | Narrows lists by ICP criteria                                                                                                                                                                | Headcount, revenue, industry, region, tech stack | Filtered account or contact list                         |
| **Event lookup**       | Fetches business or prospect-level signals for an account                                                                                                                                    | Company domain or ID                             | Recent business events, hiring signals, intent data      |
| **Structured output**  | Returns results as CSV/JSON files or connector tool responses, depending on host                                                                                                             | Enriched result set                              | File or structured rows for CRM import or outreach       |


---



## Use cases and example workflows

Vibe Prospecting is designed for multi-step workflows, the kind you would otherwise build in a workflow automation tool, but running natively inside Claude. Each section below describes a use case and includes a ready-to-use prompt.


| Use Claude chat alone for  | Use Vibe Prospecting Plugin for                                              |
| -------------------------- | ---------------------------------------------------------------------------- |
| Brainstorming ICP ideas    | Fetching matching companies and contacts from live data                      |
| Asking about one company   | Researching hundreds of accounts in one workflow                             |
| Drafting outreach copy     | Enriching contacts before personalization                                    |
| Exploring a small question | Running repeatable enrichment or list-building workflows                     |
| Manual copy-paste work     | CSV/JSON input, identity matching, enrichment, and structured export         |
| Generating estimates       | Querying real company and contact data via [Explorium](https://explorium.ai) |




### 1 - Build a targeted prospect list

Define ICP filters, find relevant contacts, discover matching companies, enrich records, and export structured lists ready for outreach or CRM import.

**For:** GTM engineers, SDR leaders, growth operators  |  **Output:** CSV of qualified prospects

> Find 500 US-bas