<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/logo/dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="docs/logo/light.svg">
    <img alt="HyperFrames" src="docs/logo/light.svg" width="300">
  </picture>
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/hyperframes"><img src="https://img.shields.io/npm/v/hyperframes.svg?style=flat" alt="npm version"></a>
  <a href="https://www.npmjs.com/package/hyperframes"><img src="https://img.shields.io/npm/dm/hyperframes.svg?style=flat" alt="npm downloads"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-Apache%202.0-blue.svg" alt="License"></a>
  <a href="https://nodejs.org"><img src="https://img.shields.io/badge/node-%3E%3D22-brightgreen" alt="Node.js"></a>
  <a href="https://discord.gg/fzbdWyjphr"><img src="https://img.shields.io/badge/Discord-Join-5865F2?logo=discord&logoColor=white" alt="Discord"></a>
</p>

<p align="center"><b>Write HTML. Render video. Built for agents.</b></p>

<p align="center">
  <a href="https://hyperframes.studio/studio?utm_source=github&utm_medium=readme">Studio</a> |
  <a href="https://hyperframes.heygen.com/quickstart?utm_source=github&utm_medium=readme">Quickstart</a> |
  <a href="https://hyperframes.heygen.com/examples?utm_source=github&utm_medium=readme">Showcase</a> |
  <a href="https://hyperframes.studio/?utm_source=github&utm_medium=readme">Playground</a> |
  <a href="https://hyperframes.heygen.com/catalog/blocks/data-chart?utm_source=github&utm_medium=readme">Catalog</a> |
  <a href="https://hyperframes.heygen.com/introduction?utm_source=github&utm_medium=readme">Docs</a> |
  <a href="https://discord.gg/fzbdWyjphr">Discord</a>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/f6ff9fae-f33d-4f68-bd54-f3ed4ba6473b" alt="The HyperFrames Studio app opening from the Dock: free for Mac, Windows and Linux" width="800">
</p>

<p align="center">
  <b>Download the desktop app:</b>
  <a href="https://hyperframes.studio/studio/download?os=mac&src=github-readme&utm_source=github&utm_medium=readme">macOS</a> ·
  <a href="https://hyperframes.studio/studio/download?os=windows&src=github-readme&utm_source=github&utm_medium=readme">Windows</a> ·
  <a href="https://hyperframes.studio/studio/download?os=deb&src=github-readme&utm_source=github&utm_medium=readme">Linux (.deb)</a>
</p>

HyperFrames is a free, open-source framework for turning HTML, CSS, media, and seekable animations into deterministic MP4 videos. Use it locally with the CLI, from AI coding agents with skills, or as the rendering core behind hosted authoring workflows.

