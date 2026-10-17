# Duende Agent Skills

A set of agent skills and specialized agents for Duende IdentityServer, Backend-for-Frontend (BFF), and identity/access management development. Covers OAuth 2.0, OpenID Connect, Duende, token management, ASP.NET Core authentication and authorization, and related skills needed to build production-grade identity infrastructure.

> ## Your Feedback 🗣️
>
> We would love to hear your feedback about these skills! What's working? What's not? What's missing?
>
> For questions, feedback, or community discussions, visit the [Duende Community](https://duende.link/community).

## Installation

You can use several AI coding assistants that support skills/agents.

### Claude Code (CLI)

[Official Docs](https://code.claude.com/docs/en/discover-plugins)

Run these commands inside the Claude Code CLI:

```
/plugin marketplace add DuendeSoftware/duende-skills
/plugin install duende-skills
```

To update:
```
/plugin marketplace update
```

> **Recommended:** Also install [dotnet-skills](https://github.com/Aaronontheweb/dotnet-skills) for general .NET development coverage:
> ```
> /plugin marketplace add Aaronontheweb/dotnet-skills
> /plugin install dotnet-skills
> ```

### GitHub Copilot CLI

[Official Docs](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing)

Copilot CLI reads the Claude-format marketplace in `.claude-plugin/`, so the same plugin installs directly:

```bash
copilot plugin marketplace add DuendeSoftware/duende-skills
copilot plugin install duende-skills@duende-skills
```

Or from inside an interactive session: `/plugin marketplace add DuendeSoftware/duende-skills` then `/plugin install duende-skills@duende-skills`.

### VS Code / VS Code Insiders (Preview)

[Official Docs](https://code.visualstudio.com/docs/copilot/customization/agent-plugins)

> Plugin support in VS Code is a preview feature and subject to change.

Enable plugins and register the marketplace in `settings.json`:

```jsonc
{
  "chat.plugins.enabled": true,
  "chat.plugins.marketplaces": ["DuendeSoftware/duende-skills"]
}
```

Then type `/plugins` in Copilot Chat (or use the `@agentPlugins` filter in Extensions) to browse and install `duende-skills`. You can also use `/plugin marketplace add DuendeSoftware/duende-skills` in chat.

### Cursor

[Official Docs](https://cursor.com/docs/plugins)

The repository ships a Cursor plugin manifest (`.cursor-plugin/plugin.json`). Once the plugin is listed on the [Cursor Marketplace](https://cursor.com/marketplace), install it from the Customize page / marketplace panel in Cursor. Until then, or for local use, either use `npx skills` (below) or copy/symlink a checkout to `~/.cursor/plugins/local/duende-skills` and run **Developer: Reload Window**.

### ChatGPT / Codex

```bash
codex plugin marketplace add DuendeSoftware/duende-skills
```

### Any agent via `npx skills` (OpenCode, Copilot, Cursor, Codex, Claude Code, and [many more](https://github.com/vercel-labs/skills#supported-agents))

[vercel-labs/skills](https://github.com/vercel-labs/skills) installs skills for whichever coding agents it detects:

```bash
# Install all Duende skills (interactive: pick agents and project/global scope)
npx skills add DuendeSoftware/duende-skills

# Global, non-interactive, for a specific agent
npx skills add DuendeSoftware/duende-skills --all -g -a opencode -y

# List what is available
npx skills add DuendeSoftware/duende-skills --list

# Update / remove later
npx skills update
npx skills remove duende-bff
```

> `npx skills` installs **skills only**. The two agents in `agents/` (`identity-server-specialist`, `oauth-oidc-specialist`) are installed by the plugin routes above, or manually (see OpenCode below).

### Install a single skill

Every skill is a self-contained folder under `skills/`, so you can install just the ones you need:

```bash
# Any agent (OpenCode, Copilot, Cursor, Codex, Claude Code, ...)
npx skills add DuendeSoftware/duende-skills --skill duende-bff
npx skills add DuendeSoftware/duende-skills --skill duende-bff --skill token-management

# Equivalent, pointing at the folder directly
npx skills add https://github.com/DuendeSoftware/duende-skills/tree/main/skills/duende-bff
```

Copilot CLI / VS Code plugins and the Claude Code plugin are installed as a whole (all skills). To pick individual skills for Copilot manually, copy the folder into `.github/skills/` (project) or `~/.copilot/skills/` (global).

### OpenCode

[Official Docs](https://opencode.ai/docs/skills)

Recommended: `npx skills add DuendeSoftware/duende-skills -a opencode -g` (see above).

<details>
<summary>Manual installation (skills + agents)</summary>

```bash
git clone https://github.com/DuendeSoftware/duende-skills.git /tmp/duende-skills

# Global installation (directory names must match frontmatter 'name' field)
mkdir -p ~/.config/opencode/skills ~/.config/opencode/agents
for skill_file in /tmp/duende-skills/skills/*/SKILL.md; do
  skill_dir=$(dirname "$skill_file")
  skill_name=$(grep -m1 "^name:" "$skill_file" | sed 's/name: *//')
  mkdir -p ~/.config/opencode/skills/$skill_name
  cp "$skill_file" ~/.config/opencode/skills/$skill_name/SKILL.md
  # Copy bundled resources (docs/, references/, etc.) if present
  find "$skill_dir" -mindepth 1 -maxdepth 1 -type d -exec cp -r {} ~/.config/opencode/skills/$skill_name/ \;
done
cp /tmp/duende-skills/agents/*.md ~/.config/opencode/agents/
```

</details>

### Manual (GitHub Copilot and others)

```bash
git clone https://github.com/DuendeSoftware/duende-skills.git /tmp/duende-skills
# Project-level
mkdir -p .github/skills && cp -r /tmp/duende-skills/skills/* .github/skills/
# Global
mkdir -p ~/.copilot/skills && cp -r /tmp/duende-skills/skills/* ~/.copilot/skills/
```

> **Recommended:** Also install [dotnet-skills](https://github.com/Aaronontheweb/dotnet-skills) for general .NET development coverage.

---

## Skills Library

### Identity & OAuth

| Skill                               | Description                                                                                                                                                                                                                                        |
|-------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `aspnetcore-authentication`         | ASP.NET Core authentication middleware — OIDC, JWT Bearer, cookies, schemes, external providers                                                                                                                                                    |
| `aspnetcore-authorization`          | ASP.NET Core authorization — policies, IAuthorizationHandler, scope-based API authz, minimal APIs                                                                                                                                                  |
| `claims-authorization`              | Claims-based authorization — policies, requirement handlers, resource-based authz, claims transformation                                                                                                                                           |
| `duende-bff`                        | Backend-for-Frontend security framework for SPAs — session management, API proxying, token management                                                                                                                                              |
| `identity-security-hardening`       | Security hardening — key rotation, HTTPS, CORS, CSP, rate limiting, token lifetime tuning                                                                                                                                                          |
| `identity-testing-patterns`         | Testing IdentityServer integrations — WebApplicationFactory, mock token issuance, protocol validation                                                                                                                                              |
| `identityserver-api-protection`     | Protecting APIs — JWT bearer authentication, reference token introspection, scope-based authorization, DPoP/mTLS proof-of-possession, local API auth                                                                                               |
| `identityserver-aspire`             | Aspire AppHost orchestration — dependency graphs, authority URL wiring, health checks, multi-instance                                                                                                                                              |
| `identityserver-configuration`      | IdentityServer host configuration — clients, resources, scopes, signing credentials, server-side sessions, client types (M2M, interactive, SPA), grant types, API Scopes vs API Resources vs Identity Resources, and client authentication methods |
| `identityserver-dcr`                | Dynamic Client Registration — endpoint setup, validation, software statements, client stores                                                                                                                                                       |
| `identityserver-deployment`         | Production deployment — reverse proxy configuration, data protection, health checks, distributed caching, OpenTelemetry, logging                                                                                                                   |
| `identityserver-duende-storage`     | Duende Storage (preview) — AddStorage/AddConfigurationStorage/AddOperationalStorage, storage instances, config admin APIs, data extension schemas, CLI migrations, EF Core migration                                                               |
| `identityserver-hosting-setup`      | Setting up and hosting IdentityServer — DI registration, middleware pipeline, hosting patterns, license configuration, ASP.NET Identity integration                                                                                                |
| `identityserver-key-management`     | Cryptographic signing keys — automatic key management, data protection at rest, static key configuration, multi-instance deployment                                                                                                                |
| `identityserver-saml`               | SAML 2.0 Identity Provider — service provider registration, SSO/SLO flows, claim mappings, extensibility, production stores                                                                                                                       |
| `identityserver-sessions-providers` | Server-side sessions, session management/querying, inactivity timeout, dynamic identity providers, CIBA                                                                                                                                            |
| `identityserver-spaces`             | Spaces (preview) — multi-tenancy with isolated config/operational data per space, Duende.Spaces setup, ISpaceAdmin, origin/path resolution, issuer rules                                                                                           |
| `identityserver-stores`             | Persistent stores — EF Core configuration/operational stores, migrations, custom implementations                                                                                                                                                   |
| `identityserver-token-lifecycle`    | Token types, refresh token management, token exchange (RFC 8693), extension grants, IProfileService claims, lifetime best practices                                                                                                                |
| `identityserver-token-security`     | Advanced token security — DPoP, 