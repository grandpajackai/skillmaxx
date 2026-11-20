# SkillMaxx Carousel Generator

Free, local 1080×1350 PNG and animated MP4 carousel generator for Instagram, LinkedIn, and X.

Reads only committed nightly test data (`src/_data/reports.json`, `src/_data/weeks.json`, `src/_data/latestRows.json`, `data/skills.json`, `data/meta/meta.json`) and renders HTML/CSS slides with bundled `Inter` and `JetBrains Mono` fonts via headless Chromium. With `--animate` (requires `ffmpeg` + Python `playwright`), records deterministic 30fps `1080×1350` H.264 (`yuv420p`) MP4 slides, final-frame PNG fallbacks, and a stitched `preview.mp4`. Never posts or queues to Buffer.

## Usage

```bash
python3 growth/carousels/generate.py --format all --out /workspace/carousels-samples --zip
python3 growth/carousels/generate.py --format v2 --animate --out /workspace/carousels-samples --zip
python3 growth/carousels/generate.py --format news --date 2026-11-20 --out /tmp/carousels
python3 growth/carousels/generate.py --format leaderboard --out /tmp/carousels
```
