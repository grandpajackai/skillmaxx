# LogRocket Plugin for Claude Code

Connect Claude Code to [LogRocket](https://logrocket.com) to query session replays, metrics, issues, and user behavior using natural language — powered by the [LogRocket MCP Server](https://docs.logrocket.com/docs/mcp) and [Ask Galileo](https://docs.logrocket.com/docs/ask-galileo).

## What's Included

| Component | Description |
|-----------|-------------|
| **MCP Server** | Connects Claude Code to the LogRocket API |
| **Use LogRocket Skill** | Teaches your AI agent how to query LogRocket on your behalf |

### Available Tools

This plugin connects with `?toolsets=all`, so the full set of LogRocket MCP tools is enabled out of the box (including new toolsets as they're added):

| Tool | Toolset | Description |
|------|---------|-------------|
| `list_organizations` | _default_ | List the LogRocket organizations you can access |
| `list_projects` | _default_ | List the LogRocket projects within an organization |
| `use_logrocket` | `ask-galileo` | Run natural language queries against your LogRocket data, powered by Ask Galileo |
| `find_sessions` | `sessions` | Filter LogRocket sessions by user, URL, time range, events, and more |
| `watch_sessions` | `sessions` | Analyze or extract details from specific sessions |
| `get_network_entries` | `sessions` | Retrieve a session's network requests and responses as a HAR document |
| `build_metric` | `metrics` | Query LogRocket analytics data |
| `find_issues` | `issues` | List a project's issues, filtered by severity, triage status, type, and time range |

To restrict which tools are exposed, change the `toolsets` query parameter on the MCP server URL in `plugins/logrocket/.mcp.json` (e.g. `?toolsets=sessions,metrics`). See the [MCP tools docs](https://docs.logrocket.com/docs/mcp#tools) for details.

## Setup

1. Add the marketplace: `/plugin marketplace add logrocket/logrocket-claude-plugin`
2. Install the plugin: `/plugin install logrocket@logrocket`
3. Connect to the MCP server when prompted to authenticate.

## Example Prompts

- "User X reported a problem with checkout. Can you use LogRocket to watch their sessions and figure out the root cause?"
- "I'm about to work on the search feature — can you use LogRocket to help me understand how it's currently being used?"
- "Can you look at LogRocket for new issues from the past week, try to figure out their root causes, and then suggest which ones I can fix?"
- "Look at all commits from last week, and check LogRocket data to ensure they didn't introduce any regressions."
- "Use LogRocket to watch sessions and look at issues to figure out what is highest priority that I work on next."

## Learn More

- [LogRocket MCP Server Docs](https://docs.logrocket.com/docs/mcp)
- [Ask Galileo Docs](https://docs.logrocket.com/docs/ask-galileo)

## Privacy

This plugin connects to the LogRocket MCP server and handles user session data. See LogRocket's [Privacy Policy](https://logrocket.com/privacy/) for details on how data is collected and used.

## Validation

Validate the plugin structure using Claude Code's built-in validator:

```sh
claude plugin validate .
```
