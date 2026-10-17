# Greptile for Claude Code

The official [Greptile](https://greptile.com) plugin for Claude Code.

This repository is a Claude Code plugin marketplace. Add it directly:

```
/plugin marketplace add greptileai/claude-plugin
/plugin install greptile@greptile-claude-plugin
```

The plugin gives Claude Code two ways to work with Greptile:

- the **Greptile MCP server**, for reading and resolving review results and for searching your knowledge base and coding patterns
- the **Greptile CLI**, for reviewing your working branch before a pull request exists

Both authenticate over OAuth against your Greptile account. There is no API key to create and nothing to install — the CLI ships with the plugin, so it needs no npm or Homebrew install, only Node on your machine.

See [`plugins/greptile`](./plugins/greptile) for setup, commands, and the full tool list.
