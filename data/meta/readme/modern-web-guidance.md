<p align="center">
  <img src="https://github.com/GoogleChrome/modern-web-guidance/raw/main/.github/img/modern-web-guidance.svg" alt="Modern Web Guidance Logo" width="150" />
</p>

# Modern Web Guidance

[Modern Web Guidance](https://developer.chrome.com/docs/modern-web-guidance) is a set of skills that embed web platform expertise, best practices, and browser compatibility data directly into your coding agents. It helps to steer your coding agents away from legacy patterns, and instead toward solutions that harness the power and capabilities of the modern web platform.

*Supported by the Google Chrome team, the Microsoft Edge team, and the web development community.*

> [!NOTE]
> This is a **preview release** of Modern Web Guidance. We're actively adding new content and we [welcome contributions or feedback on GitHub](https://github.com/GoogleChrome/modern-web-guidance-src).

<!-- <LIKE A DEMO VIDEO LOOP OR SOMETHING?> -->

## <img src="https://github.com/GoogleChrome/modern-web-guidance/raw/main/.github/img/terminal.svg" width="24" height="24" style="vertical-align: middle; margin-right: 4px;"> Quickstart

```shell
npx modern-web-guidance@latest install
```

This command runs an interactive wizard to install Modern Web Guidance. See [Alternative Installation Methods](#-alternative-installation-methods) below.

#### Try it out (without installing)

```shell
# Search for relevant guides
npx modern-web-guidance@latest search "animate a dialog modal backdrop"

# Retrieve a guide by ID
npx modern-web-guidance@latest retrieve "animate-to-from-top-layer"
```

## <img src="https://github.com/GoogleChrome/modern-web-guidance/raw/main/.github/img/lightbulb.svg" width="24" height="24" style="vertical-align: middle; margin-right: 4px;"> Why?

Coding agents often default to older patterns because LLM training data contains vast amounts of legacy code. This often leads them to generate bloated JavaScript for tasks that now have native, high-performance web platform solutions.

Even if a model knows an API exists, it often lacks the density of real-world, modern implementation patterns required for production-ready code.

**Modern Web Guidance bridges this gap.** Our skill's CLI returns targeted, expert-curated guidelines directly into your agent's context window, focusing on:
* **Modern Browser APIs**: Helping models correctly structure APIs they frequently misuse.
* **Performance & Accessibility**: Preferring platform-level APIs that can be optimized by the browser and include built-in accessibility affordances.
* **Responsible Fallbacks**: Guiding models to use sensible, lightweight fallbacks instead of heavy polyfills or legacy libraries.

## <img src="https://github.com/GoogleChrome/modern-web-guidance/raw/main/.github/img/package.svg" width="24" height="24" style="vertical-align: middle; margin-right: 4px;"> What's Included?

We cover the past several years of the web platform's new features, all the way up to the cutting edge. The guides are **designed to be token-efficient**; we run evals enabling us to prune lowest-common-denominator content that models already know.

### Core Disciplines

<table width="100%" style="border-collapse: collapse; border: none;">
  <tr style="border: none;">
    <td width="33%" valign="top" style="border: none; padding: 6px;">
      <h4>🎨 User Experience</h4>
      <p style="font-size: 0.9em; line-height: 1.4;">Smooth visual states (View Transitions, entry/exit animations, parallax scroll, CSS <code>scrollbar-color</code>).</p>
    </td>
    <td width="33%" valign="top" style="border: none; padding: 6px;">
      <h4>📐 CSS Layout</h4>
      <p style="font-size: 0.9em; line-height: 1.4;">Modern layout systems (container queries, <code>subgrid</code>, modern color spaces like <code>oklch</code>, text-wrap tuning, and line-height trimming).</p>
    </td>
    <td width="33%" valign="top" style="border: none; padding: 6px;">
      <h4>⚡ Performance</h4>
      <p style="font-size: 0.9em; line-height: 1.4;">Speed optimizations (instant preloading, Interaction to Next Paint (INP) diagnostics, and scheduling tasks via <code>scheduler.yield</code>).</p>
    </td>
  </tr>
  <tr style="border: none;">
    <td width="33%" valign="top" style="border: none; padding: 6px;">
      <h4>📝 Forms & UI</h4>
      <p style="font-size: 0.9em; line-height: 1.4;">Native components (Anchor Positioning for tooltips, Popover API, dialogs, <code>:user-invalid</code> validation, and auto-sizing fields).</p>
    </td>
    <td width="33%" valign="top" style="border: none; padding: 6px;">
      <h4>♿ Accessibility</h4>
      <p style="font-size: 0.9em; line-height: 1.4;">Important considerations (screen reader and keyboard operability, content navigation and discoverability).</p>
    </td>
    <td width="33%" valign="top" style="border: none; padding: 6px;">
      <h4>🤖 Built-in AI</h4>
      <p style="font-size: 0.9em; line-height: 1.4;">Local client models (native translation, summarization, and language detection APIs).</p>
    </td>
  </tr>
</table>

_View an example:_ [the `navigation-drawer` guide](https://github.com/GoogleChrome/modern-web-guidance/blob/main/skills/modern-web-guidance/guides/overlays/navigation-drawer.md).

<!-- INJECT_SKILL_COVERAGE_START -->
#### The full list

<details>
<summary><strong>217 modern web features</strong></summary>

### CSS & Layout (123 features)

| | | |
| :--- | :--- | :--- |
| [::backdrop](https://web-platform-dx.github.io/web-features-explorer/features/backdrop/) | [content-visibility](https://web-platform-dx.github.io/web-features-explorer/features/content-visibility/) | [overscroll-behavior](https://web-platform-dx.github.io/web-features-explorer/features/overscroll-behavior/) |
| [::file-selector-button](https://web-platform-dx.github.io/web-features-explorer/features/file-selector-button/) | [contrast-color()](https://web-platform-dx.github.io/web-features-explorer/features/contrast-color/) | [prefers-color-scheme media query](https://web-platform-dx.github.io/web-features-explorer/features/prefers-color-scheme/) |
| [::placeholder](https://web-platform-dx.github.io/web-features-explorer/features/placeholder/) | [Cross-document view transitions](https://web-platform-dx.github.io/web-features-explorer/features/cross-document-view-transitions/) | [prefers-contrast media query](https://web-platform-dx.github.io/web-features-explorer/features/prefers-contrast/) |
| [::selection](https://web-platform-dx.github.io/web-features-explorer/features/selection/) | [currentColor](https://web-platform-dx.github.io/web-features-explorer/features/currentcolor/) | [prefers-reduced-motion media query](https://web-platform-dx.github.io/web-features-explorer/features/prefers-reduced-motion/) |
| [:dir()](https://web-platform-dx.github.io/web-features-explorer/features/dir-pseudo/) | [Custom highlights](https://web-platform-dx.github.io/web-features-explorer/features/highlight/) | [progress()](https://web-platform-dx.github.io/web-features-explorer/features/progress-function/) |
| [:has()](https://web-platform-dx.github.io/web-features-explorer/features/has/) | [Custom properties](https://web-platform-dx.github.io/web-features-explorer/features/custom-properties/) | [Relative colors](https://web-platform-dx.github.io/web-features-explorer/features/relative-color/) |
| [:host-context()](https://web-platform-dx.github.io/web-features-explorer/features/host-context/) | [display animation](https://web-platform-dx.github.io/web-features-explorer/features/display-animation/) | [rem](https://web-platform-dx.github.io/web-features-explorer/features/rem/) |
| [:is()](https://web-platform-dx.github.io/web-features-explorer/features/is/) | [Element-scoped view transitions](https://web-platform-dx.github.io/web-features-explorer/features/view-transitions-element-scoped/) | [resize (CSS property)](https://web-platform-dx.github.io/web-features-explorer/features/resize/) |
| [:modal](https://web-platform-dx.github.io/web-features-explorer/features/modal/) | [em unit](https://web-platform-dx.github.io/web-features-explorer/features/em-unit/) | [revert](https://web-platform-dx.github.io/web-features-explorer/features/revert-value/) |
| [:not()](https://web-platform-dx.github.io/web-features-explorer/features/not/) | [field-sizing](https://web-platform-dx.github.io/web-features-explorer/features/field-sizing/) | [revert-rule](https://web-platform-dx.github.io/web-features-explorer/features/revert-rule/) |
| [:nth-child() of &lt;selector>](https://web-platform-dx.github.io/web-features-explorer/features/nth-child-of/) | [filter](https://web-platform-dx.github.io/web-features-explorer/features/filter/) | [Scroll marker target pseudo-classes](https://web-platform-dx.github.io/web-features-explorer/features/scroll-marker-targets/) |
| [:placeholder-shown](https://web-platform-dx.github.io/web-features-explorer/features/placeholder-shown/) | [flex-wrap: balance](https://web-platform-dx.github.io/web-features-explorer/features/flexbox-flex-wrap-balance/) | [Scroll method promises](https://web-platform-dx.github.io/web-features-explorer/features/scroll-promises/) |
| [:user-valid and :user-invalid](https://web-platform-dx.github.io/web-features-explorer/features/user-pseudos/) | [Flexbox](https://web-platform-dx.github.io/web-features-explorer/features/flexbox/) | [Scroll snap](https://web-platform-dx.github.io/web-features-explorer/features/scroll-snap/) |
| [:where()](https://web-platform-dx.github.io/web-features-explorer/features/where/) | [font-size](https://web-platform-dx.github.io/web-features-explorer/features/font-size/) | [Scroll snap events](https://web-platform-dx.github.io/web-features-explorer/features/scroll-snap-events/) |
| [@function](https://web-platform-dx.github.io/web-features-explorer/features/function/) | [font-size-adjust](https://web-platform-dx.github.io/web-features-explorer/features/font-size-adjust/) | [scroll-axis-lock](https://web-platform-dx.github.io/web-features-explorer/features/scroll-axis-lock/) |
| [@scope](https://web-platform-dx.github.io/web-features-explorer/features/scope/) | [Forced colors](https://web-platform-dx.github.io/web-features-explorer/features/forced-colors/) | [Scroll-driven animations](https://web-platform-dx.github.io/web-features-explorer/features/scroll-driven-animations/) |
| [@starting-style](https://web-platform-dx.github.io/web-features-explorer/features/starting-style/) | [Gradient interpolation](https://web-platform-dx.github.io/web-features-explorer/features/gradient-interpolation/) | [scroll-initial-target](https://web-platform-dx.github.io/web-features-explorer/features/scroll-initial-target/) |
| [@supports](https://web-platform-dx.github.io/web-features-explorer/features/supports/) | [Gradients](https://web-platform-dx.github.io/web-features-explorer/features/gradients/) | [scroll-target-group](https://web-platform-dx.github.io/web-features-explorer/features/scroll-target-group/) |
| [accent-color](https://web-platform-dx.github.io/web-features-explorer/features/accent-color/) | [Grid](https://web-platform-dx.github.io/web-features-explorer/features/grid/) | [scrollbar-color](https://web-platform-dx.github.io/web-features-explorer/features/scrollbar-color/) |
| [Active view transition](https://web-platform-dx.github.io/web-features-explorer/features/active-view-transition/) | [Grid lanes](https://web-platform-dx.github.io/web-features-explorer/features/grid-lanes/) | [scrollbar-gutter](https://web-platform-dx.github.io/web-features-explorer/features/scrollbar-gutter/) |
| [Alt text for generated content](https://web-platform-dx.github.io/web-features-explorer/features/alt-text-generated-content/) | [image-set()](https://web-platform-dx.github.io/web-features-explorer/features/image-set/) | [scrollbar-width](https://web-platform-dx.github.io/web-features-explorer/features/scrollbar-width/) |
| [Anchor position container queries](https://web-platform-dx.github.io/web-features-explorer/features/container-a