The [HyperFrames Studio app](https://hyperframes.heygen.com/studio-app) is free to use as well; its [Pro plan](https://hyperframes.studio/pricing) adds HeyGen's top video, image, voice and music models.

Using Claude Code, Codex, Cursor, or another coding agent? Run `npx hyperframes skills update` once, then ask your agent to make a video.

## Quick Start

### With an AI coding agent

For Claude Code, install the versioned plugin:

```bash
claude plugin marketplace add heygen-com/hyperframes
claude plugin install hyperframes@hyperframes
```

To enable auto-update for the **hyperframes** marketplace, run `claude` in a
terminal in your project. In Claude Code's terminal UI, run `/plugin`, then select
**Marketplaces** → **hyperframes** → **Enable auto-update**. Afterward, use
`/hyperframes:hyperframes`. See the [plugin guide](docs/guides/plugins.mdx)
for Copilot, VS Code, Cursor, Gemini CLI, updates, and migration.

For standalone skills (including OpenCode), use:

```bash
npx skills add heygen-com/hyperframes
```

> The picker opens with nothing pre-selected — the **Core Skills** group is all you need; `/slideshow`, `/remotion-to-hyperframes`, `/reverse-any-video`, `/style-sampling` and `/figma` install on demand. Without the picker (a script or a CI job), `npx hyperframes skills update` installs exactly the core set, whereas `skills add --all` installs all 9 published skills. The six repo-internal skills under `.claude/skills` / `.agents/skills` are excluded by default. For the full published set use `npx hyperframes skills`.
>
> `skills add` resolves the skills.sh registry blob, which can lag `main` by hours. `npx hyperframes skills update` installs the skills from the release tag that matches your CLI version, so they match the CLI that runs them.

Run project-local installs from your video project's directory. From a HyperFrames
checkout, use `npx hyperframes skills update` for a global install instead: a
project-local installer target can overlap the tracked `skills/` source and
overwrite uncommitted edits. See [contributor setup](CONTRIBUTING.md#getting-started).

Try a prompt like:

> Using `/hyperframes`, create a 10-second product intro with a fade-in title, a background video, and subtle background music.

The skills teach agents the HyperFrames production loop: plan the video, write valid HTML, wire seekable animations, add media, lint, preview, and render. They work with Claude Code, Codex, Cursor, Gemini CLI, IBM Bob, and other coding agents that support skills.

## Skills

HyperFrames ships 9 skills. Make any video by asking for it; the `/hyperframes` skill carries the contract and the references (film, captions, overlays, motion, look). Read it first.

For standalone installation, default to the **core set** (`/hyperframes`, `/hyperframes-cli`, `/hyperframes-registry`, `/media-use`). `npx hyperframes skills update` installs exactly that from anywhere; the interactive picker (`npx skills add heygen-com/hyperframes`) lists it as the "Core Skills" group, nothing pre-selected. The picker is interactive-only — a non-interactive or agent run without `--skill` installs all 9. Use `npx skills add heygen-com/hyperframes --all` to install the complete published set deliberately (skips the picker), or `npx skills add heygen-com/hyperframes --skill <name>` for just one (bare name, no leading `/`).

Standalone installs stay lean after that: `npx hyperframes init` installs the **core set** only when it is missing and never touches a skill you already have (`npx hyperframes skills update` refreshes them, and never removes one); `/figma`, `/slideshow`, `/remotion-to-hyperframes` and `/reverse-any-video` install **on demand** with `npx hyperframes skills update <name>`. Nothing re-pulls the full set behind your back.

### Plugin packages

Plugins bundle the full skill catalog and use their agent's update manager.
`bun run package:agent-plugin` builds the committed portable ZIP, source metadata,
and SHA-256 checksum. See the [maintainer checklist](docs/contributing/agent-plugins.mdx).

### Upload to Codex

Build the upload-ready Codex plugin archive from the committed `HEAD` version of the manifest, brand assets, and skills:

```bash
bun run package:codex-plugin
```

This writes `dist/hyperframes-plugin.zip` with a `hyperframes/` root folder and fails if the archive exceeds Codex's 100 MB upload limit.

### Core set

| Skill                   | Use when                                                                                                                                                                                                                                                                                            |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/hyperframes`          | **Read first** for any request to make, edit, animate or render a video, motion graphic, captions or overlays with HyperFrames (HTML rendered to video). Holds the render contract and the work loop, and points to the references for format, motion, look, captions, whole films and storyboards. |
| `/hyperframes-cli`      | The HyperFrames CLI by job — scaffold, check, look at frames, edit the timeline, preview, render locally or in the cloud, publish, project history — plus reading its JSON and recovering from build or render failures.                                                                            |
| `/hyperframes-registry` | About 450 ready-made blocks and components installed as editable source — transitions, overlays, titles, kinetic type, captions, charts, maps, 3D, camera moves. Use before hand-building any named visual; also for `hyperframes add` and `catalog`.                                               |
| `/media-use`            | Get or make any media for a video — music, sound effects, images, icons, logos, voiceover, avatar and generated video, transcripts, cutouts, colour grades and looks — with HeyGen or free local tools, and mix placed audio. Also for footage that looks dark, flat or dull.                       |

### On demand

| Skill                      | Use when                                                                                                                                                                                              |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/figma`                   | Bring Figma into a video — rendered assets, brand tokens, components, storyboard frames as reconstructed motion, shaders and connector-assisted motion. Use when you paste a figma.com link.          |
| `/slideshow`               | A presentation, pitch deck or interactive deck — discrete slides, fragment reveals, branching, hotspot navigation, presenter mode with speaker notes. Output is a navigable deck, not a rendered MP4. |
| `/remotion-to-hyperframes` | Bringing existing video code or footage into HyperFrames (Remotion first; also Motion Canvas, Lottie, Three.js, canvas, other tools' renders), verified frame by frame.                               |
| `/reverse-any-video`       | Rebuilding any video file as an editable HyperFrames project (motion graphics, talking heads, live action, AI-generated footage), checked frame by frame against the original. HyperFrames Pro.       |
| `/style-sampling`          | Making a new episode on your topic in one of five proven styles: Collage Explainer, Finance Explainer, Animated Science Explainer, 3D Brand Explainer, 3D True Crime. HyperFrames Pro.                |

For visual design handoff workflows, see the [Claude Design guide](https://hyperframes.heygen.com/guides/design-tools?utm_source=github&utm_medium=readme#start-from-claude-design-or-open-design) and [Open Design guide](https://hyperframes.heygen.com/guides/design-tools?utm_source=github&utm_medium=readme#start-from-claude-design-or-open-design).

### Manually with the CLI

```bash
npx hyperframes init my-video
cd my-video
npx hyperframes preview      # preview in browser with live reload
npx hyperframes render       # render to MP4
```

**Requirements:** Node.js 22+, FFmpeg

## What You Can Build

Need ideas? Browse the [Showcase](https://hyperframes.heygen.com/examples?utm_source=github&utm_medium=readme) for finished videos you can watch, read, run, and remix.

- Product launch videos and feature announcements
- PR walkthroughs with animated code diffs, narration, and captions
- Data visualizations, chart races, and map animations
- Social videos with kinetic captions, overlays, and music
- Docs-to-video, PDF-to-video, and site-tour explainers
- Reusable motion graphics for automated content pipelines

## Frame.md

**frame.md — your design system, ready for video.**

Every brand has a `design.md`. None of them were written for a camera. `frame.md` is the missing translation layer: it takes your web-context design spec and inverts it for the frame — 