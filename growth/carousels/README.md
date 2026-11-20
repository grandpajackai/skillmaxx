# SkillMaxx Carousel Generator

Free, local 1080×1350 PNG carousel generator for Instagram, LinkedIn, and X.

Reads only committed nightly test data (`src/_data/reports.json`, `src/_data/weeks.json`, `src/_data/latestRows.json`, `data/skills.json`, `data/meta/meta.json`) and renders HTML/CSS slides with bundled `Inter` and `JetBrains Mono` fonts via headless Chromium. Never posts or queues to Buffer.

## Usage

```bash
python3 growth/carousels/generate.py --format all --out /workspace/carousels-samples --zip
python3 growth/carousels/generate.py --format news --date 2026-11-20 --out /tmp/carousels
python3 growth/carousels/generate.py --format leaderboard --out /tmp/carousels
```
