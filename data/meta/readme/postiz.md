<p align="center">
  <img src="assets/logo.svg" alt="Postiz" width="96" />
</p>

<p align="center">
  <strong>Schedule posts with agents to:</strong><br />
  <a href="https://postiz.com/chatgpt">ChatGPT</a> ·
  <a href="https://postiz.com/claude">Claude</a> ·
  <a href="https://postiz.com/claude-cowork">Claude Cowork</a> ·
  <a href="https://postiz.com/claude-code">Claude Code</a> ·
  <a href="https://postiz.com/codex">Codex</a> ·
  <a href="https://postiz.com/cursor">Cursor</a> ·
  <a href="https://postiz.com/openclaw">OpenClaw</a> ·
  <a href="https://postiz.com/hermes">Hermes Agent</a> ·
  <a href="https://postiz.com/grok-bot">Grok Bot</a> ·
  <a href="https://postiz.com/grok-build">Grok Build</a> ·
  <a href="https://postiz.com/muse">Muse</a> ·
  <a href="https://postiz.com/perplexity-computer">Perplexity Computer</a> ·
  <a href="https://postiz.com/nanoclaw">nanoclaw</a> ·
  <a href="https://postiz.com/paperclip">Paperclip</a> ·
  <a href="https://postiz.com/mcp">MCP Server</a> ·
  <a href="https://postiz.com/agent">AI Agents CLI</a>
</p>

## Install as a skill

```bash
npx skills add gitroomhq/postiz-agent
```

### Claude Code plugin

```bash
/plugin marketplace add gitroomhq/postiz-agent
/plugin install postiz@postiz-agent
```

### Grok Build plugin

