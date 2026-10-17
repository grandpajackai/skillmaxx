<p align="center">
  <img src="https://brightdata.com/wp-content/themes/brightdata/assets/images/favicon.png" alt="Bright Data" width="80" height="80">
</p>

<h1 align="center">Bright Data Plugin for Claude Code</h1>

<p align="center">
  <strong>Unlock the web with AI-powered scraping, search, and structured data</strong>
</p>

<p align="center">
  <a href="https://brightdata.com"><img src="https://img.shields.io/badge/Powered%20by-Bright%20Data-3D7FFC?style=for-the-badge" alt="Powered by Bright Data"></a>
  <a href="#license"><img src="https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge" alt="MIT License"></a>
  <a href="#skills"><img src="https://img.shields.io/badge/Skills-21-9D97F4?style=for-the-badge" alt="21 Skills"></a>
  <a href="#data-feeds-skill"><img src="https://img.shields.io/badge/Scrapers-thousands-15C1E6?style=for-the-badge" alt="Thousands of pre-built scrapers"></a>
  <a href="#bright-data-mcp-skill"><img src="https://img.shields.io/badge/MCP_Tools-30+-FF6B35?style=for-the-badge" alt="30+ MCP Tools"></a>
</p>

<p align="center">
  <a href="#-quick-start">Quick Start</a> •
  <a href="#-skills">Skills</a> •
  <a href="#agent-onboarding-skill">Agent Onboarding</a> •
  <a href="#-data-feeds">Data Feeds</a> •
  <a href="#bright-data-mcp-skill">MCP</a> •
  <a href="#brightdata-cli-skill">CLI</a> •
  <a href="#competitive-intel-skill">Competitive Intel</a> •
  <a href="#scraper-builder-skill">Scraper Builder</a> •
  <a href="#scraper-studio-skill">Scraper Studio</a> •
  <a href="#proxy-skill">Proxy</a> •
  <a href="#best-practices-skill">Best Practices</a> •
  <a href="#python-sdk-best-practices-skill">Python SDK</a> •
  <a href="#javascript-sdk-best-practices-skill">JavaScript SDK</a> •
  <a href="#discover-api-skill">Discover API</a> •
  <a href="#live-research-skill">Live Research</a> •
  <a href="#rag-pipeline-skill">RAG Pipeline</a> •
  <a href="#-setup">Setup</a> •
  <a href="#-examples">Examples</a>
</p>

---

## Overview

This plugin brings **Bright Data's powerful web infrastructure** directly into Claude Code, enabling AI agents to:

- **Scrape any webpage** as clean markdown — bypassing bot detection, CAPTCHAs, and JavaScript rendering
- **Search Google** with structured JSON results — titles, links, and descriptions ready for processing
- **Extract structured data** with thousands of pre-built scrapers — Amazon, LinkedIn, Instagram, TikTok, YouTube, and more
- **Orchestrate 30+ MCP tools** — search, scrape, extract structured data from 1,200+ pre-built scrapers, and automate browsers via Bright Data's MCP server
- **Use the Bright Data CLI** — scrape, search, extract data, manage zones, and check budget directly from the terminal with `brightdata` / `bdata`
- **Run competitive intelligence** — real-time competitor analysis, pricing monitoring, review mining, hiring signal analysis, and market landscape mapping using live web data
- **Write correct Bright Data code** — built-in best practices for Web Unlocker, SERP API, Web Scraper API, and Browser API
- **Route requests through proxies** — generate working code for Datacenter, ISP, Residential, and Mobile proxy networks, with the right network, IP pool type, targeting, and SSL setup
- **Build with the Python SDK** — comprehensive guide for the `brightdata-sdk` package with patterns for async/sync clients, platform scrapers, SERP, datasets, and more
- **Build with the JavaScript/TypeScript SDK** — comprehensive guide for the `@brightdata/sdk` package (`bdclient`) with patterns for web unlocker, platform scrapers, SERP, discover, datasets, browser automation, and Scraper Studio
- **Run the Discover API** — intent-ranked, AI-relevance-scored semantic web search with parsed page content, across REST/CLI/SDK (the foundation for research and RAG)
- **Produce live research briefs** — decompose a question into multi-angle Discover queries, dedup and rank by relevance, and synthesize a cited report from live web data
- **Build RAG / search-engine pipelines** — use Discover as the retrieval layer for an LLM, via live web-grounded retrieval or vector-store ingestion

