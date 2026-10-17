# Mapbox Agent Skills

**Comprehensive Agent Skills** that teach AI assistants how to build fast, beautiful, secure Mapbox applications across **Web, iOS, Android, and Flutter** platforms. Covers performance optimization, cartographic design, framework integration, platform migration, search integration, geospatial operations, navigation, and security best practices.

## Quick Start

### Codex Plugin Local Testing

This repository includes a Codex plugin manifest at `plugins/mapbox/.codex-plugin/plugin.json` and a repo marketplace at `.agents/plugins/marketplace.json`.

Codex marketplaces currently expect a plugin subdirectory such as `plugins/mapbox`. To avoid maintaining a second tracked copy of every skill, keep editing the root `skills/` directory and generate the local plugin package before testing:

```bash
npm run build:codex-plugin
codex plugin marketplace add .
codex plugin marketplace list
```

Then restart Codex and install the `mapbox` plugin from the `Mapbox Agent Skills` marketplace.

The generated `plugins/mapbox/skills/` and `plugins/mapbox/.mcp.json` files are ignored by git.

### Open Plugins (Cursor, Codex, GitHub Copilot, Claude Code)

This repository conforms to the [Open Plugins specification](https://open-plugins.com/), making it installable in any conformant tool - Cursor, Codex, GitHub Copilot, Claude Code, and more.

Add the marketplace source:

```
/plugin marketplace add mapbox/mapbox-agent-skills
```

Then install the plugin:

```
/plugin install mapbox
```

### Claude Plugin (Claude Code)

Install as a Claude Code plugin to get skills and MCP servers in one step:

```
/plugin marketplace add mapbox/mapbox-agent-skills
```

Then install the plugin:

```
/plugin install mapbox
```

This adds all Mapbox skills and connects the `mapbox`, `mapbox-devkit`, and `mapbox-docs` MCP servers automatically.

### Skills CLI

Install all Mapbox Agent Skills:

```bash
npx skills add mapbox/mapbox-agent-skills
```

Install specific skills:

```bash
npx skills add mapbox/mapbox-agent-skills --skill mapbox-web-performance-patterns
```

List available skills:

```bash
npx skills add mapbox/mapbox-agent-skills --list
```

> **💡 Pro tip:** These skills work great on their own, but they're even more powerful when combined with the [Mapbox MCP DevKit Server](https://github.com/mapbox/mcp-devkit-server). Skills provide the expertise (performance patterns, design principles), while MCP tools provide the actions (create styles, generate previews). Together, they enable complete workflows from design to deployment.

## What are Agent Skills?

Agent Skills are folders containing instructions and resources that AI assistants (like Claude Code, Cursor, GitHub Copilot) can discover and use to perform tasks more effectively. Unlike tools (which provide actions) or prompts (which provide workflows), skills provide **domain expertise** - the "know-how" that helps AI make informed decisions.

Think of skills as giving your AI assistant a specialized education in Mapbox development best practices.

## Available Skills

**Platform Coverage:**

- 🌐 **Web**: React, Vue, Svelte, Angular, Next.js (Mapbox GL JS)
- 📱 **iOS**: Swift, SwiftUI, UIKit (Maps SDK for iOS)
- 📱 **Android**: Kotlin, Jetpack Compose, View system (Maps SDK for Android)
- 📱 **Flutter**: Dart (Maps SDK for Flutter, iOS and Android)

---

### 🗺️ mapbox-geospatial-operations

**Expert guidance on choosing between offline geometric tools and routing APIs for geospatial operations.**

Helps AI assistants select the right tool based on problem type (geometric vs routing), accuracy requirements, and performance needs. Features the "as the crow flies" vs "as the crow drives" decision framework.

**Use when:**

- Deciding between offline calculations and API calls
- Calculating distances (straight-line vs road distance)
- Checking if points are within an area
- Creating travel-time zones vs distance buffers
- Optimizing geospatial operations for performance
- Understanding when to use routing vs geometry

**Key topics:**

- Decision framework: geometric operations vs routing APIs
- Distance calculations (crow flies vs crow drives)
- Proximity and containment checks
- Area and shape operations
- Routing and navigation patterns
- Clustering and optimization
- Hybrid approaches (combining tools)
- Common anti-patterns to avoid
- Performance and scale considerations

**Tool categories covered:**

- Offline geometric: distance, bearing, buffer, centroid, area, containment
- Routing APIs: directions, matrix, optimization, isochrone, map matching

[View skill →](./skills/mapbox-geospatial-operations/SKILL.md)

---

### 🔍 mapbox-search-integration

**Complete workflow for implementing Mapbox search in applications from discovery to production.**

Guides AI assistants through the entire search integration process: asking discovery questions, selecting the right product, implementing with best practices, and avoiding common pitfalls. Embodies collective knowledge from the Mapbox search team and customer learnings.

**Use when:**

- User needs to add search to their app
- Implementing location search or geocoding
- Need to ask the right questions about requirements
- Want production-ready search implementation
- Avoiding common integration mistakes

**Key workflow:**

1. **Discovery questions** - What to ask users (POIs? Addresses? Geographic scope? Platform?)
2. **Product selection** - Search Box API vs Geocoding API, SDK vs direct API
3. **Implementation patterns** - Complete code examples for web, iOS, Android
4. **Best practices** - Debouncing, session tokens, error handling, UX patterns
5. **Common pitfalls** - What goes wrong and how to avoid it

**Covers all platforms:**

- Web (Mapbox Search JS React/Web/Core, Vue, Angular, Next.js)
- iOS (Search SDK for iOS with UISearchController integration)
- Android (Search SDK for Android with SearchView integration)
- Node.js (Mapbox Search JS Core)

**Best practices from "the good parts":**

- ✅ Debouncing (prevent API spam)
- ✅ Session token management (cost optimization)
- ✅ Geographic filtering (better results)
- ✅ Error handling (all failure cases)
- ✅ Mobile UX (touch targets, keyboards)
- ✅ Accessibility (keyboard nav, ARIA)
- ✅ Caching strategies (high-volume apps)
- ✅ Token security (proper scoping)

[View skill →](./skills/mapbox-search-integration/SKILL.md)

---

### 🔍 mapbox-search-patterns

**Expert guidance on choosing the right search tool and parameters for geocoding, POI search, and location discovery.**

Helps AI assistants select between search_and_geocode, category_search, and reverse_geocode tools, and optimize parameters like proximity, bbox, country, limit, and more.

**Use when:**

- Choosing between search tools (specific names vs categories)
- Setting up geocoding or POI search
- Optimizing search parameters for accuracy
- Implementing "near me" searches
- Building autocomplete functionality
- Troubleshooting search results

**Key topics:**

- Tool selection decision matrix (brands vs categories vs coordinates)
- Parameter guidance (proximity, bbox, country, limit, types, ETA)
- Common patterns ("near me", route-based search, multilingual)
- Anti-patterns to avoid (missing proximity, wrong tool choice)
- Performance optimization (minimizing API calls, appropriate limits)
- Combining search with geospatial operations

**Search tools covered:**

- search_and_geocode_tool: Specific places, addresses, brands
- category_search_tool: Generic categories, plural queries
- reverse_geocode_tool: Coordinates to addresses

[View skill →](./skills/mapbox-search-patterns/SKILL.md)

---

### 🔄 mapbox-maplibre-migration

**Migration guide between Mapbox GL JS and MapLibre GL JS in both directions.**

Covers the fork history, API compatibility (~95% identical), token handling, style differences, and feature parity. Helps developers migrate in either direction or use both libraries together.

**Use when:**

- Migrating from Mapbox to MapLibre (or vice versa)
- Evaluating which library to use
- Understanding API compatibility
- Switching tile sources
- Combining MapLibre rendering with Mapbox APIs

**Key topics:**

- Fork history and license differences
- Package and import changes
- Token handling (Mapbox token vs no token)
- Style URL differences (mapbox:// vs OSM/custom)
- Feature parity comparison
- Plugin compatibility
- Migration in both directions
- When to choose each library
- Using both together

**Covers:**

- Step-by-step migration guides (both directions)
- API compatibility matrix (100% compatible vs minor differences)
- Common migration issues and solutions
- Decision guide (when to use which)
- Side-by-side code examples

[View skill →](./skills/mapbox-maplibre-migration/SKILL.md)

---

### ⚡ mapbox-web-performance-patterns

**Performance optimization patterns for building fast, efficient Mapbox GL JS web applications.**

Covers initialization waterfalls, bundle size, rendering performance, memory management, and web optimization. Patterns are prioritized by impact on user experience (Critical → High Impact → Optimization).

**Use when:**

- Optimizing map load time and time-to-interactive
- Reducing bundle size or implementing code splitting
- Debugging slow rendering or janky interactions
- Managing thousands of markers or large datasets
- Optimizing for web browsers and low-end hardware
- Preventing memory leaks in long-running applications

**Key topics:**

- Eliminating initialization waterfalls (parallel loading, data fetching)
- Bundle size optimization (code splitting)
- Marker performance (HTML vs Canvas vs Symbol layers, clustering)
- Data loading strategies (GeoJSON vs vector tiles, viewport-based loading)
- Event handling optimization (debouncing, throttling)
- Memory management (cleanup patterns, feature state)
- Web-specific optimizations (browser performance, touch events)

**Based on:** Performance principles from [Vercel's react-best-practices](https://vercel.com/blog/introducing-react-best-practices) and Mapbox GL JS patterns

[View skill →](./skills/mapbox-web-performance-patterns/SKILL.md)

---

### 🎨 mapbox-cartography

**Expert guidance on map design principles, color theory, visual hierarchy, typography, and cartographic best practices.**

**Use when:**

- Designing a new map style
- Choosing colors for map elements
- Making decisions about visual hierarchy
- Optimizing for specific use cases (navigation, data viz, etc.)
- Ensuring accessibility
- Creating themed maps (dark mode, vintage, etc.)

**Key topics:**

- Core cartographic principles (visual hierarchy, color theory)
- Typography best practices for maps
- Map context considerations (audience, platform, use case)
- Zoom level strategies
- Color palette templates
- Common mapping scenarios (restaurant finders, real estate, etc.)

[View skill →](./skills/mapbox-cartography/SKILL.md)

---

### 🔧 mapbox-web-integration-patterns

**Official integration patterns for Mapbox GL JS across popular web frameworks and Web Components.**

Covers React, Vue, Svelte, Angular, Next.js, and framework-agnostic Web Components (Custom Elements) with proper lifecycle management, token handling, and search integration. Based on Mapbox's `create-web-app` scaffolding tool.

**Use when:**

- Setting up Mapbox GL JS in a new web project
- Integrating Mapbox into a specific web framework
- Building framework-agnostic Web Components
- Creating reusable component libraries
- Adding Mapbox Search functionality
- Implementing proper cleanup and lifecycle management
- Debugging map initialization issues in web apps
- Converting between frameworks

**Key topics:**

- Framework-specific patterns (React hooks, Vue composition API, Svelte stores, Angular services)
- Web Components (Custom Elements, Shadow DOM, reactive attributes)
- Token management (environment variables across frameworks)
- Lifecycle management and cleanup (preventing memory leaks)
- Mapbox Search JS integration
- Common mistakes and how to avoid th