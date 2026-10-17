![Ory Lumen: Semantic code search for AI agents](.github/lumen-banner.png)

[![CI](https://github.com/ory/lumen/actions/workflows/ci.yml/badge.svg)](https://github.com/ory/lumen/actions/workflows/ci.yml)
[![Go Report Card](https://goreportcard.com/badge/github.com/ory/lumen)](https://goreportcard.com/report/github.com/ory/lumen)
[![Go Reference](https://pkg.go.dev/badge/github.com/ory/lumen.svg)](https://pkg.go.dev/github.com/ory/lumen)
[![Coverage Status](https://coveralls.io/repos/github/ory/lumen/badge.svg?branch=main)](https://coveralls.io/github/ory/lumen?branch=main)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

Claude reads entire files to find what it needs. Lumen gives it a map.

Lumen is a 100% local semantic code search engine for AI coding agents. No API
keys, no cloud, no external database, just open-source embedding models
([Ollama](https://ollama.com/) or [LM Studio](https://lmstudio.ai/)), SQLite,
and your CPU. A single static binary and your own local embedding server.

The payoff is measurable and reproducible: across 9 benchmark runs on 9
languages and real GitHub bug-fix tasks, Lumen cuts cost in **every single
language** — up to 39%. Output tokens drop by up to 66%, sessions complete up to
53% faster, and patch quality is maintained in every task. All verified with a
[transparent, open-source benchmark framework](docs/BENCHMARKS.md) that you can
run yourself.

|                        | With Lumen                    | Baseline (no Lumen)  |
| ---------------------- | ----------------------------- | -------------------- |
| Cost (avg, bug-fix)    | **$0.29** (-26%)              | $0.40                |
| Time (avg, bug-fix)    | **125s** (-28%)               | 174s                 |
| Output tokens (avg)    | **5,247** (-37%)              | 8,323                |
| JavaScript (marked)    | **$0.32, 119s** (-33%, -53%)  | $0.48, 255s          |
| Rust (toml)            | **$0.38, 204s** (-39%, -34%)  | $0.61, 310s          |
| PHP (monolog)          | **$0.14, 34s** (-27%, -34%)   | $0.19, 52s           |
| TypeScript (commander) | **$0.14, 56s** (-27%, -33%)   | $0.19, 84s           |
| Svelte (chat-ui)       | **$0.10, 56s** (-26%, -31%)   | $0.14, 80s           |
| Patch quality          | **Maintained in all 9 tasks** | —                    |

## Table of contents

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Demo](#demo)
- [Quick start](#quick-start)
- [What you get](#what-you-get)
- [How it works](#how-it-works)
- [Benchmarks](#benchmarks)
- [Supported languages](#supported-languages)
- [Configuration](#configuration)
  - [Supported embedding models](#supported-embedding-models)
- [Controlling what gets indexed](#controlling-what-gets-indexed)
- [Database location](#database-location)
- [CLI Reference](#cli-reference)
- [Troubleshooting](#troubleshooting)
- [Development](#development)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Demo

<img src="docs/demo/demo.gif" alt="Lumen demo" width="600"/>

_Claude Code asking about the
[Prometheus](https://github.com/prometheus/prometheus) codebase. Lumen's
`semantic_search` finds the relevant code without reading entire files._

## Quick start

**Prerequisites:**

> **Platform support:** Linux, macOS, and Windows. File locking for background
> indexing coordination uses `flock(2)` on Unix and `LockFileEx` on Windows
> (via [gofrs/flock](https://github.com/gofrs/flock)).

1. [Ollama](https://ollama.com/) installed and running, then pull the default
   embedding model:
   ```bash
   ollama pull ordis/jina-embeddings-v2-base-code
   ```
2. One of:
   [Claude Code](https://code.claude.com/docs/en/quickstart),
   [Cursor](https://cursor.com/),
   [Codex](https://developers.openai.com/codex/cli), or
   [OpenCode](https://opencode.ai/)

**Note:** Installation differs by platform. Claude Code and Codex install from
plugin marketplaces. OpenCode installs from npm. Cursor packaging is shipped
in this repository and is ready for Cursor's plugin distribution workflow.

**Install:**

**Claude Code**

```bash
/plugin marketplace add ory/claude-plugins
/plugin install lumen@ory
```

Verify by starting a new Claude session and running `/lumen:doctor`.

**Cursor**

Lumen ships a native Cursor plugin bundle in this repository:

- `.cursor-plugin/plugin.json` - plugin manifest
- `mcp.json` - local `lumen` MCP server wiring
- `hooks/hooks-cursor.json` - SessionStart hook
- `skills/` - shared `doctor` and `reindex` skills

Use Cursor's plugin installation or distribution workflow with this bundle.
Detailed packaging notes: [.cursor-plugin/INSTALL.md](.cursor-plugin/INSTALL.md)

Verify by opening a new Cursor agent session and asking it to use the `doctor`
skill or the Lumen `semantic_search` tool.

**Codex**

Codex CLI 0.147.0 or newer installs Lumen as a native plugin:

```bash
codex plugin marketplace add ory/claude-plugins
codex plugin add lumen@ory
```

If the marketplace already exists, run `codex plugin marketplace upgrade ory`
before installing. Legacy manual-clone and broken-plugin repair instructions:
[.codex/INSTALL.md](.codex/INSTALL.md).

Verify with:

```bash
codex mcp get lumen --json
```

**OpenCode**

Add `@ory/lumen-opencode` to the `plugin` array in your `opencode.json`:

```json
{
  "plugin": ["@ory/lumen-opencode"]
}
```

Detailed docs: [.opencode/INSTALL.md](.opencode/INSTALL.md)

Verify with:

```bash
opencode mcp list
```

**Updating**

- **Claude Code** - update through Claude's plugin marketplace
- **Cursor** - refresh or reinstall the bundled plugin through Cursor after
  updating this repository or the published package
- **Codex** - upgrade the `ory` marketplace, reinstall `lumen@ory`, and restart
- **OpenCode** - update the version pin in `opencode.json` (e.g.
  `@ory/lumen-opencode@0.0.29`) and restart OpenCode

On first Claude Code or Cursor session start, Lumen:

1. Downloads the binary automatically from the
   [latest GitHub release](https://github.com/ory/lumen/releases)
2. Indexes your project in the background using Merkle tree change detection
3. Registers a `semantic_search` MCP tool that the host can use automatically

In Codex and OpenCode, the same binary download and index seeding happen on the
first `semantic_search` call. Codex stores the downloaded binary in the
plugin's writable data directory rather than the read-only package cache.

Two shared skills are also available: `doctor` (health check) and `reindex`
(forced re-indexing). Claude exposes them as `/lumen:doctor` and
`/lumen:reindex`; the other hosts discover the same shared skill content
through their native skill systems.

The same `semantic_search`, `health_check`, and `index_status` MCP tools plus
the shared `doctor` and `reindex` skills are exposed through the Codex,
Cursor, and OpenCode surfaces as well. The first `semantic_search` call seeds
or refreshes the index automatically.

## What you get

- **Semantic vector search** — Claude finds relevant functions, types, and
  modules by meaning, not keyword matching
- **Auto-indexing** — indexes on session start, only re-processes changed files
  via Merkle tree diffing
- **Incremental updates** — re-indexes only what changed; large codebases
  re-index in seconds after the first run
- **12 language families** — Go, Python, TypeScript, JavaScript, Svelte, Rust,
  Ruby, Java, PHP, C/C++, C#, Dart
- **Git worktree support** — worktrees share index data automatically; a new
  worktree seeds from a sibling's index and only re-indexes changed files,
  turning minutes of embedding into seconds
- **Zero cloud** — embeddings stay on your machine; no data leaves your network
- **Ollama and LM Studio** — works with either local embedding backend

## How it works

Lumen sits between your codebase and Claude as an MCP server. When a session
starts, it walks your project and builds a **Merkle tree** over file hashes:
only changed files get re-chunked and re-embedded. Each file is split into
semantic chunks (functions, types, methods) using Go's native AST or tree-sitter
grammars for other languages. Chunks are embedded and stored in **SQLite +
sqlite-vec** using cosine-distance KNN for retrieval.

```
Files → semantic chunks → vector embeddings → SQLite/sqlite-vec → KNN search
```

When Claude needs to understand code, it calls `semantic_search` instead of
reading entire files. The index is stored outside your repo
(`~/.local/share/lumen/<hash>/index.db`). Git worktrees from the same repository
use one collection for a compatible model, vector-storage, and chunking profile;
non-Git projects use private collections. Different profiles never collide.

## Benchmarks

Lumen is evaluated using **bench-swe**: a SWE-bench-style harness that runs
Claude on real GitHub bug-fix tasks and measures cost, time, output tokens, and
patch quality — with and without Lumen. All results are reproducible: raw JSONL
streams, patch diffs, and judge ratings are committed to this repository.

**Key results** — 9 runs across 9 languages, hard difficulty, real GitHub
issues (`ordis/jina-embeddings-v2-base-code`, Ollama):

| Language   | Cost Reduction | Time Reduction | Output Token Reduction  | Quality        |
| ---------- | -------------- | -------------- | ----------------------- | -------------- |
| Rust       | **-39%**       | **-34%**       | **-31%** (18K → 12K)    | Poor (both)    |
| JavaScript | **-33%**       | **-53%**       | **-66%** (14K → 5K)     | Perfect (both) |
| TypeScript | **-27%**       | **-33%**       | **-64%** (5K → 1.8K)    | Good (both)    |
| PHP        | **-27%**       | **-34%**       | **-59%** (1.9K → 0.8K)  | Good (both)    |
| Ruby       | **-24%**       | **-11%**       | -9% (6.1K → 5.6K)       | Good (both)    |
| Python     | **-20%**       | **-29%**       | **-36%** (1.7K → 1.1K)  | Perfect (both) |
| Go         | **-12%**       | -9%            | -10% (11K → 10K)         | Good (both)    |
| C++        | **-8%**        | -3%            | +42% (feature task)      | Good (both)    |
| Svelte     | **-26%**       | **-31%**       | **-26%** (4.0K → 3.0K)  | Poor (both)    |

**Cost was reduced in every language tested. Quality was maintained in every
task — zero regressions.** JavaScript and TypeScript show the most dramatic
efficiency gains: same quality fixes in half the time with two-thirds fewer
tokens. Even on tasks too hard for either approach (Rust, Svelte), Lumen cuts
the cost of failure by 26–39%.

See [docs/BENCHMARKS.md](docs/BENCHMARKS.md) for all 9 per-language deep dives,
judge rationales, and reproduce instructions.

## Supported languages

Supports **12 language families** with semantic chunking (10 benchmarked):

| Language         | Parser      | Extensions                                | Benchmark status                              |
| ---------------- | ----------- | ----------------------------------------- | --------------------------------------------- |
| Go               | Native AST  | `.go`                                     | Benchmarked: -12% cost, Good quality          |
| Python           | tree-sitter | `.py`                                     | Benchmarked: Perfect quality, -36% tokens     |
| TypeScript / TSX | tree-sitter | `.ts`, `.tsx`                             | Benchmarked: -64% tokens, -33% time           |
| JavaScript / JSX | tree-sitter | `.js`, `.jsx`, `.mjs`                     | Benchmarked: -66% tokens, -53% time           |
| Dart             | tree-sitter | `.dart`                                   | Benchmarked: -76% cost, -82% tokens, -79% time |
| Rust             | tree-sitter | `.rs`                                     | Benchmarked: -39% cost, -34% time             |
| Ruby             | tree-sitter | `.rb`                                     | Benchmarked: -24% cost, -11% time             |
| PHP              | tree-sitter | 