Built on Bright Data's [Web Unlocker](https://brightdata.com/products/web-unlocker), [SERP API](https://brightdata.com/products/serp-api), and [Web Data APIs](https://brightdata.com/products/web-scraper), this plugin handles the complexity of web access so your AI agents can focus on what matters.

---

## Skills

| Skill | Description |
|-------|-------------|
| **`agent-onboarding`** | Entry point for agents new to Bright Data — one install command, then routes to the right path: live CLI tools, app integration, MCP server, auth-only, or REST without installing |
| **`search`** | Search Google and get structured JSON results with titles, links, and descriptions |
| **`scrape`** | Scrape any webpage as clean markdown with automatic bot detection bypass |
| **`data-feeds`** | Extract structured data with thousands of pre-built scrapers (`bdata pipelines search`, `info`, `run`) |
| **`bright-data-mcp`** | Orchestrate 30+ Bright Data MCP tools for search, scraping, structured extraction, and browser automation |
| **`scraper-builder`** | Build production-ready scrapers for any website — guides through site analysis, API selection, selector extraction, pagination, and complete implementation. Triggers on "build a scraper for..." |
| **`scraper-studio`** | Build and run AI-generated Bright Data scrapers from the terminal via `bdata scraper create` (generate from a natural-language description) and `bdata scraper run` (execute against a URL). Handles async + poll, `--sync` fast-path, and silent auto-fallback to batch for paginated pages |
| **`bright-data-best-practices`** | Built-in reference for Web Unlocker, SERP API, Web Scraper API, and Browser API — Claude consults this automatically when writing Bright Data code |
| **`brightdata-proxy`** | Generate working code to route requests through Bright Data's Datacenter, ISP, Residential, and Mobile proxy networks — network and IP-pool selection, username targeting/session params, SSL CA setup, and integrations for cURL, Python (requests/httpx/aiohttp/Scrapy), Node (fetch/axios), Playwright, Puppeteer, and Selenium |
| **`python-sdk-best-practices`** | Comprehensive guide for the `brightdata-sdk` Python package — async/sync clients, platform scrapers, SERP, datasets, Scraper Studio, Browser API, error handling, and common patterns |
| **`js-sdk-best-practices`** | Comprehensive guide for the `@brightdata/sdk` JavaScript/TypeScript package (`bdclient`, Node ≥20, ESM+CJS) — web unlocker, 11 platform scrapers, SERP, Discover, datasets, Browser API, Scraper Studio, error classes, and batch/trigger orchestration |
| **`discover-api`** | Use the Discover API — intent-ranked, AI-relevance-scored semantic web search with parsed page content. Covers REST (`POST`/`GET /discover`), CLI (`bdata discover`), the SDKs (`client.discover`), the standard/zeroRanking/deep/fast modes, and the trigger→poll flow. Foundation for `live-research` and `rag-pipeline` |
| **`live-research`** | Produce a deep, multi-source, cited research brief — decompose a question into multiple intent-ranked Discover queries, pull page content, dedup and rank by relevance, then synthesize a structured report with inline citations |
| **`rag-pipeline`** | Build a RAG pipeline or custom search engine on top of Discover — live web-grounded retrieval for an LLM, or ingestion into a vector store (discover → chunk → embed → retrieve). Provider-agnostic JS + Python code |
| **`brightdata-cli`** | Guide for using the Bright Data CLI (`brightdata` / `bdata`) to scrape, search, extract structured data with thousands of pre-built scrapers, manage proxy zones, and check account budget — all from the terminal |
| **`competitive-intel`** | Real-time competitive intelligence using live web data — competitor snapshots, pricing comparison, review mining, hiring signal analysis, content & SEO battles, and market landscape mapping. Replaces $15K+/yr enterprise CI tools at pennies per analysis |
| **`brand-listening`** | Social listening and brand reputation research — collects what people are saying about a brand across Reddit, X, Instagram, TikTok, YouTube, news, and review sites, then classifies sentiment, clusters themes, and delivers a cited digest with recommendations. Triggers on "what are people saying about us", "monitor mentions", "brand sentiment" |
| **`price-comparison`** | Shopping price comparison using live retailer data — resolves a product (name, ASIN, or URL) across Amazon, Walmart, eBay, Best Buy, and Google Shopping, normalizes prices/availability/condition into one ranked table, and names the cheapest in-stock buy. Region-aware (currency, stock, local retailers). Triggers on "compare prices", "find the cheapest", "price check", "how much is X on Amazon vs Walmart" |
| **`seo-audit`** | Comprehensive SEO audit using live web data — sitemap-stratified sampling, JS-injected schema detection (Yoast/RankMath/AIOSEO), hreflang validation, signal-driven SERP ranking checks, HTML-level Core Web Vitals proxies. Auto-routes between single-page and site-wide audits |
| **`design-mirror`** | Replicates design system patterns, tokens, and components to build consistent, high-quality UIs |
| **`brd-browser-debug`** | Debug Bright Data Scraping Browser sessions — smart triage of failures, per-session bandwidth tracking, captcha reporting, and pattern detection using the Browser Sessions API |

