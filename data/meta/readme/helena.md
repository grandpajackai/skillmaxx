# Helena for Grok

Bring [Helena](https://enrichlabs.ai), the first autonomous AI marketer, to
Grok. Helena learns your brand, builds a personalized marketing strategy, and
executes it 24/7—writing, publishing, optimizing, and reporting across SEO,
social, ads, and email.

## What this plugin installs

This plugin installs one remote, Streamable HTTP MCP server:

- Name: `helena`
- Endpoint: `https://agent.enrichlabs.ai/api/mcp`
- Tools: `send_turn_start`, `send_turn_status`

`send_turn_start` begins a Helena agent turn and returns a job ID. Poll
`send_turn_status` with that job ID until it finishes and returns final text,
a session ID, the tools Helena called, and any generated media assets. Pass
the returned session ID on later turns to continue the same conversation.

The plugin contains no executable scripts, hooks, downloaded binaries, or
embedded credentials.

## Authentication and access

Authenticate once from Grok's interactive `/mcps` screen (steps below).
The connection uses Enrich Labs OAuth 2.1 with PKCE. Sign in to Enrich Labs,
select a brand, and approve access. Grok handles the resulting OAuth
credentials; no API key is stored in this repository. Installing the plugin
or running `grok mcp doctor` alone does not complete this sign-in.

The shorter setup URL `https://enrichlabs.ai/mcp` is a reverse proxy to the
same MCP service at `https://agent.enrichlabs.ai/api/mcp`. This plugin uses the
canonical endpoint directly; both URLs reach the same server and OAuth flow.

MCP access requires an eligible Enrich Labs plan and completed account
onboarding. Each authorization is scoped to the selected Enrich Labs account.

## Data and actions

Requests sent through this plugin go to `agent.enrichlabs.ai`. Helena may read
the brand, product, campaign, and connected marketing data available to the
selected Enrich Labs account. Conversations and generated assets may be stored
in that account's Helena workspace according to the Enrich Labs terms and
privacy policy.

The `send_turn_start` tool is intentionally marked as potentially destructive because
Helena can use connected services to take real-world actions when the user asks.
Review the proposed action and require explicit approval before publishing
content, changing a storefront or campaign, contacting customers, or spending
money.

## Install from source

```bash
grok plugin install EnrichLabsAI/helena-grok-plugin --trust
```

After installation:

1. Start interactive `grok` and open `/mcps`.
2. Select `helena` and press `i` to authenticate.
3. In the browser, sign in to Enrich Labs, select your brand, and approve access.
4. Return to Grok and press `r` to refresh the MCP server list.

Then inspect its status with:

```bash
grok mcp doctor helena
```

A successful check reports a healthy connection and discovers the two tools.
Grok documents the authentication controls in its
[MCP guide](https://github.com/xai-org/grok-build/blob/main/crates/codegen/xai-grok-pager/docs/user-guide/07-mcp-servers.md).

### If Helena stays disconnected

- **Needs auth / 401 / handshake failed:** use `/mcps` → `helena` → `i`.
  Grok's diagnostic command and headless runs can fail without opening the
  browser. Retrying those commands does not authorize the connection. Finish
  the interactive sign-in first, then use the same Grok home for headless runs.
- **Previously connected, now refresh fails:** authenticate again from `/mcps`.
  An expired or already-used refresh token cannot be recovered by retrying it.
- **403 / onboarding or plan required:** follow the response's Enrich Labs link
  to finish onboarding or choose an eligible plan, then retry. Reinstalling the
  plugin does not change account eligibility.

## License

Apache-2.0