Postiz is listed in the [xAI plugin marketplace](https://github.com/xai-org/plugin-marketplace) — install it from the marketplace inside Grok Build. This repo also carries its own `.grok-plugin/plugin.json` manifest and `.grok-plugin/marketplace.json` catalog, so it can be added as a marketplace source directly.

The Grok plugin also bundles the hosted Postiz MCP server (`https://mcp.postiz.com/mcp-oauth-dynamic`) via the `mcpServers` field in `.grok-plugin/plugin.json` — you'll be asked to sign in to Postiz on first connection; no token or local install needed. The Claude Code and Cursor plugins are skill/CLI-only and do not register an MCP server.

### Cursor plugin

This repo ships a [Cursor plugin](https://cursor.com/docs/reference/plugins) manifest at `.cursor-plugin/plugin.json`.

- **From the marketplace / Customize panel:** open **Customize** in the Cursor sidebar, find **postiz**, and select **Install** (project or user scope).
- **Local install (development):**

  ```bash
  git clone https://github.com/gitroomhq/postiz-agent.git
  ln -s "$(pwd)/postiz-agent" ~/.cursor/plugins/local/postiz
  ```

  then restart Cursor or run **Developer: Reload Window**.

The plugin exposes the `postiz` skill, which drives the `postiz` CLI (the CLI handles media uploads, which is required for image/video posts). Make sure the CLI is installed (`npm install -g postiz`) and authenticated (`postiz auth:login` or `export POSTIZ_API_KEY=...`) before asking the agent to post.

### Gemini CLI extension

This repo is a [Gemini CLI extension](https://geminicli.com/docs/extensions/) (`gemini-extension.json` at the root) and is indexed in the [extensions gallery](https://geminicli.com/extensions/browse/).

```bash
gemini extensions install https://github.com/gitroomhq/postiz-agent
```

It installs the `postiz` skill and the hosted Postiz MCP server (`https://mcp.postiz.com/mcp-oauth-dynamic`). Gemini CLI opens a browser to sign in to Postiz on first use; run `/mcp auth postiz` to re-authenticate. The skill drives the `postiz` CLI for media uploads, so install it with `npm install -g postiz` for image or video posts.

### Qwen Code

Qwen Code installs Claude Code marketplaces directly, so no separate manifest is needed:

```bash
qwen extensions install gitroomhq/postiz-agent:postiz
```

### DeepSeek Harness plugin

This repo ships a [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness) (`dsh`) bundle at [`plugins/dsh-postiz`](plugins/dsh-postiz). It connects the agent to the hosted Postiz MCP server and registers a `postiz` workflow skill.

```bash
dsh plugin --profile web add "github:gitroomhq/postiz-agent#path:/plugins/dsh-postiz"
export POSTIZ_API_KEY=your-api-key   # Postiz → Settings → Developers → Public API
dsh web
```

The Postiz tools then appear as `mcp__postiz__*` (`integrationList`, `integrationSchema`, `schedulePostTool`, ...). Self-hosted instances override `baseUrl` on the `postiz` row. See the [plugin README](plugins/dsh-postiz/README.md) for configuration.

# Postiz CLI

**Social media automation CLI for AI agents** - Schedule posts across 28+ platforms programmatically.

The Postiz CLI provides a command-line interface to the Postiz API, enabling developers and AI agents to automate social media posting, manage content, and handle media uploads across platforms like Twitter/X, LinkedIn, Reddit, YouTube, TikTok, Instagram, Facebook, and more.

---

## Installation

### From npm (Recommended)

```bash
npm install -g postiz
# or
pnpm install -g postiz
```

---

## Authentication

### Option 1: OAuth2 (Recommended)

Authenticate using the device flow — no client ID or secret needed:

```bash
postiz auth:login
```

This will:
1. Display a one-time code in your terminal
2. Open your browser to authorize
3. Automatically save credentials to `~/.postiz/credentials.json`

```bash
# Check current auth status (verifies credentials are still valid)
postiz auth:status

# Remove stored credentials
postiz auth:logout
```

#### Self-Hosting the Auth Server

By default, `postiz auth:login` uses the hosted auth server at `cli-auth.postiz.com`. If you want to self-host the OAuth2 device flow server, follow the guide in [`server/SERVER.md`](./server/SERVER.md).

### Option 2: API Key

```bash
export POSTIZ_API_KEY=your_api_key_here
```

**Optional:** Custom API endpoint

```bash
export POSTIZ_API_URL=https://your-custom-api.com
```

> **Note:** OAuth2 credentials take priority over the API key when both are present.

---

## Commands

### Discovery & Settings

**List all connected integrations**
```bash
postiz integrations:list
postiz integrations:list --group "customer-id"
```

Returns integration IDs, provider names, and metadata. Use `--group` to return only the channels assigned to a specific group (customer).

**List all groups (customers)**
```bash
postiz integrations:groups
```

Returns all groups (customers) for your organization as `{id, name}`. Use a group's `id` with `integrations:list --group` to filter channels.

**Get integration settings schema**
```bash
postiz integrations:settings <integration-id>
```

Returns character limits, required settings, and available tools for fetching dynamic data.

**Trigger integration tools**
```bash
postiz integrations:trigger <integration-id> <method-name>
postiz integrations:trigger <integration-id> <method-name> -d '{"key":"value"}'
```

Fetch dynamic data like Reddit flairs, YouTube playlists, LinkedIn companies, etc.

**Examples:**
```bash
# Get Reddit flairs
postiz integrations:trigger reddit-123 getFlairs -d '{"subreddit":"programming"}'

# Get YouTube playlists
postiz integrations:trigger youtube-456 getPlaylists

# Get LinkedIn companies
postiz integrations:trigger linkedin-789 getCompanies

# Find a LinkedIn company page to tag, by its exact vanity name
postiz integrations:trigger linkedin-789 mention -d '{"query":"microsoft"}'
```

---

### Creating Posts

**Simple scheduled post**
```bash
postiz posts:create -c "Content" -s "2024-12-31T12:00:00Z" -i "integration-id"
```

**Draft post**
```bash
postiz posts:create -c "Content" -s "2024-12-31T12:00:00Z" -t draft -i "integration-id"
```

**Post with media**
```bash
postiz posts:create -c "Content" -m "img1.jpg,img2.jpg" -s "2024-12-31T12:00:00Z" -i "integration-id"
```

**Post with comments** (each comment can have its own media)
```bash
postiz posts:create \
  -c "Main post" -m "main.jpg" \
  -c "First comment" -m "comment1.jpg" \
  -c "Second comment" -m "comment2.jpg,comment3.jpg" \
  -s "2024-12-31T12:00:00Z" \
  -i "integration-id"
```

**Multi-platform post**
```bash
postiz posts:create -c "Content" -s "2024-12-31T12:00:00Z" -i "twitter-id,linkedin-id,facebook-id"
```

**Platform-specific settings**
```bash
postiz posts:create \
  -c "Content" \
  -s "2024-12-31T12:00:00Z" \
  --settings '{"subreddit":[{"value":{"subreddit":"programming","title":"Post Title","type":"text"}}]}' \
  -i "reddit-id"
```

**Complex post from JSON file**
```bash
postiz posts:create --json post.json
```

**Options:**
- `-c, --content` - Post/comment content (use multiple times for posts with comments)
- `-s, --date` - Schedule date in ISO 8601 format (REQUIRED)
- `-t, --type` - Post type: "schedule" or "draft" (default: "schedule")
- `-m, --media` - Comma-separated media URLs for corresponding `-c`
- `-i, --integrations` - Comma-separated integration IDs (required)
- `-d, --delay` - Delay between comments in minutes (default: 0)
- `--settings` - Platform-specific settings as JSON string
- `-j, --json` - Path to JSON file with full post structure
- `--shortLink` - Use short links (default: true)

---

### Managing Posts

**List posts**
```bash
postiz posts:list
postiz posts:list --startDate "2024-01-01T00:00:00Z" --endDate "2024-12-31T23:59:59Z"
postiz posts:list --customer "customer-id"
```

Defaults to last 30 days to next 30 days if dates not specified. Each returned post includes its current `settings` (returned as a JSON string — `JSON.parse` it). The intended workflow is `posts:list` (read current settings) → `posts:settings` (patch them).

**Delete post**
```bash
postiz posts:delete <post-id>
```

**Change post status (draft ↔ schedule)**
```bash
postiz posts:status <post-id> --status draft
postiz posts:status <post-id> --status schedule
```

Move a scheduled post back to a draft, or promote a draft into the publishing queue. Switching to `draft` also terminates any workflow that's already running for the post, so it won't publish. Switching to `schedule` queues the post for publishing at its stored date.

**Update a post's provider-specific settings**
```bash
postiz posts:settings <post-id> --settings '{"content_posting_method":"DIRECT_POST"}'
postiz posts:settings <post-id> --settings '{"subreddit":[{"value":{"subreddit":"/r/selfhosted","title":"My title","type":"self","is_flair_required":true}}]}'
```

Patches a post's settings server-side. The backend **merges** the object — only the keys you pass change, everything else is preserved — so pass a partial object, not the full settings blob. Only **DRAFT/QUEUE** (unpublished) posts can be updated; published posts are rejected. Pass the **main post id**, not a comment id. Do **not** include `__type` — the backend adds it automatically from the integration.

---

### Analytics

**Get platform analytics**
```bash
postiz analytics:platform <integration-id>
postiz analytics:platform <integration-id> -d 30
```

Returns metrics like followers, impressions, and engagement over time for a specific integration/channel. The `-d` flag specifies the number of days to look back (default: 7).

**Get post analytics**
```bash
postiz analytics:post <post-id>
postiz analytics:post <post-id> -d 30
```

Returns metrics like likes, comments, shares, and impressions for a specific published post.

**⚠️ If `analytics:post` returns `{"missing": true}`**, the post was published but the platform didn't return a usable post ID. You must resolve this before analytics will work:

```bash
# 1. List available content from the provider
postiz posts:missing <post-id>

# 2. Connect the correct content to the post
postiz posts:connect <post-id> --release-id "7321456789012345678"

# 3. Analytics will now work
postiz analytics:post <post-id>
```

---

### Connecting Missing Posts

Some platforms (e.g. TikTok) don't return a post ID immediately after publishing. The post's `releaseId` is set to `"missing"` and analytics won't work until resolved.

**List available content from the provider**
```bash
postiz posts:missing <post-id>
```

Returns an array of `{id, url}` items representing recent content from the provider. Returns an empty array if the provider doesn't support this feature.

**Connect a post to its publis