---

## Agent Onboarding Skill

The `agent-onboarding` skill is the **entry point** for any coding agent that's new to Bright Data. It runs the install once, walks the human through OAuth, verifies the environment, and then routes the agent to the right narrower skill instead of dumping everything into one place.

### How it works

One install command sets up the CLI, agent skills, and authentication:

```bash
# macOS / Linux
curl -fsSL https://cli.brightdata.com/install.sh | bash

# Cross-platform
npm install -g @brightdata/cli

# Then authenticate once (browser OAuth)
bdata login

# Headless / SSH
bdata login --device
```

`bdata login` saves the API key locally, auto-creates the `cli_unlocker` and `cli_browser` zones, and sets defaults — no token plumbing required.

### Path routing

After install, the skill routes the agent based on the task:

| Situation | Path | Hands off to |
|---|---|---|
| Need web data **during this session** | **A** — live CLI tools | `brightdata-cli`, `search`, `scrape`, `data-feeds`, `competitive-intel`, `seo-audit` |
| Need to **add Bright Data to app code** | **B** — SDK / REST integration | `python-sdk-best-practices`, `bright-data-best-practices`, `scraper-builder` |
| Want a **drop-in tool layer for an LLM agent** | **M** — MCP server | `bright-data-mcp` |
| Need an **API key first** | **C** — auth only | dashboard or `bdata login` |
| Don't want to install anything | **D** — REST API directly | direct calls to `api.brightdata.com` |

### Why this skill matters

Without onboarding, agents either skip auth and crash on the first request, or pick the wrong path (calling REST when the CLI would do, or scraping a site that has a pre-built dataset). This skill makes the first 60 seconds deterministic: install, log in, verify, then hand off.

### Reference files

- [skills/agent-onboarding/SKILL.md](skills/agent-onboarding/SKILL.md) — install, auth, path routing, and the post-onboarding skill map

---

## Quick Start

### 1. Get Your Credentials

1. Sign up at [brightdata.com](https://brightdata.com) if you haven't already
2. Go to the [Bright Data Dashboard](https://brightdata.com/cp)
3. Create a **Web Unlocker zone**: Click "Add" → Select "Unlocker zone"
4. Copy your **API Key** from the dashboard

### 2. Set Environment Variables

```bash
export BRIGHTDATA_API_KEY="your-api-key"
export BRIGHTDATA_UNLOCKER_ZONE="your-zone-name"
```

### 3. Start Using

```bash
# Search Google
bash skills/search/scripts/search.sh "artific